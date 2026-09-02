"""Groq API transport for every LLM call in the system, replacing the local
Ollama HTTP calls that fact_extraction.py and lpu_classification.py used to
make directly.

ONLY the transport changes. Prompts, JSON parsing, the grounding check and
comparative-fact matching are all untouched - callers still hand this module a
prompt string and get the model's raw text response back, exactly as
_call_ollama() did, so the swap is invisible above this layer.

The API key comes from the GROQ_API_KEY environment variable and is never
hardcoded, never logged, and never written to any data file.

Rate limiting is the substantive difference from a local model. A local Ollama
had no quota - it was only ever slow. A hosted API has hard per-minute and
per-day caps, so this module:

  1. Reads the x-ratelimit-* headers Groq returns on EVERY response and keeps
     them in module-level state shared by all callers, so decomposition and
     classification throttle against one budget rather than each assuming it
     has the whole thing.
  2. Throttles PROACTIVELY: as remaining requests/tokens approach zero it
     sleeps until the reset window rather than sprinting into a 429.
  3. On a 429 anyway, waits exactly as long as the response says to
     (retry-after, or x-ratelimit-reset-*), not a guessed backoff.
  4. Raises GroqRateLimited after persistent 429s so callers can degrade
     gracefully (the single-fact fallback) instead of stalling the pipeline.

Everything here is stdlib urllib for the same reason the rest of the project
is: no new dependency, and the request shape is a single JSON POST.
"""
import json
import os
import threading
import time
import urllib.error
import urllib.request

from .config import (
    GROQ_BASE_URL,
    GROQ_MAX_ATTEMPTS,
    GROQ_MODEL,
    GROQ_RATE_LIMIT_SAFETY_MARGIN,
    GROQ_TIMEOUT_SECONDS,
)

API_KEY_ENV_VAR = "GROQ_API_KEY"


class GroqError(RuntimeError):
    """Any non-retryable Groq failure (missing key, auth, malformed request)."""


class GroqRateLimited(GroqError):
    """Raised when rate limiting persists across every attempt. Callers should
    degrade (e.g. fact_extraction's single-fact fallback) rather than stall."""


class _RateLimitState:
    """Last-seen rate-limit budget, shared process-wide. Groq reports the
    remaining allowance on every response, so the cheapest way to avoid a 429
    is to believe those numbers and slow down before hitting zero."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.remaining_requests: int | None = None
        self.remaining_tokens: int | None = None
        self.reset_requests_seconds: float = 0.0
        self.reset_tokens_seconds: float = 0.0
        self.limit_requests: int | None = None
        self.limit_tokens: int | None = None

    def update(self, headers) -> None:
        with self._lock:
            self.remaining_requests = _as_int(headers.get("x-ratelimit-remaining-requests"), self.remaining_requests)
            self.remaining_tokens = _as_int(headers.get("x-ratelimit-remaining-tokens"), self.remaining_tokens)
            self.limit_requests = _as_int(headers.get("x-ratelimit-limit-requests"), self.limit_requests)
            self.limit_tokens = _as_int(headers.get("x-ratelimit-limit-tokens"), self.limit_tokens)
            self.reset_requests_seconds = _as_duration(
                headers.get("x-ratelimit-reset-requests"), self.reset_requests_seconds)
            self.reset_tokens_seconds = _as_duration(
                headers.get("x-ratelimit-reset-tokens"), self.reset_tokens_seconds)

    def sleep_if_nearly_exhausted(self) -> float:
        """Sleeps until the budget resets if we're within the safety margin of
        running out, and returns how long it slept. This is the proactive half
        of the strategy: a 429 costs a full round-trip plus its retry-after,
        so it is strictly cheaper to pause voluntarily just before the wall."""
        with self._lock:
            waits = []
            if self.remaining_requests is not None and self.remaining_requests <= GROQ_RATE_LIMIT_SAFETY_MARGIN:
                waits.append(self.reset_requests_seconds)
            if self.remaining_tokens is not None and self.remaining_tokens <= 0:
                waits.append(self.reset_tokens_seconds)
            wait = max(waits) if waits else 0.0
        if wait > 0:
            print(f"  [groq] budget nearly exhausted (requests left="
                  f"{self.remaining_requests}, tokens left={self.remaining_tokens}) - "
                  f"pausing {wait:.1f}s until reset")
            time.sleep(wait)
        return wait

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "limit_requests": self.limit_requests,
                "remaining_requests": self.remaining_requests,
                "limit_tokens": self.limit_tokens,
                "remaining_tokens": self.remaining_tokens,
            }


def _as_int(raw, fallback):
    try:
        return int(raw)
    except (TypeError, ValueError):
        return fallback


def _as_duration(raw, fallback) -> float:
    """Groq expresses resets as durations like "7.66s", "2m59.56s" or "1h2m3s"
    rather than plain seconds, so parse the unit suffixes instead of assuming
    a number (treating "2m59s" as 2 seconds would defeat the whole point)."""
    if raw is None:
        return fallback
    text = str(raw).strip()
    try:
        return float(text)  # already-plain seconds
    except ValueError:
        pass
    total, number = 0.0, ""
    for char in text:
        if char.isdigit() or char == ".":
            number += char
        elif char in ("h", "m", "s"):
            if not number:
                continue
            value = float(number)
            total += value * {"h": 3600.0, "m": 60.0, "s": 1.0}[char]
            number = ""
    return total if total > 0 else fallback


rate_limit_state = _RateLimitState()


def api_key_present() -> bool:
    return bool(os.environ.get(API_KEY_ENV_VAR, "").strip())


def _request(prompt: str, temperature: float, timeout: int):
    api_key = os.environ.get(API_KEY_ENV_VAR, "").strip()
    if not api_key:
        raise GroqError(
            f"{API_KEY_ENV_VAR} is not set. Export it before running "
            "(the key is read from the environment and never stored in the repo)."
        )
    payload = json.dumps({
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        # Same temperature the Ollama path used, for the same reason: the
        # extraction/classification outputs are nested JSON schemas, and low
        # temperature buys schema compliance (not truthfulness).
        "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(
        GROQ_BASE_URL,
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    return urllib.request.urlopen(req, timeout=timeout)


def call_groq(prompt: str, temperature: float = 0.2, attempts: int = GROQ_MAX_ATTEMPTS,
              timeout: int = GROQ_TIMEOUT_SECONDS) -> str:
    """Returns the model's raw text response - the same contract the old
    _call_ollama() had, so callers' parsing logic is unchanged.

    Raises GroqRateLimited if rate limiting persists across every attempt, and
    GroqError for a missing key or other non-retryable failure. Transient
    network errors are retried with exponential backoff.
    """
    last_rate_limit_wait = 0.0
    for attempt in range(1, attempts + 1):
        rate_limit_state.sleep_if_nearly_exhausted()
        try:
            with _request(prompt, temperature, timeout) as resp:
                rate_limit_state.update(resp.headers)
                body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]

        except urllib.error.HTTPError as exc:
            rate_limit_state.update(exc.headers or {})
            if exc.code == 429:
                # Wait EXACTLY as long as the response instructs, rather than a
                # guessed backoff: retrying early just burns another request
                # against the same exhausted budget.
                wait = _as_duration(
                    (exc.headers or {}).get("retry-after"),
                    max(rate_limit_state.reset_requests_seconds, rate_limit_state.reset_tokens_seconds) or 5.0,
                )
                last_rate_limit_wait = wait
                if attempt < attempts:
                    print(f"  [groq] 429 rate limited - waiting {wait:.1f}s as instructed "
                          f"(attempt {attempt}/{attempts})")
                    time.sleep(wait)
                    continue
                raise GroqRateLimited(
                    f"rate limited on all {attempts} attempts (last wait {last_rate_limit_wait:.1f}s)"
                ) from exc
            if exc.code in (500, 502, 503, 504) and attempt < attempts:
                time.sleep(2.0 * (2 ** (attempt - 1)))
                continue
            detail = ""
            try:
                detail = exc.read().decode("utf-8")[:200]
            except Exception:  # noqa: BLE001 - diagnostics only, never fatal
                pass
            raise GroqError(f"Groq HTTP {exc.code}: {detail}") from exc

        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if attempt < attempts:
                print(f"  [groq] transport error ({exc}) - retry {attempt}/{attempts}")
                time.sleep(2.0 * (2 ** (attempt - 1)))
                continue
            raise GroqError(f"Groq unreachable after {attempts} attempts: {exc}") from exc

    raise GroqRateLimited(f"exhausted {attempts} attempts")

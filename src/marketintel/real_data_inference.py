"""Migrates the live ingestion path's (ingestion.py) k-NN reference pool from the
fabricated seed corpus onto the accumulated real-fact corpus itself, PER
DIMENSION rather than as a single all-or-nothing switch.

seed_inference.py's functions (nearest_neighbors, infer_relevance,
infer_categorical) already take their reference pool as an explicit
parameter - no code there needed to change. What lives here is the POLICY
layer deciding WHICH pool each of the 11 PESTLE/Porter's dimensions should
draw from, based on a direct coverage check (assess_dimension_coverage)
rather than assuming the real corpus is ready across the board.

Diagnosed via a real coverage check (CLAUDE.md's "Known gaps" has the exact
numbers): only 4 of 11 dimensions (political, economic, technological,
competitive_rivalry) currently have enough real facts, of BOTH polarities,
to support a reliable lookup. The other 7 - notably "environmental", which
had ZERO positive real examples at the time of the check, meaning any new
environmental-topic fact could never be inferred as positive polarity no
matter what it actually said - keep drawing from the fabricated corpus.
This is re-checked fresh on every ingestion run, so a dimension is expected
to graduate from fabricated to real as more real data accumulates, with no
code change required.

Scope (infer_scope_best_match) gets the same per-class blending treatment,
but with a much lower bar: its per-class-BEST-match mechanism (as opposed to
pooled k-NN voting) only needs a single good exemplar per class to work
correctly - not real breadth - so a class graduates to the real corpus as
soon as at least one real example of it exists (assess_scope_coverage),
rather than needing the same volume/polarity-balance bar as relevance.
"""
import numpy as np

from .config import (
    PESTLE_DIMS,
    PORTERS_DIMS,
    REAL_DATA_MIN_FACTS_FOR_GATE_RECALIBRATION,
    REAL_DATA_MIN_PER_POLARITY,
    REAL_DATA_MIN_TOTAL_PER_DIM,
    SCOPES,
    SUBCLUSTER_RELEVANCE_THRESHOLD,
)
from .seed_inference import calibrate_relevance_threshold, infer_categorical, infer_relevance, nearest_neighbors

DIM_NAMES = PESTLE_DIMS + PORTERS_DIMS
SCORE_FIELD_DIMS = [("pestle_scores", d) for d in PESTLE_DIMS] + [("porters_scores", d) for d in PORTERS_DIMS]


def assess_dimension_coverage(real_facts: list[dict]) -> dict[str, bool]:
    """For each of the 11 dimensions: True if the accumulated real-fact corpus
    has enough of its OWN data (REAL_DATA_MIN_TOTAL_PER_DIM facts scoring
    above SUBCLUSTER_RELEVANCE_THRESHOLD on that dimension, with at least
    REAL_DATA_MIN_PER_POLARITY of EACH polarity among them) to support a
    reliable k-NN lookup on that dimension. Recomputed fresh from whatever's
    accumulated so far every time this is called - never a one-time,
    hardcoded decision."""
    coverage = {}
    for score_field, dim in SCORE_FIELD_DIMS:
        relevant = [f for f in real_facts if f[score_field][dim] > SUBCLUSTER_RELEVANCE_THRESHOLD]
        if len(relevant) < REAL_DATA_MIN_TOTAL_PER_DIM:
            coverage[dim] = False
            continue
        pos = sum(1 for f in relevant if f["polarity"] == "positive")
        neg = sum(1 for f in relevant if f["polarity"] == "negative")
        coverage[dim] = pos >= REAL_DATA_MIN_PER_POLARITY and neg >= REAL_DATA_MIN_PER_POLARITY
    return coverage


def infer_hybrid(
    embedding: np.ndarray,
    real_news: list[dict],
    real_embeddings: np.ndarray,
    fabricated_news: list[dict],
    fabricated_embeddings: np.ndarray,
    dimension_coverage: dict[str, bool],
):
    """Returns (relevance, polarity, source_summary) for one new fact.

    relevance: computed against BOTH pools (each via its own independent k-NN
    lookup); each of the 11 dimensions takes its value from whichever pool
    dimension_coverage says is trustworthy for that dimension - a real,
    per-dimension blend, not one pool winning outright for the whole fact.

    polarity: a single categorical field, not naturally splittable per
    dimension - drawn from whichever pool "owns" this fact's own DOMINANT
    dimension (its highest real-pool relevance score, since that's the most
    directly-grounded signal for what the fact is actually about) is
    trustworthy for; falls back to the fabricated pool's polarity vote
    whenever the real pool is empty or the dominant dimension hasn't earned
    coverage yet.

    source_summary: which pool polarity came from and which dimensions came
    from which pool - for logging/spot-checking only, not used downstream.
    """
    real_relevance, real_polarity = None, None
    if len(real_news) > 0:
        top_idx_r, w_r = nearest_neighbors(embedding, real_embeddings)
        real_relevance = infer_relevance(real_news, top_idx_r, w_r)
        real_polarity = infer_categorical(real_news, top_idx_r, w_r, "polarity")

    top_idx_f, w_f = nearest_neighbors(embedding, fabricated_embeddings)
    fabricated_relevance = infer_relevance(fabricated_news, top_idx_f, w_f)
    fabricated_polarity = infer_categorical(fabricated_news, top_idx_f, w_f, "polarity")

    merged_relevance = {}
    dims_from_real, dims_from_fabricated = [], []
    for dim in DIM_NAMES:
        if dimension_coverage.get(dim) and real_relevance is not None:
            merged_relevance[dim] = real_relevance[dim]
            dims_from_real.append(dim)
        else:
            merged_relevance[dim] = fabricated_relevance[dim]
            dims_from_fabricated.append(dim)

    if real_relevance is not None:
        dominant = max(real_relevance.items(), key=lambda kv: kv[1])[0]
        if dimension_coverage.get(dominant):
            polarity, polarity_source = real_polarity, "real"
        else:
            polarity, polarity_source = fabricated_polarity, "fabricated"
    else:
        polarity, polarity_source = fabricated_polarity, "fabricated"

    source_summary = {
        "polarity_source": polarity_source,
        "dims_from_real": dims_from_real,
        "dims_from_fabricated": dims_from_fabricated,
    }
    return merged_relevance, polarity, source_summary


def assess_scope_coverage(real_facts: list[dict]) -> dict[str, bool]:
    """Per scope class: True if the real corpus has at least one example of
    it. infer_scope_best_match's per-class-BEST-match mechanism only needs a
    single good exemplar per class to work correctly (that's the whole point
    of it over pooled k-NN voting, which needs real breadth per class to
    avoid population-size bias) - so the bar here is simply "does at least
    one example exist," not a count threshold like the relevance/polarity
    checks above."""
    present = {f["scope"] for f in real_facts}
    return {scope: scope in present for scope in SCOPES}


def infer_scope_hybrid(
    embedding: np.ndarray,
    real_embeddings: np.ndarray,
    real_scope_indices: dict,
    fabricated_embeddings: np.ndarray,
    fabricated_scope_indices: dict,
    scope_coverage: dict[str, bool],
):
    """Per-class-best-match, blended: for each of the 7 scope classes, uses
    the real corpus's single best match if scope_coverage says that class is
    covered, otherwise the fabricated corpus's - then picks the overall
    highest-similarity winner across all classes regardless of which pool it
    came from, exactly like the original per-class-best-match mechanism
    except each class's candidate can now come from either pool."""
    sims_real = real_embeddings @ embedding if len(real_embeddings) > 0 else None
    sims_fab = fabricated_embeddings @ embedding

    best_scope, best_sim, best_source = None, -1.0, None
    for scope in SCOPES:
        if scope_coverage.get(scope) and sims_real is not None and scope in real_scope_indices:
            class_best = float(sims_real[real_scope_indices[scope]].max())
            source = "real"
        elif scope in fabricated_scope_indices:
            class_best = float(sims_fab[fabricated_scope_indices[scope]].max())
            source = "fabricated"
        else:
            continue
        if class_best > best_sim:
            best_sim, best_scope, best_source = class_best, scope, source
    return best_scope, best_sim, best_source


def choose_gate_threshold(real_facts: list[dict], fabricated_news: list[dict]):
    """Returns (threshold, source). The relevance GATE threshold itself
    (distinct from per-dimension relevance values above) is a single scalar
    cutoff - it switches to being calibrated from the real corpus's own
    relevance distribution only once there are enough facts
    (REAL_DATA_MIN_FACTS_FOR_GATE_RECALIBRATION) for a 5th-percentile
    estimate to be statistically stable; below that it stays calibrated from
    the fabricated corpus, same as before this migration."""
    if len(real_facts) >= REAL_DATA_MIN_FACTS_FOR_GATE_RECALIBRATION:
        return calibrate_relevance_threshold(real_facts), "real"
    return calibrate_relevance_threshold(fabricated_news), "fabricated"

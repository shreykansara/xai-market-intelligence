#!/usr/bin/env python3
"""
Explainable Market Intelligence Chatbot Engine
----------------------------------------------
Core backend module featuring:
1. VectorPlacementEngine: Maps user businesses into the 11-D strategic vector space (PESTLE + Porter)
   and computes Cosine Similarities against the 50-company benchmark dataset.
2. MarketKnowledgeBase: Loads 50_companies_analysis.json and GDELT enriched news records.
3. GroqOllamaProvider: Hybrid LLM interface supporting Groq API with local Ollama fallback.
4. BusinessEvaluator: Formats CVP statements adhering strictly to the standard template.
"""

import csv
import json
import math
import os
import re
import sys
import urllib.request
import urllib.parse
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.resolve()
COMPANIES_500_PATH = BASE_DIR / "500_companies_analysis.json"
COMPANIES_JSON_PATH = COMPANIES_500_PATH if COMPANIES_500_PATH.exists() else (BASE_DIR / "50_companies_analysis.json")
ENRICHED_CSV_PATH = BASE_DIR / "enriched_news_202601.csv"
ENV_PATH = BASE_DIR / ".env"


def load_dotenv():
    """Simple lightweight .env parser without external dependencies."""
    if ENV_PATH.exists():
        try:
            with open(ENV_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and v and v != "your_groq_api_key_here":
                            os.environ[k] = v
        except Exception as e:
            print(f"[DotEnv] Warning parsing .env: {e}")

load_dotenv()


def l2_normalize(vec: list) -> list:
    """L2 normalizes a float vector."""
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """Computes Cosine Similarity between two vectors of equal length."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


class VectorPlacementEngine:
    """
    Engine to embed user business descriptions into the 11-Dimensional Strategic Space
    and find Nearest-Neighbor benchmark companies.
    """
    
    STRATEGIC_CONCEPT_ANCHORS = {
        0: ["tariff", "sanction", "sanctions", "government", "policy", "trade war", "regulation", "state subsidy", "geopolitical", "ministry", "legislation", "bipartisan", "election", "diplomatic", "embargo", "parliament", "congress", "executive order", "state department", "customs duty"],
        1: ["inflation", "interest rate", "gdp", "recession", "central bank", "currency", "devaluation", "spending freeze", "capital cost", "monetary policy", "debt market", "fiscal", "purchasing power", "stock market", "financial crisis", "revenue dip", "price hike"],
        2: ["demographic", "lifestyle", "public health", "labor union", "workforce", "consumer trend", "brand perception", "boycott", "employment", "cultural", "societal", "community welfare", "household spending", "public sentiment"],
        3: ["ai", "artificial intelligence", "software", "automation", "semiconductor", "chip", "cloud", "cybersecurity", "r&d", "patent", "digital", "algorithm", "platform", "machine learning", "hardware", "microcontroller", "it infrastructure"],
        4: ["lawsuit", "court", "antitrust", "gdpr", "privacy", "compliance", "ftc", "sec", "litigation", "verdict", "patent infringement", "contract dispute", "liability", "statute", "legal penalty", "court ruling"],
        5: ["climate", "carbon", "emissions", "esg", "sustainability", "renewable", "green energy", "recycling", "pollution", "waste", "weather disaster", "ecological", "resource conservation", "environmental penalty"],
        6: ["startup", "new entrant", "barrier to entry", "capital requirement", "incumbent moat", "licensing barrier", "scale economies", "market entry", "new competitor", "setup cost", "entry barrier"],
        7: ["buyer", "customer leverage", "price sensitivity", "switching cost", "churn", "buyer discount", "pricing power", "customer choice", "client retention", "shopper demand", "buyer leverage"],
        8: ["supply chain", "supplier", "raw material", "shortage", "vendor price", "port congestion", "bottleneck", "shipping delay", "component cost", "freight transit", "logistics delay", "fabrication", "input cost"],
        9: ["substitute", "alternative product", "workaround", "obsolete", "competing replacement", "at-home alternative", "cannibalization", "disruptive tech", "replacement solution", "alternative adoption"],
        10: ["price war", "rivalry", "competitor", "market share", "freemium", "merger", "acquisition", "rival campaign", "consolidation", "head to head", "competitive battle", "race", "dominant player"]
    }

    @classmethod
    def compute_11d_vector(cls, text: str) -> list:
        """
        Computes an authentic 11-dimensional strategic vector (0.05 to 0.95) based on semantic concept activation.
        """
        if not text or not text.strip():
            return [0.05] * 11

        text_lower = text.lower()
        words = set(re.findall(r"\w+", text_lower))
        vector = []

        for dim_idx in range(11):
            anchors = cls.STRATEGIC_CONCEPT_ANCHORS.get(dim_idx, [])
            exact_matches = 0
            phrase_matches = 0

            for anchor in anchors:
                if " " in anchor:
                    if anchor in text_lower:
                        phrase_matches += 1
                else:
                    if anchor in words or anchor in text_lower:
                        exact_matches += 1

            total_signal = (phrase_matches * 2.0) + (exact_matches * 1.0)

            if total_signal == 0:
                score = 0.05
            elif total_signal == 1.0:
                score = 0.35
            elif total_signal == 2.0:
                score = 0.70
            elif total_signal == 3.0:
                score = 0.85
            else:
                score = min(0.95, round(0.85 + ((total_signal - 3.0) * 0.03), 2))

            vector.append(score)

        return vector

    @classmethod
    def compute_384d_text_embedding(cls, text: str, dim: int = 384) -> list:
        """Deterministic 384-D character/word n-gram text embedding."""
        if not text:
            return [0.0] * dim
        vec = [0.0] * dim
        words = re.findall(r"\w+", text.lower())
        for word in words:
            h = abs(int(math.sin(hash(word)) * 1000000)) % dim
            vec[h] += 1.0
            for i in range(len(word) - 2):
                ngram = word[i:i+3]
                h_ng = abs(int(math.sin(hash(ngram)) * 1000000)) % dim
                vec[h_ng] += 0.5
        return [round(x, 4) for x in l2_normalize(vec)]

    @classmethod
    def find_nearest_cvps(cls, user_cvp_text: str, companies_data: list, top_k: int = 4) -> list:
        """
        Computes 384-D text embedding for user's CVP and finds top-k companies with closest CVP embeddings.
        """
        user_cvp_384d = cls.compute_384d_text_embedding(user_cvp_text)
        results = []

        for comp in companies_data:
            comp_cvp_384d = comp.get("cvp_embedding_384d")
            if not comp_cvp_384d:
                comp_cvp_384d = cls.compute_384d_text_embedding(comp.get("cvp", ""))

            sim_cvp = cosine_similarity(user_cvp_384d, comp_cvp_384d)
            similarity_pct = round(max(0.0, min(1.0, sim_cvp)) * 100, 1)

            results.append({
                "id": comp.get("id"),
                "company": comp.get("company"),
                "sector": comp.get("sector"),
                "product_name": comp.get("product_name"),
                "similarity_pct": similarity_pct,
                "cvp": comp.get("cvp", ""),
                "strategic_11d": comp.get("strategic_embedding_11d", [0.5] * 11)
            })

        results.sort(key=lambda x: x["similarity_pct"], reverse=True)
        unique_results = []
        seen_names = set()
        for r in results:
            base_name = re.sub(r"\s*\(.*?\)", "", r.get("company", "")).strip().lower()
            if base_name not in seen_names:
                seen_names.add(base_name)
                unique_results.append(r)
            if len(unique_results) >= top_k:
                break
        return unique_results

    @classmethod
    def find_nearest_neighbors(cls, user_11d: list, user_384d: list, companies_data: list, top_k: int = 4) -> list:
        """
        Calculates similarity between user's business vector and all 500 benchmark companies.
        Returns top-k closest matches with similarity scores.
        """
        results = []
        for comp in companies_data:
            comp_11d = comp.get("strategic_embedding_11d", [0.5] * 11)
            comp_384d = comp.get("cvp_embedding_384d")
            if not comp_384d:
                comp_text = f"{comp.get('company', '')} {comp.get('sector', '')} {comp.get('cvp', '')}"
                comp_384d = cls.compute_384d_text_embedding(comp_text)

            sim_11d = cosine_similarity(user_11d, comp_11d)
            sim_384d = cosine_similarity(user_384d, comp_384d)

            # Combined Similarity score (70% strategic 11-D + 30% text 384-D)
            combined_sim = (sim_11d * 0.70) + (sim_384d * 0.30)
            similarity_pct = round(max(0.0, min(1.0, combined_sim)) * 100, 1)

            results.append({
                "id": comp.get("id"),
                "company": comp.get("company"),
                "sector": comp.get("sector"),
                "product_name": comp.get("product_name"),
                "similarity_pct": similarity_pct,
                "cvp": comp.get("cvp", f"For {comp.get('target_customer', '')} who {comp.get('statement_of_need', '')}, the {comp.get('product_name', '')} is a {comp.get('product_category', '')} that {comp.get('statement_of_key_benefit', '')}."),
                "strategic_11d": comp_11d,
                "key_pestle": comp.get("pestle", {}),
                "key_porters": comp.get("porters", {})
            })

        results.sort(key=lambda x: x["similarity_pct"], reverse=True)
        unique_results = []
        seen_names = set()
        for r in results:
            base_name = re.sub(r"\s*\(.*?\)", "", r.get("company", "")).strip().lower()
            if base_name not in seen_names:
                seen_names.add(base_name)
                unique_results.append(r)
            if len(unique_results) >= top_k:
                break
        return unique_results


class MarketKnowledgeBase:
    """Knowledge base holding 50 benchmark companies and enriched GDELT news records."""
    
    def __init__(self):
        self.companies = []
        self.news_records = []
        self.load_companies()
        self.load_news()

    def load_companies(self):
        if COMPANIES_JSON_PATH.exists():
            try:
                with open(COMPANIES_JSON_PATH, "r", encoding="utf-8") as f:
                    self.companies = json.load(f)
            except Exception as e:
                print(f"[KnowledgeBase] Error loading companies JSON: {e}")

    def load_news(self):
        if ENRICHED_CSV_PATH.exists():
            try:
                with open(ENRICHED_CSV_PATH, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    count = 0
                    for row in reader:
                        if count >= 200:  # Load top 200 sample news items into memory
                            break
                        self.news_records.append(row)
                        count += 1
            except Exception as e:
                print(f"[KnowledgeBase] Error loading news CSV: {e}")

    def get_company_by_name(self, name: str) -> dict:
        name_lower = name.lower()
        for c in self.companies:
            if name_lower in c.get("company", "").lower():
                return c
        return None

    def search_news(self, query: str, limit: int = 3) -> list:
        query_lower = query.lower()
        matches = []
        for r in self.news_records:
            headline = r.get("headline", "").lower()
            if any(q in headline for q in query_lower.split()):
                matches.append({
                    "headline": r.get("headline"),
                    "date": r.get("date"),
                    "source_link": r.get("source_link"),
                    "location": r.get("location_affected")
                })
                if len(matches) >= limit:
                    break
        return matches


class GroqOllamaProvider:
    """Hybrid LLM Provider supporting Groq API with local Ollama fallback."""

    def __init__(self, groq_api_key: str = None, ollama_url: str = "http://localhost:11434"):
        self.groq_api_key = groq_api_key or os.environ.get("GROQ_API_KEY", "")
        self.ollama_url = ollama_url

    def generate_response(self, system_prompt: str, user_prompt: str, chat_history: list = None) -> str:
        effective_groq_key = self.groq_api_key or os.environ.get("GROQ_API_KEY", "")
        # Try Groq API first if key is present
        if effective_groq_key and effective_groq_key != "your_groq_api_key_here":
            self.groq_api_key = effective_groq_key
            res = self._call_groq(system_prompt, user_prompt, chat_history=chat_history)
            if res:
                return self._clean_output(res)

        # Try Local Ollama fallback
        res = self._call_ollama(system_prompt, user_prompt, chat_history=chat_history)
        if res:
            return self._clean_output(res)

        # Fallback intelligent rule response
        return self._clean_output(self._rule_fallback_response(user_prompt, system_prompt))

    def _clean_output(self, text: str) -> str:
        """Strips markdown hashtags (#) and asterisks (*) for clean plain-text formatting."""
        if not text:
            return ""
        # Remove hashtags
        text = re.sub(r"#+\s*", "", text)
        # Remove asterisks
        text = text.replace("*", "")
        # Remove any leftover Groq note lines
        text = re.sub(r"💡?\s*(?:Pro Tip|Note):\s*To enable full unrestricted real-time LLM chat.*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"💡?\s*(?:Pro Tip|Note):\s*Use our settings menu to configure.*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"💡?\s*(?:Pro Tip|Note):\s*Provide your free Groq API key.*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"💡?\s*(?:Pro Tip|Note):\s*You can add your.*", "", text, flags=re.IGNORECASE)
        return text.strip()

    OBSOLETE_GROQ_MODELS = {
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "mixtral-8x7b-32768",
        "gemma-7b-it",
        "gemma2-9b-it"
    }

    DEFAULT_ACTIVE_GROQ_MODELS = [
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "llama-3.1-8b-instant",
        "qwen/qwen3.6-27b",
        "qwen/qwen3.8-27b",
        "groq/compound"
    ]

    def _get_active_groq_models(self) -> list:
        """Dynamically queries Groq API for active non-obsolete models, falling back to curated active list."""
        if not self.groq_api_key:
            return self.DEFAULT_ACTIVE_GROQ_MODELS

        url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {self.groq_api_key}",
            "Content-Type": "application/json"
        }
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models_data = data.get("data", [])
                active_ids = [
                    m["id"] for m in models_data 
                    if isinstance(m, dict) and "id" in m and m["id"] not in self.OBSOLETE_GROQ_MODELS
                ]
                if active_ids:
                    priority_order = [
                        "openai/gpt-oss-120b", 
                        "openai/gpt-oss-20b", 
                        "llama-3.1-8b-instant", 
                        "qwen/qwen3.6-27b", 
                        "qwen/qwen3.8-27b", 
                        "groq/compound"
                    ]
                    sorted_models = [m for m in priority_order if m in active_ids]
                    for m in active_ids:
                        if m not in sorted_models:
                            sorted_models.append(m)
                    return sorted_models
        except Exception as e:
            print(f"[GroqProvider] Dynamic model list fetch skipped: {e}")

        return self.DEFAULT_ACTIVE_GROQ_MODELS

    def _call_groq(self, system_prompt: str, user_prompt: str, chat_history: list = None) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        models_to_try = self._get_active_groq_models()

        messages = [{"role": "system", "content": system_prompt}]
        if chat_history and isinstance(chat_history, list):
            for msg in chat_history[-8:]:
                if isinstance(msg, dict) and msg.get("role") in ["user", "assistant"] and msg.get("content"):
                    messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_prompt})

        for model in models_to_try:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.4,
                "max_tokens": 1200
            }
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            try:
                req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    content = data["choices"][0]["message"]["content"].strip()
                    if content:
                        return content
            except Exception as e:
                print(f"[GroqProvider] Model {model} failed: {e}")
                continue
        return ""

    def _call_ollama(self, system_prompt: str, user_prompt: str, chat_history: list = None) -> str:
        url = f"{self.ollama_url}/api/chat"
        messages = [{"role": "system", "content": system_prompt}]
        if chat_history and isinstance(chat_history, list):
            for msg in chat_history[-8:]:
                if isinstance(msg, dict) and msg.get("role") in ["user", "assistant"] and msg.get("content"):
                    messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_prompt})

        payload = {
            "model": "llama3.2",
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0.4, "num_predict": 1000}
        }
        headers = {"Content-Type": "application/json"}
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"[OllamaProvider] Ollama call failed: {e}")
            return ""

    @staticmethod
    def _is_gibberish_token(w: str) -> bool:
        w_lower = w.lower()
        keyboard_mashes = {"asdf", "qwerty", "zxcv", "dfgh", "hjkl", "jkl", "qwer", "asdfg", "zxcvbn", "1234", "12345", "testtest", "asdfasdf", "asdfasdfasdf", "zxcvbnm"}
        if w_lower in keyboard_mashes:
            return True
        # Repeated pattern check (e.g. asdfasdf, abab, xyzxyz, testtest)
        if len(w_lower) >= 4 and re.search(r'(.{2,})\1', w_lower):
            return True
        # No vowels in words 4+ chars
        if len(w_lower) >= 4 and not re.search(r'[aeiouy]', w_lower):
            return True
        # Low character diversity in longer words
        if len(w_lower) >= 6 and len(set(w_lower)) <= 3:
            return True
        # 4+ consecutive consonants
        if re.search(r'[bcdfghjklmnpqrstvwxz]{4,}', w_lower):
            return True
        return False

    @staticmethod
    def check_query_intent(user_prompt: str) -> tuple:
        """
        Categorizes user query intent:
        Returns ('GIBBERISH' | 'OFF_TOPIC' | 'GREETING' | 'INAPPROPRIATE' | 'BUSINESS_QUERY', message_override_if_any)
        """
        raw = (user_prompt or "").strip()
        p_lower = raw.lower()

        if len(raw) < 2:
            return ('GIBBERISH', "Please ask a specific business strategy, CVP evaluation, or market risk query.")

        # 1. Inappropriate / Explicit Content Filter
        inappropriate_keywords = [
            "porn", "xxx", "sex", "erotic", "nsfw", "nude", "naked", "adult content",
            "gambling", "casino", "betting", "illegal", "drugs", "weed", "cocaine",
            "weapon", "bomb", "kill", "suicide", "hack", "exploit"
        ]
        if any(re.search(r'\b' + re.escape(kw) + r'\b', p_lower) for kw in inappropriate_keywords):
            return ('INAPPROPRIATE', "I am strictly configured as a professional AI Market Intelligence Assistant focused on legitimate business strategy, Customer Value Propositions, PESTLE forces, and competitive market dynamics. I cannot process explicit, adult, or illegal product queries.")

        # 2. Check for non-word keyboard mashing or random numbers
        words = re.findall(r'\b[a-zA-Z]+\b', p_lower)

        if not words and not any(char.isdigit() for char in raw):
            return ('GIBBERISH', "Please ask a specific business strategy, CVP evaluation, or market risk query.")

        # Check gibberish tokens
        gibberish_count = sum(1 for w in words if GroqOllamaProvider._is_gibberish_token(w))
        if words and (gibberish_count / len(words)) >= 0.3:
            return ('GIBBERISH', "I am strictly configured as an AI Market Intelligence Assistant. Please ask a relevant business strategy or CVP query regarding your market environment.")

        # Dictionary validation for short 1-3 token prompts to catch random non-English keyboard strings
        common_vocab = {
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you",
            "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one",
            "all", "would", "there", "their", "what", "so", "up", "out", "if", "about", "who", "get", "which", "go", "me", "when",
            "make", "can", "like", "time", "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some",
            "could", "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think", "also", "back",
            "after", "use", "two", "how", "our", "work", "first", "well", "way", "even", "new", "want", "because", "any", "these",
            "give", "day", "most", "us", "product", "business", "market", "risk", "strategy", "customer", "price", "pestle", "porter",
            "force", "value", "cvp", "sales", "revenue", "cost", "competitor", "peer", "lead", "app", "service", "company", "industry",
            "tech", "growth", "launch", "brand", "user", "help", "flipkart", "ebay", "amazon", "india", "lpu"
        }
        if len(words) <= 3 and not any(w in common_vocab for w in words):
            return ('GIBBERISH', "I am strictly configured as an AI Market Intelligence Assistant. Please ask a relevant business strategy or CVP query regarding your market environment.")

        # 3. Check simple greetings
        greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "greetings"}
        if p_lower in greetings or (len(words) <= 2 and words[0] in greetings):
            return ('GREETING', "Hello! I am your AI Market Intelligence Assistant. I am configured to help you evaluate your Customer Value Proposition (CVP), analyze PESTLE macro risks, assess Porter's 5 Forces, and benchmark against 500 industry leaders. How can I help you navigate your market strategy today?")

        # 4. Off-topic domain queries
        off_topic_patterns = [
            "capital of", "president of", "prime minister of", "weather in", "tell me a joke",
            "who wrote", "recipe for", "how to code", "write python code", "translate to",
            "who won", "score of", "movie review", "game rules", "what is 2+"
        ]
        if any(pat in p_lower for pat in off_topic_patterns):
            return ('OFF_TOPIC', "I am strictly configured to answer business strategy, CVP placement, PESTLE forces, and competitive market queries. Please ask a question related to your Customer Value Proposition or industry dynamics.")

        return ('BUSINESS_QUERY', "")

    def _rule_fallback_response(self, user_prompt: str, system_prompt: str = "") -> str:
        intent, override_msg = self.check_query_intent(user_prompt)
        if intent in ['GIBBERISH', 'OFF_TOPIC', 'GREETING', 'INAPPROPRIATE']:
            return override_msg

        prompt_lower = user_prompt.lower()
        target_entity = "your business"
        if "flipkart" in prompt_lower:
            target_entity = "Flipkart"

        # 1. PESTLE & Risk Intent
        if any(w in prompt_lower for w in ["pestle", "risk", "political", "economic", "social", "tech", "legal", "environment", "threat"]):
            return f"""Evaluating the macro-environment for {target_entity} reveals key strategic considerations across your 11-dimensional vector space:

Primary PESTLE Risk Factors:
- Economic Sensitivity: Consumer purchasing behavior is highly elastic. Cost fluctuations or inflation mean value retention and price transparency are critical.
- Social Proof & Trust: Customer adoption relies heavily on peer recommendations, transparent fulfillment, and brand reliability.
- Technological Infrastructure: High mobile usage requires fast load times, seamless checkout, and scalable digital support.

Strategic Mitigation:
1. Maintain transparent landed pricing to counter Economic buyer sensitivity.
2. Build strong customer guarantees and social proof mechanisms to strengthen Social trust.
3. Optimize mobile app responsiveness and data security to minimize technical churn."""

        # 2. Competitor / Buyer Power / Porter's Intent
        elif any(w in prompt_lower for w in ["buyer", "competitor", "rival", "porter", "force", "substitute", "supplier", "peer", "differentiate", "moat"]):
            return f"""Analyzing industry competition and force dynamics for {target_entity}:

Porter's 5 Forces Overview:
- Buyer Power: High. Customers have low switching costs and easy access to alternatives, making customer retention vital.
- Threat of Substitutes: Moderate to High. Generic alternatives exist, requiring clear differentiation in delivery speed, service quality, or pricing.
- Competitive Rivalry: Intense. Established peers compete on scale, requiring you to focus on operational speed and niche focus.

Recommended Countermeasures:
1. Differentiate your CVP by delivering superior speed, reliability, or hyper-local service that generalist peers cannot match.
2. Introduce loyalty loops or bundled value deals to increase buyer switching costs and boost customer lifetime value.
3. Diversify vendor and logistics partnerships to protect operating margins against supplier pricing pressure."""

        # 3. GTM / Launch Intent
        elif any(w in prompt_lower for w in ["go to market", "gtm", "launch", "pilot", "university", "campus", "lpu", "college", "growth"]):
            return f"""For a targeted go-to-market execution, focus on building hyper-local density before expanding:

Go-To-Market Blueprint for {target_entity}:
1. Hyper-Local Density: Target a single geographic hub or tight customer segment first. Achieve 35%+ penetration in your initial pilot before expanding.
2. Zero-Friction Onboarding: Eliminate setup friction with 1-click digital ordering or instant messaging integrations.
3. Peer Referral Loops: Leverage referral incentives where existing users bring new customers with mutual discounts.
4. Operational Speed: Maintain fast, reliable fulfillment to create a competitive moat against regional incumbents."""

        # 4. General Dynamic Response
        else:
            return f"""Based on your Customer Value Proposition and 384-dimensional vector placement, here is a strategic perspective on your question:

Key Business Focus Areas for {target_entity}:
- Value Proposition Alignment: Focus on clear customer pain points, ensuring your pricing and fulfillment match target customer expectations.
- Unit Economics & Execution: Prioritize customer retention and positive unit margins over broad, unprofitable customer acquisition.
- Strategic Risk Management: Monitor buyer price sensitivity and competitor movements closely to preserve market share.

How would you like to dive deeper into your PESTLE macro risks, Porter's competitive forces, or go-to-market tactics?"""


class BusinessEvaluator:
    """Formats exact Customer Value Proposition (CVP) statements and generates risk scorecards."""

    @staticmethod
    def format_cvp(target_customer: str, statement_of_need: str, product_name: str, product_category: str, statement_of_key_benefit: str) -> str:
        """
        Formats CVP strictly adhering to the standard template:
        For [target customer] who [statement of need], the [product name] is a [product category] that [statement of key benefit].
        """
        tc = target_customer.strip() or "target customers"
        sn = statement_of_need.strip() or "need effective market solutions"
        pn = product_name.strip() or "Our Product"
        pc = product_category.strip() or "innovative solution"
        kb = statement_of_key_benefit.strip() or "delivers superior value and performance"

        return f"For {tc} who {sn}, the {pn} is a {pc} that {kb}."

    @staticmethod
    def evaluate_revenue_events(events: list) -> dict:
        """
        Analyzes historical revenue time-series events (dips & spikes) to calculate PESTLE & Porter 5 Forces risk vectors.
        """
        axis_names = [
            'Political', 'Economic', 'Social', 'Technological', 'Legal', 'Environmental',
            'Threat of New Entrants', 'Buyer Power', 'Supplier Power', 'Threat of Substitutes', 'Competitive Rivalry'
        ]

        scores = [0.35] * 11
        event_impacts = []

        category_map = {
            'political': 0, 'economic': 1, 'social': 2, 'technological': 3, 'legal': 4, 'environmental': 5,
            'threat of new entrants': 6, 'entrants': 6,
            'buyer power': 7, 'buyer': 7,
            'supplier power': 8, 'supplier': 8,
            'threat of substitutes': 9, 'substitutes': 9,
            'competitive rivalry': 10, 'rivalry': 10
        }

        for ev in events:
            title = ev.get('event_title', '').strip()
            desc = ev.get('event_description', '').strip()
            cat = ev.get('category_tag', '').strip().lower()
            impact = ev.get('impact_type', 'dip').lower()
            change_str = str(ev.get('revenue_change', '10')).replace('%', '').replace('$', '').strip()

            try:
                change_val = abs(float(change_str))
            except ValueError:
                change_val = 10.0

            severity = min(0.35, max(0.05, change_val / 50.0))

            full_text = f"{title} {desc}"
            text_vector = VectorPlacementEngine.compute_11d_vector(full_text)
            target_idx = category_map.get(cat, None)

            if impact == 'dip':
                if target_idx is not None:
                    scores[target_idx] += severity * 1.5
                for idx in range(11):
                    scores[idx] += text_vector[idx] * severity * 0.4
                event_impacts.append({
                    "event": title or "Revenue Dip Event",
                    "impact": f"-{change_val}% Revenue Dip",
                    "primary_factor": axis_names[target_idx] if target_idx is not None else "Multi-Factor Market Shock"
                })
            else:
                if target_idx is not None:
                    scores[target_idx] = max(0.10, scores[target_idx] - severity * 0.8)
                for idx in range(11):
                    scores[idx] = max(0.10, scores[idx] - text_vector[idx] * severity * 0.2)
                event_impacts.append({
                    "event": title or "Revenue Spike Event",
                    "impact": f"+{change_val}% Revenue Growth",
                    "primary_factor": axis_names[target_idx] if target_idx is not None else "Market Opportunity"
                })

        clamped_scores = [round(min(0.95, max(0.12, s)), 2) for s in scores]

        return {
            "pestle_vector": clamped_scores[0:6],
            "porter_vector": clamped_scores[6:11],
            "11d_vector": clamped_scores,
            "event_impacts": event_impacts
        }


class TemporalClusterMatcher:
    """
    Parses date-indexed revenue time series data, detects significant sales dips/rises,
    and correlates them against market event clusters to filter verified relevant clusters vs noise.
    """

    SAMPLE_MARKET_CLUSTERS = [
        {
            "id": "cluster_pol_01",
            "period": "2025-Q1",
            "title": "Cross-Border Import Tariff Increase",
            "description": "Government enacted 18% import duty hike on textile and retail apparel imports.",
            "category": "Political",
            "axis_idx": 0
        },
        {
            "id": "cluster_sup_02",
            "period": "2025-Q2",
            "title": "Port Freight Congestion & Shipping Bottleneck",
            "description": "Major container shipping hub delays caused 4-week supply chain inventory shortages.",
            "category": "Supplier Power",
            "axis_idx": 8
        },
        {
            "id": "cluster_tech_03",
            "period": "2025-Q3",
            "title": "Direct-to-Consumer Mobile Checkout Release",
            "description": "Rolled out 1-click native checkout app reducing buyer abandon rates.",
            "category": "Technological",
            "axis_idx": 3
        },
        {
            "id": "cluster_riv_04",
            "period": "2025-Q1",
            "title": "Aggressive Competitor Freemium Launch",
            "description": "Market leader slashed subscription prices by 30% and introduced free tier.",
            "category": "Competitive Rivalry",
            "axis_idx": 10
        },
        {
            "id": "cluster_eco_05",
            "period": "2025-Q2",
            "title": "Corporate IT Procurement Spend Freeze",
            "description": "Macro-economic rate hikes led enterprise buyers to pause software renewals.",
            "category": "Economic",
            "axis_idx": 1
        },
        {
            "id": "cluster_noise_06",
            "period": "2025-Q4",
            "title": "Unrelated Regional Labor Union Negotiation",
            "description": "Local transit union negotiations occurred with zero impact on digital operations.",
            "category": "Social",
            "axis_idx": 2
        }
    ]

    @staticmethod
    def process_time_series(revenue_series: list) -> dict:
        """
        Input: list of dicts: [{'period': '2025-Q1', 'change_pct': -18.5, 'revenue': 120000}, ...]
        Returns:
            - analyzed_series: series tagged with dip/rise/stable
            - matched_clusters: clusters evaluated for temporal consistency (stored vs discarded)
            - pestle_vector: 6-D scores from stored clusters only
            - porter_vector: 5-D scores from stored clusters only
            - 11d_vector: 11-D scores
        """
        axis_names = [
            'Political', 'Economic', 'Social', 'Technological', 'Legal', 'Environmental',
            'Threat of New Entrants', 'Buyer Power', 'Supplier Power', 'Threat of Substitutes', 'Competitive Rivalry'
        ]

        scores = [0.35] * 11
        analyzed_series = []
        fluctuation_periods = {}

        for item in revenue_series:
            period = str(item.get('period', '')).strip()
            try:
                val = float(item.get('revenue', item.get('value', 0)))
            except (ValueError, TypeError):
                val = 0.0

            try:
                chg = float(item.get('change_pct', item.get('change', 0)))
            except (ValueError, TypeError):
                chg = 0.0

            label = item.get('label', '')

            trend = 'stable'
            if chg <= -5.0:
                trend = 'dip'
            elif chg >= 5.0:
                trend = 'spike'

            entry = {
                'period': period,
                'revenue': val,
                'change_pct': chg,
                'trend': trend,
                'label': label
            }
            analyzed_series.append(entry)
            if trend != 'stable':
                fluctuation_periods[period.lower()] = entry

        matched_clusters = []
        stored_clusters = []

        for cluster in TemporalClusterMatcher.SAMPLE_MARKET_CLUSTERS:
            c_period = cluster['period'].lower()
            fluc = fluctuation_periods.get(c_period)

            if not fluc:
                for period_key, f_data in fluctuation_periods.items():
                    if c_period in period_key or period_key in c_period:
                        fluc = f_data
                        break

            if fluc:
                trend = fluc['trend']
                chg_mag = abs(fluc['change_pct'])
                severity = min(0.40, max(0.10, chg_mag / 40.0))

                axis_idx = cluster['axis_idx']
                if trend == 'dip':
                    scores[axis_idx] += severity * 1.6
                else:
                    scores[axis_idx] = max(0.10, scores[axis_idx] - severity * 0.8)

                matched_item = {
                    **cluster,
                    "matched_period": fluc['period'],
                    "sales_impact": f"{fluc['change_pct']:+.1f}% Revenue {trend.upper()}",
                    "status": "VERIFIED_RELEVANT",
                    "stored": True,
                    "rationale": f"Consistent Temporal Match: Sales {trend} of {fluc['change_pct']:+.1f}% occurred in {fluc['period']} co-occurring with market event cluster."
                }
                matched_clusters.append(matched_item)
                stored_clusters.append(matched_item)
            else:
                matched_item = {
                    **cluster,
                    "matched_period": cluster['period'],
                    "sales_impact": "0.0% (No Sales Impact)",
                    "status": "UNCORRELATED_NOISE",
                    "stored": False,
                    "rationale": "Uncorrelated Noise: No significant sales dip or rise detected during this market cluster period. Discarded from intelligence base."
                }
                matched_clusters.append(matched_item)

        clamped_scores = [round(min(0.95, max(0.12, s)), 2) for s in scores]

        return {
            "analyzed_series": analyzed_series,
            "matched_clusters": matched_clusters,
            "stored_clusters": stored_clusters,
            "pestle_vector": clamped_scores[0:6],
            "porter_vector": clamped_scores[6:11],
            "11d_vector": clamped_scores
        }


class ChatbotEngine:
    """Main Orchestrator for the Market Intelligence Chatbot."""

    def __init__(self, groq_api_key: str = None):
        self.kb = MarketKnowledgeBase()
        self.llm = GroqOllamaProvider(groq_api_key=groq_api_key)

    def process_message(self, user_message: str, user_business_context: dict = None, groq_key_override: str = None, chat_history: list = None) -> dict:
        """
        Main entry point for processing chat queries.
        Returns a dict containing:
        - text: AI response string
        - nearest_neighbors: top 3-4 matched companies from the 50 dataset
        - user_11d_vector: 11-dimensional strategic scores
        - cvp_statement: formatted CVP if applicable
        """
        if groq_key_override:
            self.llm.groq_api_key = groq_key_override

        text_to_vectorize = user_message
        if user_business_context:
            if isinstance(user_business_context, dict):
                text_to_vectorize += " " + json.dumps(user_business_context)
            else:
                text_to_vectorize += " " + str(user_business_context)

        # 1. Compute 11-D Strategic Vector & 384-D Text Embedding
        user_11d = VectorPlacementEngine.compute_11d_vector(text_to_vectorize)
        user_384d = VectorPlacementEngine.compute_384d_text_embedding(text_to_vectorize)

        # 2. Find Nearest-Neighbor Benchmark Companies from 50 Dataset
        nearest_neighbors = VectorPlacementEngine.find_nearest_neighbors(
            user_11d, user_384d, self.kb.companies, top_k=3
        )

        # 3. Format CVP if business details provided and compute 384-D CVP vector matches
        cvp_statement = ""
        user_cvp_search_text = user_message
        if isinstance(user_business_context, str):
            cvp_statement = user_business_context
            user_cvp_search_text = user_business_context
        elif isinstance(user_business_context, dict):
            if user_business_context.get("cvp_text"):
                cvp_statement = user_business_context.get("cvp_text")
                user_cvp_search_text = cvp_statement
            elif user_business_context.get("product_name"):
                cvp_statement = BusinessEvaluator.format_cvp(
                    user_business_context.get("target_customer", ""),
                    user_business_context.get("statement_of_need", ""),
                    user_business_context.get("product_name", ""),
                    user_business_context.get("product_category", ""),
                    user_business_context.get("statement_of_key_benefit", "")
                )
                user_cvp_search_text = cvp_statement

        nearest_cvps = VectorPlacementEngine.find_nearest_cvps(
            user_cvp_search_text, self.kb.companies, top_k=3
        )

        # Check intent for relevance, gibberish, greeting, off-topic, or inappropriate
        intent, override_msg = GroqOllamaProvider.check_query_intent(user_message)
        if intent in ['GIBBERISH', 'OFF_TOPIC', 'GREETING', 'INAPPROPRIATE']:
            return {
                "text": override_msg,
                "nearest_neighbors": nearest_neighbors,
                "nearest_cvps": nearest_cvps,
                "user_11d_vector": user_11d,
                "cvp_statement": cvp_statement
            }

        # 4. Construct System Prompt with Vector Context & Strict Formatting Rules
        neighbors_summary = "\n".join([
            f"- {n['company']} ({n['sector']}): {n['similarity_pct']}% similarity. Primary CVP: {n['cvp']}"
            for n in nearest_neighbors
        ])

        cvp_matches_summary = "\n".join([
            f"- {c['company']} ({c['sector']}): {c['similarity_pct']}% CVP vector match. CVP: {c['cvp']}"
            for c in nearest_cvps
        ])

        system_prompt = f"""You are an expert AI Market Intelligence Strategist and executive business advisor.
Your goal is to provide fluid, engaging, highly relevant, and natural strategic market guidance strictly tailored to the user's Customer Value Proposition (CVP) and market environment.

CRITICAL BEHAVIOR & RELEVANCE RULES:
1. STRICT RELEVANCE RULE: You must ONLY answer queries related to business strategy, market intelligence, Customer Value Propositions (CVP), PESTLE risks, Porter's 5 Forces, competitive benchmarking, unit economics, go-to-market strategies, or industry analysis.
   - If the user prompt is off-topic, gibberish (e.g. "asdfasdf", random letters), or unrelated to business strategy, POLITELY DECLINE to answer and instruct the user to ask a relevant business strategy or CVP query. Do NOT attempt to evaluate gibberish or off-topic prompts as business strategy.
2. FLUID, CONVERSATIONAL & ADAPTIVE RESPONSE STYLE:
   - Speak naturally and fluidly like a senior strategy advisor.
   - DO NOT use rigid, repetitive template titles or uppercase boilerplate headers (NEVER output headers like "STRATEGIC MARKET INTELLIGENCE SYNTHESIS" or "1. EXECUTIVE SUMMARY").
   - Adapt your answer structure dynamically to the specific question asked, using clear paragraphs, smooth transitions, and bullet points where helpful.
3. EMBEDDING & VECTOR CONTEXT INTEGRATION:
   - Inform your response using the user's 384-D vector placement, CVP embedding matches, and 11-D strategic scores below:

NEAREST BENCHMARK PEERS (11-D Vector Placement):
{neighbors_summary}

NEAREST CVP EMBEDDING PEERS (384-D Vector Space):
{cvp_matches_summary}

USER STRATEGIC 11-D VECTOR SCORES:
- Political: {user_11d[0]} | Economic: {user_11d[1]} | Social: {user_11d[2]} | Tech: {user_11d[3]} | Legal: {user_11d[4]} | Environmental: {user_11d[5]}
- Threat of New Entrants: {user_11d[6]} | Buyer Power: {user_11d[7]} | Supplier Power: {user_11d[8]} | Threat of Substitutes: {user_11d[9]} | Competitive Rivalry: {user_11d[10]}

STRICT FORMATTING RULES:
- NEVER use markdown hashtags (#, ##, ###) or asterisks (* or **) anywhere in your response.
- Keep response formatting clean and readable using plain text, single-dash bullet points (- ), and numbered lists (1., 2., 3.).
"""

        user_prompt = user_message
        if cvp_statement:
            user_prompt += f"\n\nFormatted Business CVP: {cvp_statement}"

        ai_response = self.llm.generate_response(system_prompt, user_prompt, chat_history=chat_history)

        return {
            "text": ai_response,
            "nearest_neighbors": nearest_neighbors,
            "nearest_cvps": nearest_cvps,
            "user_11d_vector": user_11d,
            "cvp_statement": cvp_statement
        }


if __name__ == "__main__":
    print("Testing Chatbot Engine...")
    engine = ChatbotEngine()
    res = engine.process_message("I want to launch an AI-powered EV charging station mobile app in India.")
    print("AI Response Preview:", res["text"][:200])
    print("Top Nearest Neighbor:", res["nearest_neighbors"][0]["company"], f"({res['nearest_neighbors'][0]['similarity_pct']}%)")
    print("11-D Strategic Vector:", res["user_11d_vector"])

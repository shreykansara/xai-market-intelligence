#!/usr/bin/env python3
"""
Explainable Market Intelligence Web Server
------------------------------------------
Lightweight REST API and Static File Server serving the Market Intelligence Chatbot.
"""

import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Import engine
from chatbot_engine import ChatbotEngine, BusinessEvaluator, VectorPlacementEngine, TemporalClusterMatcher, COMPANIES_JSON_PATH

BASE_DIR = Path(__file__).parent.resolve()
WEB_DIR = BASE_DIR / "web"
PORT = 8080

# Instantiate Chatbot Engine
engine = ChatbotEngine()



class ChatbotHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler serving static files and API endpoints."""

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def _send_error(self, message: str, status: int = 400):
        self._send_json({"error": message}, status=status)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/api/companies":
            if COMPANIES_JSON_PATH.exists():
                with open(COMPANIES_JSON_PATH, "r", encoding="utf-8") as f:
                    companies = json.load(f)
                return self._send_json({"companies": companies})
            return self._send_json({"companies": []})

        # Static file serving
        if path == "/":
            file_path = WEB_DIR / "index.html"
        else:
            relative_path = path.lstrip("/")
            file_path = WEB_DIR / relative_path

        if file_path.exists() and file_path.is_file():
            content_type = "text/html"
            if file_path.suffix == ".css":
                content_type = "text/css"
            elif file_path.suffix == ".js":
                content_type = "application/javascript"
            elif file_path.suffix == ".json":
                content_type = "application/json"
            elif file_path.suffix == ".png":
                content_type = "image/png"
            elif file_path.suffix == ".svg":
                content_type = "image/svg+xml"
            elif file_path.suffix == ".ico":
                content_type = "image/x-icon"
            elif file_path.suffix == ".jpg" or file_path.suffix == ".jpeg":
                content_type = "image/jpeg"

            try:
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self._send_error(f"Failed to read file: {e}", 500)
        else:
            self._send_error("404 Not Found", 404)

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            payload = json.loads(post_body.decode("utf-8"))
        except Exception:
            payload = {}

        if path == "/api/chat":
            message = payload.get("message", "").strip()
            if not message:
                return self._send_error("Message parameter is required.")

            context = payload.get("business_context")
            groq_key = payload.get("groq_api_key")
            chat_history = payload.get("chat_history", [])

            res = engine.process_message(message, user_business_context=context, groq_key_override=groq_key, chat_history=chat_history)
            return self._send_json(res)

        elif path == "/api/evaluate_cvp":
            cvp_text = payload.get("cvp_text", "").strip()
            if not cvp_text:
                return self._send_error("cvp_text parameter is required.")

            # Compute vectors and find nearest CVP embeddings
            user_11d = VectorPlacementEngine.compute_11d_vector(cvp_text)
            nearest_cvps = VectorPlacementEngine.find_nearest_cvps(cvp_text, engine.kb.companies, top_k=3)
            nearest_neighbors = VectorPlacementEngine.find_nearest_neighbors(user_11d, VectorPlacementEngine.compute_384d_text_embedding(cvp_text), engine.kb.companies, top_k=3)

            pestle_vector = user_11d[0:6]
            porter_vector = user_11d[6:11]

            return self._send_json({
                "cvp_text": cvp_text,
                "cvp_statement": cvp_text,
                "pestle_vector": pestle_vector,
                "porter_vector": porter_vector,
                "user_11d_vector": user_11d,
                "nearest_cvps": nearest_cvps,
                "nearest_neighbors": nearest_neighbors
            })

        elif path == "/api/evaluate_revenue_events":
            events = payload.get("events", [])
            if not isinstance(events, list) or len(events) == 0:
                return self._send_error("events list parameter is required.")

            result = BusinessEvaluator.evaluate_revenue_events(events)

            combined_event_text = " ".join([f"{e.get('event_title', '')} {e.get('event_description', '')} {e.get('category_tag', '')}" for e in events])
            user_11d = result["11d_vector"]
            user_384d = VectorPlacementEngine.compute_384d_text_embedding(combined_event_text)

            nearest_neighbors = VectorPlacementEngine.find_nearest_neighbors(user_11d, user_384d, engine.kb.companies, top_k=3)
            nearest_cvps = VectorPlacementEngine.find_nearest_cvps(combined_event_text, engine.kb.companies, top_k=3)

            return self._send_json({
                "events": events,
                "pestle_vector": result["pestle_vector"],
                "porter_vector": result["porter_vector"],
                "user_11d_vector": user_11d,
                "event_impacts": result["event_impacts"],
                "nearest_cvps": nearest_cvps,
                "nearest_neighbors": nearest_neighbors
            })

        elif path == "/api/match_revenue_clusters":
            revenue_series = payload.get("revenue_series", [])
            if not isinstance(revenue_series, list) or len(revenue_series) == 0:
                return self._send_error("revenue_series array parameter is required.")

            result = TemporalClusterMatcher.process_time_series(revenue_series)

            stored_titles = " ".join([c["title"] + " " + c["description"] for c in result["stored_clusters"]])
            if not stored_titles:
                stored_titles = "Revenue Market Intelligence Analysis"

            user_11d = result["11d_vector"]
            user_384d = VectorPlacementEngine.compute_384d_text_embedding(stored_titles)

            nearest_neighbors = VectorPlacementEngine.find_nearest_neighbors(user_11d, user_384d, engine.kb.companies, top_k=3)
            nearest_cvps = VectorPlacementEngine.find_nearest_cvps(stored_titles, engine.kb.companies, top_k=3)

            return self._send_json({
                "analyzed_series": result["analyzed_series"],
                "matched_clusters": result["matched_clusters"],
                "stored_clusters": result["stored_clusters"],
                "pestle_vector": result["pestle_vector"],
                "porter_vector": result["porter_vector"],
                "user_11d_vector": user_11d,
                "nearest_cvps": nearest_cvps,
                "nearest_neighbors": nearest_neighbors
            })

        elif path == "/api/evaluate_business":
            tc = payload.get("target_customer", "")
            sn = payload.get("statement_of_need", "")
            pn = payload.get("product_name", "")
            pc = payload.get("product_category", "")
            kb = payload.get("statement_of_key_benefit", "")

            cvp_str = BusinessEvaluator.format_cvp(tc, sn, pn, pc, kb)
            business_text = f"{pn} {pc} {tc} {sn} {kb}"

            res = engine.process_message(
                user_message=f"Evaluate this business and explain strategic risks for: {business_text}",
                user_business_context={
                    "target_customer": tc,
                    "statement_of_need": sn,
                    "product_name": pn,
                    "product_category": pc,
                    "statement_of_key_benefit": kb
                },
                groq_key_override=payload.get("groq_api_key")
            )

            res["cvp_statement"] = cvp_str
            return self._send_json(res)

        else:
            self._send_error("Unknown Endpoint", 404)


def run_server():
    WEB_DIR.mkdir(exist_ok=True)
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, ChatbotHTTPRequestHandler)
    print(f"[Market Intelligence Server] Serving on http://localhost:{PORT}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Market Intelligence Server] Shutting down...")
        httpd.server_close()


if __name__ == "__main__":
    run_server()

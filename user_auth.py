"""
Omniscope AI - User Authentication and Intelligence Persistence Layer
---------------------------------------------------------------------
Handles secure user registration, authentication (PBKDF2-HMAC-SHA256),
token generation/verification (HMAC-SHA256), and persistence for:
1. User Profiles (Full Name, Company, Email, Role)
2. Saved Analyses (CVP Evaluator and Revenue Fluctuation Models)
3. Chatbot Conversation Sessions & Strategy Inquiries
4. Seamless Guest-to-User Data Migration

Primary Database: Supabase PostgreSQL
Resilience Fallback: Local SQLite database (`scratch/user_intelligence.db`)
"""

import os
import re
import json
import time
import uuid
import hmac
import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "scratch"
DATA_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_DB_PATH = DATA_DIR / "user_intelligence.db"

# Auto-load Environment Variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

USER_AUTH_SECRET = os.environ.get("USER_AUTH_SECRET") or os.environ.get("ADMIN_AUTH_SECRET", "omniscope_user_secret_key_production_2026")
DEFAULT_SUPABASE_URL = os.environ.get("SUPABASE_DB_URL", "")



# ==========================================
# DATABASE CONNECTION & SCHEMA INIT
# ==========================================

def get_pg_connection():
    """Attempt direct PostgreSQL connection if configured."""
    db_url = os.environ.get("SUPABASE_DB_URL", DEFAULT_SUPABASE_URL)
    if not db_url:
        return None
    try:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(db_url, connect_timeout=6)
        conn.autocommit = True
        return conn
    except Exception as err:
        print(f"[UserAuth] Note: PostgreSQL connection unavailable, falling back to SQLite: {err}")
        return None


def get_sqlite_connection():
    """Returns a local SQLite connection for offline/resilience mode."""
    conn = sqlite3.connect(str(SQLITE_DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Ensures user tables exist in both PostgreSQL (if reachable) and SQLite fallback."""
    # 1. PostgreSQL Schema
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(64) PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    salt VARCHAR(64) NOT NULL,
                    full_name VARCHAR(255) NOT NULL,
                    company_name VARCHAR(255),
                    role VARCHAR(50) DEFAULT 'user',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP WITH TIME ZONE
                );
                CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

                CREATE TABLE IF NOT EXISTS user_analyses (
                    id VARCHAR(64) PRIMARY KEY,
                    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    analysis_type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    summary TEXT,
                    input_data JSONB NOT NULL,
                    results_data JSONB NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_user_analyses_user ON user_analyses (user_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_user_analyses_type ON user_analyses (analysis_type);

                CREATE TABLE IF NOT EXISTS user_conversations (
                    id VARCHAR(64) PRIMARY KEY,
                    user_id VARCHAR(64) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    analysis_id VARCHAR(64) REFERENCES user_analyses(id) ON DELETE SET NULL,
                    title VARCHAR(255) NOT NULL,
                    mode VARCHAR(50) DEFAULT 'cvp',
                    messages JSONB NOT NULL DEFAULT '[]'::jsonb,
                    context JSONB,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_user_conversations_user ON user_conversations (user_id, created_at DESC);
            """)
            cur.close()
            pg_conn.close()
            print("[UserAuth] PostgreSQL schema initialized successfully.")
        except Exception as e:
            print(f"[UserAuth] Warning: Could not initialize PG schema: {e}")

    # 2. SQLite Fallback Schema
    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    company_name TEXT,
                    role TEXT DEFAULT 'user',
                    created_at TEXT,
                    last_login TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_sq_users_email ON users (email);

                CREATE TABLE IF NOT EXISTS user_analyses (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    analysis_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    summary TEXT,
                    input_data TEXT NOT NULL,
                    results_data TEXT NOT NULL,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                CREATE INDEX IF NOT EXISTS idx_sq_analyses_user ON user_analyses (user_id, created_at DESC);

                CREATE TABLE IF NOT EXISTS user_conversations (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    analysis_id TEXT,
                    title TEXT NOT NULL,
                    mode TEXT DEFAULT 'cvp',
                    messages TEXT NOT NULL DEFAULT '[]',
                    context TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                CREATE INDEX IF NOT EXISTS idx_sq_conversations_user ON user_conversations (user_id, created_at DESC);
            """)
        sq_conn.close()
    except Exception as e:
        print(f"[UserAuth] Warning: Could not initialize SQLite schema: {e}")


# ==========================================
# CRYPTOGRAPHY & TOKEN MANAGEMENT
# ==========================================

def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Hashes password with PBKDF2-HMAC-SHA256 (100k iterations)."""
    if not salt:
        salt = uuid.uuid4().hex
    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    pwd_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, 100000).hex()
    return pwd_hash, salt


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Constant-time verification of password against stored hash."""
    pwd_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")
    computed_hash = hashlib.pbkdf2_hmac("sha256", pwd_bytes, salt_bytes, 100000).hex()
    return hmac.compare_digest(computed_hash, stored_hash)


def generate_user_token(user_id: str, email: str) -> str:
    """
    Generates a secure, signed token:
    Format: timestamp.user_id.signature
    Valid for 30 days.
    """
    timestamp = int(time.time())
    payload = f"{user_id}:{email}:{timestamp}"
    sig = hmac.new(USER_AUTH_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{timestamp}.{user_id}.{sig}"


def verify_user_token(token: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Verifies user token signature and expiration (30 days).
    Returns (is_valid, user_id, error_message).
    """
    if not token or not isinstance(token, str):
        return False, None, "Missing authentication token"

    parts = token.split(".")
    if len(parts) != 3:
        return False, None, "Malformed authentication token"

    timestamp_str, user_id, sig = parts
    try:
        timestamp = int(timestamp_str)
    except ValueError:
        return False, None, "Invalid token timestamp"

    # 30-day token lifetime
    if time.time() - timestamp > (86400 * 30):
        return False, None, "Session expired, please sign in again"

    # Fetch user to verify email in signature
    user = get_user_by_id(user_id)
    if not user:
        return False, None, "User account no longer exists"

    expected_payload = f"{user_id}:{user['email']}:{timestamp}"
    expected_sig = hmac.new(USER_AUTH_SECRET.encode("utf-8"), expected_payload.encode("utf-8"), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(sig, expected_sig):
        return False, None, "Invalid token signature"

    return True, user_id, None


# ==========================================
# USER MANAGEMENT (CRUD)
# ==========================================

def register_user(email: str, password: str, full_name: str, company_name: str = "", role: str = "user") -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Registers a new user."""
    email = (email or "").strip().lower()
    full_name = (full_name or "").strip()
    company_name = (company_name or "").strip()

    if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False, None, "Please enter a valid email address."
    if not password or len(password) < 6:
        return False, None, "Password must be at least 6 characters long."
    if not full_name:
        return False, None, "Please provide your full name."

    # Check if user already exists
    existing = get_user_by_email(email)
    if existing:
        return False, None, "An account with this email address already exists. Please sign in."

    user_id = f"usr_{uuid.uuid4().hex[:16]}"
    pwd_hash, salt = hash_password(password)
    now_iso = datetime.now(timezone.utc).isoformat()

    # Try PostgreSQL
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                INSERT INTO users (id, email, password_hash, salt, full_name, company_name, role, created_at, last_login)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW());
            """, (user_id, email, pwd_hash, salt, full_name, company_name, role))
            cur.close()
            pg_conn.close()
        except Exception as e:
            print(f"[UserAuth] PG insert error: {e}")

    # Also keep SQLite in sync
    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.execute("""
                INSERT OR REPLACE INTO users (id, email, password_hash, salt, full_name, company_name, role, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (user_id, email, pwd_hash, salt, full_name, company_name, role, now_iso, now_iso))
        sq_conn.close()
    except Exception as e:
        print(f"[UserAuth] SQLite insert error: {e}")

    user_data = {
        "id": user_id,
        "email": email,
        "full_name": full_name,
        "company_name": company_name,
        "role": role,
        "created_at": now_iso
    }
    return True, user_data, None


def authenticate_user(email: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Authenticates user with email and password."""
    email = (email or "").strip().lower()
    if not email or not password:
        return False, None, "Email and password are required."

    user = get_user_by_email(email, include_secrets=True)
    if not user:
        return False, None, "No account found with this email address."

    if not verify_password(password, user["password_hash"], user["salt"]):
        return False, None, "Invalid email or password. Please verify your credentials."

    # Update last login
    now_iso = datetime.now(timezone.utc).isoformat()
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("UPDATE users SET last_login = NOW() WHERE id = %s;", (user["id"],))
            cur.close()
            pg_conn.close()
        except Exception:
            pass

    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.execute("UPDATE users SET last_login = ? WHERE id = ?;", (now_iso, user["id"]))
        sq_conn.close()
    except Exception:
        pass

    user_info = {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "company_name": user.get("company_name", ""),
        "role": user.get("role", "user"),
        "created_at": str(user.get("created_at", ""))
    }
    return True, user_info, None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves user info by user_id."""
    # Try PostgreSQL first
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("SELECT id, email, full_name, company_name, role, created_at, last_login FROM users WHERE id = %s;", (user_id,))
            row = cur.fetchone()
            cur.close()
            pg_conn.close()
            if row:
                return {
                    "id": row[0],
                    "email": row[1],
                    "full_name": row[2],
                    "company_name": row[3] or "",
                    "role": row[4] or "user",
                    "created_at": str(row[5]),
                    "last_login": str(row[6]) if row[6] else None
                }
        except Exception:
            pass

    # Fallback to SQLite
    try:
        sq_conn = get_sqlite_connection()
        cur = sq_conn.cursor()
        cur.execute("SELECT id, email, full_name, company_name, role, created_at, last_login FROM users WHERE id = ?;", (user_id,))
        row = cur.fetchone()
        sq_conn.close()
        if row:
            return dict(row)
    except Exception:
        pass

    return None


def get_user_by_email(email: str, include_secrets: bool = False) -> Optional[Dict[str, Any]]:
    """Retrieves user by email."""
    email = email.strip().lower()
    # Try PostgreSQL
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                SELECT id, email, password_hash, salt, full_name, company_name, role, created_at, last_login 
                FROM users WHERE email = %s;
            """, (email,))
            row = cur.fetchone()
            cur.close()
            pg_conn.close()
            if row:
                data = {
                    "id": row[0],
                    "email": row[1],
                    "full_name": row[4],
                    "company_name": row[5] or "",
                    "role": row[6] or "user",
                    "created_at": str(row[7]),
                    "last_login": str(row[8]) if row[8] else None
                }
                if include_secrets:
                    data["password_hash"] = row[2]
                    data["salt"] = row[3]
                return data
        except Exception:
            pass

    # Fallback to SQLite
    try:
        sq_conn = get_sqlite_connection()
        cur = sq_conn.cursor()
        cur.execute("""
            SELECT id, email, password_hash, salt, full_name, company_name, role, created_at, last_login 
            FROM users WHERE email = ?;
        """, (email,))
        row = cur.fetchone()
        sq_conn.close()
        if row:
            d = dict(row)
            if not include_secrets:
                d.pop("password_hash", None)
                d.pop("salt", None)
            return d
    except Exception:
        pass

    return None


# ==========================================
# USER ANALYSES PERSISTENCE (CVP & REVENUE)
# ==========================================

def save_analysis(user_id: str, analysis_type: str, title: str, summary: str, input_data: Dict[str, Any], results_data: Dict[str, Any], analysis_id: Optional[str] = None) -> Dict[str, Any]:
    """Saves or updates a CVP or Revenue analysis."""
    if not analysis_id:
        analysis_id = f"anl_{uuid.uuid4().hex[:16]}"

    title = (title or "").strip() or ("CVP Evaluation" if analysis_type == "cvp" else "Revenue Fluctuation Model")
    summary = (summary or "").strip()
    now_iso = datetime.now(timezone.utc).isoformat()

    input_json = json.dumps(input_data)
    results_json = json.dumps(results_data)

    # 1. PostgreSQL
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                INSERT INTO user_analyses (id, user_id, analysis_type, title, summary, input_data, results_data, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    summary = EXCLUDED.summary,
                    input_data = EXCLUDED.input_data,
                    results_data = EXCLUDED.results_data,
                    updated_at = NOW();
            """, (analysis_id, user_id, analysis_type, title, summary, input_json, results_json))
            cur.close()
            pg_conn.close()
        except Exception as e:
            print(f"[UserAuth] PG save_analysis error: {e}")

    # 2. SQLite
    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.execute("""
                INSERT INTO user_analyses (id, user_id, analysis_type, title, summary, input_data, results_data, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    summary = excluded.summary,
                    input_data = excluded.input_data,
                    results_data = excluded.results_data,
                    updated_at = excluded.updated_at;
            """, (analysis_id, user_id, analysis_type, title, summary, input_json, results_json, now_iso, now_iso))
        sq_conn.close()
    except Exception as e:
        print(f"[UserAuth] SQLite save_analysis error: {e}")

    return {
        "id": analysis_id,
        "user_id": user_id,
        "analysis_type": analysis_type,
        "title": title,
        "summary": summary,
        "input_data": input_data,
        "results_data": results_data,
        "created_at": now_iso,
        "updated_at": now_iso
    }


def list_analyses(user_id: str, analysis_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Lists saved analyses for a user."""
    items = []
    # Try PostgreSQL
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            if analysis_type:
                cur.execute("""
                    SELECT id, analysis_type, title, summary, input_data, results_data, created_at, updated_at 
                    FROM user_analyses 
                    WHERE user_id = %s AND analysis_type = %s 
                    ORDER BY created_at DESC LIMIT %s;
                """, (user_id, analysis_type, limit))
            else:
                cur.execute("""
                    SELECT id, analysis_type, title, summary, input_data, results_data, created_at, updated_at 
                    FROM user_analyses 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC LIMIT %s;
                """, (user_id, limit))
            rows = cur.fetchall()
            cur.close()
            pg_conn.close()

            for r in rows:
                inp = r[4] if isinstance(r[4], dict) else json.loads(r[4])
                res = r[5] if isinstance(r[5], dict) else json.loads(r[5])
                items.append({
                    "id": r[0],
                    "analysis_type": r[1],
                    "title": r[2],
                    "summary": r[3] or "",
                    "input_data": inp,
                    "results_data": res,
                    "created_at": str(r[6]),
                    "updated_at": str(r[7])
                })
            return items
        except Exception as e:
            print(f"[UserAuth] PG list_analyses error: {e}")

    # Fallback to SQLite
    try:
        sq_conn = get_sqlite_connection()
        cur = sq_conn.cursor()
        if analysis_type:
            cur.execute("""
                SELECT id, analysis_type, title, summary, input_data, results_data, created_at, updated_at 
                FROM user_analyses 
                WHERE user_id = ? AND analysis_type = ? 
                ORDER BY created_at DESC LIMIT ?;
            """, (user_id, analysis_type, limit))
        else:
            cur.execute("""
                SELECT id, analysis_type, title, summary, input_data, results_data, created_at, updated_at 
                FROM user_analyses 
                WHERE user_id = ? 
                ORDER BY created_at DESC LIMIT ?;
            """, (user_id, limit))
        rows = cur.fetchall()
        sq_conn.close()

        for r in rows:
            inp = json.loads(r["input_data"]) if isinstance(r["input_data"], str) else r["input_data"]
            res = json.loads(r["results_data"]) if isinstance(r["results_data"], str) else r["results_data"]
            items.append({
                "id": r["id"],
                "analysis_type": r["analysis_type"],
                "title": r["title"],
                "summary": r["summary"] or "",
                "input_data": inp,
                "results_data": res,
                "created_at": str(r["created_at"]),
                "updated_at": str(r["updated_at"])
            })
    except Exception as e:
        print(f"[UserAuth] SQLite list_analyses error: {e}")

    return items


def get_analysis(user_id: str, analysis_id: str) -> Optional[Dict[str, Any]]:
    """Fetches a specific analysis."""
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                SELECT id, analysis_type, title, summary, input_data, results_data, created_at, updated_at 
                FROM user_analyses WHERE id = %s AND user_id = %s;
            """, (analysis_id, user_id))
            r = cur.fetchone()
            cur.close()
            pg_conn.close()
            if r:
                inp = r[4] if isinstance(r[4], dict) else json.loads(r[4])
                res = r[5] if isinstance(r[5], dict) else json.loads(r[5])
                return {
                    "id": r[0],
                    "analysis_type": r[1],
                    "title": r[2],
                    "summary": r[3] or "",
                    "input_data": inp,
                    "results_data": res,
                    "created_at": str(r[6]),
                    "updated_at": str(r[7])
                }
        except Exception:
            pass

    try:
        sq_conn = get_sqlite_connection()
        cur = sq_conn.cursor()
        cur.execute("SELECT * FROM user_analyses WHERE id = ? AND user_id = ?;", (analysis_id, user_id))
        r = cur.fetchone()
        sq_conn.close()
        if r:
            inp = json.loads(r["input_data"]) if isinstance(r["input_data"], str) else r["input_data"]
            res = json.loads(r["results_data"]) if isinstance(r["results_data"], str) else r["results_data"]
            return {
                "id": r["id"],
                "analysis_type": r["analysis_type"],
                "title": r["title"],
                "summary": r["summary"] or "",
                "input_data": inp,
                "results_data": res,
                "created_at": str(r["created_at"]),
                "updated_at": str(r["updated_at"])
            }
    except Exception:
        pass

    return None


def delete_analysis(user_id: str, analysis_id: str) -> bool:
    """Deletes an analysis belonging to a user."""
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("DELETE FROM user_analyses WHERE id = %s AND user_id = %s;", (analysis_id, user_id))
            cur.close()
            pg_conn.close()
        except Exception:
            pass

    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.execute("DELETE FROM user_analyses WHERE id = ? AND user_id = ?;", (analysis_id, user_id))
        sq_conn.close()
    except Exception:
        pass

    return True


# ==========================================
# USER CONVERSATIONS (CHAT SESSIONS)
# ==========================================

def save_conversation(user_id: str, title: str, mode: str = "cvp", messages: Optional[List[Dict[str, Any]]] = None, context: Optional[Dict[str, Any]] = None, analysis_id: Optional[str] = None, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """Saves or updates a chatbot conversation session."""
    if not conversation_id:
        conversation_id = f"cnv_{uuid.uuid4().hex[:16]}"

    messages = messages or []
    title = (title or "").strip()
    if not title:
        first_user_msg = next((m.get("content") for m in messages if m.get("role") == "user"), None)
        title = first_user_msg[:45] + "..." if first_user_msg else "Market Intelligence Chat"

    now_iso = datetime.now(timezone.utc).isoformat()
    msg_json = json.dumps(messages)
    ctx_json = json.dumps(context or {})

    # 1. PostgreSQL
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                INSERT INTO user_conversations (id, user_id, analysis_id, title, mode, messages, context, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    mode = EXCLUDED.mode,
                    messages = EXCLUDED.messages,
                    context = EXCLUDED.context,
                    updated_at = NOW();
            """, (conversation_id, user_id, analysis_id, title, mode, msg_json, ctx_json))
            cur.close()
            pg_conn.close()
        except Exception as e:
            print(f"[UserAuth] PG save_conversation error: {e}")

    # 2. SQLite
    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.execute("""
                INSERT INTO user_conversations (id, user_id, analysis_id, title, mode, messages, context, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    mode = excluded.mode,
                    messages = excluded.messages,
                    context = excluded.context,
                    updated_at = excluded.updated_at;
            """, (conversation_id, user_id, analysis_id, title, mode, msg_json, ctx_json, now_iso, now_iso))
        sq_conn.close()
    except Exception as e:
        print(f"[UserAuth] SQLite save_conversation error: {e}")

    return {
        "id": conversation_id,
        "user_id": user_id,
        "analysis_id": analysis_id,
        "title": title,
        "mode": mode,
        "messages": messages,
        "context": context or {},
        "created_at": now_iso,
        "updated_at": now_iso
    }


def list_conversations(user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Lists recent conversation sessions for a user."""
    items = []
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                SELECT id, analysis_id, title, mode, messages, context, created_at, updated_at 
                FROM user_conversations 
                WHERE user_id = %s 
                ORDER BY updated_at DESC LIMIT %s;
            """, (user_id, limit))
            rows = cur.fetchall()
            cur.close()
            pg_conn.close()

            for r in rows:
                msgs = r[4] if isinstance(r[4], list) else json.loads(r[4])
                ctx = r[5] if isinstance(r[5], dict) else json.loads(r[5])
                items.append({
                    "id": r[0],
                    "analysis_id": r[1],
                    "title": r[2],
                    "mode": r[3],
                    "message_count": len(msgs),
                    "last_message": msgs[-1]["content"][:100] if msgs else "",
                    "context": ctx,
                    "created_at": str(r[6]),
                    "updated_at": str(r[7])
                })
            return items
        except Exception as e:
            print(f"[UserAuth] PG list_conversations error: {e}")

    try:
        sq_conn = get_sqlite_connection()
        cur = sq_conn.cursor()
        cur.execute("""
            SELECT id, analysis_id, title, mode, messages, context, created_at, updated_at 
            FROM user_conversations 
            WHERE user_id = ? 
            ORDER BY updated_at DESC LIMIT ?;
        """, (user_id, limit))
        rows = cur.fetchall()
        sq_conn.close()

        for r in rows:
            msgs = json.loads(r["messages"]) if isinstance(r["messages"], str) else r["messages"]
            ctx = json.loads(r["context"]) if isinstance(r["context"], str) else r["context"]
            items.append({
                "id": r["id"],
                "analysis_id": r["analysis_id"],
                "title": r["title"],
                "mode": r["mode"],
                "message_count": len(msgs) if isinstance(msgs, list) else 0,
                "last_message": msgs[-1].get("content", "")[:100] if msgs else "",
                "context": ctx or {},
                "created_at": str(r["created_at"]),
                "updated_at": str(r["updated_at"])
            })
    except Exception as e:
        print(f"[UserAuth] SQLite list_conversations error: {e}")

    return items


def get_conversation(user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
    """Fetches full conversation message history."""
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("""
                SELECT id, analysis_id, title, mode, messages, context, created_at, updated_at 
                FROM user_conversations WHERE id = %s AND user_id = %s;
            """, (conversation_id, user_id))
            r = cur.fetchone()
            cur.close()
            pg_conn.close()
            if r:
                msgs = r[4] if isinstance(r[4], list) else json.loads(r[4])
                ctx = r[5] if isinstance(r[5], dict) else json.loads(r[5])
                return {
                    "id": r[0],
                    "analysis_id": r[1],
                    "title": r[2],
                    "mode": r[3],
                    "messages": msgs,
                    "context": ctx,
                    "created_at": str(r[6]),
                    "updated_at": str(r[7])
                }
        except Exception:
            pass

    try:
        sq_conn = get_sqlite_connection()
        cur = sq_conn.cursor()
        cur.execute("SELECT * FROM user_conversations WHERE id = ? AND user_id = ?;", (conversation_id, user_id))
        r = cur.fetchone()
        sq_conn.close()
        if r:
            msgs = json.loads(r["messages"]) if isinstance(r["messages"], str) else r["messages"]
            ctx = json.loads(r["context"]) if isinstance(r["context"], str) else r["context"]
            return {
                "id": r["id"],
                "analysis_id": r["analysis_id"],
                "title": r["title"],
                "mode": r["mode"],
                "messages": msgs,
                "context": ctx,
                "created_at": str(r["created_at"]),
                "updated_at": str(r["updated_at"])
            }
    except Exception:
        pass

    return None


def delete_conversation(user_id: str, conversation_id: str) -> bool:
    """Deletes a conversation session."""
    pg_conn = get_pg_connection()
    if pg_conn:
        try:
            cur = pg_conn.cursor()
            cur.execute("DELETE FROM user_conversations WHERE id = %s AND user_id = %s;", (conversation_id, user_id))
            cur.close()
            pg_conn.close()
        except Exception:
            pass

    try:
        sq_conn = get_sqlite_connection()
        with sq_conn:
            sq_conn.execute("DELETE FROM user_conversations WHERE id = ? AND user_id = ?;", (conversation_id, user_id))
        sq_conn.close()
    except Exception:
        pass

    return True


# ==========================================
# GUEST TO USER DATA MIGRATION
# ==========================================

def sync_guest_data(user_id: str, analyses: Optional[List[Dict[str, Any]]] = None, conversations: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Imports and saves analyses and conversation sessions accumulated while user was a guest.
    """
    analyses = analyses or []
    conversations = conversations or []
    saved_analyses_count = 0
    saved_conversations_count = 0

    for a in analyses:
        try:
            save_analysis(
                user_id=user_id,
                analysis_type=a.get("analysis_type", "cvp"),
                title=a.get("title", ""),
                summary=a.get("summary", ""),
                input_data=a.get("input_data", {}),
                results_data=a.get("results_data", {}),
                analysis_id=a.get("id")
            )
            saved_analyses_count += 1
        except Exception as err:
            print(f"[UserAuth] Failed importing guest analysis: {err}")

    for c in conversations:
        try:
            save_conversation(
                user_id=user_id,
                title=c.get("title", ""),
                mode=c.get("mode", "cvp"),
                messages=c.get("messages", []),
                context=c.get("context", {}),
                analysis_id=c.get("analysis_id"),
                conversation_id=c.get("id")
            )
            saved_conversations_count += 1
        except Exception as err:
            print(f"[UserAuth] Failed importing guest conversation: {err}")

    return {
        "success": True,
        "saved_analyses": saved_analyses_count,
        "saved_conversations": saved_conversations_count
    }


# Auto-initialize database schemas on import
init_db()

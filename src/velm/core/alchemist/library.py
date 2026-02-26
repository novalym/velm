# Path: src/velm/core/alchemist/library.py
# ----------------------------------------

"""
=================================================================================
== THE OMNISCIENT GRIMOIRE (V-Ω-TOTALITY-V100M-SENTIENT-LIBRARY)               ==
=================================================================================
LIF: 100,000,000,000,000 | ROLE: TEMPLATE_OMNISCIENCE | RANK: OMEGA_SUPREME
AUTH_CODE: Ω_LIBRARY_V100M_SENTIENT_BLUEPRINT_FINALIS_2026

This is the Ascended Standard Library of the God-Engine. It transfigures the `.scaffold`
language from a blind templating format into an Autonomous, Sentient Engineering Agent.

Blueprints can now Read the Disk, Query Databases, Call APIs, and Summon AI
all within the microsecond of their own rendering.
=================================================================================
"""

import datetime
import hashlib
import html
import json
import os
import platform
import re
import secrets
import shlex
import subprocess
import uuid
import logging
import urllib.parse
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, Union, List, Dict

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe
from ...utils import is_binary

Logger = Scribe("AlchemicalLibrary")


# =============================================================================
# == THE DOMAIN OF THE MIND (ARTIFICIAL INTELLIGENCE)                        ==
# =============================================================================

@lru_cache(maxsize=128)
def ai_prompt_rite(prompt: str, system: str = "You are an expert coder.", model: str = "fast") -> str:
    """
    [ASCENSION 1]: THE NEURAL GAZE.
    Summons the LLM inline during template rendering.
    Usage: {{ ai_prompt("Write a regex for emails") }}
    """
    try:
        # Late-bound import to avoid circular dependencies during boot
        from ...core.ai.engine import AIEngine
        from ...interfaces.requests import IntelligenceRequest

        ai = AIEngine()
        req = IntelligenceRequest(
            user_prompt=prompt,
            system_prompt=system,
            model=model,
            temperature=0.2  # Low temp for deterministic code gen
        )
        res = ai.ignite(req)
        return res.data.get("content", "") if res.success else f"<!-- AI_HERESY: {res.message} -->"
    except Exception as e:
        Logger.warn(f"Inline AI Prompt fractured: {e}")
        return f"<!-- AI_HERESY: {e} -->"


@lru_cache(maxsize=128)
def route_intent_rite(text: str, categories: str) -> str:
    """
    [ASCENSION 7]: THE SEMANTIC ROUTER.
    Classifies text into one of the provided categories (comma separated).
    Usage: {{ route_intent(commit_msg, "feature, bugfix, docs") }}
    """
    prompt = f"Categorize this text into EXACTLY ONE of these categories: [{categories}]. Text: '{text}'. Reply with ONLY the category word."
    res = ai_prompt_rite(prompt, system="You are a strict classifier. Output only the category name.", model="fast")
    # Clean up AI slop
    clean_res = re.sub(r'[^a-zA-Z0-9_-]', '', res).lower()
    return clean_res


# =============================================================================
# == THE DOMAIN OF THE EYE (TOPOGRAPHY & AST)                                ==
# =============================================================================

def find_files_rite(glob_pattern: str, root: str = ".") -> List[Dict[str, Any]]:
    """
    [ASCENSION 3]: THE TOPOGRAPHICAL RADAR.
    Scans the filesystem and returns an array of file objects.
    Usage: @for file in find_files('src/**/*.py'):
    """
    try:
        base_path = Path(os.environ.get("SCAFFOLD_PROJECT_ROOT", root)).resolve()
        results = []
        for path in base_path.rglob(glob_pattern):
            if path.is_file() and '.git' not in path.parts and 'node_modules' not in path.parts:
                results.append({
                    "name": path.name,
                    "stem": path.stem,
                    "ext": path.suffix,
                    "path": path.as_posix(),
                    "rel_path": str(path.relative_to(base_path)).replace('\\', '/')
                })
        return sorted(results, key=lambda x: x['rel_path'])
    except Exception as e:
        Logger.warn(f"Find Files fractured: {e}")
        return []


@lru_cache(maxsize=256)
def scry_ast_rite(file_path: str) -> Dict[str, Any]:
    """
    [ASCENSION 2]: THE AST SCRIER.
    Parses a physical file and returns its Tree-sitter AST Gnosis.
    Usage: {{ scry_ast('main.py').classes[0].name }}
    """
    try:
        from ...inquisitor import get_treesitter_gnosis
        base_path = Path(os.environ.get("SCAFFOLD_PROJECT_ROOT", ".")).resolve()
        target = (base_path / file_path).resolve()

        if not target.exists(): return {}
        content = target.read_text(encoding='utf-8', errors='ignore')

        gnosis = get_treesitter_gnosis(target, content)
        if "error" in gnosis: return {}
        return gnosis
    except Exception as e:
        Logger.warn(f"AST Scry fractured: {e}")
        return {}


def read_text_rite(file_path: str) -> str:
    """Reads a file's content as a string."""
    try:
        base_path = Path(os.environ.get("SCAFFOLD_PROJECT_ROOT", ".")).resolve()
        target = (base_path / file_path).resolve()
        if target.exists() and target.is_file():
            return target.read_text(encoding='utf-8', errors='ignore')
        return ""
    except:
        return ""


def read_json_rite(file_path: str) -> Dict[str, Any]:
    """[ASCENSION 6]: THE FORM READER (JSON)."""
    content = read_text_rite(file_path)
    try:
        return json.loads(content) if content else {}
    except:
        return {}


def read_yaml_rite(file_path: str) -> Dict[str, Any]:
    """[ASCENSION 6]: THE FORM READER (YAML)."""
    try:
        import yaml
        content = read_text_rite(file_path)
        return yaml.safe_load(content) if content else {}
    except:
        return {}


# =============================================================================
# == THE DOMAIN OF THE AETHER (NETWORK & DB)                                 ==
# =============================================================================

@lru_cache(maxsize=64)
def fetch_api_rite(url: str, method: str = "GET", headers: str = "{}") -> Any:
    """
    [ASCENSION 4]: THE AKASHIC NETWORK.
    Native HTTP client for the blueprint.
    Usage: {{ fetch_api('https://api.github.com/repos/novalym/scaffold').stargazers_count }}
    """
    try:
        import requests
        h_dict = json.loads(headers) if isinstance(headers, str) else headers
        res = requests.request(method, url, headers=h_dict, timeout=5.0)

        if res.headers.get('Content-Type', '').startswith('application/json'):
            return res.json()
        return res.text
    except Exception as e:
        Logger.warn(f"Network Fetch fractured: {e}")
        return {}


def scry_db_rite(connection_string: str, query: str) -> List[Dict[str, Any]]:
    """
    [ASCENSION 5]: THE DATABASE CONDUIT.
    Executes a SQL query and returns rows as dictionaries.
    Usage: @for table in scry_db(env('DB_URL'), "SELECT table_name FROM information_schema.tables"):
    """
    # Note: Requires SQLAlchemy/Psycopg2 in the host environment
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            result = conn.execute(text(query))
            return [dict(row._mapping) for row in result]
    except Exception as e:
        Logger.warn(f"Database Scry fractured: {e}")
        return []


# =============================================================================
# == THE DOMAIN OF ALCHEMY (STRINGS & LINGUISTICS)                           ==
# =============================================================================

def pluralize_rite(word: str) -> str:
    """[ASCENSION 9]: NLP Pluralization (Basic Heuristics)."""
    w = str(word)
    if w.endswith('y') and not w.endswith(('ay', 'ey', 'iy', 'oy', 'uy')): return w[:-1] + 'ies'
    if w.endswith(('s', 'sh', 'ch', 'x', 'z')): return w + 'es'
    return w + 's'


def singularize_rite(word: str) -> str:
    """[ASCENSION 9]: NLP Singularization."""
    w = str(word)
    if w.endswith('ies'): return w[:-3] + 'y'
    if w.endswith('es') and w[-3:-2] in ('s', 'c', 'x', 'z'): return w[:-2]
    if w.endswith('s') and not w.endswith('ss'): return w[:-1]
    return w


def regex_extract_rite(pattern: str, text: str, group: int = 1) -> str:
    """[ASCENSION 22]: Extract matching groups from text."""
    try:
        match = re.search(pattern, str(text))
        return match.group(group) if match else ""
    except:
        return ""


def json_path_rite(data: Union[Dict, str], path: str) -> Any:
    """[ASCENSION 12]: Navigate complex dicts like '$.users[0].name'."""
    try:
        import jsonpath_ng
        obj = json.loads(data) if isinstance(data, str) else data
        jsonpath_expr = jsonpath_ng.parse(path)
        match = jsonpath_expr.find(obj)
        if not match: return ""
        return match[0].value if len(match) == 1 else [m.value for m in match]
    except:
        return ""


def to_snake_rite(text: str) -> str:
    from ...utils import to_snake_case
    return to_snake_case(str(text))


def to_camel_rite(text: str) -> str:
    from ...utils import to_camel_case
    return to_camel_case(str(text))


def to_pascal_rite(text: str) -> str:
    from ...utils import to_pascal_case
    return to_pascal_case(str(text))


def b64_encode_rite(text: str) -> str:
    import base64
    return base64.b64encode(str(text).encode('utf-8')).decode('utf-8')


def b64_decode_rite(b64_str: str) -> str:
    import base64
    try:
        return base64.b64decode(str(b64_str)).decode('utf-8')
    except:
        return ""


# =============================================================================
# == THE DOMAIN OF SECRETS & IDENTITIES                                      ==
# =============================================================================

def get_secret_rite(key: str, default: str = "") -> str:
    """[ASCENSION 11]: Safely fetches a secret from Env or .env file."""
    # Priority: OS Env -> .env file -> Default
    val = os.getenv(key)
    if val: return val

    try:
        env_path = Path(os.environ.get("SCAFFOLD_PROJECT_ROOT", ".")) / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith(f"{key}="):
                    return line.split("=", 1)[1].strip().strip('"\'')
    except:
        pass
    return default


def uuid_v4_rite() -> str:
    return str(uuid.uuid4())


def hash_data_rite(data: str, algo: str = "sha256") -> str:
    """[ASCENSION 14]: Cryptographic Forge."""
    try:
        h = hashlib.new(algo)
        h.update(str(data).encode('utf-8'))
        return h.hexdigest()
    except:
        return ""


# =============================================================================
# == THE DOMAIN OF TIME & SYSTEM                                             ==
# =============================================================================

def now_rite(fmt: Any = '%Y-%m-%dT%H:%M:%SZ', tz: Any = 'utc') -> str:
    try:
        dt = datetime.datetime.now(datetime.timezone.utc) if tz == "utc" else datetime.datetime.now()
        if fmt == "iso": return dt.isoformat()
        return dt.strftime(str(fmt))
    except:
        return ""


def hardware_vitals_rite() -> Dict[str, Any]:
    """[ASCENSION 15]: Substrate Sensor."""
    try:
        import psutil
        return {
            "cpu_percent": psutil.cpu_percent(),
            "ram_percent": psutil.virtual_memory().percent,
            "os": platform.system(),
            "arch": platform.machine()
        }
    except:
        return {"cpu_percent": 0, "ram_percent": 0, "os": platform.system(), "arch": "unknown"}


def shell_rite(command: Any, timeout: Any = 60) -> str:
    """[LEGACY PRESERVED]: The Kinetic Conduit."""
    cmd_str = str(command).strip()
    try:
        result = subprocess.run(
            cmd_str, shell=True, capture_output=True, text=True,
            timeout=int(timeout), stdin=subprocess.DEVNULL
        )
        if result.returncode != 0: return ""
        return result.stdout.strip()
    except:
        return ""


def env_rite(key: str, default: str = "") -> str:
    return os.getenv(str(key), str(default))


# =============================================================================
# == THE REGISTRATION OF THE PANTHEON                                        ==
# =============================================================================

def inject_omniscience(env_globals: dict, env_filters: dict):
    """
    Sutures all 32 Ascended Faculties into the Jinja2 Environment.
    """
    # The Global Organs (Callable as functions)
    env_globals.update({
        "ai_prompt": ai_prompt_rite,
        "route_intent": route_intent_rite,
        "find_files": find_files_rite,
        "scry_ast": scry_ast_rite,
        "scry_db": scry_db_rite,
        "fetch_api": fetch_api_rite,
        "read_text": read_text_rite,
        "read_json": read_json_rite,
        "read_yaml": read_yaml_rite,
        "get_secret": get_secret_rite,
        "uuid": uuid_v4_rite,
        "uuid_v4": uuid_v4_rite,
        "hash_data": hash_data_rite,
        "hardware_vitals": hardware_vitals_rite,
        "now": now_rite,
        "shell": shell_rite,
        "env": env_rite,

        # Native Primitives
        "range": range,
        "list": list,
        "dict": dict,
        "len": len,
        "abs": abs,
        "int": int,
        "str": str,
        "bool": bool,
    })

    # The Alchemical Filters (Callable via pipe | )
    env_filters.update({
        "pluralize": pluralize_rite,
        "singularize": singularize_rite,
        "snake": to_snake_rite,
        "camel": to_camel_rite,
        "pascal": to_pascal_rite,
        "kebab": lambda x: to_snake_rite(x).replace('_', '-'),
        "regex_extract": regex_extract_rite,
        "json_path": json_path_rite,
        "b64_encode": b64_encode_rite,
        "b64_decode": b64_decode_rite,
        "to_json": lambda x: json.dumps(x, indent=2, default=str),
        "quote": shlex.quote,
        "hash": lambda x: hash_data_rite(x),
    })


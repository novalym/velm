# Path: artisans/dream/heuristic_engine/ner.py
# --------------------------------------------

import re
from typing import Dict, Any, List
from ....logger import Scribe

Logger = Scribe("Dream:NER")


class NamedEntityRecognizer:
    """
    =============================================================================
    == THE NAMED ENTITY RECOGNIZER (V-Ω-REGEX-PHALANX)                         ==
    =============================================================================
    LIF: 50,000x | ROLE: VARIABLE_EXTRACTOR

    Surgically extracts variable bindings from natural language without AI.
    It understands "Identity" (naming), "Topology" (ports), and "Substrate" (DBs).
    """

    # --- I. THE IDENTITY PHALANX ---
    _NAME_PATTERNS = [
        re.compile(r'(?:named|called|title[d]?|project)\s+(?P<val>[a-z0-9_-]+)', re.I),
        re.compile(r'name=["\']?(?P<val>[a-z0-9_-]+)["\']?', re.I),
        re.compile(
            r'(?:create|make|forge)\s+(?:a|an)\s+(?:new\s+)?(?:\w+\s+){0,3}(?P<val>[a-z0-9_-]+)\s*(?:app|project|service|api)',
            re.I)
    ]

    # --- II. THE TOPOLOGY PHALANX ---
    _PORT_PATTERNS = [
        re.compile(r'(?:on|at)\s+port\s+(?P<val>\d{4,5})', re.I),
        re.compile(r'port[:=]\s*(?P<val>\d{4,5})', re.I)
    ]

    # --- III. THE SUBSTRATE PHALANX ---
    _DB_MAP = {
        "postgres": "postgres", "postgresql": "postgres", "pg": "postgres",
        "mysql": "mysql", "mariadb": "mysql",
        "sqlite": "sqlite", "file db": "sqlite",
        "redis": "redis", "cache": "redis",
        "mongo": "mongo", "mongodb": "mongo"
    }

    _LANG_MAP = {
        "python": "python", "py": "python",
        "typescript": "typescript", "ts": "typescript", "node": "typescript",
        "javascript": "javascript", "js": "javascript",
        "rust": "rust", "rs": "rust",
        "go": "go", "golang": "go"
    }

    def extract(self, prompt: str) -> Dict[str, Any]:
        """
        The Rite of Extraction. Returns a dictionary of discovered Gnosis.
        """
        variables: Dict[str, Any] = {}
        text = prompt.strip()

        # 1. Scry Identity (Project Name)
        for pattern in self._NAME_PATTERNS:
            if match := pattern.search(text):
                # Heuristic check: Ensure we didn't capture a common stopword
                val = match.group("val")
                if val.lower() not in ("a", "an", "the", "new", "simple", "basic", "modern"):
                    variables['project_name'] = val
                    variables['project_slug'] = val
                    break

        # 2. Scry Topology (Ports)
        for pattern in self._PORT_PATTERNS:
            if match := pattern.search(text):
                try:
                    variables['port'] = int(match.group("val"))
                    break
                except ValueError:
                    pass

        # 3. Scry Substrate (Database)
        lower_text = text.lower()
        for key, val in self._DB_MAP.items():
            # Use word boundary to avoid partial matches
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                variables['database_type'] = val
                variables['use_database'] = True
                break

        # 4. Scry Tongue (Language)
        for key, val in self._LANG_MAP.items():
            if re.search(rf'\b{re.escape(key)}\b', lower_text):
                variables['language'] = val
                variables['project_type'] = val  # Common alias
                break

        # 5. Scry Boolean Flags (Adjectives)
        if "docker" in lower_text or "container" in lower_text:
            variables['use_docker'] = True
        if "git" in lower_text:
            variables['use_git'] = True
        if "auth" in lower_text or "login" in lower_text:
            variables['use_auth'] = True

        return variables
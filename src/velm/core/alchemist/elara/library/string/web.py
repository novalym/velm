# Path: core/alchemist/elara/library/string_rites/web.py
# ------------------------------------------------------

import urllib.parse
import json
import re
from typing import Any
from ..registry import register_rite

RE_HTML_TAGS = re.compile(r'<[^>]+>')

@register_rite("to_json")
def to_json(value: Any, indent: int = 2) -> str:
    from .....runtime.vessels import SovereignEncoder
    return json.dumps(value, indent=int(indent), cls=SovereignEncoder, ensure_ascii=False)

@register_rite("from_json")
def from_json(value: str) -> Any:
    if not value: return {}
    try: return json.loads(value)
    except Exception: return {}

@register_rite("url_encode")
def url_encode(value: Any) -> str:
    return urllib.parse.quote(str(value))

@register_rite("to_query_string")
def to_query_string(value: Any) -> str:
    """[ASCENSION 15]: Query String Forger."""
    try:
        if isinstance(value, dict):
            return "?" + urllib.parse.urlencode(value)
    except Exception: pass
    return ""

@register_rite("safe_path")
def safe_path_rite(value: Any) -> str:
    """[ASCENSION 16]: URI Path Sanitizer."""
    try:
        s = str(value)
        # Banish directory traversal
        s = s.replace("../", "").replace("..\\", "")
        # Banish illegal OS characters
        s = re.sub(r'[<>:"|?*]', "", s)
        return s.strip()
    except Exception: return ""

@register_rite("strip_tags")
def strip_html_tags(value: Any) -> str:
    """[ASCENSION 17]: The HTML Exorcist."""
    try:
        return RE_HTML_TAGS.sub('', str(value))
    except Exception: return str(value)
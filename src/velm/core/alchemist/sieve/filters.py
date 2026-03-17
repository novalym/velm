# Path: core/alchemist/sieve/filters.py
# -------------------------------------


import re
import json
import html
import base64
import hashlib
from typing import Any, Dict, Final, Optional

from ....logger import Scribe

Logger = Scribe("ApophaticFilterGrimoire")


class ApophaticFilterGrimoire:
    """
    =============================================================================
    == THE APOPHATIC FILTER GRIMOIRE (V-Ω-TOTALITY-O1-SUTURE)                  ==
    =============================================================================
    LIF: ∞ | ROLE: ZERO_LATENCY_TRANSMUTATOR

    [ASCENSION 13 & 34]: A native, hard-coded dictionary of filters that can be
    executed without ever waking the AST or the primary Alchemist environment.
    Supports argument parsing natively.
    """

    @classmethod
    def apply(cls, value: Any, filter_stmt: str, gnosis: Dict[str, Any]) -> Any:
        """
        Parses `filter(arg1, arg2)` and routes it to the static grimoire.
        """
        match = re.match(r'^(?P<name>[a-zA-Z0-9_]+)(?:\((?P<args>.*?)\))?$', filter_stmt)
        if not match:
            return value

        name = match.group("name").lower()
        args_str = match.group("args")

        # Extract arguments safely
        args =[]
        if args_str:
            # Simple CSV split respecting quotes
            # (In the Sieve, we keep it lightweight)
            import shlex
            try:
                args = [a.strip().strip('"\'') for a in shlex.split(args_str)]
            except Exception:
                args = [a.strip().strip('"\'') for a in args_str.split(',')]

        # --- 1. THE SAVIOR (DEFAULT / D) ---
        if name in ('default', 'd', 'coalesce'):
            default_val = args[0] if args else ""
            if value is None or value == "" or str(value).lower() in ('none', 'null', 'void'):
                return default_val
            return value

        # --- 2. O(1) GRIMOIRE DISPATCH ---
        handler = getattr(cls, f"_filter_{name}", None)
        if handler:
            try:
                return handler(value, *args)
            except Exception as e:
                Logger.debug(f"Sieve Filter '{name}' fractured: {e}")
                return value

        return value

    # =========================================================================
    # == NATIVE FILTER IMPLEMENTATIONS                                       ==
    # =========================================================================

    @staticmethod
    def _filter_snake(v: Any, *args) -> str:
        s = str(v).replace("-", "_").replace(" ", "_")
        return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower().strip('_')

    @staticmethod
    def _filter_slug(v: Any, *args) -> str:
        return str(v).lower().replace("_", "-").replace(" ", "-")

    @staticmethod
    def _filter_kebab(v: Any, *args) -> str:
        return ApophaticFilterGrimoire._filter_slug(v)

    @staticmethod
    def _filter_pascal(v: Any, *args) -> str:
        return "".join(x.title() for x in re.split(r'[^a-zA-Z0-9]', str(v)))

    @staticmethod
    def _filter_camel(v: Any, *args) -> str:
        s = ApophaticFilterGrimoire._filter_pascal(v)
        return s[0].lower() + s[1:] if s else ""

    @staticmethod
    def _filter_upper(v: Any, *args) -> str:
        return str(v).upper()

    @staticmethod
    def _filter_lower(v: Any, *args) -> str:
        return str(v).lower()

    @staticmethod
    def _filter_title(v: Any, *args) -> str:
        return str(v).title()

    @staticmethod
    def _filter_trim(v: Any, *args) -> str:
        return str(v).strip()

    @staticmethod
    def _filter_len(v: Any, *args) -> int:
        return len(v) if hasattr(v, '__len__') else 0

    @staticmethod
    def _filter_json(v: Any, *args) -> str:
        indent = int(args[0]) if args and args[0].isdigit() else 2
        return json.dumps(v, indent=indent, ensure_ascii=False)

    @staticmethod
    def _filter_e(v: Any, *args) -> str:
        return html.escape(str(v))

    @staticmethod
    def _filter_escape(v: Any, *args) -> str:
        return html.escape(str(v))

    @staticmethod
    def _filter_b64encode(v: Any, *args) -> str:
        return base64.b64encode(str(v).encode()).decode()

    @staticmethod
    def _filter_hash(v: Any, *args) -> str:
        algo = args[0] if args else "sha256"
        data = str(v).encode()
        try:
            return hashlib.new(algo, data).hexdigest()
        except ValueError:
            return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _filter_join(v: Any, *args) -> str:
        sep = args[0] if args else ""
        if isinstance(v, (list, tuple, set)):
            return sep.join(str(x) for x in v)
        return str(v)
# Path: scaffold/artisans/definition/oracle.py
# -------------------------------------------

import re
from pathlib import Path
from typing import Dict, Optional, List, Any, TYPE_CHECKING

from ...contracts.data_contracts import GnosticLineType
from ...logger import Scribe

if TYPE_CHECKING:
    from ...core.runtime.engine import ScaffoldEngine
    from ...core.cortex.engine import GnosticCortex

Logger = Scribe("OriginOracle")


class OriginOracle:
    """
    =============================================================================
    == THE ORACLE OF ORIGINS (V-Ω-MULTIDIMENSIONAL-TRIAGE)                     ==
    =============================================================================
    LIF: 1,000,000,000,000

    The cognitive core of the Definition system. It performs a hierarchical,
    multi-vector triage to locate the genesis of any token.

    ### THE PANTHEON OF 4 GAZES:
    1. **The Local Gaze:** Scans the current document for variable definitions.
    2. **The Cortex Gaze:** Queries the global symbol map for code entities.
    3. **The Canon Gaze:** Consults the language grimoire for internal keywords.
    4. **The Seed Gaze:** Resolves file paths used in seeding directives.
    """

    def __init__(self, engine: 'ScaffoldEngine', cortex: 'GnosticCortex', project_root: Path, current_path: Path):
        self.engine = engine
        self.cortex = cortex
        self.root = project_root
        self.current_path = current_path

    def find_origin(self, token: str, content: str) -> Optional[Dict[str, Any]]:
        """The Grand Triage. Orders the Gazes by probability of intent."""

        # 1. Local variable check (Highest priority in Blueprints)
        if local := self._gaze_local(token, content):
            return local

        # 2. Cortex check (Highest priority in Source Code)
        if cortex_hit := self._gaze_cortex(token):
            return cortex_hit

        # 3. Canon check (Directives/Sigils)
        if canon_hit := self._gaze_canon(token):
            return canon_hit

        # 4. Seed check (File paths)
        if seed_hit := self._gaze_seed(token):
            return seed_hit

        return None

    def _gaze_local(self, token: str, content: str) -> Optional[Dict[str, Any]]:
        """Scans for $$ name, let name, or def name."""
        pattern = re.compile(fr'^\s*(?:\$\$|let|def|const)?\s*{re.escape(token)}\s*[:=]', re.MULTILINE)
        match = pattern.search(content)
        if match:
            line_idx = content.count('\n', 0, match.start())
            return {
                "uri": self.current_path.as_uri(),
                "range": {
                    "start": {"line": line_idx, "character": 0},
                    "end": {"line": line_idx, "character": 0}
                }
            }
        return None

    def _gaze_cortex(self, token: str) -> Optional[Dict[str, Any]]:
        """Consults the GnosticCortex for symbol definitions."""
        if not self.cortex._memory or not self.cortex._memory.symbol_map:
            return None

        def_path_str = self.cortex._memory.symbol_map.get(token)
        if not def_path_str:
            return None

        target_path = (self.root / def_path_str).resolve()
        file_gnosis = self.cortex._memory.project_gnosis.get(str(def_path_str), {})

        line_num = 0
        # Find exact line in pre-computed AST metrics
        all_symbols = file_gnosis.get("functions", []) + file_gnosis.get("classes", [])
        for sym in all_symbols:
            if sym.get("name") == token:
                # Use start_point if available, fallback to 1-indexed lineno
                if "start_point" in sym:
                    line_num = sym["start_point"][0]
                elif "lineno" in sym:
                    line_num = sym["lineno"] - 1
                break

        return {
            "uri": target_path.as_uri(),
            "range": {
                "start": {"line": line_num, "character": 0},
                "end": {"line": line_num, "character": 0}
            }
        }

    def _gaze_canon(self, token: str) -> Optional[Dict[str, Any]]:
        """Consults Introspection data for language origin."""
        # Note: This requires the 'source' metadata we added to the Canon
        # in the 'gnosis/canon.py' Apotheosis.
        from ..introspect import IntrospectionArtisan
        res = self.engine.dispatch(self.engine.registry.get_request_type("introspect")(topic="all"))
        if not res.success or not res.data: return None

        canon = res.data
        pools = [
            canon.get("scaffold_language", {}).get("sigils", []),
            canon.get("scaffold_language", {}).get("directives", {}).get("pantheon", []),
            canon.get("symphony_language", {}).get("directives", {}).get("pantheon", [])
        ]

        for pool in pools:
            for entry in pool:
                name = entry.get("token", entry.get("name", "")).split(' ')[0]
                if (name == token or name == f"@{token}") and entry.get("source"):
                    src = entry["source"]
                    return {
                        "uri": (self.root / src['file']).as_uri(),
                        "range": {
                            "start": {"line": src['line'] - 1, "character": 0},
                            "end": {"line": src['line'] - 1, "character": 0}
                        }
                    }
        return None

    def _gaze_seed(self, token: str) -> Optional[Dict[str, Any]]:
        """Checks if the token is a valid file path (for << seeding)."""
        # Resolve relative to current blueprint
        candidate = (self.current_path.parent / token).resolve()
        if candidate.is_file() and str(candidate).startswith(str(self.root)):
            return {
                "uri": candidate.as_uri(),
                "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}}
            }
        return None


# Path: scaffold/core/structure_sentinel/strategies/python_strategy/semantic/harvester.py
# ---------------------------------------------------------------------------------------


import re
from pathlib import Path
from typing import List, Set

# We import the Gnostic Inquisitor, but we prepare for its absence via the Low Gaze.
from ......inquisitor import get_treesitter_gnosis
from ......logger import Scribe

Logger = Scribe("SymbolHarvester")


class SymbolHarvester:
    """
    =============================================================================
    == THE REAPER OF SYMBOLS (V-Ω-DUAL-GAZE-ULTIMA)                            ==
    =============================================================================
    LIF: 10,000,000,000,000

    Extracts the 'Soul' of a Python scripture—the symbols that are meant to be
    exposed to the world.

    It possesses a **Dual Gaze**:
    1.  **The High Gaze:** Tree-sitter (Precise, Structural).
    2.  **The Low Gaze:** Regex (Robust, Fallback).

    It enforces the Laws of Privacy (underscores), Separation (tests), and
    Purpose (scripts).
    """

    # [FACULTY 2 & 3 & 4 & 5] The Low Gaze Grimoire (Regexes)
    REGEX_CLASS = re.compile(r"^\s*class\s+([a-zA-Z_]\w*)", re.MULTILINE)
    REGEX_FUNC = re.compile(r"^\s*(?:async\s+)?def\s+([a-zA-Z_]\w*)", re.MULTILINE)
    REGEX_CONST = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=", re.MULTILINE)
    REGEX_TYPE = re.compile(r"^([a-zA-Z_]\w*)\s*:\s*TypeAlias\s*=", re.MULTILINE)

    def harvest(self, file_path: Path, content: str) -> List[str]:
        """
        The Rite of Harvest.
        Returns a sorted list of public symbol names found in the content.
        """
        # [FACULTY 8] The Test Ward & [FACULTY 7] The Script Guard
        # If the file is not a library module, we harvest nothing.
        if self._is_script_or_test(file_path, content):
            return []

        symbols: Set[str] = set()

        # --- MOVEMENT I: THE HIGH GAZE (TREE-SITTER) ---
        # We attempt to parse the AST for maximum precision.
        high_gaze_success = False
        try:
            gnosis = get_treesitter_gnosis(file_path, content)
            if "error" not in gnosis:
                # Harvest Classes
                for cls in gnosis.get('classes', []):
                    if self._is_public(cls['name']):
                        symbols.add(cls['name'])

                # Harvest Functions
                for func in gnosis.get('functions', []):
                    if self._is_public(func['name']):
                        symbols.add(func['name'])

                high_gaze_success = True
            else:
                # [FACULTY 11] Luminous Logging
                # Only log verbose warnings if TS fails, not errors, as fallback exists.
                Logger.verbose(f"Harvester's High Gaze clouded on '{file_path.name}'. Reason: {gnosis.get('error')}")

        except Exception as e:
            # [FACULTY 10] The Unbreakable Ward
            Logger.warn(f"Harvester's High Gaze shattered by paradox on '{file_path.name}': {e}")

        # --- MOVEMENT II: THE LOW GAZE (REGEX) ---
        # [FACULTY 2] The Regex Fallback
        # We ALWAYS run the Low Gaze for Constants and TypeAliases (which TS might miss depending on query),
        # AND we run it for Classes/Funcs if the High Gaze failed.

        # 1. Harvest Constants [FACULTY 4]
        for match in self.REGEX_CONST.finditer(content):
            name = match.group(1)
            if self._is_public(name):
                symbols.add(name)

        # 2. Harvest TypeAliases [FACULTY 5]
        for match in self.REGEX_TYPE.finditer(content):
            name = match.group(1)
            if self._is_public(name):
                symbols.add(name)

        # 3. Fallback for Classes/Funcs if High Gaze failed
        if not high_gaze_success:
            Logger.verbose(f"Engaging Low Gaze (Regex) for '{file_path.name}'...")

            for match in self.REGEX_CLASS.finditer(content):
                name = match.group(1)
                if self._is_public(name):
                    symbols.add(name)

            # [FACULTY 3] Async Awareness included in Regex
            for match in self.REGEX_FUNC.finditer(content):
                name = match.group(1)
                if self._is_public(name):
                    symbols.add(name)

        # [FACULTY 9] The Robust Merge is implicit in the Set usage.

        # [FACULTY 12] The Sorted Proclamation
        return sorted(list(symbols))

    def _is_public(self, name: str) -> bool:
        """
        [FACULTY 6] The Privacy Filter.
        Adjudicates if a symbol is public API (no leading underscore).
        """
        return not name.startswith('_')

    def _is_script_or_test(self, path: Path, content: str) -> bool:
        """
        [FACULTY 7 & 8] The Script Guard & Test Ward.
        Adjudicates if the file is a script or test, unworthy of export.
        """
        name = path.name

        # 1. Test Ward
        if name.startswith("test_") or name.endswith("_test.py"):
            return True
        if name in ("conftest.py", "setup.py", "manage.py", "wsgi.py", "asgi.py"):
            return True

        # 2. Script Guard
        # If it has a main block, it is likely an entry point, not a library module.
        # While some modules have main blocks for testing, they are rarely exported via __init__.
        if 'if __name__ == "__main__":' in content or "if __name__ == '__main__':" in content:
            return True

        return False


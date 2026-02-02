# Path: artisans/distill/core/skeletonizer/utils.py
# -------------------------------------------------

import re
from typing import List, Dict, Optional, Set


class SurgicalUtils:
    """
    =============================================================================
    == THE SURGICAL TRAY (SHARED INSTRUMENTS)                                  ==
    =============================================================================
    """

    SACRED_SYMBOLS = {
        '__init__', 'main', 'run', 'setup', 'create_app',  # Python
        'constructor', 'ngOnInit', 'componentDidMount', 'render',  # JS/TS
        'init', 'ServeHTTP',  # Go
        'initialize'  # Ruby
    }

    @staticmethod
    def get_sorted_nodes(dossier: Dict) -> List[Dict]:
        """Combines functions and classes and sorts by line number."""
        nodes = dossier.get("classes", []) + dossier.get("functions", [])
        nodes.sort(key=lambda x: x.get('start_point', [0, 0])[0])
        return nodes

    @staticmethod
    def summarize_imports(dossier: Dict, comment_char: str) -> List[str]:
        """
        [FACULTY 4] Condenses imports into a single summary line.
        NOW ROBUST against Dictionary objects.
        """
        raw_imports = dossier.get("dependencies", {}).get("imports", [])
        if not raw_imports: return []

        # Normalization Loop
        clean_imports = []
        for imp in raw_imports:
            if isinstance(imp, dict):
                # Extract path from rich object
                if 'path' in imp:
                    clean_imports.append(imp['path'])
            elif isinstance(imp, str):
                clean_imports.append(imp)

        # Remove duplicates and sort
        clean_imports = sorted(list(set(clean_imports)))

        if not clean_imports: return []

        lines = []
        lines.append(f"{comment_char} --- Dependencies ---")

        count = len(clean_imports)

        if count <= 5:
            lines.append(f"{comment_char} Imports: {', '.join(clean_imports)}")
        else:
            top_5 = clean_imports[:5]
            lines.append(f"{comment_char} Imports: {', '.join(top_5)}, ... (+{count - 5} more)")

        lines.append("")
        return lines

    @staticmethod
    def scan_globals(lines: List[str], pattern: str, comment_char: str) -> List[str]:
        """[FACULTY 5] Finds global constants to preserve configuration."""
        found = []
        # Scan header area
        scan_limit = min(len(lines), 100)

        for line in lines[:scan_limit]:
            if re.match(pattern, line.strip()):
                found.append(line.strip())

        if found:
            result = [f"{comment_char} --- Global Configuration ---"]
            result.extend(found)
            result.append("")
            return result
        return []

    @staticmethod
    def adjudicate_relevance(
            name: str,
            docstring: str,
            active_symbols: Optional[Set[str]],
            focus_keywords: List[str],
            is_stub_mode: bool
    ) -> bool:
        """
        [THE GAZE OF JUDGMENT]
        Decides if a symbol is worthy of the Full Gaze or the Knife.
        """
        # [FACULTY 2] Apophatic Filter: In stub mode, we prune everything not essential
        if is_stub_mode:
            return True

        # 1. Sacred Symbols are always kept
        if name in SurgicalUtils.SACRED_SYMBOLS:
            return True

        # 2. Semantic Resonance (Focus)
        if focus_keywords:
            search_space = (name + " " + (docstring or "")).lower()
            if any(k in search_space for k in focus_keywords):
                return True

        # 3. Causal Necessity (Active Symbols)
        if active_symbols is not None:
            return name in active_symbols

        # Default: Keep it (Conservative)
        return True


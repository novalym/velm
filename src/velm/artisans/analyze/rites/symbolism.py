# Path: artisans/analyze/rites/symbolism.py
# -----------------------------------------

import re
from typing import List, Dict, Any
from ..reporting.diagnostics import DiagnosticForge


class RiteOfSymbolism:
    """
    =============================================================================
    == THE RITE OF SYMBOLISM (V-Ω-OUTLINE-GENESIS)                             ==
    =============================================================================
    Preserves `_rite_of_symbolism`.
    Extracts outline symbols from parsed items and variables.
    """

    @staticmethod
    def conduct(content: str, items: List[Any], edicts: List[Any], variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        symbols = []

        # 1. Variables (Shared across Scaffold/Symphony)
        for var_name in variables.keys():
            # Heuristic regex to find definition line
            match = re.search(fr'^\s*(?:\$\$|let|def|const)?\s*{re.escape(var_name)}\s*[:=]', content, re.MULTILINE)
            if match:
                l = content.count('\n', 0, match.start())
                symbols.append({
                    "name": var_name,
                    "detail": "Gnostic Variable",
                    "kind": 13,  # Variable
                    "range": DiagnosticForge.make_range(l),
                    "selectionRange": DiagnosticForge.make_range(l)
                })

        # 2. Scaffold Items (Files/Directories)
        for item in items:
            if hasattr(item, 'line_num') and item.line_num > 0 and item.path:
                # Deduplicate
                if not any(s['name'] == str(item.path) for s in symbols):
                    kind = 19 if item.is_dir else 17  # Folder / File
                    symbols.append({
                        "name": str(item.path),
                        "detail": "Sanctum" if item.is_dir else "Scripture",
                        "kind": kind,
                        "range": DiagnosticForge.make_range(item.line_num - 1),
                        "selectionRange": DiagnosticForge.make_range(item.line_num - 1)
                    })

        # 3. Symphony Edicts (Actions/Vows)
        for edict in edicts:
            if hasattr(edict, 'line_num') and edict.line_num > 0:
                name = edict.command or edict.vow_type or "Unknown Edict"
                symbols.append({
                    "name": name,
                    "detail": str(edict.type),
                    "kind": 12,  # Function/Method
                    "range": DiagnosticForge.make_range(edict.line_num - 1),
                    "selectionRange": DiagnosticForge.make_range(edict.line_num - 1)
                })

        return symbols
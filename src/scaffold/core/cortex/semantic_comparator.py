# Path: scaffold/core/cortex/semantic_comparator.py
# -------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class SemanticChange:
    symbol_name: str
    symbol_type: str  # function, class
    change_type: str  # ADDED, REMOVED, MODIFIED, MOVED
    details: str
    old_loc: Optional[int] = None
    new_loc: Optional[int] = None


class SemanticComparator:
    """
    =============================================================================
    == THE GNOSTIC COMPARATOR (V-Ω-AST-DIFFERENTIAL)                           ==
    =============================================================================
    LIF: 10,000,000,000

    Compares the souls of two scriptures, ignoring whitespace and formatting.
    """

    def compare(self, old_gnosis: Dict[str, Any], new_gnosis: Dict[str, Any]) -> List[SemanticChange]:
        changes = []

        # 1. Flatten Gnosis into Symbol Maps
        old_symbols = self._flatten_symbols(old_gnosis)
        new_symbols = self._flatten_symbols(new_gnosis)

        all_keys = set(old_symbols.keys()) | set(new_symbols.keys())

        for key in all_keys:
            old = old_symbols.get(key)
            new = new_symbols.get(key)

            if not old:
                changes.append(SemanticChange(key, new['type'], "ADDED", "New symbol born.", new_loc=new['line']))
            elif not new:
                changes.append(
                    SemanticChange(key, old['type'], "REMOVED", "Symbol returned to void.", old_loc=old['line']))
            else:
                # MODIFIED CHECK
                # Check 1: Location Move
                # We consider it a move if it shifted significantly (> 5 lines)
                is_moved = abs(new['line'] - old['line']) > 5

                # Check 2: Signature/Complexity Change
                # We use the byte size of the body or complexity score if available
                # Tree-sitter 'start_byte' vs 'end_byte' gives size
                old_size = old['end_byte'] - old['start_byte']
                new_size = new['end_byte'] - new['start_byte']
                size_delta = new_size - old_size

                # Check 3: Complexity
                old_cc = old.get('complexity', 0)
                new_cc = new.get('complexity', 0)

                details = []
                if is_moved: details.append(f"Moved (L{old['line']} -> L{new['line']})")
                if abs(size_delta) > 10: details.append(f"Body changed ({size_delta:+} bytes)")
                if old_cc != new_cc: details.append(f"Complexity {old_cc} -> {new_cc}")

                if details:
                    change_type = "MOVED" if is_moved and len(details) == 1 else "MODIFIED"
                    changes.append(SemanticChange(
                        key, old['type'], change_type, ", ".join(details),
                        old_loc=old['line'], new_loc=new['line']
                    ))

        return changes

    def _flatten_symbols(self, gnosis: Dict) -> Dict[str, Dict]:
        """
        Extracts functions and classes into a flat map: 'Name' -> Meta
        """
        symbols = {}
        for func in gnosis.get('functions', []):
            symbols[func['name']] = {
                'type': 'Function',
                'line': func['start_point'][0] + 1,
                'start_byte': func['start_byte'],
                'end_byte': getattr(func, 'end_byte', 0),  # Assume inquisitor provides this
                'complexity': func.get('cyclomatic_complexity', 0)
            }
        for cls in gnosis.get('classes', []):
            symbols[cls['name']] = {
                'type': 'Class',
                'line': cls['start_point'][0] + 1,
                'start_byte': cls['start_byte'],
                'end_byte': getattr(cls, 'end_byte', 0),
                'complexity': 0
            }
        return symbols
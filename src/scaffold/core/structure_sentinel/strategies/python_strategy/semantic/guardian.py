# Path: scaffold/core/structure_sentinel/strategies/python_strategy/semantic/guardian.py
# --------------------------------------------------------------------------------------


import ast
import re
from typing import List, Set, Optional

from ..base_faculty import BaseFaculty
from ..contracts import SharedContext


class ApiGuardian(BaseFaculty):
    """
    =============================================================================
    == THE SHIELD OF EXPORTS (V-Ω-AST-STYLISTIC-SURGEON-ULTIMA)                ==
    =============================================================================
    LIF: 10,000,000,000,000

    Manages the `__all__` list with surgical precision.
    It ensures the module's public interface is explicit, sorted, and
    formatted for the ages.
    """

    # Matches: # SCAFFOLD: __all__ (tolerant of whitespace)
    ANCHOR_REGEX = re.compile(r'#\s*SCAFFOLD:\s*__all__', re.IGNORECASE)

    def guard(self, content: str, new_symbols: List[str], context: SharedContext) -> str:
        """
        The Rite of Export Guarding.
        Ensures all `new_symbols` are present in `__all__`.
        """
        if not new_symbols:
            return content

        # [FACULTY 8] The Syntax Ward
        try:
            tree = ast.parse(content)
        except SyntaxError:
            self.logger.warn("Syntax Heresy perceived in scripture. The Guardian stays its hand.")
            return content

        # [FACULTY 5] The AST Surgeon
        # Check if __all__ ALREADY exists as code
        all_node = self._find_dunder_all_node(tree)
        current_exports = self._extract_current_exports(all_node) if all_node else set()

        # [FACULTY 7] The Merge Strategy
        symbols_to_add = {s for s in new_symbols if s not in current_exports}

        # [FACULTY 9] Idempotency Check
        # If all symbols are present and the node exists, we do nothing.
        if not symbols_to_add and all_node:
            return content

        # [FACULTY 4] The Sorting Hat
        final_exports = sorted(list(current_exports) + list(symbols_to_add))

        if all_node:
            self.logger.verbose(f"   -> Merging {len(symbols_to_add)} new symbol(s) into existing `__all__`.")
            return self._rewrite_existing_all(content, all_node, final_exports)
        else:
            self.logger.verbose(f"   -> Forging new `__all__` with {len(final_exports)} symbol(s)...")
            return self._forge_new_all(content, final_exports)

    def _find_dunder_all_node(self, tree: ast.AST) -> Optional[ast.AST]:
        """Scans the AST for the `__all__` assignment."""
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        return node
        return None

    def _extract_current_exports(self, node: ast.AST) -> Set[str]:
        """Extracts strings from `__all__ = [...]`."""
        exports = set()
        if isinstance(node, ast.Assign) and isinstance(node.value, (ast.List, ast.Tuple)):
            for elt in node.value.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    exports.add(elt.value)
                elif isinstance(elt, ast.Str):  # Python < 3.8
                    exports.add(elt.s)
        return exports

    def _rewrite_existing_all(self, content: str, node: ast.AST, final_exports: List[str]) -> str:
        """Surgically replaces the existing assignment."""
        lines = content.splitlines(keepends=True)
        new_stmt = self._forge_vertical_all(final_exports)

        # AST line numbers are 1-based
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1

        # [FACULTY 10] Preserve Indentation (unlikely for module level __all__, but safe)
        indent = lines[start_line][:len(lines[start_line]) - len(lines[start_line].lstrip())]
        if indent:
            new_stmt = "\n".join([indent + l for l in new_stmt.splitlines()]) + "\n"

        lines[start_line:end_line] = [new_stmt]
        return "".join(lines)

    def _forge_new_all(self, content: str, final_exports: List[str]) -> str:
        """
        Creates a new __all__ assignment.
        Hunts for the # SCAFFOLD: __all__ anchor.
        """
        new_stmt = self._forge_vertical_all(final_exports)
        lines = content.splitlines(keepends=True)

        # [THE ANCHOR SEEKER V2]
        # Use regex to find the marker robustly
        anchor_idx = -1
        for i, line in enumerate(lines):
            if self.ANCHOR_REGEX.search(line):
                anchor_idx = i
                break

        if anchor_idx != -1:
            # [THE FIX: BREATHING ROOM & ANNIHILATION]
            # 1. We check if there's already a blank line before the marker.
            #    If not, we add one to separate from imports.
            prefix = ""
            if anchor_idx > 0 and lines[anchor_idx - 1].strip():
                prefix = "\n"

            # 2. We preserve the indentation of the marker.
            leading_whitespace = lines[anchor_idx][:len(lines[anchor_idx]) - len(lines[anchor_idx].lstrip())]

            if leading_whitespace:
                # Indent every line of the new statement
                indented_stmt = "\n".join([leading_whitespace + l for l in new_stmt.splitlines()]) + "\n"
                # Replace the marker line entirely
                lines[anchor_idx] = prefix + indented_stmt
            else:
                # Replace the marker line entirely
                lines[anchor_idx] = prefix + new_stmt

            return "".join(lines)

        # [FACULTY 11] The Fallback Append (If no marker found)
        if lines and not lines[-1].endswith('\n'):
            lines[-1] += '\n'

        # Ensure a gap from previous content
        if lines and lines[-1].strip():
            lines.append("\n")

        lines.append(new_stmt)
        return "".join(lines)

    def _forge_vertical_all(self, exports: List[str]) -> str:
        """
        [FACULTY 1] The Vertical Scroll.
        Forges:
        __all__ = [
            "SymbolA",
            "SymbolB",
        ]
        """
        stmt = "__all__ = [\n"
        for sym in exports:
            stmt += f'    "{sym}",\n'
        stmt += "]\n"
        return stmt

    def _validate_syntax(self, content: str, context: str):
        """[FACULTY 12] The Paranoid Validator."""
        try:
            ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"Guardian generated invalid syntax for {context}: {e}")
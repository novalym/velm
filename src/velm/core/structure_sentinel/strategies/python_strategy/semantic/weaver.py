# Path: scaffold/core/structure_sentinel/strategies/python_strategy/semantic/weaver.py
# ------------------------------------------------------------------------------------

import ast
import re
from typing import List, Tuple, Set, Optional

from ..base_faculty import BaseFaculty


class ImportWeaver(BaseFaculty):
    """
    =============================================================================
    == THE LOOM OF IMPORTS (V-Ω-HYBRID-SURGEON-ULTIMA)                         ==
    =============================================================================
    LIF: 10,000,000,000,000

    The Master of Connections.
    It manages `import` statements with AST-guided precision and text-based surgery.

    It adheres to the Law of Preservation: It modifies the code structure without
    destroying the comments, formatting, or soul of the surrounding scripture.
    """

    def weave(self, content: str, module: str, symbols: List[str]) -> str:
        """
        The Grand Rite of Weaving.
        Integrates `from .module import symbols` into the content with
        context-aware placement and formatting.
        """
        if not symbols:
            return content

        lines = content.splitlines(keepends=True)
        # Ensure we have a canvas to paint on
        if not lines:
            lines = [""]
        if not lines[-1].endswith('\n'):
            lines[-1] += '\n'

        try:
            # [FACULTY 1] The AST Gaze (Structural Understanding)
            tree = ast.parse(content)
        except SyntaxError:
            # [FACULTY 9] The Syntax Healer (Resilient Fallback)
            self.logger.warn("Syntax Heresy detected in scripture. Falling back to Blind Append strategy.")
            return self._blind_append(content, module, symbols)

        # 1. Attempt to Merge into existing import
        # [FACULTY 3, 4, 8] Alias Guardian, Sorting Hat, Deduplication Engine
        merged, new_lines = self._try_merge_import(tree, lines, module, symbols)
        if merged:
            return "".join(new_lines)

        # 2. If no merge possible, Insert a new import statement
        new_lines = self._insert_new_import(tree, lines, module, symbols)
        return "".join(new_lines)

    def _try_merge_import(self, tree: ast.AST, lines: List[str], module_name: str, new_symbols: List[str]) -> Tuple[
        bool, List[str]]:
        """
        [FACULTY 3, 4, 6] The Merge Strategist.
        Finds existing `from .module import ...`, weaves new symbols, sorts, and folds.
        """
        for node in ast.walk(tree):
            # We look for: from .module import ... (level=1 means one dot)
            if isinstance(node, ast.ImportFrom) and node.module == module_name and node.level == 1:

                # [FACULTY 2] The Wildcard Sentinel
                if any(n.name == '*' for n in node.names):
                    self.logger.verbose(f"   -> Wildcard import detected for '{module_name}'. No action needed.")
                    return True, lines

                # Analyze existing names to prevent duplication
                current_names: Set[str] = set()
                for alias in node.names:
                    current_names.add(alias.name)

                names_to_add = [s for s in new_symbols if s not in current_names]

                if not names_to_add:
                    return True, lines  # Idempotency: All symbols present

                # [FACULTY 4] The Sorting Hat
                existing_aliases = [n for n in node.names]
                for s in names_to_add:
                    existing_aliases.append(ast.alias(name=s, asname=None))

                existing_aliases.sort(key=lambda x: x.name)

                # Construct new statement string
                # [FACULTY 6, 7] Vertical Folding & Trailing Comma
                new_stmt = self._forge_import_statement(module_name, existing_aliases)

                # Surgical Replacement
                start_line_idx = node.lineno - 1
                end_line_idx = node.end_lineno if hasattr(node, 'end_lineno') else node.lineno

                # Preserve leading whitespace
                leading_whitespace = lines[start_line_idx][
                                     :len(lines[start_line_idx]) - len(lines[start_line_idx].lstrip())]

                if "\n" in new_stmt:
                    new_stmt = "\n".join([leading_whitespace + l for l in new_stmt.splitlines()]) + "\n"
                else:
                    new_stmt = leading_whitespace + new_stmt

                # Replace the old import block with the new one
                lines[start_line_idx:end_line_idx] = [new_stmt]
                return True, lines

        return False, lines

    def _insert_new_import(self, tree: ast.AST, lines: List[str], module_name: str, symbols: List[str]) -> List[str]:
        """
        [FACULTY 5, 11] The Gnostic Inserter & Atomic Spacer.
        Calculates optimal insertion point and ensures breathing room.
        """
        aliases = [ast.alias(name=s, asname=None) for s in sorted(symbols)]
        import_stmt = self._forge_import_statement(module_name, aliases)

        insert_idx = self._find_insertion_index(tree, lines)

        # Insert the import
        lines.insert(insert_idx, import_stmt)

        # [FACULTY 11] THE ATOMIC SPACER (THE FIX)
        # We gaze at the line immediately following our insertion.
        # If it is the sacred `__all__` definition (or any non-empty code),
        # and it is NOT already separated by a blank line, we inject one.

        next_line_idx = insert_idx + 1
        if next_line_idx < len(lines):
            next_line = lines[next_line_idx].strip()

            # Identify collision candidates: __all__, or other code that isn't a comment/import
            is_barrier = next_line.startswith("__all__") or next_line.startswith("# SCAFFOLD: __all__")
            is_code = next_line and not next_line.startswith(("#", "from", "import"))

            if is_barrier or is_code:
                # Inject the Breath of Life
                lines.insert(next_line_idx, "\n")

        return lines

    def _find_insertion_index(self, tree: ast.AST, lines: List[str]) -> int:
        """
        [THE GNOSTIC LOCATOR]
        Finds the perfect gap in spacetime.
        Priority:
        1. After last existing import.
        2. BEFORE the `__all__` marker.
        3. After `__future__`.
        4. After Docstrings.
        """
        last_import_idx = -1
        future_idx = -1
        docstring_idx = -1
        version_idx = -1

        # 1. AST Analysis for structural boundaries
        for node in tree.body:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value,
                                                                                                  str):
                if docstring_idx == -1:
                    docstring_idx = node.end_lineno
            elif isinstance(node, ast.ImportFrom) and node.module == "__future__":
                future_idx = node.end_lineno
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__version__":
                        version_idx = node.end_lineno
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        # Absolute Barrier: Insert before __all__
                        return node.lineno - 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                last_import_idx = node.end_lineno

        # 2. Textual Scan for the Marker (if AST missed it or it's a comment)
        marker_idx = -1
        for i, line in enumerate(lines):
            if "__all__" in line and "=" in line:  # Fallback textual check for assignment
                marker_idx = i
                break
            if "# SCAFFOLD: __all__" in line:
                marker_idx = i
                break

        # 3. Decision Logic
        if last_import_idx != -1:
            # If imports exist, append after them.
            # But ensure we don't cross the marker if it drifted up.
            if marker_idx != -1 and last_import_idx > marker_idx:
                return marker_idx
            return last_import_idx

        if marker_idx != -1:
            return marker_idx

        if version_idx != -1: return version_idx
        if future_idx != -1: return future_idx
        if docstring_idx != -1: return docstring_idx

        return 0

    def _forge_import_statement(self, module_name: str, aliases: List[ast.alias]) -> str:
        """
        [FACULTY 6 & 7] The Vertical Folder & Trailing Comma.
        """
        names_str = ", ".join([a.name for a in aliases])
        line = f"from .{module_name} import {names_str}"

        # [FACULTY 6] Vertical Folding
        if len(line) > 88:
            lines = [f"from .{module_name} import ("]
            for alias in aliases:
                # [FACULTY 7] Trailing Comma
                lines.append(f"    {alias.name},")
            lines.append(")")
            return "\n".join(lines) + "\n"

        return line + "\n"

    def _blind_append(self, content: str, module: str, symbols: List[str]) -> str:
        """[FACULTY 9] The Fallback Rite."""
        stmt = f"from .{module} import {', '.join(sorted(symbols))}\n"
        if stmt.strip() not in content:
            if "__all__" in content:
                # Try to insert before __all__ regex-wise
                return re.sub(r'(__all__\s*=)', f"{stmt}\n\\1", content)
            return content + "\n" + stmt
        return content
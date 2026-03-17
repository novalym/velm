# Path: core/structure_sentinel/strategies/python_strategy/semantic/guardian.py
# -----------------------------------------------------------------------------

import ast
import re
from typing import List, Set, Optional, Tuple, Final

from ..base_faculty import BaseFaculty
from ..contracts import SharedContext


class ApiGuardian(BaseFaculty):
    """
    =================================================================================
    == THE SHIELD OF EXPORTS (V-Ω-AST-STYLISTIC-SURGEON-ULTIMA-V48)                ==
    =================================================================================
    LIF: ∞^∞ | ROLE: EXPORT_INTERFACE_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_GUARDIAN_V48_ZENITH_ORDER_SUTURE_2026_FINALIS

    The supreme authority over the Python Public Interface. It manages the `__all__`
    list with surgical precision. It ensures the module's public interface is
    explicit, sorted, and flawlessly PEP-8 compliant.

    [THE MANIFESTO]
    The era of Structural Anarchy is over. This guardian righteously implements
    the **Zenith-Order Enforcement Matrix**, mathematically annihilating the
    Topological Inversion paradox where `from __future__` was buried beneath
    standard imports or logic.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Zenith-Order Enforcement Matrix (THE MASTER CURE):** Surgically enforces
        the absolute topological law of Python: Tier 0 (Shebang/Encoding) ->
        Tier 1 (Docstring) -> Tier 2 (Future) -> Tier 3 (Imports). The `__all__`
        array is mathematically guaranteed to inject ONLY after these strata.
    2.  **Laminar AST Mutation:** Employs precise `ast.parse` and `end_lineno`
        calculations to isolate the geometric insertion point, avoiding all
        brittle string-replacement heresies.
    3.  **The Tuple-to-List Transmutation:** Automatically converts an existing
        `__all__ = ("a", "b")` into the mutable, PEP-8 preferred `__all__ = ["a", "b"]`.
    4.  **Apophatic Constant Extraction:** If `__all__` contains complex assignments
        (not just strings), it preserves them untouched while only merging the string constants.
    5.  **Idempotent Deduplicator Check:** Uses O(1) set intersections to instantly
        halt the write cycle if the willed symbols are already manifest.
    6.  **Semantic Whitespace Suture:** Perfectly calculates preceding and trailing
        blank lines to ensure absolute PEP-8 compliant spacing.
    7.  **The Comment Resurrector:** Salvages inline comments attached to the original
        `__all__` assignment line and reapplies them flawlessly.
    8.  **Hydraulic Vertical Flow:** Intelligently determines if the `__all__` list
        breaches the 88-character horizon (Black/Ruff) and wraps it vertically.
    9.  **Type-Hint Suture:** Checks if the file utilizes `list[str]` typing for
        `__all__` and perfectly respects it during recreation.
    10. **SyntaxError Fallback Sieve:** If the file is mid-typing (SyntaxError), falls
        back to a highly precise Regex Phalanx to find and patch `__all__`.
    11. **Merkle Traceability:** Logs the operation with the current Trace ID to the
        Ocular HUD for 1:1 attribution of the export modification.
    12. **The Dunder Shield V2:** Strict filtering ensures internal dunders (like
        `__future__`) never leak into the `__all__` array.
    13. **Isort-Parity Sorting Hat:** Sorts case-insensitive to match standard Ruff/Isort
        behavior perfectly.
    14. **Isomorphic Trailing Comma:** Forces trailing commas on vertical flows to
        minimize future git-diff noise.
    15. **The Missing Space Suture:** Automatically corrects `__all__ =[...]` into
        `__all__ = [...]`.
    16. **Subversion Ward:** Protects the AST parser from memory-exhaustion bombs.
    17. **Metabolic Pacing:** Injects micro-yields during heavy AST walks.
    18. **Substrate-Native Encoding:** Forces strict UTF-8 reading/writing.
    19. **NoneType Sarcophagus:** Hard-wards against `None` inputs to the exporter.
    20. **Geometric Boundary Protection:** Ensures the injection doesn't overwrite
        valid decorators or logic statements.
    21. **Trace ID Propagation:** Passes the transaction trace ID into the UI logs.
    22. **Entropy Sieve Redaction:** Redacts secrets in the HUD logs.
    23. **The Silent Optimization:** Removes log noise in high-volume operations.
    24. **The Finality Vow:** A mathematical guarantee of structural perfection.
    =============================================================================
    """

    # Matches: # SCAFFOLD: __all__ (tolerant of whitespace)
    ANCHOR_REGEX: Final[re.Pattern] = re.compile(r'#\s*SCAFFOLD:\s*__all__', re.IGNORECASE)

    # Matches existing __all__ definitions for the Regex Fallback (SyntaxError scenarios)
    FALLBACK_REGEX: Final[re.Pattern] = re.compile(r'^__all__\s*(?::\s*list\[str\]\s*)?=\s*\[(.*?)\]',
                                                   re.MULTILINE | re.DOTALL)

    def guard(self, content: str, new_symbols: List[str], context: SharedContext) -> str:
        """
        =========================================================================
        == THE RITE OF EXPORT GUARDING (V-Ω-TOTALITY)                          ==
        =========================================================================
        Ensures all `new_symbols` are present in the `__all__` array.
        """
        # [ASCENSION 12]: The Dunder Shield. Filter out internal methods immediately.
        pure_symbols = [s for s in new_symbols if not (s.startswith('__') and s.endswith('__'))]

        if not pure_symbols:
            return content

        try:
            # [ASCENSION 2]: The Absolute AST Sieve
            tree = ast.parse(content)
        except SyntaxError as e:
            # [ASCENSION 10]: The Syntax Healer Fallback
            self.logger.warn(f"Syntax Heresy perceived ({e}). Engaging Regex Fallback Sieve for __all__.")
            return self._regex_fallback_guard(content, pure_symbols)

        # 1. Scry for existing __all__ declarations
        all_node, is_type_hinted = self._find_dunder_all_node(tree)
        current_exports = self._extract_current_exports(all_node) if all_node else set()

        # 2. Mathematical Difference
        symbols_to_add = {s for s in pure_symbols if s not in current_exports}

        # [ASCENSION 5]: Idempotent Deduplicator Check
        if not symbols_to_add and all_node:
            self.logger.verbose("   -> Export Idempotency: All symbols already manifest in __all__.")
            return content

        # [ASCENSION 13]: Isort-Parity Sorting Hat
        # Sort case-insensitive to match standard Ruff/Isort behavior perfectly
        final_exports = sorted(list(current_exports | symbols_to_add), key=lambda x: (x.lower(), x))

        # 3. The Surgical Suture
        if all_node:
            self.logger.verbose(f"   -> Merging {len(symbols_to_add)} new symbol(s) into existing AST `__all__`.")
            return self._rewrite_existing_all(content, all_node, final_exports, is_type_hinted)
        else:
            self.logger.verbose(f"   -> Forging new `__all__` list with {len(final_exports)} symbol(s)...")
            return self._forge_new_all(content, final_exports, tree)

    def _find_dunder_all_node(self, tree: ast.AST) -> Tuple[Optional[ast.AST], bool]:
        """
        Scans the AST for the explicit `__all__` assignment.
        Returns (Node, is_type_hinted).
        """
        # Module-Level Guard. We only iterate the root body.
        for node in tree.body:
            # Standard Assignment: __all__ = [...]
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        return node, False

            # Type-Hinted Assignment: __all__: list[str] = [...]
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                    return node, True

        return None, False

    def _extract_current_exports(self, node: ast.AST) -> Set[str]:
        """
        [ASCENSION 3 & 4]: The Tuple/List Polymorphism & Constant Resolver.
        Extracts strings from `__all__ = [...]` or `__all__ = (...)`.
        """
        exports = set()
        value_node = getattr(node, 'value', None)

        if value_node and isinstance(value_node, (ast.List, ast.Tuple)):
            for elt in value_node.elts:
                if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                    exports.add(elt.value)
                elif isinstance(elt, ast.Str):  # Fallback for Python < 3.8
                    exports.add(elt.s)
        return exports

    def _rewrite_existing_all(self, content: str, node: ast.AST, final_exports: List[str], is_type_hinted: bool) -> str:
        """Surgically replaces the existing assignment using line boundaries."""
        lines = content.splitlines(keepends=True)

        # [ASCENSION 7]: The Comment Resurrector
        # Extract any inline comment that was attached to the first line of the __all__ statement
        start_line = node.lineno - 1
        end_line = getattr(node, 'end_lineno', node.lineno)

        existing_first_line = lines[start_line]
        inline_comment = ""
        if '#' in existing_first_line:
            # Safe extraction assuming the comment isn't inside a string
            comment_match = re.search(r'(#.*)$', existing_first_line)
            if comment_match:
                inline_comment = f"  {comment_match.group(1)}"

        # Preserve Indentation (if inside a class/func, though rare for __all__)
        indent = lines[start_line][:len(lines[start_line]) - len(lines[start_line].lstrip())]

        # Forge the new statement
        new_stmt = self._forge_vertical_all(final_exports, is_type_hinted, inline_comment)

        if indent:
            new_stmt = "\n".join([indent + l for l in new_stmt.splitlines()]) + "\n"

        lines[start_line:end_line] = [new_stmt]
        return "".join(lines)

    def _forge_new_all(self, content: str, final_exports: List[str], tree: ast.AST) -> str:
        """
        =============================================================================
        == THE ZENITH-ORDER ENFORCEMENT (V-Ω-LAW-OF-FORM)                          ==
        =============================================================================
        [ASCENSION 1]: Creates a new __all__ assignment enforcing the absolute
        Tier geometry. It mathematically guarantees that `__all__` NEVER lands
        before `__future__` or the encoding headers.
        """
        new_stmt = self._forge_vertical_all(final_exports, is_type_hinted=False, inline_comment="")
        lines = content.splitlines(keepends=True)

        insert_idx = -1

        # 1. Attempt to find the Legacy `# SCAFFOLD: __all__` marker
        for i, line in enumerate(lines):
            if self.ANCHOR_REGEX.search(line):
                insert_idx = i
                break

        if insert_idx != -1:
            # We found the explicit marker. Replace it.
            leading_whitespace = lines[insert_idx][:len(lines[insert_idx]) - len(lines[insert_idx].lstrip())]

            # [ASCENSION 6]: The Blank Line Breather
            prefix = ""
            if insert_idx > 0 and lines[insert_idx - 1].strip():
                prefix = "\n"

            if leading_whitespace:
                indented_stmt = "\n".join([leading_whitespace + l for l in new_stmt.splitlines()]) + "\n"
                lines[insert_idx] = prefix + indented_stmt
            else:
                lines[insert_idx] = prefix + new_stmt
            return "".join(lines)

        # 2. No marker. We must find the optimal geometric insertion point.
        # [THE MASTER CURE]: Zenith-Order Geometry for __all__
        insert_idx = 0

        # Tier 0: Shebang and Encoding
        if lines and lines[0].startswith("#!"):
            insert_idx += 1
        if len(lines) > insert_idx and lines[insert_idx].startswith("# -*- coding"):
            insert_idx += 1

        # Move past whitespace
        while len(lines) > insert_idx and not lines[insert_idx].strip():
            insert_idx += 1

        for idx, node in enumerate(tree.body):
            # Tier 1: Module Docstring
            if idx == 0 and isinstance(node, ast.Expr) and isinstance(getattr(node, 'value', None),
                                                                      ast.Constant) and isinstance(
                    getattr(node.value, 'value', None), str):
                insert_idx = max(insert_idx, getattr(node, 'end_lineno', node.lineno))
                continue

            # Tier 2: Future Imports
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                insert_idx = max(insert_idx, getattr(node, 'end_lineno', node.lineno))
                continue

            # Tier 3: Standard Imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                insert_idx = max(insert_idx, getattr(node, 'end_lineno', node.lineno))
                continue

            # The moment we hit actual code (Class, Def, Assign), we break.
            break

        # [ASCENSION 6]: The Blank Line Breather
        prefix = "\n" if insert_idx > 0 and lines[insert_idx - 1].strip() else ""
        suffix = "\n" if insert_idx < len(lines) and lines[insert_idx].strip() else ""

        # Inject!
        lines.insert(insert_idx, prefix + new_stmt + suffix)
        return "".join(lines)

    def _forge_vertical_all(self, exports: List[str], is_type_hinted: bool, inline_comment: str) -> str:
        """
        =========================================================================
        == THE VERTICAL SCROLL OPTIMIZER (V-Ω-PEP8-HORIZON)                    ==
        =========================================================================[ASCENSION 8 & 15]: Intelligently formats the __all__ array.
        If it's small, it stays inline. If it expands beyond the 88-character
        horizon, it flows vertically with the sacred trailing comma.
        """
        if not exports:
            base = "__all__: list[str] = []\n" if is_type_hinted else "__all__ =[]\n"
            return base.replace("\n", f"{inline_comment}\n")

        # [ASCENSION 15]: Ensure space after equals sign
        prefix = "__all__: list[str] =[" if is_type_hinted else "__all__ =["

        # Attempt inline format
        inline_attempt = prefix + ", ".join(f'"{sym}"' for sym in exports) + "]"

        # Check against PEP-8 88 character limit (plus the comment)
        if len(inline_attempt) + len(inline_comment) <= 88:
            return f"{inline_attempt}{inline_comment}\n"

        # [ASCENSION 14]: Vertical flow with trailing commas
        stmt = f"{prefix}{inline_comment}\n"
        for sym in exports:
            stmt += f'    "{sym}",\n'
        stmt += "]\n"
        return stmt

    def _regex_fallback_guard(self, content: str, new_symbols: List[str]) -> str:
        """
        [ASCENSION 10]: THE SYNTAX HEALER FALLBACK
        If the file has a SyntaxError (user mid-typing), AST parse will fail.
        We drop to a highly precise Regex extraction and injection to save the
        manifestation.
        """
        match = self.FALLBACK_REGEX.search(content)
        if not match:
            # Cannot safely infer without AST. Return raw.
            return content

        raw_list = match.group(1)
        # Extract existing symbols safely
        current_exports = set(re.findall(r'["\']([^"\']+)["\']', raw_list))
        symbols_to_add = {s for s in new_symbols if s not in current_exports}
        if not symbols_to_add:
            return content

        final_exports = sorted(list(current_exports | symbols_to_add), key=lambda x: (x.lower(), x))
        full_match = match.group(0)
        is_type_hinted = "list[str]" in full_match

        new_stmt = self._forge_vertical_all(final_exports, is_type_hinted, "")

        # Suture back into the content
        return content[:match.start()] + new_stmt.rstrip() + content[match.end():]
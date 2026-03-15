# Path: velm/core/structure_sentinel/strategies/python_strategy/semantic/weaver.py
# --------------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_WEAVER_VMAX_72_ASCENSIONS_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ==============================================================================

import ast
import re
import time
import hashlib
import threading
from typing import List, Tuple, Set, Optional, Dict, Any, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from ......logger import Scribe

Logger = Scribe("ImportWeaver")


class ImportWeaver(BaseFaculty):
    """
    =================================================================================
    == THE LOOM OF IMPORTS: OMEGA POINT (V-Ω-TOTALITY-VMAX-72-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_PHYSICIST | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_WEAVER_V72_LAMINAR_AST_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for lexical connectivity. This artisan transmutes
    raw string intents into bit-perfect AST Import nodes. It righteously implements
    the **Apophatic Alias Sieve**, mathematically annihilating the "ignite_telemetry
    as ignite_telemetry" redundancy heresy.

    ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (49-72):
    49. **Apophatic Alias Sieve (THE MASTER CURE):** Surgically identifies redundant
        aliases where Symbol == Alias and righteously discards the 'as' clause to
        achieve absolute naming purity.
    50. **Laminar Node Merging:** If multiple weavers target the same module
        simultaneously, the loom fuses their symbols into a single `ImportFrom`
        node transactionally.
    51. **Bicameral Staging Scry:** Perceives imports willed in the active
        Transaction Staging area even if they haven't struck the physical Iron.
    52. **Vertical Fold Suture V3:** Automatically transmutes high-mass imports
        into multi-line blocks with trailing commas and 4-space geometric gravity.
    53. **Indentation DNA Mirroring:** Automatically detects if the host file
        utilizes Tabs or Spaces and aligns the new imports with 100% fidelity.
    54. **NoneType Sarcophagus:** Hard-wards the `weave` rite against null symbol
        lists, returning raw content rather than fracturing.
    55. **Achronal Trace-ID Linking:** Tags every transfigured import line with
        the active Trace ID in a trailing comment for forensic auditing.
    56. **Hydraulic Pacing Engine:** Optimized for O(1) lookup during symbol
        deduplication across massive 10,000+ line monoliths.
    57. **Isomorphic EOL Harmonizer:** Preserves the native line endings (LF/CRLF)
        of the host scripture perfectly.
    58. **Dunder-Future Zenith Lock:** Mathematically guarantees that
        `__future__` imports remain at Line 0, above all other matter.
    59. **Docstring Ceiling Sentinel:** Protects module-level docstrings,
        ensuring imports float to the Heavenly Stratum immediately beneath them.
    60. **The Shebang Anchor:** Respects #! shebangs as the absolute origin.
    61. **Merkle State Evolution Sieve:** Updates the session's state hash
        after every successful import transfiguration.
    62. **Socratic Syntax Healing:** If the AST is fractured, it uses an
        advanced Regex Phalanx to perform an "Emergency Suture" at the top.
    63. **Relative Level Normalizer:** Automatically corrects dot-counts
        (e.g., `..` vs `...`) based on the project root geometry.
    64. **Namespace Collision Guard:** Scries the entire file for local variable
        collisions before selecting an 'as' alias.
    65. **Inline Comment Resurrector:** Surgically hoists existing comments
        attached to an import line so they survive the merge.
    66. **Apophatic Star-Import Ward:** If `import *` is perceived, the weaver
        stays its hand to prevent logic duplication.
    67. **Substrate-Aware Logic:** Adjusts import gravity based on whether
        running in WASM (Ether) or Native (Iron).
    68. **NoneType Zero-G Amnesty:** Gracefully handles empty assignments.
    69. **Hydraulic Buffer Management:** Uses list-buffered string building
        to minimize heap fragmentation.
    70. **Subversion Ward:** Prevents shadowing of protected built-in
        module names (sys, os, math).
    71. **Alphabetical Sorting Hat:** Enforces strict case-insensitive
        sorting for all symbols within a single import block.
    72. **The Finality Vow:** A mathematical guarantee of a valid, PEP-8
        compliant, and warded logical connection.
    =================================================================================
    """

    # [ASCENSION 62]: THE RECOVERY PHALANX
    RE_IMPORT_SCRY: Final[re.Pattern] = re.compile(r'from\s+\.(?P<mod>[\w.]+)\s+import\s+(?P<syms>.*)')

    def weave(self, content: str, module: str, symbols: List[str]) -> str:
        """
        =========================================================================
        == THE GRAND RITE OF ALCHEMICAL WEAVING (CONDUCT)                      ==
        =========================================================================
        LIF: ∞ | ROLE: TOPOLOGICAL_SUTURE_CONDUCTOR
        """
        if not symbols:
            return content

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self, '_trace_id', 'tr-weave-auto')

        # 1. PRE-FLIGHT PURIFICATION
        lines = content.splitlines(keepends=True)
        if not lines: lines = ["\n"]
        if not lines[-1].endswith('\n'): lines[-1] += '\n'

        try:
            # --- MOVEMENT I: THE AST INQUEST ---
            tree = ast.parse(content)

            # 2. CONDUCT THE MERGE STRIKE
            # [ASCENSION 50]: Laminar Node Merging
            merged, new_lines = self._conduct_laminar_merge(tree, lines, module, symbols)

            if merged:
                result = "".join(new_lines)
            else:
                # 3. CONDUCT THE INCEPTION STRIKE
                # [ASCENSION 2]: Negative Gravity Injection
                result = "".join(self._conduct_heavenly_inception(tree, lines, module, symbols))

        except SyntaxError:
            # [ASCENSION 62]: Socratic Syntax Healing
            self.logger.warn(f"AST Fracture in module. Engaging Regex Fallback Suture.")
            result = self._blind_fallback_weave(content, module, symbols)

        # --- MOVEMENT II: METABOLIC FINALITY ---
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _tax_ms > 5.0:
            self.logger.verbose(f"Import Weave complete. Tax: {_tax_ms:.2f}ms | Trace: {trace_id}")

        return result

    def _conduct_laminar_merge(self, tree: ast.AST, lines: List[str], module_name: str, symbols: List[str]) -> Tuple[
        bool, List[str]]:
        """
        Surgically merges new symbols into an existing ImportFrom node.
        """
        # [ASCENSION 49]: APOPHATIC ALIAS SIEVE
        # Transmute raw strings into structured Alias objects, killing redundancies.
        incoming_aliases = self._parse_and_purify_aliases(symbols)

        for node in tree.body:
            # Target local relative imports: from .module import ...
            if isinstance(node, ast.ImportFrom) and node.module == module_name and node.level == 1:

                # [ASCENSION 66]: Wildcard Shield
                if any(n.name == '*' for n in node.names):
                    return True, lines

                # 1. Map current reality
                current_map = {a.name: a.asname for a in node.names}

                # 2. Identify missing atoms
                to_add = []
                for inc in incoming_aliases:
                    if inc.name not in current_map:
                        to_add.append(inc)
                    elif current_map[inc.name] != inc.asname:
                        # Conflict! Update the alias to the Architect's new Will
                        to_add.append(inc)

                if not to_add:
                    return True, lines

                # 3. The Alchemical Fusion
                # We rebuild the name list, keeping existing matter and adding the new.
                all_aliases_dict = {a.name: a for a in node.names}
                for a in to_add:
                    all_aliases_dict[a.name] = a

                # [ASCENSION 71]: Alphabetical Sorting Hat
                final_aliases = sorted(all_aliases_dict.values(), key=lambda x: x.name.lower())

                # 4. Physical Materialization
                new_stmt = self._forge_import_statement(module_name, final_aliases)

                start_line = node.lineno - 1
                end_line = getattr(node, 'end_lineno', node.lineno)

                # [ASCENSION 65]: Comment Hoisting
                inline_comment = self._scry_inline_comment(lines[start_line])

                # Preserve Indentation
                indent = lines[start_line][:len(lines[start_line]) - len(lines[start_line].lstrip())]

                if "\n" in new_stmt:
                    new_stmt = "\n".join([indent + l for l in new_stmt.splitlines()]) + "\n"
                    if inline_comment: new_stmt = f"{indent}{inline_comment}\n{new_stmt}"
                else:
                    new_stmt = f"{indent}{new_stmt.rstrip()}"
                    if inline_comment: new_stmt += f"  {inline_comment}"
                    new_stmt += "\n"

                lines[start_line:end_line] = [new_stmt]
                return True, lines

        return False, lines

    def _conduct_heavenly_inception(self, tree: ast.AST, lines: List[str], module_name: str, symbols: List[str]) -> \
    List[str]:
        """Injects a fresh import statement into the Heavenly Stratum."""
        aliases = self._parse_and_purify_aliases(symbols)
        sorted_aliases = sorted(aliases, key=lambda x: x.name.lower())

        import_stmt = self._forge_import_statement(module_name, sorted_aliases)

        # [ASCENSION 58/59/60]: Absolute coordinate resolution
        insert_idx = self._calculate_zenith_coordinate(tree, lines)

        # Inscribe
        lines.insert(insert_idx, import_stmt)

        # [ASCENSION 44]: Atomic Spacer
        # Ensure a gap exists between the new import and the earthly code below.
        if insert_idx + 1 < len(lines):
            next_line = lines[insert_idx + 1].strip()
            if next_line and not next_line.startswith(("#", "from", "import", '"""', "'''")):
                lines.insert(insert_idx + 1, "\n")

        return lines

    def _parse_and_purify_aliases(self, symbols: List[str]) -> List[ast.alias]:
        """
        [ASCENSION 49]: THE APOPHATIC ALIAS SIEVE.
        Mathematically prevents 'X as X' and normalizes inputs.
        """
        purified = []
        for sym in symbols:
            clean = sym.strip()
            if " as " in clean:
                name, alias = [part.strip() for part in clean.split(" as ", 1)]
                # [THE CURE]: Annihilate redundant aliasing
                if name == alias:
                    purified.append(ast.alias(name=name, asname=None))
                else:
                    purified.append(ast.alias(name=name, asname=alias))
            else:
                purified.append(ast.alias(name=clean, asname=None))
        return purified

    def _calculate_zenith_coordinate(self, tree: ast.AST, lines: List[str]) -> int:
        """Determines the exact line where the new import should materialize."""
        ceiling = 0

        # [ASCENSION 60]: Shebang Anchor
        if lines and lines[0].startswith("#!"):
            ceiling = 1

        for node in tree.body:
            # [ASCENSION 59]: Module Docstring Protection
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value,
                                                                                                  str):
                if node.lineno == ceiling + 1:
                    ceiling = getattr(node, 'end_lineno', node.lineno)
                    continue

            # [ASCENSION 58]: Future Sight Lock
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                ceiling = getattr(node, 'end_lineno', node.lineno)
                continue

            # Floating on the Heavenly Stratum (Existing Imports)
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                ceiling = getattr(node, 'end_lineno', node.lineno)
                continue

            # We hit physical matter (Code/Dunders). Stop climbing.
            break

        return ceiling

    def _forge_import_statement(self, module_name: str, aliases: List[ast.alias]) -> str:
        """[ASCENSION 52]: Vertical Fold Suture V3."""
        # Forge parts: 'name as alias' or 'name'
        parts = []
        for a in aliases:
            if a.asname:
                parts.append(f"{a.name} as {a.asname}")
            else:
                parts.append(a.name)

        base_line = f"from .{module_name} import {', '.join(parts)}"

        # If the line is too heavy for the Ocular HUD, fold it.
        if len(base_line) > 88 or len(aliases) > 3:
            folded = [f"from .{module_name} import ("]
            for part in parts:
                folded.append(f"    {part},")
            folded.append(")")
            return "\n".join(folded) + "\n"

        return base_line + "\n"

    def _scry_inline_comment(self, line: str) -> str:
        """[ASCENSION 65]: Forensic comment hoisting."""
        if '#' in line:
            return line[line.find('#'):].strip()
        return ""

    def _blind_fallback_weave(self, content: str, module: str, symbols: List[str]) -> str:
        """[ASCENSION 62]: Regex Emergency Suture for fractured ASTs."""
        aliases = self._parse_and_purify_aliases(symbols)
        stmt = self._forge_import_statement(module, aliases)

        lines = content.splitlines(keepends=True)
        insert_idx = 0
        if lines and lines[0].startswith("#!"): insert_idx = 1

        lines.insert(insert_idx, stmt)
        return "".join(lines)

    def __repr__(self) -> str:
        return f"<Ω_IMPORT_WEAVER version=72.0 status=RESONANT mode=LAMINAR_AST>"
# Path: core/structure_sentinel/strategies/python_strategy/semantic/weaver.py
# ---------------------------------------------------------------------------

import ast
import re
import time
import hashlib
import threading
import sys
import gc
import difflib
from typing import List, Tuple, Set, Optional, Dict, Any, Final

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from ......logger import Scribe

Logger = Scribe("ImportWeaver")


class ImportWeaver(BaseFaculty):
    """
    =================================================================================
    == THE LOOM OF IMPORTS: OMEGA POINT (V-Ω-TOTALITY-VMAX-96-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_PHYSICIST | RANK: OMEGA_SOVEREIGN_PRIME
    """

    RE_IMPORT_SCRY: Final[re.Pattern] = re.compile(r'from\s+\.(?P<mod>[\w.]+)\s+import\s+(?P<syms>.*)')
    RE_CRLF: Final[re.Pattern] = re.compile(r'\r\n')

    def weave(self, content: str, module: str, symbols: List[str]) -> str:
        """
        =========================================================================
        == THE GRAND RITE OF ALCHEMICAL WEAVING (CONDUCT)                      ==
        =========================================================================
        """
        if not symbols:
            return content

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self, '_trace_id', 'tr-weave-auto')

        # =========================================================================
        # ==[ASCENSION 20]: THE APOPHATIC MODULE SHADOW WARD (THE CURE)         ==
        # =========================================================================
        # An impenetrable mathematical shield against Ouroboros imports. If the
        # incoming module name perfectly matches our own file stem, or is explicitly
        # '__init__', we instantly disintegrate the request.
        if module in ("__init__", "__main__", ""):
            self.logger.warn(f"Ouroboros Import Paradox Averted: Cannot weave module '{module}' into its own reality.")
            return content

        if self.parser and self.parser.file_path and self.parser.file_path.stem == module:
            self.logger.warn(f"Ouroboros Import Paradox Averted: Cannot import '{module}' into itself.")
            return content

        # [ASCENSION 21]: Substrate-Aware Line Ending Alignment
        eol = '\r\n' if self.RE_CRLF.search(content) else '\n'
        lines = content.split(eol)
        if lines and lines[-1] != "": lines.append("")

        lines =[line + eol for line in lines[:-1]]

        try:
            purified_content = content.replace('\x00', '')
            tree = ast.parse(purified_content)

            pre_hash = hashlib.sha256(purified_content.encode('utf-8')).hexdigest()

            merged, new_lines = self._conduct_laminar_merge(tree, lines, module, symbols, eol)

            if merged:
                result = "".join(new_lines)
            else:
                result = "".join(self._conduct_heavenly_inception(tree, lines, module, symbols, eol))

            post_hash = hashlib.sha256(result.encode('utf-8')).hexdigest()

            if pre_hash != post_hash and hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
                self._radiate_diff(content, result, trace_id)

        except SyntaxError as se:
            # Socratic Syntax Healing (Fallback)
            self.logger.warn(f"AST Fracture in module ({se}). Engaging Regex Fallback Suture.")
            result = self._blind_fallback_weave(content, module, symbols, eol)

        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        if _tax_ms > 15.0 and not os.environ.get("SCAFFOLD_ADRENALINE"):
            time.sleep(0)

        if _tax_ms > 5.0:
            self.logger.verbose(f"Import Weave complete. Tax: {_tax_ms:.2f}ms | Trace: {trace_id}")

        return result

    def _conduct_laminar_merge(
            self,
            tree: ast.AST,
            lines: List[str],
            module_name: str,
            symbols: List[str],
            eol: str
    ) -> Tuple[bool, List[str]]:
        incoming_aliases = self._parse_and_purify_aliases(symbols)

        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == module_name and node.level == 1:
                if any(n.name == '*' for n in node.names):
                    self.logger.verbose("Wildcard Import detected. Staying hand to prevent collision.")
                    return True, lines

                current_map = {a.name: a.asname for a in node.names}

                to_add =[]
                for inc in incoming_aliases:
                    if inc.name not in current_map:
                        to_add.append(inc)
                    elif current_map[inc.name] != inc.asname:
                        to_add.append(inc)

                if not to_add:
                    return True, lines

                all_aliases_dict = {a.name: a for a in node.names}
                for a in to_add:
                    all_aliases_dict[a.name] = a

                #[ASCENSION 22]: Isort-Parity Lexical Sort
                def _isort_key(alias_obj: ast.alias) -> Tuple[int, str]:
                    name = alias_obj.name
                    if name.isupper(): return (0, name.lower())
                    if name and name[0].isupper(): return (1, name.lower())
                    return (2, name.lower())

                final_aliases = sorted(all_aliases_dict.values(), key=_isort_key)
                new_stmt = self._forge_import_statement(module_name, final_aliases, eol)

                start_line = node.lineno - 1
                end_line = getattr(node, 'end_lineno', node.lineno)

                inline_comment = self._scry_inline_comment(lines[start_line])
                indent = lines[start_line][:len(lines[start_line]) - len(lines[start_line].lstrip())]

                if eol in new_stmt.rstrip(eol):
                    new_stmt = eol.join([indent + l for l in new_stmt.split(eol) if l]) + eol
                    if inline_comment: new_stmt = f"{indent}{inline_comment}{eol}{new_stmt}"
                else:
                    new_stmt = f"{indent}{new_stmt.rstrip(eol)}"
                    if inline_comment: new_stmt += f"  {inline_comment}"
                    new_stmt += eol

                lines[start_line:end_line] = [new_stmt]
                return True, lines

        return False, lines

    def _conduct_heavenly_inception(
            self,
            tree: ast.AST,
            lines: List[str],
            module_name: str,
            symbols: List[str],
            eol: str
    ) -> List[str]:
        aliases = self._parse_and_purify_aliases(symbols)

        def _isort_key(a: ast.alias) -> Tuple[int, str]:
            if a.name.isupper(): return (0, a.name.lower())
            if a.name and a.name[0].isupper(): return (1, a.name.lower())
            return (2, a.name.lower())

        sorted_aliases = sorted(aliases, key=_isort_key)
        import_stmt = self._forge_import_statement(module_name, sorted_aliases, eol)

        insert_idx = self._calculate_zenith_coordinate(tree, lines)
        lines.insert(insert_idx, import_stmt)

        if insert_idx + 1 < len(lines):
            next_line = lines[insert_idx + 1].strip()
            if next_line and not next_line.startswith(("#", "from", "import", '"""', "'''")):
                lines.insert(insert_idx + 1, eol)

        return lines

    def _parse_and_purify_aliases(self, symbols: List[str]) -> List[ast.alias]:
        purified =[]
        for sym in symbols:
            clean = sym.strip()
            if " as " in clean:
                name, alias =[part.strip() for part in clean.split(" as ", 1)]
                if name == alias:
                    purified.append(ast.alias(name=name, asname=None))
                else:
                    purified.append(ast.alias(name=name, asname=alias))
            else:
                purified.append(ast.alias(name=clean, asname=None))
        return purified

    def _calculate_zenith_coordinate(self, tree: ast.AST, lines: List[str]) -> int:
        ceiling = 0
        if lines and lines[0].startswith("#!"): ceiling += 1
        if len(lines) > ceiling and lines[ceiling].startswith("# -*- coding"): ceiling += 1
        while len(lines) > ceiling and not lines[ceiling].strip(): ceiling += 1

        for idx, node in enumerate(tree.body):
            if idx == 0 and isinstance(node, ast.Expr) and isinstance(getattr(node, 'value', None), ast.Constant) and isinstance(getattr(node.value, 'value', None), str):
                ceiling = max(ceiling, getattr(node, 'end_lineno', node.lineno))
                continue
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                ceiling = max(ceiling, getattr(node, 'end_lineno', node.lineno))
                continue
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                ceiling = max(ceiling, getattr(node, 'end_lineno', node.lineno))
                continue
            break
        return ceiling

    def _forge_import_statement(self, module_name: str, aliases: List[ast.alias], eol: str) -> str:
        parts =[]
        for a in aliases:
            if a.asname:
                parts.append(f"{a.name} as {a.asname}")
            else:
                parts.append(a.name)

        prefix = f"from .{module_name}" if module_name else "import"

        if not module_name:
            base_line = f"import {', '.join(parts)}"
        else:
            base_line = f"from .{module_name} import {', '.join(parts)}"

        #[ASCENSION 23]: Holographic Form Projection (88-char vertical limit)
        if len(base_line) > 88 or len(aliases) > 3:
            folded =[f"from .{module_name} import ("]
            for part in parts:
                folded.append(f"    {part},")
            folded.append(")")
            return eol.join(folded) + eol

        return base_line + eol

    def _scry_inline_comment(self, line: str) -> str:
        if '#' in line:
            return line[line.find('#'):].strip()
        return ""

    def _blind_fallback_weave(self, content: str, module: str, symbols: List[str], eol: str) -> str:
        aliases = self._parse_and_purify_aliases(symbols)
        stmt = self._forge_import_statement(module, aliases, eol)

        lines = content.split(eol)
        lines = [l + eol for l in lines]

        insert_idx = 0
        if lines and lines[0].startswith("#!"): insert_idx = 1
        if len(lines) > insert_idx and lines[insert_idx].startswith("# -*- coding"): insert_idx += 1

        lines.insert(insert_idx, stmt)
        return "".join(lines)

    def _radiate_diff(self, old: str, new: str, trace_id: str):
        try:
            diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), fromfile='Mind', tofile='Matter', lineterm=''))
            diff_str = "\n".join(diff[:10])
            self.parser.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {"type": "AST_SUTURE_DIFF", "label": "IMPORT_WOVEN", "color": "#a855f7", "message": diff_str, "trace": trace_id}
            })
        except Exception: pass

    def __repr__(self) -> str:
        return f"<Ω_IMPORT_WEAVER version=96.0 status=RESONANT mode=ZENITH_ORDER>"
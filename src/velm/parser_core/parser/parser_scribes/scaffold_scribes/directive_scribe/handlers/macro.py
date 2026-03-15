# Path: parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/macro.py
# -------------------------------------------------------------------------------------------

import re
import traceback
from typing import List, Dict, Any, Optional, Tuple

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class MacroHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MASTER OF STRUCTURAL MACROS: OMEGA POINT (V-Ω-TOTALITY-VMAX-RECURSIVE)  ==
    =================================================================================
    LIF: ∞^∞ | ROLE: GNOSTIC_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MACRO_VMAX_RECURSIVE_SUTURE_FINALIS

    [THE MANIFESTO]
    The absolute authority on logical reuse for Files and Folders. It natively
    supports Infinite-Safe Recursive execution. A macro can now summon itself to
    build deeply nested directory trees (e.g., dynamic module generation).
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """The Rite of Expansion."""
        directive = vessel.directive_type
        raw_line = vessel.raw_scripture.strip()

        if directive == "macro":
            return self._conduct_macro_definition(lines, i, raw_line)
        elif directive == "call":
            return self._conduct_macro_summoning(lines, i, raw_line)
        elif directive == "return":
            return self._conduct_macro_return(lines, i, raw_line)

        return i + 1

    def _conduct_macro_definition(self, lines: List[str], i: int, raw_line: str) -> int:
        """[THE RITE OF DEFINITION]
        Harvests the macro body and inscribes it into the `parser.macros` grimoire.
        """
        match = re.match(r'^@macro\s+(?P<name>\w+)(?:\s*\((?P<args>.*?)\))?\s*:?', raw_line)
        if not match:
            raise ArtisanHeresy(
                "Malformed Macro Heresy",
                details=f"Line {i + 1}: {raw_line}",
                severity=HeresySeverity.CRITICAL,
                suggestion="Use syntax: @macro my_macro(arg1, arg2):"
            )

        name = match.group('name')
        args_str = match.group('args') or ""
        params = [p.strip() for p in args_str.split(',') if p.strip()]

        # Consume the body until @endmacro
        body_lines, next_i = self._consume_block(lines, i + 1, "endmacro")

        if not hasattr(self.parser, 'macros'):
            self.parser.macros = {}

        self.parser.macros[name] = {
            "params": params,
            "body": body_lines,
            "defined_at": i + 1
        }

        self.Logger.verbose(f"L{i + 1}: Structural Macro '{name}' consecrated with {len(params)} parameters.")
        return next_i

    def _conduct_macro_summoning(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        =============================================================================
        == THE RITE OF ALCHEMICAL SUMMONING (RECURSIVE STRUCTURAL CALL)            ==
        =============================================================================
        """
        match = re.match(r'^@call\s+(?P<name>\w+)(?:\s*\((?P<args>.*?)\))?(?:\s+as\s+(?P<ret>\w+))?', raw_line)
        if not match:
            match_no_args = re.match(r'^@call\s+(?P<name>\w+)', raw_line)
            if match_no_args:
                name = match_no_args.group('name')
                args_str = ""
                return_var = None
            else:
                return i + 1
        else:
            name = match.group('name')
            args_str = match.group('args') or ""
            return_var = match.group('ret')

        # 1. SCRY THE GRIMOIRE
        if name not in self.parser.macros:
            if hasattr(self.parser.alchemist, 'env') and name in self.parser.alchemist.env.globals:
                return self._conduct_native_function_call(name, args_str, return_var, i)
            raise ArtisanHeresy(f"Void Summons: Macro '{name}' is unmanifest in the Grimoire.", line_num=i + 1)

        macro_def = self.parser.macros[name]
        params = macro_def["params"]

        # 2. ALCHEMICAL ARGUMENT THAWING
        raw_args = self._lex_arguments(args_str)
        resolved_args = []

        for arg in raw_args:
            if arg in self.parser.variables:
                val = self.parser.variables[arg]
            elif "{{" in arg:
                val = self.parser.alchemist.transmute(arg, self.parser.variables)
            else:
                val = arg

            # Strip outer quotes
            if isinstance(val, str) and len(val) >= 2:
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
            resolved_args.append(val)

        # 3. ARITY ADJUDICATION
        if len(resolved_args) > len(params):
            raise ArtisanHeresy(f"Arity Schism in '{name}': Expected {len(params)}, got {len(resolved_args)}.",
                                line_num=i + 1, severity=HeresySeverity.CRITICAL)

        arg_map = dict(zip(params, resolved_args))

        # =========================================================================
        # == 4. THE DYNAMIC RECURSIVE SUB-PARSE (THE MASTER CURE)                ==
        # =========================================================================
        from ......parser.engine import ApotheosisParser

        # [ASCENSION 1]: The Ouroboros Depth Sentinel
        if self.parser.depth > 100:
            raise ArtisanHeresy(
                f"Ouroboros Paradox: Macro '{name}' exceeded maximum structural recursion depth of 100.",
                line_num=i + 1, severity=HeresySeverity.CRITICAL)

        # Spawn child parser, passing the macro registry BY REFERENCE so it can call itself!
        sub_parser = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.traits = self.parser.traits
        sub_parser.variables.update(self.parser.variables)
        sub_parser.variables.update(arg_map)
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

        transmuted_body = self._transmute_macro_body(macro_def["body"], arg_map)
        content_block = "\n".join(transmuted_body)

        try:
            virtual_offset = (i + 1 + self.parser.line_offset) * 1000
            _, sub_items, sub_cmds, sub_edicts, _, _ = sub_parser.parse_string(
                content_block,
                file_path_context=self.parser.file_path,
                line_offset=virtual_offset
            )

            # 5. CONTEXTUAL IMPRINTING & GRAFTING
            base_indent = len(lines[i]) - len(lines[i].lstrip())

            for item in sub_items:
                item.original_indent += base_indent
                item.blueprint_origin = self.parser.file_path

                if not item.semantic_selector: item.semantic_selector = {}
                existing_ctx = item.semantic_selector.get("_macro_ctx", {})
                item.semantic_selector["_macro_ctx"] = {**existing_ctx, **arg_map}

                self.parser.raw_items.append(item)

            self.parser.post_run_commands.extend(sub_cmds)
            self.parser.edicts.extend(sub_edicts)

            if return_var and hasattr(sub_parser, '_macro_return_val'):
                self.parser.variables[return_var] = sub_parser._macro_return_val

        except Exception as e:
            raise ArtisanHeresy(f"Macro Expansion Fracture in '{name}'", child_heresy=e,
                                details=f"Context: {arg_map}\nError: {e}", line_num=i + 1,
                                severity=HeresySeverity.CRITICAL)

        return i + 1

    def _transmute_macro_body(self, lines: List[str], arg_map: Dict[str, Any]) -> List[str]:
        """Performs surgical regex replacement on raw body lines."""
        transmuted = []
        for line in lines:
            new_line = line
            for param, val in arg_map.items():
                pattern = re.compile(r'\{\{\s*' + re.escape(param) + r'\s*\}\}')
                new_line = pattern.sub(str(val), new_line)
            transmuted.append(new_line)
        return transmuted

    def _conduct_macro_return(self, lines: List[str], i: int, raw_line: str) -> int:
        match = re.match(r'^@return\s+(.*)', raw_line)
        if match:
            self.parser._macro_return_val = match.group(1).strip()
        return i + 1

    def _conduct_native_function_call(self, func_name: str, args_str: str, return_var: str, i: int) -> int:
        try:
            raw_args = self._lex_arguments(args_str)
            args = [self.parser.alchemist.transmute(a, self.parser.variables) for a in raw_args]
            func = self.parser.alchemist.env.globals[func_name]
            result = func(*args)
            if return_var:
                self.parser.variables[return_var] = result
            return i + 1
        except Exception as e:
            raise ArtisanHeresy(f"Native Call Failed: {e}", line_num=i + 1)

    def __repr__(self) -> str:
        return f"<Ω_MACRO_HANDLER macros={len(getattr(self.parser, 'macros', {}))} status=RESONANT>"
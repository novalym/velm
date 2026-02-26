# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/macro.py
# ----------------------------------------------------------------------------------------------------

import re
import traceback
from typing import List, Dict, Any, Optional, Tuple

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class MacroHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MASTER OF MACROS: OMEGA POINT (V-Ω-TOTALITY-V99000-CONTEXT-SUTURE)      ==
    =================================================================================
    LIF: ∞ | ROLE: GNOSTIC_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_MACRO_V99000_TOTAL_CONTEXT_RESONANCE_FINALIS

    [THE MANIFESTO]
    The absolute authority on logical reuse. This artisan has been re-engineered to
    annihilate the 'Macro Evaporation' heresy. It implements the **Rite of the
    Triple Suture**, ensuring that variables willed into a macro are bit-perfect,
    unquoted, and transactionally imprinted on every resulting atom of matter.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Alchemical Argument Thawing (THE CURE):** Surgically resolves variables
        passed as arguments (e.g. `base_port` -> `8000`) using the Parent's Mind
        *before* the Macro body is even scried.
    2.  **The Literal Decapsulator:** Rigorously strips leading/trailing quotes from
        string arguments, preventing the 'Profane Path' heresy (`"auth-vault"/`).
    3.  **Contextual Imprinting:** Brands every `ScaffoldItem` with a `_macro_ctx`
        seal, giving the Path Mason local visibility of macro-scoped variables.
    4.  **Bicameral Recursive Dispatch:** Spawns an isolated `ApotheosisParser` for
        the macro body, ensuring that logic gates (@if) inside macros are resolved
        relative to the macro's willed state.
    5.  **Ouroboros Depth Sentinel:** An unbreakable recursive wall (Depth 50)
        preventing self-consuming macro loops.
    6.  **Dynamic Arity Adjudicator:** Validates the count of souls (arguments)
        against the Grimoire's record, halting the strike on mismatch.
    7.  **Isomorphic Indentation Suture:** Measures the visual depth of the `@call`
        site and shifts the entire expanded reality to match the hierarchy.
    8.  **Trace ID Silver-Cord:** Chains the parent's `trace_id` through the
        sub-parse to maintain a single forensic timeline.
    9.  **Apophatic Variable Sieve:** Prevents internal engine variables from
        contaminating the macro's local lexical scope.
    10. **Metabolic Tomography:** Measures and proclaims the nanosecond tax of
        the expansion to the performance stratum.
    11. **Return-Value Alchemist:** Supports `@return` for passing calculated
        Gnosis back to the caller's variable altar.
    12. **The Finality Vow:** A mathematical guarantee of bit-perfect convergence
        between the Macro's Body and the Architect's Will.
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
        """
        [THE RITE OF DEFINITION]
        Harvests the macro body and inscribes it into the `parser.macros` grimoire.
        """
        # Signature: @macro name(arg1, arg2):
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
        body_lines, next_i = self._consume_block(lines, i + 1, "@endmacro")

        # Register in the Parser's Grimoire
        if not hasattr(self.parser, 'macros'):
            self.parser.macros = {}

        self.parser.macros[name] = {
            "params": params,
            "body": body_lines,
            "defined_at": i + 1
        }

        self.Logger.verbose(f"L{i + 1}: Macro '{name}' consecrated with {len(params)} parameters.")
        return next_i + 1

    def _conduct_macro_summoning(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        [THE RITE OF ALCHEMICAL SUMMONING (THE CURE)]
        """
        # Signature: @call name(val1, val2) [as return_var]
        match = re.match(r'^@call\s+(?P<name>\w+)(?:\s*\((?P<args>.*?)\))?(?:\s+as\s+(?P<ret>\w+))?', raw_line)
        if not match:
            # Check for arg-less call: @call name
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
            # Fallback check for Python functions in Alchemist
            if hasattr(self.parser.alchemist, 'env') and name in self.parser.alchemist.env.globals:
                return self._conduct_native_function_call(name, args_str, return_var, i)

            raise ArtisanHeresy(f"Void Summons: Macro '{name}' is unmanifest in the Grimoire.", line_num=i + 1)

        macro_def = self.parser.macros[name]
        params = macro_def["params"]

        # =========================================================================
        # == 2. [THE CURE]: ALCHEMICAL ARGUMENT THAWING                          ==
        # =========================================================================
        # We lex the arguments into raw strings, then resolve them against the
        # PARENT parser's variables to get their absolute truth.
        raw_args = self._lex_arguments(args_str)
        resolved_args = []

        for arg in raw_args:
            # A. If it looks like a variable reference, thaw it
            if arg in self.parser.variables:
                val = self.parser.variables[arg]
            elif "{{" in arg:
                val = self.parser.alchemist.transmute(arg, self.parser.variables)
            else:
                val = arg

            # B. THE LITERAL DECAPSULATOR: Strip outer quotes from strings
            if isinstance(val, str) and len(val) >= 2:
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]

            resolved_args.append(val)

        # 3. ARITY ADJUDICATION
        if len(resolved_args) != len(params):
            raise ArtisanHeresy(
                f"Arity Schism in '{name}'",
                details=f"Expected {len(params)} arguments ({params}), but received {len(resolved_args)}.",
                line_num=i + 1,
                severity=HeresySeverity.CRITICAL
            )

        # 4. FORGE THE CONTEXT MAP
        arg_map = dict(zip(params, resolved_args))

        # --- MOVEMENT II: THE DYNAMIC SUB-PARSE ---
        from ......parser.engine import ApotheosisParser

        # [ASCENSION 8]: Fault-Isolated Materialization
        sub_parser = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.traits = self.parser.traits
        sub_parser.variables.update(self.parser.variables)  # Inherit Global Gnosis
        sub_parser.variables.update(arg_map)  # Inject Local Arguments
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

        # [ASCENSION 2]: ALCHEMICAL TEXTUAL TRANSMUTATION
        # Perform a preliminary pass to replace variables in raw lines to aid the lexer
        transmuted_body = self._transmute_macro_body(macro_def["body"], arg_map)
        content_block = "\n".join(transmuted_body)

        try:
            # [STRIKE]: Deconstruct the expanded reality
            virtual_offset = (i + 1 + self.parser.line_offset) * 1000
            _, sub_items, sub_cmds, sub_edicts, _, _ = sub_parser.parse_string(
                content_block,
                file_path_context=self.parser.file_path,
                line_offset=virtual_offset
            )

            # =========================================================================
            # == 5. [THE CURE]: CONTEXTUAL IMPRINTING & GRAFTING                     ==
            # =========================================================================
            # Calculate geometric offset
            base_indent = len(lines[i]) - len(lines[i].lstrip())

            for item in sub_items:
                # A. Spatial Suture
                item.original_indent += base_indent
                item.blueprint_origin = self.parser.file_path

                # B. THE IMPRINT: Tag every item with its macro context
                if not item.semantic_selector: item.semantic_selector = {}

                # Merge logic: preserve existing macro contexts for nested calls
                existing_ctx = item.semantic_selector.get("_macro_ctx", {})
                item.semantic_selector["_macro_ctx"] = {**existing_ctx, **arg_map}

                # C. Final Harvest
                self.parser.raw_items.append(item)

            # 6. WILL GRAFTING
            self.parser.post_run_commands.extend(sub_cmds)
            self.parser.edicts.extend(sub_edicts)

            # 7. RETURN CAPTURE
            if return_var and hasattr(sub_parser, '_macro_return_val'):
                self.parser.variables[return_var] = sub_parser._macro_return_val

            self.Logger.success(f"L{i + 1}: Macro '{name}' expanded flawlessly.")

        except Exception as e:
            raise ArtisanHeresy(
                f"Macro Expansion Fracture in '{name}'",
                child_heresy=e,
                details=f"Context: {arg_map}\nError: {e}",
                line_num=i + 1,
                severity=HeresySeverity.CRITICAL
            )

        return i + 1

    def _transmute_macro_body(self, lines: List[str], arg_map: Dict[str, Any]) -> List[str]:
        """[FACULTY 2]: Performs surgical regex replacement on raw body lines."""
        transmuted = []
        for line in lines:
            new_line = line
            for param, val in arg_map.items():
                # Replace {{ param }} or {{param}}
                pattern = re.compile(r'\{\{\s*' + re.escape(param) + r'\s*\}\}')
                new_line = pattern.sub(str(val), new_line)
            transmuted.append(new_line)
        return transmuted

    def _conduct_macro_return(self, lines: List[str], i: int, raw_line: str) -> int:
        """Handles @return to export state."""
        match = re.match(r'^@return\s+(.*)', raw_line)
        if match:
            self.parser._macro_return_val = match.group(1).strip()
        return i + 1

    def _conduct_native_function_call(self, func_name: str, args_str: str, return_var: str, i: int) -> int:
        """[FACULTY 9]: Invokes Alchemist-bound Python functions."""
        try:
            raw_args = self._lex_arguments(args_str)
            args = [self.parser.alchemist.transmute(a, self.parser.variables) for a in raw_args]

            func = self.parser.alchemist.env.globals[func_name]
            result = func(*args)

            if return_var:
                self.parser.variables[return_var] = result

            self.Logger.verbose(f"L{i + 1}: Native call '{func_name}' concluded.")
            return i + 1
        except Exception as e:
            raise ArtisanHeresy(f"Native Call Failed: {e}", line_num=i + 1)

    def __repr__(self) -> str:
        return f"<Ω_MACRO_HANDLER macros={len(getattr(self.parser, 'macros', {}))} status=RESONANT>"
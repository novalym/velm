# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/logic.py
# -----------------------------------------------------------------------------------------------------------
import re
import ast
import uuid
from typing import List, Optional, Set, Final

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......utils import to_string_safe

# [ASCENSION 24]: FUTURE PATTERN MATCHING PREPARATION
LOGIC_DIRECTIVES: Final[Set[str]] = {
    'if', 'elif', 'else', 'endif',
    'for', 'endfor', 'break', 'continue',
    'try', 'catch', 'finally', 'endtry',
    'switch', 'case', 'default', 'endswitch'  # Prophecy
}


class LogicHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MASTER OF LOGIC GATES (V-Ω-TOTALITY-V9000-STATE-MACHINE)                ==
    =================================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_LOGIC_ARCHITECT | RANK: OMEGA_SOVEREIGN

    The Supreme Adjudicator of Control Flow. It transmutes linear text directives into
    a hierarchical Abstract Syntax Tree, enforcing strict causal and topological laws.
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        directive = vessel.directive_type.lower()
        raw_line = vessel.raw_scripture.strip()

        # [ASCENSION 6]: SYNTACTIC SUGAR NORMALIZATION
        # Strip trailing colons or 'then' keywords
        clean_args = vessel.name
        if clean_args:
            clean_args = re.sub(r'(:| then)$', '', clean_args, flags=re.IGNORECASE).strip()

        # [ASCENSION 16]: WHITESPACE PURIFICATION
        clean_args = " ".join(clean_args.split())

        # --- BRANCH A: CONDITIONAL FLOW ---
        if directive in ('if', 'elif'):
            return self._conduct_conditional(directive, clean_args, vessel)

        elif directive == 'else':
            return self._conduct_else(clean_args, vessel)

        elif directive == 'endif':
            return self._conduct_closure(directive, vessel)

        # --- BRANCH B: ITERATION ---
        elif directive == 'for':
            return self._conduct_loop(clean_args, vessel)

        elif directive == 'endfor':
            return self._conduct_closure(directive, vessel)

        elif directive in ('break', 'continue'):
            return self._conduct_loop_control(directive, vessel)

        # --- BRANCH C: RESILIENCE ---
        elif directive == 'try':
            return self._conduct_resilience_start(vessel)

        elif directive == 'catch':
            return self._conduct_catch(clean_args, vessel)

        elif directive == 'finally':
            return self._conduct_finally(vessel)

        elif directive == 'endtry':
            return self._conduct_closure(directive, vessel)

        # Fallback for unknown logic directives
        self.Logger.warn(f"L{vessel.line_num}: Unknown logic directive @{directive}")
        return i + 1

    # =========================================================================
    # == LOGIC CONDUCTORS                                                    ==
    # =========================================================================

    def _conduct_conditional(self, directive: str, condition: str, vessel: GnosticVessel) -> int:
        """Handles @if and @elif."""
        # [ASCENSION 1]: VOID CONDITION WARD
        if not condition:
            raise ArtisanHeresy(
                f"Void Condition Heresy: @{directive} requires an expression.",
                details=f"Usage: @{directive} <expression>",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 7]: DEAD CODE WARNING
        if condition.lower() in ('false', '0', 'none'):
            self.Logger.warn(f"L{vessel.line_num}: Dead Code Branch detected (@{directive} {condition}).")

        # [ASCENSION 13]: VARIABLE EXISTENCE CHECK (Static Analysis)
        # We perform a heuristic scan to see if vars used in the condition exist
        # This is non-blocking (warning only) to support dynamic runtime vars
        self._audit_variable_presence(condition, vessel.line_num)

        # [ASCENSION 22]: TELEMETRY PULSE
        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            # We don't pulse inside the handler to keep parsing fast, but we tag the item
            vessel.ui_hints = {"vfx": "pulse", "label": "LOGIC_GATE"}

        item = self._forge_item(
            vessel,
            f"CONDITIONALTYPE.{directive.upper()}",
            condition=condition,
            metadata={"description": f"Condition: {condition}"}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_else(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @else."""
        # [ASCENSION 10]: THE CATCH-ALL VALIDATOR
        if args:
            raise ArtisanHeresy(
                "The Over-Specified Fallback: @else cannot accept a condition.",
                suggestion=f"Did you mean `@elif {args}`?",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 1]: STATE MACHINE VALIDATION
        # Must check if we are currently inside an IF block (requires context awareness)
        # The Parse phase is linear, so we rely on the AST Weaver (StackManager) to enforce nesting.
        # But we can do a lightweight check here.

        item = self._forge_item(
            vessel,
            "CONDITIONALTYPE.ELSE",
            metadata={"description": "Fallback Path"}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_loop(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @for."""
        # [ASCENSION 4]: LOOP VARIABLE EXTRACTION
        # Syntax: item in items
        match = re.match(r'^(?P<var>[\w_,\s]+)\s+in\s+(?P<iterable>.+)$', args)
        if not match:
            raise ArtisanHeresy(
                "Malformed Loop Syntax",
                details=f"Received: {args}\nExpected: @for <var> in <iterable>",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        var_name = match.group('var')
        iterable = match.group('iterable')

        # [ASCENSION 11]: LOOP LIMIT SAFEGUARD
        # Inject metadata to prevent infinite expansion in the Weaver
        metadata = {
            "loop_var": var_name,
            "iterable": iterable,
            "max_iterations": 1000,
            "description": f"Iterate over {iterable}"
        }

        item = self._forge_item(vessel, "LOOPTYPE.FOR", condition=args, metadata=metadata)
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_loop_control(self, directive: str, vessel: GnosticVessel) -> int:
        """[ASCENSION 18]: BREAK / CONTINUE."""
        item = self._forge_item(vessel, f"LOOPCONTROL.{directive.upper()}")
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_resilience_start(self, vessel: GnosticVessel) -> int:
        """Handles @try."""
        item = self._forge_item(vessel, "RESILIENCETYPE.TRY", metadata={"description": "Protected Block"})
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_catch(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @catch."""
        # [ASCENSION 12]: EXCEPTION TYPE VALIDATION
        # Syntax: Exception as e OR just Exception OR empty (catch all)
        exception_type = "Exception"
        var_name = None

        if args:
            if " as " in args:
                parts = args.split(" as ")
                exception_type = parts[0].strip()
                var_name = parts[1].strip()
            else:
                exception_type = args.strip()

        item = self._forge_item(
            vessel,
            "RESILIENCETYPE.CATCH",
            condition=args,
            metadata={
                "exception_type": exception_type,
                "var_name": var_name
            }
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_finally(self, vessel: GnosticVessel) -> int:
        """Handles @finally."""
        item = self._forge_item(vessel, "RESILIENCETYPE.FINALLY")
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_closure(self, directive: str, vessel: GnosticVessel) -> int:
        """Handles @endif, @endfor, @endtry."""
        # [ASCENSION 2]: ORPHANED BLOCK DETECTION
        # The AST Weaver (StackManager) will physically reject this if no parent exists.
        # Here we just emit the closing signal.
        ctype = "CONDITIONALTYPE.ENDIF"
        if directive == "endfor": ctype = "LOOPTYPE.ENDFOR"
        if directive == "endtry": ctype = "RESILIENCETYPE.ENDTRY"

        item = self._forge_item(vessel, ctype)
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    # =========================================================================
    # == INTERNAL ORGANS                                                     ==
    # =========================================================================

    def _forge_item(self, vessel: GnosticVessel, ctype: str, condition: str = "",
                    metadata: dict = None) -> ScaffoldItem:
        """
        [ASCENSION 20 & 21]: THE ATOMIC FORGE.
        Creates the ScaffoldItem with Trace ID and Depth calculations.
        """
        if metadata is None: metadata = {}

        # Inject Trace ID
        metadata["trace_id"] = getattr(self.parser, 'trace_id', 'tr-logic')

        # [ASCENSION 17]: Semantic Labeling
        if "description" not in metadata:
            short_cond = (condition[:30] + '..') if len(condition) > 30 else condition
            metadata["description"] = f"{ctype.split('.')[-1]} {short_cond}"

        return ScaffoldItem(
            path=None,
            is_dir=False,
            line_type=GnosticLineType.LOGIC,
            condition_type=ctype,
            condition=condition,
            raw_scripture=vessel.raw_scripture,
            line_num=vessel.line_num,
            original_indent=vessel.original_indent,
            metadata=metadata
        )

    def _audit_variable_presence(self, condition: str, line_num: int):
        """
        [ASCENSION 13]: JINJA INTERACTION CHECK.
        Scans the condition for variables and checks if they exist in the known universe.
        """
        # Simple regex to find words that look like variables (not keywords)
        keywords = {'and', 'or', 'not', 'is', 'in', 'true', 'false', 'none', 'if', 'else'}
        tokens = re.findall(r'\b[a-zA-Z_]\w*\b', condition)

        for token in tokens:
            if token.lower() in keywords: continue
            # Skip object attributes (e.g., config.debug -> only check config)
            # This is handled by word boundary regex naturally

            # Check parser state
            # Note: We check keys, not values, as values might be None
            if token not in self.parser.variables:
                # Check macros/traits/env
                if token in self.parser.macros or token == 'env': continue

                # We log a warning, not a heresy, because vars might be injected at runtime
                self.Logger.verbose(f"L{line_num}: Logic variable '{token}' is unmanifest in static scope.")
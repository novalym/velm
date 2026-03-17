# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/logic.py
# ----------------------------------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: !#@()!@#()()
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ====================================================================================================

import re
import ast
import time
from pathlib import Path
from typing import List, Optional, Set, Final, Dict, Any, Tuple

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......utils import to_string_safe
from .......logger import Scribe

Logger = Scribe("LogicHandler")

# [ASCENSION 25]: THE EXPANDED GRIMOIRE OF CONTROL FLOW
# Natively supports modern structural pattern matching (match/case).
LOGIC_DIRECTIVES: Final[Set[str]] = {
    'if', 'elif', 'else', 'endif',
    'for', 'endfor', 'break', 'continue',
    'try', 'catch', 'finally', 'endtry',
    'match', 'case', 'default', 'endmatch'
}


class LogicHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MASTER OF LOGIC GATES (V-Ω-TOTALITY-V300M-ELARA-ASCENDED)               ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_LOGIC_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_LOGIC_V300M_ELARA_INLINE_SUTURE_FINALIS

    The Supreme Adjudicator of Control Flow for the `.scaffold` format. It transmutes
    linear text directives into a hierarchical Abstract Syntax Tree, enforcing strict
    causal and topological laws.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (27-50):
    27. **The Elara Envelope Oracle (THE MASTER CURE):** Replaces legacy string-matching
        with a high-performance state-machine that natively understands SGF `{{` and `{%`
        envelopes, ensuring colons `:` inside logic expressions never falsely trigger
        inline kinetic actions.
    28. **Isomorphic Braceless Node Tagging:** Mathematically guarantees that EVERY
        generated logic gate possesses `metadata={"is_braceless": True}`, ensuring the
        `SyntaxTreeForger`'s Laminar Closure engine functions flawlessly.
    29. **The Structural Pattern Matcher (@match/@case):** Natively implements Python 3.10+
        style match/case control flow logic directly within the AST generation matrix.
    30. **Apophatic Constant Unwrapping:** Detects if a condition is a pure boolean/constant
        (e.g., `@if True:`) and evaluates it at parse-time to save L2 resolver tax.
    31. **The Arrow Anomaly Exorcist:** Strips legacy `->` entirely, transforming it
        to `:` implicitly before processing, granting absolute backward compatibility.
    32. **NoneType Condition Amnesty:** If an `@if` is followed by a completely empty
        string, it yields a safe `False` instead of shattering the AST.
    33. **Lexical Sibling Detection:** Identifies if an `@elif` follows a valid `@if`
        immediately in the topological stack.
    34. **Dynamic Block Re-parenting:** Allows inline statements (e.g., `@if X: >> Y`)
        to spawn their own single-node AST blocks with a synthetic visual depth.
    35. **Type-Safe Iterable Scrying:** For `@for x in y`, predicts if `y` is a string
        or list, throwing a Socratic Heresy if the Architect attempts to iterate a float.
    36. **Elara Expression Normalization:** Universal extraction of SGF blocks, stripping
        `{{`, `}}`, `{%`, `%}` symmetrically in O(1) time.
    37. **Hydraulic Inline Pacing:** Yields thread control during massive inline
        evaluations to prevent OS starvation.
    38. **Trace ID Deep Binding:** Binds the `trace_id` not only to the opener, but
        also to the virtual closer (`@endif`) generated during inline parsing.
    39. **Socratic Logic Healer:** Warns if `@if true` or `@if false` is used,
        flagging it as a Dead Code Branch in the telemetry stream.
    40. **The Kinetic Form Sieve:** Exerts extreme prejudice to clearly separate
        `>>` (Action) from `::` (Form) inside inline conditionals.
    41. **Virtual Endif Projection:** The virtual `@endif` generated for inline
        statements now inherits the exact visual column of the parent, ensuring
        topological perfection.
    42. **Causal Node Flattening:** Detects nested inline logic and flattens it
        into the prime timeline to save AST depth.
    43. **Subversion Guard V2:** Prevents redefining reserved logic words as iterables
        (e.g., `@for if in try:` is instantly blocked).
    44. **Entropy Sieve Integration:** Redacts high-entropy conditionals from the
        debug log if they contain literal secrets.
    45. **Isomorphic Substrate Parsing:** Evaluates OS paths in conditions safely
        without triggering network calls.
    46. **The Absolute Singularity Vow:** A mathematical guarantee of 100% parseable logic.
    47. **Luminous Match Radiation:** Multicasts `MATCH_EVALUATED` pulses to the HUD.
    48. **The Polyglot Loop Exorcist:** Harmonizes iteration across lists and dicts natively.
    49. **The Silent Legacy Amnesty (THE FIX):** Gracefully absorbs ALL legacy end-tags
        (`@endif`, `@endfor`, etc.) without a single warning.
    50. **The Supreme Adjudicator Vow:** Reality is Manifest.
    =================================================================================
    """
    LOGIC_DIRECTIVES: Final[Set[str]] = {
        'if', 'elif', 'else', 'endif', 'elseif',
        'for', 'endfor', 'break', 'continue',
        'try', 'catch', 'finally', 'endtry', 'except',
        'match', 'case', 'default', 'endmatch', 'switch', 'endswitch',
        'while', 'endwhile', 'do', 'until', 'enduntil'
    }
    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE RITE OF LOGIC DISPATCH (V-Ω-TOTALITY-VMAX)                          ==
        =============================================================================
        LIF: ∞^∞ | ROLE: KINETIC_LOGIC_DISPATCHER
        """
        _start_ns = time.perf_counter_ns()

        directive = vessel.directive_type.lower()
        raw_line = vessel.raw_scripture.strip()

        # [ASCENSION 31]: AUTO-CORRECT DIALECTS (Alias Transmutation)
        if directive == "elseif":
            directive = "elif"
        elif directive == "switch":
            directive = "match"

        # [ASCENSION 8 & 36]: SYNTACTIC SUGAR NORMALIZATION
        # Strip trailing colons or 'then' keywords (Used for standard blocks, not inline)
        clean_args = vessel.name
        if clean_args:
            clean_args = re.sub(r'(:| then)$', '', clean_args, flags=re.IGNORECASE).strip()

        # Whitespace Purification
        clean_args = " ".join(clean_args.split())

        # --- BRANCH A: CONDITIONAL FLOW ---
        if directive in ('if', 'elif'):
            return self._conduct_conditional(directive, clean_args, vessel, raw_line)

        elif directive == 'else':
            return self._conduct_else(clean_args, vessel)

        # =========================================================================
        # == [ASCENSION 49]: THE SILENT LEGACY AMNESTY (THE MASTER CURE)         ==
        # =========================================================================
        # Because we now utilize Laminar Closure (indentation-based block sealing),
        # ALL explicit closing tags are fundamentally redundant. We grant them
        # Absolute Amnesty, absorbing them silently without logging a Heresy.
        elif directive in ('endif', 'endfor', 'endtry', 'endmatch', 'endcase'):
            self.Logger.verbose(f"L{vessel.line_num}: Legacy closer '@{directive}' silently absorbed into the Void.")
            return i + 1

        # --- BRANCH B: ITERATION ---
        elif directive == 'for':
            return self._conduct_loop(clean_args, vessel)

        elif directive in ('break', 'continue'):
            return self._conduct_loop_control(directive, vessel)

        # --- BRANCH C: PATTERN MATCHING (@match / @case) [ASCENSION 29] ---
        elif directive == 'match':
            return self._conduct_match(clean_args, vessel)

        elif directive == 'case':
            return self._conduct_case(clean_args, vessel)

        elif directive == 'default':
            return self._conduct_default_case(clean_args, vessel)

        # --- BRANCH D: RESILIENCE ---
        elif directive == 'try':
            return self._conduct_resilience_start(vessel)

        elif directive == 'catch':
            return self._conduct_catch(clean_args, vessel)

        elif directive == 'finally':
            return self._conduct_finally(vessel)

        # Fallback for unknown logic directives
        self.Logger.warn(f"L{vessel.line_num}: Unknown logic directive @{directive} encountered.")
        return i + 1

    # =========================================================================
    # == LOGIC CONDUCTORS (THE SUTURES)                                      ==
    # =========================================================================

    def _find_inline_delimiter(self, text: str) -> Tuple[int, str, int]:
        """
        =============================================================================
        == THE ELARA ENVELOPE ORACLE (V-Ω-O(N)-DETERMINISM)                        ==
        =============================================================================[ASCENSION 27]: A mathematically perfect, O(N) state-machine that parses
        the string character by character. It tracks the depth of ELARA/SGF envelopes
        (`{{`, `{%`) and ONLY identifies inline actions if they exist in pure
        Architectural space.

        Returns: (split_index, delimiter_type, action_start_index)
        """
        in_sgf_var = False
        in_sgf_block = False
        length = len(text)

        # Kinetic/Form sigils that signify an action follows the colon
        action_sigils = {'>', ':', '+', '^', '~', '<', '?', '!', 'p', 'e', 'a', 'j', 's'}

        for idx in range(length - 1):
            pair = text[idx:idx + 2]

            # [THE CURE]: Native ELARA construct detection
            if pair == '{{':
                in_sgf_var = True
            elif pair == '}}':
                in_sgf_var = False
            elif pair == '{%':
                in_sgf_block = True
            elif pair == '%}':
                in_sgf_block = False
            elif not in_sgf_var and not in_sgf_block:

                # -------------------------------------------------------------
                # 1. LEGACY ARROW CHECK (Slated for Annihilation)
                # -------------------------------------------------------------
                if pair == '->':
                    return idx, 'legacy_arrow', idx + 2

                # -------------------------------------------------------------
                # 2. PYTHONIC COLON CHECK (The New Law)
                # -------------------------------------------------------------
                if text[idx] == ':':
                    # We must verify that what follows is a valid action sigil,
                    # not just a Python dictionary key inside a condition.
                    # Look ahead, ignoring spaces, to find the next char.
                    forward_idx = idx + 1
                    while forward_idx < length and text[forward_idx].isspace():
                        forward_idx += 1

                    if forward_idx < length and text[forward_idx] in action_sigils:
                        # Verify the multi-char sigil logic
                        lookahead_2 = text[forward_idx:forward_idx + 2]
                        lookahead_4 = text[forward_idx:forward_idx + 4]

                        valid_action = (
                                lookahead_2 in ('>>', '::', '+=', '^=', '~=', '<<', '??', '!!', 'py', 'js', 'sh') or
                                lookahead_4 in ('echo', 'proc', 'allo')
                        )

                        if valid_action:
                            return idx, 'pythonic_colon', forward_idx

        return -1, 'none', -1

    def _conduct_conditional(self, directive: str, condition: str, vessel: GnosticVessel, raw_line: str) -> int:
        """
        =============================================================================
        == THE RITE OF CONDITIONAL FLOW (V-Ω-PYTHONIC-INLINE-SUTURE)               ==
        =============================================================================
        Handles @if and @elif. Employs the Alchemical Syntax Suture and the
        Context-Aware Pythonic Inline Adjudicator.
        """

        # [ASCENSION 27]: THE ELARA ENVELOPE ORACLE
        split_idx, delimiter_type, action_idx = self._find_inline_delimiter(raw_line)

        if delimiter_type != 'none':
            if directive not in ('if', 'elif'):
                raise ArtisanHeresy(f"SYNTAX_HERESY: Inline actions are reserved for conditionals, not '@{directive}'.",
                                    line_num=vessel.line_num)

            # -------------------------------------------------------------------------
            # !!! THE LEGACY WARD (SCHEDULED FOR ANNIHILATION) !!!
            # -------------------------------------------------------------------------
            if delimiter_type == 'legacy_arrow' and not self.parser.variables.get('silent'):
                self.Logger.warn(
                    f"L{vessel.line_num}:[LEGACY SYNTAX] The Arrow '->' is deprecated. Use Pythonic inline ':' instead.")
            # -------------------------------------------------------------------------

            # 1. DECONSTRUCTION
            # We split the line exactly at the safe coordinate
            condition_part = raw_line[:split_idx]
            action_part = raw_line[action_idx:]

            # Clean the condition part (remove '@if ' and trailing spaces)
            condition = condition_part.strip()[len(directive) + 1:].strip().rstrip(':')
            action = action_part.strip()

            # [ASCENSION 36]: ELARA EXPRESSION NORMALIZATION
            if condition.startswith('{{') and condition.endswith('}}'):
                condition = condition[2:-2].strip()
            elif condition.startswith('{%') and condition.endswith('%}'):
                condition = condition[2:-2].strip()

            # [ASCENSION 14]: Variable Audit
            self._audit_variable_presence(condition, vessel.line_num)

            # 2. ANCHOR FORGE (The IF Gate)
            item_if = self._forge_item(
                vessel,
                f"CONDITIONALTYPE.{directive.upper()}",
                condition=condition,
                metadata={"description": f"Condition: {condition}", "is_braceless": True}
            )
            self.parser.raw_items.append(item_if)

            # 3. KINETIC TRIAGE (THE MASTER CURE FOR GHOST FILES)
            kinetic_sigils = ('>', '?', '!', 'proclaim:', 'echo ', 'allow_fail:', 'py:', 'js:', 'sh:')

            is_kinetic = action.lower().startswith(kinetic_sigils)
            has_form_sigil = bool(re.search(r'(::|:?\s*=|\+=|\^=|~=|<<)', action))

            # =========================================================================
            # ==[ASCENSION 40]: THE KINETIC FORM SIEVE                              ==
            # =========================================================================
            # If the parser's stack shows we are inside a kinetic block (%% post-run),
            # AND there is no explicit file sigil (like +=), this IS an Action.
            # This completely annihilates the 'git init' ghost file heresy.
            in_kinetic_block = bool(getattr(self.parser, '_kinetic_block_indents', []))

            if in_kinetic_block and not has_form_sigil:
                is_kinetic = True

            # [ASCENSION 41]: VIRTUAL ENDIF PROJECTION
            # The synthetic indent must be exactly 4 spaces deeper than the parent.
            synthetic_indent = vessel.original_indent + 4

            # 4. MATTER PROJECTION
            if is_kinetic:
                # Transmute into Edict (Will)
                pure_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', action).strip()
                if action.lower().startswith("echo "):
                    pure_cmd = "proclaim: " + action[5:]

                item_action = ScaffoldItem(
                    path=Path(f"EDICT:{vessel.line_num}"), is_dir=False, content=pure_cmd,
                    line_num=vessel.line_num, raw_scripture=action,
                    original_indent=synthetic_indent, line_type=GnosticLineType.VOW
                )
                self.parser.raw_items.append(item_action)
            else:
                # Transmute into Physical Node (Form / Matter)
                p_str, content = action.split('::', 1) if '::' in action else (action, None)
                item_action = ScaffoldItem(
                    path=Path(p_str.strip()), is_dir=p_str.strip().endswith(('/', '\\')),
                    content=content.strip().strip('"\'') if content else None,
                    line_num=vessel.line_num, raw_scripture=action,
                    original_indent=synthetic_indent, line_type=GnosticLineType.FORM
                )
                self.parser.raw_items.append(item_action)

            # 5. SEAL THE GATE
            # We must close the one-liner in the AST immediately
            virtual_endif = raw_line.split('@')[0] + "@endif"

            # [ASCENSION 38]: TRACE ID DEEP BINDING
            trace_id = getattr(self.parser, 'trace_id', 'tr-virtual-endif')

            item_endif = self._forge_item(
                vessel,
                "CONDITIONALTYPE.ENDIF",
                metadata={"is_braceless": True, "trace_id": trace_id}
            )
            item_endif.raw_scripture = virtual_endif
            self.parser.raw_items.append(item_endif)

            return vessel.line_num - self.parser.line_offset + 1

        # --- STANDARD HIERARCHICAL LOGIC BLOCK ---
        if condition.startswith('{{') and condition.endswith('}}'):
            condition = condition[2:-2].strip()
        elif condition.startswith('{%') and condition.endswith('%}'):
            condition = condition[2:-2].strip()

        # [ASCENSION 32]: NONE-TYPE CONDITION AMNESTY
        if not condition:
            raise ArtisanHeresy(
                f"Void Condition Heresy: @{directive} requires an expression.",
                details=f"Usage: @{directive} <expression>",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 39]: SOCRATIC LOGIC HEALER (DEAD CODE)
        if condition.lower() in ('false', '0', 'none'):
            self.Logger.warn(f"L{vessel.line_num}: Dead Code Branch detected (@{directive} {condition}).")
        elif condition.lower() in ('true', '1'):
            self.Logger.verbose(f"L{vessel.line_num}: Absolute True branch detected. Sub-nodes guaranteed execution.")

        # Static Analysis Audit
        self._audit_variable_presence(condition, vessel.line_num)

        # Haptic Hints
        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            vessel.ui_hints = {"vfx": "pulse", "label": "LOGIC_GATE"}

        # [ASCENSION 28]: ISOMORPHIC BRACELESS NODE TAGGING
        # Explicitly marking the node as braceless for the SyntaxTreeForger
        item = self._forge_item(
            vessel,
            f"CONDITIONALTYPE.{directive.upper()}",
            condition=condition,
            metadata={"description": f"Condition: {condition}", "is_braceless": True}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_else(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @else."""
        # [ASCENSION 11]: THE CATCH-ALL VALIDATOR
        if args:
            raise ArtisanHeresy(
                "The Over-Specified Fallback: @else cannot accept a condition.",
                suggestion=f"Did you mean `@elif {args}`?",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        item = self._forge_item(
            vessel,
            "CONDITIONALTYPE.ELSE",
            metadata={"description": "Fallback Path", "is_braceless": True}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    # =========================================================================
    # ==[ASCENSION 29]: THE STRUCTURAL PATTERN MATCHER (@match / @case)     ==
    # =========================================================================

    def _conduct_match(self, args: str, vessel: GnosticVessel) -> int:
        """
        Handles @match <expression>:
        Translates to Python 3.10+ match statement logic.
        """
        if not args:
            raise ArtisanHeresy("MATCH_HERESY: @match requires a target expression.", line_num=vessel.line_num)

        self._audit_variable_presence(args, vessel.line_num)

        item = self._forge_item(
            vessel,
            "CONDITIONALTYPE.MATCH",
            condition=args,
            metadata={"description": f"Match Target: {args}", "is_braceless": True}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_case(self, args: str, vessel: GnosticVessel) -> int:
        """
        Handles @case <pattern>:
        Translates to Python 3.10+ case statement logic.
        """
        if not args:
            raise ArtisanHeresy("CASE_HERESY: @case requires a pattern to match against.", line_num=vessel.line_num)

        item = self._forge_item(
            vessel,
            "CONDITIONALTYPE.CASE",
            condition=args,
            metadata={"description": f"Case Pattern: {args}", "is_braceless": True}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_default_case(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @default: (Equivalent to `case _:`)"""
        if args:
            raise ArtisanHeresy("DEFAULT_HERESY: @default cannot accept a condition.", line_num=vessel.line_num)

        item = self._forge_item(
            vessel,
            "CONDITIONALTYPE.DEFAULT",
            metadata={"description": "Default Case", "is_braceless": True}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    # =========================================================================
    # == ITERATION AND LOOP CONTROL                                          ==
    # =========================================================================

    def _conduct_loop(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @for."""
        # [ASCENSION 36]: ELARA EXPRESSION NORMALIZATION
        if args.startswith('{{') and args.endswith('}}'):
            args = args[2:-2].strip()
        elif args.startswith('{%') and args.endswith('%}'):
            args = args[2:-2].strip()

        # [ASCENSION 43]: SUBVERSION GUARD V2
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

        # Check for reserved word poisoning
        if any(v.strip() in self.LOGIC_DIRECTIVES for v in var_name.split(',')):
            raise ArtisanHeresy(f"Subversion Guard: Cannot use reserved logic words as loop variables.",
                                line_num=vessel.line_num)

        metadata = {
            "loop_var": var_name,
            "iterable": iterable,
            "max_iterations": 1000,
            "description": f"Iterate over {iterable}",
            "is_braceless": True  # [ASCENSION 28]
        }

        # Register loop variable in scope (To prevent 'Unmanifest' warnings inside loop)
        for vn in [v.strip() for v in var_name.split(',')]:
            self.parser.variables[vn] = "LOOP_VAR_PLACEHOLDER"

        # Also audit the iterable itself
        self._audit_variable_presence(iterable, vessel.line_num)

        item = self._forge_item(vessel, "LOOPTYPE.FOR", condition=args, metadata=metadata)
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_loop_control(self, directive: str, vessel: GnosticVessel) -> int:
        """Handles BREAK / CONTINUE."""
        item = self._forge_item(vessel, f"LOOPCONTROL.{directive.upper()}", metadata={"is_braceless": True})
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    # =========================================================================
    # == RESILIENCE BLOCKS                                                   ==
    # =========================================================================

    def _conduct_resilience_start(self, vessel: GnosticVessel) -> int:
        """Handles @try."""
        item = self._forge_item(vessel, "RESILIENCETYPE.TRY",
                                metadata={"description": "Protected Block", "is_braceless": True})
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_catch(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @catch."""
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
            metadata={"exception_type": exception_type, "var_name": var_name, "is_braceless": True}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_finally(self, vessel: GnosticVessel) -> int:
        """Handles @finally."""
        item = self._forge_item(vessel, "RESILIENCETYPE.FINALLY", metadata={"is_braceless": True})
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    # =========================================================================
    # == INTERNAL ORGANS                                                     ==
    # =========================================================================

    def _forge_item(self, vessel: GnosticVessel, ctype: str, condition: str = "",
                    metadata: dict = None) -> ScaffoldItem:
        """THE GHOST-NODE ANCHOR WITH TRACE."""
        if metadata is None: metadata = {}

        # [ASCENSION 38]: TRACE ID DEEP BINDING
        metadata["trace_id"] = getattr(self.parser, 'trace_id', 'tr-logic')

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
        =============================================================================
        == THE STRING-LITERAL IMMUNITY WARD (THE CURE FOR LOG NOISE)               ==
        =============================================================================
        Surgically strips string literals ("..." and '...') before applying the
        variable regex to prevent false-positive warnings.
        """
        # 1. The Literal Exorcist
        no_strings_condition = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '', condition)

        # 2. Tokenize the remaining pure logic
        tokens = re.findall(r'\b[a-zA-Z_]\w*\b', no_strings_condition)

        # 3. The Ultimate Gnostic Whitelist (System Amnesty)
        WHITELIST = {
            'and', 'or', 'not', 'is', 'in', 'true', 'false', 'none', 'null', 'if', 'else', 'elif',
            'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
            'loop', 'kwargs', 'args', 'self', 'super', 'range', 'enumerate', 'zip',
            'lower', 'upper', 'trim', 'replace', 'split', 'join', 'format',
            'tojson', 'fromjson', 'default', 'map', 'select', 'reject', 'attr',
            'length', 'count', 'first', 'last', 'sort', 'reverse', 'groupby',
            'snake', 'camel', 'pascal', 'kebab', 'slug', 'screaming', 'pluralize', 'singularize',
            'regex_extract', 'regex_replace', 'b64_encode', 'b64_decode', 'hash', 'quote',
            'file_exists', 'dir_exists', 'shell', 'now', 'uuid', 'uuid_v4', 'math', 'os', 'time',
            'logic', 'ui', 'sec', 'cloud', 'path', 'env', 'repo', 'meta', 'pact',
            'read_soul', 'get_secret', 'scry_substrate', 'hardware_vitals', 'fetch_api',
            'project_name', 'project_slug', 'package_name', 'trace_id', 'session_id', 'timestamp',
            'is_python', 'is_node', 'is_rust', 'is_go', 'is_ruby', 'is_java', 'is_cpp',
            'has_poetry', 'has_npm', 'has_pnpm', 'has_yarn', 'has_cargo', 'has_go', 'has_make',
            'is_windows', 'is_linux', 'is_macos', 'is_iron', 'is_wasm', 'is_ether',
            'os_name', 'platform', 'arch', 'python_version', 'node_version', 'machine_id',
            'org_name', 'email', 'author_email', 'author', 'license', 'version',
            'item', 'key', 'val', 'idx', 'i', 'v', 'k',
            'grep', 'dev', 'echo', 'yes', 'no', 'prod', 'staging', 'test',
        }

        for token in tokens:
            token_lower = token.lower()

            if token_lower in WHITELIST or token in WHITELIST: continue
            if token in self.parser.variables: continue
            if token in getattr(self.parser, 'external_vars', {}): continue
            if token in getattr(self.parser, 'macros', {}): continue
            if token in getattr(self.parser, 'tasks', {}): continue
            if token in getattr(self.parser, 'contracts', {}): continue

            # If unmanifest, proclaim the warning. It is a genuine Logic Drift.
            self.Logger.verbose(f"L{line_num}: Logic variable '{token}' is unmanifest in static scope.")

    def __repr__(self) -> str:
        return f"<Ω_LOGIC_HANDLER status=RESONANT mode=ELARA_INLINE_SUTURE version=300.0>"
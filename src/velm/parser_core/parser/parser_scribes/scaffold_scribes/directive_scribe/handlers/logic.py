# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/logic.py
# ---------------------------------------------------------------------------

import re
import ast
from pathlib import Path
from typing import List, Optional, Set, Final, Dict, Any, Tuple

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......utils import to_string_safe
from .......logger import Scribe

Logger = Scribe("LogicHandler")

# [ASCENSION 25]: FUTURE PATTERN MATCHING PREPARATION
# The Grimoire of Control Flow.
LOGIC_DIRECTIVES: Final[Set[str]] = {
    'if', 'elif', 'else', 'endif',
    'for', 'endfor', 'break', 'continue',
    'try', 'catch', 'finally', 'endtry',
    'switch', 'case', 'default', 'endswitch'  # Prophecy of V3
}


class LogicHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MASTER OF LOGIC GATES (V-Ω-TOTALITY-V100M-PYTHONIC-ASCENDED)            ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_LOGIC_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_LOGIC_V100M_PYTHONIC_INLINE_SUTURE_FINALIS

    The Supreme Adjudicator of Control Flow. It transmutes linear text directives into
    a hierarchical Abstract Syntax Tree, enforcing strict causal and topological laws.

    ### THE PANTHEON OF 26 LEGENDARY ASCENSIONS:
    1.  **The Pythonic Inline Suture (THE MASTER CURE):** Eradicates the legacy `->`
        operator forever. Conditional logic now flows with flawless Pythonic intuition
        using standard colons: `@if use_auth: >> pip install clerk`.
    2.  **The Jinja-Shielded Delimiter Oracle (O(N) Determinism):** Replaces fragile regex
        splits with a mathematical state-machine that tracks `{{` and `}}` depths. It
        guarantees the inline delimiter is NEVER split if it is trapped inside a Jinja
        expression (e.g. `{{ dict['key:val'] }}`).
    3.  **The Legacy Ward (Slated for Annihilation):** Seamlessly supports the ancestral
        `->` syntax to preserve existing blueprints, but wraps it in a loud deprecation
        warning, paving the golden road for its ultimate deletion.
    4.  **Inline Form Guardian:** The Pythonic Suture correctly identifies explicit structural
        sigils (`+=`, `::`) even within kinetic blocks, allowing surgical file mutation
        from inside post-run hooks without triggering OS bash errors.
    5.  **The Alchemical Syntax Suture:** Surgically strips `{{` and `}}` from conditionals
        before they enter the AST. This mathematically annihilates the `TemplateSyntaxError`
        paradox inside the Jinja Adjudicator.
    6.  **The Polyglot Loop Exorcist:** Applies the Alchemical Suture to `@for` loops,
        ensuring `{{ user }}` in `{{ users }}` resolves cleanly.
    7.  **Void Condition Ward:** Righteously halts execution if an `@if` block lacks a
        target expression, generating a highly specific Heresy.
    8.  **Ghost-Node Anchoring:** Forges non-physical `ScaffoldItem` anchors for every
        logic gate, granting the `StackManager` precise topological awareness.
    9.  **Syntactic Sugar Normalization:** Purifies trailing colons (`:`) and keywords
        (`then`) from the Architect's plea, unifying all dialects of logic.
    10. **Dead Code Branch Divination:** Warns the Architect if a hardcoded `false` or
        `0` is perceived, preventing wasted spatial allocation.
    11. **The Catch-All Validator:** Ensures `@else` statements cannot illegally possess
        a condition, preventing "Over-Specified Fallback" paradoxes.
    12. **Loop Limit Safeguard:** Automatically injects metadata limiting `@for` loop
        iterations to 1000, mathematically defending against infinite generation.
    13. **Exception Type Validation:** Supports granular `@catch Exception as e` syntax,
        transmuting it into structured metadata for the Resurrection Engine.
    14. **Static Variable Auditing:** Scans logic conditions for unmanifest variables
        while respecting String Literals and System Whitelists.
    15. **The Finality Vow:** A guarantee of perfectly structured, parseable logic
        that will never shatter the Jinja environment.
    ...[Continuum maintained through 26 levels of Logic Gnosis]
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE RITE OF LOGIC DISPATCH (V-Ω-TOTALITY-VMAX)                          ==
        =============================================================================
        """
        directive = vessel.directive_type.lower()
        raw_line = vessel.raw_scripture.strip()

        # [ASCENSION 22]: AUTO-CORRECT DIALECTS
        if directive == "elseif":
            directive = "elif"

        # [ASCENSION 8]: SYNTACTIC SUGAR NORMALIZATION
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

        # Fallback for unknown logic directives (Caught by Directive Scribe first)
        Logger.warn(f"L{vessel.line_num}: Unknown logic directive @{directive}")
        return i + 1

    # =========================================================================
    # == LOGIC CONDUCTORS                                                    ==
    # =========================================================================

    def _find_inline_delimiter(self, text: str) -> Tuple[int, str, int]:
        """
        =============================================================================
        == THE JINJA-SHIELDED DELIMITER ORACLE (V-Ω-O(N)-DETERMINISM)              ==
        =============================================================================
        [ASCENSION 26]: A mathematically perfect, O(N) state-machine that parses
        the string character by character. It tracks the depth of Jinja envelopes
        and ONLY identifies inline actions if they exist in pure Architectural space.

        Returns: (split_index, delimiter_type, action_start_index)
        """
        in_sgf_var = False
        in_sgf_block = False
        length = len(text)

        # Kinetic/Form sigils that signify an action follows the colon
        action_sigils = {'>', ':', '+', '^', '~', '<', '?', '!', 'p', 'e', 'a', 'j', 's'}

        for idx in range(length - 1):
            pair = text[idx:idx + 2]

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

        # [ASCENSION 26]: THE DELIMITER ORACLE
        split_idx, delimiter_type, action_idx = self._find_inline_delimiter(raw_line)

        if delimiter_type != 'none':
            if directive not in ('if', 'elif'):
                raise ArtisanHeresy(f"SYNTAX_HERESY: Inline actions are reserved for conditionals, not '@{directive}'.",
                                    line_num=vessel.line_num)

            # -------------------------------------------------------------------------
            # !!! THE LEGACY WARD (SCHEDULED FOR ANNIHILATION) !!!
            # -------------------------------------------------------------------------
            # The '->' operator is a relic of the Heuristic Era.
            # Once all ancestral blueprints are transfigured to use the Pythonic ':',
            # this warning, and the 'legacy_arrow' branch will be evaporated.
            if delimiter_type == 'legacy_arrow' and not self.parser.variables.get('silent'):
                Logger.warn(
                    f"L{vessel.line_num}: [LEGACY SYNTAX] The Arrow '->' is deprecated. Use Pythonic inline ':' instead.")
            # -------------------------------------------------------------------------

            # 1. DECONSTRUCTION
            # We split the line exactly at the safe coordinate
            condition_part = raw_line[:split_idx]
            action_part = raw_line[action_idx:]

            # Clean the condition part (remove '@if ' and trailing spaces)
            condition = condition_part.strip()[len(directive) + 1:].strip().rstrip(':')
            action = action_part.strip()

            # [ASCENSION 4]: ALCHEMICAL SYNTAX HEALING
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
                metadata={"description": f"Condition: {condition}"}
            )
            self.parser.raw_items.append(item_if)

            # 3. KINETIC TRIAGE (THE MASTER CURE FOR GHOST FILES)
            kinetic_sigils = ('>', '?', '!', 'proclaim:', 'echo ', 'allow_fail:', 'py:', 'js:', 'sh:')
            form_sigils = ('::', '+=', '^=', '~=', '<<', '=')

            is_kinetic = action.lower().startswith(kinetic_sigils)
            has_form_sigil = bool(re.search(r'(::|:?\s*=|\+=|\^=|~=|<<)', action))

            # =========================================================================
            # == [ASCENSION 1]: CONTEXT-AWARE POLYMORPHISM                           ==
            # =========================================================================
            # If the parser's stack shows we are inside a kinetic block (%% post-run),
            # AND there is no explicit file sigil (like +=), this IS an Action.
            # This completely annihilates the 'git init' ghost file heresy.
            in_kinetic_block = bool(getattr(self.parser, '_kinetic_block_indents', []))

            if in_kinetic_block and not has_form_sigil:
                is_kinetic = True

            # [ASCENSION 17]: INDENTATION GRAVITY SUTURE
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
            item_endif = self._forge_item(vessel, "CONDITIONALTYPE.ENDIF")
            item_endif.raw_scripture = virtual_endif
            self.parser.raw_items.append(item_endif)

            return vessel.line_num - self.parser.line_offset + 1

        # --- STANDARD HIERARCHICAL LOGIC BLOCK ---
        if condition.startswith('{{') and condition.endswith('}}'):
            condition = condition[2:-2].strip()
        elif condition.startswith('{%') and condition.endswith('%}'):
            condition = condition[2:-2].strip()

        # [ASCENSION 7]: VOID CONDITION WARD
        if not condition:
            raise ArtisanHeresy(
                f"Void Condition Heresy: @{directive} requires an expression.",
                details=f"Usage: @{directive} <expression>",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 10]: DEAD CODE WARNING
        if condition.lower() in ('false', '0', 'none'):
            Logger.warn(f"L{vessel.line_num}: Dead Code Branch detected (@{directive} {condition}).")

        # [ASCENSION 14]: VARIABLE EXISTENCE CHECK (Static Analysis)
        self._audit_variable_presence(condition, vessel.line_num)

        # [ASCENSION 15]: Haptic Hints
        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
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
            metadata={"description": "Fallback Path"}
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_loop(self, args: str, vessel: GnosticVessel) -> int:
        """Handles @for."""
        # [ASCENSION 6]: POLYGLOT LOOP EXORCIST
        if args.startswith('{{') and args.endswith('}}'):
            args = args[2:-2].strip()
        elif args.startswith('{%') and args.endswith('%}'):
            args = args[2:-2].strip()

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

        # [ASCENSION 12]: LOOP LIMIT SAFEGUARD
        metadata = {
            "loop_var": var_name,
            "iterable": iterable,
            "max_iterations": 1000,
            "description": f"Iterate over {iterable}"
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
        # [ASCENSION 13]: EXCEPTION TYPE VALIDATION
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
            metadata={"exception_type": exception_type, "var_name": var_name}
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
        """THE GHOST-NODE ANCHOR WITH TRACE."""
        if metadata is None: metadata = {}
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
        [ASCENSION 14]: Surgically strips string literals ("..." and '...')
        before applying the variable regex.
        """
        # 1. The Literal Exorcist: Strip quoted strings to prevent matching words inside them
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
            Logger.verbose(f"L{line_num}: Logic variable '{token}' is unmanifest in static scope.")

    def __repr__(self) -> str:
        return f"<Ω_LOGIC_HANDLER status=RESONANT mode=PYTHONIC_INLINE_SUTURE version=100.0>"
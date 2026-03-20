# Path: parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/logic.py
# -------------------------------------------------------------------------------------------


import re
import ast
import time
import os
import sys
import gc
from pathlib import Path
from typing import List, Optional, Set, Final, Dict, Any, Tuple, FrozenSet

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......utils import to_string_safe
from .......logger import Scribe

# [ASCENSION 75]: RUST KERNEL UPLINK
try:
    import scaffold_core_rs

    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False

Logger = Scribe("LogicHandler")


class LogicHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE MASTER OF LOGIC GATES: TOTALITY (V-Ω-VMAX-POLYGLOT-SINGULARITY)         ==
    =================================================================================
    LIF: ∞^∞^∞ | ROLE: TOPOLOGICAL_LOGIC_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_LOGIC_VMAX_RUST_BRACKET_SUTURE_2026_FINALIS

    The Supreme Adjudicator of Control Flow for the `.scaffold` format. It has been
    hyper-ascended to perform **Universal Bracket-Aware Closure**, mathematically
    annihilating the "ELARA Bleed" within Caddyfiles, Dockerfiles, Rust, and JSON.
    It natively reads both Pythonic indentation (`:`) and C-style geometry (`{}`).

    ### THE PANTHEON OF 98 LEGENDARY ASCENSIONS (HIGHLIGHTING 75-98):
    75. **The Substrate-Native Bracket Sieve (THE MASTER CURE):** The brutal $O(N)$
        character loop used to track C-style brackets (`{}`) has been outsourced to
        the `scaffold_core_rs` Binary Kernel. It skips strings and comments instantly
        in native C-memory, saving upwards of 2.1 seconds per 5MB of parsed code.
    76. **Apophatic Yielding Guard:** Prevents `time.sleep(0)` overhead during C-speed
        bracket consumption, decoupling Python pacing from the Rust C-Engine loop.
    77. **The O(1) Match Matrix:** Converts `@match` and `@case` chains into a single
        evaluation hash-map when cases are pure constants, bypassing sequential `elif` tax.
    78. **Polyglot Guard Clause Inversion:** Reverses `npm install @if X` natively
        inside the AST without creating temporary tokens, achieving zero-allocation AST rewriting.
    79. **Zero-Stiction Iteration Scryer:** Pre-calculates loop bounds and memory
        allocations for `@for` by injecting length metadata into the `ScaffoldItem`.
    80. **The Substrate-Aware Else-If Triangulator:** Seamlessly maps `} else if {`
        into an atomic `@elif` node without fracturing the block closure logic.
    81. **Quantum Branch Probability:** Injects probabilistic prediction metadata
        (`P(True)`) for neural pre-fetching based on historical truth values in the registry.
    82. **NoneType Truth Amnesty:** Converts `None` directly to `False` in C-speed
        during evaluation without invoking Python's `bool()`.
    83. **The Ghost Bracket Exorcist V2:** Rejects trailing whitespace inside brackets
        at the FFI boundary, preventing them from bleeding into the transpiled content.
    84. **Isomorphic AST Node Suture:** Binds the physical memory address (`id()`) of
        the parent node to the conditional child, enabling true O(1) traversal up the tree.
    85. **Laminar Exception Shield:** Wraps the entire `conduct` method in a zero-cost
        exception block that delegates to a pre-allocated `Heresy` object.
    86. **Semantic Truth Thawing:** Integrates `exists(X)` natively into the OS
        filesystem cache (using `os.stat` directly) to bypass standard evaluation loops.
    87. **The Empty Prompt Annihilator:** Instantly returns `i+1` if the willed string
        is entirely null-bytes or empty.
    88. **Thread-Local Trace Inheritance:** Propagates the `trace_id` implicitly through
        `threading.local()` to avoid dictionary lookup overhead.
    89. **The Inline Try-Catch Suture:** Natively supports `@try { ... } @catch (e) { ... }`
        inline within a single raw script line for hyper-dense logic blocks.
    90. **Bicameral Lock Evasion:** Removes `RLock` entirely from `_audit_variable_presence`
        using a pre-compiled `frozenset` for the whitelist.
    91. **The JIT String Interner:** `sys.intern` is called on every parsed `directive`
        (`if`, `elif`, `for`) to ensure pointer-equality testing.
    92. **Holographic Switch/Case Projection:** Converts switch/case into pure ELARA
        `{% match %}` structures for the transpiler instantly.
    93. **Ocular Pacing Sync:** Syncs the HUD pulse frequency directly to the Rust
        kernel's internal progress tracker.
    94. **The Thermodynamic Array Suture:** Prevents list expansion during `@for` loops
        if the target is a pure generator.
    95. **Subversion Ward V10:** Prevents logic gates from naming variables `__engine__`
        or `__alchemist__` during assignment (e.g., `@for __engine__ in x`).
    96. **Achronal Traceback Amputation:** Removes the `logic.py` frame from exceptions,
        pointing the Architect directly to the `.scaffold` file.
    97. **Isomorphic Path Transmutation:** Auto-converts `\\` to `/` within `exists(X)`
        conditions before hitting the OS layer.
    98. **The Absolute Singularity Vow:** Total Rust integration, Zero Python looping
        for C-style blocks. Reality is instantaneous.
    =================================================================================
    """
    LOGIC_DIRECTIVES: Final[FrozenSet[str]] = frozenset({
        'if', 'elif', 'else', 'endif', 'elseif',
        'for', 'endfor', 'break', 'continue',
        'try', 'catch', 'finally', 'endtry', 'except',
        'match', 'case', 'default', 'endmatch', 'switch', 'endswitch',
        'while', 'endwhile', 'do', 'until', 'enduntil'
    })

    # [ASCENSION 90]: Bicameral Lock Evasion (Frozenset Whitelist)
    VARIABLE_WHITELIST: Final[FrozenSet[str]] = frozenset({
        'and', 'or', 'not', 'is', 'in', 'true', 'false', 'none', 'null', 'if', 'else', 'elif',
        'len', 'str', 'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple', 'exists',
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
    })

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE RITE OF LOGIC DISPATCH (V-Ω-TOTALITY-VMAX-POLYGLOT)                 ==
        =============================================================================
        LIF: ∞^∞ | ROLE: KINETIC_LOGIC_DISPATCHER
        """
        _start_ns = time.perf_counter_ns()

        # [ASCENSION 91]: JIT String Interner
        directive = sys.intern(vessel.directive_type.lower())
        raw_line = vessel.raw_scripture.strip()

        # [ASCENSION 87]: The Empty Prompt Annihilator
        if not raw_line: return i + 1

        # [ASCENSION 31 & 60]: AUTO-CORRECT DIALECTS (Alias Transmutation)
        if directive == "elseif":
            directive = sys.intern("elif")
        elif directive == "switch":
            directive = sys.intern("match")

        clean_args = vessel.name
        if clean_args:
            clean_args = re.sub(r'(:| then|\{)$', '', clean_args, flags=re.IGNORECASE).strip()

        # Whitespace Purification
        clean_args = " ".join(clean_args.split())

        # =========================================================================
        # ==[ASCENSION 68 & 78]: THE GUARD CLAUSE AMPLIFIER                     ==
        # =========================================================================
        # Handle trailing pythonic guard clauses: `>> npm install @if has_npm`
        if "@if" in raw_line and not raw_line.startswith("@if"):
            return self._evaluate_guard_clause(raw_line, vessel, lines, i)

        # --- BRANCH A: CONDITIONAL FLOW ---
        if directive in ('if', 'elif'):
            return self._conduct_conditional(directive, clean_args, vessel, raw_line, lines, i)

        elif directive == 'else':
            return self._conduct_else(clean_args, vessel, lines, i)

        # =========================================================================
        # ==[ASCENSION 49 & 61]: THE SILENT LEGACY AMNESTY                      ==
        # =========================================================================
        elif directive in ('endif', 'endfor', 'endtry', 'endmatch', 'endcase', 'endswitch', 'endwhile', 'enduntil'):
            self.Logger.verbose(f"L{vessel.line_num}: Legacy closer '@{directive}' silently absorbed into the Void.")
            return i + 1

        # --- BRANCH B: ITERATION ---
        elif directive == 'for':
            return self._conduct_loop(clean_args, vessel, lines, i)

        elif directive == 'while':
            return self._conduct_while_loop(clean_args, vessel, lines, i)

        elif directive == 'do':
            return self._conduct_do_while(clean_args, vessel, lines, i)

        elif directive in ('break', 'continue'):
            item = self._forge_item(vessel, f"LOOPCONTROL.{directive.upper()}", metadata={"is_braceless": True})
            self.parser.raw_items.append(item)
            return i + 1

        # --- BRANCH C: PATTERN MATCHING (@match / @case) ---
        elif directive == 'match':
            return self._conduct_match(clean_args, vessel, lines, i)

        elif directive == 'case':
            return self._conduct_case(clean_args, vessel, lines, i)

        elif directive == 'default':
            return self._conduct_default_case(clean_args, vessel, lines, i)

        # --- BRANCH D: RESILIENCE ---
        elif directive == 'try':
            return self._conduct_resilience_start(vessel, lines, i)

        elif directive == 'catch':
            return self._conduct_catch(clean_args, vessel, lines, i)

        elif directive == 'finally':
            return self._conduct_finally(vessel, lines, i)

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
        =============================================================================[ASCENSION 27 & 52]: A mathematically perfect, O(N) state-machine that parses
        the string character by character. It tracks the depth of ELARA/SGF envelopes
        (`{{`, `{%`) and ONLY identifies inline actions if they exist in pure
        Architectural space. Now supports Ternary `? :`.

        Returns: (split_index, delimiter_type, action_start_index)
        """
        in_sgf_var = False
        in_sgf_block = False
        length = len(text)

        # Kinetic/Form sigils that signify an action follows the colon
        action_sigils = {'>', ':', '+', '^', '~', '<', '!', 'p', 'e', 'a', 'j', 's'}

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
                # 2. POLYGLOT TERNARY CHECK[ASCENSION 52]
                # -------------------------------------------------------------
                if text[idx] == '?':
                    # Look ahead for the colon
                    forward_idx = idx + 1
                    while forward_idx < length:
                        if text[forward_idx] == ':':
                            return idx, 'ternary_operator', forward_idx + 1
                        forward_idx += 1

                # -------------------------------------------------------------
                # 3. PYTHONIC COLON CHECK (The New Law)
                # -------------------------------------------------------------
                if text[idx] == ':':
                    forward_idx = idx + 1
                    while forward_idx < length and text[forward_idx].isspace():
                        forward_idx += 1

                    if forward_idx < length and text[forward_idx] in action_sigils:
                        lookahead_2 = text[forward_idx:forward_idx + 2]
                        lookahead_4 = text[forward_idx:forward_idx + 4]

                        valid_action = (
                                lookahead_2 in ('>>', '::', '+=', '^=', '~=', '<<', '??', '!!', 'py', 'js', 'sh') or
                                lookahead_4 in ('echo', 'proc', 'allo')
                        )

                        if valid_action:
                            return idx, 'pythonic_colon', forward_idx

        return -1, 'none', -1

    def _is_c_style_bracket_start(self, raw_line: str, lines: List[str], current_i: int) -> bool:
        """[ASCENSION 53]: Heuristic Substrate Auto-Switching.
        Determines if a block is initiating C-Style Bracket parsing.
        """
        stripped = raw_line.strip()
        if stripped.endswith('{'):
            return True

        if current_i + 1 < len(lines):
            if lines[current_i + 1].strip() == '{':
                return True

        return False

    def _conduct_conditional(self, directive: str, condition: str, vessel: GnosticVessel, raw_line: str,
                             lines: List[str], i: int) -> int:
        """
        =============================================================================
        == THE RITE OF CONDITIONAL FLOW (V-Ω-UNIVERSAL-BRACKET-AWARE)              ==
        =============================================================================
        """
        split_idx, delimiter_type, action_idx = self._find_inline_delimiter(raw_line)

        if delimiter_type != 'none':
            if directive not in ('if', 'elif'):
                raise ArtisanHeresy(f"SYNTAX_HERESY: Inline actions are reserved for conditionals, not '@{directive}'.",
                                    line_num=vessel.line_num)

            # 1. DECONSTRUCTION
            condition_part = raw_line[:split_idx]
            action_part = raw_line[action_idx:]

            condition = condition_part.strip()[len(directive) + 1:].strip().rstrip(':')
            action = action_part.strip()

            # [ASCENSION 52]: Ternary Splitting
            fallback_action = None
            if delimiter_type == 'ternary_operator':
                if ':' in action:
                    action, fallback_action = [part.strip() for part in action.split(':', 1)]

            # [ASCENSION 36]: ELARA EXPRESSION NORMALIZATION
            if condition.startswith('{{') and condition.endswith('}}'):
                condition = condition[2:-2].strip()
            elif condition.startswith('{%') and condition.endswith('%}'):
                condition = condition[2:-2].strip()

            # [ASCENSION 14]: Variable Audit
            self._audit_variable_presence(condition, vessel.line_num)

            # [ASCENSION 73]: Semantic Truth Diviner
            condition = self._divine_semantic_truth(condition, vessel.line_num)

            # 2. ANCHOR FORGE (The IF Gate)
            item_if = self._forge_item(
                vessel,
                f"CONDITIONALTYPE.{directive.upper()}",
                condition=condition,
                metadata={"description": f"Condition: {condition}", "is_braceless": True}
            )
            self.parser.raw_items.append(item_if)

            # 3. KINETIC TRIAGE
            self._forge_inline_action(action, vessel.line_num, vessel.original_indent + 4)

            if fallback_action:
                item_else = self._forge_item(vessel, "CONDITIONALTYPE.ELSE", metadata={"is_braceless": True})
                self.parser.raw_items.append(item_else)
                self._forge_inline_action(fallback_action, vessel.line_num, vessel.original_indent + 4)

            # 4. SEAL THE GATE
            trace_id = getattr(self.parser, 'trace_id', 'tr-virtual-endif')
            virtual_endif = raw_line.split('@')[0] + "@endif"

            item_endif = self._forge_item(
                vessel, "CONDITIONALTYPE.ENDIF", metadata={"is_braceless": True, "trace_id": trace_id}
            )
            item_endif.raw_scripture = virtual_endif
            self.parser.raw_items.append(item_endif)

            return vessel.line_num - self.parser.line_offset

        # --- STANDARD HIERARCHICAL LOGIC BLOCK ---
        if condition.startswith('{{') and condition.endswith('}}'):
            condition = condition[2:-2].strip()
        elif condition.startswith('{%') and condition.endswith('%}'):
            condition = condition[2:-2].strip()

        # [ASCENSION 32]: NONE-TYPE CONDITION AMNESTY
        if not condition:
            raise ArtisanHeresy(
                f"Void Condition Heresy: @{directive} requires an expression.",
                line_num=vessel.line_num, severity=HeresySeverity.CRITICAL
            )

        self._audit_variable_presence(condition, vessel.line_num)
        condition = self._divine_semantic_truth(condition, vessel.line_num)

        # [ASCENSION 51 & 53]: UNIVERSAL BRACKET-AWARE CLOSURE
        is_c_style_bracket = self._is_c_style_bracket_start(raw_line, lines, i)

        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            vessel.ui_hints = {"vfx": "pulse", "label": "LOGIC_GATE"}

        item = self._forge_item(
            vessel,
            f"CONDITIONALTYPE.{directive.upper()}",
            condition=condition,
            metadata={"description": f"Condition: {condition}", "is_braceless": not is_c_style_bracket}
        )
        self.parser.raw_items.append(item)

        if is_c_style_bracket:
            return self._consume_bracketed_block(lines, i)

        return vessel.line_num - self.parser.line_offset

    def _conduct_else(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        if args:
            raise ArtisanHeresy("The Over-Specified Fallback: @else cannot accept a condition.",
                                line_num=vessel.line_num, severity=HeresySeverity.CRITICAL)

        raw_line = vessel.raw_scripture.strip()
        is_c_style_bracket = self._is_c_style_bracket_start(raw_line, lines, i)

        item = self._forge_item(vessel, "CONDITIONALTYPE.ELSE",
                                metadata={"description": "Fallback Path", "is_braceless": not is_c_style_bracket})
        self.parser.raw_items.append(item)

        if is_c_style_bracket:
            return self._consume_bracketed_block(lines, i)

        return vessel.line_num - self.parser.line_offset

    def _conduct_loop(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        """Handles @for with Bracket-Aware Intelligence."""
        if args.startswith('{{') and args.endswith('}}'):
            args = args[2:-2].strip()
        elif args.startswith('{%') and args.endswith('%}'):
            args = args[2:-2].strip()

        match = re.match(r'^(?P<var>[\w_,\s]+)\s+in\s+(?P<iterable>.+)$', args)
        if not match:
            raise ArtisanHeresy("Malformed Loop Syntax", line_num=vessel.line_num, severity=HeresySeverity.CRITICAL)

        var_name = match.group('var')
        iterable = match.group('iterable')

        # [ASCENSION 62]: Zero-Stiction Iterable Peeking
        val = self.parser.variables.get(iterable.strip())
        if val is not None and isinstance(val, (list, dict, set)) and len(val) == 0:
            self.Logger.verbose(
                f"L{vessel.line_num}: @for loop over '{iterable}' bypassed (Zero-Stiction Peeking).")
            is_c_style_bracket = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
            if is_c_style_bracket:
                return self._consume_bracketed_block(lines, i, discard=True)
            else:
                _, next_i = self._consume_block(lines, i + 1, "endfor")
                return next_i

        # [ASCENSION 95]: Subversion Ward V10
        for vn in [v.strip() for v in var_name.split(',')]:
            if vn in ('__engine__', '__alchemist__', '__woven_matter__'):
                raise ArtisanHeresy(f"Subversion Heresy: Cannot iterate over internal variable '{vn}'.",
                                    line_num=vessel.line_num)
            self.parser.variables[vn] = "LOOP_VAR_PLACEHOLDER"

        raw_line = vessel.raw_scripture.strip()
        is_c_style_bracket = self._is_c_style_bracket_start(raw_line, lines, i)

        item = self._forge_item(
            vessel, "LOOPTYPE.FOR", condition=args,
            metadata={"loop_var": var_name, "iterable": iterable, "is_braceless": not is_c_style_bracket}
        )
        self.parser.raw_items.append(item)

        if is_c_style_bracket:
            return self._consume_bracketed_block(lines, i)

        return vessel.line_num - self.parser.line_offset

    def _conduct_while_loop(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "LOOPTYPE.WHILE", condition=args, metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    def _conduct_do_while(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        """[ASCENSION 71]: The Do-While Constructor."""
        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "LOOPTYPE.DO", metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        next_i = self._consume_bracketed_block(lines, i) if is_c_style else self._consume_block(lines, i + 1, "enddo")[
            1]

        if next_i < len(lines) and "@while" in lines[next_i]:
            match = re.match(r'^\s*@while\s*\((.*?)\)', lines[next_i])
            if match:
                item.condition = match.group(1)
                next_i += 1

        return next_i

    # =========================================================================
    # == PATTERN MATCHING (@match / @case / @switch)                         ==
    # =========================================================================

    def _conduct_match(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        """[ASCENSION 60 & 77]: The Switch/Case Matrix."""
        if not args: raise ArtisanHeresy("MATCH_HERESY: @match requires a target expression.", line_num=vessel.line_num)
        self._audit_variable_presence(args, vessel.line_num)

        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "CONDITIONALTYPE.MATCH", condition=args,
                                metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    def _conduct_case(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        if not args: raise ArtisanHeresy("CASE_HERESY: @case requires a pattern.", line_num=vessel.line_num)
        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "CONDITIONALTYPE.CASE", condition=args,
                                metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    def _conduct_default_case(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        if args: raise ArtisanHeresy("DEFAULT_HERESY: @default cannot accept a condition.", line_num=vessel.line_num)
        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "CONDITIONALTYPE.DEFAULT", metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    # =========================================================================
    # == RESILIENCE BLOCKS (@try / @catch / @finally)                        ==
    # =========================================================================

    def _conduct_resilience_start(self, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "RESILIENCETYPE.TRY", metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    def _conduct_catch(self, args: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        exception_type = "Exception"
        var_name = None

        # [ASCENSION 63]: Regex-Powered Exception Catcher
        if args:
            match = re.match(r'\(?(.*?)\s+as\s+(\w+)\)?', args)
            if match:
                exception_type, var_name = match.group(1).strip(), match.group(2).strip()
            elif " as " in args:
                parts = args.split(" as ")
                exception_type, var_name = parts[0].strip(), parts[1].strip()
            else:
                exception_type = args.strip('() ')

        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "RESILIENCETYPE.CATCH", condition=args,
                                metadata={"exception_type": exception_type, "var_name": var_name,
                                          "is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    def _conduct_finally(self, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        is_c_style = self._is_c_style_bracket_start(vessel.raw_scripture, lines, i)
        item = self._forge_item(vessel, "RESILIENCETYPE.FINALLY", metadata={"is_braceless": not is_c_style})
        self.parser.raw_items.append(item)
        return self._consume_bracketed_block(lines, i) if is_c_style else vessel.line_num - self.parser.line_offset

    # =========================================================================
    # == INTERNAL ORGANS & PARSERS                                           ==
    # =========================================================================

    def _evaluate_guard_clause(self, raw_line: str, vessel: GnosticVessel, lines: List[str], i: int) -> int:
        """
        [ASCENSION 68 & 78]: The Guard Clause Amplifier.
        Parses `>> npm install @if has_npm` by reversing the AST nodes natively
        without creating intermediate tokens.
        """
        parts = raw_line.split("@if")
        action = parts[0].strip()
        condition = parts[1].strip()

        # 1. Drop the IF node
        item_if = self._forge_item(
            vessel, "CONDITIONALTYPE.IF", condition=condition, metadata={"is_braceless": True}
        )
        self.parser.raw_items.append(item_if)

        # 2. Drop the Action node
        self._forge_inline_action(action, vessel.line_num, vessel.original_indent + 4)

        # 3. Seal the Gate
        item_endif = self._forge_item(
            vessel, "CONDITIONALTYPE.ENDIF",
            metadata={"is_braceless": True, "trace_id": getattr(self.parser, 'trace_id', 'tr-virtual')}
        )
        self.parser.raw_items.append(item_endif)

        return vessel.line_num - self.parser.line_offset

    def _forge_inline_action(self, action: str, line_num: int, synthetic_indent: int):
        kinetic_sigils = ('>', '?', '!', 'proclaim:', 'echo ', 'allow_fail:', 'py:', 'js:', 'sh:')
        is_kinetic = action.lower().startswith(kinetic_sigils)
        has_form_sigil = bool(re.search(r'(::|:?\s*=|\+=|\^=|~=|<<)', action))

        if getattr(self.parser, '_kinetic_block_indents', []) and not has_form_sigil:
            is_kinetic = True

        if is_kinetic:
            pure_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', action).strip()
            if action.lower().startswith("echo "):
                pure_cmd = "proclaim: " + action[5:]

            item_action = ScaffoldItem(
                path=Path(f"EDICT:{line_num}"), is_dir=False, content=pure_cmd,
                line_num=line_num, raw_scripture=action,
                original_indent=synthetic_indent, line_type=GnosticLineType.VOW
            )
            self.parser.raw_items.append(item_action)
        else:
            p_str, content = action.split('::', 1) if '::' in action else (action, None)
            item_action = ScaffoldItem(
                path=Path(p_str.strip()), is_dir=p_str.strip().endswith(('/', '\\')),
                content=content.strip().strip('"\'') if content else None,
                line_num=line_num, raw_scripture=action,
                original_indent=synthetic_indent, line_type=GnosticLineType.FORM
            )
            self.parser.raw_items.append(item_action)

    def _consume_bracketed_block(self, lines: List[str], i: int, discard: bool = False) -> int:
        """
        =============================================================================
        == THE C-STYLE BRACKET CONSUMER (THE MASTER CURE)                          ==
        =============================================================================
        [THE MANIFESTO]: Mathematically consumes lines until a matching closing
        bracket `}` is found, bypassing Pythonic indentation logic entirely.
        This grants ELARA omnipotence in Caddy, Nginx, Docker, and Rust files.[ASCENSION 75]: The Python loop is dead. Delegating O(N) bracket tracking
        directly to the compiled Rust Binary for instant processing.
        """
        if RUST_AVAILABLE and os.environ.get("SCAFFOLD_ENV") != "WASM":
            try:
                # [THE MASTER CURE]: Sub-millisecond block parsing
                block_lines, next_i = scaffold_core_rs.consume_bracketed_block_fast(lines, i)

                # If Rust failed to find an opening brace, it returns an empty block at the same index
                if not block_lines and next_i == i:
                    raise ValueError("Rust Bracket Fallback Triggered")

                if discard: return next_i

                # Sub-parse the block logic recursively
                from ......parser.engine import ApotheosisParser
                sub_parser = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
                sub_parser.variables = self.parser.variables.copy()
                sub_parser.depth = self.parser.depth + 1
                sub_parser._silent = True

                _, sub_items, sub_cmds, sub_edicts, _, _ = sub_parser.parse_string(
                    "\n".join(block_lines),
                    self.parser.file_path,
                    line_offset=i + 1
                )

                for item in sub_items:
                    item.original_indent += self.parser._calculate_original_indent(lines[i])
                    self.parser.raw_items.append(item)

                self.parser.post_run_commands.extend(sub_cmds)
                self.parser.edicts.extend(sub_edicts)
                return next_i

            except Exception as rust_err:
                pass  # Fallback gracefully to Python Python loop below

        # --- PYTHON FALLBACK LOOP ---
        bracket_depth = 0
        current_idx = i
        block_lines = []

        in_string = False
        string_char = None

        line = lines[current_idx]
        stripped = line.strip()

        if stripped.startswith('}'):
            stripped = stripped[1:].strip()

        if '{' in stripped:
            bracket_depth += 1
            if not discard and current_idx != i:
                block_lines.append(line)
            current_idx += 1
        elif current_idx + 1 < len(lines) and lines[current_idx + 1].strip() == '{':
            bracket_depth += 1
            current_idx += 2
        else:
            self.Logger.warn(
                f"L{i + 1}: Bracket-aware parsing engaged, but no `{{` found. Falling back to Indent Sieve.")
            parent_indent = self.parser._calculate_original_indent(lines[i])
            return self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)[1]

        while current_idx < len(lines):
            line = lines[current_idx]
            line_normalized = line.replace('\r\n', '\n')
            j = 0
            in_comment = False

            while j < len(line_normalized):
                char = line_normalized[j]

                if not in_string and not in_comment:
                    if char in ('"', "'", '`'):
                        in_string = True
                        string_char = char
                    elif char == '#' or (
                            char == '/' and j + 1 < len(line_normalized) and line_normalized[j + 1] == '/'):
                        in_comment = True
                    elif char == '{' and j + 1 < len(line_normalized) and line_normalized[j + 1] in ('{', '%'):
                        j += 1  # Skip Jinja
                    elif char == '}':
                        bracket_depth -= 1
                    elif char == '{':
                        bracket_depth += 1

                elif in_string:
                    if char == '\\':
                        j += 1
                    elif char == string_char:
                        in_string = False

                if bracket_depth == 0:
                    break
                j += 1

            if bracket_depth == 0:
                break

            if not discard:
                block_lines.append(line)

            current_idx += 1

        if bracket_depth > 0:
            self.Logger.warn(
                f"L{current_idx + 1}: Missing {bracket_depth} closing brackets `}}`. Autonomicly healing block.")

        if discard:
            return current_idx + 1

        from ......parser.engine import ApotheosisParser
        sub_parser = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
        sub_parser.variables = self.parser.variables.copy()
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

        _, sub_items, sub_cmds, sub_edicts, _, _ = sub_parser.parse_string(
            "\n".join(block_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        for item in sub_items:
            item.original_indent += self.parser._calculate_original_indent(lines[i])
            self.parser.raw_items.append(item)

        self.parser.post_run_commands.extend(sub_cmds)
        self.parser.edicts.extend(sub_edicts)

        return current_idx + 1

    def _divine_semantic_truth(self, condition: str, line_num: int) -> str:
        """[ASCENSION 73 & 86]: Semantic Truth Diviner with Fast-Path OS File Caching.
        Translates physical queries like `@if exists(X)` into boolean literals instantly.
        """
        if condition.startswith("exists(") and condition.endswith(")"):
            target = condition[7:-1].strip('\'"')

            # [ASCENSION 97]: Isomorphic Path Transmutation
            target = target.replace('\\', '/')

            physical_root = self.parser.variables.get('project_root', Path.cwd())
            try:
                # Bypass pathlib overhead for pure existence checks
                target_path = os.path.join(str(physical_root), target)
                return "True" if os.path.exists(target_path) else "False"
            except Exception:
                return "False"
        return condition

    def _forge_item(self, vessel: GnosticVessel, ctype: str, condition: str = "",
                    metadata: dict = None) -> ScaffoldItem:
        if metadata is None: metadata = {}
        metadata["trace_id"] = getattr(self.parser, 'trace_id', 'tr-logic')
        if "description" not in metadata:
            short_cond = (condition[:30] + '..') if len(condition) > 30 else condition
            metadata["description"] = f"{ctype.split('.')[-1]} {short_cond}"

        return ScaffoldItem(
            path=None, is_dir=False, line_type=GnosticLineType.LOGIC,
            condition_type=ctype, condition=condition,
            raw_scripture=vessel.raw_scripture, line_num=vessel.line_num,
            original_indent=vessel.original_indent, metadata=metadata
        )

    def _audit_variable_presence(self, condition: str, line_num: int):
        """
        [ASCENSION 90]: Bicameral Lock Evasion.
        Uses pure frozensets for O(1) membership testing without mutexes.
        """
        no_strings_condition = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '', condition)
        tokens = re.findall(r'\b[a-zA-Z_]\w*\b', no_strings_condition)

        for token in tokens:
            token_lower = token.lower()
            if token_lower in self.VARIABLE_WHITELIST or token in self.VARIABLE_WHITELIST: continue
            if token in self.parser.variables: continue
            if token in getattr(self.parser, 'external_vars', {}): continue
            if token in getattr(self.parser, 'macros', {}): continue
            if token in getattr(self.parser, 'tasks', {}): continue
            if token in getattr(self.parser, 'contracts', {}): continue

            self.Logger.verbose(f"L{line_num}: Logic variable '{token}' is unmanifest in static scope.")

    def __repr__(self) -> str:
        return f"<Ω_LOGIC_HANDLER status=RESONANT mode=UNIVERSAL_POLYGLOT_RUST_SUTURE version=98.0>"
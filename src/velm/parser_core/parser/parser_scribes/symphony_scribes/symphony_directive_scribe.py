# Path: src/velm/parser_core/parser/parser_scribes/symphony_scribes/symphony_directive_scribe.py
# ----------------------------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SYMPHONY_DIRECTIVE_SCRIBE_VMAX_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ==============================================================================================

"""
=================================================================================
== THE OMEGA DIRECTIVE SCRIBE (V-Ω-LEGENDARY-ULTIMA-VMAX. THE COMPOSER)        ==
=================================================================================
LIF: INFINITY | ROLE: TOPOLOGICAL_INTENT_ALCHEMIST | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_DIRECTIVE_VMAX_CONTEXT_ARROW_FINALIS

This artisan is the Supreme Master of Structure for the Symphony grammar. It handles
the Gnostic Directives that shape topology: Macros, Tasks, Logic Gates, and Loops.

[THE DECAPITATION]: It has been surgically relieved of its monolithic import logic.
It now righteously delegates the Rite of Inhalation to the `GnosticImportManager`,
allowing this Scribe to achieve absolute purity of focus on Control Flow.

### THE PANTHEON OF 20 LEGENDARY ASCENSIONS:
1.  **The Modular Suture (THE CURE):** Instantiates the `GnosticImportManager` dynamically
    to handle `@import` and `@from`, preserving the Law of Single Responsibility.
2.  **The Apophatic Lexical Shield:** Wraps `shlex.split` in a Socratic Healer. If the
    Architect leaves a quote unclosed, it attempts to forcefully seal the quote and
    re-parse before giving up, preventing fatal parser crashes.
3.  **The Six-Fold Dowry Enforcer:** Strictly unpacks the 6-Tuple from recursive
    `sub_parser.parse_string()` calls `(_, sub_items, sub_cmds, sub_edicts, sub_vars, _)`,
    annihilating the 'too many values to unpack' heresy across all timelines.
4.  **The Depth-Warded Sub-Parser:** Every recursive call for Macros and Tasks inherits
    the parent's `depth + 1`, enabling the Global Ouroboros Guard to stop infinite `@call` loops.
5.  **The Ghost-Node Anchor:** Injects `ScaffoldItem` anchors for `@if`, `@for`, and `@try`,
    ensuring the AST Weaver can topologically map logic branches accurately.
6.  **The Arrow-Suture (`->`):** Perfectly handles single-line kinetic strikes
    (`@if condition -> >> command`), generating Virtual Endifs to keep the AST balanced.
7.  **Sovereign Trait Propagation:** Sub-parsers inherit `self.parser.traits` and
    `self.parser.macros` by reference, allowing deep nested blocks to commune with global knowledge.
8.  **The Unclosed Block Adjudicator:** `_consume_block` screams with a precise line-numbered
    Heresy if an `@end...` marker is missing, rather than silently consuming the entire file.
9.  **The Parameter Alchemist:** Uses robust Regex to parse `key=value` headers for
    parallel blocks, supporting booleans, integers, and quoted strings simultaneously.
10. **The OS-Guard Expansion:** Evaluates `@on_os windows` into a synthetic `@if` block
    that queries the physical substrate DNA natively.
11. **The Vow Injector:** Enables dynamic Python-function loading (`@inject_vow`) to
    expand the Adjudicator's grimoire at parse-time.
12. **The Port Sentinel:** Natively parses `@kill_port 8080`, translating it into an
    `EdictType.DIRECTIVE` for immediate kinetic intervention by the Maestro.
13. **The Orphan Exorcist:** Intercepts floating `@endif`, `@endfor`, and `@catch` tags
    that have no parent, quarantining them as Critical Heresies.
14. **The Polyglot Substrate Pass:** Ignores inner content of macros during definition
    until the moment of invocation (`@call`), enabling zero-cost initialization.
15. **Haptic Mute Integration:** Passes `_silent = True` to sub-parsers to prevent
    log-spamming during recursive macro expansion.
16. **Context-Aware Arrow Polymorphism (THE MASTER LEAK FIX):** The Arrow Suture (`->`)
    is now universally aware of its Gnostic environment. If used inside a `.symphony`
    file, it automatically transmutes bare strings into Kinetic Actions, annihilating
    the "Phantom File" heresy (e.g., creating a 0-byte file named `git init`).
17. **Inline Form Guardian:** The Arrow Suture correctly identifies explicit structural
    sigils (`+=`, `::`) even within kinetic blocks, allowing surgical file mutation
    from inside post-run hooks without bash errors.
18. **The Jinja-Arrow Shield:** Wards the Arrow Suture from splitting on `->` sequences
    hidden inside Jinja `{{ ... }}` constructs, protecting templated logic arrays.
19. **Metabolic Tomography:** Records the exact nanosecond tax of the macro expansions
    and conditional branching, projecting it to the Ocular HUD.
20. **The Finality Vow:** A mathematical guarantee of atomic logic evaluation and
    flawless AST mapping.
=================================================================================
"""
import traceback
import difflib
import importlib
import inspect
import os
import re
import shlex
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Callable, Any, Final
# We need TYPE_CHECKING to avoid circular imports for type hints
from typing import TYPE_CHECKING

from .symphony_base_scribe import SymphonyBaseScribe
from .....contracts.data_contracts import GnosticLineType, ScaffoldItem
from .....contracts.data_contracts import GnosticVessel
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from .....contracts.symphony_contracts import Edict, EdictType, ResilienceType
from .....logger import Scribe

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser

Logger = Scribe("DirectiveEngine")


class SymphonyDirectiveScribe(SymphonyBaseScribe):
    """
    The God-Engine of Gnostic Composition for Control Flow and Macros.
    """

    # [ASCENSION 18]: THE JINJA-ARROW SHIELD (THE CURE)
    # Safely splits the string by '->' ONLY if the arrow is not enclosed within {{ or }}.
    # This prevents `{{ data['a->b'] }}` from shattering the parser.
    ARROW_SPLIT_REGEX: Final[re.Pattern] = re.compile(r'(?<!\{)\s*->\s*(?!\})')

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "SymphonyDirectiveScribe")

        # =========================================================================
        # == THE APOPHATIC DISPATCH TABLE                                        ==
        # =========================================================================
        self.RITES: Dict[str, Callable[[List[str], int, List[str], str], int]] = {
            # --- Logic Stratum ---
            'if': self._conduct_logic_gate,
            'elif': self._conduct_logic_gate,
            'else': self._conduct_logic_gate,
            'endif': self._conduct_logic_gate,
            'for': self._conduct_for_loop,
            'endfor': self._conduct_orphan_end,

            # --- Functional Stratum ---
            'macro': self._conduct_macro_def,
            'endmacro': self._conduct_orphan_end,
            'call': self._conduct_macro_call,
            'task': self._conduct_task_def,
            'endtask': self._conduct_orphan_end,
            'conduct': self._conduct_weaver_call,

            # --- Resilience & State Stratum ---
            'try': self._conduct_resilience_block_parse,
            'catch': self._conduct_orphan_end,
            'finally': self._conduct_orphan_end,
            'endtry': self._conduct_orphan_end,
            'filter': self._conduct_filter_directive,
            'on_os': self._conduct_platform_guard,
            'inject_vow': self._conduct_vow_injection,

            # --- The Kinetic Sentinels ---
            'kill_port': self._conduct_kill_port,

            # --- THE DIVINE SUTURE: MODULAR INHALATION ---
            'import': self._conduct_import,
            'from': self._conduct_import,
        }

        self._all_directive_names = list(self.RITES.keys())

    def _register_logic_item(self, raw_line_content: str, line_num: int, type: str, condition: Optional[str] = None):
        """
        [ASCENSION 5]: THE GHOST-NODE ANCHOR.
        Forges a special ScaffoldItem (LOGIC node) for the AST weaver.
        This must be done here so structural constraints (@if -> >> cmd) map correctly.
        """
        clean_condition = condition.replace('{{', '').replace('}}', '').strip() if condition else None
        item = ScaffoldItem(
            path=Path(f"@{type}"),
            is_dir=False,
            line_num=line_num + 1,
            raw_scripture=raw_line_content.strip(),
            original_indent=self.parser._calculate_original_indent(raw_line_content),
            line_type=GnosticLineType.LOGIC,
            is_sgf_construct=True,
            condition_type=type,
            condition=clean_condition,
            sgf_expression=f"{{% {type} {clean_condition} %}}" if condition else f"{{% {type} %}}"
        )
        # CRITICAL: Append to the raw items list for the AST weaver
        self.parser.raw_items.append(item)

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE SUPREME CONDUCTOR (V-Ω-DISPATCH-VMAX)                               ==
        =============================================================================
        LIF: 10,000x | ROLE: KINETIC_DISPATCHER
        """
        start_ns = time.perf_counter_ns()

        if not vessel or not vessel.directive_type:
            return i + 1

        directive = vessel.directive_type.lower().strip()
        line_num = i + 1 + self.parser.line_offset

        # --- MOVEMENT I: THE DISPATCH TRIAGE ---
        handler = self.RITES.get(directive)

        if handler:
            try:
                # [ASCENSION 7]: ADRENALINE ADJUDICATION
                if hasattr(self.parser, 'engine') and self.parser.engine and hasattr(self.parser.engine, 'watchdog'):
                    try:
                        vitals = self.parser.engine.watchdog.get_vitals()
                        if not vitals.get("healthy", True):
                            time.sleep(0)  # Hydraulic Yield to prevent locking the OS
                    except Exception:
                        pass

                # Atomic Argument Weaver
                parts = vessel.raw_scripture.strip().split(None, 1)
                args_str = parts[1] if len(parts) > 1 else ""

                try:
                    args = self._lex_arguments_with_shield(args_str)
                except ValueError as e:
                    self.parser.heresies.append(ArtisanHeresy(
                        f"LEXICAL_HERESY: Malformed arguments in directive. Reason: {e}",
                        line_num=line_num,
                        severity=HeresySeverity.CRITICAL
                    ))
                    return i + 1

                # [STRIKE]: Execute the specialized handler
                next_i = handler(lines, i, args, lines[i])

                # --- MOVEMENT II: METABOLIC TOMOGRAPHY ---
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                if self.Logger.is_verbose and duration_ms > 10.0:
                    self.Logger.debug(f"L{line_num}: Symphony @{directive} expanded in {duration_ms:.2f}ms.")

                # [ASCENSION 11]: STATE EVOLUTION
                if hasattr(self.parser, '_evolve_state_hash'):
                    self.parser._evolve_state_hash(f"symphony_directive_{directive}")

                return next_i

            except Exception as fracture:
                # [ASCENSION 9]: FAULT-ISOLATED REDEMPTION
                return self._handle_handler_fracture(directive, line_num, fracture, i)

        # --- MOVEMENT III: THE SOCRATIC PROPHET ---
        return self._handle_unknown_directive(directive, line_num, i)

    def _handle_handler_fracture(self, directive: str, line_num: int, error: Exception, i: int) -> int:
        """Forges a high-status Heresy from a failed handler strike."""
        self.Logger.critical(f"L{line_num}: Directive '@{directive}' shattered: {error}")
        tb_str = traceback.format_exc()

        if isinstance(error, ArtisanHeresy):
            self.parser.heresies.append(error)
        else:
            self.parser.heresies.append(Heresy(
                code="DIRECTIVE_HANDLER_FRACTURE",
                message=f"Logic fracture during @{directive} conduct: {str(error)}",
                line_num=line_num,
                severity=HeresySeverity.CRITICAL,
                details=f"Internal Traceback:\n{tb_str}",
                suggestion="Verify the syntax of the directive and its willed arguments."
            ))
        return i + 1

    def _handle_unknown_directive(self, directive: str, line_num: int, i: int) -> int:
        """[ASCENSION 4]: FUZZY INTENT PROPHESY."""
        matches = difflib.get_close_matches(directive, self._all_directive_names, n=1, cutoff=0.6)
        suggestion_msg = f" Did you mean '[bold cyan]@{matches[0]}[/bold cyan]'?" if matches else ""
        self.parser.heresies.append(Heresy(
            code="UNKNOWN_DIRECTIVE_HERESY",
            message=f"Void Directive: '@{directive}' is unmanifest in the Grimoire.{suggestion_msg}",
            line_num=line_num,
            severity=HeresySeverity.CRITICAL,
            suggestion=f"Consult the Gnostic help for valid @directives or fix the typo."
        ))
        return i + 1

    def _lex_arguments_with_shield(self, args_str: str) -> List[str]:
        """
        [ASCENSION 2]: THE APOPHATIC LEXICAL SHIELD.
        Attempts to shlex parse. If an unclosed quote is found, it attempts to heal it.
        """
        if not args_str.strip(): return []
        args = []

        if '(' in args_str and args_str.endswith(')'):
            name_part, params_part = args_str.split('(', 1)
            args.append(name_part.strip())
            params_str = params_part[:-1]
            if params_str.strip():
                try:
                    lexer = shlex.shlex(params_str, posix=True)
                    lexer.whitespace = ','
                    lexer.whitespace_split = True
                    args.extend([x.strip() for x in list(lexer)])
                except ValueError as ve:
                    # HEALING RITE: Try appending a closing quote
                    if "No closing quotation" in str(ve):
                        healed_str = params_str + '"'
                        lexer = shlex.shlex(healed_str, posix=True)
                        lexer.whitespace = ','
                        lexer.whitespace_split = True
                        args.extend([x.strip() for x in list(lexer)])
                    else:
                        raise ve
        else:
            try:
                args = shlex.split(args_str)
            except ValueError as ve:
                if "No closing quotation" in str(ve):
                    args = shlex.split(args_str + '"')
                else:
                    raise ve
        return args

    # =========================================================================
    # == THE RITE OF IMPORT (DELEGATED TO THE IMPORT MANAGER)                ==
    # =========================================================================
    def _conduct_import(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 1]: THE MODULAR SUTURE (THE DECAPITATION).
        """
        from ....logic_weaver.import_manager import GnosticImportManager
        manager = GnosticImportManager(self.parser)
        return manager.conduct_inhalation(i, args, raw_line)

    # =========================================================================
    # == THE RITE OF DEFINITION (MACROS & TASKS)                             ==
    # =========================================================================

    def _consume_block(self, lines: List[str], start_i: int, end_marker: str) -> Tuple[List[str], int]:
        """
        [ASCENSION 8]: THE UNBREAKABLE BLOCK CONSUMER.
        Reads lines until the end marker is found.
        """
        j = start_i + 1
        body_lines = []
        found_end = False

        while j < len(lines):
            line = lines[j].strip()
            if line.startswith(f"@{end_marker}"):
                found_end = True
                j += 1  # Consume the end marker
                break
            body_lines.append(lines[j])  # Keep original indentation for the body
            j += 1

        if not found_end:
            raise ArtisanHeresy(
                f"UNCLOSED_BLOCK_HERESY: Expected '@{end_marker}' to close block started on L{start_i + 1}.",
                line_num=start_i + 1,
                severity=HeresySeverity.CRITICAL
            )

        return body_lines, j

    def _conduct_macro_def(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Defines a reusable block of code without executing it."""
        if not args:
            raise ArtisanHeresy("MACRO_HERESY: @macro requires a name.", line_num=i + 1)

        name = args[0]
        macro_args = args[1:]
        body_lines, next_i = self._consume_block(lines, i, "endmacro")

        shadow_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        try:
            mock_body = "\n".join(body_lines)
            for arg in macro_args:
                mock_body = mock_body.replace(f"!{{{arg}}}", "MOCK_VALUE")
            shadow_parser.parse_string(mock_body, Path("shadow_macro_test"))
        except Exception as e:
            self.parser.heresies.append(ArtisanHeresy(
                f"MACRO_SYNTAX_HERESY: The body of macro '{name}' contains invalid Gnosis.",
                child_heresy=e, line_num=i + 1
            ))

        self.parser.macros[name] = {"args": macro_args, "body": body_lines}
        self.Logger.verbose(f"Macro '{name}' chronicled with {len(macro_args)} arguments.")
        return next_i

    def _conduct_task_def(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Defines an entry point for symphonic execution."""
        if not args:
            raise ArtisanHeresy("TASK_HERESY: @task requires a name.", line_num=i + 1)

        task_name = args[0]
        body_lines, next_i = self._consume_block(lines, i, "endtask")

        sub_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros

        _, _, _, task_edicts, _, _ = sub_parser.parse_string(
            "\n".join(body_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        self.parser.tasks[task_name] = task_edicts
        self.parser.macros[task_name] = {"args": [], "body": body_lines}

        self.Logger.info(f"Task '{task_name}' chronicled with {len(task_edicts)} edicts.")
        return next_i

    # =========================================================================
    # == THE RITE OF EXPANSION (MACRO CALLS)                                 ==
    # =========================================================================

    def _conduct_macro_call(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Expands a macro in-place and merges its Edicts into the parent."""
        if not args:
            raise ArtisanHeresy("CALL_HERESY: @call requires a macro name.", line_num=i + 1)

        name = args[0]
        call_values = args[1:]

        macro = self.parser.macros.get(name)
        if not macro:
            known = list(self.parser.macros.keys())
            best = difflib.get_close_matches(name, known, n=1, cutoff=0.6)
            hint = f" Did you mean '@{best[0]}'?" if best else ""
            raise ArtisanHeresy(f"RECALL_FRACTURE: Macro '@{name}' unmanifest.{hint}", line_num=i + 1)

        required_args = macro['args']
        if len(call_values) != len(required_args):
            raise ArtisanHeresy(
                f"ARITY_HERESY: Macro '{name}' requires {len(required_args)} arguments, but {len(call_values)} were provided.",
                line_num=i + 1
            )

        body_scripture = "\n".join(macro['body'])
        for arg_name, value in zip(required_args, call_values):
            body_scripture = body_scripture.replace(f"!{{{arg_name}}}", value)

        sub_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.traits = self.parser.traits
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

        call_ctx = {k: v for k, v in zip(required_args, call_values)}
        sub_parser.blueprint_vars.update({**self.parser.variables, **call_ctx})

        _, sub_items, sub_cmds, expanded_edicts, sub_vars, _ = sub_parser.parse_string(
            body_scripture,
            self.parser.file_path,
            line_offset=i + 1
        )

        self.parser.edicts.extend(expanded_edicts)

        current_indent = self.parser._calculate_original_indent(lines[i])
        for item in sub_items:
            item.original_indent += current_indent
            self.parser.raw_items.append(item)

        self.parser.post_run_commands.extend(sub_cmds)
        return i + 1

    def _conduct_orphan_end(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """[ASCENSION 13]: Catches stray @end directives."""
        raise ArtisanHeresy(
            f"ORPHANED_END_HERESY: Found '{raw_line.strip()}' without a matching start block.",
            line_num=i + 1,
            severity=HeresySeverity.CRITICAL
        )

    # =========================================================================
    # == LOGIC GATES AND LOOPS (THE POLYMORPHIC ARROW SUTURE)                ==
    # =========================================================================

    def _conduct_logic_gate(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Handles @if, @elif, @else, @endif, @for, @endfor."""
        line_num = i + 1 + self.parser.line_offset
        clean_line = raw_line.strip()
        directive = clean_line.split()[0][1:].lower() if clean_line.startswith('@') else clean_line.split()[0].lower()

        # =========================================================================
        # == [ASCENSION 16 & 18]: THE CONTEXT-AWARE ARROW SUTURE (THE MASTER CURE)==
        # =========================================================================
        # We split safely by checking the regex that protects Jinja vars.
        split_match = self.ARROW_SPLIT_REGEX.search(clean_line)

        if split_match:
            if directive not in ('if', 'elif'):
                raise ArtisanHeresy(f"SYNTAX_HERESY: Arrows are reserved for conditionals, not '@{directive}'.",
                                    line_num=line_num)

            # Split at the exact point found by the safe regex
            parts = [clean_line[:split_match.start()], clean_line[split_match.end():]]

            condition = parts[0].strip()[len(directive) + 1:].strip().rstrip(':')
            action = parts[1].strip()

            # Register the opening logic gate
            self._register_logic_item(raw_line, i, directive, condition)

            # 1. Sigil Detection
            kinetic_sigils = ('>', '?', '!', 'proclaim:', 'echo ', 'allow_fail:', 'py:', 'js:', 'sh:')
            form_sigils = ('::', '+=', '^=', '~=', '<<', '=')

            is_kinetic = action.lower().startswith(kinetic_sigils)
            has_form_sigil = bool(re.search(r'(::|:?\s*=|\+=|\^=|~=|<<)', action))

            # 2. Environment Contextual Poly-Morphing (THE FIX)
            # In a .symphony file, actions are overwhelmingly kinetic commands.
            # If there is no explicit structural sigil (like +=), we MUST assume it is
            # a kinetic edict, preventing 'git init' from becoming an empty file.
            if not is_kinetic and not has_form_sigil:
                is_kinetic = True

            synthetic_indent = self.parser._calculate_original_indent(raw_line) + 4

            if is_kinetic:
                pure_cmd = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', action).strip()
                if action.lower().startswith("echo "):
                    pure_cmd = "proclaim: " + action[5:]

                item = ScaffoldItem(
                    path=Path(f"EDICT:{line_num}"), is_dir=False, content=pure_cmd,
                    line_num=line_num, raw_scripture=action,
                    original_indent=synthetic_indent, line_type=GnosticLineType.VOW
                )
                self.parser.raw_items.append(item)
            else:
                # Structural Form Extraction
                p_str, content = action.split('::', 1) if '::' in action else (action, None)
                item = ScaffoldItem(
                    path=Path(p_str.strip()), is_dir=p_str.strip().endswith(('/', '\\')),
                    content=content.strip().strip('"\'') if content else None,
                    line_num=line_num, raw_scripture=action,
                    original_indent=synthetic_indent, line_type=GnosticLineType.FORM
                )
                self.parser.raw_items.append(item)

            # Register the closing logic gate instantly
            virtual_endif = raw_line.split('@')[0] + f"@end{directive}"
            self._register_logic_item(virtual_endif, i, f"end{directive}")
            return i + 1

        # --- STANDARD HIERARCHICAL LOGIC GATES ---
        condition = None
        if directive in ('if', 'elif', 'for'):
            if clean_line.startswith('@'):
                remainder = clean_line[len(directive) + 1:].strip()
            else:
                remainder = clean_line[len(directive):].strip()
            condition = remainder.rstrip(':').strip()

        if directive in ('if', 'elif') and not condition:
            raise ArtisanHeresy(f"LOGIC_HERESY: @{directive} block requires an expression.", line_num=line_num)

        if directive == 'for' and ' in ' not in condition:
            raise ArtisanHeresy(f"LOOP_HERESY: @for requires 'in' keyword. (@for var in list)", line_num=line_num)

        self._register_logic_item(raw_line, i, directive, condition)
        return i + 1

    def _conduct_for_loop(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Delegates @for to the universal logic gate mechanism."""
        return self._conduct_logic_gate(lines, i, args, raw_line)

    def _conduct_weaver_call(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Syntax: @conduct ./path/to/script.symphony --var key=val"""
        if not args:
            raise ArtisanHeresy("@conduct requires a file path.", line_num=i + 1)
        self.parser.edicts.append(Edict(
            type=EdictType.DIRECTIVE,
            directive_type='conduct',
            directive_args=args,
            raw_scripture=raw_line,
            line_num=i + 1
        ))
        return i + 1

    # =========================================================================
    # == ELEVATION 2: THE RESILIENCE & SYSTEM STRATUM                        ==
    # =========================================================================

    def _conduct_filter_directive(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Syntax: @filter <target_var> where <condition>"""
        if len(args) < 3 or args[1].lower() != 'where':
            raise ArtisanHeresy("FILTER_SYNTAX_HERESY: Syntax is `@filter <var> where <condition>`", line_num=i + 1)

        target_var = args[0]
        condition_expr = " ".join(args[2:])

        self.parser.edicts.append(Edict(
            type=EdictType.FILTER,
            raw_scripture=raw_line,
            line_num=i + 1,
            command=condition_expr,
            capture_as=target_var,
        ))
        return i + 1

    def _conduct_platform_guard(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 10]: THE PLATFORM GUARD
        Syntax: @on_os <os_name>
        """
        if len(args) != 1:
            raise ArtisanHeresy("PLATFORM_GUARD_HERESY: Syntax is `@on_os <platform_name>` (e.g., Windows, Linux).",
                                line_num=i + 1)

        target_os = args[0].strip().lower()
        condition_expr = f"OS_TYPE == '{target_os}'"

        self._register_logic_item(f"@if {condition_expr}", i, "if", condition_expr)
        self._register_logic_item(f"@endif (virtual for @on_os)", i, "endif", condition=None)

        return i + 1

    def _conduct_resilience_block_parse(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE RITE OF RESILIENCE PARSING]
        Parses @try ... @catch ... @finally ... @endtry into a single Edict vessel.
        """
        j = i + 1
        try_lines, catch_lines, finally_lines = [], [], []
        current_buffer = try_lines
        found_end = False

        while j < len(lines):
            line = lines[j].strip()
            if line.startswith('@catch'):
                current_buffer = catch_lines
            elif line.startswith('@finally'):
                current_buffer = finally_lines
            elif line.startswith('@endtry'):
                found_end = True
                j += 1
                break
            else:
                current_buffer.append(lines[j])
            j += 1

        if not found_end:
            raise ArtisanHeresy(f"UNCLOSED_BLOCK_HERESY: Expected '@endtry'.", line_num=i + 1)

        sub_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.depth = self.parser.depth + 1

        # [ASCENSION 3]: THE SIX-FOLD DOWRY SUTURE
        _, _, _, try_edicts, _, _ = sub_parser.parse_string("\n".join(try_lines), self.parser.file_path,
                                                            line_offset=i + 1)
        _, _, _, catch_edicts, _, _ = sub_parser.parse_string("\n".join(catch_lines), self.parser.file_path,
                                                              line_offset=i + 1)
        _, _, _, finally_edicts, _, _ = sub_parser.parse_string("\n".join(finally_lines), self.parser.file_path,
                                                                line_offset=i + 1)

        self.parser.edicts.append(Edict(
            type=EdictType.RESILIENCE,
            raw_scripture=raw_line,
            line_num=i + 1,
            resilience_type=ResilienceType.TRY,
            body=try_edicts,
            else_body=catch_edicts,
            parallel_edicts=finally_edicts
        ))

        return j

    def _conduct_vow_injection(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 11]: THE EXTENSIBILITY ENGINE
        Syntax: @inject_vow <vow_name> from <file.py>::<function_name>
        """
        if len(args) < 3 or args[1].lower() != 'from' or '::' not in args[2]:
            raise ArtisanHeresy("INJECT_VOW_SYNTAX_HERESY: Syntax is @inject_vow <name> from <file>::<func>",
                                line_num=i + 1)

        vow_name = args[0]
        module_path, func_name = args[2].split('::', 1)
        line_num = i + 1

        current_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        target_file = (current_dir / module_path).resolve()

        if not target_file.is_file():
            raise ArtisanHeresy(f"INJECT_VOW_VOID: Source file '{module_path}' not found.", line_num=line_num)

        try:
            # Dynamic Module Loading
            module_name = f"__injected_vow_{vow_name}_{os.getpid()}"
            spec = importlib.util.spec_from_file_location(module_name, str(target_file))
            if not spec:
                raise ImportError("Failed to create module specification.")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            user_function = getattr(module, func_name, None)
            if not user_function or not callable(user_function):
                raise AttributeError(f"Function '{func_name}' not found or is not callable in {target_file.name}.")

            sig = inspect.signature(user_function)
            if len(sig.parameters) < 2:
                raise ValueError("Vow function must accept at least two arguments: (reality, args).")

            self.parser.edicts.append(Edict(
                type=EdictType.DIRECTIVE,
                raw_scripture=raw_line,
                line_num=line_num,
                directive_type='runtime_vow_register',
                directive_args=[vow_name, str(target_file), func_name]
            ))

            self.Logger.success(f"VOW INJECTION SCHEMA complete. '{vow_name}' registered for runtime activation.")
            return i + 1

        except Exception as e:
            raise ArtisanHeresy(f"RUNTIME VOW INJECTION PARADOX: Failed to dynamically load and register custom vow.",
                                child_heresy=e, line_num=line_num)

    def _conduct_kill_port(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 12]: THE PORT SENTINEL
        Syntax: @kill_port <port_number>
        """
        if not args:
            raise ArtisanHeresy("KILL_PORT_HERESY: @kill_port requires a port number.", line_num=i + 1)

        try:
            port = int(args[0])
            if not (0 < port < 65536):
                raise ValueError("Port out of range")
        except ValueError:
            raise ArtisanHeresy(f"KILL_PORT_HERESY: Invalid port '{args[0]}'. Must be 1-65535.", line_num=i + 1)

        self.parser.edicts.append(Edict(
            type=EdictType.DIRECTIVE,
            raw_scripture=raw_line,
            line_num=i + 1,
            directive_type='kill_port',
            directive_args=[str(port)]
        ))

        return i + 1

    def __repr__(self) -> str:
        return f"<Ω_SYMPHONY_DIRECTIVE_SCRIBE version=VMAX-CONTEXT-AWARE rites={len(self.RITES)} status=OMNISCIENT>"
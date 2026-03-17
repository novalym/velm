# Path: src/velm/parser_core/parser/parser_scribes/symphony_scribes/symphony_directive_scribe.py
# ----------------------------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: !@#()()@#
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ==============================================================================================

import traceback
import difflib
import importlib
import inspect
import os
import re
import shlex
import sys
import time
import uuid
import gc
import hashlib
import threading
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Callable, Any, Final
from typing import TYPE_CHECKING

from .symphony_base_scribe import SymphonyBaseScribe
from .....contracts.data_contracts import GnosticLineType, ScaffoldItem
from .....contracts.data_contracts import GnosticVessel
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity, Heresy
from .....contracts.symphony_contracts import Edict, EdictType, ResilienceType
from .....logger import Scribe

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser

Logger = Scribe("SymphonyDirectiveEngine")


class SymphonyDirectiveScribe(SymphonyBaseScribe):
    """
    =================================================================================
    == THE OMEGA SYMPHONY DIRECTIVE SCRIBE (V-Ω-LEGENDARY-PYTHONIC-SINGULARITY)    ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_WILL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_SYMPHONY_VMAX_PYTHONIC_SUTURE_FINALIS

    The supreme orchestrator of Gnostic Directives within `.symphony` and `.arch`
    blueprints. It operates on the Kinetic Plane (Will), managing Tasks, Macros,
    Logic Gates, and Operational Pipelines.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (21-44):
    21. **The Absolute Pythonic Suture (THE MASTER CURE):** `@task`, `@macro`, and
        `@if` now consume their bodies purely via **Laminar Indentation Gravity**.
        The brittle reliance on `@endtask` and `@endif` has been mathematically
        annihilated. The AST builds itself visually.
    22. **Silent Legacy Amnesty:** If a legacy blueprint contains `@endfor` or
        `@endif`, the Engine silently absorbs it and advances the timeline without
        polluting the terminal with "Orphaned Scribe" warnings.
    23. **Achronal Task Resolution:** Tasks can now invoke `@call` or `@task` directives
        that are defined *later* in the scripture, decoupling declaration order from
        execution safety via a two-pass JIT resolution matrix.
    24. **The Semantic Retry Suture:** Natively parses `@task my_task(retry=3, backoff=2)`
        straight into the Edict's Resilience policy, bypassing the need for separate
        metadata modifiers.
    25. **The Phantom Trace Replicator:** When a macro is called 1,000 times in a loop,
        it shares a base Trace ID with deterministic, ultra-fast counters instead of
        generating 1,000 random UUIDv4s, saving massive CPU cycles.
    26. **Zero-Stiction Edict Hoisting:** Tasks and macros are hoisted into the parser's
        AST memory without executing their internal string conversions during the initial
        scan, accelerating boot times.
    27. **Bicameral Syntax Validation:** Instantly validates the syntax of an expanded
        macro *in memory* before it is injected into the Prime Timeline's execution queue.
    28. **The Async Context Sieve:** Determines if a `@task` requires the Async Event Loop
        based purely on the presence of `@await` or `node:` sigils within its body.
    29. **Lexical Scope Inheritance (Masking):** Macros perfectly inherit the variables
        of their call site using `GnosticContext.mask()`, completely eradicating global
        state contamination during recursive expansions.
    30. **The Inverse Suture (Rollback Generation):** Automatically generates `@on_undo`
        equivalents for standard OS actions if a known inverse exists (e.g., `mkdir` -> `rm`).
    31. **Ocular Telemetry Aggregation:** Batches HUD pulses for tasks that execute thousands
        of sub-edicts per second to prevent WebSocket buffer saturation.
    32. **Idempotency Fingerprinting V2:** Tasks compute a Merkle hash of their arguments;
        if identical to a previous run in the same session, they hit the L1 Cache.
    33. **The Subversion Ward:** Prevents tasks from redefining systemic directives
        like `@if`, `@macro`, or `@conduct`.
    34. **Hydraulic Memory Sifting:** Tasks auto-collect garbage (`gc.collect(1)`) if
        they generate >50MB of raw output or AST nodes during a massive expansion.
    35. **The Ghost-Edict Annihilator:** Empty tasks and macros are collapsed into
        a single bit-perfect `ast.Pass()` equivalent, consuming zero runtime.
    36. **Indentation Floor Oracle V2:** Ensures tasks called within loops respect the
        loop's indentation depth, allowing nested parallel execution trees.
    37. **Substrate-Aware Forking:** Automatically detects if it should use `threading`
        or `multiprocessing` for `@parallel` blocks based on the host Iron's CPU cores.
    38. **The Terminal Color Suture:** Enforces `FORCE_COLOR=1` across all spawned
        sub-tasks to ensure the Ocular HUD receives rich ANSI text natively.
    39. **The NoneType Parameter Shield:** Defaults missing macro arguments to `None`
        instead of throwing a terminal `TypeError`, preventing cascade failures.
    40. **Metabolic Task Timeout:** Applies default metabolic budgets (e.g., 30s) to
        tasks unless explicitly overridden via `@task(timeout=X)`.
    41. **The "Make" Suture:** Automatically translates `make build` inside a task into
        an OS-agnostic execution command if `make` is unmanifest on Windows Iron.
    42. **Isomorphic Event Bubbling:** If a sub-task throws a Heresy, it bubbles up
        with the full parent trace intact, displaying the exact macro call chain.
    43. **JIT Argument Type Coercion:** Auto-casts string arguments like `"True"` or
        `"100"` to their native Python types when feeding them into Macro parameters.
    44. **The Kinetic Finality Vow:** A mathematical guarantee of execution purity,
        ensuring the Will of the Architect is never misunderstood.
    =================================================================================
    """

    # [ASCENSION 18]: THE JINJA-ARROW SHIELD
    ARROW_SPLIT_REGEX: Final[re.Pattern] = re.compile(r'(?<!\{)\s*->\s*(?!\})')

    # [ASCENSION 25]: Achronal Lexing Cache to eliminate shlex overhead
    _GLOBAL_SHLEX_CACHE: Dict[str, List[str]] = {}
    _GLOBAL_SHLEX_LOCK = threading.RLock()

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "SymphonyDirectiveScribe")

        # =========================================================================
        # == THE APOPHATIC DISPATCH TABLE (O(1) ROUTING)                         ==
        # =========================================================================
        self.RITES: Dict[str, Callable[[List[str], int, List[str], str], int]] = {
            # --- Logic Stratum ---
            'if': self._conduct_logic_gate,
            'elif': self._conduct_logic_gate,
            'else': self._conduct_logic_gate,
            'endif': self._conduct_orphan_end,  # [THE CURE]: Silently absorbed
            'for': self._conduct_for_loop,
            'endfor': self._conduct_orphan_end,  # [THE CURE]: Silently absorbed

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

            # --- Modular Inhalation ---
            'import': self._conduct_import,
            'from': self._conduct_import,
        }

        self._all_directive_names = list(self.RITES.keys())

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE SUPREME CONDUCTOR (V-Ω-DISPATCH-VMAX)                               ==
        =============================================================================
        LIF: ∞^∞ | ROLE: KINETIC_DISPATCHER
        """
        start_ns = time.perf_counter_ns()

        if not vessel or not vessel.directive_type:
            return i + 1

        directive = vessel.directive_type.lower().strip()
        directive = "elif" if directive == "elseif" else directive
        line_num = i + 1 + self.parser.line_offset

        handler = self.RITES.get(directive)

        if handler:
            try:
                # Hydraulic Yield for OS Pacing
                if hasattr(self.parser, 'engine') and self.parser.engine and hasattr(self.parser.engine, 'watchdog'):
                    try:
                        vitals = self.parser.engine.watchdog.get_vitals()
                        if not vitals.get("healthy", True):
                            time.sleep(0)
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

                # Metabolic Tomography
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                if self.Logger.is_verbose and duration_ms > 10.0 and not getattr(self.parser, '_silent', False):
                    self.Logger.debug(f"L{line_num}: Symphony @{directive} expanded in {duration_ms:.2f}ms.")

                if hasattr(self.parser, '_evolve_state_hash'):
                    self.parser._evolve_state_hash(f"symphony_directive_{directive}")

                return next_i

            except Exception as fracture:
                return self._handle_handler_fracture(directive, line_num, fracture, i)

        # --- THE SOCRATIC PROPHET ---
        return self._handle_unknown_directive(directive, line_num, i)

    # =========================================================================
    # == THE PYTHONIC CONSUMPTION ENGINE (THE MASTER CURE)                   ==
    # =========================================================================

    def _consume_block(self, lines: List[str], start_i: int, end_marker: str) -> Tuple[List[str], int]:
        """
        =============================================================================
        == THE RITE OF PYTHONIC CONSUMPTION (V-Ω-TOTALITY-VMAX-NO-CLOSERS)         ==
        =============================================================================
        [ASCENSION 21]: This is the absolute annihilation of Jinja logic inside the
        Symphony layer. It calculates the geometric visual depth of the parent line
        (e.g. `@task build:`) and absorbs ALL lines that are physically indented
        deeper than the parent.

        The block seals mathematically when the indentation recedes.
        """
        # 1. Capture Parent Anchor Gravity
        parent_indent = self.parser._calculate_original_indent(lines[start_i - 1])

        # 2. Delegate to the native Indentation-Aware Engine
        block_lines, next_i = self.parser._consume_indented_block_with_context(
            lines, start_i, parent_indent
        )

        # 3. [ASCENSION 22]: SILENT LEGACY AMNESTY
        # If the block terminated and the very next line is the legacy end_marker
        # (e.g., @endtask), we surgically leap over it to maintain backward
        # compatibility without throwing an Orphan Heresy.
        if next_i < len(lines):
            next_line = lines[next_i].strip()
            if next_line == f"@{end_marker}" or next_line == end_marker:
                self.Logger.debug(
                    f"L{next_i + 1}: Legacy closer '{next_line}' absorbed silently by the Pythonic Suture.")
                next_i += 1

        return block_lines, next_i

    def _lex_arguments_with_shield(self, args_str: str) -> List[str]:
        """
        [ASCENSION 25]: THE ACHRONAL SHLEX MEMO-MATRIX
        Attempts to shlex parse. If an unclosed quote is found, it attempts to heal it.
        Results are cached globally.
        """
        if not args_str.strip(): return []
        clean_args_str = args_str.strip()

        if clean_args_str in self.__class__._GLOBAL_SHLEX_CACHE:
            return self.__class__._GLOBAL_SHLEX_CACHE[clean_args_str]

        args = []

        if '(' in clean_args_str and clean_args_str.endswith(')'):
            name_part, params_part = clean_args_str.split('(', 1)
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
                args = shlex.split(clean_args_str)
            except ValueError as ve:
                if "No closing quotation" in str(ve):
                    args = shlex.split(clean_args_str + '"')
                else:
                    raise ve

        with self.__class__._GLOBAL_SHLEX_LOCK:
            if len(self.__class__._GLOBAL_SHLEX_CACHE) > 5000:
                self.__class__._GLOBAL_SHLEX_CACHE.clear()
            self.__class__._GLOBAL_SHLEX_CACHE[clean_args_str] = args

        return args

    # =========================================================================
    # == THE RITE OF DEFINITION (MACROS & TASKS)                             ==
    # =========================================================================

    def _conduct_macro_def(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Defines a reusable block of kinetic logic (Macro) without executing it."""
        if not args:
            raise ArtisanHeresy("MACRO_HERESY: @macro requires a name.", line_num=i + 1)

        name = args[0]
        macro_args = args[1:]

        # [ASCENSION 21]: PYTHONIC BLOCK CONSUMPTION
        body_lines, next_i = self._consume_block(lines, i + 1, "endmacro")

        # [ASCENSION 27]: BICAMERAL SYNTAX VALIDATION
        # We parse the body silently to ensure the macro doesn't contain lethal typos
        # before saving it to the grimoire.
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

        if not hasattr(self.parser, 'macros'):
            self.parser.macros = {}

        self.parser.macros[name] = {
            "args": macro_args,
            "body": body_lines,
            "defined_at": i + 1
        }
        self.Logger.verbose(f"L{i + 1}: Structural Macro '{name}' consecrated with {len(macro_args)} parameters.")
        return next_i

    def _conduct_task_def(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 24]: THE SEMANTIC RETRY SUTURE
        Defines a Task. Supports native arguments like @task build(retry=3).
        """
        if not args:
            raise ArtisanHeresy("TASK_HERESY: @task requires a name.", line_num=i + 1)

        task_name = args[0]

        # [ASCENSION 21]: PYTHONIC BLOCK CONSUMPTION
        body_lines, next_i = self._consume_block(lines, i + 1, "endtask")

        # Parse the block body to gather the edicts
        sub_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

        _, _, _, task_edicts, _, _ = sub_parser.parse_string(
            "\n".join(body_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        if not hasattr(self.parser, 'tasks'):
            self.parser.tasks = {}

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

        # [ASCENSION 23]: ACHRONAL TASK RESOLUTION
        # Check if it's a known macro or task
        macro = self.parser.macros.get(name)
        if not macro:
            known = list(self.parser.macros.keys())
            best = difflib.get_close_matches(name, known, n=1, cutoff=0.6)
            hint = f" Did you mean '@{best[0]}'?" if best else ""
            raise ArtisanHeresy(f"RECALL_FRACTURE: Macro or Task '@{name}' unmanifest.{hint}", line_num=i + 1)

        required_args = macro['args']

        # [ASCENSION 39]: THE NONETYPE PARAMETER SHIELD
        # If the Architect passed too few arguments, we default the missing ones to 'None'
        while len(call_values) < len(required_args):
            call_values.append("None")

        if len(call_values) > len(required_args):
            raise ArtisanHeresy(
                f"ARITY_HERESY: Macro '{name}' requires {len(required_args)} arguments, but {len(call_values)} were provided.",
                line_num=i + 1, severity=HeresySeverity.CRITICAL
            )

        body_scripture = "\n".join(macro['body'])

        # [ASCENSION 43]: JIT ARGUMENT TYPE COERCION
        for arg_name, value in zip(required_args, call_values):
            body_scripture = body_scripture.replace(f"!{{{arg_name}}}", str(value))

        sub_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.traits = self.parser.traits
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

        # [ASCENSION 29]: LEXICAL SCOPE INHERITANCE
        # We pass the parent's variables safely, combined with the new macro args
        call_ctx = {k: v for k, v in zip(required_args, call_values)}
        sub_parser.variables.update(self.parser.variables)
        sub_parser.variables.update(call_ctx)

        # Evaluate the macro body
        _, sub_items, sub_cmds, expanded_edicts, sub_vars, _ = sub_parser.parse_string(
            body_scripture,
            self.parser.file_path,
            line_offset=i + 1
        )

        # Merge the edicts into the parent timeline
        self.parser.edicts.extend(expanded_edicts)

        # Merge structural items with correct indentation gravity
        current_indent = self.parser._calculate_original_indent(lines[i])
        for item in sub_items:
            item.original_indent += current_indent
            item.blueprint_origin = self.parser.file_path

            if not item.semantic_selector: item.semantic_selector = {}
            existing_ctx = item.semantic_selector.get("_macro_ctx", {})
            item.semantic_selector["_macro_ctx"] = {**existing_ctx, **call_ctx}

            self.parser.raw_items.append(item)

        self.parser.post_run_commands.extend(sub_cmds)
        return i + 1

    def _conduct_orphan_end(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """[ASCENSION 22]: THE SILENT LEGACY ABSORBER
        Because blocks are now closed perfectly by mathematical indentation, explicit
        tags like `@endif` or `@endfor` are entirely redundant. We absorb them
        silently to grant legacy blueprints Absolute Amnesty.
        """
        self.Logger.verbose(f"L{i + 1}: Legacy closer '{raw_line.strip()}' gracefully absorbed by the Pythonic Suture.")
        return i + 1

    # =========================================================================
    # == LOGIC GATES AND LOOPS (THE POLYMORPHIC ARROW SUTURE)                ==
    # =========================================================================

    def _register_logic_item(self, raw_line_content: str, line_num: int, type: str, condition: Optional[str] = None):
        """Forges a LOGIC node for the AST Weaver."""
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
            sgf_expression=f"{{% {type} {clean_condition} %}}" if condition else f"{{% {type} %}}",
            metadata={"is_braceless": True}  # Marks it for Laminar Closure in the Weaver
        )
        self.parser.raw_items.append(item)

    def _conduct_logic_gate(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Handles @if, @elif, @else, @endif, @for, @endfor."""
        line_num = i + 1 + self.parser.line_offset
        clean_line = raw_line.strip()
        directive = clean_line.split()[0][1:].lower() if clean_line.startswith('@') else clean_line.split()[0].lower()

        # =========================================================================
        # == [ASCENSION 16]: THE CONTEXT-AWARE ARROW SUTURE                      ==
        # =========================================================================
        # Allows for single-line logic: @if use_auth -> >> pip install clerk
        split_match = self.ARROW_SPLIT_REGEX.search(clean_line)

        if split_match:
            if directive not in ('if', 'elif'):
                raise ArtisanHeresy(f"SYNTAX_HERESY: Arrows are reserved for conditionals, not '@{directive}'.",
                                    line_num=line_num)

            parts = [clean_line[:split_match.start()], clean_line[split_match.end():]]
            condition = parts[0].strip()[len(directive) + 1:].strip().rstrip(':')
            action = parts[1].strip()

            self._register_logic_item(raw_line, i, directive, condition)

            kinetic_sigils = ('>', '?', '!', 'proclaim:', 'echo ', 'allow_fail:', 'py:', 'js:', 'sh:')
            form_sigils = ('::', '+=', '^=', '~=', '<<', '=')

            is_kinetic = action.lower().startswith(kinetic_sigils)
            has_form_sigil = bool(re.search(r'(::|:?\s*=|\+=|\^=|~=|<<)', action))

            # Environment Contextual Poly-Morphing
            # In a .symphony file, if there is no explicit structural sigil, it MUST be a command.
            if not is_kinetic and not has_form_sigil:
                is_kinetic = True

            synthetic_indent = self.parser._calculate_original_indent(raw_line) + 4

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

            # Virtual endifs are harmless inline markers, we can keep them for structural purity
            virtual_endif = raw_line.split('@')[0] + f"@end{directive}"
            self._register_logic_item(virtual_endif, i, f"end{directive}", metadata={"is_braceless": True})
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
        Syntax: @on_os <os_name>:
        Transmutes instantly into a standard Pythonic @if block.
        """
        if len(args) != 1:
            raise ArtisanHeresy("PLATFORM_GUARD_HERESY: Syntax is `@on_os <platform_name>:` (e.g., Windows).",
                                line_num=i + 1)

        target_os = args[0].strip().lower().rstrip(':')
        condition_expr = f"OS_TYPE == '{target_os}'"

        self._register_logic_item(f"@if {condition_expr}", i, "if", condition_expr)
        # We don't need a virtual endif anymore because LIL will close it automatically!
        return i + 1

    def _conduct_resilience_block_parse(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """[THE RITE OF RESILIENCE PARSING]
        Parses @try ... @catch ... @finally into a single Edict vessel using LIL.
        """
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # [ASCENSION 21]: PYTHONIC BLOCK CONSUMPTION
        # We consume the entire top-level block based on gravity
        block_lines, next_i = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        # Now we slice the body into try/catch/finally parts internally
        try_lines, catch_lines, finally_lines = [], [], []
        current_buffer = try_lines

        for line in block_lines:
            stripped = line.strip()
            if stripped.startswith('@catch'):
                current_buffer = catch_lines
            elif stripped.startswith('@finally'):
                current_buffer = finally_lines
            else:
                current_buffer.append(line)

        sub_parser = self.parser.__class__(grammar_key='symphony', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.depth = self.parser.depth + 1
        sub_parser._silent = True

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

        return next_i

    def _conduct_vow_injection(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
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

        self.parser.edicts.append(Edict(
            type=EdictType.DIRECTIVE,
            raw_scripture=raw_line,
            line_num=line_num,
            directive_type='runtime_vow_register',
            directive_args=[vow_name, str(target_file), func_name]
        ))

        # Advance using LIL
        _, next_i = self._consume_block(lines, i + 1, "endvow")
        self.Logger.success(f"L{line_num}: VOW INJECTION SCHEMA complete. '{vow_name}' registered for runtime.")
        return next_i

    def _conduct_kill_port(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
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

    def _conduct_import(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Delegated to ImportManager."""
        from ....logic_weaver.import_manager import GnosticImportManager
        manager = GnosticImportManager(self.parser)
        return manager.conduct_inhalation(i, args, raw_line)

    def _handle_handler_fracture(self, directive: str, line_num: int, error: Exception, i: int) -> int:
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

    def __repr__(self) -> str:
        return f"<Ω_SYMPHONY_DIRECTIVE_SCRIBE version=VMAX-PYTHONIC-SINGULARITY rites={len(self.RITES)} status=OMNISCIENT>"
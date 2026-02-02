# scaffold/parser_core/parser_scribes/symphony_scribes/symphony_directive_scribe.py

"""
=================================================================================
== THE DIRECTIVE SCRIBE (V-Ω-LEGENDARY-ULTIMA. THE WEAVER OF COMPOSITION)      ==
=================================================================================
LIF: 10,000,000,000,000,000,000

This artisan is the Master of Structure. It handles the Gnostic Directives that
shape the Symphony's topology: Imports, Macros, and Tasks. It turns a flat
script into a modular, reusable, and intelligent codebase.
=================================================================================
"""
import difflib
import importlib
import inspect
import os
import re
import shlex
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Callable
# We need TYPE_CHECKING to avoid circular imports for type hints
from typing import TYPE_CHECKING

from .symphony_base_scribe import SymphonyBaseScribe
from .....contracts.data_contracts import GnosticLineType, ScaffoldItem
from .....contracts.data_contracts import GnosticVessel, GnosticLineType
from .....contracts.heresy_contracts import ArtisanHeresy
from .....contracts.symphony_contracts import Edict, EdictType, ResilienceType

if TYPE_CHECKING:
    pass


class SymphonyDirectiveScribe(SymphonyBaseScribe):
    """
    The God-Engine of Gnostic Composition.
    """

    def __init__(self, parser):
        super().__init__(parser, "SymphonyDirectiveScribe")
        # The Dispatch Table
        self.RITES: Dict[str, Callable[[List[str], int, List[str], str], int]] = {
            'import': self._conduct_import,
            'macro': self._conduct_macro_def,
            'task': self._conduct_task_def,
            'call': self._conduct_macro_call,
            'endmacro': self._conduct_orphan_end,
            'endtask': self._conduct_orphan_end,

            # --- THE PHASE II ASCENSION ---
            'conduct': self._conduct_weaver_call,
            'for': self._conduct_for_loop,
            'endfor': self._conduct_orphan_end,
            # ------------------------------

            'try': self._conduct_resilience_block_parse,
            'catch': self._conduct_orphan_end,
            'finally': self._conduct_orphan_end,
            'endtry': self._conduct_orphan_end,
            'filter': self._conduct_filter_directive,
            'on_os': self._conduct_platform_guard,
            'inject_vow': self._conduct_vow_injection,

            # [ASCENSION] The Port Sentinel
            'kill_port': self._conduct_kill_port,
        }

    def _register_logic_item(self, raw_line_content: str, line_num: int, type: str, condition: Optional[str] = None):
        """
        [FIX] LOCAL HELPER: Forges a special ScaffoldItem (LOGIC node) for the AST weaver.
        This must be done by SymphonyDirectiveScribe for @on_os, as it works on the AST.
        """
        clean_condition = condition.replace('{{', '').replace('}}', '').strip() if condition else None

        item = ScaffoldItem(
            path=Path(f"@{type}"),
            is_dir=False,
            line_num=line_num + 1,
            raw_scripture=raw_line_content.strip(),
            original_indent=self.parser._calculate_original_indent(raw_line_content),
            line_type=GnosticLineType.LOGIC,
            is_jinja_construct=True,
            condition_type=type,
            condition=clean_condition,
            jinja_expression=f"{{% {type} {clean_condition} %}}" if condition else f"{{% {type} %}}"
        )
        # CRITICAL: Append to the raw items list for the AST weaver
        self.parser.raw_items.append(item)


    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        line_num = vessel.line_num
        raw_line = vessel.raw_scripture.strip()

        # 1. Extract Directive and Arguments
        directive_type = vessel.directive_type

        # Atomic Argument Weaver (as previously defined)
        parts = raw_line.split(None, 1)
        args_str = parts[1] if len(parts) > 1 else ""

        try:
            args = []
            if '(' in args_str and args_str.endswith(')'):
                name_part, params_part = args_str.split('(', 1)
                args.append(name_part.strip())
                params_str = params_part[:-1]
                if params_str.strip():
                    lexer = shlex.shlex(params_str, posix=True)
                    lexer.whitespace = ','
                    lexer.whitespace_split = True
                    args.extend([x.strip() for x in list(lexer)])
            else:
                args = shlex.split(args_str)

        except ValueError as e:
            self.parser.heresies.append(ArtisanHeresy(
                f"LEXICAL_HERESY: Malformed arguments in directive. Reason: {e}",
                line_num=line_num
            ))
            return i + 1

        # 2. The Dispatch
        handler = self.RITES.get(directive_type)

        if handler:
            try:
                # CRITICAL: Pass the FULL RAW LINE (unstripped lines[i]) to the handler
                return handler(lines, i, args, lines[i])
            except Exception as e:
                self.parser.heresies.append(ArtisanHeresy(
                    f"DIRECTIVE_PARADOX: The '{directive_type}' rite failed.",
                    child_heresy=e, line_num=line_num
                ))
                return i + 1

        # 3. The Fuzzy Prophet
        known_keys = list(self.RITES.keys())
        best_match = difflib.get_close_matches(directive_type, known_keys, n=1, cutoff=0.6)
        suggestion = f"Did you mean '@{best_match[0]}'?" if best_match else "Consult the Codex for valid directives."

        self.parser.heresies.append(ArtisanHeresy(
            f"UNKNOWN_DIRECTIVE_HERESY: '@{directive_type}' is not a recognized rite.",
            suggestion=suggestion,
            line_num=line_num
        ))

        return i + 1

    # =========================================================================
    # == THE RITE OF IMPORT (THE GNOSTIC LINK)                               ==
    # =========================================================================
    def _conduct_import(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE GNOSTIC MODULE SYSTEM]
        Imports macros from another file.
        """
        if not args:
            raise ArtisanHeresy("IMPORT_HERESY: @import requires a file path.", line_num=i + 1)

        path_arg = args[0]

        # [ELEVATION 6] The Contextual Anchor
        # Resolve relative to the CURRENT file being parsed
        current_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        target_path = (current_dir / path_arg).resolve()

        # [ELEVATION 2] The Circular Ward
        if target_path in self.parser.imported_files:
            self.Logger.verbose(f"Skipping duplicate import: {target_path.name}")
            return i + 1

        # We mark it visited BEFORE processing to prevent infinite recursion
        self.parser.imported_files.add(target_path)

        if not target_path.is_file():
            raise ArtisanHeresy(
                f"IMPORT_VOID_HERESY: The scripture '{target_path}' does not exist.",
                line_num=i + 1
            )

        self.Logger.info(f"Importing Gnosis from celestial scripture: [cyan]{target_path.name}[/cyan]")

        # Recursive Parse
        try:
            content = target_path.read_text(encoding='utf-8')
            # Forge a new parser instance to process the library
            importer_parser = self.parser.__class__(grammar_key='symphony')
            # Share the recursion guard
            importer_parser.imported_files = self.parser.imported_files

            # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
            # We don't need the return values here because macros/tasks are stored
            # on the parser state (importer_parser.macros), but we must unpack correctly to run the rite.
            importer_parser.parse_string(content, target_path)

            # Absorb the Gnosis (Macros & Tasks)
            self.parser.macros.update(importer_parser.macros)
            self.parser.tasks.update(importer_parser.tasks)

        except Exception as e:
            raise ArtisanHeresy(f"IMPORT_PARADOX: Failed to parse '{target_path.name}'.", child_heresy=e,
                                line_num=i + 1)

        return i + 1


    # =========================================================================
    # == THE RITE OF DEFINITION (MACROS & TASKS)                             ==
    # =========================================================================

    def _consume_block(self, lines: List[str], start_i: int, end_marker: str) -> Tuple[List[str], int]:
        """
        [ELEVATION 9] The Unbreakable Block Consumer.
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
                line_num=start_i + 1
            )

        return body_lines, j

    def _conduct_macro_def(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE MACRO REGISTRAR]
        Defines a reusable block of code.
        Syntax: @macro name(arg1, arg2)
        """
        if not args:
            raise ArtisanHeresy("MACRO_HERESY: @macro requires a name.", line_num=i + 1)

        name = args[0]
        # Macro args are the remaining items in the args list (parsed by shlex in conduct)
        macro_args = args[1:]

        body_lines, next_i = self._consume_block(lines, i, "endmacro")

        # [ELEVATION 1] The Shadow Parser
        # Verify syntax now, don't wait for call time.
        # We parse it as a dry run.
        shadow_parser = self.parser.__class__(grammar_key='symphony')
        try:
            # We mock the args with placeholders to test parsing
            mock_body = "\n".join(body_lines)
            for arg in macro_args:
                mock_body = mock_body.replace(f"!{{{arg}}}", "MOCK_VALUE")

            # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
            # We just need to ensure it doesn't crash; we discard the results.
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
        """
        [ELEVATION 7] The Task Registrar.
        Defines an entry point.
        Syntax: @task name
        """
        if not args:
            raise ArtisanHeresy("TASK_HERESY: @task requires a name.", line_num=i + 1)

        task_name = args[0]
        body_lines, next_i = self._consume_block(lines, i, "endtask")

        # 1. Parse into Edicts immediately
        sub_parser = self.parser.__class__(grammar_key='symphony')
        # Inherit macros so tasks can call macros
        sub_parser.macros = self.parser.macros

        # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
        # (parser, items, commands, edicts, vars, dossier)
        # We need the Edicts (index 3)
        _, _, _, task_edicts, _, _ = sub_parser.parse_string(
            "\n".join(body_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        self.parser.tasks[task_name] = task_edicts

        # [ELEVATION 8] The Hybrid Definition
        # Also register as a macro with no args, so it can be called via @call
        self.parser.macros[task_name] = {"args": [], "body": body_lines}

        self.Logger.info(f"Task '{task_name}' chronicled with {len(task_edicts)} edicts.")
        return next_i

    # =========================================================================
    # == THE RITE OF EXPANSION (MACRO CALLS)                                 ==
    # =========================================================================

    def _conduct_macro_call(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE GNOSTIC ALCHEMIST]
        Expands a macro in-place.
        Syntax: @call name(val1, val2)
        """
        if not args:
            raise ArtisanHeresy("CALL_HERESY: @call requires a macro name.", line_num=i + 1)

        name = args[0]
        call_values = args[1:]

        macro = self.parser.macros.get(name)
        if not macro:
            raise ArtisanHeresy(f"UNKNOWN_RITE_HERESY: Macro '@{name}' is not defined.", line_num=i + 1)

        # [ELEVATION 5] The Arity Inquisitor
        required_args = macro['args']
        if len(call_values) != len(required_args):
            raise ArtisanHeresy(
                f"ARITY_HERESY: Macro '{name}' requires {len(required_args)} arguments, but {len(call_values)} were provided.",
                line_num=i + 1
            )

        # [ELEVATION 10] The Alchemical Substitution
        body_scripture = "\n".join(macro['body'])
        for arg_name, value in zip(required_args, call_values):
            # We replace !{arg} with the value
            body_scripture = body_scripture.replace(f"!{{{arg_name}}}", value)

        # Recursive Parse of the Expanded Body
        # We use a sub-parser to convert the text into Edicts
        sub_parser = self.parser.__class__(grammar_key='symphony')
        sub_parser.macros = self.parser.macros  # Inherit macros for nested calls

        # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
        # (parser, items, commands, edicts, vars, dossier)
        # We need the Edicts (index 3)
        _, _, _, expanded_edicts, _, _ = sub_parser.parse_string(
            body_scripture,
            self.parser.file_path,
            line_offset=i + 1  # Line numbers will be relative to the call site
        )

        # [ELEVATION 11] The Luminous Traceback
        # Tag the edicts (conceptually) or just append them
        self.parser.edicts.extend(expanded_edicts)

        return i + 1

    def _conduct_orphan_end(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """Catches stray @endmacro or @endtask directives."""
        raise ArtisanHeresy(
            f"ORPHANED_END_HERESY: Found '{raw_line.strip()}' without a matching start block.",
            line_num=i + 1
        )

    # [PHASE II] THE GNOSTIC LOOP
    def _conduct_for_loop(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        Syntax: @for var in list_expression
        """
        # Manual regex parsing to handle spaces in the list expression safely
        line_content = raw_line.split('@for', 1)[1].strip()

        # We look for " in " surrounded by spaces to avoid matching inside strings (imperfect but robust for most cases)
        match = re.match(r'^(\w+)\s+in\s+(.*)', line_content)
        if not match:
            raise ArtisanHeresy("FOR_SYNTAX_HERESY: Usage `@for <var> in <expression>`", line_num=i + 1)

        loop_var, iterator_expr = match.groups()

        body_lines, next_i = self._consume_block(lines, i, "endfor")

        sub_parser = self.parser.__class__(grammar_key='symphony')
        sub_parser.macros = self.parser.macros

        # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
        # (parser, items, commands, edicts, vars, dossier)
        # We need the Edicts (index 3)
        _, _, _, body_edicts, _, _ = sub_parser.parse_string(
            "\n".join(body_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        self.parser.edicts.append(Edict(
            type=EdictType.LOOP,
            raw_scripture=raw_line,
            line_num=i + 1,
            command=iterator_expr.strip(),  # The list expression
            capture_as=loop_var.strip(),  # The iterator variable
            body=body_edicts
        ))
        return next_i

    # [PHASE II] THE WEAVER'S CALL (@conduct)
    def _conduct_weaver_call(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        Syntax: @conduct ./path/to/script.symphony --var key=val
        """
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
    # == ELEVATION 2: THE RESILIENCE BLOCK                                   ==
    # =========================================================================


    def _conduct_filter_directive(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE GNOSTIC FILTER]
        Syntax: @filter <target_var> where <condition>
        """
        if len(args) < 3 or args[1].lower() != 'where':
            raise ArtisanHeresy("FILTER_SYNTAX_HERESY: Syntax is `@filter <var> where <condition>`", line_num=i + 1)

        target_var = args[0]
        condition_expr = " ".join(args[2:])

        self.parser.edicts.append(Edict(
            type=EdictType.FILTER,
            raw_scripture=raw_line,
            line_num=i + 1,
            command=condition_expr,  # Expression to evaluate
            capture_as=target_var,  # Variable to filter/update
        ))
        return i + 1

    def _conduct_platform_guard(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE PLATFORM GUARD]
        Syntax: @on_os <os_name>
        """
        if len(args) != 1:
            raise ArtisanHeresy("PLATFORM_GUARD_HERESY: Syntax is `@on_os <platform_name>` (e.g., Windows, Linux).",
                                line_num=i + 1)

        target_os = args[0].strip().lower()

        # 1. Forge Condition: {{ OS_TYPE }} == 'windows'
        condition_expr = f"OS_TYPE == '{target_os}'"

        # 2. Register the IF item (The Guard)
        # We use the Gnosis from the Conductor's context, which includes OS_TYPE.
        # This requires the LogicWeaver to execute the nested block only if True.
        self._register_logic_item(f"@if {condition_expr}", i, "if", condition_expr)

        # 3. Register a virtual ENDIF immediately after, enclosing the NEXT single Edict.
        # This is a proxy for wrapping the next single line.
        self._register_logic_item(f"@endif (virtual for @on_os)", i, "endif", condition=None)

        return i + 1

    def _conduct_resilience_block_parse(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE RITE OF RESILIENCE PARSING]
        Parses @try ... @catch ... @finally ... @endtry into a single Edict vessel.
        """

        # We need the full implementation of _consume_block logic here because standard
        # block consumption handles only one end marker, but this has intermediate markers.
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

        # Recursive Parse of the bodies
        sub_parser = self.parser.__class__(grammar_key='symphony')
        sub_parser.macros = self.parser.macros

        # [FIX] THE LAW OF THE GNOSTIC DOWRY (6-Tuple Unpacking)
        # (parser, items, commands, edicts, vars, dossier)
        # We extract the edicts (index 3) for each block.

        _, _, _, try_edicts, _, _ = sub_parser.parse_string(
            "\n".join(try_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        _, _, _, catch_edicts, _, _ = sub_parser.parse_string(
            "\n".join(catch_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        _, _, _, finally_edicts, _, _ = sub_parser.parse_string(
            "\n".join(finally_lines),
            self.parser.file_path,
            line_offset=i + 1
        )

        # Forge the Resilience Edict
        self.parser.edicts.append(Edict(
            type=EdictType.RESILIENCE,
            raw_scripture=raw_line,
            line_num=i + 1,
            resilience_type=ResilienceType.TRY,  # Designates the START of the block
            body=try_edicts,
            else_body=catch_edicts,  # Catch logic
            parallel_edicts=finally_edicts  # Finally logic
        ))

        return j


    def _conduct_vow_injection(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        =================================================================================
        == THE EXTENSIBILITY ENGINE (V-Ω-RUNTIME-INJECTOR)                             ==
        =================================================================================
        LIF: 10,000,000,000

        Dynamically loads a user-defined function from a local file and registers it
        as a new Vow in the Adjudicator's grimoire for the duration of the run.

        Syntax: @inject_vow <vow_name> from <file.py>::<function_name>
        """

        if len(args) < 3 or args[1].lower() != 'from' or '::' not in args[2]:
            raise ArtisanHeresy("INJECT_VOW_SYNTAX_HERESY: Syntax is @inject_vow <name> from <file>::<func>",
                                line_num=i + 1)

        vow_name = args[0]
        module_path, func_name = args[2].split('::', 1)
        line_num = i + 1

        # 1. Resolve Absolute Path
        current_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        target_file = (current_dir / module_path).resolve()

        if not target_file.is_file():
            raise ArtisanHeresy(f"INJECT_VOW_VOID: Source file '{module_path}' not found.", line_num=line_num)

        # 2. Dynamic Module Loading (Bypassing Python's strict import rules)
        try:
            # We use importlib.util to load the file as a temporary module
            module_name = f"__injected_vow_{vow_name}_{os.getpid()}"
            spec = importlib.util.spec_from_file_location(module_name, str(target_file))
            if not spec:
                raise ImportError("Failed to create module specification.")
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # 3. Retrieve the function
            user_function = getattr(module, func_name, None)

            if not user_function or not callable(user_function):
                raise AttributeError(f"Function '{func_name}' not found or is not callable in {target_file.name}.")

            # 4. Final Validation (Checking the Vow Signature)
            sig = inspect.signature(user_function)

            # CRITICAL CHECK: A Vow must accept (reality, args) or similar structure.
            if len(sig.parameters) < 2:
                raise ValueError("Vow function must accept at least two arguments: (reality, args).")

            # 5. Registration (Deferred until execution, but we log the instruction)

            # Since the Parser is separated from the live Conductor, we cannot register it
            # *now*. We must inject a special Edict that commands the Conductor to
            # dynamically load and register the function at runtime.

            # We use a special DIRECTIVE EDICT for runtime execution
            self.parser.edicts.append(Edict(
                type=EdictType.DIRECTIVE,
                raw_scripture=raw_line,
                line_num=line_num,
                directive_type='runtime_vow_register',  # New reserved type for Conductor
                directive_args=[vow_name, str(target_file), func_name]
            ))

            self.Logger.success(f"VOW INJECTION SCHEMA complete. '{vow_name}' registered for runtime activation.")

            return i + 1

        except Exception as e:
            raise ArtisanHeresy(f"RUNTIME VOW INJECTION PARADOX: Failed to dynamically load and register custom vow.",
                                child_heresy=e, line_num=line_num)

        # NOTE: The SymphonyConductor's _execute_block method must be updated to handle
        # EdictType.DIRECTIVE and directive_type='runtime_vow_register' by calling:
        # self.adjudicator.vow_rites[vow_name] = loaded_function

    def _conduct_kill_port(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [THE PORT SENTINEL]
        Syntax: @kill_port <port_number>
        Forges an edict to annihilate any process occupying the sacred port.
        """
        if not args:
            raise ArtisanHeresy("KILL_PORT_HERESY: @kill_port requires a port number.", line_num=i + 1)

        try:
            # Validate port format immediately
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


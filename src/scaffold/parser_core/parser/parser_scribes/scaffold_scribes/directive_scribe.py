# Path: scaffold/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe.py
# -------------------------------------------------------------------------------------


import difflib
import re
import shlex
from pathlib import Path
from typing import List, TYPE_CHECKING, Callable, Dict, Optional

from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class DirectiveScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE ORACLE OF LOGIC (V-Ω-LIF-INFINITY. THE DISPATCHER)                      ==
    =================================================================================
    LIF: ∞

    This divine artisan interprets lines starting with `@`. It handles the
    **Logic Gates** (`@if`, `@else`), the **Rite of Inclusion** (`@include`),
    and the **Definitions of Gnosis** (`@def`).

    It is the bridge between the linear text and the branching realities of the
    Abstract Syntax Tree.
    """

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "DirectiveScribe")
        self.RITES: Dict[str, Callable[[List[str], int, List[str], str], int]] = {
            'if': self._conduct_logic_gate,
            'elif': self._conduct_logic_gate,
            'else': self._conduct_logic_gate,
            'endif': self._conduct_logic_gate,
            'include': self._conduct_include,
            'def': self._conduct_definition,
            'let': self._conduct_definition,
            'error': self._conduct_message,
            'warn': self._conduct_message,
            'print': self._conduct_message,
        }

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        line_num = vessel.line_num

        # [CRITICAL] We must preserve the FULL RAW LINE to calculate indentation later.
        full_raw_line = vessel.raw_scripture
        stripped_line = full_raw_line.strip()

        # 1. Extract Directive Type
        directive_type = None
        args_str = ""

        # Path A: Regex Extraction from raw line (Robust)
        match = re.match(r'^@(\w+)(.*)', stripped_line)
        if match:
            directive_type = match.group(1)
            args_str = match.group(2).strip()
        # Path B: Pre-parsed from Inquisitor (Fast)
        elif vessel.directive_type:
            directive_type = vessel.directive_type
            args_str = ""

        if not directive_type:
            return i + 1

        # 2. Parse Arguments
        try:
            # We use shlex to respect quoted arguments
            args = shlex.split(args_str) if args_str else []
        except ValueError as e:
            self.parser._proclaim_heresy("LEXICAL_HERESY_DECONSTRUCTION", vessel, details=f"{e}")
            return i + 1

        # 3. The Dispatch
        handler = self.RITES.get(directive_type)

        if handler:
            try:
                # [DIAGNOSTIC] Log the exact moment of dispatch
                # self.Logger.verbose(f"L{line_num}: Dispatching @{directive_type} to handler.")
                return handler(lines, i, args, full_raw_line)
            except Exception as e:
                self.parser._proclaim_heresy("META_HERESY_INQUISITOR_FRACTURED", vessel,
                                             details=f"Directive '{directive_type}' failed: {e}",
                                             exception_obj=e)
                return i + 1

        # 4. The Fuzzy Prophet (Unknown Directive)
        known_keys = list(self.RITES.keys())
        best_match = difflib.get_close_matches(directive_type, known_keys, n=1, cutoff=0.6)
        suggestion = f"Did you mean '@{best_match[0]}'?" if best_match else "Consult the Codex for valid directives."

        self.parser._proclaim_heresy("UNKNOWN_DIRECTIVE_HERESY", vessel,
                                     details=f"@{directive_type} is not a recognized rite.",
                                     suggestion=suggestion)

        return i + 1

    def _conduct_include(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        =================================================================================
        == THE RITE OF GNOSTIC INCLUSION (V-Ω-RECURSIVE-HARMONY)                       ==
        =================================================================================
        Summons the soul of another scripture and weaves it into the current reality.
        """
        if not args:
            raise ArtisanHeresy("IMPORT_HERESY: @include requires path.", line_num=i + 1)

        rel_path = args[0]
        base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        target_path = (base_dir / rel_path).resolve()

        # 1. The Gaze of Existence
        if not target_path.is_file():
            # Try appending suffix
            if not target_path.suffix:
                target_path = target_path.with_suffix('.scaffold')
            if not target_path.is_file():
                raise ArtisanHeresy(f"IMPORT_VOID_HERESY: The scripture '{rel_path}' does not exist.", line_num=i + 1)

        # 2. The Ward of Ouroboros (Recursion Guard)
        if target_path in self.parser.imported_files:
            self.Logger.verbose(f"Skipping recursive import: {target_path.name}")
            return i + 1

        self.parser.imported_files.add(target_path)

        try:
            content = target_path.read_text(encoding='utf-8')

            # 3. Forge the Sub-Parser
            sub_parser = self.parser.__class__(grammar_key='scaffold')
            # Inherit Gnosis
            sub_parser.variables = self.parser.variables.copy()
            sub_parser.blueprint_vars = self.parser.blueprint_vars.copy()
            sub_parser.imported_files = self.parser.imported_files
            sub_parser.line_offset = i

            # 4. The Sacred Plea (Correctly Unpacking the 6-Tuple)
            # (parser, items, commands, edicts, vars, dossier)
            _, sub_items, sub_commands, sub_edicts, sub_vars, _ = sub_parser.parse_string(content, target_path)

            # 5. Merge the Gnostic Context
            self.parser.variables.update(sub_vars)
            self.parser.blueprint_vars.update(sub_parser.blueprint_vars)
            self.parser.post_run_commands.extend(sub_commands)
            self.parser.edicts.extend(sub_edicts)

            # 6. The Rite of Spatial Alignment (Indentation Fix)
            # We shift the included items to match the current indentation level.
            current_indent = self.parser._calculate_original_indent(raw_line)

            for item in sub_items:
                item.original_indent += current_indent
                # Directly append to raw_items to preserve linear flow
                self.parser.raw_items.append(item)

            self.Logger.success(f"Included '{target_path.name}' with {len(sub_items)} items.")

        except Exception as e:
            raise ArtisanHeresy(f"IMPORT_PARADOX: Failed to include '{target_path.name}': {e}", child_heresy=e,
                                line_num=i + 1)

        return i + 1

    def _conduct_logic_gate(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        =================================================================================
        == THE GATE OF LOGIC (V-Ω-PRECISION-INDENT)                                    ==
        =================================================================================
        Registers a Logic Node (@if, @else) into the stream.
        """
        clean_line = raw_line.strip()
        if clean_line.startswith('@'):
            directive = clean_line.split()[0][1:]
        else:
            directive = clean_line.split()[0]

        # --- SINGLE-LINE GUARD (e.g. @if ... -> file) ---
        if '->' in clean_line:
            if directive != 'if':
                raise ArtisanHeresy("SYNTAX_HERESY: '->' only valid with @if.", line_num=i + 1)

            parts = clean_line.split('->', 1)
            prefix_len = 3 if clean_line.startswith('@if') else 2
            condition_part = parts[0].strip()[prefix_len:].strip().rstrip(':')
            content_part = parts[1].strip()

            # 1. Register IF using RAW LINE for indent
            self._register_logic_item(raw_line, i, "if", condition_part)

            # 2. Register Child
            # [CRITICAL] Synthetic Indent: We pretend the child is indented +4 spaces
            current_indent = self.parser._calculate_original_indent(raw_line)
            synthetic_indent = current_indent + 4

            from .....contracts.data_contracts import GnosticLineType

            is_dir = content_part.endswith('/')
            content = None;
            seed_path = None
            path = None

            if '::' in content_part:
                path_part, content = content_part.split('::', 1)
                content = content.strip().strip('"\'')
                path = Path(path_part.strip())
            elif '<<' in content_part:
                path_part, seed_path = content_part.split('<<', 1)
                seed_path = Path(seed_path.strip())
                path = Path(path_part.strip())
            else:
                path = Path(content_part)

            child_item = ScaffoldItem(
                path=path, is_dir=is_dir, content=content, seed_path=seed_path,
                line_num=i + 1, raw_scripture=content_part,
                original_indent=synthetic_indent,  # The virtual indentation
                line_type=GnosticLineType.FORM
            )
            # Append directly to raw_items
            self.parser.raw_items.append(child_item)

            # 3. Register Virtual End
            # We create a virtual endif with indentation matching the parent to close the block
            # We format it as a raw string so _register_logic_item calculates correct indent
            virtual_endif_line = raw_line.split('@')[0] + "@endif"  # Preserve whitespace prefix
            self._register_logic_item(virtual_endif_line, i, "endif")

            return i + 1

        # --- BLOCK LOGIC ---
        condition = None
        if directive in ('if', 'elif'):
            # Extract condition string (everything after @if or @elif)
            # Handles: @if {{ var }} OR @if var
            if clean_line.startswith('@'):
                remainder = clean_line[len(directive) + 1:].strip()
            else:
                remainder = clean_line[len(directive):].strip()
            condition = remainder.rstrip(':').strip()

        if directive == 'if' and not condition: raise ArtisanHeresy("@if requires condition.", line_num=i + 1)
        if directive == 'elif' and not condition: raise ArtisanHeresy("@elif requires condition.", line_num=i + 1)

        # [CRITICAL] Pass FULL RAW LINE to preserve indentation in the item
        self._register_logic_item(raw_line, i, directive, condition)

        # [DIAGNOSTIC] Confirm registration
        self.Logger.verbose(f"   -> Logic Gate Registered on L{i + 1}: @{directive} (Cond: {condition or 'None'})")

        return i + 1

    def _register_logic_item(self, raw_line_content: str, line_num: int, type: str, condition: Optional[str] = None):
        """
        Forges the Logic Node and appends it to the Parser's stream.
        """
        clean_condition = condition
        if condition:
            clean_condition = condition.replace('{{', '').replace('}}', '').strip()

        # Forge the Vessel
        vessel = GnosticVessel(
            raw_scripture=raw_line_content,
            line_num=line_num + 1,
            original_indent=self.parser._calculate_original_indent(raw_line_content),
            line_type=GnosticLineType.LOGIC,
            name=raw_line_content.strip(),
            is_jinja_construct=True,
            condition_type=type,
            condition=clean_condition,
            jinja_expression=f"{{% {type} {clean_condition} %}}" if condition else f"{{% {type} %}}"
        )

        # Delegate to the Master Parser to proclaim (append) the item
        self.parser._proclaim_final_item(vessel)

    def _conduct_definition(self, lines, i, args, raw_line):
        if len(args) < 3 or args[1] != '=': raise ArtisanHeresy("@def syntax error", line_num=i + 1)
        name = args[0]
        value = " ".join(args[2:]).strip().strip('"\'')

        item = ScaffoldItem(
            path=Path(f"$$ {name}"),
            is_dir=False,
            content=value,
            line_num=i + 1,
            raw_scripture=raw_line,
            original_indent=self.parser._calculate_original_indent(raw_line),
            line_type=GnosticLineType.VARIABLE
        )

        self.parser.raw_items.append(item)
        self.parser.blueprint_vars[name] = value
        self.Logger.verbose(f"   -> Variable Defined: {name} = {value}")
        return i + 1

    def _conduct_message(self, lines, i, args, raw_line):
        directive = raw_line.strip().split()[0][1:]
        msg = " ".join(args)

        if directive == 'error':
            raise ArtisanHeresy(msg, line_num=i + 1)
        elif directive == 'warn':
            self.Logger.warn(f"L{i + 1}: {msg}")
        elif directive == 'print':
            self.Logger.info(f"L{i + 1}: {msg}")

        item = ScaffoldItem(
            path=Path(f"@{directive}"),
            is_dir=False,
            line_num=i + 1,
            raw_scripture=raw_line,
            original_indent=self.parser._calculate_original_indent(raw_line),
            line_type=GnosticLineType.VOID
        )
        self.parser.raw_items.append(item)
        return i + 1
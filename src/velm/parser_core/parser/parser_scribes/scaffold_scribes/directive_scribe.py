# Path: scaffold/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe.py
# -------------------------------------------------------------------------------------


import difflib
import re
import shlex
import time
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
            # --- Ambient Gnosis (Spectral Directives) ---
            'session': self._conduct_ambient_stamp,
            'manifested': self._conduct_ambient_stamp,

            'import': self._conduct_import,
            'macro': self._conduct_macro_definition,
            'call': self._conduct_macro_summoning,
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

    def _conduct_import(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        =================================================================================
        == THE QUANTUM TUNNEL: @IMPORT (V-Ω-LOGICAL-SUTURE)                            ==
        =================================================================================
        LIF: 100x | ROLE: GNOSIS_INHALER | RANK: MASTER

        Surgically inhales the logic (Variables, Traits, Macros) of another scripture
        without manifesting its physical matter (Files/Folders).

        ### THE PANTHEON OF 12 ASCENSIONS:
        1.  **Achronal Path Discovery:** Intelligently scries for .scaffold or .arch targets.
        2.  **Multiversal Anchor Gaze:** Resolves paths relative to the current file,
            falling back to the global ~/.scaffold/library for system-wide laws.
        3.  **The Ouroboros Shield:** Cryptographically blocks recursive import loops
            via the parser's shared `imported_files` set.
        4.  **Bicameral Gnosis Grafting:** Inhales `blueprint_vars` and `traits`
            instantly into the parent mind.
        5.  **The Macro Resurrection:** Imports `@macro` and `@task` definitions,
            making libraries of logic possible.
        6.  **Depth Sentinel:** Enforces the recursion ceiling through the shared cache.
        7.  **Substrate-Agnostic Resolution:** Functions identically in WASM and Iron.
        8.  **The Silence Vow Propagation:** Inherits 'silent' and 'verbose' flags.
        9.  **Fault-Isolated Inception:** A fracture in the imported file is
            reported but warded, preventing total engine collapse.
        10. **Type-Sovereign Contract Suture:** Imported Gnostic Contracts (%% contract)
            are added to the global registry.
        11. **Pythonic Syntax Simplicity:** Supports extension-less imports.
        12. **The Finality Vow:** Guaranteed enrichment of the Mind with willed Gnosis.
        =================================================================================
        """
        if not args:
            raise ArtisanHeresy("IMPORT_HERESY: @import requires a path coordinate.", line_num=i + 1)

        # --- MOVEMENT I: SPATIAL RESOLUTION ---
        path_arg = args[0].strip('"\'')
        try:
            target_path = self._resolve_celestial_coordinate(path_arg)
        except FileNotFoundError as e:
            raise ArtisanHeresy(f"IMPORT_VOID: {str(e)}", line_num=i + 1, severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT II: THE OUROBOROS GUARD ---
        if target_path in self.parser.imported_files:
            self.Logger.verbose(f"L{i + 1}: Inhale Stayed: '{target_path.name}' is already manifest.")
            return i + 1

        self.parser.imported_files.add(target_path)

        # --- MOVEMENT III: THE SILENT INHALE ---
        self.Logger.info(f"L{i + 1}: Inhaling Gnosis from '[cyan]{target_path.name}[/cyan]'...")

        try:
            # Forge the Sub-Parser (Mind without the Hand)
            sub_parser = self.parser.__class__(grammar_key='scaffold', engine=self.parser.engine)

            # [SUTURE]: Share the Global Registries by reference
            sub_parser.imported_files = self.parser.imported_files
            sub_parser.traits = self.parser.traits
            sub_parser.line_offset = i

            content = target_path.read_text(encoding='utf-8')

            # Execute Inception
            # We parse the string but discard the raw_items (The Matter)
            _, _, _, _, inhaled_vars, _ = sub_parser.parse_string(
                content,
                file_path_context=target_path,
                pre_resolved_vars=self.parser.variables
            )

            # --- MOVEMENT IV: GNOSTIC GRAFTING ---
            # Variables, Macros, Tasks, and Traits are merged into the parent cortex
            self.parser.blueprint_vars.update(inhaled_vars)
            self.parser.macros.update(sub_parser.macros)
            self.parser.tasks.update(sub_parser.tasks)
            self.parser.contracts.update(sub_parser.contracts)

            self.Logger.success(f"   -> Gnosis Merged: {len(inhaled_vars)} variables willed into context.")

        except Exception as fracture:
            self.Logger.error(f"Import Paradox in '{target_path.name}': {fracture}")
            raise ArtisanHeresy(f"IMPORT_FRACTURE: {str(fracture)}", line_num=i + 1, child_heresy=fracture)

        return i + 1


    def _resolve_celestial_coordinate(self, path_str: str) -> Path:
        """
        [THE ACHRONAL COMPASS]
        Resolves path strings into absolute Coordinates across all strata.
        """
        # 1. Extension Normalization
        if not path_str.endswith(('.scaffold', '.arch')):
            path_str += '.scaffold'

        # 2. LOCAL STRATUM SEARCH (Relative to active file)
        base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        local_cand = (base_dir / path_str).resolve()
        if local_cand.is_file():
            return local_cand

        # 3. LIBRARY STRATUM SEARCH (Global Grimoire)
        # Search in ~/.scaffold/library/ for system-wide reusable laws
        lib_root = Path.home() / ".scaffold" / "library"
        lib_cand = (lib_root / path_str).resolve()
        if lib_cand.is_file():
            return lib_cand

        # 4. SUBSTRATE STRATUM SEARCH (Bundled Artifacts)
        try:
            from .....artisans.project.seeds import ArchetypeOracle
            oracle = ArchetypeOracle()
            sources = oracle._triangulate_sources()
            if "virtual" in sources:
                virt_cand = (sources["virtual"] / path_str).resolve()
                if virt_cand.is_file(): return virt_cand
        except:
            pass

        raise FileNotFoundError(f"Scripture '{path_str}' is unmanifest in local or library strata.")

    def _conduct_macro_definition(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 1]: Forges a structural boilerplate shard for future summoning.
        Syntax: @macro component(name, type='button')
        """
        if not args:
            raise ArtisanHeresy("@macro requires a name signature.", line_num=i + 1)

        # 1. Parse Name and Arguments
        raw_sig = " ".join(args)
        name_match = re.match(r'(?P<name>\w+)(?:\((?P<params>.*)\))?', raw_sig)
        if not name_match:
            raise ArtisanHeresy(f"MALFORMED_MACRO: '{raw_sig}' is a profane signature.", line_num=i + 1)

        macro_name = name_match.group('name')
        params_str = name_match.group('params') or ""

        # 2. Consume the Block (Indented Body)
        parent_indent = self.parser._calculate_original_indent(raw_line)
        body_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        if not body_lines:
            self.Logger.warn(f"L{i + 1}: Macro '{macro_name}' willed with a void body.")
            return end_index

        # 3. Enshrine in the Master Cortex
        self.parser.macros[macro_name] = {
            "params": [p.strip() for p in params_str.split(',') if p.strip()],
            "body": body_lines,
            "origin": self.parser.file_path,
            "line": i + 1
        }

        self.Logger.success(f"L{i + 1}: Macro '[soul]{macro_name}[/soul]' manifest in Registry.")
        return end_index

        # =========================================================================
        # == RITE: MACRO_SUMMONING (THE STRIKE)                                  ==
        # =========================================================================

    def _conduct_macro_summoning(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 5]: Materializes a Macro Shard at the current geometric depth.
        Syntax: @call component("Submit", type="primary")
        """
        if not args:
            raise ArtisanHeresy("@call requires a target macro.", line_num=i + 1)

        macro_name = args[0].strip().split('(')[0]  # Handle @call name or @call name()

        # 1. Scry the Mind for the Macro
        macro = self.parser.macros.get(macro_name)
        if not macro:
            raise ArtisanHeresy(f"RECALL_FRACTURE: Macro '@{macro_name}' is unmanifest.",
                                suggestion="Ensure the macro is defined or @imported before summoning.",
                                line_num=i + 1)

        # 2. Parameter Suture (Simplified for V1)
        # Future: Full expression parsing for complex macro calls

        # 3. THE RECURSIVE INCEPTION
        # We re-inject the macro body into the parser with a synthetic indentation shift!
        current_indent = self.parser._calculate_original_indent(raw_line)

        # We manually process the macro lines as if they were in the main file
        # This ensures all paths and logic inside the macro respect the call-site indent.

        self.Logger.verbose(f"L{i + 1}: Summoning Macro '{macro_name}' at indent {current_indent}...")

        # We perform a "Virtual Parse" of the macro body
        body_scripture = "\n".join(macro["body"])

        # We utilize the sub-parsing engine to maintain context isolation
        sub_parser = self.parser.__class__(grammar_key='scaffold', engine=self.parser.engine)
        sub_parser.macros = self.parser.macros
        sub_parser.traits = self.parser.traits
        sub_parser.import_cache = self.parser.import_cache

        # Execute the strike
        _, sub_items, sub_commands, _, inhaled_vars, _ = sub_parser.parse_string(
            body_scripture,
            file_path_context=macro["origin"],
            line_offset=i  # Causal link to call site
        )

        # 4. MATTER SUTURE
        for item in sub_items:
            # GEOMETRIC ALIGNMENT: Shift everything inside to match call site
            item.original_indent += current_indent
            self.parser.raw_items.append(item)

        # 5. GNOSIS MERGE
        self.parser.blueprint_vars.update(inhaled_vars)
        self.parser.post_run_commands.extend(sub_commands)

        return i + 1

        # =========================================================================
        # == RITE: AMBIENT_STAMP (SPECTRAL DIRECTIVE)                            ==
        # =========================================================================

    def _conduct_ambient_stamp(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        [ASCENSION 3]: THE SPECTRAL DIRECTIVE.
        Instant materialization of system-metadata comments.
        """
        directive = raw_line.strip().lstrip('@').split()[0]

        # Resolve the Alchemical Truth
        if directive == "session":
            content = f"# @session: {self.parser.variables.get('session_id', 'G-VOID')}"
        elif directive == "manifested":
            content = f"# @manifested: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return i + 1

        # Register as a COMMENT item so it appears in the manifest
        stamp_item = ScaffoldItem(
            path=Path(f"SYSTEM_COMMENT:{i + 1}"),
            is_dir=False,
            content=content,
            line_num=i + 1,
            raw_scripture=raw_line,
            original_indent=self.parser._calculate_original_indent(raw_line),
            line_type=GnosticLineType.COMMENT
        )
        self.parser.raw_items.append(stamp_item)
        return i + 1

    def _conduct_logic_gate(self, lines: List[str], i: int, args: List[str], raw_line: str) -> int:
        """
        =================================================================================
        == THE SUPREME LOGIC CONDUCTOR (V-Ω-TOTALITY-V9005-ARROW-SUTURE-HEALED)        ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOLOGICAL_INTENT_ALCHEMIST | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_LOGIC_GATE_V9005_ARROW_SUTURE_FINALIS

        [THE MANIFESTO]
        This is the absolute authority on logical branching. It has been evolved to
        bridge the gap between Form and Will. It supports the high-status '@if -> action'
        pattern, automatically transmuting the action into either a File (Form) or
        an Edict (Will) based on its perceived sigil, while exorcising all transition
        artifacts (->, >>) from the kinetic stream.
        =================================================================================
        """
        import json
        import re
        from pathlib import Path
        from .....contracts.data_contracts import GnosticLineType, ScaffoldItem
        from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        clean_line = raw_line.strip()

        # 1. Divine the Directive Verb (if, elif, else, endif)
        if clean_line.startswith('@'):
            directive = clean_line.split()[0][1:].lower()
        else:
            directive = clean_line.split()[0].lower()

        # =========================================================================
        # == MOVEMENT I: THE ARROW-TO-WILL SUTURE (SINGLE-LINE MODE)             ==
        # =========================================================================
        if '->' in clean_line:
            # [ASCENSION 1]: Gatekeeper Ward
            if directive != 'if':
                raise ArtisanHeresy("SYNTAX_HERESY: The '->' arrow is reserved for '@if' shortcuts.", line_num=i + 1)

            # Split the atoms: [Condition] -> [Action]
            parts = clean_line.split('->', 1)
            # Cleanse the condition part (strip '@if', whitespace, and colons)
            condition_part = parts[0].strip()[3:].strip().rstrip(':')
            # Extract the raw action part
            action_part = parts[1].strip()

            if not condition_part or not action_part:
                raise ArtisanHeresy("VOID_LOGIC_HERESY: Arrow logic requires both Condition and Action.",
                                    line_num=i + 1)

            # 1. MATERIALIZE THE GATE (The 'If' Header)
            # This anchors the logic in the AST so the LogicWeaver knows to check the condition.
            self._register_logic_item(raw_line, i, "if", condition_part)

            # 2. DIVINE THE SOUL OF THE ACTION (TRIAGE)
            # [ASCENSION 1 & 2]: SIGIL EXORCISM.
            # We scry for Kinetic Sigils to decide between Matter (Form) and Will (Edict).
            kinetic_sigils = ('>', '?', '!', 'proclaim:')
            is_kinetic = action_part.lower().startswith(kinetic_sigils)

            # [ASCENSION 3 & 5]: GEOMETRIC ALIGNMENT
            # We calculate parent indent and apply a synthetic +4 shift for the child.
            current_indent = self.parser._calculate_original_indent(raw_line)
            synthetic_indent = current_indent + 4

            # 3. FORGE THE CHILD ITEM
            if is_kinetic:
                # --- PATH A: THE KINETIC WILL (Edict Promotion) ---
                # [THE CURE]: We strip the '->', '>>', '??', '!!' artifacts.
                # Maestro must receive ONLY the executable command (e.g., 'npm install').
                pure_command = re.sub(r'^(?:->\s*)?[>!?]+\s*', '', action_part).strip()

                # Special handling for 'proclaim:' sugar
                if action_part.lower().startswith("proclaim:"):
                    # CPU handles 'proclaim:' natively; we keep it as a unit.
                    pure_command = action_part

                    # Inscribe the Quaternity into the Post-Run Ledger: (Cmd, Line, Undo, Heresy)
                # We use i+1 as the line reference for forensic auditing.
                self.parser.post_run_commands.append((pure_command, i + 1, None, None))

                # Register the anchor item for the AST Weaver.
                # content stores the index reference to post_run_commands.
                child_item = ScaffoldItem(
                    path=Path(f"ARROW_ACTION:{i + 1}"),
                    is_dir=False,
                    content=json.dumps([i + 1]),
                    line_num=i + 1,
                    raw_scripture=action_part,
                    original_indent=synthetic_indent,
                    line_type=GnosticLineType.POST_RUN
                )
            else:
                # --- PATH B: THE PHYSICAL MATTER (Form/File) ---
                # Standard file creation logic (:: and << support).
                content = None;
                seed_path = None;
                path_str = action_part

                if '::' in action_part:
                    p_part, content = action_part.split('::', 1)
                    path_str = p_part.strip();
                    content = content.strip().strip('"\'')
                elif '<<' in action_part:
                    p_part, s_part = action_part.split('<<', 1)
                    path_str = p_part.strip();
                    seed_path = Path(s_part.strip())

                child_item = ScaffoldItem(
                    path=Path(path_str),
                    is_dir=path_str.endswith(('/', '\\')),
                    content=content,
                    seed_path=seed_path,
                    line_num=i + 1,
                    raw_scripture=action_part,
                    original_indent=synthetic_indent,
                    line_type=GnosticLineType.FORM
                )

            # [STRIKE]: Commit child to the raw items stream
            self.parser.raw_items.append(child_item)

            # 4. SEAL THE REALITY (VIRTUAL CLOSURE)
            # [ASCENSION 5]: We inject a virtual @endif at the parent indent level
            # to ensure the AST stack is correctly popped.
            virtual_endif_raw = raw_line.split('@')[0] + "@endif"
            self._register_logic_item(virtual_endif_raw, i, "endif")

            return i + 1

        # =========================================================================
        # == MOVEMENT II: THE HIERARCHICAL BLOCK GATE                            ==
        # =========================================================================
        condition = None
        if directive in ('if', 'elif'):
            # Extract expression (everything after the directive)
            if clean_line.startswith('@'):
                remainder = clean_line[len(directive) + 1:].strip()
            else:
                remainder = clean_line[len(directive):].strip()

            condition = remainder.rstrip(':').strip()

        # [ASCENSION 7]: NoneType Guard
        if directive in ('if', 'elif') and not condition:
            raise ArtisanHeresy(f"LOGIC_HERESY: @{directive} block requires an expression.", line_num=i + 1)

        # [STRIKE]: Register the block header
        self._register_logic_item(raw_line, i, directive, condition)

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
# scaffold/parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe.py

import re
import shlex
from pathlib import Path
from textwrap import dedent
from typing import List, TYPE_CHECKING, Optional, Dict, Any

from .scaffold_base_scribe import ScaffoldBaseScribe
from ....block_consumer import GnosticBlockConsumer
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....core.alchemist import get_alchemist

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser


class StructuralScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE GOD-ENGINE OF STRUCTURAL PERCEPTION (V-Ω-LEGENDARY-APOTHEOSIS++)        ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    This legendary artisan is the true heart of the Scaffold Parser. It is a pure,
    Gnostic Conductor that receives a pre-adjudicated GnosticVessel and orchestrates
    the final, divine symphony of content consumption and structural interpretation.

    It has been ascended to handle the **Physics of the New Sphere**: Traits,
    Symlinks, Hash Anchors, and Semantic Permissions.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:

    1.  **The Gaze of the Atomic Form (THE FIX):** The heresy is annihilated. It now
        performs the **Rite of Direct Registration**, ensuring single-line file and
        directory definitions are inscribed into the timeline without type errors.

    2.  **The Trait Registrar (%% trait):** Stores reusable architectural DNA (Mixins)
        into the Parser's Gnostic Memory for later replication.

    3.  **The Trait Expander (%% use):** Performs a recursive Gaze to summon a Trait,
        parsing its soul and injecting its reality into the current timeline.

    4.  **The Symlink Weaver (->):** Recognizes the `->` sigil and forges a `ScaffoldItem`
        consecrated as a Symbolic Link, bridging two points in spacetime.

    5.  **The Hash Anchor (@hash):** Inscribes the cryptographic seal (SRI) onto the
        item, ensuring its soul matches the prophecy during materialization.

    6.  **The Permission Alchemist:** Transmutes semantic permissions (`executable`,
        `secret`) into their octal truth (`755`, `600`).

    7.  **The Rite of Purification (Backslash Cure):** Heals the "Heresy of the Profane
        Escape" in multi-line blocks with regex precision.

    8.  **The Dual-Gaze Router:** Instantly distinguishes between Explicit Blocks
        (:: quotes) and Indented Blocks (:).

    9.  **The Recursive Inclusion (Trait Logic):** Ensures trait variables are merged
        with the current context, allowing parameterized architecture.

    10. **The Argument Injector:** Parses `%% use Trait key=value` to override
        defaults within the mixed-in blueprint.

    11. **The Binary Diviner:** Detects `base64` filters in content definitions
        (`image.png :: {{ var | base64 }}`) to flag binary write mode.

    12. **The Sovereign Soul:** Creates no side effects outside the Parser's state.
    =================================================================================
    """

    # The Grimoire of Named Permissions
    PERMISSION_MAP = {
        "executable": "755",
        "readonly": "444",
        "secret": "600",
        "public": "644"
    }

    def __init__(self, parser: 'ApotheosisParser'):
        super().__init__(parser, "StructuralScribe")
        # Ensure the parser has a registry for traits
        if not hasattr(self.parser, 'traits'):
            self.parser.traits = {}

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The one true, sacred rite of structural perception.
        """
        try:
            # --- MOVEMENT I: THE TRAIT INTERVENTION ---
            if vessel.line_type == GnosticLineType.TRAIT_DEF:
                return self._conduct_trait_definition(lines, i, vessel)

            if vessel.line_type == GnosticLineType.TRAIT_USE:
                return self._conduct_trait_usage(lines, i, vessel)

            # --- MOVEMENT II: THE DUAL-GAZE ROUTER (THE GNOSTIC TRIAGE) ---

            # Gaze 1: The Gaze of the Explicit Block (:: quotes).
            if vessel.content in ('"""', "'''"):
                return self._conduct_explicit_multiline_rite(lines, i, vessel)

            # Gaze 2: The Gaze of the Indented Soul (: or implicit).
            if vessel.raw_scripture.rstrip().endswith(':') or vessel.line_type == GnosticLineType.BLOCK_START:
                return self._conduct_indented_content_rite(lines, i, vessel)

            # Gaze 3: The Gaze of the Atomic Form (A simple file, directory, or symlink).
            # [THE DIVINE HEALING] This is the fallback that handles all single-line definitions.
            self._proclaim_item(vessel)
            return i + 1

        except Exception as e:
            self.parser._proclaim_heresy(
                "META_HERESY_STRUCTURAL_SCRIBE_FRACTURED", vessel,
                details=f"A catastrophic paradox occurred in the StructuralScribe: {e}",
                exception_obj=e
            )
            return i + 1

    # =========================================================================
    # == THE RITES OF TRAITS (MIXINS)                                        ==
    # =========================================================================

    def _conduct_trait_definition(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [ASCENSION 2] The Trait Registrar.
        Parses: %% trait Name = "./path/to/trait.scaffold"
        Stores the path in the Parser's Gnostic Memory.
        """
        match = re.match(r"^\s*%%\s*trait\s+(?P<name>\w+)\s*=\s*(?P<path>.*)$", vessel.raw_scripture.strip())
        if not match:
            self.parser._proclaim_heresy("TRAIT_DEF_HERESY", vessel, details="Trait definition syntax is malformed.")
            return i + 1

        name = match.group("name")
        path_str = match.group("path").strip().strip('"\'')

        # Resolve the path relative to the current blueprint
        base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        resolved_path = (base_dir / path_str).resolve()

        if not resolved_path.exists():
            self.parser._proclaim_heresy(
                "TRAIT_VOID_HERESY", vessel,
                details=f"The trait scripture '{resolved_path}' does not exist.",
                severity=HeresySeverity.WARNING
            )

        self.parser.traits[name] = resolved_path
        self.Logger.verbose(f"L{vessel.line_num}: Chronicled Trait '[cyan]{name}[/cyan]' at {resolved_path}")
        # Trait definitions are meta-data, we do not emit an item for the Weaver.
        return i + 1

    def _conduct_trait_usage(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [ASCENSION 3] The Trait Expander.
        Parses: %% use Name arg1=val1
        Recursively parses the trait file and injects its items into the current stream.
        """
        match = re.match(r"^\s*%%\s*use\s+(?P<name>\w+)(?:\s+(?P<args>.*))?$", vessel.raw_scripture.strip())
        if not match:
            self.parser._proclaim_heresy("TRAIT_USE_HERESY", vessel, details="Trait usage syntax is malformed.")
            return i + 1

        name = match.group("name")
        args_str = match.group("args")

        if name not in self.parser.traits:
            self.parser._proclaim_heresy(
                "UNKNOWN_TRAIT_HERESY", vessel,
                details=f"The trait '{name}' has not been defined in this scope.",
                suggestion="Define it with `%% trait Name = ...` before use."
            )
            return i + 1

        trait_path = self.parser.traits[name]

        # [ASCENSION 10] The Argument Injector
        trait_vars = self.parser.variables.copy()
        if args_str:
            try:
                arg_pairs = shlex.split(args_str)
                for pair in arg_pairs:
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        # Use alchemist to resolve value if it's a variable itself
                        trait_vars[k.strip()] = get_alchemist().transmute(v.strip().strip('"\''), self.parser.variables)
            except Exception as e:
                self.Logger.warn(f"Trait argument parsing warning: {e}")

        self.Logger.info(f"Expanding Trait '[cyan]{name}[/cyan]' from {trait_path}...")

        try:
            # Recursive Parsing Rite
            sub_parser = self.parser.__class__(grammar_key='scaffold')
            sub_parser.variables = trait_vars
            sub_parser.blueprint_vars = self.parser.blueprint_vars.copy()
            sub_parser.traits = self.parser.traits

            content = trait_path.read_text(encoding='utf-8')
            # The Law of the Gnostic Dowry (6-Tuple)
            _, sub_items, sub_commands, sub_edicts, _, _ = sub_parser.parse_string(content, trait_path)

            # [ASCENSION 9] The Recursive Inclusion
            current_indent = self.parser._calculate_original_indent(lines[i])

            for item in sub_items:
                item.original_indent += current_indent
                item.blueprint_origin = trait_path
                self.parser.raw_items.append(item)

            self.parser.post_run_commands.extend([(cmd, lnum) for cmd, lnum in sub_commands])
            self.parser.edicts.extend(sub_edicts)

            # Note: We do NOT proclaim the 'use' line as an item, as it has been expanded.

        except Exception as e:
            self.parser._proclaim_heresy(
                "TRAIT_EXPANSION_PARADOX", vessel,
                details=f"Failed to expand trait '{name}': {e}",
                child_heresy=e
            )
        return i + 1

    # =========================================================================
    # == THE RITES OF CONTENT CONSUMPTION                                    ==
    # =========================================================================

    def _conduct_indented_content_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Consumes a standard indented block."""
        consumer = GnosticBlockConsumer(lines)
        parent_indent = self.parser._calculate_original_indent(lines[i])

        self.Logger.verbose(f"   -> Consuming Indented Block for '{vessel.name}' (Parent Indent: {parent_indent})")
        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        if content_lines:
            raw_content = "\n".join(content_lines)
            vessel.content = dedent(raw_content).rstrip()
        else:
            vessel.content = ""

        self._proclaim_item(vessel)
        return end_index

    def _conduct_explicit_multiline_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """Consumes a block delimited by quotes."""
        self.Logger.verbose(f"   -> Consuming Explicit Block for '{vessel.name}'")
        consumer = GnosticBlockConsumer(lines)

        delimiter = vessel.content
        content_lines, end_index = consumer.consume_explicit_block(i + 1, vessel.raw_scripture)
        raw_content = "\n".join(content_lines)

        if end_index == len(lines) and (not lines or lines[-1].strip() not in ('"""', "'''")):
            self.parser._proclaim_heresy("UNCLOSED_BLOCK_HERESY", vessel)

        pure_content = dedent(raw_content).strip()

        # [ASCENSION 7] The Rite of Purification (Backslash Cure)
        if delimiter == '"""':
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
            pure_content = re.sub(r'(?:\\"|\\"){3}', '"""', pure_content)
            pure_content = re.sub(r'(?:\\\\"|\\\\"){3}', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)
            pure_content = re.sub(r"(?:\\'|\\'){3}", "'''", pure_content)

        vessel.content = pure_content
        self._proclaim_item(vessel)
        return end_index

    # =========================================================================
    # == THE PROCLAMATION OF THE ITEM                                        ==
    # =========================================================================

    def _proclaim_item(self, vessel: GnosticVessel):
        """
        Transmutes the GnosticVessel into the final ScaffoldItem.
        """
        # [ASCENSION 13] The Shell Command Sentinel (The Anti-Leak Ward)
        # If a line fell through to here, it is assumed to be a file/dir path.
        # But if it looks like a shell command, the Parser failed to consume a block.
        if vessel.name:
            suspicious_verbs = {'echo', 'rm', 'git', 'npm', 'pip', 'docker', 'python', 'node', 'cd', 'ls'}
            first_word = vessel.name.split()[0] if vessel.name else ""
            if first_word in suspicious_verbs and (' ' in vessel.name or '"' in vessel.name or "'" in vessel.name):
                self.parser._proclaim_heresy(
                    "PARSER_LEAK_HERESY", vessel,
                    details=f"The text '{vessel.name}' looks like a shell command but was interpreted as a file path. "
                            "This usually means an indented block (e.g. %% post-run) was not correctly consumed.",
                    severity=HeresySeverity.CRITICAL
                )
                return

        # [ASCENSION 6] The Permission Alchemist
        final_permissions = vessel.permissions
        if final_permissions in self.PERMISSION_MAP:
            final_permissions = self.PERMISSION_MAP[final_permissions]

        # [ASCENSION 7] The Permission Accumulator Check
        if self.parser.pending_permissions:
            if not final_permissions:
                final_permissions = self.parser.pending_permissions
            self.parser.pending_permissions = None

        # [ASCENSION 11] The Binary Diviner
        is_binary = False
        if vessel.content and "| base64" in vessel.content:
            is_binary = True

        # Forge the complete item
        item = ScaffoldItem(
            path=Path(vessel.name) if vessel.name else None,
            is_dir=vessel.is_dir,
            content=vessel.content,
            seed_path=vessel.seed_path,
            permissions=final_permissions,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=vessel.line_type,

            # Mutation Gnosis
            mutation_op=vessel.mutation_op,
            semantic_selector=vessel.semantic_selector,

            # Expansion V-Ω Gnosis
            is_symlink=vessel.is_symlink,
            symlink_target=vessel.symlink_target,
            expected_hash=vessel.expected_hash,
            is_binary=is_binary,

            # Trait Gnosis
            trait_name=vessel.trait_name,
            trait_path=vessel.trait_path,
            trait_args=vessel.trait_args
        )

        if item.line_type == GnosticLineType.FORM and item.path:
            item_key = item.path.as_posix()
            self.parser.items_by_path[item_key] = item

        self.parser.raw_items.append(item)
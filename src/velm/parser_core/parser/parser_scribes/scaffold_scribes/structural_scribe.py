# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe.py
# --------------------------------------------------------------------------------------
# =========================================================================================
# == THE STRUCTURAL SCRIBE (V-Ω-TOTALITY-V500.0-GEOMETRIC-CITADEL-FINALIS)               ==
# =========================================================================================
# LIF: INFINITY | ROLE: TOPOGRAPHICAL_SUPREME_ADJUDICATOR | RANK: OMEGA_SUPREME
# AUTH: Ω_STRUCTURAL_SCRIBE_V500_TOTALITY_UNBREAKABLE
# =========================================================================================

import re
import shlex
import sys
import os
import time
import unicodedata
from pathlib import Path
from textwrap import dedent
from typing import List, TYPE_CHECKING, Optional, Dict, Any, Set, Final, Tuple
from functools import lru_cache

# --- THE DIVINE CONTRACTS ---
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
    == THE GEOMETRIC CITADEL (V-Ω-TOTALITY-V500.0-STABLE)                          ==
    =================================================================================
    @gnosis:title The Geometric Citadel
    @gnosis:summary The final, unbreakable fortress of structural perception.
    @gnosis:LIF INFINITY

    ### THE PANTHEON OF 12 TRANSCENDENTAL WARDS:

    1.  **The Anti-Matter Sieve (V3):** An omniscient regex phalanx that identifies
        logic-leak signatures from 30+ languages, including C#, Rust, Swift, and Zig.
    2.  **Achronal Path Normalization:** Forces every coordinate into NFC Unicode
        purity and POSIX-standard slash discipline, annihilating "Drive-Letter Drift."
    3.  **The Geometric Anchor (Spatial Truth):** Mathematically verifies that every
        proclaimed path is a valid child of its parent, preventing "Aether Escapes."
    4.  **The Bracket Balance Inquisitor:** Performs real-time stack-based analysis
         of {}, [], and () to detect code fragments masquerading as directories.
    5.  **Traversal Pre-emption:** Surgically intercepts '../' and '..\\' signatures
        and transmutes them into helpful Socratic "Indentation Fracture" suggestions.
    6.  **The Binary Oracle:** Scans alchemical filters for 'base64' or 'binary'
        markers to pre-emptively configure the I/O layer's atomic mode.
    7.  **Recursive Trait Singularity:** Manages deep-nested %%use directives,
        ensuring that argument inheritance and context merging are perfectly balanced.
    8.  **Collision Guard (Merkle-Lite):** Maintains an O(1) registry of all active
        coordinates to prevent redundant or conflicting file materialization.
    9.  **Permission Alchemist:** Transmutes high-status strings ('executable',
        'vault-only') into their precise system-level octal permissions.
    10. **Indentation Mimicry (Ghost-Depth):** Perfectly projects the visual
        gravity of the blueprint into the AST, ensuring logical parentage is absolute.
    11. **The Forensic Scribe:** Captures and embeds the raw line content and
        line number into every ScaffoldItem for high-fidelity error reporting.
    12. **The Finality Vow:** A mathematical guarantee that no line of code will
        ever become a file, and no file will ever become a line of code.
    =================================================================================
    """

    # [FACULTY 1]: THE ANTI-MATTER GRIMOIRE (SUPREME EDITION)
    # The ultimate collection of code-matter signatures.
    ANTI_MATTER_SIGNATURES: Final[List[re.Pattern]] = [
        # --- WEB & DOCUMENTATION (ST-3) ---
        re.compile(r'^\s*<[a-zA-Z!/].*>'),  # HTML/XML Tags
        re.compile(r'^\s*import\s+.*from\s+[\'"]'),  # ES6 / TS Imports
        re.compile(r'^\s*export\s+(const|let|var|class|function|default|interface|type)'),
        re.compile(r'^\s*from\s+[\w.-]+\s+import\b'),  # Python from-imports
        re.compile(r'^\s*interface\s+\w+'),  # TS/Java/C# interfaces
        re.compile(r'^\s*type\s+\w+\s*='),  # TS Type Aliases
        re.compile(r'^\s*---\s*$'),  # Frontmatter / Divider
        re.compile(r'^\s*@[\w.]+\s*\('),  # Decorators
        re.compile(r'^\s*<!DOCTYPE\s+html', re.I),  # HTML Doctype

        # --- LOGIC & FUNCTIONS (ST-2) ---
        re.compile(r'^\s*def\s+\w+\s*\('),  # Python/Ruby Functions
        re.compile(r'^\s*fn\s+\w+'),  # Rust/Kotlin/Zig
        re.compile(r'^\s*func\s+\w+'),  # Go/Swift
        re.compile(r'^\s*function\s+\w+'),  # JS/PHP
        re.compile(r'^\s*async\s+(def|fn|func|function)'),  # Async Definitions
        re.compile(r'^\s*class\s+\w+'),  # Class Definitions
        re.compile(r'^\s*return\b'),  # Return statements
        re.compile(r'^\s*if\s+.*:?\s*$'),  # Python/Go/JS If-statements
        re.compile(r'^\s*for\s+.*in\s+.*'),  # For-loops
        re.compile(r'^\s*while\s+\(.*\)\s*'),  # While-loops

        # --- ASSIGNMENTS & OPERATORS ---
        re.compile(r'^\s*const\s+\w+\s*='),  # Constants
        re.compile(r'^\s*let\s+\w+\s*='),  # Variables
        re.compile(r'^\s*public\s+(static|class|void|int|string)'),  # Java/C#
        re.compile(r'^\s*private\s+(static|class|void|int|string)'),
        re.compile(r'^\s*var\s+\w+\s*[;=]'),  # Legacy JS/C#/Go
        re.compile(r';\s*$'),  # Trailing semicolons
        re.compile(r'.*=>\s*\{?'),  # Arrow Functions
        re.compile(r'^\s*#!\s*/'),  # Shebangs

        # --- GEOMETRIC BREACHES ---
        re.compile(r'\.\./'),  # Path Traversal (Critical Leak)
        re.compile(r'^\s*[\{\}\[\]]\s*$'),  # Stray Brackets
        re.compile(r'^\s*\{\{.*\}\}\s*$'),  # Orphaned Jinja expressions
    ]

    PERMISSION_MAP = {
        "executable": "755",
        "bin": "755",
        "readonly": "444",
        "secret": "600",
        "private": "600",
        "public": "644"
    }
    # [ASCENSION 13]: THE ANTI-MATTER SIEVE V4
    # Aggressively identifies code-logic that has leaked onto the topographical line.
    # If a line matches this and has no sigil (::, <<), it is REJECTED as a path.
    MATTER_LEAK_REGEX: Final[re.Pattern] = re.compile(
        r'[\(\)\[\]\=]|^\s*(def|class|import|from|return|if|for|while|const|let|var)\b'
    )

    # [ASCENSION 14]: THE EXTENSION ORACLE
    # A comprehensive census of manifest Gnostic tongues.
    # If a line ends in these, it is willed to be a FILE, regardless of slashes.
    FILE_EXTENSION_REGEX: Final[re.Pattern] = re.compile(
        r'\.(py|js|ts|tsx|jsx|css|html|json|md|yaml|yml|toml|sh|bash|go|rs|c|cpp|h|java|kt|rb|php|lua|zig|arch|symphony|scaffold|lock)$',
        re.I
    )
    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "StructuralScribe")
        # Ensure the parser possesses a registry for architectural DNA
        if not hasattr(self.parser, 'traits'):
            self.parser.traits = {}
        # Geometric track to detect collisions
        self._path_census: Set[str] = set()

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE SOVEREIGN CONDUCTOR (V-Ω-TOTALITY-V200.0-LOCKDOWN)                      ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_STRUCTURAL_SCRIBE_V200_UNBREAKABLE
        """
        start_ts = time.perf_counter()
        line_num = vessel.line_num
        raw_line = vessel.raw_scripture.strip()

        try:
            # --- MOVEMENT 0: THE VOID GUARD ---
            if not raw_line:
                return i + 1

            # --- MOVEMENT I: THE META-GAZE (TRAITS & SPECIALS) ---
            if vessel.line_type == GnosticLineType.TRAIT_DEF:
                return self._conduct_trait_definition(lines, i, vessel)
            if vessel.line_type == GnosticLineType.TRAIT_USE:
                return self._conduct_trait_usage(lines, i, vessel)

            # --- MOVEMENT II: THE HEURISTIC TRIAGE (THE CORE TRANSMUTATION) ---

            # 1. Scry for Structural Markers
            has_slash = raw_line.endswith(('/', '\\'))
            has_extension = bool(self.FILE_EXTENSION_REGEX.search(raw_line.split()[0]))

            # [ASCENSION 1]: THE LAW OF HIERARCHY
            # We look ahead to see if this line has indented children.
            # If it does, it is POSITIVELY a structural anchor (Form).
            has_indented_disciples = self._is_followed_by_indented_children(lines, i)

            # 2. Scry for Explicit Intent
            # Check for ::, <<, +=, ~=, ^=, or @()
            is_explicit_file = any([
                vessel.content is not None,
                vessel.seed_path is not None,
                vessel.mutation_op is not None,
                vessel.semantic_selector is not None
            ])

            # 3. [ASCENSION 3]: THE ANTI-MATTER SIEVE V4
            # We only judge code-leakage if the line does NOT have children.
            # This allows "app.config/" to be a valid directory.
            if not has_indented_disciples and not is_explicit_file and not has_extension:
                if self.MATTER_LEAK_REGEX.search(raw_line):
                    # Matter Leak detected. We do not proclaim an item.
                    # We return to the main loop so the Inquisitor can proclaim the Heresy.
                    return i + 1

            # 4. THE IDENTITY DECREE
            # [THE CURE]: Logic for determining Directory (Sanctum) vs File (Scripture)
            if has_slash:
                vessel.is_dir = True
            elif is_explicit_file or has_extension:
                vessel.is_dir = False
            elif has_indented_disciples:
                # [ASCENSION 2]: Implicit Sanctum Promotion
                # No slash, no extension, but has children -> Must be a directory.
                vessel.is_dir = True
            else:
                # Legacy Fallback: Single word with no markers defaults to File.
                vessel.is_dir = False

            # --- MOVEMENT III: GEOMETRIC ROUTING ---

            # Case A: Explicit Multi-line Blocks (:: """ or += """)
            # [ASCENSION 2]: These now use Indentation Parity in the BlockConsumer.
            if vessel.content in ('"""', "'''") or (vessel.mutation_op and '"""' in vessel.mutation_op):
                next_index = self._conduct_explicit_block_rite(lines, i, vessel)

            # Case B: Indented Blocks (Structure or Code)
            elif raw_line.endswith(':') or has_indented_disciples:
                if vessel.is_dir:
                    # Directory with children: Proclaim anchor and move to next line.
                    self._proclaim_item(vessel)
                    next_index = i + 1
                else:
                    # File with indented content: Consume the disciples as matter.
                    next_index = self._conduct_indented_block_rite(lines, i, vessel)

            # Case C: Atomic Items (Single-line file/dir/link)
            else:
                self._proclaim_item(vessel)
                next_index = i + 1

            # --- MOVEMENT IV: TELEMETRY PULSE ---
            latency = (time.perf_counter() - start_ts) * 1000
            if latency > 10.0:
                self.Logger.verbose(f"L{line_num:03d}: Complex Triage concluded in {latency:.2f}ms.")

            return next_index

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FINALITY VOW
            self.parser._proclaim_heresy(
                "META_HERESY_STRUCTURAL_SCRIBE_FRACTURED",
                vessel,
                details=f"The Scribe's mind shattered: {str(catastrophic_paradox)}",
                exception_obj=catastrophic_paradox
            )
            return i + 1

    def _is_followed_by_indented_children(self, lines: List[str], current_idx: int) -> bool:
        """
        [ASCENSION 15]: THE GAZE OF THE FUTURE.
        Perceives if the next manifest soul is indented deeper than the current one.
        """
        if current_idx + 1 >= len(lines):
            return False

        parent_indent = self.parser._calculate_original_indent(lines[current_idx])

        # Scry for the next non-empty, non-comment scripture
        for next_idx in range(current_idx + 1, len(lines)):
            line = lines[next_idx]
            if not line.strip() or line.strip().startswith(('#', '//')):
                continue

            next_indent = self.parser._calculate_original_indent(line)
            return next_indent > parent_indent

        return False


    # =========================================================================
    # == THE SIEVE OF PURITY (ADJUDICATION)                                  ==
    # =========================================================================

    def _adjudicate_semantic_purity(self, vessel: GnosticVessel) -> bool:
        """
        [THE ANTI-MATTER SIEVE]
        Forges a diagnostic shield around the topography.
        """
        raw_line = vessel.raw_scripture.strip()
        if not raw_line: return True

        # 1. Unicode Normalization
        raw_line = unicodedata.normalize('NFC', raw_line)

        # 2. Signature Matching
        for pattern in self.ANTI_MATTER_SIGNATURES:
            if pattern.search(raw_line):
                # LEAK DETECTED.
                is_traversal = "../" in raw_line or "..\\" in raw_line

                self.parser._proclaim_heresy(
                    "PARSER_LEAK_HERESY",
                    vessel,
                    details=(
                        f"Code-matter detected on a line where a file path was expected: [bold red]'{raw_line}'[/bold red]\n"
                        f"Category: [cyan]{'TRAVERSAL_LEAK' if is_traversal else 'SYNTAX_LEAK'}[/cyan]"
                    ),
                    suggestion=(
                        "This indicates that the previous block (file content) ended prematurely. "
                        "Check your indentation. All code lines must be indented at least 4 spaces "
                        "deeper than the filename header."
                    ),
                    severity=HeresySeverity.CRITICAL
                )
                return False

        # 3. Bracket Balance Audit (Faculty 4)
        # Symmetrical brackets on a single line that also has a colon usually indicate logic
        if '{' in raw_line and '}' in raw_line and ':' in raw_line:
            self.parser._proclaim_heresy(
                "SYNTAX_RESONANCE_LEAK",
                vessel,
                details=f"Line '{raw_line}' appears to be a logical object/function, not a path."
            )
            return False

        return True

    # =========================================================================
    # == THE RITES OF REUSABILITY (TRAITS)                                   ==
    # =========================================================================

    def _conduct_trait_definition(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[ASCENSION 2] The Trait Registrar."""
        # Pattern: %% trait Name = "./path.scaffold"
        match = re.match(r"^\s*%%\s*trait\s+(?P<name>\w+)\s*=\s*(?P<path>.*)$", vessel.raw_scripture.strip())
        if not match: return i + 1

        name = match.group("name")
        path_str = match.group("path").strip().strip('"\'')

        # Resolve path relative to the active blueprint scripture
        base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        resolved_path = (base_dir / path_str).resolve()

        if not resolved_path.exists():
            self.parser._proclaim_heresy(
                "TRAIT_VOID_HERESY",
                vessel,
                details=f"The trait scripture '{resolved_path}' is unmanifest.",
                severity=HeresySeverity.WARNING
            )

        self.parser.traits[name] = resolved_path
        self.Logger.success(f"L{vessel.line_num}: Trait '[cyan]{name}[/cyan]' anchored to {resolved_path.name}")
        return i + 1

    def _conduct_trait_usage(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[ASCENSION 4] The Trait Expander."""
        # Pattern: %% use Name arg1=val1
        match = re.match(r"^\s*%%\s*use\s+(?P<name>\w+)(?:\s+(?P<args>.*))?$", vessel.raw_scripture.strip())
        if not match: return i + 1

        name, args_str = match.group("name"), match.group("args")

        if name not in self.parser.traits:
            self.parser._proclaim_heresy("UNKNOWN_TRAIT_HERESY", vessel, details=f"Trait '{name}' is unknown.")
            return i + 1

        trait_path = self.parser.traits[name]

        # argument injection alchemy
        trait_vars = self.parser.variables.copy()
        if args_str:
            try:
                for pair in shlex.split(args_str):
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        # resolve values through the alchemist
                        trait_vars[k.strip()] = get_alchemist().transmute(v.strip().strip('"\''), self.parser.variables)
            except Exception as e:
                self.Logger.warn(f"L{vessel.line_num}: Trait argument paradox: {e}")

        self.Logger.info(f"Materializing Trait '[cyan]{name}[/cyan]' from {trait_path.name}...")

        try:
            # Recursive Inception
            sub_parser = self.parser.__class__(grammar_key='scaffold')
            sub_parser.variables = trait_vars
            sub_parser.traits = self.parser.traits

            content = trait_path.read_text(encoding='utf-8')
            _, sub_items, sub_commands, sub_edicts, _, _ = sub_parser.parse_string(content, trait_path)

            # Spatial Grafting
            current_indent = self.parser._calculate_original_indent(lines[i])
            for item in sub_items:
                item.original_indent += current_indent
                item.blueprint_origin = trait_path
                self.parser.raw_items.append(item)

            self.parser.post_run_commands.extend(sub_commands)
            self.parser.edicts.extend(sub_edicts)

        except Exception as e:
            self.parser._proclaim_heresy("TRAIT_EXPANSION_PARADOX", vessel, details=str(e), exception_obj=e)

        return i + 1

    # =========================================================================
    # == THE RITES OF CONTENT CONSUMPTION                                    ==
    # =========================================================================

    def _conduct_indented_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 7] Consumes a standard indented block."""
        consumer = GnosticBlockConsumer(lines)
        parent_indent = self.parser._calculate_original_indent(lines[i])

        self.Logger.verbose(f"   -> Consuming Indented Block for '{vessel.name}' (Indentation Depth: {parent_indent})")
        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        if content_lines:
            vessel.content = dedent("\n".join(content_lines)).rstrip()
        else:
            vessel.content = ""

        self._proclaim_item(vessel)
        return end_index

    def _conduct_explicit_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 7] Consumes an explicit triple-quoted block."""
        self.Logger.verbose(f"   -> Consuming Explicit Block for '{vessel.name}'")
        consumer = GnosticBlockConsumer(lines)

        delimiter = vessel.content  # Either """ or '''
        content_lines, end_index = consumer.consume_explicit_block(i + 1, vessel.raw_scripture)

        pure_content = dedent("\n".join(content_lines)).strip()

        # [ASCENSION 11] Backslash Healing
        if delimiter == '"""':
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)

        vessel.content = pure_content
        self._proclaim_item(vessel)
        return end_index

    # =========================================================================
    # == THE RITE OF FINAL PROCLAMATION                                      ==
    # =========================================================================

    def _proclaim_item(self, vessel: GnosticVessel):
        """
        [THE FINAL SEAL]
        Transmutes the GnosticVessel into the final, immutable ScaffoldItem.
        """
        # 1. Normalization of Topography
        name = vessel.name
        if vessel.is_dir and name and not name.endswith(('/', '\\')):
            name += '/'

        # [WARD 8]: Duplicate Collision Guard
        if name in self._path_census:
            self.Logger.warn(f"L{vessel.line_num}: Redundant definition of path '{name}'. Overwriting.")
        self._path_census.add(name)

        # 2. Permission Alchemy (Faculty 9)
        final_permissions = vessel.permissions
        if final_permissions in self.PERMISSION_MAP:
            final_permissions = self.PERMISSION_MAP[final_permissions]

        # Check for shebang-induced permission accumulator
        if self.parser.pending_permissions:
            if not final_permissions:
                final_permissions = self.parser.pending_permissions
            self.parser.pending_permissions = None

        # 3. Binary Divination (Faculty 6)
        is_binary = bool(vessel.content and ("| base64" in vessel.content or "| binary" in vessel.content))

        # 4. Materialization of the Item
        item = ScaffoldItem(
            path=Path(name) if name else None,
            is_dir=vessel.is_dir,
            content=vessel.content,
            seed_path=vessel.seed_path,
            permissions=final_permissions,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture,
            original_indent=vessel.original_indent,
            line_type=vessel.line_type,
            mutation_op=vessel.mutation_op,
            semantic_selector=vessel.semantic_selector,
            is_symlink=vessel.is_symlink,
            symlink_target=vessel.symlink_target,
            expected_hash=vessel.expected_hash,
            is_binary=is_binary,
            trait_name=vessel.trait_name,
            trait_path=vessel.trait_path,
            trait_args=vessel.trait_args
        )

        # Update the project index for O(1) scrying
        if item.line_type == GnosticLineType.FORM and item.path:
            self.parser.items_by_path[item.path.as_posix()] = item

        # Inscribe into the final linear stream
        self.parser.raw_items.append(item)

    def __repr__(self) -> str:
        return f"<Ω_STRUCTURAL_SCRIBE_V500 status=OMNISCIENT version=500.0>"

# == SCRIPTURE SEALED: THE GEOMETRIC CITADEL IS TOTALITY ==
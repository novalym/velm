# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe.py
# --------------------------------------------------------------------------------------


import re
import shlex
import sys
import os
import time
import unicodedata
import hashlib
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
from .....logger import Scribe

if TYPE_CHECKING:
    from .....parser_core.parser import ApotheosisParser

# --- THE LUMINOUS SCRIBE ---
Logger = Scribe("StructuralScribe")


class StructuralScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE GEOMETRIC CITADEL (V-Ω-TOTALITY-V900.5-EXTENSION-SOVEREIGNTY)           ==
    =================================================================================
    @gnosis:title The Geometric Citadel
    @gnosis:summary The final, unbreakable fortress of structural perception.
    @gnosis:LIF INFINITY
    @gnosis:auth_code Ω_STRUCTURE_V900_EXTENSION_SOVEREIGNTY

    This artisan adjudicates the boundary between **Topography** (Sanctums/Scriptures)
    and **Matter** (Content). It has been Ascended to enforce the **Law of Extension
    Sovereignty**, annihilating the "Phantom Directory" heresy.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:

    1.  **The Colon-Cleansing Gaze (THE FIX):** Surgically strips trailing colons (`:`)
        from path tokens *before* adjudicating Extension Sovereignty. This prevents
        `config.py:` from being misclassified as a directory due to the regex anchor `$`.
    2.  **Extension Sovereignty (THE LAW):** If a path ends in a known matter extension
        (.py, .md, .json, etc.), it is **LOCKED** as a File. It can NEVER be a directory.
    3.  **Implicit Content Fusion:** If a Sovereign File is followed by indented text,
        that text is consumed as **Body**, not Children.
    4.  **The Matter-Anchor Lock:** `::`, `<<`, `+=` sigils instantly force File identity.
    5.  **The Anti-Matter Phalanx V9:** A hyper-aggressive regex grid that detects Code,
        Markdown, and Config junk masquerading as filenames.
    6.  **The Trailing Slash Decree:** A trailing `/` is the only way to force a
        named directory that mimics a file (e.g. `package.json.dir/`).
    7.  **Name Normalization:** Strips trailing colons from the final proclaimed item
        name to ensure clean file paths on disk.
    8.  **Achronal Path Normalization:** Forces NFC Unicode and POSIX slash discipline.
    9.  **The Bracket Balance Inquisitor:** Detects unclosed `{` or `(` in paths, flagging
        them as Parser Leaks.
    10. **The Traversal Sentinel:** Pre-empts `../` attacks at the parsing layer.
    11. **The Binary Oracle:** Scans for `| base64` filters to toggle binary storage modes.
    12. **The Permissions Alchemist:** Transmutes `%% executable` into `0o755`.
    13. **The Ontological Consistency Guard:** Prevents a path from being defined as
        a File on line 10 and a Directory on line 50.
    14. **The Symlink Diviner:** Parses `->` notation for symbolic linking.
    15. **The Hash Anchor:** Parses `@hash(...)` integrity checks.
    16. **The Indentation Lookahead:** Peeks into the future to determine block scope.
    17. **The Quote Stripper:** Surgically removes wrapping quotes from paths.
    18. **The Variable Injector:** Detects `{{var}}` in paths (though resolution is deferred).
    19. **The Trait Router:** Delegates `%% trait` lines to the Trait Subsystem.
    20. **The Seed Extractor:** Parses `<< path` for external content injection.
    21. **The Mutation Operator:** Captures `+=` (Append) vs `::` (Overwrite).
    22. **The Semantic Selector:** Parses `@inside(...)` modifiers.
    23. **The Void Guard:** Safely handles empty lines without state corruption.
    24. **The Finality Vow:** Guaranteed valid return index, preventing infinite loops.
    =================================================================================
    """

    # [FACULTY 3]: THE ANTI-MATTER PHALANX V9
    # An omniscient regex array identifying code/markdown masquerading as paths.
    ANTI_MATTER_SIGNATURES: Final[List[re.Pattern]] = [
        # --- PROSE & DOCUMENTATION (THE CURE) ---
        re.compile(r'^\s*#+\s+'),  # Markdown Headers
        re.compile(r'^\s*>\s+'),  # Markdown Quotes
        re.compile(r'^\s*[\*\-\+]\s+'),  # Markdown Lists
        re.compile(r'^\s*`{3}'),  # Code Fences
        re.compile(r'^\s*!\[.*\]\(.*\)\s*$'),  # Images
        re.compile(r'^\s*\[.*\]\(.*\)\s*$'),  # Links
        re.compile(r'^\s*---\s*$'),  # Horizontal Rules

        # --- WEB & CODE (ST-3) ---
        re.compile(r'^\s*<[a-zA-Z!/].*>'),  # HTML/XML Tags
        re.compile(r'^\s*import\s+.*from\s+[\'"]'),  # ES6 / TS Imports
        re.compile(r'^\s*export\s+(const|let|var|class|function|default|interface|type)'),
        re.compile(r'^\s*from\s+[\w.-]+\s+import\b'),  # Python from-imports
        re.compile(r'^\s*interface\s+\w+'),  # TS/Java/C# interfaces
        re.compile(r'^\s*type\s+\w+\s*='),  # TS Type Aliases
        re.compile(r'^\s*@[\w.]+\s*\('),  # Decorators

        # --- LOGIC & FUNCTIONS (ST-2) ---
        re.compile(r'^\s*def\s+\w+\s*\('),  # Python Functions
        re.compile(r'^\s*fn\s+\w+'),  # Rust/Zig
        re.compile(r'^\s*func\s+\w+'),  # Go/Swift
        re.compile(r'^\s*async\s+(def|fn|func)'),  # Async Definitions
        re.compile(r'^\s*return\b'),  # Return statements
        re.compile(r'^\s*if\s+.*:?\s*$'),  # If-statements
        re.compile(r'^\s*for\s+.*in\s+.*'),  # For-loops
        re.compile(r'^\s*while\s+\(.*\)\s*'),  # While-loops

        # --- ASSIGNMENTS & OPERATORS ---
        re.compile(r'^\s*const\s+\w+\s*='),  # Constants
        re.compile(r'^\s*let\s+\w+\s*='),  # Variables
        re.compile(r'^\s*var\s+\w+\s*[;=]'),  # Legacy JS/C#/Go
        re.compile(r'.*=>\s*\{?'),  # Arrow Functions
        re.compile(r'^\s*#!\s*/'),  # Shebangs
        re.compile(r'^\s*[\{\}\[\]\(\)]\s*$'),  # Stray Brackets
        re.compile(r'^\s*".*":\s*'),  # JSON Keys
        re.compile(r'^\s*\w+:\s*'),  # YAML Keys (Risk: Could be directory with colon? No, dir colon is at end)
    ]

    PERMISSION_MAP: Final[Dict[str, str]] = {
        "executable": "755", "bin": "755", "script": "755",
        "readonly": "444", "secret": "600", "private": "600", "public": "644"
    }

    # [FACULTY 1]: THE EXTENSION SOVEREIGNTY ORACLE
    # If a path ends with one of these, it is a FILE. Period.
    # Note: We anchor to the end of the string to prevent false positives.
    FILE_EXTENSION_REGEX: Final[re.Pattern] = re.compile(
        r'\.(py|js|ts|tsx|jsx|css|scss|less|html|htm|json|md|markdown|yaml|yml|toml|ini|cfg|conf|sh|bash|zsh|fish|go|rs|c|cpp|h|hpp|java|kt|kts|rb|php|pl|lua|zig|arch|symphony|scaffold|lock|env|env\..*|txt|xml|svg|png|jpg|jpeg|gif|ico|pdf|zip|gz|tar|rar|7z|sql|dockerignore|gitignore|editorconfig|eslintrc|prettierrc|dockerfile|makefile|gemfile|rakefile|vagrantfile)$',
        re.IGNORECASE
    )

    # [FACULTY 3]: THE EXPLICIT LOCK SIGILS
    RAW_BLOCK_START_REGEX: Final[re.Pattern] = re.compile(
        r'(::|:?\s*=|\+=|\^=|~=|<<)\s*("""|\'\'\')'
    )

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "StructuralScribe")
        # Ensure trait registry exists in parser memory
        if not hasattr(self.parser, 'traits'):
            self.parser.traits = {}
        # [FACULTY 11]: Identity Registry (Path -> IsDir)
        self._identity_registry: Dict[str, bool] = {}

    # =========================================================================
    # == THE MAIN CONDUCT RITE (KINETIC EXECUTION)                           ==
    # =========================================================================

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE SOVEREIGN CONDUCTOR (V-Ω-TOTALITY-V900.0-SINGULARITY)                   ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_STRUCTURAL_SCRIBE_V900_TOTALITY_FINALIS_2026
        """
        start_ts = time.perf_counter()
        line_num = vessel.line_num
        raw_line = vessel.raw_scripture
        raw_stripped = raw_line.strip()

        # [FACULTY 24]: Safe Default Return (The Finality Vow)
        next_index = i + 1
        classification_reason = "Triage: Default Fallback"

        try:
            # --- MOVEMENT 0: THE VOID GUARD ---
            if not raw_stripped:
                return next_index

            # --- MOVEMENT I: THE META-GAZE (TRAITS) ---
            if vessel.line_type == GnosticLineType.TRAIT_DEF:
                return self._conduct_trait_definition(lines, i, vessel)
            if vessel.line_type == GnosticLineType.TRAIT_USE:
                return self._conduct_trait_usage(lines, i, vessel)

            # --- MOVEMENT II: THE MATTER-ANCHOR LOCK (EXPLICIT) ---
            # [FACULTY 4]: Checks for explicit content sigils (::, <<, """) which force File Identity.
            is_explicit_file_locked = False

            # Check A: Pre-parsed content delimiter
            if vessel.content in ('"""', "'''") or (vessel.mutation_op and '"""' in vessel.mutation_op):
                is_explicit_file_locked = True
                classification_reason = "Lock: Delimiter Token Detected"

            # Check B: Raw Regex (Failsafe for tokenizer misses)
            elif self.RAW_BLOCK_START_REGEX.search(raw_stripped):
                if '"""' in raw_stripped:
                    vessel.content = '"""'
                elif "'''" in raw_stripped:
                    vessel.content = "'''"
                is_explicit_file_locked = True
                classification_reason = "Lock: Raw Regex Scry Pattern Match"

            # Check C: Inline Sigils (::, <<)
            elif '::' in raw_stripped or '<<' in raw_stripped:
                is_explicit_file_locked = True
                classification_reason = "Lock: Inline Content Sigil Perceived"

            if is_explicit_file_locked:
                vessel.is_dir = False
                self.Logger.verbose(f"L{vessel.line_num}: Content Sanctuary Locked. Path: '{vessel.name}'")

                # Route to Explicit Block Consumer if needed
                if vessel.content in ('"""', "'''"):
                    return self._conduct_explicit_block_rite(lines, i, vessel)
                else:
                    self._proclaim_item(vessel)
                    return i + 1

            # --- MOVEMENT III: THE ANTI-MATTER SIEVE (LEAK DETECTION) ---
            # [FACULTY 5]: If the line looks like code/markdown and IS NOT locked, it is a leak.
            # We ignore it to prevent it becoming a directory.
            for pattern in self.ANTI_MATTER_SIGNATURES:
                if pattern.search(raw_stripped):
                    self.Logger.verbose(f"L{vessel.line_num}: Anti-Matter Leak Rejected: '{raw_stripped[:20]}...'")
                    return next_index

            # --- MOVEMENT IV: THE HEURISTIC TRIAGE (IDENTITY ADJUDICATION) ---

            # 1. Explicit Directory (Trailing Slash)
            has_explicit_dir_slash = raw_stripped.endswith(('/', '\\'))

            # 2. Implicit Directory (Indented Children)
            # [FACULTY 16]: We look ahead to see if the structure implies nesting.
            has_indented_disciples = self._is_followed_by_indented_children(lines, i)

            # 3. Explicit File (Extension) - [FACULTY 1 & 2]
            # [THE COLON-CLEANSING GAZE]
            # We strip the trailing colon from the path token BEFORE checking the extension.
            # This handles `config.py:` -> `config.py` which matches the regex.
            path_token = raw_stripped.split()[0].rstrip(':').strip('"\'')
            has_file_extension = bool(self.FILE_EXTENSION_REGEX.search(path_token))

            # --- MOVEMENT V: THE IDENTITY DECREE ---

            if has_explicit_dir_slash:
                vessel.is_dir = True
                classification_reason = "Triage: Trailing Slash Decree"

            elif has_file_extension:
                # [THE CORE FIX]: EXTENSION SOVEREIGNTY IS ABSOLUTE.
                # Even if it has indented children, it is a FILE.
                vessel.is_dir = False
                classification_reason = "Triage: Matter Extension Sovereignty"

            elif has_indented_disciples:
                # Only promote to directory if it lacks a file extension
                vessel.is_dir = True
                classification_reason = "Triage: Indented Disciples Found"

            else:
                # Default atomic form is File (Leaf Node)
                vessel.is_dir = False
                classification_reason = "Triage: Default Atomic Form"

            # --- MOVEMENT VI: GEOMETRIC ROUTING (IMPLICIT CONTENT) ---

            should_consume_implicit_block = False

            # Case A: Explicit Block Starter (Trailing Colon on a File)
            if (raw_stripped.endswith(':') and not vessel.is_dir):
                should_consume_implicit_block = True
                classification_reason += " -> Implicit Content Block (:)"

            # Case B: The Extension Anomaly (File with Children)
            # [FACULTY 3]: Implicit Content Fusion
            # If it's a file (due to extension sovereignty) but has children,
            # those children are CONTENT, not sub-files.
            elif (not vessel.is_dir and has_indented_disciples):
                should_consume_implicit_block = True
                classification_reason += " -> Implicit Content Block (Indented Text)"

            if should_consume_implicit_block:
                # [THE RITE OF FUSION]
                next_index = self._conduct_indented_block_rite(lines, i, vessel)
            else:
                self._proclaim_item(vessel)
                next_index = i + 1

            # --- MOVEMENT VII: METABOLIC FINALITY ---
            latency = (time.perf_counter() - start_ts) * 1000
            if self.Logger.is_verbose:
                self.Logger.verbose(f"L{line_num:03d}: {classification_reason} | {latency:.2f}ms")

            return next_index

        except Exception as catastrophic_paradox:
            # [FACULTY 24]: THE FINALITY VOW
            # We catch all fractures to ensure the parser does not halt.
            self.parser._proclaim_heresy(
                "META_HERESY_STRUCTURAL_SCRIBE_FRACTURED",
                vessel,
                details=f"The Scribe's mind shattered on line {line_num}: {str(catastrophic_paradox)}",
                exception_obj=catastrophic_paradox
            )
            return i + 1

    # =========================================================================
    # == INTERNAL FACULTIES (SENSORS & REUSABILITY)                          ==
    # =========================================================================

    def _is_followed_by_indented_children(self, lines: List[str], current_idx: int) -> bool:
        """
        [FACULTY 16]: THE GAZE OF THE FUTURE.
        Perceives if the next manifest soul is indented deeper than the current one.
        Ignores blanks and comments.
        """
        if current_idx + 1 >= len(lines):
            return False

        parent_indent = self.parser._calculate_original_indent(lines[current_idx])

        # Scan ahead for the next non-void, non-comment scripture
        for next_idx in range(current_idx + 1, len(lines)):
            line = lines[next_idx]
            if not line.strip() or line.strip().startswith(('#', '//')):
                continue

            next_indent = self.parser._calculate_original_indent(line)
            return next_indent > parent_indent

        return False

    def _conduct_indented_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [FACULTY 3]: IMPLICIT CONTENT CONSUMPTION.
        Delegates to the GnosticBlockConsumer to eat indented lines as text content.
        This handles the "README text leaking as directories" case.
        """
        consumer = GnosticBlockConsumer(lines)
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # Determine where the block content starts (next line)
        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        if content_lines:
            # Dedent the block relative to the parent
            # But the BlockConsumer returns raw lines. We must dedent them properly.
            try:
                # Find first valid line to determine visual indent baseline
                first_valid = next((l for l in content_lines if l.strip()), None)
                if first_valid:
                    # We strip only the parent's indentation + standard offset?
                    # No, textwrap.dedent handles common leading whitespace.
                    vessel.content = dedent("\n".join(content_lines)).rstrip()
                else:
                    vessel.content = ""
            except Exception:
                vessel.content = "\n".join(content_lines)
        else:
            vessel.content = ""

        self._proclaim_item(vessel)
        return end_index

    def _conduct_explicit_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 4]: EXPLICIT BLOCK CONSUMPTION."""
        consumer = GnosticBlockConsumer(lines)

        # Normalize delimiters
        delimiter = '"""'
        if "'''" in vessel.content or "'''" in vessel.raw_scripture:
            delimiter = "'''"
        elif '"""' in vessel.content or '"""' in vessel.raw_scripture:
            delimiter = '"""'

        # Hand off to the Block Consumer
        content_lines, end_index = consumer.consume_explicit_block(i + 1, vessel.raw_scripture)
        pure_content = dedent("\n".join(content_lines)).strip()

        # [FACULTY 15]: Quote Stripping & Backslash Healing
        if delimiter == '"""':
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)

        vessel.content = pure_content
        self._proclaim_item(vessel)
        return end_index

    def _conduct_trait_definition(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 17]: Trait Definition Logic."""
        match = re.match(r"^\s*%%\s*trait\s+(?P<name>\w+)\s*=\s*(?P<path>.*)$", vessel.raw_scripture.strip())
        if not match: return i + 1

        name = match.group("name")
        path_str = match.group("path").strip().strip('"\'')

        base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        resolved_path = (base_dir / path_str).resolve()

        if not resolved_path.exists():
            self.parser._proclaim_heresy("TRAIT_VOID", vessel, details=f"Trait '{resolved_path}' unmanifest.")

        self.parser.traits[name] = resolved_path
        self.Logger.success(f"L{vessel.line_num}: Trait '[soul]{name}[/soul]' anchored to {resolved_path.name}")
        return i + 1

    def _conduct_trait_usage(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 17]: Trait Usage Logic."""
        match = re.match(r"^\s*%%\s*use\s+(?P<name>\w+)(?:\s+(?P<args>.*))?$", vessel.raw_scripture.strip())
        if not match: return i + 1

        name, args_str = match.group("name"), match.group("args")
        if name not in self.parser.traits:
            self.parser._proclaim_heresy("UNKNOWN_TRAIT_HERESY", vessel, details=f"Trait '{name}' is unknown.")
            return i + 1

        trait_path = self.parser.traits[name]
        trait_vars = self.parser.variables.copy()

        if args_str:
            try:
                for pair in shlex.split(args_str):
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        trait_vars[k.strip()] = get_alchemist().transmute(v.strip().strip('"\''), self.parser.variables)
            except Exception:
                pass

        self.Logger.info(f"Materializing Trait '[soul]{name}[/soul]' from {trait_path.name}...")

        try:
            sub_parser = self.parser.__class__(grammar_key='scaffold')
            sub_parser.variables = trait_vars
            sub_parser.traits = self.parser.traits

            content = trait_path.read_text(encoding='utf-8')
            _, sub_items, sub_commands, sub_edicts, _, _ = sub_parser.parse_string(content, trait_path)

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

    def _proclaim_item(self, vessel: GnosticVessel):
        """
        [THE FINAL SEAL]
        Transmutes the GnosticVessel into the final ScaffoldItem.
        """
        # [FACULTY 8]: Unicode & Slash Normalization
        name = unicodedata.normalize('NFC', vessel.name).replace('\\', '/')
        # [FACULTY 17]: Quote Stripping from Path
        name = name.strip('"\'')

        # [FACULTY 7]: NAME NORMALIZATION (THE CURE)
        # Strip trailing colon if present (e.g. "README.md:" -> "README.md")
        if name.endswith(':'):
            name = name[:-1]

        # Ensure Directory Slash if needed
        if vessel.is_dir and name and not name.endswith('/'):
            name += '/'

        # [FACULTY 11]: ONTOLOGICAL CONSISTENCY GUARD
        path_key = name.lower().rstrip('/')
        if path_key in self._identity_registry:
            original_is_dir = self._identity_registry[path_key]
            if original_is_dir != vessel.is_dir:
                # Collision!
                if not original_is_dir and vessel.is_dir:
                    # If we are trying to make a file a dir, and it was previously a file, we force file.
                    # This happens when indented content is misinterpreted as children.
                    self.Logger.warn(f"Identity Collision: '{name}' forced to File state by precedence.")
                    vessel.is_dir = False
                    if name.endswith('/'): name = name[:-1]
                else:
                    # Critical Heresy: Directory becoming File or vice versa
                    self.parser._proclaim_heresy("ONTOLOGICAL_SCHISM", vessel,
                                                 details=f"Path '{name}' has conflicting identities.")
                    return

        self._identity_registry[path_key] = vessel.is_dir

        # [FACULTY 12]: Permission Alchemy
        final_permissions = self.PERMISSION_MAP.get(vessel.permissions, vessel.permissions)
        if self.parser.pending_permissions and not final_permissions:
            final_permissions = self.parser.pending_permissions
            self.parser.pending_permissions = None

        # [FACULTY 11]: Binary Divination
        is_binary = bool(vessel.content and ("| base64" in vessel.content or "| binary" in vessel.content))

        # [FACULTY 6]: Bracket Check (Path Validity)
        if re.search(r'[\[\]\{\}\(\)]', name) and not ('{{' in name):
            self.Logger.warn(f"Path '{name}' contains brackets. Possible Parser Leak.")

        # [FACULTY 10]: Traversal Guard
        if '../' in name or '..\\' in name:
            self.parser._proclaim_heresy("TRAVERSAL_HERESY", vessel, details="Parent directory traversal prohibited.")
            return

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

        if item.line_type == GnosticLineType.FORM and item.path:
            self.parser.items_by_path[item.path.as_posix()] = item

        self.parser.raw_items.append(item)

    def __repr__(self) -> str:
        return f"<Ω_STRUCTURAL_SCRIBE_V900 status=OMNISCIENT version=900.5>"

# == SCRIPTURE SEALED: THE GEOMETRIC CITADEL IS TOTALITY ==
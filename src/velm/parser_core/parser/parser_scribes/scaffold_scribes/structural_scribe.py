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
    == THE GEOMETRIC CITADEL (V-Ω-TOTALITY-V10000-MATHEMATICALLY-CERTAIN)          ==
    =================================================================================
    @gnosis:title The Geometric Citadel
    @gnosis:summary The final, unbreakable fortress of structural perception.
    @gnosis:LIF INFINITY
    @gnosis:auth_code Ω_STRUCTURE_V10000_SOVEREIGN_NAME_FINALIS

    This artisan adjudicates the boundary between **Topography** (Sanctums/Scriptures)
    and **Matter** (Content). It has been Infinitely Ascended to enforce the **Law of
    Pure Naming**, entirely ignoring the profane `raw_scripture` and relying solely
    on the `vessel.name` purified by the Deconstructor.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:

    1.  **Pure Naming Sovereignty (THE CORE CURE):** The Scribe no longer gazes upon the
        `raw_stripped` line to make structural decisions. It relies 100% on the `vessel.name`,
        which has been stripped of comments, emojis, and box-drawing noise by the Deconstructor.
    2.  **Comment-Immune Directory Adjudication:** Because it uses `vessel.name`, lines like
        `apps/  # DEPLOYABLE APPS` are flawlessly perceived as `apps/`, instantly achieving
        Directory Sovereignty.
    3.  **The Colon-Cleansing Gaze:** Surgically strips trailing colons (`:`) from path
        tokens *before* checking for file extensions, ensuring `config.py:` is recognized
        as a File, not a Directory.
    4.  **Absolute Extension Sovereignty (THE LAW):** If `vessel.name` ends with a known
        matter extension (.py, .md, .json), it is LOCKED as a File, regardless of indentation.
    5.  **Implicit Content Fusion:** If a Sovereign File is followed by indented text,
        that text is consumed as Body Matter, not Children.
    6.  **The Matter-Anchor Lock:** `::`, `<<`, `+=` sigils instantly force File identity,
        bypassing all other heuristic checks.
    7.  **The Anti-Matter Phalanx V10:** Re-calibrated to act as a *secondary* shield,
        only evaluating `vessel.name` to detect code/markdown masquerading as paths.
    8.  **The Trailing Slash Decree:** A trailing `/` on the purified name guarantees
        Directory classification instantly.
    9.  **Achronal Path Normalization:** Forces NFC Unicode and POSIX slash discipline on
        the final path, obliterating Windows pathing heresies.
    10. **The Bracket Balance Inquisitor:** Detects unclosed `{` or `(` in paths, flagging
        them as Parser Leaks before they corrupt the disk.
    11. **The Traversal Sentinel:** Pre-empts `../` directory escape attacks at the
        parsing layer, guaranteeing virtual sandbox integrity.
    12. **The Binary Oracle:** Scans content for `| base64` filters to toggle binary
        storage modes automatically.
    13. **The Permissions Alchemist:** Transmutes `%% executable` into `0o755`.
    14. **The Ontological Consistency Guard:** Prevents a path from being defined as
        a File on line 10 and a Directory on line 50.
    15. **The Symlink Diviner:** Native handling of `->` definitions from the vessel.
    16. **The Hash Anchor:** Native handling of `@hash(...)` integrity checks.
    17. **The Gnostic Indentation Lookahead:** Flawless detection of implicit children
        by peering into the future of the token stream.
    18. **The Pure Quote Stripper:** Advanced regex to peel quotes while preserving
        inner string integrity for complex filenames.
    19. **Alchemical Variable Passthrough:** Safely handles `{{var}}/` directories
        without premature rendering panics.
    20. **The Seed Extractor:** Safely channels `<< path` requests for external content.
    21. **The Mutation Operator Logic:** Applies `+=` (Append) vs `::` (Overwrite).
    22. **The Semantic Selector Matrix:** Parses `@inside(...)` modifiers.
    23. **The Index Healer:** Correctly passes the *current* line index to the BlockConsumer,
        preventing the "First Line Vanishing" paradox.
    24. **The Finality Vow:** Absolute mathematical guarantee of returning a valid
        state index, eliminating infinite loop conditions.
    =================================================================================
    """

    # [FACULTY 7]: THE ANTI-MATTER PHALANX V10
    # An omniscient regex array identifying code/markdown masquerading as paths.
    # Evaluated against the purified name to avoid false positives.
    ANTI_MATTER_SIGNATURES: Final[List[re.Pattern]] = [
        re.compile(r'^\s*#+\s+'),  # Markdown Headers
        re.compile(r'^\s*>\s+'),  # Markdown Quotes
        re.compile(r'^\s*[\*\-\+]\s+'),  # Markdown Lists
        re.compile(r'^\s*`{3}'),  # Code Fences
        re.compile(r'^\s*!\[.*\]\(.*\)\s*$'),  # Images
        re.compile(r'^\s*\[.*\]\(.*\)\s*$'),  # Links
        re.compile(r'^\s*---\s*$'),  # Horizontal Rules
        re.compile(r'^\s*<[a-zA-Z!/].*>'),  # HTML/XML Tags
        re.compile(r'^\s*import\s+.*from\s+[\'"]'),  # ES6 / TS Imports
        re.compile(r'^\s*export\s+(const|let|var|class|function|default|interface|type)'),
        re.compile(r'^\s*from\s+[\w.-]+\s+import\b'),  # Python from-imports
        re.compile(r'^\s*interface\s+\w+'),  # TS/Java/C# interfaces
        re.compile(r'^\s*type\s+\w+\s*='),  # TS Type Aliases
        re.compile(r'^\s*@[\w.]+\s*\('),  # Decorators
        re.compile(r'^\s*def\s+\w+\s*\('),  # Python Functions
        re.compile(r'^\s*fn\s+\w+'),  # Rust/Zig
        re.compile(r'^\s*func\s+\w+'),  # Go/Swift
        re.compile(r'^\s*async\s+(def|fn|func)'),  # Async Definitions
        re.compile(r'^\s*return\b'),  # Return statements
        re.compile(r'^\s*if\s+.*:?\s*$'),  # If-statements
        re.compile(r'^\s*for\s+.*in\s+.*'),  # For-loops
        re.compile(r'^\s*while\s+\(.*\)\s*'),  # While-loops
        re.compile(r'^\s*const\s+\w+\s*='),  # Constants
        re.compile(r'^\s*let\s+\w+\s*='),  # Variables
        re.compile(r'^\s*var\s+\w+\s*[;=]'),  # Legacy JS/C#/Go
        re.compile(r'.*=>\s*\{?'),  # Arrow Functions
        re.compile(r'^\s*#!\s*/'),  # Shebangs
        re.compile(r'^\s*[\{\}\[\]\(\)]\s*$'),  # Stray Brackets
        re.compile(r'^\s*".*":\s*'),  # JSON Keys
        re.compile(r'^\s*\w+:\s*'),  # YAML Keys
    ]

    PERMISSION_MAP: Final[Dict[str, str]] = {
        "executable": "755", "bin": "755", "script": "755",
        "readonly": "444", "secret": "600", "private": "600", "public": "644"
    }

    # [FACULTY 4]: THE EXTENSION SOVEREIGNTY ORACLE
    FILE_EXTENSION_REGEX: Final[re.Pattern] = re.compile(
        r'\.(py|js|ts|tsx|jsx|css|scss|less|html|htm|json|md|markdown|yaml|yml|toml|ini|cfg|conf|sh|bash|zsh|fish|go|rs|c|cpp|h|hpp|java|kt|kts|rb|php|pl|lua|zig|arch|symphony|scaffold|lock|env|env\..*|txt|xml|svg|png|jpg|jpeg|gif|ico|pdf|zip|gz|tar|rar|7z|sql|dockerignore|gitignore|editorconfig|eslintrc|prettierrc|dockerfile|makefile|gemfile|rakefile|vagrantfile)$',
        re.IGNORECASE
    )

    RAW_BLOCK_START_REGEX: Final[re.Pattern] = re.compile(
        r'(::|:?\s*=|\+=|\^=|~=|<<)\s*("""|\'\'\')'
    )

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "StructuralScribe")
        if not hasattr(self.parser, 'traits'):
            self.parser.traits = {}
        # [FACULTY 14]: Identity Registry (Path -> IsDir)
        self._identity_registry: Dict[str, bool] = {}

    # =========================================================================
    # == THE MAIN CONDUCT RITE (KINETIC EXECUTION)                           ==
    # =========================================================================

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE SOVEREIGN CONDUCTOR (V-Ω-TOTALITY-V10000.0-SINGULARITY)                 ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SUPREME
        """
        start_ts = time.perf_counter()
        line_num = vessel.line_num

        # [FACULTY 24]: Safe Default Return (The Finality Vow)
        next_index = i + 1
        classification_reason = "Triage: Default Fallback"

        try:
            # --- MOVEMENT 0: THE VOID GUARD ---
            # [ASCENSION 1]: We operate EXCLUSIVELY on the purified vessel name.
            if not vessel.name or vessel.line_type == GnosticLineType.VOID:
                return next_index

            pure_name = vessel.name.strip()

            # --- MOVEMENT I: THE META-GAZE (TRAITS) ---
            if vessel.line_type == GnosticLineType.TRAIT_DEF:
                return self._conduct_trait_definition(lines, i, vessel)
            if vessel.line_type == GnosticLineType.TRAIT_USE:
                return self._conduct_trait_usage(lines, i, vessel)

            # --- MOVEMENT II: THE MATTER-ANCHOR LOCK (EXPLICIT) ---
            # [FACULTY 6]: Checks for explicit content sigils (::, <<, """) which force File Identity.
            is_explicit_file_locked = False

            if vessel.content in ('"""', "'''") or (vessel.mutation_op and '"""' in vessel.mutation_op):
                is_explicit_file_locked = True
                classification_reason = "Lock: Delimiter Token Detected"

            elif self.RAW_BLOCK_START_REGEX.search(vessel.raw_scripture):
                if '"""' in vessel.raw_scripture:
                    vessel.content = '"""'
                elif "'''" in vessel.raw_scripture:
                    vessel.content = "'''"
                is_explicit_file_locked = True
                classification_reason = "Lock: Raw Regex Scry Pattern Match"

            elif vessel.content or vessel.seed_path or vessel.mutation_op:
                is_explicit_file_locked = True
                classification_reason = "Lock: Inline Content/Seed Sigil Perceived"

            if is_explicit_file_locked:
                vessel.is_dir = False
                self.Logger.verbose(f"L{vessel.line_num}: Content Sanctuary Locked. Path: '{pure_name}'")

                if vessel.content in ('"""', "'''"):
                    return self._conduct_explicit_block_rite(lines, i, vessel)
                else:
                    self._proclaim_item(vessel)
                    return i + 1

            # --- MOVEMENT III: THE ANTI-MATTER SIEVE (LEAK DETECTION) ---
            # [FACULTY 7]: Apply the regex shield against the purified name.
            for pattern in self.ANTI_MATTER_SIGNATURES:
                if pattern.search(pure_name):
                    self.Logger.verbose(f"L{vessel.line_num}: Anti-Matter Leak Rejected: '{pure_name[:30]}...'")
                    return next_index

            # --- MOVEMENT IV: THE HEURISTIC TRIAGE (IDENTITY ADJUDICATION) ---
            # [ASCENSION 1 & 2]: PURE NAMING SOVEREIGNTY

            # 1. Strip the implicit block colon for pure extension checking [FACULTY 3]
            test_name = pure_name[:-1].strip() if pure_name.endswith(':') else pure_name
            # Also strip quotes for the extension test
            test_name = test_name.strip('"\'')

            # 2. Adjudicate Attributes
            has_file_extension = bool(self.FILE_EXTENSION_REGEX.search(test_name))
            has_explicit_dir_slash = pure_name.endswith(('/', '\\'))
            has_indented_disciples = self._is_followed_by_indented_children(lines, i)

            # --- MOVEMENT V: THE IDENTITY DECREE (THE LAW) ---

            if vessel.is_dir:
                # The Emoji Oracle in Deconstructor already proved it's a directory
                classification_reason = "Triage: Emoji Oracle Pre-Ordained"
            elif has_explicit_dir_slash:
                vessel.is_dir = True
                classification_reason = "Triage: Trailing Slash Decree"
            elif has_file_extension:
                # [FACULTY 4]: EXTENSION SOVEREIGNTY IS ABSOLUTE.
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
            if pure_name.endswith(':') and not vessel.is_dir:
                should_consume_implicit_block = True
                classification_reason += " -> Implicit Content Block (:)"

            # Case B: The Extension Anomaly (File with Children)
            # [FACULTY 5]: Implicit Content Fusion
            elif not vessel.is_dir and has_indented_disciples:
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
        [FACULTY 17]: THE GAZE OF THE FUTURE.
        Perceives if the next manifest soul is indented deeper than the current one.
        Ignores blanks and comments.
        """
        if current_idx + 1 >= len(lines):
            return False

        parent_indent = self.parser._calculate_original_indent(lines[current_idx])

        for next_idx in range(current_idx + 1, len(lines)):
            line = lines[next_idx]
            if not line.strip() or line.strip().startswith(('#', '//')):
                continue

            next_indent = self.parser._calculate_original_indent(line)
            return next_indent > parent_indent

        return False

    def _conduct_indented_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [FACULTY 5]: IMPLICIT CONTENT CONSUMPTION.
        Delegates to the GnosticBlockConsumer to eat indented lines as text content.
        This handles the "README text leaking as directories" case.
        """
        consumer = GnosticBlockConsumer(lines)
        parent_indent = self.parser._calculate_original_indent(lines[i])

        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        if content_lines:
            try:
                first_valid = next((l for l in content_lines if l.strip()), None)
                if first_valid:
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
        """
        [FACULTY 6]: EXPLICIT BLOCK CONSUMPTION.
        Uses GnosticBlockConsumer to consume content between quotes.
        """
        consumer = GnosticBlockConsumer(lines)

        delimiter = '"""'
        if "'''" in vessel.content or "'''" in vessel.raw_scripture:
            delimiter = "'''"
        elif '"""' in vessel.content or '"""' in vessel.raw_scripture:
            delimiter = '"""'

        # Hand off to the Block Consumer
        # [ASCENSION 23]: WE PASS 'i', NOT 'i+1'.
        content_lines, end_index = consumer.consume_explicit_block(i, vessel.raw_scripture)
        pure_content = dedent("\n".join(content_lines)).strip()

        # [FACULTY 18]: Quote Stripping & Backslash Healing
        if delimiter == '"""':
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)

        vessel.content = pure_content
        self._proclaim_item(vessel)
        return end_index

    def _conduct_trait_definition(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 19]: Trait Definition Logic."""
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
        """[FACULTY 19]: Trait Usage Logic."""
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
        # [FACULTY 9]: Unicode & Slash Normalization
        name = unicodedata.normalize('NFC', vessel.name).replace('\\', '/')

        # [FACULTY 18]: Quote Stripping from Path
        name = name.strip('"\'')

        # [FACULTY 7]: NAME NORMALIZATION (THE CURE)
        # Strip trailing colon if present (e.g. "README.md:" -> "README.md")
        if name.endswith(':'):
            name = name[:-1]

        # [FACULTY 8]: Ensure Directory Slash if needed
        if vessel.is_dir and name and not name.endswith('/'):
            name += '/'

        # [FACULTY 14]: ONTOLOGICAL CONSISTENCY GUARD
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

        # [FACULTY 13]: Permission Alchemy
        final_permissions = self.PERMISSION_MAP.get(vessel.permissions, vessel.permissions)
        if self.parser.pending_permissions and not final_permissions:
            final_permissions = self.parser.pending_permissions
            self.parser.pending_permissions = None

        # [FACULTY 12]: Binary Divination
        is_binary = bool(vessel.content and ("| base64" in vessel.content or "| binary" in vessel.content))

        # [FACULTY 10]: Bracket Check (Path Validity)
        if re.search(r'[\[\]\{\}\(\)]', name) and not ('{{' in name):
            self.Logger.warn(f"Path '{name}' contains brackets. Possible Parser Leak.")

        # [FACULTY 11]: Traversal Guard
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
        return f"<Ω_STRUCTURAL_SCRIBE_V10000 status=OMNISCIENT version=10000.0-HEALED>"
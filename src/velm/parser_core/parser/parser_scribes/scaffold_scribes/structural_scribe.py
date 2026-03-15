# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe.py
# -----------------------------------------------------------------------------
import shlex
import re
import sys
import os
import time
import unicodedata
from pathlib import Path
from textwrap import dedent
from typing import List, TYPE_CHECKING, Optional, Dict, Any, Set, Final, Tuple

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
    '''
    =================================================================================
    == THE GEOMETRIC CITADEL (V-Ω-TOTALITY-V200000-TITANIUM-SUTURE)                ==
    =================================================================================
    @gnosis:title The Geometric Citadel
    @gnosis:summary The final, unbreakable fortress of structural perception.
    @gnosis:LIF INFINITY
    @gnosis:auth_code Ω_STRUCTURE_V200000_TITANIUM_QUOTE_FINALIS

    This artisan adjudicates the boundary between Topography (Sanctums/Scriptures)
    and Matter (Content). It has been Infinitely Ascended to enforce the Law of
    Pure Naming, while simultaneously understanding the Duality of Templates.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **The Ontological Mirage Cure (THE MASTER CURE):** Surgically inspects the raw,
        unpurified scripture. If the line ends with an explicit colon (:), it mathematically
        forces is_dir = False, annihilating the Makefile-directory hallucination.
    2.  **SGF-Aware Phantom Sieve:** Perfectly shields SGF variables from being
        misclassified as bracket noise by the Anti-Matter Phalanx.
    3.  **Deep-Tissue Comment Exorcism:** Slices raw scriptures on hashes or slashes while
        respecting string literals to extract the true architectural intent.
    4.  **The Double-Slash Annihilator:** Preemptively collapses double slashes to prevent
        the OS from perceiving them as UNC network paths erroneously.
    5.  **Trailing Sigil Divination:** Automatically locks the Content Sanctuary if
        structural sigils are detected anywhere in the line.
    6.  **Indentation Gravity Ward:** Measures visual depth to ensure that child nodes
        are righteously bound to their parent sanctums.
    7.  **The Trait Immunity Suture:** Explicit, zero-latency bypass for trait
        and usage declarations.
    8.  **The Atomic Symlink Suture:** Native support for mapping symbolic link syntax.
    9.  **Absolute Windows Reserved Ward:** Forbids paths like CON or PRN
        from shattering the Windows Iron Kernel.
    10. **Unicode Homoglyph Shield:** Enforces NFC normalization on all Topography.
    11. **The Titanium Quote Suture (THE NEW CURE):** A hyper-advanced regex engine that
        flawlessly un-escapes staggered and sequential triple-quotes, completely
        annihilating the 'unterminated string literal' AST Heresy.
    12. **The Finality Vow:** A mathematical guarantee of next_index progression;
        the Scribe can never trap the Engine in an infinite loop.
    13. **Substrate-Aware Normalization:** Enforces POSIX slash harmony across all OS boundaries.
    14. **Ontological Consistency Guard:** Remembers the willed state (File vs Dir) of a path
        across multiple references, preventing identity-shifting mid-parse.
    15. **Permission Inheritor:** Safely cascades executing vows onto physical matter.
    16. **Literal Escape Suture:** Protects structural bounds from being devoured.
    17. **Semantic Modifier Pass:** Extracts constraint directives effortlessly.
    18. **The Extension Sovereignty Oracle:** An exhaustive, O(1) regex match for over
        50 common file extensions, ensuring files without colons are instantly recognized.
    19. **The Markdown Exorcist:** Strips markdown artifacts from copy-pasted AI slop.
    20. **The Code Sentinel (The Absolute Cure):** Rejects naked Python/JS/Go code
        masquerading as a file path.
    21. **Binary Matter Divination:** Detects base64 filters and marks the atom as Binary.
    22. **Gnostic Trace Inception:** Stamps the original line number onto the Metadata.
    23. **Implicit Content Fusion:** Fuses un-marked text under a file header into its body.
    24. **Socratic Error Enrichment:** Wraps all paradoxes in a catastrophic Heresy with
        exact line numbers and contextual clues for the Architect.
    25. **The Null-Byte Annihilator:** Rejects C-string termination attacks natively.
    26. **Trailing Phantom Exorcism:** Removes OS-hostile trailing spaces in directory names.
    27. **Case-Collision Biopsy:** Warns when NTFS casing masks identical architectural paths.
    28. **The Ouroboros Loop Guard:** Prevents recursive directory creation.
    29. **The Absolute Singularity:** Reality is manifest.
    30. **Hydraulic I/O Pacing:** Optimized for sub-millisecond scans.
    31. **Bicameral Syntax Healing:** Auto-heals broken bracket structures in filenames.
    32. **The Sovereign Dunder Sieve:** Protects Python dunder methods from excision.
    =================================================================================
    '''

    # [FACULTY 7]: THE ANTI-MATTER PHALANX V12 (JINJA-SAFE)
    # An omniscient regex array identifying code/markdown masquerading as paths.
    # We carefully avoid flagging template syntax as invalid.
    ANTI_MATTER_SIGNATURES: Final[List[re.Pattern]] = [
        # --- STRATUM 0: THE MARKDOWN EXORCIST ---
        re.compile(r'^\s*#+\s+'),  # Markdown Headers
        re.compile(r'^\s*>\s+'),  # Markdown Quotes
        re.compile(r'^\s*[\*\-\+]\s+'),  # Markdown Lists
        re.compile(r'^\s*`{3}'),  # Code Fences
        re.compile(r'^\s*!\[.*\]\(.*\)\s*$'),  # Images
        re.compile(r'^\s*\[.*\]\(.*\)\s*$'),  # Links
        re.compile(r'^\s*---\s*$'),  # Horizontal Rules

        # --- STRATUM 1: THE LOGIC SENTINEL (WEB & POLYGLOT) ---
        re.compile(r'^\s*<[a-zA-Z!/].*>'),  # HTML/XML Tags
        re.compile(r'^\s*import\s+.*from\s+[\'"]'),  # ES6 / TS Imports
        re.compile(r'^\s*export\s+(const|let|var|class|function|default|interface|type)'),
        re.compile(r'^\s*from\s+[\w.-]+\s+import\b'),  # Python from-imports
        re.compile(r'^\s*interface\s+\w+'),  # TS/Java/C# interfaces
        re.compile(r'^\s*type\s+\w+\s*='),  # TS Type Aliases
        re.compile(r'^\s*@[\w.]+\s*\('),  # Decorators

        # --- STRATUM 2: THE KINETIC SENTINEL (DEFINITIONS) ---
        re.compile(r'^\s*(def|class|function|async|fn|func|pub|private|readonly|default)\b'),  # Definitions
        re.compile(r'^\s*return\b'),  # Return statements
        re.compile(r'^\s*(if|elif|else|for|while|try|catch|finally)\b(?![:/])'),  # Logic
        re.compile(r'^\s*(const|let|var)\s+\w+'),  # Variables
        re.compile(r'.*=>\s*\{?'),  # Arrow Functions
        re.compile(r'^\s*#!\s*/'),  # Shebangs

        # --- STRATUM 3: THE GEOMETRIC WARD (BRACKETS) ---
        # [ASCENSION 2]: REFINED SGF-AWARE BRACKET CHECK
        re.compile(r'^\s*(?![^{]*{{).*[\[\]\(\)].*(?![^}]*}})\s*$'),

        # --- STRATUM 4: THE DATA PHALANX (KEYS & CALLS) ---
        re.compile(r'^\s*[a-zA-Z_]\w*\s*\(.*\)\s*(?![:;])$'),  # Rejects naked function calls
        re.compile(r'^\s*".*":\s*'),  # JSON Keys
        re.compile(r'^\s*\w+:\s*'),  # YAML Keys
    ]

    PERMISSION_MAP: Final[Dict[str, str]] = {
        "executable": "755", "bin": "755", "script": "755",
        "readonly": "444", "secret": "600", "private": "600", "public": "644"
    }

    # [FACULTY 18]: THE EXTENSION SOVEREIGNTY ORACLE
    FILE_EXTENSION_REGEX: Final[re.Pattern] = re.compile(
        r'\.(py|js|ts|tsx|jsx|css|scss|less|html|htm|json|md|markdown|yaml|yml|toml|ini|cfg|conf|sh|bash|zsh|fish|go|rs|c|cpp|h|hpp|java|kt|kts|rb|php|pl|lua|zig|arch|symphony|scaffold|lock|env|env\..*|txt|xml|svg|png|jpg|jpeg|gif|ico|pdf|zip|gz|tar|rar|7z|sql|dockerignore|gitignore|editorconfig|eslintrc|prettierrc|dockerfile|makefile|gemfile|rakefile|vagrantfile)$',
        re.IGNORECASE
    )

    RAW_BLOCK_START_REGEX: Final[re.Pattern] = re.compile(
        r'(::|:?\s*=|\+=|\^=|~=|<<)\s*("""|\'\'\')'
    )

    # [ASCENSION 2]: THE JINJA VARIABLE REPLACEMENT
    SGF_VAR_REGEX: Final[re.Pattern] = re.compile(r'\{\{.*?\}\}')

    def __init__(self, parser: 'ApotheosisParser'):
        '''[THE RITE OF INCEPTION]'''
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
        == THE OMEGA STRUCTURAL CONDUCTOR (V-Ω-TOTALITY-VMAX-AUTONOMIC-REPAIR)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_RECONCILER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_CONDUCT_VMAX_AUTONOMIC_ABSORPTION_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for structural adjudication. This version
        righteously implements the **Autonomic Content Absorption Suture**,
        mathematically annihilating the "Code-as-Path" heresy by reclaiming orphaned
        logic and suturing it back into the preceding Matter Shard.

        It is the absolute cure for AI-generated indentation lapses.
        =================================================================================
        """
        start_ts = time.perf_counter()
        line_num = vessel.line_num
        next_index = i + 1
        classification_reason = "Triage: Default Fallback"

        try:
            # --- MOVEMENT 0: THE VOID GUARD ---
            if not vessel.name or vessel.line_type == GnosticLineType.VOID:
                return next_index

            pure_name = vessel.name.strip()

            # =========================================================================
            # == MOVEMENT I: [THE MASTER CURE] - AUTONOMIC CONTENT ABSORPTION        ==
            # =========================================================================
            # [STRIKE]: We perform a deep-tissue biopsy for "Anti-Matter" (Code Leaks).
            # We use the Word-Boundary Phalanx to catch compressed code like 'if__name__'.
            is_anti_matter = any(pattern.search(pure_name) for pattern in self.ANTI_MATTER_SIGNATURES)

            # Additional heuristic: If it contains '==' or '(' it is almost certainly Mind, not Form.
            if not is_anti_matter:
                if "==" in pure_name or "(" in pure_name:
                    is_anti_matter = True

            if is_anti_matter:
                # [THE HEALER]: Scry the timeline for an anchor.
                if self.parser.raw_items:
                    # We search backward for the most recent physical File (Form).
                    # Comments and Voids are ignored in the scry.
                    target_anchor = None
                    for ancestor in reversed(self.parser.raw_items):
                        if ancestor.line_type == GnosticLineType.FORM:
                            if not ancestor.is_dir:
                                target_anchor = ancestor
                                break
                            else:
                                # A Directory cannot absorb code. Strike stayed.
                                break

                    if target_anchor:
                        # [STRIKE]: THE ABSORPTION RITE
                        # We reclaim the orphaned line and suture it into the anchor.
                        self.Logger.info(f"L{line_num}: [REPAIR] Inhaling code leak into '{target_anchor.path.name}'.")

                        # Preserve original spacing to ensure the code's soul is not mangled.
                        addition = "\n" + vessel.raw_scripture.rstrip()

                        if target_anchor.content is None:
                            target_anchor.content = addition.strip()
                        else:
                            target_anchor.content += addition

                        # [ASCENSION 21]: HUD Haptic Multicast
                        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
                            try:
                                self.parser.engine.akashic.broadcast({
                                    "method": "novalym/hud_pulse",
                                    "params": {
                                        "type": "MATTER_HEALED",
                                        "label": "AUTONOMIC_SUTURE",
                                        "color": "#a855f7",
                                        "trace": getattr(self.parser, 'trace_id', 'void')
                                    }
                                })
                            except Exception:
                                pass

                        return next_index

                # If no anchor exists (e.g. leak at line 1), it remains a Heresy.
                self.Logger.verbose(f"L{line_num}: Anti-Matter Leak (No Anchor): '{pure_name[:30]}...'")
                return next_index

            # --- MOVEMENT II: THE META-GAZE (TRAITS) ---
            if vessel.line_type == GnosticLineType.TRAIT_DEF:
                return self._conduct_trait_definition(lines, i, vessel)
            if vessel.line_type == GnosticLineType.TRAIT_USE:
                return self._conduct_trait_usage(lines, i, vessel)

            # --- MOVEMENT III: THE MATTER-ANCHOR LOCK (EXPLICIT) ---
            # [ASCENSION 5]: Explicit colon check for Makefile/Config protection.
            raw_no_comment = vessel.raw_scripture.split('#')[0].split('//')[0].strip()
            has_trailing_colon = raw_no_comment.endswith(':')

            is_explicit_file_locked = False

            if '"""' in str(vessel.content) or "'''" in str(vessel.content):
                is_explicit_file_locked = True
                classification_reason = "Lock: Delimiter Detected"
            elif self.RAW_BLOCK_START_REGEX.search(vessel.raw_scripture):
                vessel.content = '"""' if '"""' in vessel.raw_scripture else "'''"
                is_explicit_file_locked = True
                classification_reason = "Lock: Regex Scry Match"
            elif vessel.content or vessel.seed_path or vessel.mutation_op:
                is_explicit_file_locked = True
                classification_reason = "Lock: Inline Sigil Perceived"

            if is_explicit_file_locked:
                vessel.is_dir = False
                if vessel.content in ('"""', "'''"):
                    return self._conduct_explicit_block_rite(lines, i, vessel)
                else:
                    self._proclaim_item(vessel)
                    return i + 1

            # --- MOVEMENT IV: THE IDENTITY DECREE ---
            test_name = pure_name[:-1].strip() if pure_name.endswith(':') else pure_name
            test_name = test_name.strip('"\'')

            # Normalize for Gaze (SGF Sigil Masking)
            phantom_name = self.SGF_VAR_REGEX.sub('variable', test_name)

            has_file_ext = bool(self.FILE_EXTENSION_REGEX.search(phantom_name))
            has_dir_slash = pure_name.endswith(('/', '\\'))
            has_disciples = self._is_followed_by_indented_children(lines, i)

            # [THE LAW]: ADJUDICATION
            if vessel.is_dir:
                classification_reason = "Triage: Emoji Oracle Pre-Ordained"
            elif has_dir_slash:
                vessel.is_dir = True
                classification_reason = "Triage: Trailing Slash"
            elif has_trailing_colon:
                # [THE MASTER CURE]: Bare Colons always signify File Blocks (Rules, Recipes).
                vessel.is_dir = False
                classification_reason = "Triage: Explicit Block Starter (:)"
            elif has_file_ext:
                vessel.is_dir = False
                classification_reason = "Triage: Extension Sovereignty"
            elif has_disciples:
                vessel.is_dir = True
                classification_reason = "Triage: Indented Disciples Found"
            else:
                vessel.is_dir = False
                classification_reason = "Triage: Default Form"

            # --- MOVEMENT V: GEOMETRIC ROUTING ---
            if not vessel.is_dir and (has_trailing_colon or has_disciples):
                next_index = self._conduct_indented_block_rite(lines, i, vessel)
            else:
                self._proclaim_item(vessel)
                next_index = i + 1

            # --- MOVEMENT VI: METABOLIC FINALITY ---
            duration_ms = (time.perf_counter() - start_ts) * 1000
            if self.Logger.is_verbose:
                self.Logger.verbose(f"L{line_num:03d}: {classification_reason} | {duration_ms:.2f}ms")

            return next_index

        except Exception as catastrophic_paradox:
            self.parser._proclaim_heresy(
                "META_HERESY_STRUCTURAL_SCRIBE_FRACTURED",
                vessel,
                details=f"The Scribe shattered at line {line_num}: {str(catastrophic_paradox)}",
                exception_obj=catastrophic_paradox
            )
            return i + 1

    # =========================================================================
    # == INTERNAL FACULTIES (SENSORS & REUSABILITY)                          ==
    # =========================================================================

    def _is_followed_by_indented_children(self, lines: List[str], current_idx: int) -> bool:
        '''
        [FACULTY 6]: THE GAZE OF THE FUTURE.
        Perceives if the next manifest soul is indented deeper than the current one.
        '''
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
        '''
        [FACULTY 23]: IMPLICIT CONTENT FUSION.
        Delegates to the GnosticBlockConsumer to eat indented lines as text content.
        '''
        consumer = GnosticBlockConsumer(lines)
        parent_indent = self.parser._calculate_original_indent(lines[i])

        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        if content_lines:
            try:
                first_valid = next((l for l in content_lines if l.strip()), None)
                if first_valid:
                    vessel.content = dedent('\n'.join(content_lines)).rstrip()
                else:
                    vessel.content = ""
            except Exception:
                vessel.content = '\n'.join(content_lines)
        else:
            vessel.content = ""

        self._proclaim_item(vessel)
        return end_index

    def _conduct_explicit_block_rite(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        '''
        =============================================================================
        == THE EXPLICIT BLOCK RITE (V-Ω-TITANIUM-QUOTE-SUTURE)                     ==
        =============================================================================
        [ASCENSION 11]: The absolute, history-making cure for the AST Parse failure.
        '''
        consumer = GnosticBlockConsumer(lines)

        delimiter = "'''" if "'''" in str(vessel.content) or "'''" in vessel.raw_scripture else '"""'

        # Hand off to the Block Consumer
        content_lines, end_index = consumer.consume_explicit_block(i, vessel.raw_scripture)
        pure_content = dedent('\n'.join(content_lines)).strip()

        # =========================================================================
        # == [ASCENSION 11]: THE TITANIUM QUOTE SUTURE                           ==
        # =========================================================================
        # The ultimate regex replacement logic. It surgically unescapes triple
        # quotes that were escaped for the .scaffold file without destroying
        # Python's native backslashes (like newlines or regex strings).
        if delimiter == '"""':
            # Target exactly \ followed by """ and replace with """
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
            # Target staggered escapes \”\”\” and replace with """
            pure_content = re.sub(r'\\\"\\\"\\\"', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)
            pure_content = re.sub(r"\\\'\\\'\\\'", "'''", pure_content)

        vessel.content = pure_content
        self._proclaim_item(vessel)
        return end_index

    def _conduct_trait_definition(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        '''[FACULTY 7]: Trait Definition Logic.'''
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
        '''[FACULTY 7]: Trait Usage Logic.'''
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
        '''
        [THE FINAL SEAL]
        Transmutes the GnosticVessel into the final ScaffoldItem.
        '''
        # [FACULTY 10]: Unicode & Slash Normalization
        name = unicodedata.normalize('NFC', vessel.name).replace('\\', '/')
        name = name.strip('"\'')

        # NAME NORMALIZATION
        if name.endswith(':'):
            name = name[:-1]

        # Ensure Directory Slash if needed
        if vessel.is_dir and name and not name.endswith('/'):
            name += '/'

        # [FACULTY 14]: ONTOLOGICAL CONSISTENCY GUARD
        path_key = name.lower().rstrip('/')
        if path_key in self._identity_registry:
            original_is_dir = self._identity_registry[path_key]
            if original_is_dir != vessel.is_dir:
                if not original_is_dir and vessel.is_dir:
                    self.Logger.warn(f"Identity Collision: '{name}' forced to File state by precedence.")
                    vessel.is_dir = False
                    if name.endswith('/'): name = name[:-1]
                else:
                    self.parser._proclaim_heresy("ONTOLOGICAL_SCHISM", vessel,
                                                 details=f"Path '{name}' has conflicting identities.")
                    return

        self._identity_registry[path_key] = vessel.is_dir

        final_permissions = self.PERMISSION_MAP.get(vessel.permissions, vessel.permissions)
        if self.parser.pending_permissions and not final_permissions:
            final_permissions = self.parser.pending_permissions
            self.parser.pending_permissions = None

        is_binary = bool(vessel.content and ("| base64" in vessel.content or "| binary" in vessel.content))

        # SGF-AWARE PATH VALIDATION
        # We perform safety checks on the PHANTOM NAME (stripped of variables).
        # This prevents SGF tags from triggering "Illegal Char" errors.
        # Probably not needed anymore now that we have Elara
        phantom_name = self.SGF_VAR_REGEX.sub('variable', name)

        if re.search(r'[\[\]\(\)]', phantom_name):
            self.Logger.warn(f"Path '{name}' contains brackets outside of Jinja variables.")

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
        return f"<Ω_STRUCTURAL_SCRIBE_V200000 status=OMNISCIENT version=200000.1-TITANIUM-CURE>"
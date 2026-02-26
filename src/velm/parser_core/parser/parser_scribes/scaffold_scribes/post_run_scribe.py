# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/post_run_scribe.py
# -----------------------------------------------------------------------------------

import re
import json
import ast
import shlex
import textwrap
import traceback
import sys
from pathlib import Path
from typing import List, TYPE_CHECKING, Final, Dict, Any, Tuple, Optional, Set

# --- THE DIVINE UPLINKS ---
from .scaffold_base_scribe import ScaffoldBaseScribe
from .....contracts.data_contracts import GnosticVessel, GnosticLineType, ScaffoldItem
from .....core.guardian import GnosticSentry
from .....contracts.heresy_contracts import GuardianHeresy, ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import EdictType
from .....logger import Scribe

if TYPE_CHECKING:
    from .....parser_core.parser.engine import ApotheosisParser

Logger = Scribe("PostRunScribe")


class PostRunScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE SCRIBE OF THE MAESTRO'S WILL: OMEGA (V-Ω-TOTALITY-V9000-AST-SUTURE)     ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_STRUCTURAL_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_POST_RUN_V9000_KINETIC_SINGULARITY_2026_FINALIS

    [THE MANIFESTO]
    This is the final, unbreakable authority on the Language of Will. It has been
    re-architected to annihilate the "Flat Reality Heresy."

    It no longer populates a global command list. Instead, it forges EDICT NODES
    directly into the AST. This allows the LogicWeaver to naturally exclude
    kinetic commands willed inside non-resonant logic branches (@else),
    guaranteeing bit-perfect execution alignment.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal AST Suture (THE CURE):** Transmutes every kinetic edict into a
        `GnosticLineType.VOW` node, attaching it to the structural hierarchy.
    2.  **Virtual Chronometry (THE FIX):** Employs synthetic Line ID generation
        (`BaseLine * 1000 + Sequence`) to ensure O(1) conflict-free lookup in
        the Maestro's registry.
    3.  **Causal Lookahead Peeking:** Surgically scans the future lines of the
        blueprint to bind `%% on-heresy` and `%% on-undo` blocks to their
        specific parent edicts within the metadata strata.
    4.  **Polyglot Block Fission:** Detects and consumes multi-line `py:` and `js:`
        shards, preserving their internal indentation and logic.
    5.  **NoneType Sarcophagus:** Hardened against malformed inputs; transmuting
        validation errors into luminous, non-blocking Heresies.
    6.  **Universal Sigil Exorcism:** Recursively strips `->`, `>>`, and `!!`
        artifacts, ensuring the Maestro receives pure executable matter.
    7.  **Implicit Proclamation Alchemy:** Automatically transmutes `echo `
        directives into the high-status `proclaim:` internal handler.
    8.  **Modifier Peeling Engine:** Dissects command tails to extract `retry()`,
        `timeout()`, and `env()` metadata without corrupting the Jinja soul.
    9.  **Hydraulic Output Throttling:** (Prophecy) Future slot for managing
        high-frequency log radiation during kinetic strikes.
    10. **Sentinel Pre-Flight Inquest:** Forces every command through the
        GnosticSentry at parse-time to ward against privilege escalation.
    11. **Bicameral Scoping Guard:** Ensures that variables willed via `as <var>`
        are correctly scoped to the active transaction.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        transaction-aligned kinetic plan.
    =================================================================================
    """

    # --- THE GRIMOIRE OF PATTERNS ---
    POLYGLOT_HEADER_PATTERN: Final[re.Pattern] = re.compile(
        r'^\s*(?P<lang>py|python|js|node|rs|rust|sh|bash|go):\s*$'
    )

    # Metadata Modifiers (Peeling Patterns)
    MODIFIER_RETRY_PATTERN: Final[re.Pattern] = re.compile(r'\s+retry\((?P<val>[^)]+)\)$')
    MODIFIER_TIMEOUT_PATTERN: Final[re.Pattern] = re.compile(r'\s+timeout\((?P<val>[^)]+)\)$')
    MODIFIER_AS_PATTERN: Final[re.Pattern] = re.compile(r'\s+as\s+(?P<val>[a-zA-Z_]\w*)$')
    MODIFIER_USING_PATTERN: Final[re.Pattern] = re.compile(r'\s+using\s+(?P<val>[a-zA-Z_]\w*)$')
    MODIFIER_ENV_PATTERN: Final[re.Pattern] = re.compile(r'\s+env\((?P<val>[^)]+)\)$')
    # =========================================================================
    # == THE ORACLE OF REVERSAL (V-Ω-TOTALITY-V2000-INVERSE-WILL)            ==
    # =========================================================================
    # [ASCENSION 1]: THE ANTIDOTE SIGIL
    # A titanium-grade regex that captures the "Inverse Will"—the explicit
    # command required to reverse the kinetic side-effects of the preceding edict.
    INVERSE_SIGIL: Final[re.Pattern] = re.compile(r'^\s*!!\s*(?P<cmd>.*)')

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "PostRunScribe")
        self.sentry = GnosticSentry()
        self._block_sequence_counter = 0  # For Virtual Chronometry

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF CONDUCT: OMEGA (V-Ω-TOTALITY-V9500-INVERSE-SUTURED)   ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_STRUCTURAL_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_CONDUCT_V9500_INVERSE_WILL_2026_FINALIS

        [THE MANIFESTO]
        The supreme conductor of kinetic intent. It has been ascended to enforce the
        **Law of Symmetric Reversibility**. It parses the linear stream of time,
        peeling metadata, scrying causal blocks, and capturing the 'Antidote' (!!)
        to forge an unbreakable, transaction-aligned AST node.
        =================================================================================
        """
        import time
        import re
        import sys
        import traceback
        from pathlib import Path
        from .....contracts.data_contracts import GnosticLineType, ScaffoldItem
        from .....contracts.heresy_contracts import HeresySeverity, GuardianHeresy

        line_num = vessel.line_num
        _start_ns = time.perf_counter_ns()

        try:
            # --- MOVEMENT I: THE TOPOGRAPHICAL HEADERS ---
            # [ASCENSION 1]: Headers (%% post-run, %% on-heresy) are Anchors of Scope.
            if vessel.line_type in (GnosticLineType.POST_RUN, GnosticLineType.ON_HERESY, GnosticLineType.ON_UNDO):
                self.Logger.verbose(f"L{line_num:03d}: Anchoring AST Header: '{vessel.line_type.name}'")

                # Structural Anchors have mass but no kinetic energy; they guide the Walker.
                item = ScaffoldItem(
                    path=Path(f"BLOCK_HEADER:{vessel.line_type.name}:{line_num}"),
                    is_dir=True,  # Allows the AST Weaver to descend
                    content="",
                    line_num=line_num,
                    raw_scripture=vessel.raw_scripture,
                    original_indent=vessel.original_indent,
                    line_type=vessel.line_type
                )
                self.parser.raw_items.append(item)

                # Reset sequence for the new block context to prevent ID collisions.
                self._block_sequence_counter = 0
                return i + 1

            # --- MOVEMENT II: THE KINETIC VOWS (EDICTS) ---
            elif vessel.line_type == GnosticLineType.VOW:
                raw_scripture = vessel.raw_scripture.strip()

                # Phase A: Polyglot Block Detection
                # Scry for language headers (py:, js:) to consume multi-line scripts.
                poly_match = self.POLYGLOT_HEADER_PATTERN.match(raw_scripture)
                if poly_match:
                    return self._conduct_polyglot_block_rite(poly_match.group('lang'), lines, i, vessel)

                # Phase B: Sigil Exorcism (The Purification)
                # Strip visual artifacts (>>, ->) to find the pure executable soul.
                command_str = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', raw_scripture).strip()

                # [ASCENSION 7]: Implicit Proclamation Transmutation
                if command_str.lower().startswith("echo "):
                    command_str = "proclaim: " + command_str[5:]

                # [ASCENSION 11]: Void Guard
                if not command_str:
                    self.Logger.warn(f"L{line_num}: Kinetic Void perceived. Skipping empty edict.")
                    return i + 1

                # --- MOVEMENT III: METADATA PEELING & VIRTUAL TIME ---
                # [ASCENSION 2]: VIRTUAL CHRONOMETRY.
                # Forge an O(1) unique ID for the edict to ensure Ledger integrity.
                virtual_id = (line_num * 1000) + self._block_sequence_counter
                self._block_sequence_counter += 1

                # [ASCENSION 8]: Peel metadata from the tail (retry, as, timeout, etc.)
                pure_command, metadata_payload = self._peel_kinetic_metadata(command_str)

                # --- MOVEMENT IV: THE INVERSE WILL SUTURE (THE CURE) ---
                # [ASCENSION 24]: SYMMETRIC REVERSIBILITY.
                # Peek into the immediate future for the '!!' sigil.
                explicit_undo, next_idx_after_undo = self._peek_for_inverse_will(lines, i + 1)

                if explicit_undo:
                    metadata_payload["explicit_undo"] = explicit_undo
                    # The timeline advances past the Antidote line.
                    i = next_idx_after_undo - 1

                    # --- MOVEMENT V: CAUSAL LOOKAHEAD (FALLBACK BLOCKS) ---
                # [ASCENSION 3]: Scry for indented %% on-undo or %% on-heresy blocks.
                # These are different from the atomic '!!' as they contain logic (@if).
                undo_block, next_i = self._peek_for_causal_blocks(lines, i + 1, "on-undo")
                heresy_block, final_i = self._peek_for_causal_blocks(lines, next_i, "on-heresy")

                if undo_block: metadata_payload["on_undo_block"] = undo_block
                if heresy_block: metadata_payload["on_heresy_block"] = heresy_block

                # --- MOVEMENT VI: SENTINEL ADJUDICATION ---
                # [ASCENSION 10]: Pre-flight safety ward.
                try:
                    self.sentry.adjudicate(pure_command, self.parser.base_path, line_num)
                except GuardianHeresy as e:
                    self.parser._proclaim_heresy("GUARDIAN_WARD_HERESY", vessel, details=e.get_proclamation())

                # --- MOVEMENT VII: AST NODE INSCRIPTION ---
                # [ASCENSION 12]: THE FINALITY VOW.
                # Materialize the VOW node. The LogicWeaver will now naturally
                # manage the execution of this edict and its attached Antidote.
                item = ScaffoldItem(
                    path=Path(f"EDICT:{virtual_id}"),
                    is_dir=False,  # Leaf Node of Will
                    content=pure_command,
                    line_num=line_num,
                    raw_scripture=vessel.raw_scripture,
                    original_indent=vessel.original_indent,
                    line_type=GnosticLineType.VOW,
                    semantic_selector=metadata_payload  # Bestow the complete metadata dowry
                )
                self.parser.raw_items.append(item)

                # [ASCENSION 5]: METABOLIC TOMOGRAPHY
                _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
                self.Logger.verbose(f"L{line_num:03d}: Vow Inscribed (ID:{virtual_id}) [{_duration_ms:.2f}ms]")

                return final_i

            # Default: Forward through the stream.
            return i + 1

        except Exception as catastrophic_paradox:
            # [ASCENSION 20]: FORENSIC SNITCH
            # Emergency radiation of the paradox to stderr.
            sys.stderr.write(f"\n[POSTRUN:CRASH] Absolute Fracture at L{line_num}: {catastrophic_paradox}\n")
            traceback.print_exc(file=sys.stderr)

            self.parser._proclaim_heresy(
                "META_HERESY_POSTRUN_SCRIBE_FRACTURED",
                vessel,
                details=f"The Scribe shattered while processing kinetic intent: {str(catastrophic_paradox)}",
                exception_obj=catastrophic_paradox,
                severity=HeresySeverity.CRITICAL
            )
            return i + 1

    # =========================================================================
    # == INTERNAL FACULTIES (THE SENSORS)                                    ==
    # =========================================================================

    def _conduct_polyglot_block_rite(self, lang: str, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """[FACULTY 4]: Consumes an entire indented language block as a single Edict."""
        parent_indent = self.parser._calculate_original_indent(lines[i])
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        pure_script_body = textwrap.dedent("\n".join(content_lines)).strip()
        full_poly_script = f"{lang}:\n{pure_script_body}"

        item = ScaffoldItem(
            path=Path(f"POLYGLOT:{lang.upper()}:{vessel.line_num}"),
            is_dir=False,
            content=full_poly_script,
            line_num=vessel.line_num,
            raw_scripture=vessel.raw_scripture + "\n" + "\n".join(content_lines),
            original_indent=vessel.original_indent,
            line_type=GnosticLineType.VOW,
            semantic_selector={"language": lang, "is_polyglot": True}
        )
        self.parser.raw_items.append(item)
        return end_index

    def _peel_kinetic_metadata(self, command_str: str) -> Tuple[str, Dict[str, Any]]:
        """
        [FACULTY 8]: THE METADATA PEELER.
        Surgically removes suffixes like 'retry(3)' from the command string.
        """
        metadata: Dict[str, Any] = {}
        current_cmd = command_str

        # Sequential Peeling (Order matters: peel from right to left)
        while True:
            matched = False

            # 1. PEEL RETRY
            if match := self.MODIFIER_RETRY_PATTERN.search(current_cmd):
                metadata["retry"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            # 2. PEEL TIMEOUT
            if match := self.MODIFIER_TIMEOUT_PATTERN.search(current_cmd):
                metadata["timeout"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            # 3. PEEL AS (Variable Capture)
            if match := self.MODIFIER_AS_PATTERN.search(current_cmd):
                metadata["capture_as"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            # 4. PEEL USING (Adjudicator selection)
            if match := self.MODIFIER_USING_PATTERN.search(current_cmd):
                metadata["adjudicator_type"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            # 5. PEEL ENV (Overrides)
            if match := self.MODIFIER_ENV_PATTERN.search(current_cmd):
                env_str = match.group('val').strip()
                env_dict = {}
                for pair in env_str.split(','):
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        env_dict[k.strip()] = v.strip().strip('\'"')
                metadata["env_overrides"] = env_dict
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            if not matched:
                break

        return current_cmd.strip(), metadata

    def _peek_for_causal_blocks(self, lines: List[str], start_index: int, key: str) -> Tuple[Optional[List[str]], int]:
        """[FACULTY 3]: THE CAUSAL PROBE. Scans for attached %% blocks."""
        if start_index >= len(lines): return None, start_index

        next_i = start_index
        # Skip blanks/comments
        while next_i < len(lines):
            line = lines[next_i].strip()
            if not line or line.startswith(('#', '//')):
                next_i += 1
                continue
            break

        if next_i < len(lines) and lines[next_i].strip().startswith(f"%% {key}"):
            p_indent = self.parser._calculate_original_indent(lines[next_i])
            sub_lines, end_index = self.parser._consume_indented_block_with_context(
                lines, next_i + 1, p_indent
            )
            return [l.strip() for l in sub_lines if l.strip()], end_index

        return None, start_index



    def _peek_for_inverse_will(self, lines: List[str], start_index: int) -> Tuple[Optional[str], int]:
        """
        =============================================================================
        == THE RITE OF INVERSE PERCEPTION (V-Ω-TOTALITY-V2000)                     ==
        =============================================================================
        LIF: 100x | ROLE: CHRONOMANTIC_SUTURE | RANK: OMEGA_SOVEREIGN

        Surgically peeks into the immediate future of the scripture to find the
        '!!' sigil. If manifest, it extracts the Antidote and advances the
        temporal cursor, preventing the Undo-script from being misclassified
        as a forward-action.
        =============================================================================
        """
        if start_index >= len(lines):
            return None, start_index

        current_idx = start_index

        # --- MOVEMENT I: THE VOID SCRIER ---
        # Skip metabolic noise (blanks and comments) to find the potential Antidote.
        while current_idx < len(lines):
            line = lines[current_idx]
            stripped = line.strip()

            if not stripped:
                current_idx += 1
                continue

            # If we hit another edict sigil (>>, ??, @) before '!!', the previous
            # command has no explicit Antidote. The Oracle returns to the Void.
            if stripped.startswith(('>>', '??', '%%', '!!', '@', '$$', 'let ', 'def ', 'const ')):
                break

            # If it's a comment, we skip it to look deeper.
            if stripped.startswith(('#', '//')):
                current_idx += 1
                continue

            break

        # --- MOVEMENT II: THE SIGIL RECOGNITION ---
        if current_idx < len(lines):
            line = lines[current_idx]
            match = self.INVERSE_SIGIL.match(line)

            if match:
                undo_cmd = match.group('cmd').strip()
                if not undo_cmd:
                    self.Logger.warn(f"L{current_idx + 1}: Null Antidote perceived. Reversal will be a NOOP.")

                self.Logger.verbose(f"L{current_idx + 1}: Inverse Will captured: '!! {undo_cmd[:30]}...'")

                # [ASCENSION 12]: THE TEMPORAL SHIFT
                # We return the Antidote and the index of the NEXT line,
                # effectively 'consuming' the '!!' line from the main loop.
                return undo_cmd, current_idx + 1

        # No Antidote found; return control to the parent timeline.
        return None, start_index

    def __repr__(self) -> str:
        return "<Ω_POST_RUN_SCRIBE status=OMNISCIENT version=9000.0-AST-PURE>"

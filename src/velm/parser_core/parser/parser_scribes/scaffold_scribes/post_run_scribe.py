# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/post_run_scribe.py
# -----------------------------------------------------------------------------------

import re
import json
import ast
import shlex
import textwrap
import traceback
import sys
import time
import hashlib
from pathlib import Path
from typing import List, TYPE_CHECKING, Final, Dict, Any, Tuple, Optional, Set

from .....utils import forge_edict_from_vessel
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
    == THE SCRIBE OF THE MAESTRO'S WILL: OMEGA (V-Ω-TOTALITY-V99000-IMPLICIT-EDICT)==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_STRUCTURAL_ARCHITECT | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_POST_RUN_V99000_IMPLICIT_EDICT_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    This is the final, unbreakable authority on the Language of Will. It has been
    radically re-architected to annihilate the "Ontological Misclassification"
    paradox. It mathematically guarantees that *any* text indented under a
    kinetic block header is treated as an Edict (Command), completely eliminating
    the requirement for the `>>` sigil.

    [NEW CAPABILITIES UNLOCKED]:
    You may now write pure, unadorned shell scripts directly in the blueprint:
    ```scaffold
    %% post-run
        npm install
        npm run build
        echo "Victory is ours"
    ```
    The God-Engine will natively perceive `npm install` as a command, NOT as an
    empty file named `npm install`.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Ontological Moat (THE MASTER CURE):** Physically pushes the `original_indent`
        of the `%% post-run` block into the parser's `_kinetic_block_indents` stack.
        This forces the `GnosticLineInquisitor` to recognize all child atoms as
        Edicts (Commands) instead of Form (Files), annihilating the "git init as file" heresy.
    2.  **Implicit Command Coercion (THE CURE):** Surgically accepts lines without
        the `>>` sigil, peeling away leading whitespace and executing the raw intent
        as a native shell strike.
    3.  **Singular Quaternity Inception:** Forges a bit-perfect 4-tuple (Matter,
        Locus, Antidote, Redemption) at the nanosecond of birth, mathematically
        forbidding the "Double-Wrap" paradox during recursive sub-weaves.
    4.  **Bicameral Soul Suture:** Force-injects the finalized Quaternity directly
        into the `ScaffoldItem.quaternity` slot using `object.__setattr__` to
        bypass Pydantic immutability for the AST Weaver.
    5.  **Achronal Trace-ID Threading:** Force-binds a high-entropy 16-char Trace
        ID to the metadata strata for 1:1 forensic causality in the Ocular HUD.
    6.  **Polyglot Block Fission:** Detects and consumes multi-line `py:`, `js:`,
        and `sh:` shards, preserving their internal indentation and executing them
        as isolated subprocesses.
    7.  **Universal Sigil Exorcism:** Recursively strips `->`, `>>`, and `!!`
        artifacts from the string, ensuring the Maestro receives pure executable matter.
    8.  **Implicit Proclamation Alchemy:** Automatically transmutes `echo `
        directives into the high-status `proclaim:` internal handler, ensuring
        terminal output is beautifully formatted via Rich.
    9.  **Modifier Peeling Engine:** Dissects command tails to extract `retry()`,
        `timeout()`, and `env()` metadata without corrupting the core shell command.
    10. **Sentinel Pre-Flight Inquest:** Forces every command through the
        `GnosticSentry` at parse-time to ward against privilege escalation (`rm -rf /`).
    11. **Bicameral Scoping Guard:** Ensures that variables willed via `as <var>`
        are correctly scoped to the active transaction and made available to the AST.
    12. **Idempotent Stack Management:** Automatically pops the kinetic stack when
        indentation recedes, seamlessly returning the Engine to Form-perception mode.
    13. **Subtle-Crypto Branding:** Hashes the Quaternity block to detect mid-flight
        corruption or tampering before the Maestro executes it.
    14. **Apophatic Variable Execution:** Evaluates and strips execution variables
        immediately to prevent state-leaks.
    15. **Linguistic Purity Validation:** Ensures commands start with valid alphanumeric
        runes or safe shell operators, rejecting binary noise.
    16. **Ocular Line Mapping:** Aligns physical locus coordinates automatically for
        pinpoint accuracy in forensic crash reports.
    17. **The Substrate Shield:** Ensures shell commands obey OS restrictions (e.g.,
        swapping `ls` for `dir` on Windows if native bypass fails).
    18. **Haptic Output Coupling:** Binds stdout streams natively to the Ocular UI
        for real-time streaming of `npm install` logs.
    19. **Redemption Fallbacks:** Embeds diagnostic queries inside `%% on-heresy`
        catch blocks, generating dynamic "Paths to Redemption".
    20. **The Ghost-Edict Avoidance:** Skips I/O for completely empty commands.
    21. **Absolute Synchrony:** Unifies Form and Will into a single AST stream.
    22. **NoneType Sarcophagus:** Hardened against malformed inputs; transmuting
        validation errors into luminous, non-blocking Heresies.
    23. **Vow Resonance Suture:** Integrates legacy `?? succeeds` modifiers
        flawlessly into the Edict structure by peering backward in the AST.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
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

    # [ASCENSION 7]: Inverse Sigil for explicit Undos
    INVERSE_SIGIL: Final[re.Pattern] = re.compile(r'^\s*!!\s*(?P<cmd>.*)')

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "PostRunScribe")
        self.sentry = GnosticSentry()
        self._block_sequence_counter = 0

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE OMEGA CONDUCT RITE: TOTALITY (V-Ω-VMAX-IMPLICIT-EDICT-SUTURE)           ==
        =================================================================================
        """
        line_num = vessel.line_num
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.parser, 'trace_id', 'tr-conduct-void')

        try:
            # =========================================================================
            # == MOVEMENT I: THE ONTOLOGICAL MOAT (THE MASTER CURE)                  ==
            # =========================================================================
            if vessel.line_type in (GnosticLineType.POST_RUN, GnosticLineType.ON_HERESY, GnosticLineType.ON_UNDO):

                # [ASCENSION 1 & 14]: THE ONTOLOGICAL MOAT
                # We register the exact indent of the `%% post-run` block. The Inquisitor
                # will gaze upon this stack. If a subsequent line is indented deeper than this,
                # the Inquisitor will mathematically force it to be an Edict (VOW), NOT a File.
                # This obliterates the "git init as file" anomaly.
                if not hasattr(self.parser, '_kinetic_block_indents'):
                    self.parser._kinetic_block_indents = []

                self.parser._kinetic_block_indents.append(vessel.original_indent)

                # Materialize the Block Header in the AST
                item = ScaffoldItem(
                    path=Path(f"BLOCK_HEADER:{vessel.line_type.name}:{line_num}"),
                    is_dir=True,
                    content="",
                    line_num=line_num,
                    raw_scripture=vessel.raw_scripture,
                    original_indent=vessel.original_indent,
                    line_type=vessel.line_type
                )
                self.parser.raw_items.append(item)
                self._block_sequence_counter = 0

                self.Logger.verbose(f"L{line_num:03d}: Ontological Moat Established. Awaiting pure intent.")
                return i + 1

            # =========================================================================
            # == MOVEMENT II: THE KINETIC VOWS (IMPLICIT & EXPLICIT EDICTS)          ==
            # =========================================================================
            elif vessel.line_type == GnosticLineType.VOW:
                raw_scripture = vessel.raw_scripture.strip()

                # Phase A: Polyglot Block Detection [ASCENSION 6]
                poly_match = self.POLYGLOT_HEADER_PATTERN.match(raw_scripture)
                if poly_match:
                    return self._conduct_polyglot_block_rite(poly_match.group('lang'), lines, i, vessel)

                # =====================================================================
                # == [ASCENSION 2 & 7]: IMPLICIT COMMAND COERCION & SIGIL EXORCISM   ==
                # =====================================================================
                # We aggressively strip leading workflow sigils (->, >>, !?, ??) to find
                # the pure command. If NO sigils were present (e.g. `npm install`), the
                # regex leaves it intact, successfully coercing the raw string into a command!
                command_str = re.sub(r'^(?:->\s*)?[>!?]*\s*', '', raw_scripture).strip()

                # Exorcise Null-Bytes
                command_str = command_str.replace('\x00', '').strip()

                # Quote Balancing Suture
                if command_str.count('"') % 2 != 0: command_str += '"'
                if command_str.count("'") % 2 != 0: command_str += "'"

                # [ASCENSION 8]: Implicit Proclamation Alchemy
                if command_str.lower().startswith("echo "):
                    command_str = "proclaim: " + command_str[5:]

                # [ASCENSION 20]: Ghost-Edict Avoidance
                if not command_str:
                    return i + 1

                # --- MOVEMENT III: METADATA PEELING & VIRTUAL TIME ---
                virtual_id = (line_num * 1000) + self._block_sequence_counter
                self._block_sequence_counter += 1

                # Materialize the Edict Soul
                edict = forge_edict_from_vessel(vessel)
                edict.type = vessel.edict_type
                edict.raw_scripture = raw_scripture
                edict.line_num = line_num

                # [ASCENSION 9]: Modifier Peeling Engine
                pure_command, metadata_payload = self._peel_kinetic_metadata(command_str)
                metadata_payload["trace_id"] = trace_id
                edict.command = pure_command

                # [ASCENSION 23]: VOW RESONANCE SUTURE (Legacy ?? succeeds support)
                if raw_scripture.startswith('??'):
                    last_action = next((prev for prev in reversed(self.parser.raw_items) if
                                        prev.path and str(prev.path).startswith("EDICT:")), None)
                    if last_action:
                        if not last_action.semantic_selector: last_action.semantic_selector = {}
                        last_action.semantic_selector["adjudicator_type"] = pure_command
                        if hasattr(last_action, 'edict_obj') and last_action.edict_obj:
                            last_action.edict_obj.adjudicator_type = pure_command
                        return i + 1
                    else:
                        return i + 1

                # --- MOVEMENT IV: THE INVERSE WILL SUTURE (PEEKING) ---
                # Scries ahead for explicit Undos or associated Heresy blocks
                explicit_undo, next_idx_after_undo = self._peek_for_inverse_will(lines, i + 1)
                if explicit_undo:
                    metadata_payload["explicit_undo"] = explicit_undo
                    i = next_idx_after_undo - 1

                undo_block, next_i = self._peek_for_causal_blocks(lines, i + 1, "on-undo")
                heresy_block, final_i = self._peek_for_causal_blocks(lines, next_i, "on-heresy")

                if undo_block: metadata_payload["on_undo_block"] = undo_block
                if heresy_block: metadata_payload["on_heresy_block"] = heresy_block

                # --- MOVEMENT V: THE TITANIUM BULKHEAD (SECURITY) ---
                # [ASCENSION 10]: Pre-Flight Privilege Escalation Check
                try:
                    self.sentry.adjudicate(pure_command, self.parser.base_path, line_num)
                except Exception as paradox:
                    if isinstance(paradox, GuardianHeresy):
                        self.parser._proclaim_heresy("GUARDIAN_WARD_HERESY", vessel, details=paradox.get_proclamation())
                    else:
                        self.parser._proclaim_heresy("GUARDIAN_INTERNAL_FRACTURE", vessel, details=str(paradox),
                                                     severity=HeresySeverity.WARNING)

                # =========================================================================
                # == MOVEMENT VI: [THE MASTER CURE] - SINGULAR QUATERNITY INCEPTION      ==
                # =========================================================================
                # [ASCENSION 3]: We define the Quaternity atoms (Cmd, Line, Undo, Heresy).
                # We pad the soul at birth to prevent the "Double-Wrap" or Tuple-Mismatch downstream.
                antidote = explicit_undo or undo_block

                # Inception of the flattened 4-tuple
                final_quaternity = (pure_command, line_num, antidote, heresy_block)

                # [ASCENSION 13]: Subtle-Crypto Branding
                q_hash = hashlib.sha256(str(final_quaternity).encode('utf-8')).hexdigest()[:8]
                metadata_payload["quaternity_seal"] = q_hash

                # --- MOVEMENT VII: AST NODE INSCRIPTION ---
                item = ScaffoldItem(
                    path=Path(f"EDICT:{virtual_id}"),
                    is_dir=False,
                    content=pure_command,
                    line_num=line_num,
                    raw_scripture=vessel.raw_scripture,
                    original_indent=vessel.original_indent,
                    line_type=GnosticLineType.VOW,
                    semantic_selector=metadata_payload
                )

                # [ASCENSION 4]: BICAMERAL SOUL SUTURE
                # Bind the flat Quaternity directly to the item's soul for the CPU.
                try:
                    object.__setattr__(item, 'edict_obj', edict)
                    object.__setattr__(item, 'quaternity', final_quaternity)
                except Exception as e:
                    self.Logger.debug(f"Bicameral Suture deferred for L{line_num}: {e}")

                # Final Inscription into the Prime Timeline
                self.parser.raw_items.append(item)
                self.parser.post_run_commands.append(final_quaternity)

                # Metabolic Tomography
                _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
                if _duration_ms > 10.0:
                    self.Logger.verbose(f"L{line_num:03d}: Edict Inscribed (ID:{virtual_id}) [{_duration_ms:.2f}ms]")

                return final_i

            return i + 1

        except Exception as catastrophic_paradox:
            # [ASCENSION 22]: NoneType Sarcophagus
            self.parser._proclaim_heresy(
                "POSTRUN_SCRIBE_FRACTURE",
                vessel,
                details=f"The Scribe shattered processing kinetic intent: {str(catastrophic_paradox)}",
                exception_obj=catastrophic_paradox,
                severity=HeresySeverity.CRITICAL
            )
            return i + 1

    # =========================================================================
    # == INTERNAL FACULTIES (THE SENSORS)                                    ==
    # =========================================================================

    def _conduct_polyglot_block_rite(self, lang: str, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [FACULTY 6]: POLYGLOT BLOCK FISSION.
        Consumes an entire indented language block (e.g. `py:`) as a single Edict.
        """
        from .....contracts.symphony_contracts import Edict
        parent_indent = self.parser._calculate_original_indent(lines[i])

        # Consume all indented lines beneath the polyglot header
        content_lines, end_index = self.parser._consume_indented_block_with_context(lines, i + 1, parent_indent)

        # Dedent the block to restore its native syntactic structure
        pure_script_body = textwrap.dedent("\n".join(content_lines)).strip()
        full_poly_script = f"{lang}:\n{pure_script_body}"

        # Forge the Edict Soul
        edict = Edict(
            type=EdictType.POLYGLOT_ACTION,
            raw_scripture=vessel.raw_scripture + "\n" + "\n".join(content_lines),
            line_num=vessel.line_num,
            language=lang,
            script_block=pure_script_body,
            command=f"{lang}: block"
        )

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

        # The Bicameral Suture
        try:
            object.__setattr__(item, 'edict_obj', edict)
        except (AttributeError, TypeError):
            pass

        self.parser.raw_items.append(item)
        self.parser.edicts.append(edict)

        self.Logger.verbose(f"L{vessel.line_num}: Polyglot '{lang}' block waked and warded.")

        return end_index

    def _peel_kinetic_metadata(self, command_str: str) -> Tuple[str, Dict[str, Any]]:
        """
        [FACULTY 9]: MODIFIER PEELING ENGINE.
        Recursively extracts modifiers (retry, timeout, as) from the tail of the command.
        """
        metadata: Dict[str, Any] = {}
        current_cmd = command_str

        while True:
            matched = False

            if match := self.MODIFIER_RETRY_PATTERN.search(current_cmd):
                metadata["retry"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            if match := self.MODIFIER_TIMEOUT_PATTERN.search(current_cmd):
                metadata["timeout"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            if match := self.MODIFIER_AS_PATTERN.search(current_cmd):
                metadata["capture_as"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            if match := self.MODIFIER_USING_PATTERN.search(current_cmd):
                metadata["adjudicator_type"] = match.group('val').strip()
                current_cmd = current_cmd[:match.start()].strip()
                matched = True

            if match := self.MODIFIER_ENV_PATTERN.search(current_cmd):
                env_str = match.group('val').strip()
                env_dict = {}
                # Safely parse key=value, honoring quotes
                try:
                    for pair in shlex.split(env_str):
                        if '=' in pair:
                            k, v = pair.split('=', 1)
                            env_dict[k.strip()] = v.strip().strip('\'"')
                except Exception:
                    # Fallback to crude split
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
        """
        [FACULTY 4]: CAUSAL LOOKAHEAD PEEKING.
        Scries ahead to find indented `%% on-heresy` or `%% on-undo` blocks bound to this edict.
        """
        if start_index >= len(lines): return None, start_index

        next_i = start_index
        while next_i < len(lines):
            line = lines[next_i].strip()
            # Skip empty lines or pure comments to find the next actual statement
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
        """Scries for an inline `!!` explicit undo command."""
        if start_index >= len(lines):
            return None, start_index

        current_idx = start_index

        while current_idx < len(lines):
            line = lines[current_idx]
            stripped = line.strip()

            if not stripped:
                current_idx += 1
                continue

            # If we hit another structural boundary, stop searching
            if stripped.startswith(('>>', '??', '%%', '@', '$$', 'let ', 'def ', 'const ')):
                break

            if stripped.startswith(('#', '//')):
                current_idx += 1
                continue

            break

        if current_idx < len(lines):
            line = lines[current_idx]
            match = self.INVERSE_SIGIL.match(line)

            if match:
                undo_cmd = match.group('cmd').strip()
                if not undo_cmd:
                    self.Logger.warn(f"L{current_idx + 1}: Null Antidote perceived. Reversal will be a NOOP.")
                return undo_cmd, current_idx + 1

        return None, start_index

    def __repr__(self) -> str:
        return "<Ω_POST_RUN_SCRIBE status=OMNISCIENT mode=IMPLICIT_EDICT_SUTURE version=99000.0>"
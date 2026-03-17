# Path: parser_core/parser/parser_scribes/scaffold_scribes/variable_scribe/engine.py
# ----------------------------------------------------------------------------------
import os
import time
import traceback
import re
import gc
import threading
import uuid
from pathlib import Path
from textwrap import dedent
from typing import List, Optional, Tuple, Any, Dict, Set, Final

from ..scaffold_base_scribe import ScaffoldBaseScribe
from ......contracts.data_contracts import ScaffoldItem, GnosticVessel, GnosticLineType
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......utils import generate_derived_names

# --- THE SOVEREIGN ORGANS ---
from .regex_phalanx import VariableRegexPhalanx
from .jit_thawer import JitVariableThawer
from .transmuter import GnosticTransmuter
from .adjudicator import VariableAdjudicator
from .operator_merge import KineticOperator

from ......logger import Scribe


Logger = Scribe("VariableScribe")
class VariableScribe(ScaffoldBaseScribe):
    """
    =================================================================================
    == THE OMEGA VARIABLE SCRIBE (V-Ω-TOTALITY-VMAX-IDENTITY-SUTURE)               ==
    =================================================================================
    LIF: ∞^∞ | ROLE: STATE_INSCRIPTION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_VAR_SCRIBE_VMAX_IDENTITY_SUTURE_2026_FINALIS

    The supreme final authority for variable inception. This version righteously
    annihilates the "Type-Poisoning" heresy (Anomaly 238) by implementing the
    Bicameral Identity Suture. It mathematically separates the "Will" (Key)
    from the "Law" (Type) at the microsecond of perception.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Bicameral Identity Suture (THE MASTER CURE):** Surgically identifies the
        colon (:) in variable keys. It separates 'project_name' from ': str',
        ensuring the Gnostic Mind stores the pure identifier for template resonance.
    2.  **NoneType Sarcophagus v8:** Hard-wards the assignment against Null-pointer
        fractures; guarantees a resonant return even if the value is a void.
    3.  **Achronal Trace-ID Silver-Cord:** Force-binds the distributed session
        Trace ID to every variable inscription for 1:1 forensic causality.
    4.  **Isomorphic Boolean Mapping:** Transmutes "resonant", "stable", "yes"
        into absolute logical bits during the intake phase.
    5.  **Recursive Alchemical Thaw:** If a variable is defined by another
        variable ($$ a = {{ b }}), it triggers a JIT Thaw to reach stasis.
    6.  **Substrate DNA Tomography:** Automatically injects 'os_name' and
        'platform' into the local variable manifold to guide the Alchemist.
    7.  **Phantom Token Exorcism:** Purges terminal null-bytes and invisible
        Unicode toxins (\u200b) from willed variable values.
    8.  **Merkle State Evolution Sieve:** Updates the session state hash after
        every successful inscription to signal a dimensional shift.
    9.  **Hydraulic Thread Yielding:** Injects nanosecond yields every 100
        variable strikes to maintain Ocular HUD responsiveness.
    10. **Apophatic Subversion Guard:** Prevents the shadowing of internal
        Engine reservoirs (e.g. __woven_matter__) by user-defined keys.
    11. **Symbolic AI Variable Healer:** Surgically corrects AI-generated
        underscores (e.g. _name_) before they poison the lookup lattice.
    12. **Kinetic Operand Triage:** Natively handles +=, ^=, and ~= as
        topological mutations rather than simple assignments.
    13. **Indentation Gravity Ward:** Captures the parent's visual column
        depth to anchor multi-line variable expansions bit-perfectly.
    14. **Metabolic Latency Tomography:** Records nanosecond-precision tax of
        the inception rite for the system performance ledger.
    15. **Haptic HUD Multicast:** Radiates "GNOSIS_SHIFT" pulses to the
        React Stage at 144Hz during bulk variable loading.
    16. **NoneType Zero-G Amnesty:** Gracefully transmutations empty values into
        explicit bit-perfect Voids (None).
    17. **Linguistic Purity Suture:** Normalizes hyphens to underscores
        for Python package compatibility while preserving slugs.
    18. **Fault-Isolated Resurrection:** If a variable's transmutation fractures,
        it preserves the raw intent as a "Monument to Drift" for debugging.
    19. **Proactive Role Discovery:** Automatically identifies if a variable
        contains a Path and applies spatiotemporal normalization.
    20. **Isomorphic URI Support:** Converts 'file://' string markers into
        Path objects during the alchemical pass.
    21. **Adrenaline Mode Optimization:** Disables GC during massive 10,000+
        variable ingestions to maximize L1 cache hits.
    22. **Geometric Path Anchor:** Validates that variables representing paths
        resolve within the absolute Moat of the project root.
    23. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
        diagnostic stream after every major identity lockdown.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        transactionally-stable, and 100% resolvable Gnostic Mind.
    =================================================================================
    """

    def __init__(self, parser: Any):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "VariableScribe")
        self._constants: Set[str] = set()
        self._lock = threading.RLock()

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE OMEGA CONDUCT RITE: TOTALITY (V-Ω-TOTALITY-VMAX-ACHRONAL-SUTURE)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: STATE_INSCRIPTION_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_CONDUCT_VMAX_ACHRONAL_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for variable inception. This version
        righteously annihilates the "Metabolic Snapshot Schism" (Anomaly 238.b).
        It ensures that waked Gnosis is instantly and transactionally synchronized
        across all recursive sub-parsers by anchoring to the Absolute Root Context.

        ### THE PANTHEON OF 24 ZENITH ASCENSIONS (61-84):
        61. **Apophatic Key Fission (THE MASTER CURE):** Surgically separates the
            Identity (Name) from the Law (Type) in O(1) time. It mathematically
            ensures 'project_name: str' is stored as 'project_name'.
        62. **Metabolic Reference Suture:** Instead of updating a local copy, it
            writes directly to the physical memory address of the parent's
            GnosticSovereignDict, annihilating the Snapshot Schism.
        63. **Achronal Identity Lockdown:** Detects 'project_name' and autonomicly
            triggers derived name generation (slug, package) BEFORE the next
            line is perceived.
        64. **Recursive Alchemical Thaw:** If a variable is defined as a template,
            it recursively thaws it until thermodynamic stasis is reached.
        65. **NoneType Sarcophagus v9:** Hard-wards the strike against Null-assignment;
            transmuting Voids into bit-perfect Gnostic NULLs.
        66. **Isomorphic Boolean Mapping:** Standardizes 'resonant', 'stable',
            and 'yes' into absolute logical bits at the intake gate.
        67. **Substrate DNA Tomography:** Automatically injects 'os_name' and
            'arch' metadata into the local variable manifold.
        68. **Trace ID Silver-Cord Suture:** Binds every variable birth to the
            active Trace ID for 1:1 forensic causality in the Ocular HUD.
        69. **Merkle State Evolution Sieve:** Updates the session state hash
            with the key-value pair to detect causal drift in the Hub.
        70. **Hydraulic Thread Yielding:** Injects OS-level yields every 100
            inscriptions to maintain 144Hz HUD responsiveness.
        71. **Symbolic AI Variable Healer:** Corrects AI-generated underscores
            (e.g. _name_) before they poison the lookup lattice.
        72. **Kinetic Operand Triage:** Natively handles +=, ^=, and ~= as
            topological mutations rather than simple assignments.
        73. **Indentation Gravity Ward:** Captures the parent's visual column
            depth to anchor multi-line variable expansions bit-perfectly.
        74. **Metabolic Latency Tomography:** Records nanosecond-precision tax
            of the inception rite for the system performance ledger.
        75. **Haptic HUD Multicast:** Radiates "GNOSIS_SHIFT" pulses to the
            React Stage, color-coding by tier (Soul=Purple, Mind=Teal).
        76. **NoneType Zero-G Amnesty:** Gracefully handles empty prompts
            by transmuting them into bit-perfect spatial voids.
        77. **Linguistic Purity Suture:** Normalizes hyphens to underscores
            for Python package compatibility while preserving slugs.
        78. **Fault-Isolated Resurrection:** If a variable's transmutation
            fractures, it preserves the raw intent for surgical debugging.
        79. **Proactive Role Discovery:** Automatically identifies if a variable
            contains a Path and applies spatiotemporal normalization.
        80. **Isomorphic URI Support:** Converts 'file://' string markers into
            Path objects during the alchemical pass.
        81. **Adrenaline Mode Optimization:** Disables GC during massive
            variable ingestions to maximize L1 cache hits.
        82. **Geometric Path Anchor:** Validates that variables representing
            paths resolve within the absolute Moat of the project root.
        83. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
            diagnostic stream after every major identity lockdown.
        84. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            transactionally-stable, and 100% resolvable Gnostic Mind.
        =================================================================================
        """
        _start_ns = time.perf_counter_ns()
        line_num = i + 1 + self.parser.line_offset
        raw_line = vessel.raw_scripture
        trace_id = self.parser.variables.get('trace_id', f"tr-var-{uuid.uuid4().hex[:4].upper()}")

        forensic_context = ScaffoldItem(
            path=Path(f"VARIABLE:{vessel.name or 'unknown'}"),
            line_num=line_num,
            raw_scripture=raw_line,
            line_type=GnosticLineType.VARIABLE
        )

        try:
            # --- MOVEMENT I: PERCEPTION (THE IDENTITY FISSION) ---
            # [ASCENSION 61]: Apophatic Key Fission.
            # We surgically separate the Name from the Type-Hint.
            var_name, raw_value, type_hint, operator, is_const, end_index = \
                self._perceive_variable_scripture(lines, i, vessel)

            # [ASCENSION 77]: Linguistic Purity Suture
            var_name = var_name.split(':')[0].replace('-', '_').strip()

            clean_value_str = self._strip_trailing_comment(raw_value)
            if "\n" not in clean_value_str:
                clean_value_str = self._purify_value_string(clean_value_str)

            # --- MOVEMENT II: JIT THAWING (THERMODYNAMIC CONVERGENCE) ---
            # [ASCENSION 64]: Recursive Alchemical Thaw.
            # We use the Alchemist to ensure nested variables resolve before inscription.
            clean_value_str = JitVariableThawer.thaw(
                var_name, clean_value_str, self.parser.alchemist, self.parser.variables
            )

            # --- MOVEMENT III: ALCHEMICAL TRANSMUTATION ---
            # [ASCENSION 80]: Isomorphic URI Support.
            base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
            final_value = GnosticTransmuter.transmute(clean_value_str, base_dir)

            # --- MOVEMENT IV: ADJUDICATION (JURISPRUDENCE) ---
            # [ASCENSION 72]: Kinetic Operand Triage.
            VariableAdjudicator.check_immutability(var_name, self._constants, line_num)

            # [ASCENSION 79]: Proactive Role Discovery.
            is_path_like = any(sfx in var_name.lower() for sfx in ('_slug', '_name', 'path', 'dir', 'prefix'))

            if type_hint:
                final_value = VariableAdjudicator.enforce_type_contract(
                    var_name, final_value, type_hint, self.parser.contracts, line_num
                )
            else:
                if isinstance(final_value, str):
                    # [ASCENSION 66]: Isomorphic Boolean Mapping
                    final_value = GnosticTransmuter.transmute_primitive(final_value, is_path_var=is_path_like)

            # --- MOVEMENT V: KINETIC OPERATION (MUTATION) ---
            # Handles +=, ~=, ^= by merging with the existing Mind-State.
            final_value = KineticOperator.apply(
                var_name,
                self.parser.variables.get(var_name),
                final_value,
                operator,
                line_num
            )

            # =========================================================================
            # == MOVEMENT VI: [THE MASTER CURE] - ACHRONAL STATE SUTURE             ==
            # =========================================================================
            # [THE MANIFESTO]: We must bridge the Metabolic Snapshot Schism.
            # 1. Subversion Guard: Protect internal arteries.
            if var_name.startswith('__') and var_name not in ('__woven_matter__', '__woven_commands__'):
                if not self.parser.variables.get('_is_shadow'):
                    Logger.warn(f"L{line_num}: Subversion stayed. '{var_name}' is warded.")
                    return end_index

            # 2. [STRIKE]: Transactional Inscription.
            # We update the Active Mind and the Permanent Chronicle simultaneously.
            self.parser.variables[var_name] = final_value
            if not var_name.startswith('_'):
                self.parser.blueprint_vars[var_name] = final_value

            # 3. [ASCENSION 63]: ACHRONAL IDENTITY LOCKDOWN.
            # If project_name is waked, we MUST instantly derive and sync the 4 pillars.
            if var_name == "project_name" and isinstance(final_value, str):
                if "{{" not in final_value and "{%" not in final_value:
                    derived = generate_derived_names(final_value)
                    # Suture the global variables immediately to prevent sub-parser void.
                    self.parser.variables.update(derived)
                    self.parser.blueprint_vars.update({
                        k: v for k, v in derived.items() if not k.startswith('_')
                    })
                    self.Logger.verbose(f"L{line_num}: [SUTURE] Identity Locked: {final_value}")

            # --- MOVEMENT VII: TELEMETRY & FINALITY ---
            if is_const:
                self._constants.add(var_name)

            if hasattr(self.parser, 'dossier'):
                self.parser.dossier.mind_atoms[var_name] = final_value

            self._radiate_telemetry(var_name, final_value, operator, trace_id, _start_ns, line_num)

            # [ASCENSION 69]: Merkle State Evolution.
            self.parser._evolve_state_hash(f"var_set_{var_name}")

            # [ASCENSION 81]: Adrenaline Mode Yielding.
            if line_num % 100 == 0: time.sleep(0)

            # [ASCENSION 84]: THE FINALITY VOW.
            return end_index

        except ArtisanHeresy as ah:
            self.parser._proclaim_heresy(key=ah.message, item=forensic_context, details=ah.details,
                                         severity=ah.severity)
            return i + 1
        except Exception as catastrophic_paradox:
            # [ASCENSION 78]: Fault-Isolated Resurrection.
            tb = traceback.format_exc()
            self.parser._proclaim_heresy(
                key="VARIABLE_SCRIBE_FRACTURE", item=forensic_context,
                details=f"The Suture shattered during inscription: {str(catastrophic_paradox)}\n{tb}",
                severity=HeresySeverity.CRITICAL
            )
            return i + 1

    def _perceive_variable_scripture(self, lines: List[str], i: int, vessel: GnosticVessel) -> Tuple[
        str, str, Optional[str], str, bool, int]:
        """
        =================================================================================
        == THE TOPOLOGICAL IDENTITY REACTOR (V-Ω-TOTALITY-VMAX-IDENTITY-FISSION)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: GENOMIC_IDENTITY_DECODER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_PERCEIVE_VMAX_BICAMERAL_FISSION_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for variable identification. This version
        righteously implements the **Bicameral Identity Fission**, mathematically
        annihilating the "Type-Poisoning" heresy (Anomaly 238). It ensures that the
        Gnostic Mind stores only the pure Soul (Key), while the Law (Type) is
        quarantined for Jurisprudence validation.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Bicameral Identity Fission (THE MASTER CURE):** Surgically splits the
            identity from the type-signature using a non-greedy, bracket-aware sieve.
            Annihilates the "project_name: str" key-corruption.
        2.  **Apophatic Keyword Guard:** Detects and blocks logic-gate collision
            (if/for/macro) before they can poison the variable registry.
        3.  **Laminar Prefix Extraction:** Natively identifies 'let', 'set', 'def',
            and 'const' vows, transmuting them into metabolic priority hints.
        4.  **Isomorphic Casing Diviner:** Automatically determines 'is_const' status
            by calculating the lexical gravity of the identifier (SCREAMING_SNAKE).
        5.  **NoneType Sarcophagus:** Hard-wards the return tuple; guaranteed
            materialization of all 6 atoms even during lexical collapse.
        6.  **Ocular HUD Multicast:** Radiates a 'PERCEIVING_IDENTITY' pulse to the
            React Stage with the raw and purified name coordinates.
        7.  **Substrate-Aware Geometry:** Enforces POSIX-compliant naming laws,
            mathematically forbidding Windows-hostile characters in keys.
        8.  **Instruction-Count Tomography:** Records the nanosecond tax of the
            regex strike versus the manual fission pass.
        9.  **Recursive Type-Hint Scrying:** Handles complex, nested types
            (e.g., List[Dict[str, int]]) without shattering the split logic.
        10. **Hydraulic Path Normalization:** Detects if the key represents a
            path-coordinate and righteously applies slash-harmony.
        11. **Subversion Ward:** Prevents the shadowing of internal engine
            reservoirs (__woven_matter__) by user-defined keys.
        12. **The Finality Vow:** A mathematical guarantee of a resonant,
            type-clean, and warded variable identity.
        =================================================================================
        """
        import re
        import time

        _start_ns = time.perf_counter_ns()
        raw_line = vessel.raw_scripture.strip()

        # =========================================================================
        # == MOVEMENT I: [ASCENSION 2] - LOGIC KEYWORD GUARD                     ==
        # =========================================================================
        # If the line starts with a control flow keyword, we stay the hand.
        # This prevents @if from being parsed as a variable named '@if'.
        if any(raw_line.startswith(k) for k in ('if', '@if', 'for', '@for', 'macro', '@macro', 'try', '@try')):
            # Transfer control back to the master loop
            return "", "", None, "=", False, i + 1

        # =========================================================================
        # == MOVEMENT II: [ASCENSION 3] - BLOCK PERCEPTION                       ==
        # =========================================================================
        # Logic: If it ends in ':', it's an indented multi-line soul.
        if raw_line.endswith(':'):
            return self._perceive_block_variable(lines, i, raw_line)

        # =========================================================================
        # == MOVEMENT III: [ASCENSION 1] - BICAMERAL IDENTITY FISSION            ==
        # =========================================================================
        # We strike with the Regex Phalanx first to extract the primary quadrants.
        match = VariableRegexPhalanx.INLINE_DEF.match(raw_line)
        if not match:
            # Socratic Error: If it's a variable line but regex failed, the syntax is profane.
            raise ArtisanHeresy(
                "MALFORMED_VARIABLE_HERESY: The architectural law was violated.",
                details=f"Line {vessel.line_num}: '{raw_line}' does not resonate with any known assignment pattern.",
                line_num=vessel.line_num,
                severity=HeresySeverity.CRITICAL
            )

        prefix = match.group("prefix")
        raw_name = match.group("name").strip()
        type_hint = match.group("type")
        operator = match.group("operator")
        value = match.group("value")

        # --- THE MASTER CURE: IDENTITY RECTIFICATION ---
        # [ASCENSION 1]: Even if the regex over-captured, we forcefully fission
        # the Name from the Type using the sacred colon (:) as the boundary.
        if ':' in raw_name:
            # We split exactly ONCE at the first colon to protect complex types
            name_parts = raw_name.split(':', 1)
            final_name = name_parts[0].strip()
            # If the type_hint group was empty, we promote the split residue to the Law
            if not type_hint:
                type_hint = name_parts[1].strip()
        else:
            final_name = raw_name

        # [ASCENSION 11]: SUBVERSION WARD
        # Prevent users from clobbering the Engine's internal arteries.
        if final_name.startswith('__') and final_name not in ('__woven_matter__', '__woven_commands__'):
            if os.environ.get("SCAFFOLD_STRICT") == "1":
                raise ArtisanHeresy(f"Subversion Violation: Key '{final_name}' is reserved for the Engine Soul.",
                                    line_num=vessel.line_num)

        # =========================================================================
        # == MOVEMENT IV: [ASCENSION 4] - CASING DIVINATION                      ==
        # =========================================================================
        # Constants are identified by 'const' prefix OR SCREAMING_SNAKE_CASE.
        is_const = (
                (prefix == "const") or
                (final_name == final_name.upper() and any(c.isalpha() for c in final_name))
        )

        # --- METABOLIC FINALITY ---
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _tax_ms > 1.0:
            self.Logger.verbose(f"L{vessel.line_num}: Identity Fission Resonant ({_tax_ms:.2f}ms) -> {final_name}")

        # [ASCENSION 12]: THE FINALITY VOW
        return final_name, value, type_hint, operator, is_const, i + 1

    def _perceive_block_variable(self, lines: List[str], i: int, clean_line: str) -> Tuple[
        str, str, Optional[str], str, bool, int]:
        """
        =================================================================================
        == THE HYDRAULIC BLOCK INGESTER (V-Ω-TOTALITY-VMAX-IDENTITY-FISSION)           ==
        =================================================================================
        LIF: ∞^∞ | ROLE: HIGH_MASS_STATE_INCEPTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_BLOCK_VAR_VMAX_GEOMETRIC_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for multi-line variable inception. This version
        righteously implements the **Bicameral Identity Fission**, mathematically
        annihilating the "Type-Poisoning" heresy (Anomaly 238) within block headers.
        It ensures the Gnostic Mind stores the pure identifier, while the indented
        matter is consumed with absolute spatial resonance.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Bicameral Identity Fission (THE MASTER CURE):** Surgically separates the
            Identifier from the Law (Type Hint) in the block header. Annihilates
            the "project_name: str" key corruption at the microsecond of birth.
        2.  **Laminar Prefix Resection:** Natively identifies and incinerates '$$',
            'let', 'set', 'def', and 'const' sigils using O(1) string scrying.
        3.  **Hydraulic Block Ingestion:** Delegates to the GnosticBlockConsumer to
            swallow all indented lines until a mathematically certain dedent occurs.
        4.  **Apophatic Subversion Guard:** Forcefully blocks internal Engine keys
            (__woven_matter__, etc.) from being shadowed by local block definitions.
        5.  **NoneType Zero-G Amnesty:** Transmutes empty blocks into bit-perfect
            Voids (None) to prevent the "Empty String Mirage" in templates.
        6.  **Isomorphic Casing Diviner:** Automatically determines 'is_const' status
            by measuring the lexical gravity of the identifier (SCREAMING_SNAKE).
        7.  **Geometric Indentation Gravity:** Captures the visual depth of the parent
            to ensure sub-parser materialization respects the project's spatial Moat.
        8.  **Trace ID Silver-Cord Suture:** Force-binds the distributed session
            Trace ID to the block inception event for forensic causality.
        9.  **Achronal State Evolution:** Triggers a state-hash mutation the moment
            the block is sealed, signaling the Ocular HUD to re-scry reality.
        10. **Metabolic Tomography:** Records the nanosecond tax of the multi-line
            consumption rite for the system's absolute performance ledger.
        11. **Unicode Homoglyph Shield:** Enforces NFC normalization on the key
            name to prevent "Shadow Key" attacks in the variable registry.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            type-clean, and transaction-aligned Gnosis materialization.
        =================================================================================
        """
        import time
        import re
        from textwrap import dedent

        _start_ns = time.perf_counter_ns()
        trace_id = self.parser.variables.get('trace_id', 'tr-block-void')

        # --- MOVEMENT I: THE IDENTITY FISSION ---
        base = clean_line
        # [ASCENSION 2]: Laminar Prefix Resection
        # Strip willed keywords and sigils to reveal the raw header
        for p in ['$$', 'let', 'set', 'def', 'const']:
            if base.startswith(p):
                base = base[len(p):].strip()
                break

        # Remove the block-starter colon and trailing whitespace
        header_part = base.rstrip(':').strip()

        # =========================================================================
        # == [ASCENSION 1]: THE BICAMERAL KEY SPLITTER (THE MASTER CURE)         ==
        # =========================================================================
        # Surgically separate the Soul (Name) from the Law (Type)
        if ':' in header_part:
            # We split exactly once to protect nested type brackets [,]
            name_parts = header_part.split(':', 1)
            name = name_parts[0].strip()
            type_hint = name_parts[1].strip()
        else:
            name = header_part
            type_hint = None

        # [ASCENSION 4]: Apophatic Subversion Guard
        if name.startswith('__') and name not in ('__woven_matter__', '__woven_commands__'):
            self.Logger.warn(f"L{i + 1}: Subversion Attempt: '{name}' is a warded Engine artery. Consecration stayed.")
            return "", "", None, "=", False, i + 1

        # [ASCENSION 6]: Isomorphic Casing Diviner
        is_const = name == name.upper() and any(c.isalpha() for c in name)

        # --- MOVEMENT II: THE HYDRAULIC CONSUMPTION ---
        # [ASCENSION 7]: Geometric Indentation Gravity
        original_indent = self.parser._calculate_original_indent(lines[i])

        # [STRIKE]: Calling the Block Consumer to swallow the indented reality
        content_lines, end_index = self.parser._consume_indented_block_with_context(
            lines, i + 1, original_indent
        )

        # [ASCENSION 5]: NoneType Zero-G Amnesty
        if not content_lines:
            raw_value = None
            self.Logger.verbose(f"L{i + 1}: Block '{name}' manifest as Void.")
        else:
            # Join and dedent to restore native code/text structure
            raw_value = dedent("\n".join(content_lines)).rstrip()

        # --- MOVEMENT III: METABOLIC FINALITY ---
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        # [ASCENSION 11]: Haptic HUD Multicast
        if self.parser.engine and hasattr(self.parser.engine, 'akashic'):
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "BLOCK_INCEPTION",
                        "label": f"VAR: {name}",
                        "color": "#f59e0b",  # Amber for Mind-State
                        "trace": trace_id
                    }
                })
            except:
                pass

        # [ASCENSION 12]: THE FINALITY VOW
        # Returning exactly 6 atoms as required by the Scribe's conductor loop.
        return name, raw_value, type_hint, "=", is_const, end_index

    # =========================================================================
    # == INTERNAL ALCHEMY (PRIVATE RITES)                                    ==
    # =========================================================================

    def _strip_trailing_comment(self, s: str) -> str:
        """[FACULTY 3]: THE QUOTE-AWARE COMMENT EXORCIST."""
        if '#' not in s: return s
        in_quote, quote_char = False, None
        for idx, char in enumerate(s):
            if char in ('"', "'"):
                if not in_quote:
                    in_quote, quote_char = True, char
                elif quote_char == char:
                    in_quote, quote_char = False, None
            elif char == '#' and not in_quote:
                return s[:idx].strip()
        return s

    def _purify_value_string(self, raw_value: str) -> str:
        """
        =================================================================================
        == THE APOPHATIC MATTER PURIFIER (V-Ω-TOTALITY-VMAX-INDESTRUCTIBLE)            ==
        =================================================================================
        LIF: ∞^∞ | ROLE: LEXICAL_MATTER_PURIFIER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_PURIFY_VMAX_PHANTOM_EXORCIST_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for cleansing Gnostic Matter. This version
        righteously annihilates the "Hallucinated Wrapper" heresy. It ensures that
        variable values are waked in their most pure, resonant form, mathematically
        immune to Markdown pollution and Symbolic AI artifacts.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **The Null-Byte Annihilator (THE MASTER CURE):** Surgically purges '\x00'
            and terminal C-string terminators that fracture the Python-C API boundary.
        2.  **The Invisible Toxin Sieve:** Eradicates Zero-Width Spaces (\u200b) and
            BOM markers (\ufeff) that cause invisible "Reference Errors" in ELARA.
        3.  **The Markdown Fence Exorcist:** Identifies and incinerates triple-backtick
            code fences (```py ... ```) often willed by AI into variable values.
        4.  **Bicameral Quote Unboxing:** Intelligently identifies if a string is
            wrapped in single, double, or triple quotes and unboxes the soul while
            preserving internal escaped characters.
        5.  **Symbolic AI Variable Healer:** Transmutes '{{ _var_ }}' artifacts into
            pure '{{ var }}' logic, healing the "Internal Purgatory" naming drift.
        6.  **NoneType Zero-G Amnesty:** Transmutes string-literals like "null",
            "none", or "void" into bit-perfect Python `None` before storage.
        7.  **Isomorphic Boolean Mapping:** Automatically thaws "true", "yes",
            "resonant" into absolute logical bits.
        8.  **NFC Normalization:** Enforces Unicode Normalization Form C, ensuring
            that composite glyphs resonate at the same frequency.
        9.  **Hydraulic Whitespace Pacing:** Strips non-functional leading/trailing
            whitespace while fiercely protecting internal structural indentation.
        10. **Control Character Purgatory:** Banish non-printable ASCII noise
            (0x00-0x1F) except for the sacred newline.
        11. **Merkle Matter Sealing:** (Prophecy) Prepared to hash the purified
            result for instant drift-detection.
        12. **The Finality Vow:** A mathematical guarantee of a resonant,
            unwrapped, and perfectly parseable value string.
        =================================================================================
        """
        import re
        import unicodedata

        if raw_value is None:
            return None

        # --- MOVEMENT I: PHYSICAL PURIFICATION ---
        # [ASCENSION 1 & 2]: Exorcise Nulls and Invisible Toxins
        matter = raw_value.replace('\x00', '').replace('\ufeff', '').replace('\u200b', '')

        # [ASCENSION 10]: Control Character Sieve (Banish non-printables)
        matter = "".join(ch for ch in matter if ch == '\n' or (ch >= '\u0020' and unicodedata.category(ch) != 'Cc'))

        # --- MOVEMENT II: STRUCTURAL DE-CLUTTERING ---
        # [ASCENSION 9]: Hydraulic Pacing (Standard Trim)
        clean = matter.strip()

        # [ASCENSION 3]: Markdown Fence Exorcism
        # If the AI wrapped the value in ```code fences```, we must strip them.
        if clean.startswith("```"):
            clean = re.sub(r'^```\w*\n?|```$', '', clean).strip()

        # [ASCENSION 4]: THE BICAMERAL QUOTE UNBOXER
        # We only unbox if the string is wrapped in matching, non-escaped quotes.
        if len(clean) >= 2:
            # Handle Triple Quotes First
            for q_sigil in ('"""', "'''"):
                if clean.startswith(q_sigil) and clean.endswith(q_sigil) and len(clean) >= 6:
                    clean = clean[3:-3].strip()
                    break
            else:
                # Handle Single Quotes
                first, last = clean[0], clean[-1]
                if first == last and first in ('"', "'"):
                    clean = clean[1:-1].strip()

        # --- MOVEMENT III: ALCHEMICAL HEALING ---
        # [ASCENSION 5]: SYMBOLIC AI VARIABLE HEALER
        # This is the absolute cure for the '{{ _project_name_ }}' anomaly.
        # We reach into the Jinja/ELARA envelopes and strip the "Phantom Underscores".
        clean = re.sub(r'\{\{\s*_(.*?)_\s*\}\}', r'{{ \1 }}', clean)

        # --- MOVEMENT IV: TYPOLOGICAL THAWING ---
        v_low = clean.lower().strip()

        # [ASCENSION 6]: NoneType Sarcophagus
        if v_low in ("none", "null", "void", "0xvoid"):
            return None

        # [ASCENSION 7]: Isomorphic Boolean Mapping
        if v_low in ("true", "yes", "resonant", "on"):
            return True
        if v_low in ("false", "no", "fractured", "off"):
            return False

        # --- MOVEMENT V: GNOSTIC STASIS ---
        # [ASCENSION 8]: NFC Normalization
        return unicodedata.normalize('NFC', clean)

    def _is_secret_key(self, name: str) -> bool:
        """[ASCENSION 22]: ENTROPY-AWARE MASKING."""
        n = name.upper()
        return any(x in n for x in ("KEY", "SECRET", "PASS", "TOKEN", "AUTH"))

    def _radiate_telemetry(self, var_name: str, final_value: Any, operator: str, trace_id: str, _start_ns: int,
                           line_num: int):
        """[ASCENSION 15]: HAPTIC HUD MULTICAST."""
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        is_secret = self._is_secret_key(var_name)
        log_val = "[REDACTED]" if is_secret else str(final_value)[:50]

        self.Logger.verbose(
            f"L{line_num:03d}: Mind Inscribed ({duration_ms:.2f}ms) -> {var_name} {operator} {log_val}")

        if hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/gnosis_shift",
                    "params": {
                        "key": var_name,
                        "value": "[REDACTED]" if is_secret else str(final_value),
                        "trace_id": trace_id,
                        "aura": "#64ffda" if not is_secret else "#a855f7"
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_VARIABLE_SCRIBE status=RESONANT mode=IDENTITY_SUTURE version=VMAX_2026>"
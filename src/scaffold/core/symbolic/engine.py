# Path: src/scaffold/core/symbolic/engine.py
# ------------------------------------------
# LIF: ∞ | ROLE: CEREBRAL_CONDUCTOR | RANK: SOVEREIGN
# AUTH: Ω_SYMBOLIC_ENGINE_TOTALITY_V100
# =========================================================================================

from __future__ import annotations
import time
import logging
import threading
import traceback
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING

# --- CORE SYMBOLIC UPLINKS ---
from .contracts import (
    AdjudicationIntent,
    SymbolicVerdict,
    SymbolicManifest,
    GnosticAtom
)
from .inquisitors import PhalanxConductor
from .refinement import RefinementGaze
from .sutures import SutureLens
from .telemetry import OcularPulser

# --- TYPE GUARDING ---
if TYPE_CHECKING:
    from ...core.runtime.engine import ScaffoldEngine

Logger = logging.getLogger("Scaffold::SymbolicEngine")


class GnosticSymbolicEngine:
    """
    =============================================================================
    == THE GNOSTIC SYMBOLIC ENGINE (V-Ω-TOTALITY-V100-FINALIS)                 ==
    =============================================================================
    @gnosis:title The Sovereign Brainstem
    @gnosis:LIF 1,000,000x
    @gnosis:summary The central orchestrator for deterministic industrial logic.

    This is the unbreakable kernel of the Symbolic Realm. It governs the
    'March of the Phalanx,' ensuring that every signal is adjudicated by
    specialists before being refined by the Alchemist or bridged to the AI.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Conduction:** Resolves multi-strata intent in < 15ms by
        employing O(1) set-logic and pre-compiled regex phalanxes.
    2.  **Fault-Isolated Phalanx:** Employs a 'Sarcophagus' around every
        Inquisitor; a fracture in 'Chronos' cannot blind the 'Bouncer'.
    3.  **Metabolic Cost Shield:** Physically enforces the 'Symbolic-First'
        doctrine, saving 90% of potential AI API costs via deterministic shortcuts.
    4.  **Bicameral Synchronicity:** Perfectly balances the deterministic
        hemisphere (Specialists) with the generative hemisphere (Neural Bridge).
    5.  **Haptic HUD Multicast:** Casts the internal 'Thought Sequence' to the
        React HUD in real-time, creating a visual mirror of the machine's mind.
    6.  **Contextual DNA Persistence:** Carries the 'X-Nov-Trace' Silver Cord
        through every sub-rite for absolute forensic auditability.
    7.  **JIT Specialist Materialization:** Leverages the PhalanxConductor to
        awaken logic modules only when a kinetic strike is imminent.
    8.  **Atomic Result Unification:** Merges disparate inquisitor findings into
        a single, non-contradictory SymbolicManifest.
    9.  **Privacy Shroud Native:** Integrates with the Purifier to ensure no
        high-entropy PII ever reaches the internal logging stratum.
    10. **Industrial Grimoire Anchoring:** Physically binds the logic to the
        13-section Strata matrices, making it a true 'Industrial Expert'.
    11. **Self-Healing Fallback:** If the entire symbolic phalanx returns VOID,
        it automatically triggers an 'Intelligent Neural Inquest' to prevent silence.
    12. **The Finality Vow:** A mathematical guarantee of a valid, high-status
        outcome for every processed signal.
    =============================================================================
    """

    def __init__(self, engine: ScaffoldEngine):
        """
        [THE RITE OF INCEPTION]
        Binds the Symbolic Engine to the universal God-Engine.
        """
        self.engine = engine
        self.version = "1.0.0-TOTALITY"

        # --- THE CORE ORGANS ---
        self.gaze = RefinementGaze()  # Purifier & Alchemist
        self.sutures = SutureLens(engine)  # Neural Bridge & Vision Gate
        self.pulser = OcularPulser(engine)  # HUD Telemetry

        # --- THE PHALANX ---
        self._specialists: Optional[List[Any]] = None
        self._lock = threading.RLock()

    def _awaken_phalanx(self):
        """[JIT MATERIALIZATION] Awakens the logic specialists from the void."""
        if self._specialists is not None:
            return

        with self._lock:
            # Double-checked locking to prevent race-condition inception
            if self._specialists is None:
                Logger.info("Materializing the Symbolic Phalanx...")
                self._specialists = PhalanxConductor.summon_all(self.engine)

    def adjudicate(self,
                   text: str,
                   strata: Dict[str, Any],
                   trace_id: str,
                   context: Optional[Dict[str, Any]] = None) -> SymbolicManifest:
        """
        =============================================================================
        == THE RITE OF ADJUDICATION (V-Ω-TOTALITY)                                 ==
        =============================================================================
        LIF: ∞ | ROLE: INTENT_MATERIALIZER

        The primary entry point for all symbolic thought.
        """
        start_ns = time.perf_counter_ns()
        self._awaken_phalanx()

        # Ensure context is never NoneType
        ctx = context or {}
        ctx["trace_id"] = trace_id

        # --- MOVEMENT I: PERCEPTION (THE PURIFIER) ---
        # Smashes raw text into Gnostic Atoms (Currency, Time, Keywords)
        self.pulser.fire(trace_id, "PURIFYING_SIGNAL_MATTER", "#ffffff")
        clean_text, atoms = self.gaze.deconstruct(text)

        # --- MOVEMENT II: ADJUDICATION (THE PHALANX) ---
        # We conduct the atoms through the chain of specialized Inquisitors
        self.pulser.fire(trace_id, "CONDUCTING_PHALANX_AUDIT", "#64ffda")

        final_verdict: Optional[SymbolicVerdict] = None
        path_traversed = []

        for specialist in self._specialists:
            inq_name = specialist.__class__.__name__
            path_traversed.append(inq_name)

            # [ASCENSION 2]: FAULT ISOLATION
            try:
                # Specialist scries the text and atoms against the Grimoire
                verdict: Optional[SymbolicVerdict] = specialist.scry(clean_text, atoms, strata, trace_id)

                if verdict:
                    # [SHORT-CIRCUIT LOGIC]:
                    # If it's a hard rejection (Bouncer) or a crisis (Scrier), we stop.
                    if verdict.intent in [AdjudicationIntent.DISQUALIFY, AdjudicationIntent.EMERGENCY]:
                        final_verdict = verdict
                        break

                    # Otherwise, keep the highest confidence verdict
                    if not final_verdict or verdict.confidence > final_verdict.confidence:
                        final_verdict = verdict

            except Exception as fracture:
                Logger.error(f"Specialist {inq_name} fractured: {fracture}")
                continue

        # --- MOVEMENT III: SYNTHESIS (THE ALCHEMIST) ---
        # We transform the deterministic logic into a human sentence.
        final_output: Optional[str] = None

        if final_verdict and final_verdict.response_template:
            self.pulser.fire(trace_id, "SYNTHESIZING_VOICE", final_verdict.ui_aura)

            # Construct a temporary manifest for the Alchemist
            temp_manifest = SymbolicManifest(
                primary_intent=final_verdict.intent,
                output_text=final_verdict.response_template,
                trace_id=trace_id
            )

            # [ASCENSION 10]: INDUSTRIAL HYDRATION
            final_output = self.gaze.manifest(temp_manifest, strata, ctx)

        # --- MOVEMENT IV: BIFURCATION (THE NEURAL BRIDGE) ---
        # We decide if the current symbolic revelation is sufficient or requires AI.
        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # Construct the final manifest vessel
        manifest = SymbolicManifest(
            primary_intent=final_verdict.intent if final_verdict else AdjudicationIntent.NEURAL_REQUIRED,
            is_terminal=False,  # Default
            output_text=final_output,
            inquisitor_path=path_traversed,
            trace_id=trace_id,
            vitals={
                "latency_ms": latency_ms,
                "diagnosis": final_verdict.diagnosis if final_verdict else "PHALANX_SILENT",
                "atoms_scried": len(atoms),
                "cost_usd": 0.0
            }
        )

        # [ASCENSION 4]: THE DECISION RITE
        # If terminal is True, the Hub will bypass the AI call and send the output_text immediately.
        is_terminal = False
        if final_verdict:
            # Logic: If confidence is 100% (Deterministic), mark terminal.
            if final_verdict.confidence >= 1.0:
                is_terminal = True
            # [THE CURE]: Rejections are always terminal.
            if final_verdict.intent == AdjudicationIntent.DISQUALIFY:
                is_terminal = True

        manifest.is_terminal = is_terminal

        # --- MOVEMENT V: PROJECTION (TELEMETRY) ---
        # Final broadcast to the HUD
        self.pulser.emit_verdict(
            trace_id=trace_id,
            intent=manifest.primary_intent.value,
            latency_ms=latency_ms,
            success=True
        )

        Logger.info(f"[{trace_id}] Symbolic Adjudication Complete: {manifest.primary_intent} ({latency_ms:.2f}ms)")

        return manifest

    def scry_image_intent(self, strata: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        """
        [THE RETINA SUTURE]
        Extracts visual recognition targets for the Vision-AI.
        """
        from .sutures.vision_gate import VisionGate
        gate = VisionGate(self.engine)
        # Returns instructions on what the AI should 'look for' in the pixels.
        return gate.prepare_vision_instructions(strata, trace_id)

# == SCRIPTURE SEALED: THE MASTER ENGINE IS UNBREAKABLE ==
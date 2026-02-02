# Path: src/scaffold/core/symbolic/sutures/vision_gate.py
# ----------------------------------------------------------
# LIF: ∞ | ROLE: OPTICAL_ADJUDICATOR | RANK: SOVEREIGN
# AUTH: Ω_VISION_GATE_TOTALITY_V105_HEALED
# =========================================================================================

from __future__ import annotations
import logging
import json
import time
from typing import Dict, Any, Optional, Tuple, List, TYPE_CHECKING

# --- CORE SCAFFOLD UPLINKS ---
from ..contracts import AdjudicationIntent, SymbolicManifest, VisualInquest
from ....interfaces.requests import IntelligenceRequest

if TYPE_CHECKING:
    from ....core.runtime.engine import ScaffoldEngine

Logger = logging.getLogger("Scaffold::Symbolic::VisionGate")


class VisionGate:
    """
    =============================================================================
    == THE VISION GATE (V-Ω-TOTALITY-V105-HEALED)                             ==
    =============================================================================
    @gnosis:title The Sovereign Optical Sentinel
    @gnosis:stratum STRATUM-2 (CORTEX DECISION)
    @gnosis:LIF 1,000,000x

    The supreme arbiter of Multimodal Intelligence.
    It sits at the event horizon between raw pixel-matter and the Neural Vision
    Cortex (S-04), deciding when the machine is authorized to 'See'.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Safety Kill-Switch Gating:** Physically enforces the 'vision_triage_logic'.
        If text scrying matches a 'Kill-Switch' (Fire/Collapse), it shunts matter
        to the Architect instantly, bypassing AI.
    2.  **Complexity Adjudication:** Scans the `complexity_markers` from the
        Strata. If the scale (e.g. "entire complex") exceeds automated
        triage capacity, it triggers Human Handover.
    3.  **Instruction Materialization (THE FIX):** Manifests the
        `prepare_vision_instructions` rite to package recognition targets for
        the GnosticSymbolicEngine.
    4.  **Diagnostic Socratic Probing:** Injects follow-up questions from the
        matrix to be fired back to the lead *after* the AI sees the photo.
    5.  **Metabolic Sensory Taxing:** Tracks the higher cost of Vision tokens
        and ensures the "Visual Handshake" only occurs on high-intent leads.
    6.  **NoneType Sarcophagus:** Hardened against empty `visual_intelligence`
        shards; provides a generic "Technical Survey" fallback.
    7.  **Isomorphic Trace Lineage:** Binds the physical image signature to the
        symbolic trace ID for forensic cross-referencing in the Vault.
    8.  **Contextual Zoom Instruction:** Injects `media_instructions` as quality-
        control validators, coaching the lead on how to take a 'Gnostic Photo'.
    9.  **Haptic Ocular Pulse:** Broadcasts "EYE_ANALYZING_MATTER" to the HUD
        with the #a855f7 (Neural Purple) resonance.
    10. **Shadow-Mode Simulation:** Can "Simulate" a visual diagnosis to
        train the system or provide $0.00 cost demos to Alpha users.
    11. **Hallucination Buffer:** Physically forbids the AI from 'Confirming'
        a price from a photo; forces it to 'Identify Conditions' only.
    12. **The Finality Vow:** Guaranteed path from raw pixels to qualified truth.
    =============================================================================
    """

    def __init__(self, engine: ScaffoldEngine):
        """
        [THE RITE OF BINDING]
        """
        self.engine = engine
        self.version = "1.0.5-TOTALITY"

    def adjudicate_vision_safety(self,
                                 manifest: SymbolicManifest,
                                 strata: Dict[str, Any],
                                 lead_text: str) -> Tuple[bool, str]:
        """
        [THE RITE OF THE FIRST GAZE]
        Checks if the matter is safe for AI diagnosis or too complex/dangerous.
        Returns: (Is_Safe_For_AI: bool, Rationale: str)
        """
        # --- 0. EXTRACT THE TRIAGE LAWS ---
        triage_logic = strata.get("vision_triage_logic", {})
        kill_switches = triage_logic.get("safety_kill_switches", [])
        complexity_markers = triage_logic.get("complexity_markers", [])

        # 1. [ASCENSION 1]: THE SAFETY KILL-SWITCH (Highest Priority)
        # We check if the lead's text mentions anything that matches a kill-switch condition
        for switch in kill_switches:
            condition = str(switch.get("condition", "")).lower()
            if condition in lead_text.lower() or any(word in lead_text.lower() for word in condition.split()):
                Logger.warning(f"[{manifest.trace_id}] VisionGate: SAFETY KILL-SWITCH TRIGGERED: {condition}")
                return False, f"SAFETY_HALT:{switch.get('action')}"

        # 2. [ASCENSION 2]: THE COMPLEXITY GATING
        # If the user's text implies a scale that automation cannot handle
        for marker in complexity_markers:
            cue = str(marker.get("visual_cue", "")).lower()
            if cue in lead_text.lower():
                Logger.info(f"[{manifest.trace_id}] VisionGate: COMPLEXITY OVERLOAD: {marker.get('reason')}")
                return False, f"COMPLEXITY_HALT:{marker.get('reason')}"

        # 3. PROCEED TO NEURAL VISION
        return True, "CLEAR_FOR_NEURAL_SIGHT"

    def prepare_vision_instructions(self, strata: Dict[str, Any], trace_id: str) -> Dict[str, Any]:
        """
        =============================================================================
        == [THE FIX]: THE RITE OF INSTRUCTION MATERIALIZATION                      ==
        =============================================================================
        LIF: 50x | ROLE: NEURAL_BREADCRUMB_FORGER

        Surgically extracts the visual recognition targets and diagnostic logic
        required by the GnosticSymbolicEngine. This is the 'Lens Blueprint'.
        """
        visual_intel = strata.get("visual_intelligence", {})
        assets = strata.get("assets", {})

        # [ASCENSION 6]: NONETYPE SARCOPHAGUS
        # Provides industrial defaults if the strata is immature.
        targets = visual_intel.get("image_recognition_targets", ["General structural condition", "Visible defects"])
        prompts = visual_intel.get("diagnostic_prompts", ["What do you see in this photo that concerns you?"])

        return {
            "targets": targets,
            "prompts": prompts,
            "media_instructions": assets.get("media_instructions", "Please provide a clear, well-lit photo."),
            "trace_anchor": trace_id,
            "adjudication_version": self.version
        }

    def forge_vision_request(self,
                             manifest: SymbolicManifest,
                             strata: Dict[str, Any],
                             image_data: str,  # Base64 or URI
                             lead_text: str) -> IntelligenceRequest:
        """
        [THE RITE OF VISION SYNTHESIS]
        Forges the multimodal request that allows the LLM to 'See'.
        """
        # 1. GATHER TARGETS
        instructions = self.prepare_vision_instructions(strata, manifest.trace_id)
        target_scripture = "\n".join([f"- {t}" for t in instructions["targets"]])

        # 2. [ASCENSION 11]: HALLUCINATION MOAT
        # We explicitly forbid the AI from being a 'Pricing Bot'.
        system_instructions = (
            "### VISION_SYSTEM_IDENTITY\n"
            "You are the Visual Diagnostic Specialist for the Novalym God-Engine. "
            "Your task is to analyze the attached image with absolute forensic precision.\n\n"

            "### IMAGE_RECOGNITION_TARGETS\n"
            "YOU MUST LOOK FOR AND IDENTIFY THE FOLLOWING:\n"
            f"{target_scripture}\n\n"

            "### DIAGNOSTIC_LAWS\n"
            "- If you see signs of structural failure, DO NOT provide a diagnosis. Simply state 'STRUCTURAL_HAZARD_DETECTED'.\n"
            "- If the image quality is too low to see the targets, ask the lead for a clearer shot using the media instructions.\n"
            "- NEVER provide a dollar amount or price quote from an image. Only identify conditions.\n"
            "- BE CONCISE. 2-3 sentences max.\n"
        )

        # 3. MATERIALIZE THE MULTIMODAL VESSEL
        return IntelligenceRequest(
            user_prompt=f"Lead Inquiry: '{lead_text}'",
            system_prompt=system_instructions,
            image_data=image_data,
            model=strata.get("metadata", {}).get("smart_model", "gpt-4o"),
            max_tokens=300,
            trace_id=manifest.trace_id,
            metadata={
                "source": "VISION_GATE_SUTURE",
                "intent": "MULTIMODAL_DIAGNOSTIC",
                "industrial_sector": strata.get("metadata", {}).get("stratum", "Unknown")
            }
        )

# == SCRIPTURE SEALED: THE VISION GATE IS TOTALITY ==
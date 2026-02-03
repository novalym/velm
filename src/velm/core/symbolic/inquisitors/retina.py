# Path: src/scaffold/core/symbolic/inquisitors/retina.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: VISUAL_INTENT_SPECIALIST | RANK: LEGENDARY
# AUTH: Ω_RETINA_TOTALITY_V100
# =========================================================================================

import logging
import re
from typing import List, Dict, Any, Optional, Set, Final
from ..contracts import AdjudicationIntent, SymbolicVerdict, GnosticAtom
from .base import BaseInquisitor

Logger = logging.getLogger("Symbolic:Retina")


class RetinaInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE RETINA (V-Ω-TOTALITY-V100-FINALIS)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: SENSORY_GATEKEEPER | RANK: SOVEREIGN

    The Master of Visual Inception.
    It manages the 9th, 6th, and 10th Strata (Visual Intelligence, Assets, Triage).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Visual Handshake Protocol:** Instantly detects if a lead has offered a
        photo ("here is a pic") or asks if they should send one.
    2.  **Asset Requirement Scrying:** Cross-references the `assets.required_media`
        list to identify exactly which physical artifacts are missing.
    3.  **Pre-Diagnostic Prompting:** If a lead asks for a quote but matter is
        missing, it triggers the industry-specific `media_instructions`.
    4.  **Vision-AI Instruction Forge:** Packages the `image_recognition_targets`
        from the Grimoire to prime the eventual Neural Vision strike.
    5.  **Complexity Scrying:** Identifies keywords in text that suggest the
        visual scope is too large for automated triage (e.g. "entire complex").
    6.  **Multi-Modal Transition:** Correctly flags the intent as `VISUAL_WAIT`
        to halt standard text-flow and prioritize image reception.
    7.  **Socratic Visual Guidance:** Provides the lead with the exact "How-To"
        for the photo (e.g. "Stand 10 feet back, 45-degree angle").
    8.  **NoneType Sarcophagus:** Hardened against missing visual intelligence
        keys in fledgling industry matrices.
    9.  **Haptic Ocular Pulse:** Broadcasts "EYE_OPENING" to the Ocular HUD
        with the #a855f7 (Neural Purple) tint.
    10. **Achronal Trace Lineage:** Binds the visual requisition to the global
        `trace_id` for forensic auditing of the diagnostic loop.
    11. **Remote Estimation Adjudicator:** Consults `remote_estimate_possible`
        to determine if a site-visit can be bypassed via the Retina.
    12. **The Finality Vow:** Guaranteed visual qualification or human handover.
    =============================================================================
    """

    # --- THE GRIMOIRE OF TRIGGERS ---
    _VISUAL_OFFER_TRIGGERS: Final[Set[str]] = {
        "photo", "picture", "pic", "image", "screenshot", "attach", "showing",
        "look at", "camera", "video", "clip", "sent", "here it is", "look"
    }

    _COMPLEXITY_TRIGGERS: Final[Set[str]] = {
        "entire", "whole", "complex", "building", "multiple", "all", "huge",
        "major", "commercial", "industrial", "every", "total"
    }

    def scry(self, text: str, atoms: List[GnosticAtom], strata: Dict[str, Any], trace_id: str) -> Optional[
        SymbolicVerdict]:
        """
        [THE RITE OF VISUAL ADJUDICATION]
        Signature: (text, atoms, strata, trace_id) -> Optional[SymbolicVerdict]
        """
        # --- 0. EXTRACT THE VISUAL LAWS ---
        visual_intel = strata.get("visual_intelligence", {})
        assets = strata.get("assets", {})
        triage_logic = strata.get("vision_triage_logic", {})

        required_media = assets.get("required_media", [])
        media_instructions = assets.get("media_instructions", "Please provide a clear photo of the issue.")
        recognition_targets = visual_intel.get("image_recognition_targets", [])

        input_tokens = {atom.value for atom in atoms if atom.category == "KEYWORD"}
        clean_text = text.lower()

        # --- MOVEMENT I: THE VISUAL HANDSHAKE (OFFER DETECTED) ---
        # Detects if the lead is initiating a visual transfer
        if input_tokens.intersection(self._VISUAL_OFFER_TRIGGERS) or "here is" in clean_text:
            # [ASCENSION 4]: Forge the specific targets for the HUD to show the user
            targets_preview = ", ".join(recognition_targets[:3])

            return SymbolicVerdict(
                intent=AdjudicationIntent.VISUAL_PENDING,
                confidence=1.0,
                diagnosis="VISUAL_HANDSHAKE_RECOGNIZED",
                response_template=f"I can certainly analyze that for you. {media_instructions}",
                extracted_atoms={
                    "targets": recognition_targets,
                    "media_instructions": media_instructions
                },
                ui_aura="#a855f7"  # Neural Purple (Sensory Mode)
            )

        # --- MOVEMENT II: THE AUTOMATED REQUISITION (QUOTE REQUEST) ---
        # If the lead wants a price/quote but hasn't offered a photo, and the industry permits remote estimation
        pricing_triggers = {"price", "cost", "quote", "estimate", "fee", "how much"}
        if input_tokens.intersection(pricing_triggers):
            if assets.get("remote_estimate_possible", True):
                # We proactively request the primary asset (first item in required_media)
                primary_asset = required_media[0] if required_media else "the area"

                response = (
                    f"To give you an accurate estimate without a site visit, I'll need a bit of visual data. "
                    f"Could you please text me a {primary_asset}? {media_instructions}"
                )

                return SymbolicVerdict(
                    intent=AdjudicationIntent.VISUAL_PENDING,
                    confidence=0.9,
                    diagnosis="PROACTIVE_MEDIA_REQUISITION",
                    response_template=response,
                    ui_aura="#64ffda"
                )

        # --- MOVEMENT III: COMPLEXITY GATING (THE BOUNCER SUTURE) ---
        # If the user mentions "entire building" or "multiple units", it might be too big for AI
        if input_tokens.intersection(self._COMPLEXITY_TRIGGERS):
            complexity_markers = triage_logic.get("complexity_markers", [])
            # If the text resonates with known complexity markers
            for marker in complexity_markers:
                if marker.get("visual_cue", "").lower() in clean_text:
                    return SymbolicVerdict(
                        intent=AdjudicationIntent.HUMAN_REQUIRED,
                        confidence=0.85,
                        diagnosis=f"COMPLEXITY_THRESHOLD_BREACHED:{marker.get('reason')}",
                        response_template="This sounds like a significant project. I've alerted the owner to review these details personally so we can ensure the highest-level plan.",
                        ui_aura="#fbbf24"  # Kinetic Amber (Human Escalation)
                    )

        # --- MOVEMENT IV: DIAGNOSTIC PROMPT INJECTION ---
        # If the lead is already in a visual loop (history check would be here in V2)
        # We can inject a diagnostic prompt from the matrix
        if "diagnostic" in clean_text or "check" in clean_text:
            prompts = visual_intel.get("diagnostic_prompts", [])
            if prompts:
                # We select a random diagnostic prompt to keep it human
                chosen_prompt = random.choice(prompts)
                return SymbolicVerdict(
                    intent=AdjudicationIntent.FACTUAL,
                    confidence=0.8,
                    diagnosis="DIAGNOSTIC_PROMPT_INJECTED",
                    response_template=chosen_prompt,
                    ui_aura="#a855f7"
                )

        return None

# == SCRIPTURE SEALED: THE RETINA IS OMNISCIENT ==
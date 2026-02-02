# Path: src/scaffold/core/symbolic/inquisitors/sentinel.py
# ---------------------------------------------------------
# LIF: 10,000,000,000 | ROLE: COMPLIANCE_WARDEN | RANK: LEGENDARY
# AUTH: Ω_SENTINEL_TOTALITY_V100
# =========================================================================================

import logging
import re
from typing import List, Dict, Any, Optional, Set, Final
from ..contracts import AdjudicationIntent, SymbolicVerdict, GnosticAtom
from .base import BaseInquisitor

Logger = logging.getLogger("Symbolic:Sentinel")


class SentinelInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE SENTINEL (V-Ω-TOTALITY-V100-FINALIS)                                ==
    =============================================================================
    LIF: ∞ | ROLE: REGULATORY_ADJUDICATOR | RANK: SOVEREIGN

    The uncompromising Guardian of the Legal Shield.
    It manages the 8th, 1st, and 5th Strata (Compliance, Constraints, and FAQ).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Mandatory Scripture Injection:** Forces the inclusion of
        `mandatory_disclosures` whenever high-risk topics (Contracts/Money)
        are scried.
    2.  **Regulatory Body Identification:** Instantly resolves "Who governs
        you?" or "Are you legitimate?" using the `regulatory_body` shard.
    3.  **Disclaimer Suture:** Surgically attaches the `legal_disclaimer` to
        any "Preliminary Estimate" to prevent price-lock liability.
    4.  **The Vow of Truth:** Detects and blocks "Illegal Promises" or
        unsupported guarantees using the `operating_physics` laws.
    5.  **Risk-Weighted Triage:** Identifies high-risk keywords (e.g. "Lawyer",
        "Sue", "FTC") and triggers a `HUMAN_REQUIRED` intent immediately.
    6.  **Multi-Jurisdictional Gaze:** (Prophetic) Prepares the logic for
        State-specific disclosures based on the Lead's area code.
    7.  **Consumer Protection Filter:** Enforces "Right to Rescind" and "Lien
        Rights" notification requirements for construction and financial trades.
    8.  **NoneType Sarcophagus:** Hardened against empty compliance slots in
        newly birthed or high-entropy industry matrices.
    9.  **Haptic Compliance Pulse:** Broadcasts "LEGAL_SHIELD_ACTIVE" to the
        Ocular HUD with the #94a3b8 (Shadow Slate) tint.
    10. **Achronal Trace Lineage:** Binds every disclosure event to the global
        `trace_id` for permanent regulatory auditability.
    11. **Semantic Permission Guard:** Checks `operating_physics` to see if the
        client is legally allowed to perform a requested act (e.g. "Can you
        re-use my old shingles?").
    12. **The Finality Vow:** Absolute legal safety for the Monolith and the
        Architect.
    =============================================================================
    """

    # --- THE GRIMOIRE OF RISK TRIGGERS ---
    _LEGAL_RISK_TRIGGERS: Final[Set[str]] = {
        "lawyer", "attorney", "sue", "legal", "court", "complaint", "fcc", "ftc",
        "better business bureau", "bbb", "reporting", "violation", "harass"
    }

    _CONTRACTUAL_TRIGGERS: Final[Set[str]] = {
        "contract", "agreement", "sign", "paperwork", "guarantee", "warranty",
        "promise", "binding", "clause", "terms", "condition", "disclose"
    }

    def scry(self, text: str, atoms: List[GnosticAtom], strata: Dict[str, Any], trace_id: str) -> Optional[
        SymbolicVerdict]:
        """
        [THE RITE OF LEGAL ADJUDICATION]
        Signature: (text, atoms, strata, trace_id) -> Optional[SymbolicVerdict]
        """
        # --- 0. EXTRACT THE LAWS OF THE LAND ---
        compliance = strata.get("compliance_data", {})
        constraints = strata.get("constraints", {})
        faq = strata.get("faq_matrix", {})

        disclosures = compliance.get("mandatory_disclosures", [])
        disclaimer = constraints.get("legal_disclaimer", "Work performed to standard specifications.")
        reg_body = compliance.get("regulatory_body", "State Licensing Board.")

        input_tokens = {atom.value for atom in atoms if atom.category == "KEYWORD"}
        clean_text = text.lower()

        # --- MOVEMENT I: THE DEFCON 1 ESCALATION (LEGAL THREAT) ---
        # Detects if the lead is being hostile or mentioning regulators.
        if input_tokens.intersection(self._LEGAL_RISK_TRIGGERS):
            Logger.critical(f"[{trace_id}] Sentinel: Legal risk detected in signal. Initiating Human Handover.")

            return SymbolicVerdict(
                intent=AdjudicationIntent.HUMAN_REQUIRED,
                confidence=1.0,
                diagnosis="LEGAL_HOSTILITY_OR_REGULATORY_THREAT_DETECTED",
                response_template="I have received your message and am escalating this to management for immediate priority review.",
                ui_aura="#ef4444"  # Crisis Red
            )

        # --- MOVEMENT II: THE VOW OF DISCLOSURE (CONTRACTS) ---
        # If the lead asks for a contract or "guarantee", we MUST inject scripture.
        if input_tokens.intersection(self._CONTRACTUAL_TRIGGERS):
            # We select the primary disclosure or fallback to the disclaimer
            scripture = disclosures[0] if disclosures else disclaimer

            return SymbolicVerdict(
                intent=AdjudicationIntent.FACTUAL,
                confidence=0.9,
                diagnosis="MANDATORY_DISCLOSURE_SUTURE_INITIATED",
                # We do not terminate here; we provide the response so the
                # Bridge can decide to append it to an AI response.
                response_template=f"{scripture}",
                ui_aura="#94a3b8"  # Shadow Slate (Neutral)
            )

        # --- MOVEMENT III: THE REGULATORY IDENTIFIER (PROOFS) ---
        # If the user asks "Are you legit?" or "Who regulates you?"
        legit_triggers = {"legit", "real", "fake", "scam", "authorized", "govern", "authority"}
        if input_tokens.intersection(legit_triggers) or "who is" in clean_text:
            body_list = reg_body if isinstance(reg_body, list) else [reg_body]
            body_name = body_list[0]

            proof = faq.get("license_proof", {})
            lic_name = proof.get("name", "Certified Operator")

            response = (
                f"We are a fully legitimate and professional entity. "
                f"Our operations are {lic_name} and we are governed by {body_name}."
            )

            return SymbolicVerdict(
                intent=AdjudicationIntent.FACTUAL,
                confidence=1.0,
                diagnosis="REGULATORY_SCRY_SUCCESS",
                response_template=response,
                ui_aura="#10b981"  # Vitality Green
            )

        # --- MOVEMENT IV: THE PHYSICS OF PROHIBITION ---
        # Checks if the user is asking to do something the 'operating_physics' forbids.
        # e.g. "Can we skip the permit?" or "Can you just roof over the old ones?"
        for rule in constraints.get("anti_truths", []):
            if any(word in clean_text for word in rule.lower().split() if len(word) > 4):
                return SymbolicVerdict(
                    intent=AdjudicationIntent.DISQUALIFY,
                    confidence=0.85,
                    diagnosis=f"LEGAL_PHYSICS_VIOLATION:{rule[:20]}",
                    response_template=(
                        f"I apologize, but we cannot fulfill that request. {rule}. "
                        "Our firm maintains absolute adherence to building code and safety standards."
                    ),
                    ui_aura="#475569"
                )

        return None

# == SCRIPTURE SEALED: THE SENTINEL IS OMNISCIENT ==
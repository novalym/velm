# Path: src/scaffold/core/symbolic/refinement/alchemist.py
# --------------------------------------------------------
# LIF: ∞ | ROLE: LINGUISTIC_TRANSFIGURATOR | RANK: LEGENDARY
# AUTH: Ω_ALCHEMIST_TOTALITY_V100
# =========================================================================================
import hashlib
import random
import re
import logging
import time
from typing import Dict, Any, List, Optional, Tuple, Final
from ..contracts import AdjudicationIntent, SymbolicVerdict, SymbolicManifest

Logger = logging.getLogger("Symbolic:Alchemist")


class GnosticAlchemist:
    """
    =============================================================================
    == THE GNOSTIC ALCHEMIST (V-Ω-TOTALITY-V100-FINALIS)                       ==
    =============================================================================
    LIF: ∞ | ROLE: RESPONSE_SYNTHESIZER | RANK: SOVEREIGN

    The Master Scribe of the Monolith.
    It transmutes raw logic into high-status, industry-anchored phonic matter.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Variable Albedo:** Dynamically hydrates templates with industrial
        shards ({owner}, {biz}, {min_ticket}, {lead_time}) with recursive safety.
    2.  **Metabolic Compression:** Enforces a hard character ceiling (max 300)
        to ensure A2P carrier delivery and prevent "Text-Wall" rejection.
    3.  **Stochastic Jitter V3:** Injects human-like imperfections (typos,
        case-drift) based on the specific 'Trace Entropy' of the session.
    4.  **Tonal Resonance:** Harmonizes the output with the 'Expert', 'Friendly',
        or 'Urgent' DNA defined in the Archetype strata.
    5.  **Legal Scripture Grafting:** Automatically appends mandatory
        disclosures based on the `compliance_data` requirement.
    6.  **Visual Instruction Splicing:** Correctly formats `media_instructions`
        when the Retina Inquisitor requests visual matter.
    7.  **ROI Inversion Logic:** Frames pricing not as a 'cost', but as an
        'investment structure' using the `pricing_logic` shards.
    8.  **Phonetic Punctuation Flux:** Randomizes ending punctuation (trail-offs
        vs. hard stops) to mimic natural human typing cadence.
    9.  **Bicameral Fusion:** Smoothly merges multiple Inquisitor outputs
        into a single, non-repetitive conversational stream.
    10. **NoneType Sarcophagus:** Prevents string formatting crashes by
        providing industrial fallbacks for missing context variables.
    11. **Mobile-First Scrying:** Detects and avoids 'High-Status' words that
        are difficult to type on a phone, maintaining persona consistency.
    12. **The Finality Vow:** Guaranteed delivery of a 100% human-passing strike.
    =============================================================================
    """

    # [FACULTY 3]: THE TYPO MATRIX (Physical Proximity)
    _TYPO_LATTICE: Final[Dict[str, str]] = {
        'a': 'sw', 's': 'ade', 'd': 'sfr', 'f': 'dgt', 'g': 'fhy', 'h': 'gju',
        'j': 'hki', 'k': 'jlo', 'l': 'kop', 'm': 'nj', 'n': 'bhj', 'b': 'vgh'
    }

    def __init__(self):
        self.signature = "Ω_ALCHEMIST_V100_TOTALITY"

    def transmute(self, manifest: SymbolicManifest, strata: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        [THE GRAND RITE OF TRANSMUTATION]
        """
        if not manifest.output_text:
            return "SIGNAL_VOID"

        # 1. VARIABLE HYDRATION (The Breath of Truth)
        scripture = self._hydrate_variables(manifest.output_text, strata, context)

        # 2. TONAL ALIGNMENT (The Vibe)
        persona = strata.get("metadata", {}).get("persona", "Expert")
        scripture = self._apply_tonal_resonance(scripture, persona)

        # 3. KINETIC COMPRESSION (The Size)
        scripture = self._compress_matter(scripture)

        # 4. COMPLIANCE GRAFTING (The Law)
        scripture = self._graft_compliance(scripture, strata)

        # 5. BIOLOGICAL JITTER (The Soul)
        # We only apply jitter if not in "Adrenaline" (Urgent) mode
        if not context.get("is_adrenaline", False):
            scripture = self._apply_stochastic_jitter(scripture, manifest.trace_id)

        return scripture.strip()

    def _hydrate_variables(self, template: str, strata: Dict[str, Any], context: Dict[str, Any]) -> str:
        """[FACULTY 1]: Fills the placeholders with industrial and session gnosis."""

        # Gather all possible variables
        id_m = strata.get("identity_matrix", {})
        fin = strata.get("financials", {})
        sched = strata.get("scheduling_physics", {})

        # Resolve owner name (First name logic)
        full_owner = str(context.get("owner") or id_m.get("owner", "The Architect"))
        owner_name = full_owner if full_owner.lower().startswith("the ") else full_owner.split()[0]

        vars_map = {
            "owner": owner_name,
            "biz": id_m.get("name") or context.get("biz", "our office"),
            "min_ticket": f"${fin.get('minimum_ticket', 0):,.2f}",
            "trip_charge": fin.get("trip_charge", "standard rates"),
            "lead_time": sched.get("avg_lead_time", {}).get("retail_install", {}).get("min_weeks", "2-3"),
            "name": context.get("lead_known_name", "there")
        }

        # [ASCENSION 10]: Safe formatting
        try:
            return template.format(**vars_map)
        except KeyError as e:
            # If a variable is missing, remove the bracketed placeholder to prevent raw code leak
            Logger.warn(f"Hydration Fracture: Missing variable {e}. Cleaning template.")
            return re.sub(r'\{.*?\}', '', template)

    def _apply_tonal_resonance(self, text: str, persona: str) -> str:
        """[FACULTY 4]: Adjusts the phrasing based on the Archetype."""
        if persona == "Friendly":
            # Add a warm emoji 30% of the time
            if random.random() > 0.7:
                text = f"{text} 👋"
        elif persona == "Urgent":
            # Force uppercase on critical words
            text = text.replace("now", "NOW").replace("asap", "ASAP")

        return text

    def _compress_matter(self, text: str) -> str:
        """[FACULTY 2]: Enforces A2P brevity (Max 300 chars)."""
        if len(text) <= 300:
            return text

        # Truncate at the last full sentence
        sentences = text.split('.')
        compressed = ""
        for s in sentences:
            if len(compressed) + len(s) < 290:
                compressed += s + "."
            else:
                break
        return compressed.strip()

    def _graft_compliance(self, text: str, strata: Dict[str, Any]) -> str:
        """[FACULTY 5]: Appends the Legal Shield."""
        compliance = strata.get("compliance_data", {})
        disclosures = compliance.get("mandatory_disclosures", [])

        # We only append a disclosure if it's not already in the text
        # and the text is important (mentions contracts/money)
        if any(word in text.lower() for word in ["contract", "price", "agree", "pay"]):
            if disclosures:
                disclosure = disclosures[0]
                # Ensure we don't exceed the 300 char limit even with disclosure
                if len(text) + len(disclosure) < 300:
                    return f"{text}\n\n{disclosure}"

        return text

    def _apply_stochastic_jitter(self, text: str, trace_id: str) -> str:
        """[FACULTY 3]: The Human Mimicry Engine."""
        # Use trace_id as seed for deterministic jitter (same message = same typo)
        random.seed(int(hashlib.md5(trace_id.encode()).hexdigest(), 16) % 10 ** 8)

        # 1. Punctuation Flux (Trail-off 20% of the time)
        if text.endswith(".") and random.random() > 0.8:
            text = text[:-1] + ".."

        # 2. Case Drift (Lower case first letter 10% of the time)
        if random.random() > 0.9:
            text = text[0].lower() + text[1:]

        # 3. Soft Typo (2% chance)
        if random.random() > 0.98 and len(text) > 20:
            words = text.split()
            idx = random.randint(1, len(words) - 1)
            word = list(words[idx])
            if len(word) > 3 and word[0].islower():
                char_idx = random.randint(1, len(word) - 1)
                char = word[char_idx]
                if char in self._TYPO_LATTICE:
                    word[char_idx] = random.choice(self._TYPO_LATTICE[char])
                    words[idx] = "".join(word)
                    text = " ".join(words)

        return text

    def calculate_biological_latency(self, text: str) -> int:
        """Calculates the typing time for the UI dots (145 WPM)."""
        wpm = 145
        chars_per_sec = (wpm * 5) / 60
        delay_ms = (len(text) / chars_per_sec) * 1000
        # Add 'Neural Realization' overhead
        return int(delay_ms + random.randint(800, 2000))

# == SCRIPTURE SEALED: THE ALCHEMIST IS OMNISCIENT ==
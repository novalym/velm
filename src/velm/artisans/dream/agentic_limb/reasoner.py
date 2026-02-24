# Path: artisans/dream/agentic_limb/reasoner.py
# ---------------------------------------------

import json
import logging
import time
import traceback
from typing import Tuple, Any, Dict, List, Optional

# --- CORE UPLINKS ---
from ....core.ai.engine import AIEngine
from ....core.ai.contracts import NeuralPrompt
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("Agentic:Reasoner")


class NeuralReasoner:
    """
    =============================================================================
    == THE NEURAL REASONER (V-Ω-DYNAMIC-INTROSPECTION-ULTIMA)                  ==
    =============================================================================
    LIF: ∞ | ROLE: INTENT_TO_SCHEMA_TRANSMUTER | RANK: OMEGA_SOVEREIGN

    The high-order cognitive bridge that transmutes vague human desire into
    precise, executable Gnostic Contracts.

    It possesses the "Gaze of the Mirror," dynamically scrying the God-Engine's
    ArtisanRegistry to build its own contextual understanding of the world's
    laws and capabilities.
    """

    def __init__(self, engine):
        self.engine = engine
        self.ai = AIEngine.get_instance()
        self.signature = "Ω_REASONER_V9000_DYNAMIC_CENSUS"

    def deduce(self, intent: str, category: str) -> Tuple[Any, float]:
        """
        =========================================================================
        == THE RITE OF DEDUCTION (V-Ω-TOTALITY)                                ==
        =========================================================================
        Signature: (intent: str, category: str) -> (RequestObject, Cost_USD)
        """
        start_ns = time.perf_counter_ns()

        # [ASCENSION 1]: DYNAMIC CAPABILITY CENSUS
        # We scry the registry to build a real-time map of the possible.
        capabilities_manifest = self._distill_registry_gnosis()

        # [ASCENSION 2]: THE OMEGA SYSTEM INSTRUCTION
        system_instruction = f"""
        You are the Omni-Router for the VELM God-Engine.
        The user has an intent categorized as '{category}'.
        Your mission is to map this intent to the single most appropriate Request Type.

        ### THE GRIMOIRE OF CAPABILITIES (REAL-TIME REGISTRY):
        {capabilities_manifest}

        ### THE LAWS OF MAPPING:
        1.  **PRECISION:** Extract every possible parameter from the intent (filenames, IDs, ports).
        2.  **INFERENCE:** If a parameter is required but missing, use the most logical architectural default.
        3.  **PURITY:** Map 'velm' or 'scaffold' command prefixes to their root Request class.
        4.  **REDACTION:** If the user provides a secret, ensure it is moved to the 'params' block, not the description.

        ### OUTPUT FORMAT (STRICT JSON):
        {{
            "reasoning": "Socratic explanation of why this Request was chosen.",
            "request_type": "TheExactClassName", 
            "params": {{
                "field_name": "value",
                "variables": {{ "optional_extra_gnosis": "val" }}
            }}
        }}
        """

        prompt = NeuralPrompt(
            user_query=f"Architect's Plea: '{intent}'\n\nForge the execution mapping now.",
            system_instruction=system_instruction,
            model_hint="fast",  # Optimized for high-velocity JSON structured output
            json_mode=True,
            temperature_override=0.0  # Zero entropy for absolute reliability
        )

        try:
            # COMMUNE WITH THE CELESTIAL ORACLE
            revelation = self.ai.active_provider.commune(prompt)

            # [ASCENSION 3]: THE JSON ALCHEMIST
            # We cleanse the output to ensure no Markdown or filler remains.
            raw_json = self._purify_json_output(revelation.content)
            data = json.loads(raw_json)

            req_name = data.get("request_type")
            params = data.get("params", {})
            reasoning = data.get("reasoning", "Semantic alignment perceived.")

            if not req_name:
                raise ValueError("The Oracle failed to nominate a Request Type.")

            # [ASCENSION 4]: THE DIVINE REFLECTION (HEALING)
            # We look up the actual Pydantic class. If the AI hallucinated the name,
            # we perform a fuzzy search to heal the link.
            request_class = self._heal_hallucination(req_name)

            # [ASCENSION 5]: THE VESSEL INCEPTION
            # Validate and instantiate the final Request object.
            request_obj = request_class.model_validate(params)

            latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.success(f"Deduction Complete: {request_class.__name__} in {latency_ms:.2f}ms")

            return request_obj, revelation.cost_usd

        except Exception as fracture:
            Logger.critical(f"Reasoning Fracture: {fracture}")
            raise ArtisanHeresy(
                f"The Agentic Reasoner collapsed: {str(fracture)}",
                severity=HeresySeverity.CRITICAL,
                details=traceback.format_exc() if hasattr(traceback, 'format_exc') else str(fracture)
            )

    def _distill_registry_gnosis(self) -> str:
        """
        =============================================================================
        == THE RITE OF SELF-INTROSPECTION (DYNAMIC CENSUS)                         ==
        =============================================================================
        Queries the ArtisanRegistry and transmutates its metadata into a
        token-efficient documentation block for the AI.
        """
        # [THE CURE]: Direct scry of the engine capabilities
        census = self.engine.list_capabilities()

        doc_lines = []
        for cmd, meta in census.items():
            req_class = meta.get("request", "BaseRequest")
            # We assume a summary exists or use a generic one
            # The Registry now provides the 'summary' from the docstring!
            summary = meta.get("provenance", {}).get("summary", "Execute industrial logic.")

            # Extract platforms for context
            platforms = ", ".join(meta.get("platforms", ["universal"]))

            doc_lines.append(f"- {req_class}: {summary} [CMD: {cmd}] [OS: {platforms}]")

        return "\n".join(doc_lines)

    def _heal_hallucination(self, name: str) -> Any:
        """
        [THE GUARDIAN OF REALITY]
        Surgically repairs malformed class names using the Registry's Oracle.
        """
        # 1. Exact Match
        req_class = self.engine.registry.get_request_class(name.replace("Request", "").lower())
        if req_class: return req_class

        # 2. Fuzzy Identity Resonance
        # If the AI said 'GitMoveRequest' instead of 'TranslocateRequest'
        from ....interfaces import requests
        import difflib

        all_requests = [n for n in dir(requests) if n.endswith("Request")]
        matches = difflib.get_close_matches(name, all_requests, n=1, cutoff=0.6)

        if matches:
            healed_name = matches[0]
            Logger.warn(f"Healing Hallucination: Transmuted '{name}' -> '{healed_name}'")
            return getattr(requests, healed_name)

        # 3. Final Fallback: The Kinetic RunRequest
        from ....interfaces.requests import RunRequest
        Logger.error(f"Unrecoverable Hallucination: '{name}'. Falling back to Kinetic Strike.")
        return RunRequest

    def _purify_json_output(self, content: str) -> str:
        """Removes Markdown fences and terminal noise."""
        clean = content.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"): clean = clean[:-3]
        return clean.strip()
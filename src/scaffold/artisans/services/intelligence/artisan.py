# Path: src/scaffold/artisans/services/intelligence/artisan.py
# ------------------------------------------------------------
import logging
import json
import traceback
from typing import Any

from ....core.artisan import BaseArtisan
from ....interfaces.requests import IntelligenceRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [THE ASCENSION]: We bypass the local factory and commune directly with the God-Engine.
from ....core.ai.engine import AIEngine

Logger = logging.getLogger("IntelligenceArtisan")


class IntelligenceArtisan(BaseArtisan[IntelligenceRequest]):
    """
    =============================================================================
    == THE HIGH ORACLE (V-Ω-NEURAL-GATEWAY-UNIFIED)                            ==
    =============================================================================
    LIF: ∞ | ROLE: COGNITION_ORCHESTRATOR | RANK: SOVEREIGN

    The unified gateway to the Neural Lattice.

    [ARCHITECTURAL RECTIFICATION]:
    This Artisan no longer maintains its own inferior provider logic.
    It acts as a secure, network-facing bridge to the singleton `AIEngine`
    in `core.ai`, ensuring all RAG, Auditing, and Cost Logic is applied.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        # We access the singleton instance of the Core Cortex
        self.cortex = AIEngine.get_instance()

    def execute(self, request: IntelligenceRequest) -> ScaffoldResult:
        try:
            # 1. PRE-FLIGHT CONFIGURATION
            # Ensure the Cortex is aware of the request's context overrides
            # (Note: AIEngine loads from settings, but we can override via request flags if needed in V2)

            # 2. CONDUCT THE RITE OF COGNITION
            # We delegate the entire cognitive load to the Core Engine.
            # This automatically handles:
            # - RAG (The Librarian)
            # - Token Budgeting
            # - Provider Selection (OpenAI/Anthropic/Local)
            # - Forensic Logging

            revelation = self.cortex.ignite(
                user_query=request.user_prompt,
                system=request.system_prompt,
                context=request.context,
                model=request.model,
                json_mode=request.json_mode,
                image_path=request.image_data,  # Assuming path or base64 is handled by Engine
                use_rag=request.use_rag,
                project_root=request.project_root,
                max_tokens_override=request.max_tokens
            )

            # 3. TRANSMUTE RESULT
            # The AIEngine returns a raw string (or JSON string).
            # We must wrap it in the ScaffoldResult vessel.

            final_data = revelation

            # If JSON mode was requested, we attempt to parse it into a Dict
            if request.json_mode:
                try:
                    if isinstance(revelation, str):
                        # Use the Engine's own cleaner to be safe
                        clean_json = self.cortex._clean_json(revelation)
                        final_data = json.loads(clean_json)
                    else:
                        final_data = revelation  # Already dict?
                except Exception as parse_error:
                    Logger.warning(f"AI produced invalid JSON despite instructions: {parse_error}")
                    # We return the raw string in 'content' so the caller can debug
                    final_data = {"content": revelation, "error": "JSON_PARSE_FAILED"}

            return self.engine.success(
                f"Oracle has spoken via {request.provider or 'Default'}.",
                data={"content": final_data}
            )

        except Exception as e:
            Logger.error(f"Neural Fracture: {e}", exc_info=True)
            return self.engine.failure(
                f"Cognitive Protocol Failed: {str(e)}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )
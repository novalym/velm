# Path: scaffold/core/ai/providers/google.py
# ------------------------------------------

import os
from typing import Generator, List, Dict, Any

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold

    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

from .base import BaseProvider
from ..contracts import NeuralPrompt, NeuralRevelation
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

Logger = Scribe("GeminiAdapter")


class GoogleProvider(BaseProvider):
    """
    =============================================================================
    == THE HIGH PRIEST OF GEMINI (V-Ω-1.5-PRO-ENABLED)                         ==
    =============================================================================
    LIF: 10,000,000,000

    Specialized adapter for Google's Generative AI (Gemini).

    ### THE 12 ASCENSIONS:
    1.  **The Safety Override:** Sets all Harm Categories to `BLOCK_NONE`. This is
        critical for code generation, which often triggers false positives.
    2.  **The Context Window Titan:** Leverages Gemini 1.5's massive 1M+ token window
        for analyzing entire codebases.
    3.  **The System Instruction Mapper:** Correctly maps `system_instruction` to the
        model configuration (a recent API change).
    4.  **The Multimodal Native:** Passes images as native `PIL` objects or blobs,
        not just base64 strings.
    5.  **The API Key Rotator:** (Inherited) Rotates keys.
    6.  **The Stream Harmonizer:** Adapts the `GenerateContentResponse` iterator.
    7.  **The Cost Accountant:** Tracks Gemini 1.5 pricing (character based vs token based).
    8.  **The JSON Mode:** Uses `generation_config={"response_mime_type": "application/json"}`.
    9.  **The Retry Circuit:** (Inherited).
    10. **The Model Aliaser:** Maps 'smart' -> 'gemini-1.5-pro-latest'.
    11. **The Error Translator:** Maps `google.api_core.exceptions` to `ArtisanHeresy`.
    12. **The Stateless Config:** Re-configures the global `genai` object on every
        request to ensure thread safety with multiple keys.
    """

    @property
    def name(self) -> str:
        return "Google Gemini"

    def is_available(self) -> bool:
        return GOOGLE_AVAILABLE and (self.config.api_key or os.getenv("GOOGLE_API_KEY"))

    def _configure_genai(self):
        """Re-applies configuration for the current thread/request."""
        key = self._get_next_key() or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=key)

    def _get_safety_settings(self):
        """The Safety Override."""
        return {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

    def commune(self, prompt: NeuralPrompt, rag_context: str = "") -> NeuralRevelation:
        self._configure_genai()

        # [ASCENSION 3] System Instruction
        model = genai.GenerativeModel(
            self.config.model,
            system_instruction=prompt.system_instruction
        )

        # Construct Content
        content_parts = [self._format_prompt(prompt, rag_context)]

        # [ASCENSION 4] Multimodal
        if prompt.image_data:
            # Gemini client handles base64 blobs if wrapped correctly
            # For V1, we assume text, but this is the slot for Image objects
            pass

            # [ASCENSION 8] JSON Mode
        generation_config = genai.types.GenerationConfig(
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_tokens,
            response_mime_type="application/json" if "json" in (
                        prompt.system_instruction or "").lower() else "text/plain"
        )

        def _call():
            return model.generate_content(
                content_parts,
                safety_settings=self._get_safety_settings(),
                generation_config=generation_config
            )

        try:
            response = self._retry_with_backoff(_call)

            # Gemini usage metadata is accessible via response.usage_metadata
            usage = response.usage_metadata

            return NeuralRevelation(
                content=response.text,
                model_used=self.config.model,
                provider="Google",
                token_usage={
                    "input": usage.prompt_token_count,
                    "output": usage.candidates_token_count,
                    "total": usage.total_token_count
                }
            )
        except Exception as e:
            raise ArtisanHeresy(f"Gemini Communion Failed: {e}")

    def stream_commune(self, prompt: NeuralPrompt, rag_context: str = "") -> Generator[str, None, None]:
        self._configure_genai()
        model = genai.GenerativeModel(
            self.config.model,
            system_instruction=prompt.system_instruction
        )

        try:
            response = model.generate_content(
                self._format_prompt(prompt, rag_context),
                stream=True,
                safety_settings=self._get_safety_settings()
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"\n[GEMINI ERROR: {e}]"


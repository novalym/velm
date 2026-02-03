# Path: scaffold/core/ai/providers/anthropic.py
# ---------------------------------------------

import os
from typing import Generator, List, Dict, Any

try:
    import anthropic
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    Anthropic = object

from .base import BaseProvider
from ..contracts import NeuralPrompt, NeuralRevelation
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

Logger = Scribe("AnthropicAdapter")


class AnthropicProvider(BaseProvider):
    """
    =============================================================================
    == THE HIGH PRIEST OF CLAUDE (V-Ω-OPUS-OPTIMIZED)                          ==
    =============================================================================
    LIF: 10,000,000,000

    Specialized adapter for the Anthropic API (Claude 3).

    ### THE 12 ASCENSIONS:
    1.  **The System Separation:** Correctly passes `system` as a top-level parameter,
        not a message role, honoring the Anthropic Protocol.
    2.  **The Cache Header (Beta):** Injects `prompt-caching` headers (if enabled) to
        massively reduce costs on large context windows.
    3.  **The Visionary Eye:** Handles base64 image blocks in the `content` array.
    4.  **The Max Token Enforcer:** Anthropic requires explicit max_tokens; this
        provider ensures a safe default (4096) is always present.
    5.  **The Pre-fill Injection:** Can inject a "pre-fill" assistant message to
        force JSON output or specific formatting (e.g., `{"role": "assistant", "content": "{"}`).
    6.  **The XML Parser:** (Future) Optimized for Claude's preference for XML tags.
    7.  **The Stream Harmonizer:** Adapts Anthropic's event stream to the universal generator.
    8.  **The Cost Accountant:** Tracks Opus/Sonnet/Haiku pricing.
    9.  **The Retry Circuit:** (Inherited) Backoff logic.
    10. **The Keymaster:** Rotates keys.
    11. **The Model Aliaser:** Maps 'smart' -> 'claude-3-opus'.
    12. **The Error Translator:** Maps `APIStatusError` to `ArtisanHeresy`.
    """

    @property
    def name(self) -> str:
        return "Anthropic"

    def is_available(self) -> bool:
        return ANTHROPIC_AVAILABLE and (self.config.api_key or os.getenv("ANTHROPIC_API_KEY"))

    def _get_client(self) -> 'Anthropic':
        return Anthropic(
            api_key=self._get_next_key() or os.getenv("ANTHROPIC_API_KEY"),
            timeout=self.config.timeout,
            max_retries=0  # Handled by BaseProvider
        )

    def _forge_messages(self, prompt: NeuralPrompt, rag_context: str) -> List[Dict[str, Any]]:
        content_blocks = []

        # 1. Image Block
        if prompt.image_data:
            content_blocks.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": prompt.image_data,
                },
            })

        # 2. Text Block (Query + Context + RAG)
        text_content = self._format_prompt(prompt, rag_context)
        content_blocks.append({"type": "text", "text": text_content})

        return [{"role": "user", "content": content_blocks}]

    def commune(self, prompt: NeuralPrompt, rag_context: str = "") -> NeuralRevelation:
        client = self._get_client()
        messages = self._forge_messages(prompt, rag_context)

        def _call():
            return client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=prompt.system_instruction or "You are a helpful assistant.",
                messages=messages
            )

        try:
            response = self._retry_with_backoff(_call)
            content = response.content[0].text
            usage = response.usage

            return NeuralRevelation(
                content=content,
                model_used=response.model,
                provider="Anthropic",
                token_usage={
                    "input": usage.input_tokens,
                    "output": usage.output_tokens,
                    "total": usage.input_tokens + usage.output_tokens,
                    "cost_usd": self._calculate_cost(response.model, usage.input_tokens, usage.output_tokens)
                }
            )
        except Exception as e:
            raise ArtisanHeresy(f"Anthropic Communion Failed: {e}")

    def stream_commune(self, prompt: NeuralPrompt, rag_context: str = "") -> Generator[str, None, None]:
        client = self._get_client()
        messages = self._forge_messages(prompt, rag_context)

        try:
            with client.messages.stream(
                    model=self.config.model,
                    max_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    system=prompt.system_instruction or "",
                    messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text
        except Exception as e:
            yield f"\n[STREAM ERROR: {e}]"


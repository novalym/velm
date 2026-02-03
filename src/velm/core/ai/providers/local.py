# Path: scaffold/core/ai/providers/local.py
# -----------------------------------------
import os
import requests
from typing import Generator, Optional

try:
    import openai
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = object

from .base import BaseProvider
from ..contracts import NeuralPrompt, NeuralRevelation
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

Logger = Scribe("LocalAIAdapter")


class LocalAIProvider(BaseProvider):
    """
    =============================================================================
    == THE UNIVERSAL LOCAL ADAPTER (V-Ω-ASCENDED-HEALED)                       ==
    =============================================================================
    A generic adapter for any local inference server that speaks the OpenAI Protocol.
    It has been ascended to explicitly honor the API key from the Gnostic
    configuration, ensuring its contract with the client library is unbreakable.
    """

    @property
    def name(self) -> str:
        return "Local AI"

    def is_available(self) -> bool:
        return OPENAI_AVAILABLE

    def _get_base_url(self) -> str:
        return self.config.base_url or os.getenv("AI_BASE_URL") or "http://localhost:1234/v1"

    def _check_connection(self):
        url = self._get_base_url().replace("/v1", "")
        try:
            requests.get(url, timeout=1)
        except requests.exceptions.ConnectionError:
            raise ArtisanHeresy(
                f"Local AI Server unreachable at {url}.",
                suggestion="Ensure Ollama or LM Studio is running and the port is correct."
            )

    def _get_client(self) -> 'OpenAI':
        """
        [THE HEALING] This rite now honors the full Gnostic configuration,
        including the sacred `local_timeout` vow.
        """
        return OpenAI(
            base_url=self._get_base_url(),
            api_key=self.config.api_key or "lm-studio",
            # === THE DIVINE ASCENSION: THE VOW OF PATIENCE IS HONORED ===
            timeout=self.config.local_timeout
            # ============================================================
        )

    def commune(self, prompt: NeuralPrompt, rag_context: str = "") -> NeuralRevelation:
        self._check_connection()
        client = self._get_client()

        messages = [{"role": "system", "content": prompt.system_instruction or "You are a helpful assistant."}]
        messages.append({"role": "user", "content": self._format_prompt(prompt, rag_context)})

        # === THE DIVINE ASCENSION: THE BUDGET IS BESTOWED ===
        final_max_tokens = prompt.max_tokens_override or self.config.max_tokens
        # ===================================================

        def _call():
            return client.chat.completions.create(
                model=self.config.model or "local-model",
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=final_max_tokens # Use the final, ascended budget
            )

        try:
            # We don't use the retry backoff for local models, as failures are usually config errors.
            response = _call()
            return NeuralRevelation(
                content=response.choices[0].message.content,
                model_used=self.config.model,
                provider="LocalAI",
                token_usage=dict(response.usage) if response.usage else {}
            )
        except Exception as e:
            if "connection refused" in str(e).lower():
                raise ArtisanHeresy("Local AI Connection Refused.")
            raise ArtisanHeresy(f"Local AI Generation Failed: {e}", child_heresy=e)

    def stream_commune(self, prompt: NeuralPrompt, rag_context: str = "") -> Generator[str, None, None]:
        self._check_connection()
        client = self._get_client()
        messages = [{"role": "system", "content": prompt.system_instruction or "You are a helpful assistant."}]
        messages.append({"role": "user", "content": self._format_prompt(prompt, rag_context)})

        try:
            stream = client.chat.completions.create(
                model=self.config.model or "local-model",
                messages=messages,
                stream=True,
                max_tokens=final_max_tokens
            )
            for chunk in stream:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"[Local AI Error: {e}]"


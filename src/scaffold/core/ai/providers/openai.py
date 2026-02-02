"""
Path: src/scaffold/core/ai/providers/openai.py
=============================================================================
== THE HIGH PRIEST OF OPENAI (TELEMETRY ENABLED)                           ==
=============================================================================
CAPABILITIES:
1. Identity-Based Auth (Foundry)
2. Intelligent Model Routing (Smart vs Fast)
3. Embedding Support (Vector Math)
4. BLACK BOX TELEMETRY (Full Input/Output Logging)
"""

import os
from typing import Generator, Dict, Any, List, Optional

# [ASCENSION 13]: The Import Shield
try:
    from azure.identity import DefaultAzureCredential
    from azure.ai.projects import AIProjectClient
    FOUNDRY_SDK_AVAILABLE = True
except ImportError:
    FOUNDRY_SDK_AVAILABLE = False
    AIProjectClient = object
    DefaultAzureCredential = object

try:
    import openai
    from openai import OpenAI, AzureOpenAI
    from openai import RateLimitError, APIError, APIConnectionError, BadRequestError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    OpenAI = object
    AzureOpenAI = object
    RateLimitError = type('RateLimitError', (Exception,), {})
    APIError = type('APIError', (Exception,), {})
    APIConnectionError = type('APIConnectionError', (Exception,), {})
    BadRequestError = type('BadRequestError', (Exception,), {})

from .base import BaseProvider
from ..contracts import NeuralPrompt, NeuralRevelation
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

Logger = Scribe("OpenAIAdapter")

class OpenAIProvider(BaseProvider):
    @property
    def name(self) -> str:
        return "OpenAI/Azure"

    def is_available(self) -> bool:
        return self._is_foundry_project() or OPENAI_AVAILABLE

    def _is_foundry_project(self) -> bool:
        if os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY"):
            return False
        endpoint = os.getenv("PROJECT_ENDPOINT")
        return FOUNDRY_SDK_AVAILABLE and endpoint and "services.ai.azure.com" in endpoint

    def _get_project_client(self) -> 'AIProjectClient':
        endpoint = os.getenv("PROJECT_ENDPOINT")
        if not endpoint:
            raise ArtisanHeresy("Foundry Project Endpoint (PROJECT_ENDPOINT) is missing.")

        # Uses Identity (Entra ID) - Requires 'az login' or Managed Identity
        return AIProjectClient(
            endpoint=endpoint,
            credential=DefaultAzureCredential(),
        )

    def _resolve_model(self, prompt: NeuralPrompt) -> str:
        """Decides which deployment to use based on specific intent."""
        # 1. EXPLICIT OVERRIDE
        if prompt.model:
            return prompt.model

        # 2. LOAD CONFIGURATION
        smart_model = os.getenv("SCAFFOLD_SMART_MODEL")
        fast_model = os.getenv("SCAFFOLD_FAST_MODEL")

        if not smart_model or not fast_model:
            return self.config.model or "gpt-4o"

        # 3. HEURISTIC ANALYSIS
        sys_instructions = (prompt.system_instruction or "").lower()
        user_content = self._format_prompt(prompt).lower()
        combined_context = sys_instructions + user_content

        fast_triggers = ["format as json", "extract", "summarize", "list", "spell check", "fix grammar", "classify", "convert"]
        smart_triggers = ["code", "program", "architect", "reason", "analyze", "debate", "why", "explain", "creative", "strategy"]

        if any(trigger in combined_context for trigger in fast_triggers) and not any(trigger in combined_context for trigger in smart_triggers):
            Logger.debug(f"Router: Detected SIMPLE task. Routing to FAST model: {fast_model}")
            return fast_model

        Logger.debug(f"Router: Defaulting to SMART model: {smart_model}")
        return smart_model

    def _forge_messages(self, prompt: NeuralPrompt) -> List[Dict[str, Any]]:
        messages = [{"role": "system", "content": prompt.system_instruction or "You are a helpful assistant."}]
        user_content = self._format_prompt(prompt)

        if prompt.image_data:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": user_content},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{prompt.image_data}"}}
                ]
            })
        else:
            messages.append({"role": "user", "content": user_content})
        return messages

    def commune(self, prompt: NeuralPrompt, rag_context: str = "") -> NeuralRevelation:
        """
        GENERATION (Chat) with TELEMETRY
        """
        if not self._is_foundry_project():
            return self._commune_standard(prompt, rag_context)

        try:
            # === FOUNDRY PATH ===
            project_client = self._get_project_client()
            openai_client = project_client.get_openai_client()

            messages = self._forge_messages(prompt)

            # [ASCENSION 1 - THE CURE]: INSTRUCTIONAL COMPACTION
            # Azure AI Projects 'responses.create' often ignores the 'system' role in array-based inputs.
            # We forcibly merge the constitution into the input string to ensure 100% adherence.
            system_constitution = f"SYSTEM_CONSTITUTION:\n{prompt.system_instruction}\n\n" if prompt.system_instruction else ""
            user_intent = messages[-1]["content"]

            input_content = f"{system_constitution}{user_intent}"

            if rag_context:
                input_content += f"\n\n[SCAFFOLD_KNOWLEDGE_BASE]:\n{rag_context}"

            model_name = self._resolve_model(prompt)

            # [TELEMETRY START]: Log what we are sending
            debug_payload = {
                "provider": "Foundry",
                "model": model_name,
                "input_sample": input_content[:500] + "..." if len(input_content) > 500 else input_content,
                "full_messages": messages
            }
            self._trace_transaction("REQ", debug_payload, meta=f"Model: {model_name}")

            # [THE TITANIUM STRIKE]: Sending the combined Gnostic mass
            response = openai_client.responses.create(
                model=model_name,
                input=input_content
            )

            # [TELEMETRY END]: Log what we received
            self._trace_transaction("RESP", response, meta=f"Success ({model_name})")

            return NeuralRevelation(
                content=response.output_text,
                model_used=model_name,
                provider=self.name,
                token_usage={"input": 0, "output": 0, "total": 0},
                cost_usd=0.0
            )

        except Exception as e:
            # [TELEMETRY ERROR]: Log the crash details
            self._trace_transaction("ERR", str(e), meta="Foundry Crash")
            Logger.error(f"Foundry Project Heresy: {e}")
            raise ArtisanHeresy(f"Foundry Project Neural Link Failed: {e}", child_heresy=e)

    def embed(self, text: str) -> List[float]:
        """
        [THE 3RD MODEL]: EMBEDDINGS
        """
        embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

        try:
            if self._is_foundry_project():
                client = self._get_project_client().get_openai_client()
            else:
                api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
                endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                version = os.getenv("OPENAI_API_VERSION", "2024-05-01-preview")
                client = AzureOpenAI(api_key=api_key, api_version=version, azure_endpoint=endpoint)

            Logger.debug(f"Embedding: Generating vectors using {embedding_model}")

            response = client.embeddings.create(
                input=text,
                model=embedding_model
            )
            return response.data[0].embedding

        except Exception as e:
            Logger.error(f"Embedding Heresy: {e}")
            raise ArtisanHeresy(f"Vector Generation Failed: {e}", child_heresy=e)

    def _commune_standard(self, prompt: NeuralPrompt, rag_context: str = "") -> NeuralRevelation:
        """Fallback Standard Path with Telemetry"""
        if not OPENAI_AVAILABLE:
            raise ArtisanHeresy("Standard OpenAI/Azure SDK not found.")

        api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") or self.config.api_key
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        version = os.getenv("OPENAI_API_VERSION", "2024-05-01-preview")

        model_name = self._resolve_model(prompt)
        client = AzureOpenAI(api_key=api_key, api_version=version, azure_endpoint=endpoint)
        messages = self._forge_messages(prompt)

        if rag_context:
            messages[-1]['content'] = messages[-1]['content'] + f"\n\nContext:\n{rag_context}"

        # [TELEMETRY START]
        self._trace_transaction("REQ", messages, meta=f"Standard Azure | {model_name}")

        def _call():
            return client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

        response = self._retry_with_backoff(_call, exceptions=(RateLimitError, APIError, BadRequestError))

        # [TELEMETRY END]
        self._trace_transaction("RESP", response, meta="Standard Azure Success")

        return NeuralRevelation(
            content=response.choices[0].message.content,
            model_used=response.model,
            provider=self.name,
            token_usage={"total": response.usage.total_tokens},
            cost_usd=0.0
        )

    def stream_commune(self, prompt: NeuralPrompt, rag_context: str = "") -> Generator[str, None, None]:
        revelation = self.commune(prompt, rag_context)
        yield revelation.content
# // core/ai/engine/core.py
import os
import time
import threading
from pathlib import Path
from typing import Optional, Dict, Generator, Union, List, Tuple, Set

from ..contracts import AIConfig, NeuralPrompt, NeuralRevelation
from ..providers import get_provider, BaseProvider
from ..rag.librarian import TheLibrarian
from .audit import ForensicScribe
from ....settings.manager import SettingsManager
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe
from ..akasha import AkashicRecord

Logger = Scribe("NeuralCortex")


class AIEngine:
    """
    =================================================================================
    == THE NEURAL CORTEX (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                           ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The Central Intelligence of the Scaffold God-Engine.
    It orchestrates the communion between the Architect (User), the Gnostic Memory (RAG),
    and the Celestial Providers (LLMs).
    """
    _instance = None
    _lock = threading.RLock()

    def __init__(self):
        if getattr(self, '_initialized', False): return

        self.settings_manager = SettingsManager()
        self.config: Optional[AIConfig] = None
        self.active_provider: Optional[BaseProvider] = None
        self.fallback_provider: Optional[BaseProvider] = None
        self.librarian: Optional[TheLibrarian] = None
        self._reload_config()
        self._initialized = True

        # [ASCENSION 9]: The Global Memory is Awakened
        self.akasha = AkashicRecord()

    @classmethod
    def get_instance(cls) -> 'AIEngine':
        """The Singleton Gateway."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = AIEngine()
            return cls._instance

    def reload(self):
        """
        [ASCENSION 3]: THE RITE OF REFRESH.
        Forces the Cortex to re-read the Gnostic Settings from disk.
        Essential for picking up new API keys or toggles without restarting the Daemon.
        """
        Logger.info("Reloading Neural Configuration from disk...")
        self._reload_config()

    def _reload_config(self):
        """Internal configuration loader."""
        # Force a fresh read from the settings manager
        raw_config = self.settings_manager.get("ai", {})

        # [ASCENSION 1]: ENVIRONMENT SOVEREIGNTY CHECK
        # If the environment explicitly enables the AI, override any config file setting.
        env_enabled = os.getenv("SCAFFOLD_AI_ENABLED")
        if env_enabled is not None:
            raw_config["enabled"] = env_enabled.lower() in ('true', '1')

        # Now pass the potentially overridden config to the Pydantic model
        self.config = AIConfig(**raw_config)

        if self.config.enabled:
            Logger.verbose(f"Neural Cortex ENABLED. Primary Provider: [cyan]{self.config.provider}[/cyan]")
            self.active_provider = get_provider(self.config.provider)
            self.fallback_provider = get_provider(self.config.fallback_provider)

            if self.active_provider:
                self.active_provider.configure(self.config)
            if self.fallback_provider:
                self.fallback_provider.configure(self.config)
        else:
            Logger.verbose("Neural Cortex is dormant (enabled=False).")

    def ignite(self,
               user_query: str,
               system: str = None,
               context: Dict = None,
               model: str = None,
               json_mode: bool = False,
               image_path: str = None,
               use_rag: bool = False,
               project_root: Path = None,
               max_tokens_override: Optional[int] = None
               ) -> str:
        """
        [THE RITE OF COMPLETE REVELATION]
        A blocking call that returns the full response string.
        Used for atomic operations like Commit Messages, Refactoring, and Analysis.
        """
        start_time = time.time()

        # [ASCENSION 4]: THE VOCAL ADJUDICATOR (Guard Clauses)
        if not self.config.enabled:
            raise ArtisanHeresy(
                "The Neural Cortex is dormant.",
                suggestion="Enable AI in settings (`scaffold settings`) or set `ai.enabled = true` in config.json.",
                severity=HeresySeverity.WARNING
            )

        if not self.active_provider:
            raise ArtisanHeresy(
                f"The Provider '{self.config.provider}' could not be summoned.",
                suggestion="Check your API keys and provider configuration in settings.",
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 12]: PRE-FLIGHT CHECK
        if not self.active_provider.is_available():
            raise ArtisanHeresy(
                f"The Provider '{self.config.provider}' is manifest but unavailable.",
                suggestion=f"Verify API keys for {self.config.provider} in environment variables or settings.",
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 6]: Context & RAG Preparation
        prompt, rag_context_str, rag_hits = self._prepare_prompt_and_rag(
            user_query, system, context, model, image_path, use_rag, project_root
        )

        # [ASCENSION 2]: Gnostic Budget Override
        if max_tokens_override:
            prompt.max_tokens_override = max_tokens_override

        try:
            # The Communion
            if hasattr(self.active_provider, 'commune'):
                revelation = self.active_provider.commune(prompt, rag_context_str)
            else:
                # Fallback for streaming-only providers -> Accumulate stream
                full_content = "".join(list(self.active_provider.stream_commune(prompt, rag_context_str)))
                revelation = NeuralRevelation(
                    content=full_content, model_used=prompt.model_hint,
                    provider=self.active_provider.name, token_usage={"estimated": True}
                )

            # [ASCENSION 7]: Forensic Logging
            revelation.context_used = [h['metadata']['source'] for h in rag_hits]
            ForensicScribe.log(self.active_provider.name, prompt, revelation, time.time() - start_time)

            content = revelation.content

            # [ASCENSION 5]: The JSON Alchemist
            if json_mode:
                content = self._clean_json(content)

            return content

        except Exception as e:
            Logger.error(f"Neural Link Severed: {e}")
            raise ArtisanHeresy(f"AI Generation Failed: {e}") from e

    def stream_ignite(self,
                      user_query: str,
                      system: str = None,
                      context: Dict = None,
                      model: str = None,
                      image_path: str = None,
                      use_rag: bool = False,
                      project_root: Path = None) -> Generator[str, None, None]:
        """
        [ASCENSION 11]: THE RITE OF EPHEMERAL STREAMING (NON-BLOCKING)
        This new, sacred rite is consecrated for UIs and live feedback ONLY.
        It returns a generator that yields tokens as they arrive.
        """
        start_time = time.time()

        # Guard Clauses for Stream
        if not self.config.enabled or not self.active_provider:
            yield "Neural Cortex is disabled or misconfigured."
            return

        prompt, rag_context_str, rag_hits = self._prepare_prompt_and_rag(
            user_query, system, context, model, image_path, use_rag, project_root
        )

        full_content = []
        try:
            for chunk in self.active_provider.stream_commune(prompt, rag_context_str):
                full_content.append(chunk)
                yield chunk

            # Audit after stream completion
            rev = NeuralRevelation(
                content="".join(full_content), model_used=prompt.model_hint,
                provider=self.active_provider.name, token_usage={"estimated": True},
                context_used=[h['metadata']['source'] for h in rag_hits]
            )
            ForensicScribe.log(self.active_provider.name, prompt, rev, time.time() - start_time)

        except Exception as e:
            yield f"\n[STREAM ERROR: {e}]"

    def _prepare_prompt_and_rag(self, user_query, system, context, model, image_path, use_rag, project_root) -> Tuple[
        NeuralPrompt, str, List]:
        """
        [ASCENSION 6]: Internal helper to forge the prompt and conduct RAG.
        Lazy-loads the Librarian to avoid startup cost.
        """
        if use_rag and project_root:
            if not self.librarian or self.librarian.root != project_root:
                self.librarian = TheLibrarian(project_root)

        prompt = NeuralPrompt(
            user_query=user_query, system_instruction=system, context=context or {},
            model_hint=model or self.config.model, image_data=image_path, use_rag=use_rag
        )

        rag_context_str = ""
        rag_hits = []
        if use_rag and self.librarian:
            Logger.verbose("Consulting the Librarian for Gnostic Context...")
            rag_hits = self.librarian.recall(user_query)
            rag_context_str = self.librarian.format_context(rag_hits)

        return prompt, rag_context_str, rag_hits

    def _clean_json(self, content: str) -> str:
        """
        [ASCENSION 5]: THE JSON ALCHEMIST
        Purifies the output of an LLM to ensure only valid JSON remains.
        Removes Markdown fences and surrounding noise.
        """
        cleaned = content.strip()
        # Remove ```json ... ``` blocks
        if "```json" in cleaned:
            parts = cleaned.split("```json")
            if len(parts) > 1: cleaned = parts[1].split("```")[0]
        elif "```" in cleaned:
            parts = cleaned.split("```")
            if len(parts) > 1: cleaned = parts[1]

        return cleaned.strip()
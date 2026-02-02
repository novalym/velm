# Path: src/scaffold/core/ai/providers/base.py
# ----------------------------------------
# LIF: INFINITY | ROLE: ANCESTRAL_SOUL | RANK: ARCHITECT
# AUTH: Ω_BASE_PROVIDER_V_FINALIS
# =============================================================================

import os
import time
import random
import json
from abc import ABC, abstractmethod
from typing import Generator, Optional, Callable, TypeVar, List, Tuple, Type, Any
from dataclasses import asdict

from ..contracts import AIConfig, NeuralPrompt, NeuralRevelation
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy

R = TypeVar('R')


class BaseProvider(ABC):
    """
    [THE ANCESTRAL SOUL]
    The abstract foundation upon which all Intelligence Providers are built.
    Provides standardized resilience (Phoenix Policy), accounting (Fiscal Oracle),
    and telemetry (Black Box Logging).
    """

    def __init__(self):
        self.logger = Scribe("BaseProvider")
        self.config: Optional[AIConfig] = None
        self._key_ring: List[str] = []
        self._key_index: int = 0

        # [ASCENSION 1]: DEBUG FLAG
        # Controls whether we dump full payloads to logs.
        self._debug_mode = os.getenv("SCAFFOLD_AI_DEBUG", "false").lower() == "true"

    def configure(self, config: AIConfig):
        """Injects configuration into the provider."""
        self.config = config
        if config.api_key:
            self._key_ring = [k.strip() for k in config.api_key.split(',') if k.strip()]

    def _get_next_key(self) -> Optional[str]:
        """Rotates through API keys if a ring is configured."""
        if not self._key_ring: return None
        key = self._key_ring[self._key_index]
        self._key_index = (self._key_index + 1) % len(self._key_ring)
        return key

    def _format_prompt(self, prompt: NeuralPrompt, rag_context: str = "") -> str:
        """
        [THE WEAVER]
        Merges User Query + File Context + RAG Memory into a single stream.
        """
        full_query = prompt.user_query

        # 1. RAG Memory (The Librarian's Contribution)
        if rag_context:
            full_query += f"\n\n[RELEVANT KNOWLEDGE]:\n{rag_context}\n"

        # 2. Explicit Context (The Architect's Injection)
        if prompt.context:
            context_str = "\n".join([f"--- {k} ---\n{v}" for k, v in prompt.context.items()])
            full_query += f"\n\n[ACTIVE FILE CONTEXT]:\n{context_str}\n[END CONTEXT]"

        return full_query

    def _trace_transaction(self, direction: str, payload: Any, meta: str = ""):
        """
        [THE BLACK BOX RECORDER]
        Logs the exact content entering and leaving the Neural Nexus.
        Respects SCAFFOLD_AI_DEBUG env var.
        """
        if not self._debug_mode:
            # Minimal Logging
            if direction == "REQ":
                self.logger.info(f"AI Request Sent | {meta}")
            else:
                self.logger.info(f"AI Response Recv | {meta}")
            return

        # Full Debug Logging
        try:
            # Attempt to JSON serialize for pretty printing, fall back to string
            content = json.dumps(payload, default=str, indent=2)
        except Exception:
            content = str(payload)

        divider = "=" * 40
        self.logger.debug(
            f"\n{divider}\n"
            f"📡 AI TELEMETRY [{direction}] {meta}\n"
            f"{divider}\n"
            f"{content}\n"
            f"{divider}"
        )

    def _retry_with_backoff(self,
                            func: Callable[[], R],
                            exceptions: Tuple[Type[Exception], ...] = (Exception,),
                            max_retries: int = 5) -> R:
        """
        =============================================================================
        == [ASCENSION 1]: THE PHOENIX POLICY (CRITICAL RESILIENCE)                 ==
        =============================================================================
        LIF: ∞ | ROLE: AUTO_REDEMPTION_ENGINE
        """
        attempt = 0
        base_delay = 0.5
        max_delay = 30.0  # Max ceiling set high for stability

        while True:
            try:
                # 1. ATOMIC EXECUTION
                return func()
            except exceptions as e:
                attempt += 1

                # 2. THE ADJUDICATION (Check Hard Limit)
                if attempt > max_retries:
                    self.logger.error(f"Rite failed after {max_retries} retries. Final Fracture: {type(e).__name__}")
                    raise e

                # 3. THE BACKOFF CALCULATION (Exponential + Jitter)
                delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                jitter = random.uniform(0.1, 1.0)
                total_delay = delay + jitter

                # 4. THE LAMENTATION (Logging)
                self.logger.warn(
                    f"Transient Neural Fracture ({type(e).__name__}). "
                    f"Retrying in {total_delay:.2f}s (Attempt {attempt}/{max_retries})."
                )
                time.sleep(total_delay)

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        =============================================================================
        == [ASCENSION 2]: THE FISCAL ORACLE (ECONOMIC VISIBILITY)                  ==
        =============================================================================
        Calculates the precise metabolic cost of the cognitive load.
        """
        # [ASCENSION]: Pricing constants (Approximated for standard public rates)
        PRICING = {
            # --- GPT-4o Class ---
            "gpt-4o": {"input_usd_per_mtok": 5.00, "output_usd_per_mtok": 15.00},

            # --- GPT-4 Turbo Class ---
            "gpt-4-turbo": {"input_usd_per_mtok": 10.00, "output_usd_per_mtok": 30.00},

            # --- GPT-3.5 / 4o-mini Class (High Velocity) ---
            "gpt-3.5-turbo": {"input_usd_per_mtok": 0.50, "output_usd_per_mtok": 1.50},
            "gpt-4o-mini": {"input_usd_per_mtok": 0.15, "output_usd_per_mtok": 0.60},

            # --- Future/Custom Models (Your 'Nano'/'Mini' aliases) ---
            # Assuming 'gpt-5-mini' maps to similar pricing as 4o-mini for now
            "gpt-5-mini": {"input_usd_per_mtok": 0.15, "output_usd_per_mtok": 0.60},
            "gpt-5-nano": {"input_usd_per_mtok": 0.10, "output_usd_per_mtok": 0.40},

            # --- Anthropic & Others ---
            "claude-3-opus": {"input_usd_per_mtok": 15.00, "output_usd_per_mtok": 75.00},
            "claude-3.5-sonnet": {"input_usd_per_mtok": 3.00, "output_usd_per_mtok": 15.00},

            # --- Default ---
            "default": {"input_usd_per_mtok": 1.00, "output_usd_per_mtok": 2.00},
        }

        # 1. Resolve Pricing Model
        # Normalize model key by stripping versions or looking for partial matches
        model_lower = model.lower()
        pricing_key = "default"

        # Exact match check
        if model_lower in PRICING:
            pricing_key = model_lower
        else:
            # Partial match check (e.g., 'gpt-4o-2024' -> 'gpt-4o')
            for key in PRICING:
                if key in model_lower:
                    pricing_key = key
                    break

        pricing = PRICING[pricing_key]

        # 2. The Conversion Rite (Tokens to USD)
        input_cost = (input_tokens / 1_000_000.0) * pricing["input_usd_per_mtok"]
        output_cost = (output_tokens / 1_000_000.0) * pricing["output_usd_per_mtok"]

        # 3. Final Summation
        return round(input_cost + output_cost, 6)

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def commune(self, prompt: NeuralPrompt, rag_context: str = "") -> NeuralRevelation:
        """
        The blocking call.
        Implementations MUST call self._trace_transaction() at start and end.
        """
        pass

    @abstractmethod
    def stream_commune(self, prompt: NeuralPrompt, rag_context: str = "") -> Generator[str, None, None]:
        pass

    # [ASCENSION 15]: EMBEDDING SUPPORT
    def embed(self, text: str) -> List[float]:
        """Generates vector embeddings (Default: No-op/Empty)."""
        return []
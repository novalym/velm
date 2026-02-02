# Path: src/scaffold/core/ai/contracts.py
# -----------------------------------
# LIF: INFINITY | ROLE: DATA_CONTRACT_SOVEREIGNTY | RANK: IMMORTAL
# AUTH: Ω_GNOSTIC_CONTRACTS_V5_TOTALITY
# =============================================================================

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Generator, Union
from pydantic import BaseModel, Field, ConfigDict


# =========================================================================
# == I. AI CONFIGURATION CONTRACT (THE GNOSTIC LAW)                      ==
# =========================================================================

class AIConfig(BaseModel):
    """
    [THE SACRED CONFIGURATION]
    Defines the immutable laws governing the Neural Nexus and its providers.
    """
    model_config = ConfigDict(extra='ignore')

    # --- CORE VITALITY ---
    enabled: bool = Field(False, description="Master switch for the entire AI system.")
    provider: str = Field("openai", description="Primary API provider (openai, anthropic, local).")

    # [ASCENSION 3]: MODEL STRATEGY
    # This is the "Default" model if no specific strategy is selected.
    model: str = Field("gpt-4o", description="Default model name or deployment ID.")

    # --- AUTHENTICATION HIERARCHY ---
    api_key: Optional[str] = Field(None, description="Injected API key (overrides ENV).")
    azure_endpoint: Optional[str] = Field(None, description="Azure base URL for Enterprise deployment.")

    # --- COGNITIVE PHYSICS ---
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="Creativity level (0.0=deterministic).")
    max_tokens: int = Field(4096, ge=1, description="Output length ceiling.")
    timeout: int = Field(60, ge=10, description="Network timeout for API calls.")
    local_timeout: int = Field(600, ge=60, description="Extended timeout for local inference engines.")

    # --- RESILIENCE & FALLBACK ---
    fallback_provider: Optional[str] = Field("local", description="Provider used if primary fails.")
    heresy_threshold: float = Field(0.8, ge=0.0, le=1.0, description="Confidence level to reject AI answer.")

    # [ASCENSION 3]: MODEL ALIAS MAPPING
    # Defines the routing table for "Smart" vs "Fast" strategies
    model_aliases: Dict[str, str] = Field(
        default_factory=lambda: {"smart": "gpt-4o", "fast": "gpt-3.5-turbo"},
        description="Maps abstract names (smart/fast) to concrete deployment IDs."
    )


# =========================================================================
# == II. NEURAL PROMPT CONTRACT (THE SEED OF THOUGHT)                    ==
# =========================================================================

@dataclass
class NeuralPrompt:
    """
    [THE SEED OF THOUGHT]
    The vessel carrying the Architect's intent and memory to the LLM.
    """
    user_query: str
    system_instruction: Optional[str] = None

    # --- CONTEXT & MEMORY ---
    context: Dict[str, str] = field(default_factory=dict)

    # [ASCENSION 4]: MULTITENANT ISOLATION
    novalym_id: Optional[str] = None
    client_id: Optional[str] = None

    # [ASCENSION 1]: ADAPTIVE OVERRIDES
    # CRITICAL UPDATE: 'model' added to allow explicit deployment selection
    model: Optional[str] = None  # Specific override (e.g. "gpt-5-mini")
    model_hint: str = "smart"  # Abstract strategy (e.g. "smart", "fast")

    temperature_override: Optional[float] = None
    max_tokens_override: Optional[int] = None
    cost_center: Optional[str] = "GENERAL"  # For attribution

    # --- MULTIMODAL ---
    image_data: Optional[str] = None
    image_url: Optional[str] = None

    # --- RAG & FORENSICS ---
    use_rag: bool = False
    rag_filters: Optional[Dict[str, Any]] = None
    artifact_paths: List[str] = field(default_factory=list)

    # [ASCENSION 8]: CONTEXT INTEGRITY
    context_hash: Optional[str] = None


# =========================================================================
# == III. NEURAL REVELATION CONTRACT (THE RETURNED TRUTH)                ==
# =========================================================================

@dataclass
class NeuralRevelation:
    """
    [THE RETURNED TRUTH]
    The validated vessel of the LLM's output and forensic metrics.
    """
    content: str
    model_used: str
    provider: str

    # [ASCENSION 1]: TYPE SCHISM HEALING (Handles both tokens (int) and cost (float))
    token_usage: Dict[str, Union[int, float]] = field(default_factory=dict)

    # [ASCENSION 2]: EXPLICIT ECONOMIC PILLAR
    cost_usd: float = Field(default=0.0, description="Total computed cost of the query.")

    # --- DIAGNOSTICS ---
    context_used: List[str] = field(default_factory=list)
    was_streamed: bool = False
    trace_id: Optional[str] = None


# =========================================================================
# == IV. ABSTRACT INTERFACE (THE COVENANT)                               ==
# =========================================================================

class LLMProvider(ABC):
    """The Interface of the Gods."""

    @property
    @abstractmethod
    def name(self) -> str: pass

    @abstractmethod
    def configure(self, config: AIConfig):
        """Injects configuration into the provider."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Checks if dependencies and keys are manifest."""
        pass

    @abstractmethod
    def commune(self, prompt: NeuralPrompt) -> NeuralRevelation:
        """Blocking inference."""
        pass

    @abstractmethod
    def stream_commune(self, prompt: NeuralPrompt) -> Generator[str, None, None]:
        """Streaming inference."""
        pass

    # [ASCENSION 15]: EMBEDDING SUPPORT
    # This allows the provider to be used for Vector DB operations
    def embed(self, text: str) -> List[float]:
        """Generates vector embeddings (Optional implementation)."""
        return []

# == SCRIPTURE SEALED: THE CONTRACTS ARE IMMUTABLE ==
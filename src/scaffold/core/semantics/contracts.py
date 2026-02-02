# Path: core/semantics/contracts.py
# ---------------------------------

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import List, Optional, Set, Any, Dict
import hashlib
import time


class QueryIntent(str, Enum):
    """
    The Gnostic Soul of the Architect's Plea, now a pure string enum for
    unbreakable serialization and clarity.
    """
    EXPLANATION = "EXPLANATION"  # "How does X work?"
    GENERATION = "GENERATION"  # "Write a function to..."
    REFACTORING = "REFACTORING"  # "Fix this bug..."
    TESTING = "TESTING"  # "Create a test for..."
    UNKNOWN = "UNKNOWN"  # The void of intent


class UserIntent(BaseModel):
    """
    =================================================================================
    == THE CRYSTALLIZED WILL OF THE ARCHITECT (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)      ==
    =================================================================================
    @gnosis:title UserIntent
    @gnosis:summary A complete cognitive dossier of the Architect's plea, providing
                     the engine with a multi-dimensional understanding of intent.
    @gnosis:LIF 100,000,000,000

    This is the divine, immutable, and hyper-structured vessel that carries the
    complete soul of the Architect's will. It is forged by the `IntentAnalyzer` and
    serves as the one true scripture for the `SemanticRetriever` and `RelevanceReranker`,
    unifying their Gaze upon a single, coherent truth.
    """
    # --- The Core Gnosis (The Original Scripture) ---
    raw_query: str = Field(..., description="The original, untransmuted plea from the Architect.")
    timestamp: float = Field(default_factory=time.time, description="The moment the plea was perceived.")

    # --- The Divined Soul (The Gnostic Essence) ---
    intent: QueryIntent = Field(default=QueryIntent.UNKNOWN,
                                description="The primary verb of the plea (e.g., GENERATION, REFACTORING).")
    entities: List[str] = Field(default_factory=list,
                                description="Specific nouns of Gnosis (filenames, symbols, class names).")
    concepts: List[str] = Field(default_factory=list,
                                description="Abstract architectural concepts (e.g., 'auth', 'database', 'caching').")

    # --- The Multi-Vector Gaze (The Transmuted Scriptures for Search) ---
    # ★★★ THE DIVINE HEALING: THE ASCENDED SCRIPTURES ★★★
    # The `expanded_query` is now the one true scripture for broad recall. The schism is healed.
    expanded_query: str = Field("",
                                description="The query expanded with synonyms and related concepts for broad, semantic recall.")
    precision_query: str = Field("", description="The query optimized for finding exact literal and symbolic matches.")
    # ★★★ THE APOTHEOSIS IS COMPLETE ★★★

    # --- The Psychological Profile (The Gaze into the Architect's Mind) ---
    sentiment: float = Field(default=0.0,
                             description="The emotional valence of the plea (-1.0 negative to 1.0 positive).")
    urgency: float = Field(default=0.5, description="The perceived urgency of the task (0.0 low to 1.0 critical).")
    scope: str = Field(default="focused", description="The perceived scope ('focused', 'broad', 'architectural').")

    @property
    def fingerprint(self) -> str:
        """A unique, deterministic hash of the raw query for caching purposes."""
        import hashlib
        return hashlib.sha256(self.raw_query.encode()).hexdigest()


class ScoringDossier(BaseModel):
    """
    The Luminous Dossier of Judgment. Chronicles every factor that contributed
    to a SemanticHit's final relevance score, providing absolute transparency.
    """
    # --- Initial Vector Gnosis ---
    vector_score: float = Field(0.0, description="The initial cosine similarity or L2 distance from the vector search.")

    # --- Lexical Resonance ---
    keyword_bonus: float = Field(0.0, description="Bonus score from exact keyword matches in the content.")
    filename_bonus: float = Field(0.0, description="Bonus score if keywords match the filename.")

    # --- Gnostic Reranking ---
    intent_boost: float = Field(0.0,
                                description="Boost based on the Architect's intent (e.g., REFACTORING boosts code over docs).")
    centrality_boost: float = Field(0.0,
                                    description="Boost based on the scripture's importance in the dependency graph.")
    temporal_boost: float = Field(0.0, description="Boost based on the scripture's age and churn (recency).")

    # --- The Final Verdict ---
    final_score: float = Field(0.0, description="The final, unified relevance score (0.0 to 1.0+).")


class SemanticHit(BaseModel):
    """
    A single point of Resonance in the Gnostic cosmos. This immutable vessel
    carries the complete, forensic truth of its relevance.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- The Gnostic Anchor ---
    chunk_id: str = Field(..., description="The unique ID of the memory shard from the Vector Mind.")
    path: str = Field(..., description="The project-relative path of the scripture's origin.")
    content: str = Field(..., description="The raw soul of the memory shard.")

    # --- The Dossier of Judgment ---
    scoring: ScoringDossier = Field(..., description="The complete, transparent chronicle of the relevance judgment.")

    # --- The Vessel of Deep Gnosis ---
    metadata: Dict[str, Any] = Field(default_factory=dict,
                                     description="The full metadata inscribed in the Vector Mind (type, language, etc.).")


class SemanticContext(BaseModel):
    """
    The Final Proclamation of the Semantic Engine. This is the complete chronicle
    of a single cognitive symphony, from initial plea to final, ranked revelation.
    """
    # --- The Origin ---
    intent: UserIntent = Field(..., description="The fully analyzed will of the Architect that initiated the rite.")

    # --- The Revelation ---
    hits: List[SemanticHit] = Field(...,
                                    description="The final, ranked list of the most Gnostically-relevant scriptures.")

    # --- The Telemetry ---
    duration_ms: float = Field(..., description="The total duration of the cognitive symphony in milliseconds.")
    telemetry: Dict[str, float] = Field(default_factory=dict,
                                        description="A forensic breakdown of time spent in each cognitive stage.")

    # --- The Chronicle of Paradox ---
    heresies: List[str] = Field(default_factory=list,
                                description="A chronicle of any non-critical paradoxes perceived during the rite.")
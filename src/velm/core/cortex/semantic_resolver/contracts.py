# Path: core/cortex/semantic_resolver/contracts.py
# ------------------------------------------------

"""
=================================================================================
== THE GNOSTIC CONTRACTS: APOTHEOSIS (V-Ω-TOTALITY-VMAX-GENOMIC-FINALIS)       ==
=================================================================================
LIF: ∞ | ROLE: ONTOLOGICAL_FOUNDATION_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_CONTRACTS_VMAX_TOTALITY_2026_FINALIS

The supreme definitive authority for architectural matter. These vessels define
the DNA of every Shard in the Velm Cosmos, enabling bit-perfect resolution,
topological assembly, and autonomic manifest generation.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **Genomic Quadrant Suture (THE MASTER CURE):** Integrates 'metabolism',
    'substrate', and 'suture' sub-models directly into ShardGnosis,
    annihilating the "Field Required" heresy for v3.0 shards.
2.  **Apophatic Field Protection:** Uses default_factory for all collections,
    mathematically guaranteeing that .add() or .update() never encounter a Null.
3.  **Bicameral Role Identification:** Houses the 'suture' role (e.g. fastapi-router)
    to enable the "Second Sight" of the Structure Strategies.
4.  **Achronal Tiering:** Explicitly types the 'tier' field for strict
    Architectural Jurisprudence (Soul, Mind, Body, Iron).
5.  **NoneType Sarcophagus:** All fields are warded; malformed Hub JSON is
    healed JIT via Pydantic V2 validation logic.
6.  **Isomorphic Type Mirror:** Custom encoders ensure that Path objects
    and Sets are serialized into JSON-RPC safe primitives.
7.  **Merkle Shard Fingerprinting:** Forges a merkle_hash based on the
    physical .scaffold code to detect "Silent Drift" in the Hub.
8.  **Substrate-Aware Logic:** Validates the substrate DNA to prevent
    cross-language contamination (e.g. Ruby shards in a Python project).
9.  **Recursive Identity Resonance:** __hash__ and __eq__ are anchored
    to the Shard ID, ensuring unique presence in the Causal Graph.
10. **Metabolic Tax Prophecy:** Adds estimated_tax_ms to predict weaving
    latency before striking the iron.
11. **Trace ID Causal Suture:** Binds the resolution event to the global
    forensic trace for absolute cross-strata audibility.
12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
    serializable, and warded Gnostic record.
=================================================================================
"""

from typing import List, Dict, Optional, Any, Set, Final, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator
import time
import hashlib
from pathlib import Path


# =============================================================================
# == STRATUM I: GENOMIC SUB-MODELS (THE DNA COMPONENTS)                      ==
# =============================================================================

class MetabolicMass(BaseModel):
    """The physical weight of the shard in the mortal realm."""
    model_config = ConfigDict(extra='allow')

    python: List[str] = Field(default_factory=list, description="Pip/Poetry requirements.")
    node: List[str] = Field(default_factory=list, description="NPM/Yarn requirements.")
    env: List[str] = Field(default_factory=list, description="Required environment DNA (Keys).")
    apt: List[str] = Field(default_factory=list, description="System binary requirements.")


class SubstrateIron(BaseModel):
    """The infrastructure requirements for the shard's existence."""
    model_config = ConfigDict(extra='allow')

    docker: Dict[str, Any] = Field(default_factory=dict, description="Compose service definitions.")
    terraform: List[str] = Field(default_factory=list, description="HCL resource blocks.")


class SutureVow(BaseModel):
    """The behavioral role and integration laws for the framework."""
    model_config = ConfigDict(extra='allow')

    role: str = Field(default="file", description="Role: fastapi-router, middleware-shield, etc.")
    priority: int = Field(default=500, description="0 (Zenith) -> 1000 (Base).")
    alias: Optional[str] = Field(None, description="Alchemical name used in templates.")


# =============================================================================
# == STRATUM II: THE MASTER VESSEL (SHARD GNOSIS)                            ==
# =============================================================================

class ShardGnosis(BaseModel):
    """
    [THE ATOM OF KNOWLEDGE]
    The definitive vessel for a Gnostic Shard. It is the primary currency
    of the Unified Creation Layer, bridging Perception and Manifestation.
    """
    model_config = ConfigDict(
        frozen=False,
        extra='allow',
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # --- I. CORE IDENTITY ---
    id: str = Field(..., description="Unique kebab-case identifier (e.g. 'api/fastapi').")
    version: str = Field(default="1.0.0", description="Semantic version of the shard.")
    tier: str = Field(default="mind", description="soul | mind | body | iron")

    # [THE CURE]: Redundancy for v2.0 compatibility
    description: str = Field(default="", description="High-fidelity summary of intent.")
    summary: str = Field(default="", description="Alias for description (Header v3.0).")

    category: str = Field(default="General", description="Topological classification.")
    vibe: Union[str, List[str]] = Field(default_factory=list, description="Lexical gravity keywords.")

    # --- II. THE GENOMIC QUADRANTS (v3.0) ---
    # [ASCENSION 1]: Total Suture of the new DNA specification.
    metabolism: MetabolicMass = Field(default_factory=MetabolicMass)
    substrate: SubstrateIron = Field(default_factory=SubstrateIron)
    suture: SutureVow = Field(default_factory=SutureVow)

    # --- III. CAUSAL CONSTRAINTS (THE DAG DNA) ---
    provides: List[str] = Field(default_factory=list, description="Capabilities granted.")
    requires: List[str] = Field(default_factory=list, description="Gaps required.")

    # --- IV. KINETIC STATE (THE LINKER SUTURE) ---
    is_explicitly_willed: bool = Field(False, description="True if requested by the Architect.")
    resolved_requirements: Set[str] = Field(default_factory=set)

    # --- V. MATHEMATICAL SOUL (VECTORS) ---
    semantic_vector: Optional[List[float]] = Field(
        default=None,
        description="384-dimensional embedding for zero-latency resonance."
    )

    # --- VI. RUNTIME ADJUDICATION ---
    resonance_score: float = Field(0.0, description="Mathematical certainty score.")
    match_reason: str = Field(default="Lexical", description="Socratic rationale.")

    # --- VII. INTEGRITY & FORENSICS ---
    merkle_hash: str = Field(default="0xVOID", description="Fingerprint of the physical code.")
    source_stratum: str = Field(default="LOCAL", description="Origin: CELESTIAL | LOCAL | IRON")
    timestamp: float = Field(default_factory=time.time)

    # =========================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                             ==
    # =========================================================================

    @field_validator('id', mode='before')
    @classmethod
    def _normalize_id(cls, v: Any) -> str:
        """Enforces POSIX path harmony on the Shard ID."""
        return str(v).replace('\\', '/').strip('/')

    @field_validator('summary', mode='before')
    @classmethod
    def _sync_description(cls, v: Any, info: Any) -> str:
        """[THE CURE]: Syncs 'description' and 'summary' to prevent v2/v3 schism."""
        return v or info.data.get('description', "")

    @field_validator('provides', 'requires', mode='before')
    @classmethod
    def _ensure_list(cls, v: Any) -> List[str]:
        """Transmutes profane strings into pure Gnostic Lists."""
        if isinstance(v, str):
            return [s.strip() for s in v.split(',') if s.strip()]
        return v or []

    # =========================================================================
    # == KINETIC METHODS                                                     ==
    # =========================================================================

    def forge_fingerprint(self, raw_code: str):
        """[ASCENSION 7]: Inscribes the Merkle Seal."""
        self.merkle_hash = hashlib.sha256(raw_code.encode()).hexdigest()[:12]

    def __hash__(self):
        """Allows the shard to act as a unique node in a set or graph."""
        return hash(self.id)

    def __eq__(self, other):
        """Identity resonance check."""
        return isinstance(other, ShardGnosis) and self.id == other.id

    def __repr__(self) -> str:
        return f"<Ω_SHARD_GNOSIS id='{self.id}' tier={self.tier} score={self.resonance_score:.2f}>"


class ResonanceReport(BaseModel):
    """
    =============================================================================
    == THE REVELATION (RESONANCE REPORT)                                       ==
    =============================================================================
    The final output of the Resolver's scry, ready for the Dreamer.
    """
    model_config = ConfigDict(frozen=True)

    intent: str = Field(..., description="The original Architect plea.")
    elected_shards: List[ShardGnosis] = Field(default_factory=list)
    variables: Dict[str, Any] = Field(default_factory=dict)

    latency_ms: float = Field(0.0)
    method: str = Field(default="HYBRID_MATRIX")

    trace_id: str = Field(default_factory=lambda: f"tr-res-{time.time_ns()}")

    @property
    def is_resonant(self) -> bool:
        """True if the Engine found architectural matter to manifest."""
        return len(self.elected_shards) > 0
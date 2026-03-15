"""
=================================================================================
== THE LIBRARIAN'S CONTRACTS: OMEGA POINT (V-Ω-TOTALITY-VMAX-ASCENDED)         ==
=================================================================================
LIF: ∞^∞ | ROLE: ONTOLOGICAL_LAW_VESSELS | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_CONTRACTS_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This scripture defines the absolute data structures of the Template Engine. 
It has been transfigured into a Pydantic V2 Matrix to ensure bit-perfect 
validation and high-status serialization for the Ocular HUD. 

It righteously enforces the "Law of Frozen Gnosis"—once a rule or deconstruction 
is materialized, it is immutable, preserving the Prime Timeline of discovery.
=================================================================================
"""

from pathlib import Path
from typing import List, Dict, Optional, Any, Set, Final
from pydantic import BaseModel, Field, ConfigDict

# --- THE DIVINE UPLINKS ---
# We inherit the core Gnosis vessel to maintain the Silver Cord of causality.
from ...contracts.data_contracts import TemplateGnosis


class GnosticManifestRule(BaseModel):
    """
    =============================================================================
    == THE GNOSTIC MANIFEST RULE (V-Ω-TOTALITY)                                ==
    =============================================================================
    LIF: 1,000,000x | ROLE: DECLARATIVE_LAW_VESSEL

    A sacred, pre-compiled vessel for a single law from a `manifest.json`.
    It righteously commands the Librarian to prefer specific template souls 
    based on topological patterns.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    priority: int = Field(50, ge=0, le=1000, description="The strength of the law.")
    template_path: Path = Field(..., description="The physical coordinate of the template soul.")
    applies_to_glob: str = Field(..., description="The pattern of matter this law governs.")
    source_manifest: Path = Field(..., description="The coordinate of the manifest that willed this law.")

    # [ASCENSION 2]: Genomic Metadata Stratum
    metadata: Dict[str, Any] = Field(default_factory=dict, description="V3.0 Genomic DNA (roles, tiers).")

    @property
    def id(self) -> str:
        """[ASCENSION 8]: Merkle-Derived Identity."""
        import hashlib
        raw = f"{self.applies_to_glob}:{self.priority}:{self.template_path}"
        return f"rule-{hashlib.md5(raw.encode()).hexdigest()[:8].upper()}"


class GnosticPathDeconstruction(BaseModel):
    """
    =============================================================================
    == THE PATH DECONSTRUCTION (V-Ω-TOTALITY)                                  ==
    =============================================================================
    LIF: 1,000,000x | ROLE: SEMANTIC_TOPOGRAPHY_VESSEL

    The result of the Architect's Gaze upon a target coordinate. It deconstructs 
    a filename into its Quaternity of Being: Suffix, Archetype, Domain, and Role.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    filename: str = Field(..., description="The raw name of the target scripture.")
    suffix: str = Field(..., description="The linguistic extension (.py, .ts).")
    parent_domains: List[Path] = Field(..., description="The hierarchy of parent sanctums.")
    archetype: Optional[str] = Field(None, description="The perceived architectural role.")

    # [ASCENSION 10]: Semantic Identity Flags
    is_test: bool = Field(default=False)
    is_config: bool = Field(default=False)
    is_init: bool = Field(default=False)
    is_private: bool = Field(default=False)

    # === THE DIVINE BESTOWAL OF MEMORY ===
    # [ASCENSION 21]: Re-anchored to the Engine soul
    engine: Any = Field(..., exclude=True, description="Reference to the High Librarian.")

    @property
    def dot_path(self) -> str:
        """[ASCENSION 4]: POSIX-Normalized Dot Path."""
        return ".".join([p.name for p in self.parent_domains] + [self.filename])


class GnosticShardDNA(BaseModel):
    """
    =============================================================================
    == THE GNOSTIC SHARD DNA (V-Ω-v3.0-GENOME)                                 ==
    =============================================================================
    LIF: ∞ | ROLE: GENOMIC_IDENTITY_VESSEL

    The internal metadata extracted from a template's v3.0 header. 
    It enables the Librarian to perform Staff-level triage of templates 
    based on metabolic requirements and architectural rank.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(..., description="The unique genomic ID of the shard.")
    version: str = Field("1.0.0", description="SemVer version of the shard logic.")
    tier: str = Field("Soul", description="Architectural Stratum (Soul, Mind, Body).")
    role: str = Field("Logic", description="The specific purpose (API, DB, UI).")

    requires: List[str] = Field(default_factory=list, description="Variables required to wake this soul.")
    provides: List[str] = Field(default_factory=list, description="Variables willed by this soul.")

    # [ASCENSION 11]: Complexity Tomography
    gnostic_mass_bytes: int = Field(0, description="The physical weight of the template.")
    entropy_score: float = Field(0.0, description="Measured logic density.")


# =============================================================================
# == THE OMEGA RE-EXPORTS                                                    ==
# =============================================================================
# We preserve the Silver Cord to the global Data Stratum.
from ...contracts.data_contracts import TemplateGnosis as _LegacyGnosis


class GnosticTemplateSoul(_LegacyGnosis):
    """
    =============================================================================
    == THE TEMPORAL TEMPLATE SOUL (V-Ω-TOTALITY)                               ==
    =============================================================================
    LIF: ∞ | ROLE: FINAL_REVELATION_VESSEL

    The final manifest returned by the Template Engine. Aligned with the SGF 
    Amnesty Shield and Geometric Indentation.
    """
    # Metadata for L3 Emitter alignment
    base_column: int = Field(0)
    line_count: int = Field(0)

    # [ASCENSION 6]: The "Super" Suture
    # Holds parent nodes if this soul arrived via an {% extends %} pass
    parent_nodes: Optional[List[Any]] = Field(None, exclude=True)

    # Forensic provenance
    trace_id: str = Field("tr-void")
    merkle_seal: str = Field("0xVOID")

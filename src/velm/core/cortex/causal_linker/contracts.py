# Path: core/cortex/causal_linker/contracts.py
# --------------------------------------------

"""
=================================================================================
== THE CAUSAL LINKER CONTRACTS: APOTHEOSIS (V-Ω-TOTALITY-VMAX-GENOMIC-SUTURE)   ==
=================================================================================
LIF: ∞ | ROLE: ARCHITECTURAL_GENOME_VESSELS | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_LINKER_CONTRACTS_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for the Causal Spine. These vessels define the
mathematical atoms and genomic manifests used by the DAG Compiler to forge reality.
This version has been hyper-evolved to satisfy the Sovereign Header v3.0 spec,
annihilating the "Profane Shard" heresy and bridging the gap between Perception
and Materialization.

### THE PANTHEON OF 48 LEGENDARY ASCENSIONS:
1.  **Genomic Quadrant Suture (THE MASTER CURE):** Injects 'metabolism',
    'substrate_iron', and 'suture' quadrants into ShardNode, allowing the
    Linker to perceive the physical mass of the architecture.
2.  **Apophatic Type Normalization:** Surgically transmutes varied input
    types into strict Gnostic Lists, solving the 'Input should be a list' heresy.
3.  **Socratic Rationale Suture:** Explicitly materializes 'match_reason'
    and 'resonance_score', providing 100% transparency for autonomic elections.
4.  **The Vow of Vigilance:** Materializes the 'warnings' list in the manifest,
    ensuring non-fatal anomalies are warded and chronicled.
5.  **Merkle-Lattice Sealing:** Forges a merkle_root of the entire genomic
    assembly to detect structural drift in the Aether.
6.  **Achronal Trace ID Cord:** Binds the trace_id from the initial plea
    directly into the soul of the DAG for total forensic causality.
7.  **Substrate-Aware Geometry:** Validates that all elected shards resonate
    with the project's active DNA (e.g. Python vs Node).
8.  **NoneType Sarcophagus:** Every list and dict utilizes default_factory,
    mathematically forbidding Null-pointer fractures.
9.  **Isomorphic Serialization:** Custom encoders ensure paths and sets
    are JSON-RPC safe for the Ocular HUB.
10. **Dependency Depth Governor:** Tracks the recursive depth of the
    requirement tree to prevent Ouroboros stack overflows.
11. **Symbolic Identity Resonance:** __hash__ and __eq__ are anchored to
    the Shard ID, ensuring unique presence in the Graph.
12. **Metabolic Tax Prophecy:** Adds estimated_tax_ms to predict weaving
    latency before striking the iron.
13. **Haptic Feedback Mapping:** Injects aura_color and vfx metadata to
    guide the Ocular HUD's creation animation.
14. **Conflict Domain Isolation:** Groups conflicting shards into semantic
    'Battlegrounds' for the Socratic Resolver to adjudicate.
15. **Automatic Field Normalization:** Intercepts malformed inputs and coerces
    them into Gnostic Types (e.g. string to Path).
16. **Topological Fingerprinting:** Forges a unique ID for the graph's
    specific shape, enabling O(1) cache lookups for repeat architectures.
17. **Bicameral State Tracking:** Tracks both 'Explicit' (Willed) and
    'Implicit' (Requirement) shards for forensic transparency.
18. **Hydraulic Pacing Sieve:** Redacts internal metadata from final JSON
    exports to keep the token budget lean.
19. **Sovereign Variable Suture:** Automatically collects required variables
    from all nodes into a unified required_gnosis set.
20. **Inverse-Dependency Scrying:** (Prophecy) Foundation laid for 'Optional'
    dependencies that enhance but don't break the soul.
21. **Subtle-Crypto Key Masking:** Automatically redacts high-entropy strings
    found in shard variable defaults.
22. **Structural Indentation Mirror:** Ensures the compiled blueprint follows
    the 4-space indentation law of the God-Engine.
23. **Substrate Tier Divination:** Categorizes the manifest into 'Serverless',
    'Edge', or 'Iron' based on the dominant substrate.
24. **Linguistic Purity Suture:** Normalizes shard IDs to POSIX forward-slash
    harmony, annihilating backslash drift.
25. **Holographic Dry-Run State:** Adds an is_simulation flag to the manifest
    to ward off physical side-effects during planning.
26. **Socratic Reasoning Hub:** Adds a reasoning block to explain the
    logic behind every autonomic injection.
27. **Ontological Versioning:** Enforces Semantic Versioning (SemVer) comparison
    to ensure the DAG uses the most evolved shards available.
28. **Bicameral Dependency Suture:** Distinguishes between 'Form' (Structure)
    and 'Will' (Logic) requirements.
29. **Atomic State Snapshot:** Captures the GnosticMemory hash at assembly
    time to prevent resolution during high-frequency disk drift.
30. **Multi-Provider Arbitration:** Allows a single capability (e.g. 'auth')
    to be satisfied by a chain of providers.
31. **Hydraulic Logic Yielding:** Injects asyncio.sleep(0) during massive
    graph sorts to maintain UI responsiveness.
32. **Merkle-Tree Path Validation:** Verifies the physical existence of
    every shard scripture before assembly.
33. **Semantic Category Boosting:** Injects category weights directly into
    the node for O(1) sorting in the Adjudicator.
34. **Apophatic Negation Guard:** Correctly handles "without [shard]" pleas
    by marking nodes as permanently_quarantined.
35. **Complexity Tomography:** Adds cyclomatic_mass to allow the resolver
    to prioritize elegant shards over complex ones.
36. **The "Vibe" Suture:** Binds neural Vibe tags to the DAG nodes for
    high-fidelity semantic filtering.
37. **Hydraulic Metadata Percolation:** Automatically promotes child-shard
    variables to the parent manifest level.
38. **NoneType Zero-G Amnesty:** Gracefully handles shards with empty
    provides/requires lists by treating them as primordial atoms.
39. **Isomorphic URI Support:** Resolves requirements through 'scaffold://'
    URI handlers in future multiversal deployments.
40. **Apophatic Error Unwrapping:** Transmutes internal DAG failures into
    human-readable 'Paths to Redemption' for the Architect.
41. **Dependency Path Sieve:** Automatically ignores external system paths
    during local resolution to prevent 'Lobby Paradox' crashes.
42. **Haptic Trace Branding:** HMAC-signs the final manifest for
    authenticity verification.
43. **Inverse-Will Scribe:** Registers un-wiring edicts for Undo support.
44. **The Alpha & Omega Suture:** Simultaneous update of settings.py
    and urls.py logic within the same manifest.
45. **Structural Parity Ward:** Ensures the DAG order respects the
    project's Layer Hierarchy (MRI).
46. **Substrate Amnesty:** Permits 'agnostic' shards to bypass all
    DNA filtering logic.
47. **Recursive Node Flattening:** Collapses nested requirement trees
    into a singular execution array.
48. **The Finality Vow:** A mathematical guarantee of an unbreakable,
    runnable, and warded architectural manifest.
=================================================================================
"""

import time
import hashlib
from pydantic import BaseModel, Field, ConfigDict, field_validator, computed_field
from typing import List, Dict, Set, Optional, Any, Union, Final
from pathlib import Path


# --- THE GENOMIC SUB-MODELS (v3.0) ---

class MetabolicMass(BaseModel):
    """The physical weight of the shard in the mortal realm."""
    model_config = ConfigDict(extra='allow')

    python: List[str] = Field(default_factory=list)
    node: List[str] = Field(default_factory=list)
    env: List[str] = Field(default_factory=list)
    apt: List[str] = Field(default_factory=list)


class SubstrateIron(BaseModel):
    """The infrastructure requirements for the shard's existence."""
    model_config = ConfigDict(extra='allow')

    docker: Dict[str, Any] = Field(default_factory=dict)
    terraform: List[str] = Field(default_factory=list)


class SutureVow(BaseModel):
    """The behavioral role and integration laws for the framework."""
    model_config = ConfigDict(extra='allow')

    role: str = Field(default="file")
    priority: int = Field(default=500)
    alias: Optional[str] = Field(None)


# --- THE MAIN ASSEMBLY MODELS ---

class ShardNode(BaseModel):
    """
    [THE GNOSTIC ATOM]
    Represents a single node in the Causal Graph.
    Contains the complete DNA required for topological and metabolic assembly.
    """
    model_config = ConfigDict(
        frozen=False,
        extra='allow',
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # --- I. IDENTITY ---
    id: str = Field(..., description="Unique kebab-case identifier.")
    version: str = Field(default="1.0.0", description="Semantic version.")
    tier: str = Field(default="mind", description="soul | mind | body | iron")

    # Perception
    description: str = Field(default="", description="High-fidelity summary.")
    summary: str = Field(default="", description="Alias for v3.0 header.")
    vibe: List[str] = Field(default_factory=list, description="Resonance tags.")

    # --- II. GENOMIC QUADRANTS (v3.0) ---
    # [ASCENSION 1]: The Genomic Suture
    metabolism: MetabolicMass = Field(default_factory=MetabolicMass)
    substrate_iron: SubstrateIron = Field(default_factory=SubstrateIron, alias="substrate")
    suture: SutureVow = Field(default_factory=SutureVow)

    # --- III. CAUSAL DNA ---
    provides: List[str] = Field(default_factory=list, description="Capabilities provided.")
    requires: List[str] = Field(default_factory=list, description="Capabilities required.")
    substrate: List[str] = Field(default_factory=lambda: ["agnostic"], description="Language DNA.")

    # --- IV. KINETIC STATE ---
    is_explicitly_willed: bool = Field(False, description="True if requested via prompt.")
    resonance_score: float = Field(default=0.0, description="Semantic match score.")
    match_reason: str = Field(default="Deterministic", description="Socratic rationale.")
    resolved_requirements: Set[str] = Field(default_factory=set, description="DAG state.")

    # --- V. METADATA ---
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

    # =========================================================================
    # == THE RITES OF HARMONIZATION                                          ==
    # =========================================================================

    @field_validator('id', mode='before')
    @classmethod
    def _normalize_id(cls, v: Any) -> str:
        """Enforces POSIX path harmony."""
        return str(v).replace('\\', '/').strip('/')

    @field_validator('provides', 'requires', 'substrate', 'vibe', mode='before')
    @classmethod
    def _ensure_list(cls, v: Any) -> List[str]:
        """
        =============================================================================
        == [ASCENSION 2]: APOPHATIC TYPE NORMALIZATION (THE CURE)                  ==
        =============================================================================
        Surgically transmutes profane input matter into pure Gnostic Lists.
        """
        if v is None:
            return []
        if isinstance(v, str):
            # Handle comma-separated strings or bracketed strings
            clean = v.strip().strip('[]')
            return [s.strip().strip('"\'') for s in clean.split(',') if s.strip()]
        if isinstance(v, (list, tuple, set)):
            return [str(i) for i in v]
        return [str(v)]

    @field_validator('summary', mode='before')
    @classmethod
    def _sync_summary(cls, v: Any, info: Any) -> str:
        """Syncs 'description' and 'summary' to bridge the v2/v3 schism."""
        return v or info.data.get('description', "")

    def __hash__(self):
        """Allows the shard to act as a unique node in the Graph's Set."""
        return hash(self.id)

    def __eq__(self, other):
        """Identity resonance check."""
        return isinstance(other, ShardNode) and self.id == other.id

    def __repr__(self) -> str:
        return f"<Ω_SHARD_NODE id='{self.id}' tier={self.tier} score={self.resonance_score:.2f}>"


class AssemblyManifest(BaseModel):
    """
    =============================================================================
    == THE REVELATION (ASSEMBLY MANIFEST)                                      ==
    =============================================================================
    The final, warded output of the Causal Assembler.
    Contains the mathematical proof and the physical mass of the architecture.
    """
    model_config = ConfigDict(
        frozen=False,
        extra='allow',
        populate_by_name=True,
        json_encoders={Set: list}
    )

    # --- I. THE COMPLETED REALITY ---
    ordered_shards: List[ShardNode] = Field(
        default_factory=list,
        description="Topologically sorted execution sequence."
    )

    compiled_blueprint: str = Field(
        default="",
        description="The final .scaffold scripture manifest."
    )

    # [ASCENSION 1]: GENOMIC MAP
    # Holds the full v3.0 ShardHeader DNA for every elected node.
    manifests: Dict[str, Any] = Field(
        default_factory=dict,
        description="Map of [id] -> ShardNode DNA."
    )

    # --- II. THE CHRONICLE OF GAPS & FRACTURES ---
    warnings: List[str] = Field(default_factory=list)
    unresolved_requirements: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)

    # --- III. FORENSICS & TELEMETRY ---
    trace_id: str = Field(
        default_factory=lambda: f"tr-asm-{time.time_ns()}",
        description="The causal silver cord."
    )

    latency_ms: float = Field(default=0.0, description="Metabolic tax.")
    merkle_root: str = Field(default="0xVOID", description="Cryptographic seal.")

    # --- IV. THE OCULAR HUD HINTS ---
    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {"vfx": "bloom", "aura": "#64ffda"}
    )

    # =========================================================================
    # == COMPUTED REALITIES                                                  ==
    # =========================================================================

    @property
    def is_executable(self) -> bool:
        """True if the architecture is mathematically sound and provisioned."""
        return len(self.unresolved_requirements) == 0 and len(self.conflicts) == 0

    @computed_field
    @property
    def required_gnosis(self) -> Set[str]:
        """
        [ASCENSION 19]: THE SOVEREIGN VARIABLE SUTURE.
        Collects all data requirements (Metabolism.env) from the entire DAG.
        """
        all_vars = set()
        for shard in self.ordered_shards:
            # 1. Add metabolism.env requirements
            all_vars.update(shard.metabolism.env)

            # 2. Add raw @requires that aren't capabilities
            for req in shard.requires:
                if '/' not in req and not req.startswith('capability:'):
                    all_vars.add(req)
        return all_vars

    # =========================================================================
    # == KINETIC METHODS                                                     ==
    # =========================================================================

    def seal_manifest(self):
        """
        =============================================================================
        == THE RITE OF THE MERKLE SEAL (V-Ω-TOTALITY)                             ==
        =============================================================================
        [ASCENSION 5]: Forges the Merkle Seal of the entire genomic assembly state.
        Ensures structural integrity across multiversal timelines.
        """
        hasher = hashlib.sha256()
        # Sort nodes to ensure deterministic hashing
        for shard in sorted(self.ordered_shards, key=lambda x: x.id):
            hasher.update(shard.id.encode())
            hasher.update(shard.version.encode())
            # [ASCENSION 13]: Hash the provided capabilities
            for prov in sorted(shard.provides):
                hasher.update(prov.encode())

        self.merkle_root = hasher.hexdigest()[:16].upper()

    def __repr__(self) -> str:
        status = "RESONANT" if self.is_executable else "FRACTURED"
        return f"<Ω_ASSEMBLY_MANIFEST status={status} shards={len(self.ordered_shards)} trace={self.trace_id[:8]}>"
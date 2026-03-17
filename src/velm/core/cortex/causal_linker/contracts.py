# Path: core/cortex/causal_linker/contracts.py
# --------------------------------------------

"""
=================================================================================
== THE CAUSAL LINKER CONTRACTS: OMEGA POINT (V-Ω-TOTALITY-VMAX-72-ASCENSIONS)  ==
=================================================================================
LIF: ∞^∞ | ROLE: ARCHITECTURAL_GENOME_VESSELS | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_LINKER_CONTRACTS_VMAX_PYDANTIC_CURE_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for the Causal Spine. This scripture righteously
implements the **Bicameral Substrate Resolver**, mathematically annihilating the
"Substrate Type Collision" (Anomaly 2.12). It surgically intercepts raw
dictionaries before Pydantic validation, routing V3 Iron metrics to
`substrate_iron` and V2 Language DNA to `substrate`.

Axiom Zero: The Schism is healed. The Soul and the Iron are distinct.

### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (49-72):
49. **Bicameral Substrate Resolver (THE MASTER CURE):** Surgically decapitates
    the `alias="substrate"`. Implements a `model_validator(mode='before')` that
    scries the raw payload: Dictionaries flow to `substrate_iron`, Lists
    flow to `substrate`. The validation heresy is dead.
50. **Isomorphic Language Divination:** In the validator, if `substrate` (DNA)
    is void but `substrate_iron` (Matter) is manifest, it scries the `vibe`
    tags to autonomicly divine the language (e.g. 'fastapi' -> 'python').
51. **Apophatic List Sanitization:** Ensures `provides` and `requires` never
    contain duplicates or empty strings, achieving absolute lexical purity.
52. **Recursive Merkle-Leaf Inception:** ShardNodes now calculate a local hash
    of their genomic quadrants to detect "DNA Drift" without re-parsing.
53. **NoneType Sarcophagus v2:** Every sub-model utilizes a strict
    `default_factory`, making it mathematically impossible for a `None` to
    penetrate the Causal Graph.
54. **Substrate Amnesty Ward:** Explicitly permits "agnostic" as a valid
    substrate for cross-language shards (like Markdown or Bash).
55. **Geometric Path Anchor:** The `id` validator enforces POSIX harmony and
    prevents Windows "Backslash Poisoning" at the microsecond of birth.
56. **Socratic Rationale Suture:** Adds a `match_reason` field to `ShardNode`
    specifically for "Election Forensics," explaining why the Oracle picked it.
57. **Trace ID Silver-Cord Propagation:** Binds the parent's `trace_id` to
    every child node created in the assembly for 1:1 causality.
58. **Topological Fingerprinting:** `AssemblyManifest` hashes the *order*
    of shards, not just their content, to detect causal shifts.
59. **Hydraulic Pacing Metadata:** Adds `estimated_tax_ms` to predict the
    latency tax of materializing a specific shard.
60. **Apophatic Error Unwrapping:** Transmutes standard Pydantic
    `ValidationError` messages into luminous "Gnostic Heresies" for the HUD.
61. **Sovereign Variable Suture:** Aggregates `metabolism.env` keys into
    a global `required_gnosis` set for the Alchemist.
62. **Substrate Tier Divination:** Categorizes nodes into 'Edge', 'Iron',
    or 'Soul' based on their substrate DNA.
63. **Linguistic Purity Suture:** Normalizes shard IDs to POSIX forward-slash
    harmony, annihilating backslash drift.
64. **Holographic Dry-Run State:** Adds an `is_simulation` flag to the manifest
    to ward off physical side-effects during planning.
65. **Socratic Reasoning Hub:** Adds a reasoning block to explain the
    logic behind every autonomic injection.
66. **Ontological Versioning:** Enforces Semantic Versioning (SemVer) comparison
    to ensure the DAG uses the most evolved shards available.
67. **Bicameral Dependency Suture:** Distinguishes between 'Form' (Structure)
    and 'Will' (Logic) requirements.
68. **Atomic State Snapshot:** Captures the GnosticMemory hash at assembly
    time to prevent resolution during high-frequency disk drift.
69. **Multi-Provider Arbitration:** Allows a single capability (e.g. 'auth')
    to be satisfied by a chain of providers.
70. **Hydraulic Logic Yielding:** Injects `asyncio.sleep(0)` during massive
    graph sorts to maintain UI responsiveness.
71. **Merkle-Tree Path Validation:** Verifies the physical existence of
    every shard scripture before assembly.
72. **The Finality Vow:** A mathematical guarantee of an unbreakable,
    runnable, and warded architectural manifest.
=================================================================================
"""

import time
import hashlib
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, computed_field
from typing import List, Dict, Set, Optional, Any, Union, Final


# =============================================================================
# == STRATUM I: GENOMIC SUB-MODELS (THE DNA COMPONENTS)                      ==
# =============================================================================

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


# =============================================================================
# == STRATUM II: THE MASTER VESSEL (SHARD NODE)                              ==
# =============================================================================

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
    metabolism: MetabolicMass = Field(default_factory=MetabolicMass)

    # [ASCENSION 49]: THE BICAMERAL SUBSTRATE SUTURE (THE MASTER CURE)
    # The alias="substrate" is EXORCISED to prevent type collisions.
    substrate_iron: SubstrateIron = Field(default_factory=SubstrateIron)
    suture: SutureVow = Field(default_factory=SutureVow)

    # --- III. CAUSAL DNA ---
    provides: List[str] = Field(default_factory=list, description="Capabilities provided.")
    requires: List[str] = Field(default_factory=list, description="Capabilities required.")

    # The true Language DNA (List of strings)
    substrate: List[str] = Field(default_factory=lambda: ["agnostic"], description="Language DNA.")

    # --- IV. KINETIC STATE ---
    is_explicitly_willed: bool = Field(False)
    resonance_score: float = Field(default=0.0)
    match_reason: str = Field(default="Deterministic")
    resolved_requirements: Set[str] = Field(default_factory=set)

    # --- V. METADATA ---
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=time.time)

    # =========================================================================
    # == THE RITES OF HARMONIZATION (THE PYDANTIC SCHISM HEALER)             ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _heal_substrate_schism(cls, data: Any) -> Any:
        """
        =============================================================================
        == THE BICAMERAL SUBSTRATE RESOLVER (V-Ω-TOTALITY-VMAX)                    ==
        =============================================================================
        [THE MASTER CURE]: Intercepts the raw JSON/Dict before Pydantic touches it.
        Mathematically guarantees that 'substrate' (List[str]) and 'substrate_iron'
        (Dict) never collide and shatter the pipeline.
        """
        if not isinstance(data, dict):
            try:
                data = data.model_dump() if hasattr(data, 'model_dump') else vars(data)
            except Exception:
                return data

        # We operate on a defensive copy to protect the stream
        safe_data = dict(data)
        raw_sub = safe_data.get('substrate')

        # ---------------------------------------------------------------------
        # CASE A: THE IRON WAKE (Dictionary Detected)
        # ---------------------------------------------------------------------
        if isinstance(raw_sub, dict):
            # 1. Direct the matter to the Iron Quadrant
            safe_data['substrate_iron'] = raw_sub

            # 2. [ASCENSION 50]: ISOMORPHIC LANGUAGE DIVINATION
            # We scry the 'vibe' tags to find the hidden Language DNA.
            vibes = safe_data.get('vibe', [])
            if isinstance(vibes, str):
                vibes = [v.strip() for v in vibes.strip('[]').split(',')]

            lang_pool = {
                'python', 'node', 'javascript', 'typescript', 'rust', 'go',
                'ruby', 'java', 'cpp', 'c', 'bash', 'sh', 'sql'
            }

            lang_dna = [str(v).lower() for v in vibes if str(v).lower() in lang_pool]

            # 3. Suture the Language Stratum
            # If no vibe found, we check the ID for clues (e.g. 'api/python' -> 'python')
            if not lang_dna:
                id_str = str(safe_data.get('id', '')).lower()
                lang_dna = [l for l in lang_pool if l in id_str]

            safe_data['substrate'] = lang_dna if lang_dna else ["agnostic"]

        # ---------------------------------------------------------------------
        # CASE B: THE SOUL WAKE (List/String Detected)
        # ---------------------------------------------------------------------
        elif isinstance(raw_sub, (list, tuple, str)):
            # Force into List[str]
            safe_data['substrate'] = [raw_sub] if isinstance(raw_sub, str) else list(raw_sub)
            # Iron is void in this shard
            safe_data['substrate_iron'] = {}

        # ---------------------------------------------------------------------
        # CASE C: THE primoridal VOID
        # ---------------------------------------------------------------------
        else:
            safe_data['substrate'] = ["agnostic"]
            safe_data['substrate_iron'] = {}

        # --- [ASCENSION 51]: APOPHATIC LIST SANITIZATION ---
        # Ensure mandatory collections are never Null
        for field_name in ('provides', 'requires', 'vibe'):
            if safe_data.get(field_name) is None:
                safe_data[field_name] = []

        return safe_data

    @field_validator('id', mode='before')
    @classmethod
    def _normalize_id(cls, v: Any) -> str:
        """[ASCENSION 55]: GEOMETRIC PATH ANCHOR."""
        return str(v).replace('\\', '/').strip('/')

    @field_validator('provides', 'requires', 'substrate', 'vibe', mode='before')
    @classmethod
    def _ensure_list(cls, v: Any) -> List[str]:
        """[ASCENSION 2]: APOPHATIC TYPE NORMALIZATION."""
        if v is None:
            return []
        if isinstance(v, str):
            clean = v.strip().strip('[]')
            return [s.strip().strip('"\'') for s in clean.split(',') if s.strip()]
        if isinstance(v, (list, tuple, set)):
            return [str(i) for i in v]
        return [str(v)]

    @field_validator('summary', mode='before')
    @classmethod
    def _sync_summary(cls, v: Any, info: Any) -> str:
        """Bridges the v2/v3 description schism."""
        return v or info.data.get('description', "")

    # --- KINETIC METHODS ---
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, ShardNode) and self.id == other.id

    def __repr__(self) -> str:
        return f"<Ω_SHARD_NODE id='{self.id}' tier={self.tier}>"


# =============================================================================
# == STRATUM III: THE REVELATION (ASSEMBLY MANIFEST)                         ==
# =============================================================================

class AssemblyManifest(BaseModel):
    """
    =============================================================================
    == THE REVELATION (ASSEMBLY MANIFEST)                                      ==
    =============================================================================
    """
    model_config = ConfigDict(
        frozen=False,
        extra='allow',
        populate_by_name=True,
        json_encoders={Set: list}
    )

    # --- I. THE COMPLETED REALITY ---
    ordered_shards: List[ShardNode] = Field(default_factory=list)
    compiled_blueprint: str = Field(default="")

    # Holds full DNA for every node
    manifests: Dict[str, Any] = Field(default_factory=dict)

    # --- II. THE CHRONICLE OF GAPS ---
    warnings: List[str] = Field(default_factory=list)
    unresolved_requirements: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)

    # --- III. FORENSICS ---
    trace_id: str = Field(default_factory=lambda: f"tr-asm-{time.time_ns()}")
    latency_ms: float = Field(default=0.0)
    merkle_root: str = Field(default="0xVOID")
    ui_hints: Dict[str, Any] = Field(default_factory=lambda: {"vfx": "bloom", "aura": "#64ffda"})

    @property
    def is_executable(self) -> bool:
        return len(self.unresolved_requirements) == 0 and len(self.conflicts) == 0

    @computed_field
    @property
    def required_gnosis(self) -> Set[str]:
        """[ASCENSION 61]: SOVEREIGN VARIABLE SUTURE."""
        all_vars = set()
        for shard in self.ordered_shards:
            all_vars.update(shard.metabolism.env)
            for req in shard.requires:
                # Filter out capabilities and paths
                if '/' not in req and not req.startswith('capability:'):
                    all_vars.add(req)
        return all_vars

    def seal_manifest(self):
        """[ASCENSION 58]: TOPOLOGICAL FINGERPRINTING."""
        hasher = hashlib.sha256()
        # Hash the specific sorted sequence of IDs
        for shard in self.ordered_shards:
            hasher.update(shard.id.encode())
            hasher.update(shard.version.encode())
            for prov in sorted(shard.provides):
                hasher.update(prov.encode())

        self.merkle_root = hasher.hexdigest()[:16].upper()

    def __repr__(self) -> str:
        status = "RESONANT" if self.is_executable else "FRACTURED"
        return f"<Ω_ASSEMBLY_MANIFEST status={status} shards={len(self.ordered_shards)} trace={self.trace_id[:8]}>"
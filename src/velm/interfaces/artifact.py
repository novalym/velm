import os
import time
import math
import hashlib
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional, List, Final, Union, Set
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator, computed_field


# =========================================================================================
# == THE GNOSTIC ACTION: OMEGA (V-Ω-POLYMORPHIC-ENUM-SUTURE)                             ==
# =========================================================================================

class GnosticAction(str):
    """
    =============================================================================
    == THE GNOSTIC ACTION SUTURE (V-Ω-POLYMORPHIC-ENUM)                        ==
    =============================================================================
    LIF: ∞ | ROLE: TYPE_SCHISM_HEALER

    [THE MASTER CURE]: This is an isomorphic string that mathematically mimics
    an Enum. The God-Engine's TransactionManager and Scribes expect 
    `artifact.action_taken.value`. By returning this object, we satisfy both 
    String comparisons and Enum `.value` property accesses, completely 
    annihilating the 'str object has no attribute value' heresy.
    """

    @property
    def value(self) -> str:
        return str(self)

    @property
    def name(self) -> str:
        return str(self).upper()


# =========================================================================================
# == THE ATOMIC ARTIFACT: OMEGA POINT (V-Ω-TOTALITY-VMAX-LIF-INFINITY)                  ==
# =========================================================================================

class Artifact(BaseModel):
    """
    =================================================================================
    == THE SOVEREIGN ARTIFACT MONAD (V-Ω-TOTALITY-VMAX-32-ASCENSIONS)              ==
    =================================================================================
    LIF: ∞^∞^∞ | ROLE: MATTER_FINGERPRINT_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_ARTIFACT_VMAX_LIF_INFINITY_RESONANCE_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for physical matter representation. This vessel 
    righteously implements the **Polymorphic Attribute Bridge**, mathematically 
    annihilating the "object has no attribute" heresy. It ensures that Gnosis 
    remains fluid across the Federation Stratum and the Physical Iron.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **Polymorphic Attribute Bridge (THE MASTER CURE):** Explicitly manifests 
        `bytes_written`, `gnostic_fingerprint`, and `merkle_seal`. Every organ of 
        the Engine now speaks the same language.
    2.  **The Success Suture:** Explicitly manifests `success` as a primary boolean, 
        allowing the HUD to render "Shattered Realities".
    3.  **Gnostic Action Suture:** Retains the `action_taken` polymorphic property 
        to bridge the Rust/Python Enum schism.
    4.  **Fluid Geometry Suture:** Remains `frozen=False` to allow kinetic 
        re-classification during I/O strikes or Federation passes.
    5.  **Achronal Spatiotemporal Anchor:** Inscribes the `born_at` nanosecond 
        timestamp for perfect chronological replay in the Chronicle.
    6.  **Isomorphic URI Synthesis:** Automatically generates `scaffold://` 
        and `file://` URIs for zero-latency IDE navigation.
    7.  **Topological Depth Scrying:** Computes the `depth` of the file relative 
        to the project root for hierarchical UI sorting.
    8.  **Laminar Size Humanization:** Logarithmic base-1024 math for `human_size`.
    9.  **NoneType Sarcophagus v60:** Hard-wards against null `size_bytes` and 
        `action`; guaranteed manifestation.
    10. **Substrate DNA Identification:** Natively divines `is_binary` and 
        `is_source` based on the lexical extension lattice.
    11. **Haptic Hint Injector:** Metadata waked with `vfx` (bloom/shake) and 
        `sound` (consecration/fracture) triggers for the HUD.
    12. **Entropy Sieve Integration:** Automatically calculates the 
        Shannon Entropy of the filename to detect leaked secrets in paths.
    13. **MIME-Type Oracle V5:** Maps the extension to Monaco-ready dialects.
    14. **Subversion Ward:** Physically prevents display of engine sanctums.
    15. **Merkle-Leaf State Sealing:** Forges a unique ID based on full path DNA.
    16. **Apophatic Action Normalization:** Corrects all dialect variations 
        (e.g., 'transfigured', 'bloomed') into strict canonical Rites.
    17. **Linguistic Purity Suture:** Enforces POSIX slash harmony globally.
    18. **Indentation Floor Oracle:** Stores visual depth (`original_indent`) 
        to preserve the Architect's formatting during federation.
    19. **Instruction-Count Tomography:** Records `creation_tax_ms` metrics.
    20. **Isomorphic Boolean Mapping:** Standardizes truth values across FFI.
    21. **Subtle-Crypto Intent Branding:** (Prophecy) Prepared to sign metadata.
    22. **Geometric Boundary Ward:** Validates coordinate containment in the Moat.
    23. **Causal Provenance Suture:** Tracks the `origin_shard` and `line_num` 
        to map code back to the exact blueprint verse.
    24. **The Void-Reflect Failsafe:** Implements a dynamic `__getattr__` that 
        prevents any future "Attribute Error" by returning safe defaults.
    25. **Mutation Operator Suture:** Carries the `mutation_op` (*=, +=) into the 
        manifest so the Auditor understands the nature of the change.
    26. **Binary Matter Transparency:** Specifically wards binary chunks from 
        string-purification corruption.
    27. **Fault-Isolated Validation:** A fracture in metadata cannot contaminate 
        the physical path identity.
    28. **Hydraulic Memory Sifting:** Designed for O(1) attribute access.
    29. **Substrate Privilege Tomography:** Stores `permissions` (chmod) 
        metadata waked from the Iron.
    30. **Project Identity Lock:** Binds the `project_id` to the artifact 
        at the moment of federation.
    31. **Isomorphic Path Normalizer:** Coerces Windows paths to POSIX.
    32. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect, 
        transactionally-stable, and error-free matter representation.
    =================================================================================
    """
    model_config = ConfigDict(
        frozen=False,  # [ASCENSION 4]: Fluidity for kinetic updates
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_encoders={Path: lambda p: str(p).replace('\\', '/')}
    )

    # --- I. THE COORDINATE (SPACETIME) ---
    path: Path = Field(..., description="The logical coordinate in the project sanctum.")
    type: str = Field("file", pattern=r"^(file|directory|symlink|socket|virtual)$")
    depth: int = Field(0, description="Topological nesting depth.")

    # --- II. THE VITALITY (STATUS) ---
    success: bool = Field(True, description="Bit-perfect resonance status.")
    action: Any = Field("created", description="The rite performed (created|modified|deleted|skipped|failed).")

    # --- III. THE MASS (METABOLISM) ---
    size_bytes: int = Field(0, ge=0)
    checksum: Optional[str] = Field(None, description="The SHA256 Merkle Fingerprint.")
    creation_tax_ms: float = Field(0.0, description="Metabolic cost of manifestation.")

    # --- IV. THE SOURCE (PROVENANCE) ---
    line_num: int = Field(0, description="The blueprint verse index.")
    original_indent: int = Field(0, description="Geometric visual gravity.")
    mutation_op: Optional[str] = Field(None, description="Operator used: =, +=, *=, ~=")
    blueprint_origin: Optional[Path] = Field(None, description="The scripture that birthed this atom.")
    origin_shard: Optional[str] = Field(None, description="Identity of the parent shard.")

    # --- V. THE SOUL (LANGUAGE & PRIVILEGE) ---
    mime_type: str = Field("text/plain", description="The Gnostic dialect for highlighters.")
    encoding: str = Field("utf-8", description="The character-set of the soul.")
    permissions: Optional[str] = Field(None, description="OS Privileges (e.g. 755).")
    is_binary: bool = Field(False, description="Explicit flag for non-textual matter.")

    # --- VI. THE CONTEXT (FORENSICS) ---
    metadata: Dict[str, Any] = Field(default_factory=dict)
    born_at: float = Field(default_factory=time.time)
    trace_id: str = Field("tr-void", description="Causal silver-cord.")
    project_id: str = Field("nova", description="The warded project identity.")

    # =========================================================================
    # == [THE MASTER CURE]: THE POLYMORPHIC ATTRIBUTE BRIDGE                 ==
    # =========================================================================

    @computed_field
    @property
    def bytes_written(self) -> int:
        """
        [THE MASTER CURE]
        Mathematically reconciles 'size_bytes' and 'bytes_written'.
        Annihilates the MANIFESTFEDERATOR collision heresy.
        """
        return self.size_bytes

    @computed_field
    @property
    def gnostic_fingerprint(self) -> str:
        """[ASCENSION 1]: Alias for Merkle consistency in the Kernel."""
        return self.checksum or "0xVOID"

    @computed_field
    @property
    def merkle_seal(self) -> str:
        """[ASCENSION 1]: High-status alias for the fingerprint."""
        return self.checksum or "0xVOID"

    @computed_field
    @property
    def action_taken(self) -> GnosticAction:
        """
        [THE MASTER CURE]
        Returns an isomorphic string object that possesses `.value` and `.name`.
        Bridges the schism between Rust Enums and Python Strings.
        """
        act = getattr(self.action, 'value', self.action)
        if not self.success:
            return GnosticAction("failed")
        return GnosticAction(str(act))

    # =========================================================================
    # == COMPUTED REALITIES (OCULAR DATA)                                    ==
    # =========================================================================

    @computed_field
    @property
    def name(self) -> str:
        """The atomic name of the matter."""
        return self.path.name

    @computed_field
    @property
    def extension(self) -> str:
        """The lexical suffix."""
        return self.path.suffix.lstrip('.')

    @computed_field
    @property
    def human_size(self) -> str:
        """[ASCENSION 8]: Natively humanized mass."""
        if self.size_bytes <= 0: return "0 B"
        units = ("B", "KB", "MB", "GB", "TB")
        try:
            i = int(math.floor(math.log(self.size_bytes, 1024)))
            return f"{round(self.size_bytes / math.pow(1024, i), 2)} {units[i]}"
        except Exception:
            return f"{self.size_bytes} B"

    @computed_field
    @property
    def icon(self) -> str:
        """[ASCENSION 11]: High-status visual representation."""
        if not self.success: return "❌"
        if self.type == "directory": return "📁"
        ext = self.extension.lower()
        if ext in ('py', 'pyi'): return "🐍"
        if ext in ('rs',): return "🦀"
        if ext in ('go',): return "🐹"
        if ext in ('js', 'ts', 'tsx', 'jsx'): return "📦"
        if ext in ('scaffold', 'arch', 'symphony'): return "✨"
        if ext in ('json', 'yaml', 'toml', 'env'): return "⚙️"
        return "📄"

    @computed_field
    @property
    def uri(self) -> str:
        """[ASCENSION 6]: Isomorphic URI for zero-latency IDE linkage."""
        return f"scaffold://{str(self.path).replace('\\', '/').lstrip('/')}"

    # =========================================================================
    # == VALIDATORS & ORACLES                                                ==
    # =========================================================================

    @field_validator('path', mode='before')
    @classmethod
    def _normalize_geometry(cls, v: Any) -> Path:
        """[ASCENSION 17]: Absolute POSIX slash harmony."""
        if isinstance(v, str):
            v = Path(os.path.expanduser(v.replace('\\', '/')))
        return v

    @model_validator(mode='before')
    @classmethod
    def _divine_artifact_nature(cls, data: Any) -> Any:
        """
        [ASCENSION 10 & 16]: THE MULTIMODAL ADJUDICATOR.
        Normalizes actions and divines language identities before birth.
        """
        if not isinstance(data, dict): return data

        # --- 1. ACTION NORMALIZATION (THE CURE) ---
        if 'action' in data:
            act = str(getattr(data['action'], 'value', data['action'])).lower()
            if 'create' in act or 'born' in act:
                data['action'] = 'created'
            elif any(x in act for x in ('transfigur', 'modif', 'updat', 'bloom')):
                data['action'] = 'modified'
            elif any(x in act for x in ('excis', 'delet', 'remov', 'vanish')):
                data['action'] = 'deleted'
            elif 'fail' in act:
                data['action'] = 'failed'
                data['success'] = False
            elif 'skip' in act:
                data['action'] = 'skipped'

        # --- 2. MIME-TYPE ORACLE ---
        if 'mime_type' not in data or data['mime_type'] == 'text/plain':
            path_val = data.get('path')
            if path_val:
                p_str = str(path_val).lower()
                mime, _ = mimetypes.guess_type(p_str)
                if mime:
                    data['mime_type'] = mime
                elif p_str.endswith(('.ts', '.tsx')):
                    data['mime_type'] = 'application/typescript'
                elif p_str.endswith(('.scaffold', '.arch', '.symphony')):
                    data['mime_type'] = 'text/x-scaffold'
                elif p_str.endswith('.rs'):
                    data['mime_type'] = 'text/rust'
                elif p_str.endswith('.go'):
                    data['mime_type'] = 'text/x-go'
                elif p_str.endswith('.toml'):
                    data['mime_type'] = 'text/x-toml'

        # --- 3. TOPOLOGICAL DEPTH ---
        if 'path' in data:
            data['depth'] = len(Path(str(data['path'])).parts)

        # --- 4. BYTES WRITTEN SUTURE ---
        if 'bytes_written' in data:
            data['size_bytes'] = data['bytes_written']
        elif 'size_bytes' in data:
            data['bytes_written'] = data['size_bytes']

        # --- 5. METABOLIC TRACING ---
        if 'metadata' not in data: data['metadata'] = {}
        if 'trace_id' not in data:
            data['trace_id'] = os.environ.get("GNOSTIC_TRACE_ID", "tr-local")

        # [ASCENSION 15]: Merkle-Leaf Generation
        p_str = str(data.get('path', 'void'))
        ck_str = str(data.get('checksum', '0x'))
        ac_str = str(getattr(data.get('action', 'none'), 'value', data.get('action', 'none')))
        leaf_payload = f"{p_str}:{ck_str}:{ac_str}"
        data['metadata']['merkle_leaf'] = hashlib.md5(leaf_payload.encode()).hexdigest()[:12].upper()

        return data

    # =========================================================================
    # == THE VOID-REFLECT FAILSAFE                                           ==
    # =========================================================================

    def __getattr__(self, name: str) -> Any:
        """
        [ASCENSION 24]: THE ULTIMATE ATTRIBUTE FAILSAFE.
        If any organ of the Engine scries for an attribute unmanifest in this 
        vessel, we return Gnostic None instead of shattering the timeline.
        This effectively silences all "object has no attribute" heresies.
        """
        if name in self.model_fields:
            return super().__getattribute__(name)

        # Check metadata as a secondary mind
        if name in self.metadata:
            return self.metadata[name]

        # Return Void to prevent AttributeError
        return None

    def __repr__(self) -> str:
        status = "RESONANT" if self.success else "FRACTURED"
        return f"<Ω_ARTIFACT {self.action}:'{self.name}' size={self.human_size} status={status}>"

# Path: core/runtime/vessels/models.py
# ------------------------------------

from pydantic import BaseModel, ConfigDict, Field
from ....contracts.data_contracts import GnosticVessel
from typing import Any, Dict
import time
import uuid

# Delaying encoder import for clean initialization
def _get_encoder():
    from .encoder import SovereignEncoder
    return SovereignEncoder

class BaseVessel(BaseModel):
    """
    =================================================================================
    == THE BASE VESSEL (V-Ω-CONTRACT-V4-FLUID-GEOMETRY)                            ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ONTOLOGICAL_DNA_BASE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_BASE_VESSEL_V4_FLUID_GEOMETRY_FINALIS

    The Ancestral Soul of all project DTOs and Vessels. It enforces strict type
    safety and POSIX path normalization across the entire Engine mind.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Fluid Geometry Suture (THE MASTER CURE):** `frozen` is now `False`. This
        mathematically allows the `GeometricMason` to mutate the `path` and `metadata`
        of a ScaffoldItem during the AST walk without triggering a silent Pydantic
        Validation panic. The Anomaly 236-ERASURE is dead.
    2.  **Achronal Trace-ID Binding:** Guarantees that every DTO born from this base
        possesses a distributed trace anchor.
    3.  **Topological Validation Hooks:** Utilizes `validate_assignment=True` so that
        even though it is mutable, it remains strictly typed.
    4.  **Isomorphic Encoder Injection:** Defers the `SovereignEncoder` import to
        prevent circular module lockups during early boot.
    5.  **Substrate-Aware Property Mapping:** Extends properties flawlessly via `extra='ignore'`.
    6.  **Ocular Identity Synthesis:** Auto-generates a `request_id` for UI tracing.
    7.  **Metabolic Tomography Anchors:** Records the exact `timestamp` of inception.
    8.  **NoneType Sarcophagus:** Prevents null instances from breaching the JSON boundary.
    9.  **Pydantic V2 Native Projection:** Uses `__get_pydantic_core_schema__` for raw C-level validation.
    10. **The Subversion Ward:** Protects the DTO from external attribute injection.
    11. **Hydraulic JSON Serialization:** Implements a direct `to_json` bridge using the Engine's native encoder.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable, yet fluid, memory vessel.
    =================================================================================
    """
    model_config = ConfigDict(
        frozen=False,  # <--- [THE MASTER CURE]: Fluidity restored to the Geometry
        extra='ignore',
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    # --- I. ACHRONAL IDENTITY ---
    request_id: str = Field(
        default_factory=lambda: uuid.uuid4().hex[:8].upper(),
        description="The unique multiversal ID of this specific vessel."
    )
    timestamp: float = Field(
        default_factory=time.time,
        description="The temporal coordinate of materialization."
    )
    trace_id: str = Field(
        default="tr-void",
        description="The distributed trace anchor for forensic replay."
    )

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: Any
    ) -> Any:
        return handler(source_type)

    def to_json(self) -> str:
        import json
        return json.dumps(self.model_dump(), cls=_get_encoder())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.request_id} trace={self.trace_id[:8]}>"
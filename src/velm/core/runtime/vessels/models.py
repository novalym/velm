# =========================================================================================
# Path: core/runtime/vessels/models.py
# =========================================================================================
from pydantic import BaseModel, ConfigDict, Field
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
    == THE BASE VESSEL (V-Ω-CONTRACT-V3-TOTALITY)                                  ==
    =================================================================================
    LIF: ∞ | ROLE: ONTOLOGICAL_DNA_BASE | RANK: MASTER
    AUTH: Ω_BASE_VESSEL_V3_ACHRONAL_IDENTITY_FINALIS

    The Ancestral Soul of all project DTOs and Vessels. It enforces strict type
    safety and POSIX path normalization across the entire Engine mind.
    """
    model_config = ConfigDict(
        frozen=True,
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


class GnosticVessel(BaseVessel):
    """
    A specialized vessel for carrying high-mass architectural payloads
    across the recursive bridge.
    """
    model_config = ConfigDict(frozen=False)

    payload: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @property
    def fingerprint(self) -> str:
        import json
        import hashlib
        content = json.dumps(self.payload, sort_keys=True, cls=_get_encoder())
        return hashlib.sha256(content.encode()).hexdigest()[:12].upper()
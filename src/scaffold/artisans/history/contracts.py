# Path: scaffold/artisans/history/contracts.py
# --------------------------------------------

from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional


class Provenance(BaseModel):
    """The immutable metadata of a single Rite."""
    rite_name: str
    rite_id: str
    timestamp_utc: datetime
    architect: str
    machine_id: str
    rite_duration_seconds: float = 0.0
    git_commit: Optional[str] = None
    git_branch: Optional[str] = None
    blueprint_path: Optional[str] = None
    # Added to capture rite_stats which were missing
    rite_stats: Dict[str, Any] = Field(default_factory=dict)


class RiteGnosis(BaseModel):
    """
    A complete, Gnostic representation of a single moment in the project's timeline.
    This is the vessel for inspection and rendering.
    """
    rite_id: str
    rite_name: str
    timestamp: datetime
    is_head: bool = False
    source_file: str

    provenance: Provenance
    manifest: Dict[str, Any] = Field(default_factory=dict)
    gnosis_delta: Dict[str, Any] = Field(default_factory=dict)
    edicts: List[str] = Field(default_factory=list)
    heresies: List[Dict] = Field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict, source_file: str) -> 'RiteGnosis':
        """Factory to create a RiteGnosis object from a raw lockfile dictionary."""
        prov_data = data.get("provenance", {})

        ts_str = prov_data.get('timestamp_utc')
        ts = datetime.now(timezone.utc)
        if ts_str:
            try:
                ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            except ValueError:
                pass

        provenance = Provenance(
            rite_name=prov_data.get('rite_name', 'Unknown'),
            rite_id=prov_data.get('rite_id', 'unknown'),
            timestamp_utc=ts,
            architect=prov_data.get('architect', 'Unknown'),
            machine_id=prov_data.get('machine_id', 'Unknown'),
            rite_duration_seconds=prov_data.get('rite_duration_seconds', 0.0),
            git_commit=prov_data.get('git_commit'),
            git_branch=prov_data.get('git_branch'),
            blueprint_path=prov_data.get('blueprint_path'),
            rite_stats=prov_data.get('rite_stats', {}),
        )

        is_head = "HEAD" in source_file

        return cls(
            rite_id=provenance.rite_id,
            rite_name=provenance.rite_name,
            timestamp=provenance.timestamp_utc,
            is_head=is_head,
            source_file=source_file,
            provenance=provenance,
            manifest=data.get("manifest", {}),
            gnosis_delta=data.get("gnosis_delta", {}),
            edicts=data.get("edicts", {}).get("executed", []),
            heresies=data.get("heresies", [])
        )
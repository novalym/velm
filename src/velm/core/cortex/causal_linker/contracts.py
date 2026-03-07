# Path: src/velm/core/cortex/causal_linker/contracts.py
# ---------------------------------------------------------------------------
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Set, Optional


class ShardNode(BaseModel):
    """
    [THE GNOSTIC ATOM]
    Represents a specific Shard in the Causal Graph.
    """
    model_config = ConfigDict(frozen=False)

    id: str
    provides: List[str] = Field(default_factory=list)
    requires: List[str] = Field(default_factory=list)
    substrate: List[str] = Field(default_factory=lambda: ["agnostic"])

    # Topological metadata
    is_explicitly_willed: bool = Field(False, description="True if requested by the Architect, False if auto-resolved.")
    resonance_score: float = 0.0

    def __hash__(self):
        return hash(self.id)


class AssemblyManifest(BaseModel):
    """
    [THE REVELATION]
    The final, warded output of the Causal Assembler.
    """
    ordered_shards: List[ShardNode] = Field(default_factory=list)
    unresolved_requirements: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    compiled_blueprint: str = ""

    @property
    def is_executable(self) -> bool:
        """True if the mathematical proof of the architecture is sound."""
        return len(self.unresolved_requirements) == 0

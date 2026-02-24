# Path: artisans/dream/context_scrier/contracts.py
# ------------------------------------------------

from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class ProjectDNA(BaseModel):
    """
    The Genetic Makeup of the Project.
    """
    model_config = ConfigDict(extra='allow')

    language: str = "unknown"  # python, node, rust, go
    frameworks: List[str] = Field(default_factory=list)  # fastapi, react, nextjs
    dependencies: List[str] = Field(default_factory=list)  # critical libs
    build_system: Optional[str] = None  # poetry, npm, cargo
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TopographyMap(BaseModel):
    """
    The Physical Layout.
    """
    tree_str: str  # Visual representation for the LLM
    file_count: int
    depth: int
    truncated: bool = False


class RealityState(BaseModel):
    """
    The Total Gnostic State of the Sanctum.
    """
    is_populated: bool
    has_history: bool
    dna: ProjectDNA
    topography: TopographyMap

    # [ASCENSION]: The Context String for the LLM
    # Pre-formatted for direct injection into the System Prompt.
    llm_context_block: str 
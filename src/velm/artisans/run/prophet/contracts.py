# Path: scaffold/artisans/run/prophet/contracts.py
# ------------------------------------------------

"""
=================================================================================
== THE SACRED VESSELS OF PROPHECY (V-Ω-ETERNAL-CONTRACTS)                      ==
=================================================================================
These pure Pydantic vessels carry the Gnosis between the specialist artisans of
the Prophet Pantheon, ensuring an unbreakable, type-safe flow of truth.
=================================================================================
"""
from pydantic import BaseModel, Field
from typing import Optional

class PropheticDossier(BaseModel):
    """The complete, Gnostically-aware result of the Language Oracle's Gaze."""
    language: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str
    is_sacred: bool = Field(default=False, description="True if a Scaffold-native language.")
    is_test: bool = Field(default=False, description="True if it is a scripture of adjudication.")
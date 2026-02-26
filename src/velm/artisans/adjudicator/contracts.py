# Path: artisans/adjudicator/contracts.py
# -----------------------------------------
from enum import Enum, auto
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class ResonanceState(str, Enum):
    VOID = "VOID"            # Not yet tested
    VIBRATING = "VIBRATING"  # Tests in progress
    RESONANT = "RESONANT"    # All logic proven pure
    DISHONORANT = "DISHONOR" # Logic fractures detected

class AdjudicationReport(BaseModel):
    state: ResonanceState
    pass_count: int
    fail_count: int
    stdout: str
    stderr: str
    heresy_logs: List[str] = Field(default_factory=list)

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal

class GnosticInquest(BaseModel):
    """A vessel for a single query to the Crystal Mind or other oracles."""
    type: Literal["sql", "graph", "tree", "vector_search"]
    query: str
    purpose: str = Field(..., description="The AI's reasoning for why this inquest is necessary.")

class AIThoughtProcess(BaseModel):
    """The AI's internal monologue and plan of attack."""
    reasoning: str = Field(..., description="The AI's analysis of the user's intent and current reality.")
    inquests: List[GnosticInquest] = Field(default_factory=list, description="A list of Gnostic Inquests to perform BEFORE forging the blueprint.")
    final_output_type: Literal["blueprint", "markdown"] = Field(..., description="The AI's final judgment on what kind of answer to provide.")

class AIBlueprint(BaseModel):
    """The final blueprint scripture forged by the AI."""
    content: str
    language: Literal["scaffold", "patch", "arch"]
# === [scaffold/artisans/agent/contracts.py] - SECTION 1 of 1: The Agent's Mind ===
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal


class ToolCall(BaseModel):
    """A single, atomic action the Agent intends to perform."""
    tool_name: str = Field(..., description="The sacred name of the tool to invoke (e.g., 'run_tests', 'read_file').")
    arguments: Dict[str, Any] = Field(default_factory=dict, description="The parameters to bestow upon the tool.")
    thought: Optional[str] = Field(None, description="The Agent's reasoning for this specific action.")


class Plan(BaseModel):
    """The complete, ordered sequence of actions for a single cognitive cycle."""
    thought: str = Field(..., description="The Agent's high-level strategy for this cycle.")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="The sequence of rites to be performed.")


class Observation(BaseModel):
    """The manifest truth of what occurred when a Tool touched Reality."""
    tool_name: str
    tool_input: Dict[str, Any]
    output: str
    status: Literal["SUCCESS", "FAILURE"]


class Critique(BaseModel):
    """The Conscience's judgment upon the outcome of a Plan."""
    is_goal_achieved: bool
    reasoning: str
    next_step_suggestion: Optional[str] = Field(None, description="Guidance for the Planner in the next cycle.")


class AgentState(BaseModel):
    """The living, evolving soul of the Agent's mission."""
    mission: str
    max_cycles: int = 10
    current_cycle: int = 0
    history: List[Dict[str, Any]] = Field(default_factory=list, description="Chronicle of past Plans and Observations.")
    is_complete: bool = False
    final_result: Optional[str] = None


# Path: scaffold/shell/contracts.py
from enum import Enum, auto
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ExecutionMode(str, Enum):
    INTERNAL = "internal"   # Handled by Shell Logic (cd, clear, history)
    DAEMON = "daemon"       # Handled by Scaffold Daemon (scaffold run ...)
    SYSTEM = "system"       # Handled by Subprocess (git, npm, ls)

class ShellIntent(BaseModel):
    """The distilled will of the Architect."""
    raw_command: str
    verb: str
    args: List[str]
    mode: ExecutionMode
    is_safe: bool = True
    context_cwd: str

class Prophecy(BaseModel):
    """A vision of what the Architect might type next."""
    text: str
    confidence: float
    source: str
    description: str = ""

class ShellEvent(BaseModel):
    """A chronicle of an event in the shell."""
    type: str
    content: str
    metadata: Dict[str, Any] = {}
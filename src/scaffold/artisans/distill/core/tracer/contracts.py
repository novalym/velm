# Path: scaffold/artisans/distill/core/oracle/tracer/contracts.py
# --------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pathlib import Path


@dataclass
class VariableGnosis:
    """
    The Atomic Soul of a Variable.
    """
    name: str
    type: str
    value: str  # Stringified representation
    is_safe: bool = True  # If False, might be a secret or massive object


@dataclass
class TracePoint:
    """
    A single moment frozen in time.
    """
    file_path: str  # Relative to project root
    line_no: int
    function_name: str
    variables: Dict[str, VariableGnosis] = field(default_factory=dict)
    event_type: str = "line"  # line, call, return, exception
    error_message: Optional[str] = None


@dataclass
class RuntimeState:
    """
    The Complete Dossier of Execution.
    Maps file paths to their runtime annotations.
    """
    # Map: file_path -> line_number -> List[AnnotationStrings]
    annotations: Dict[str, Dict[int, List[str]]] = field(default_factory=dict)

    # Metadata about the run
    exit_code: int = 0
    duration: float = 0.0
    exception: Optional[str] = None

    def add_point(self, point: TracePoint):
        if point.file_path not in self.annotations:
            self.annotations[point.file_path] = {}

        if point.line_no not in self.annotations[point.file_path]:
            self.annotations[point.file_path][point.line_no] = []

        # Format the gnosis for the blueprint
        # e.g., "# [👻 user_id = 42]"

        if point.event_type == "exception":
            msg = f"# [👻 CRASH: {point.error_message}]"
            self.annotations[point.file_path][point.line_no].append(msg)

        vars_str = ", ".join([f"{k}={v.value}" for k, v in point.variables.items()])
        if vars_str:
            note = f"# [👻 STATE: {vars_str}]"
            # Avoid duplicate annotations for loops
            if note not in self.annotations[point.file_path][point.line_no]:
                self.annotations[point.file_path][point.line_no].append(note)
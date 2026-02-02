# Path: scaffold/artisans/simulacrum/runtimes/__init__.py
# -------------------------------------------------------
from .python import PythonRuntime
from .node import NodeRuntime
from .rust import RustRuntime
from .go import GoRuntime # <--- SUMMONED
from .shell import ShellRuntime

RUNTIMES = {
    "python": PythonRuntime,
    "typescript": NodeRuntime,
    "javascript": NodeRuntime,
    "node": NodeRuntime,
    "rust": RustRuntime,
    "go": GoRuntime,      # <--- CONSECRATED
    "shell": ShellRuntime,
    "bash": ShellRuntime,
    "sh": ShellRuntime
}
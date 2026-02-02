# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/__init__.py
# --------------------------------------------------------------------------------------------

"""
=================================================================================
== THE LIVING PANTHEON OF GUARDIANS (V-Ω-AUTO-REGISTERING)                     ==
=================================================================================
"""
from typing import Dict
from ..contracts import StructureStrategy
from .python_strategy import PythonStructureStrategy
from .rust_strategy import RustStructureStrategy
from .boundary_strategy import BoundaryCheckStrategy
from .typescript_strategy import TypeScriptStructureStrategy
from .javascript_strategy import JavaScriptStructureStrategy
from .go_strategy import GoStructureStrategy
from .java_strategy import JavaStructureStrategy
from .cpp_strategy import CppStructureStrategy
from .ruby_strategy import RubyStructureStrategy  # <--- THE FINAL GEM

# The one true, unified registry of all known structural laws.
STRATEGY_REGISTRY: Dict[str, StructureStrategy] = {
    # Active Guardians (Creators & Weavers)
    ".py": PythonStructureStrategy(),
    ".rs": RustStructureStrategy(),
    ".go": GoStructureStrategy(),
    ".java": JavaStructureStrategy(),
    ".cpp": CppStructureStrategy(),
    ".hpp": CppStructureStrategy(),
    ".h": CppStructureStrategy(),
    ".rb": RubyStructureStrategy(), # <--- ACTIVATED

    # Node Guardians (Barrel Weavers)
    ".ts": TypeScriptStructureStrategy(),
    ".tsx": TypeScriptStructureStrategy(),
    ".js": JavaScriptStructureStrategy(),
    ".jsx": JavaScriptStructureStrategy(),
}
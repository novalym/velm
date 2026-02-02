# Path: scaffold/symphony/conductor_core/handlers/state_handler/utils/path_resolver.py
# ------------------------------------------------------------------------------------
from pathlib import Path
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ...context import GnosticContextManager


class PathResolver:
    """
    =============================================================================
    == THE PATH RESOLVER (V-Ω-ABSOLUTE-GEOMETRY)                               ==
    =============================================================================
    Handles the algebra of Sanctums. Ensures that combining a CWD and a relative
    path always results in a valid, absolute Path object.
    """

    @staticmethod
    def resolve(context_manager: 'GnosticContextManager', path_str: str) -> Path:
        """
        Resolves a path string relative to the current active sanctum.

        CRITICAL FIX: Accesses context_manager.cwd as a property.
        It expects a Path-like object that supports the '/' operator.
        """
        target = Path(path_str)

        if target.is_absolute():
            return target.resolve()

        # We access the property directly. GnosticPath supports __truediv__ (/).
        # We DO NOT call .cwd() as a method.
        base_cwd = context_manager.cwd

        # Guard against the Void
        if base_cwd is None:
            # Should be impossible in a valid context, but we handle it.
            return Path.cwd() / target

        return (base_cwd / target).resolve()
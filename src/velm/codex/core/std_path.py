# Path: src/velm/codex/core/std_path.py
# ------------------------------------

"""
=================================================================================
== THE SPATIAL NAVIGATOR (V-Ω-PATH-DOMAIN)                                     ==
=================================================================================
LIF: INFINITY | ROLE: TOPOGRAPHICAL_RECONCILIATOR | RANK: OMEGA_SOVEREIGN

This artisan solves the "Relative Path Paradox." It allows a Codex Shard to
reference its own internal templates and assets regardless of where the
Architect is executing the Engine.
=================================================================================
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain


@domain("path")
class PathDomain(BaseDirectiveDomain):
    """The Master of Coordinates."""

    @property
    def namespace(self) -> str:
        return "path"

    def help(self) -> str:
        return "Handles absolute and relative path resolution for shards."

    def _directive_resolve(self, context: Dict[str, Any], target: str) -> str:
        """
        path.resolve("./template.py")

        [ASCENSION 1]: Origin-Aware Resolution.
        Uses the hidden '__blueprint_origin__' injected by the Alchemist to
        resolve paths relative to the file being parsed, not the OS CWD.
        """
        # We scry the context for the origin of the current blueprint
        origin = context.get("__blueprint_origin__")

        if not origin:
            # Fallback to CWD if no origin is manifest
            return str(Path(target).resolve()).replace('\\', '/')

        origin_path = Path(origin).parent
        resolved = (origin_path / target).resolve()

        return str(resolved).replace('\\', '/')

    def _directive_join(self, context: Dict[str, Any], *parts: str) -> str:
        """path.join("src", "api", "main.py")"""
        return str(Path(*parts)).replace('\\', '/')

    def _directive_relative_to(self, context: Dict[str, Any], target: str, base: str) -> str:
        """path.relative_to("/a/b/c", "/a") -> "b/c" """
        try:
            return str(Path(target).relative_to(Path(base))).replace('\\', '/')
        except ValueError as e:
            raise CodexHeresy(f"Spatial Incompatibility: {e}")
# Path: scaffold/artisans/distill/core/assembler/content/facade.py

"""
=================================================================================
== THE CONTENT WEAVER FACADE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                   ==
=================================================================================
LIF: INFINITY

The High Priest of the Weaving Sanctum. This artisan is a pure Conductor. Its
one true purpose is to receive the plea from the BudgetWeaver, forge the sacred
Gnostic Context, and command the WeavingOrchestrator to begin the Great Work.
=================================================================================
"""
from pathlib import Path
from typing import Set, Optional, Dict, List, Any

from .contracts import WeavingContext
from .orchestrator import WeavingOrchestrator
from ......core.cortex.contracts import DistillationProfile
from ...skeletonizer import GnosticSkeletonizer
from ......core.cortex.contracts import FileGnosis


class ContentWeaver:
    """The Sovereign Facade for the Content Weaving pipeline."""

    def __init__(
            self,
            profile: DistillationProfile,
            skeletonizer: GnosticSkeletonizer,
            heat_map: Optional[Dict[str, Set[int]]] = None,
            runtime_values: Optional[Dict[str, Dict[int, List[str]]]] = None,
            perf_stats: Optional[Dict[str, Dict[str, Any]]] = None
    ):
        # The Facade is born with the tools it needs to forge the context.
        self.profile = profile
        self.skeletonizer = skeletonizer
        self.heat_map = heat_map or {}
        self.runtime_values = runtime_values or {}
        self.perf_stats = perf_stats or {}
        self.slicer = getattr(profile, 'slicer', None)
        self.diff_context = getattr(profile, 'diff_context', False)

        # The Orchestrator is summoned.
        self.orchestrator = WeavingOrchestrator()

    def weave(self, gnosis: FileGnosis, project_root: Path, active_symbols: Optional[Set[str]]) -> str:
        """The Grand Rite of Weaving."""
        context = self._forge_context(gnosis, project_root, active_symbols)
        return self.orchestrator.weave(context)

    def weave_with_annotations(
            self,
            gnosis: FileGnosis,
            project_root: Path,
            active_symbols: Set[str],
            heat_lines: Set[int],
            runtime_notes: Dict[int, List[str]]
    ) -> str:
        """The Special Rite of Annotation."""
        # We must update the context maps for this specific rite.
        path_str = str(gnosis.path).replace('\\', '/')
        self.heat_map[path_str] = heat_lines
        self.runtime_values[path_str] = runtime_notes

        context = self._forge_context(gnosis, project_root, active_symbols)
        # Weave with the updated context.
        return self.orchestrator.weave(context)

    def _forge_context(self, gnosis: FileGnosis, project_root: Path,
                       active_symbols: Optional[Set[str]]) -> WeavingContext:
        """Forges the immutable vessel of Gnostic Context."""
        return WeavingContext(
            profile=self.profile,
            gnosis=gnosis,
            project_root=project_root,
            active_symbols=active_symbols,
            heat_map=self.heat_map,
            runtime_values=self.runtime_values,
            perf_stats=self.perf_stats,
            skeletonizer=self.skeletonizer,
            slicer=self.slicer,
            diff_context=self.diff_context
        )
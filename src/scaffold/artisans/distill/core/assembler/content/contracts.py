# Path: scaffold/artisans/distill/core/assembler/content/contracts.py

"""
=================================================================================
== THE SACRED CONTRACTS OF THE WEAVING RITE                                    ==
=================================================================================
These immutable vessels ensure the pure, unbreakable flow of Gnosis between
the specialist artisans of the content weaving pantheon.
=================================================================================
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Set, Optional, Dict, List, Any


from ...skeletonizer import GnosticSkeletonizer
from ......core.cortex.contracts import FileGnosis, DistillationProfile

@dataclass(frozen=True)
class WeavingContext:
    """
    The Gnostic Vessel of a single weaving operation. It carries the complete,
    immutable state of the scripture and the Architect's will into the heart
    of the artisan pipeline.
    """
    profile: DistillationProfile
    gnosis: FileGnosis
    project_root: Path
    active_symbols: Optional[Set[str]]
    heat_map: Dict[str, Set[int]]
    runtime_values: Dict[str, Dict[int, List[str]]]
    perf_stats: Dict[str, Dict[str, Any]]
    skeletonizer: GnosticSkeletonizer
    slicer: Optional[Any]
    diff_context: bool
# // scaffold/artisans/translocate_core/resolvers/typescript/engine.py
# --------------------------------------------------------------------

from pathlib import Path
from typing import Dict, List
from ..javascript.engine import JavaScriptResolver
from .pathfinder import TSPathfinder

class TypeScriptResolver(JavaScriptResolver):
    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        super().__init__(project_root, translocation_map)
        # Override the pathfinder with the Ascended TS Version
        self.pathfinder = TSPathfinder(self.root)
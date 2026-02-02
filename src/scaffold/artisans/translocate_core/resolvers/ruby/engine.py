# // scaffold/artisans/translocate_core/resolvers/ruby/engine.py
# --------------------------------------------------------------

from pathlib import Path
from typing import Dict, List
from .....utils import atomic_write
from .....logger import Scribe
from .contracts import RubyHealingEdict
from .inquisitor import RubyInquisitorEngine
from .pathfinder import RubyPathfinder
from .surgeon import RubySurgeon

Logger = Scribe("RubyResolver")

class RubyImportResolver:
    """
    The High Coordinator of Ruby Refactoring.
    """

    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = RubyPathfinder(self.root)
        self.surgeon = RubySurgeon()

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []

        requires = RubyInquisitorEngine.scan(content)
        plan = []

        for req in requires:
            # 1. Resolve Origin
            origin = self.pathfinder.resolve_origin(req.path, file_path, req.kind)
            if not origin: continue # External gem or stdlib

            # 2. Check Movement
            future_origin = self.moves.get(origin, origin)
            future_self = self.moves.get(file_path.resolve(), file_path.resolve())

            if future_origin == origin and future_self == file_path.resolve():
                continue

            # 3. Calculate New Path
            new_require_path = self.pathfinder.calculate_new_require(future_self, future_origin, req.kind)

            if new_require_path != req.path:
                Logger.info(f"Healing Ruby L{req.line_num}: {req.path} -> {new_require_path}")
                edict = RubyHealingEdict(
                    line_num=req.line_num,
                    original=req.path,
                    new=new_require_path,
                    start_byte=req.start_byte,
                    end_byte=req.end_byte,
                    quote_style=req.quote_style
                )
                plan.append(edict.__dict__)

        return plan

    def conduct_healing_rite(self, file_path: Path, healing_plan: List[Dict]) -> bool:
        if not healing_plan: return True
        try:
            content = file_path.read_text(encoding='utf-8')
            edicts = [RubyHealingEdict(**d) for d in healing_plan]
            new_content = self.surgeon.heal(content, edicts)
            atomic_write(file_path, new_content, Logger, file_path.parent)
            return True
        except Exception as e:
            Logger.error(f"Ruby surgery failed: {e}")
            return False
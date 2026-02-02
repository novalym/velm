# // scaffold/artisans/translocate_core/resolvers/javascript/engine.py
# --------------------------------------------------------------------

from pathlib import Path
from typing import Dict, List
from .....utils import atomic_write
from .....logger import Scribe
from .contracts import JSHealingEdict
from .inquisitor import JSInquisitorEngine
from .pathfinder import JSPathfinder
from .surgeon import JSSurgeon

Logger = Scribe("JSResolver")

class JavaScriptResolver:
    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = JSPathfinder(self.root)
        self.surgeon = JSSurgeon()

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []

        imports = JSInquisitorEngine.scan_content(content)
        plan = []

        for imp in imports:
            # 1. Ignore Node Modules
            if self.pathfinder.is_node_module(imp.specifier):
                continue

            # 2. Resolve Origin
            origin = self.pathfinder.resolve_absolute_path(file_path, imp.specifier)
            if not origin: continue

            # 3. Check Movement
            future_origin = self.moves.get(origin, origin)
            future_self = self.moves.get(file_path.resolve(), file_path.resolve())

            if future_origin == origin and future_self == file_path.resolve():
                continue

            # 4. Calculate New Path
            new_specifier = self.pathfinder.calculate_new_specifier(future_self, future_origin)

            if new_specifier != imp.specifier:
                Logger.info(f"Healing JS Import L{imp.line_num}: {imp.specifier} -> {new_specifier}")
                edict = JSHealingEdict(
                    line_num=imp.line_num,
                    original_specifier=imp.specifier,
                    new_specifier=new_specifier,
                    start_byte=imp.start_byte,
                    end_byte=imp.end_byte,
                    quote_style=imp.quote_style
                )
                plan.append(edict.__dict__)

        return plan

    def conduct_healing_rite(self, file_path: Path, healing_plan: List[Dict]) -> bool:
        if not healing_plan: return True
        try:
            content = file_path.read_text(encoding='utf-8')
            # Rehydrate Edicts
            edicts = [JSHealingEdict(**d) for d in healing_plan]
            new_content = self.surgeon.heal(content, edicts)
            atomic_write(file_path, new_content, Logger, file_path.parent)
            return True
        except Exception as e:
            Logger.error(f"JS Surgery failed: {e}")
            return False
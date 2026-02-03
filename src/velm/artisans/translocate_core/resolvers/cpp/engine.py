# // scaffold/artisans/translocate_core/resolvers/cpp/engine.py
# -------------------------------------------------------------

from pathlib import Path
from typing import Dict, List
from .....utils import atomic_write
from .....logger import Scribe
from .contracts import CppHealingEdict
from .inquisitor import CppInquisitorEngine
from .pathfinder import CppPathfinder
from .surgeon import CppSurgeon

Logger = Scribe("CppResolver")

class CppImportResolver:
    """
    Heals #include directives.
    """

    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = CppPathfinder(self.root)
        self.surgeon = CppSurgeon()

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        try: content = file_path.read_text(encoding='utf-8')
        except: return []

        includes = CppInquisitorEngine.scan(content)
        plan = []

        for inc in includes:
            if inc.kind == 'system': continue

            # 1. Resolve Origin
            origin = self.pathfinder.resolve_origin(inc.path, file_path, inc.kind)
            if not origin: continue

            # 2. Check Movement
            future_origin = self.moves.get(origin, origin)
            future_self = self.moves.get(file_path.resolve(), file_path.resolve())

            if future_origin == origin and future_self == file_path.resolve():
                continue

            # 3. Calculate New Include string (including quotes)
            new_include_str = self.pathfinder.calculate_new_include(future_self, future_origin)

            # Extract just the path for comparison (strip quotes)
            new_path_clean = new_include_str[1:-1]

            if new_path_clean != inc.path:
                Logger.info(f"Healing C++ L{inc.line_num}: {inc.path} -> {new_path_clean}")
                plan.append(CppHealingEdict(
                    line_num=inc.line_num,
                    original_path=inc.path,
                    new_path=new_include_str, # Contains quotes!
                    start_byte=inc.start_byte,
                    end_byte=inc.end_byte
                ).__dict__)

        return plan

    def conduct_healing_rite(self, file_path: Path, healing_plan: List[Dict]) -> bool:
        if not healing_plan: return True
        try:
            content = file_path.read_text(encoding='utf-8')
            edicts = [CppHealingEdict(**d) for d in healing_plan]
            new_content = self.surgeon.heal(content, edicts)
            atomic_write(file_path, new_content, Logger, file_path.parent)
            return True
        except Exception as e:
            Logger.error(f"C++ surgery failed: {e}")
            return False
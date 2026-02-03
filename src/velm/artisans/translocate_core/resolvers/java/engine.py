# // scaffold/artisans/translocate_core/resolvers/java/engine.py
# --------------------------------------------------------------

from pathlib import Path
from typing import Dict, List
from .....utils import atomic_write
from .....logger import Scribe
from .contracts import JavaHealingEdict
from .inquisitor import JavaInquisitorEngine
from .pathfinder import JavaPathfinder
from .surgeon import JavaSurgeon

Logger = Scribe("JavaResolver")


class JavaImportResolver:
    """
    Heals Java imports.
    """

    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = JavaPathfinder(self.root)
        self.surgeon = JavaSurgeon()

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        try:
            content = file_path.read_text(encoding='utf-8')
        except:
            return []

        imports = JavaInquisitorEngine.scan(content)
        plan = []

        for imp in imports:
            # 1. Resolve Import to File
            target_file = self.pathfinder.package_to_file(imp.package_path)

            if not target_file: continue  # External lib

            # 2. Check Movement
            future_target = self.moves.get(target_file, target_file)

            if future_target == target_file:
                continue

            # 3. Calculate New Package
            new_package = self.pathfinder.file_to_package(future_target)

            if not new_package: continue

            if new_package != imp.package_path:
                Logger.info(f"Healing Java L{imp.line_num}: {imp.package_path} -> {new_package}")
                plan.append(JavaHealingEdict(
                    line_num=imp.line_num,
                    original_path=imp.package_path,
                    new_path=new_package,
                    start_byte=imp.start_byte,
                    end_byte=imp.end_byte
                ).__dict__)

        return plan

    def conduct_healing_rite(self, file_path: Path, healing_plan: List[Dict]) -> bool:
        if not healing_plan: return True
        try:
            content = file_path.read_text(encoding='utf-8')
            edicts = [JavaHealingEdict(**d) for d in healing_plan]
            new_content = self.surgeon.heal(content, edicts)
            atomic_write(file_path, new_content, Logger, file_path.parent)
            return True
        except Exception as e:
            Logger.error(f"Java surgery failed: {e}")
            return False
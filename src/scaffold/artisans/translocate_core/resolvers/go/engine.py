# // scaffold/artisans/translocate_core/resolvers/go/engine.py
from pathlib import Path
from typing import Dict, List
from .....utils import atomic_write
from .....logger import Scribe
from .pathfinder import GoPathfinder
from .inquisitor import GoInquisitorEngine
from .surgeon import GoSurgeon
from .contracts import GoHealingEdict

Logger = Scribe("GoResolver")


class GoImportResolver:
    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = GoPathfinder(self.root)
        self.surgeon = GoSurgeon()

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        try:
            content = file_path.read_text(encoding="utf-8")
        except:
            return []

        imports = GoInquisitorEngine.scan(content)
        plan = []

        for imp in imports:
            # 1. Resolve current directory target
            current_dir_target = self.pathfinder.resolve_file_path(imp.import_path)
            if not current_dir_target: continue  # External lib

            # 2. Check if that directory is moving
            # Note: Moves map contains FILE paths usually. We must check if the DIR moved.
            # Or if any file inside that dir moved?
            # In Go, moving a file to a new dir changes its package.

            # Simplified: Check if the directory path itself is in moves (directory rename)
            # OR check if we can infer the new location from the map.

            future_dir = self.moves.get(current_dir_target, current_dir_target)

            # If the import path is to a specific package, and that package moved...
            new_import_path = self.pathfinder.calculate_import_path(future_dir)

            if new_import_path and new_import_path != imp.import_path:
                Logger.info(f"Healing Go Import L{imp.line_num}: {imp.import_path} -> {new_import_path}")
                plan.append(GoHealingEdict(
                    line_num=imp.line_num,
                    original_path=imp.import_path,
                    new_path=new_import_path,
                    start_byte=imp.start_byte,
                    end_byte=imp.end_byte
                ).__dict__)

        return plan

    def conduct_healing_rite(self, file_path: Path, plan: List[Dict]) -> bool:
        if not plan: return True
        try:
            content = file_path.read_text("utf-8")
            edicts = [GoHealingEdict(**p) for p in plan]
            new_content = self.surgeon.heal(content, edicts)
            atomic_write(file_path, new_content, Logger, file_path.parent)
            return True
        except Exception as e:
            Logger.error(f"Go surgery failed: {e}")
            return False
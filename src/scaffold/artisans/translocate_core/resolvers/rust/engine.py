# // scaffold/artisans/translocate_core/resolvers/rust/engine.py
# --------------------------------------------------------------

from pathlib import Path
from typing import Dict, List, Optional
from .....utils import atomic_write
from .....logger import Scribe
from .contracts import RustHealingEdict
from .inquisitor import RustInquisitorEngine
from .pathfinder import RustPathfinder
from .surgeon import RustSurgeon

Logger = Scribe("RustResolver")


class RustImportResolver:
    """
    Heals `use` statements when Rust files are moved.
    """

    def __init__(self, project_root: Path, translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = RustPathfinder(self.root)
        self.surgeon = RustSurgeon()

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        try:
            content = file_path.read_text(encoding='utf-8')
        except:
            return []

        uses = RustInquisitorEngine.scan(content)
        plan = []

        for use in uses:
            # 1. Identify what this use points to
            # We assume it points to a file.
            # We assume 'use crate::a::b' imports the module defined in 'src/a/b.rs'

            # Attempt to resolve the file for this module path
            # Heuristic: Strip the last part (symbol) and check if the prefix is a module file
            # or check if the whole thing is a module file.

            target_file = self._find_target_file(use.path)

            if not target_file: continue

            # 2. Check if that file is moving
            future_target = self.moves.get(target_file, target_file)

            # 3. Check if *this* file is moving (affecting `super` or `self` imports,
            # though we focus on absolute `crate::` for now)

            if future_target == target_file:
                continue

            # 4. Calculate new module path
            new_module = self.pathfinder.file_to_module(future_target)

            if not new_module: continue

            # 5. Reconstruct the use path
            # If we resolved 'crate::a::b', and 'b' moved to 'c', new path is 'crate::a::c'
            # If we resolved 'crate::a::b::Struct', and 'b' moved to 'c', new path is 'crate::a::c::Struct'

            old_module_of_target = self.pathfinder.file_to_module(target_file)
            new_use_path = use.path.replace(old_module_of_target, new_module, 1)

            if new_use_path != use.path:
                Logger.info(f"Healing Rust L{use.line_num}: {use.path} -> {new_use_path}")
                plan.append(RustHealingEdict(
                    line_num=use.line_num,
                    original_path=use.path,
                    new_path=new_use_path,
                    start_byte=use.start_byte,
                    end_byte=use.end_byte
                ).__dict__)

        return plan

    def _find_target_file(self, use_path: str) -> Optional[Path]:
        """
        Tries to map a use path to a physical file.
        Try 1: The whole path is a module (src/path.rs)
        Try 2: The path minus last segment is a module (src/path/parent.rs importing symbol)
        """
        # Exact match
        f = self.pathfinder.module_to_file(use_path)
        if f: return f

        # Parent match (importing symbol from file)
        if "::" in use_path:
            parent_mod = use_path.rsplit("::", 1)[0]
            f = self.pathfinder.module_to_file(parent_mod)
            if f: return f

        return None

    def conduct_healing_rite(self, file_path: Path, healing_plan: List[Dict]) -> bool:
        if not healing_plan: return True
        try:
            content = file_path.read_text(encoding='utf-8')
            edicts = [RustHealingEdict(**d) for d in healing_plan]
            new_content = self.surgeon.heal(content, edicts)
            atomic_write(file_path, new_content, Logger, file_path.parent)
            return True
        except Exception as e:
            Logger.error(f"Rust surgery failed: {e}")
            return False
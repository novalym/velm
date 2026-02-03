# Path: scaffold/artisans/translocate_core/resolvers/python/engine.py
# -------------------------------------------------------------------

import ast
from pathlib import Path
from typing import Dict, List

from .....utils import atomic_write
from .....logger import Scribe
from .contracts import HealingEdict
from .intelligence import PythonIntelligence
from .inquisitor import PythonInquisitorEngine
from .pathfinder import PythonPathfinder
from .surgeon import GnosticImportTransformer

Logger = Scribe("PythonResolverEngine")


class PythonImportResolver:
    """
    =================================================================================
    == THE HIGH COORDINATOR OF PYTHON REFACTORING (V-Ω-FORENSIC)                   ==
    =================================================================================
    LIF: ∞

    Orchestrates the grand symphony of Python import healing.
    1. DIAGNOSE: Scans file, finds imports, resolves origins, detects moves, calculates delta.
    2. CONDUCT: Parses AST, summons Surgeon, applies edits, writes file.
    """

    def __init__(self, project_root: Path, symbol_map: Dict[str, Path], translocation_map: Dict[Path, Path]):
        self.root = project_root
        self.symbol_map = symbol_map
        # We resolve all paths in the map to ensure absolute truth
        self.moves = {k.resolve(): v.resolve() for k, v in translocation_map.items()}
        self.pathfinder = PythonPathfinder(self.root, self.symbol_map)

    def diagnose_healing_needs(self, file_path: Path) -> List[Dict]:
        """
        Performs the Gnostic Gaze upon a scripture to see if its connections are broken.
        Returns a list of dicts (serialized HealingEdicts) for the plan.
        """
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return []

        # 1. The Inquisitor's Gaze
        imports = PythonInquisitorEngine.scan_content(content)

        plan = []

        for imp in imports:
            # Construct a readable description for the logs
            import_desc = f"{'.' * imp.level}{imp.module or ''}{'.' + imp.name if imp.module else imp.name}"
            log_prefix = f"[DIAGNOSTIC] Import L{imp.line_num} '{import_desc}'"

            # A. Intelligence Check (Standard Library)
            if PythonIntelligence.is_stdlib(imp.module):
                Logger.verbose(f"{log_prefix} -> STDLIB (Ignored)")
                continue

            # B. Wildcard Check
            if imp.is_wildcard:
                Logger.verbose(f"{log_prefix} -> WILDCARD (Ignored)")
                continue

            # C. Resolve Origin (The Pathfinder's Gaze)
            current_origin = self.pathfinder.resolve_origin(imp, file_path)

            if not current_origin:
                Logger.info(f"{log_prefix} -> RESOLVE FAILED (Not in symbol map or relative lookup failed)")
                continue

            current_origin_res = current_origin.resolve()
            # Logger.info(f"{log_prefix} -> RESOLVED TO: {current_origin_res}")

            # D. Check for Movement (The Translocation Map)
            # We check the translocation map for both the imported file and the current file
            future_origin = self.moves.get(current_origin_res, current_origin_res)
            future_self = self.moves.get(file_path.resolve(), file_path.resolve())

            has_origin_moved = future_origin != current_origin_res
            has_self_moved = future_self != file_path.resolve()

            if not has_origin_moved and not has_self_moved:
                # Logger.verbose(f"{log_prefix} -> NO MOVEMENT (Skipping)")
                continue


            # E. Pathfinding (The Calculation of the New Way)
            new_import_str = self.pathfinder.calculate_new_import_string(future_self, future_origin)

            # Reconstruct the current import string from the AST data for comparison
            dots = "." * imp.level
            mod = imp.module or ""
            current_import_str = f"{dots}{mod}"


            # F. The Final Adjudication
            if new_import_str != current_import_str:
                Logger.info(f"{log_prefix} -> HEALING REQUIRED")

                edict = HealingEdict(
                    line_num=imp.line_num,
                    symbol_name=imp.name,
                    original_module=current_import_str,
                    new_module_path=new_import_str
                )
                plan.append(edict.__dict__)
            else:
                Logger.info(f"{log_prefix} -> NO CHANGE NEEDED (Strings match)")

        return plan

    def conduct_healing_rite(self, file_path: Path, healing_plan: List[Dict]) -> bool:
        """
        Executes the plan. Performs AST surgery on the file.
        """
        if not healing_plan:
            return True


        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)

            # [THE FIX] Rehydrate the Edicts
            # The plan is passed as a list of dicts (from JSON serialization/dossier).
            # The Transformer expects proper HealingEdict objects.
            edicts = [HealingEdict(**d) for d in healing_plan]

            transformer = GnosticImportTransformer(edicts)
            new_tree = transformer.visit(tree)
            ast.fix_missing_locations(new_tree)

            # [THE SCRIBE] Unparse back to source code
            new_content = ast.unparse(new_tree)

            # Atomic Write
            atomic_write(file_path, new_content, Logger, file_path.parent)
            Logger.success(f"[SURGEON] {file_path.name} healed successfully.")
            return True

        except Exception as e:
            Logger.error(f"[SURGEON] Surgery failed on {file_path.name}: {e}", exc_info=True)
            return False
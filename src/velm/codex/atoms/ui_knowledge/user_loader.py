# Path: scaffold/semantic_injection/directives/ui_knowledge/user_loader.py
# -------------------------------------------------------------------------

import importlib.util
import sys
from pathlib import Path
from typing import Optional

from ....logger import Scribe
from ....utils import find_project_root

Logger = Scribe("UserForge")

_LOADED_ROOTS = set()


def load_user_generators(project_root: Optional[Path] = None) -> None:
    """
    =================================================================================
    == THE RITE OF USER ASCENSION (DYNAMIC LOADING)                                ==
    =================================================================================
    Scans the `.scaffold/generators/` sanctum in the user's project.
    Dynamically imports any Python scripts found there.
    This triggers the `@ComponentRegistry.register` decorators within those scripts,
    instantly teaching the God-Engine new forms.
    """
    # 1. Resolve the Sanctum
    if not project_root:
        project_root, _ = find_project_root(Path.cwd())

    if not project_root:
        return  # No project context, no user generators.

    # Idempotency Check
    if project_root in _LOADED_ROOTS:
        return
    _LOADED_ROOTS.add(project_root)

    generators_dir = project_root / ".scaffold" / "generators"

    if not generators_dir.exists():
        return

    Logger.info(f"Perceived User Forge at: [cyan]{generators_dir}[/cyan]")

    # 2. The Walk of Discovery
    # We look for all .py files that aren't special (like __init__)
    for script_path in generators_dir.glob("*.py"):
        if script_path.name.startswith("_"):
            continue

        try:
            # 3. The Rite of Import (Dynamic Module Loading)
            module_name = f"user_gen_{script_path.stem}"
            spec = importlib.util.spec_from_file_location(module_name, str(script_path))

            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                Logger.success(f"   -> Assimilated User Gnosis: [green]{script_path.name}[/green]")
            else:
                Logger.warn(f"   -> Could not inspect soul of '{script_path.name}'")

        except Exception as e:
            Logger.error(f"   -> Paradox loading user generator '{script_path.name}': {e}")
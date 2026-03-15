# Path: src/velm/codex/loader/discovery.py
# ----------------------------------------

import importlib
import importlib.util
import sys
import hashlib
import os
from pathlib import Path
from typing import Dict, Any

from ...logger import Scribe

Logger = Scribe("PluginScrier")

# Merkle Ledger for Hot-Reloading
_FILE_LEDGER: Dict[str, Dict[str, Any]] = {}


class PluginScrier:
    """
    =============================================================================
    == THE SUBSTRATE SCRIER (V-Ω-SANDBOX-IMPORTER)                             ==
    =============================================================================
    Hunts for `.py` files in internal and user-defined directories, verifying
    their Merkle hashes before securely importing them into the Engine.
    """

    @classmethod
    def scry_all_realms(cls):
        # 1. Internal Codex Atoms
        try:
            internal_path_str = "velm.codex.atoms"
            pkg = importlib.import_module(internal_path_str)
            if hasattr(pkg, '__path__') and pkg.__path__:
                root_path = Path(pkg.__path__[0])
                for py_file in root_path.rglob("*.py"):
                    if py_file.stem != "__init__":
                        rel = py_file.relative_to(root_path)
                        mod_name = f"{internal_path_str}.{'.'.join(rel.with_suffix('').parts)}"
                        cls._try_import_internal(mod_name)
        except Exception as e:
            Logger.error(f"Internal Atom Gaze Fractured: {e}")

        # 2. Internal Core (Math, Time, String)
        try:
            core_path_str = "velm.codex.core"
            pkg = importlib.import_module(core_path_str)
            if hasattr(pkg, '__path__') and pkg.__path__:
                root_path = Path(pkg.__path__[0])
                for py_file in root_path.rglob("*.py"):
                    if py_file.stem != "__init__":
                        rel = py_file.relative_to(root_path)
                        mod_name = f"{core_path_str}.{'.'.join(rel.with_suffix('').parts)}"
                        cls._try_import_internal(mod_name)
        except Exception:
            pass

        # 3. User-Forged Plugins (Project & Global)
        gaze_paths = [
            ("Project Forge", Path.cwd() / ".scaffold" / "codex" / "atoms"),
            ("Global Forge", Path.home() / ".scaffold" / "codex" / "atoms"),
        ]

        for source, path in gaze_paths:
            if path.is_dir():
                for py_file in path.rglob("*.py"):
                    if not py_file.stem.startswith("_"):
                        rel = py_file.relative_to(path)
                        mod_name = f"user_forge_{source.replace(' ', '_').lower()}.{rel.with_suffix('').as_posix().replace('/', '.')}"
                        cls.import_user_plugin(mod_name, py_file, source)

    @classmethod
    def _try_import_internal(cls, module_name: str):
        try:
            importlib.import_module(module_name)
        except Exception as e:
            Logger.error(f"Paradox awakening internal soul '{module_name}': {e}")

    @classmethod
    def import_user_plugin(cls, module_name: str, file_path: Path, source: str) -> bool:
        """Loads a user python file, tracking its Hash and Mod-Time."""
        try:
            content = file_path.read_bytes()
            file_hash = hashlib.sha256(content).hexdigest()
            mtime = file_path.stat().st_mtime

            # Skip if unchanged
            if str(file_path) in _FILE_LEDGER:
                if _FILE_LEDGER[str(file_path)]["hash"] == file_hash:
                    return True

            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if not spec or not spec.loader: return False

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Record in Ledger
            _FILE_LEDGER[str(file_path)] = {"hash": file_hash, "mtime": mtime, "mod_name": module_name}
            return True
        except Exception as e:
            Logger.error(f"Heresy awakening user plugin '{file_path.name}': {e}")
            return False
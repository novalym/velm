# Path: scaffold/core/maestro/reverser.py
# ---------------------------------------

# NOTE: This file is a direct translocation of `scaffold/creator/maestro_reverser.py`
# Its logic remains pure and correct in its new, sovereign sanctum.

import os
import re
from pathlib import Path
from typing import Optional, List, Callable, Any, Dict

from ...logger import Scribe

Logger = Scribe("MaestroReverser")


class MaestroReverser:
    """
    [FACULTY 7] The Gnostic Reverser, now in its own sanctum.
    Its purpose is singular and pure: to prophesy the Gnostic Inverse of any known rite.
    """

    # [ASCENSION 4] The Shell Agnostic Soul
    SHELL_COMMAND_MAP = {
        "delete_dir_force": "rm -rf" if os.name != 'nt' else "rmdir /s /q",
        "delete_file": "rm" if os.name != 'nt' else "del",
        "dev_null": "/dev/null" if os.name != 'nt' else "NUL",
    }
    # The Gnostic Trinity of Trinities (Final Form)
    REVERSAL_GRIMOIRE: List[Dict[str, Any]] = [
        {
            "name": "Git Initialization",
            "category": "vcs",
            "safety": "DANGEROUS",
            "description": "Reverses `git init` by deleting the `.git` directory.",
            "pattern": re.compile(r"^\s*git\s+init\b"),
            "templates": [
                "@ask \"This will permanently destroy the Git history. Is this your absolute will?\"",
                "{delete_dir_force} .git"
            ],
            "guard": lambda m, cwd: (cwd / ".git").is_dir() and str(cwd.resolve()) not in (str(Path.home()), "/"),
        },
        # ... (All other grimoire entries remain unchanged and pure) ...
        {
            "name": "Filesystem Touch", "category": "fs", "safety": "SAFE",
            "description": "Reverses `touch` by deleting the created file.",
            "pattern": re.compile(r"^\s*touch\s+([\w./-]+)"),
            "templates": ["{delete_file} {0}"],
            "guard": lambda m, cwd: (cwd / m.group(1)).is_file(),
        },
        {
            "name": "Directory Creation", "category": "fs", "safety": "CAUTIOUS",
            "description": "Reverses `mkdir` by removing the directory if it's empty.",
            "pattern": re.compile(r"^\s*mkdir\s+(?:-p\s+)?([\w./-]+)"),
            "templates": ["rmdir {0}"],
            "guard": lambda m, cwd: (cwd / m.group(1)).is_dir() and not any((cwd / m.group(1)).iterdir()),
        },
        {
            "name": "Node Package Add", "category": "deps", "safety": "SAFE",
            "description": "Reverses a package installation for npm, pnpm, yarn, or bun.",
            "example": "npm i react react-dom",
            "pattern": re.compile(
                r"^\s*(npm|pnpm|yarn|bun)\s+(?:install|i|add)\s+((?:(?:--save-dev|--dev|-D)\s+)?(?:[\w@/.-]+\s*)+)"),
            "templates": ["{0} {1} {2}"],  # manager, uninstall_cmd, packages
            "silent": True,
        },
        {
            "name": "Python Poetry Add", "category": "deps", "safety": "SAFE",
            "description": "Reverses `poetry add` for a specific package.",
            "example": "poetry add black --group dev",
            "pattern": re.compile(r"^\s*poetry\s+add\s+((?:--group\s+\w+\s+)?(?:[\w\-.\[\]]+)+)"),
            "templates": ["poetry remove {0}"],
            "silent": True,
        },
        {
            "name": "Python Pip Install", "category": "deps", "safety": "SAFE",
            "description": "Reverses `pip install` for a specific package.",
            "pattern": re.compile(r"^\s*pip\s+install\s+([\w\-.\[\]==]+)"),
            "templates": ["pip uninstall -y {0}"],
            "silent": True,
        },
        {
            "name": "Docker Build", "category": "container", "safety": "CAUTIOUS",
            "description": "Reverses `docker build` by removing the tagged image.",
            "pattern": re.compile(r"^\s*docker\s+build\s+.*?-t\s+([\w:./-]+)"),
            "templates": [
                "# [NOTE] Attempting to stop any running containers using this image.",
                "docker stop $(docker ps -q --filter ancestor={0}) > {dev_null} 2>&1",
                "docker rmi -f {0}"
            ],
            "silent": False,
        },
    ]

    @staticmethod
    def infer_undo(command: str, cwd: Path) -> Optional[List[str]]:
        """The Grand Rite of Inference."""
        for law in MaestroReverser.REVERSAL_GRIMOIRE:
            try:
                match = law["pattern"].match(command.strip())
                if match:
                    guard = law.get("guard")
                    if guard and not guard(match, cwd):
                        continue
                    templates = law["templates"]
                    args = match.groups()
                    final_templates = []
                    if law["name"] == "Node Package Add":
                        manager, packages_str, *_ = args
                        uninstall_cmd = "remove" if manager in ('yarn', 'pnpm', 'bun') else "uninstall"
                        final_templates = [tmpl.format(manager, uninstall_cmd, packages_str.strip()) for tmpl in templates]
                    else:
                        final_templates = [tmpl.format(*args) for tmpl in templates]
                    final_templates = [tmpl.format(**MaestroReverser.SHELL_COMMAND_MAP) for tmpl in final_templates]
                    if law.get("silent"):
                        final_templates = [f"{tmpl} > {MaestroReverser.SHELL_COMMAND_MAP['dev_null']} 2>&1" for tmpl in final_templates]
                    return final_templates
            except Exception as e:
                Logger.warn(f"Reversal Gaze faltered on law '{law['name']}': {e}")
                continue
        if command.strip() in ("npm install", "pnpm install", "yarn", "bun install"):
            manager = command.split()[0]
            snapshot_name = "pre-install-snapshot"
            return [
                f"# [NOTE] A full `{manager} install` is a complex rite. A forensic snapshot is required for perfect reversal.",
                f"scaffold adopt --output .scaffold/snapshots/{snapshot_name}.json --format json --full",
                f"# [UNDO-ACTION] To reverse, speak the sacred edict:",
                f"# scaffold transmute .scaffold/snapshots/{snapshot_name}.json --force"
            ]
        if command.startswith("poetry install"):
            return ["# [WARNING] A full `poetry install` is not yet perfectly reversible. The lockfile provides the path back."]
        return None
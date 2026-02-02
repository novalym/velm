# Path: scaffold/utils/workspace_utils.py
# ---------------------------------------
from pathlib import Path
from typing import Optional, List


def find_workspace_root(start_path: Path) -> Optional[Path]:
    """
    Performs a recursive Gaze upwards for the `.scaffold-workspace` scripture.
    """
    current = start_path.resolve()
    while True:
        if (current / ".scaffold-workspace").is_file():
            return current
        if current.parent == current:  # Reached the filesystem root
            return None
        current = current.parent


def read_workspace_projects(workspace_root: Path) -> List[Path]:
    """
    Reads the scripture and returns a list of absolute project paths.
    """
    scripture_path = workspace_root / ".scaffold-workspace"
    if not scripture_path.is_file():
        return []

    projects = []
    content = scripture_path.read_text(encoding='utf-8')
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            projects.append((workspace_root / line).resolve())

    return projects
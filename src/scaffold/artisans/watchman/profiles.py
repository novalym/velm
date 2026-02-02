# Path: scaffold/artisans/watchman/profiles.py
# --------------------------------------------
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class WatchProfile:
    name: str
    glob: str
    command: str
    help_text: str
    ignore: List[str] = None


# THE SENTINEL'S GRIMOIRE
# A repository of best-practice watch configurations.
WATCH_PROFILES: Dict[str, WatchProfile] = {
    "rust": WatchProfile(
        name="rust",
        glob="**/*.rs",
        command="cargo check -q",
        help_text="Watches .rs files, runs 'cargo check' (quiet).",
        ignore=["target/"]
    ),
    "rust-test": WatchProfile(
        name="rust-test",
        glob="**/*.rs",
        command="cargo test -q",
        help_text="Watches .rs files, runs 'cargo test'.",
        ignore=["target/"]
    ),
    "python": WatchProfile(
        name="python",
        glob="**/*.py",
        command="pytest",
        help_text="Watches .py files, runs 'pytest'.",
        ignore=["__pycache__/", ".pytest_cache/", "venv/", ".venv/"]
    ),
    "python-check": WatchProfile(
        name="python-check",
        glob="**/*.py",
        command="ruff check .",
        help_text="Watches .py files, runs 'ruff check'.",
    ),
    "node": WatchProfile(
        name="node",
        glob="**/*.{js,ts,jsx,tsx,json}",
        command="npm test",
        help_text="Watches JS/TS files, runs 'npm test'.",
        ignore=["node_modules/", "dist/", "build/", "coverage/"]
    ),
    "go": WatchProfile(
        name="go",
        glob="**/*.go",
        command="go run .",
        help_text="Watches .go files, runs 'go run .'.",
    ),
    "scaffold": WatchProfile(
        name="scaffold",
        glob="**/*.py",
        command="pip install . && scaffold --version",
        help_text="Dev mode: Reinstalls Scaffold on change.",
    )
}


def resolve_profile(target: str) -> Optional[WatchProfile]:
    """
    Attempts to find a profile matching the target name.
    Supports basic aliases (e.g., 'py' -> 'python').
    """
    t = target.lower()
    if t in WATCH_PROFILES:
        return WATCH_PROFILES[t]

    # Aliases
    if t == "py": return WATCH_PROFILES["python"]
    if t == "rs": return WATCH_PROFILES["rust"]
    if t == "ts" or t == "js": return WATCH_PROFILES["node"]

    return None


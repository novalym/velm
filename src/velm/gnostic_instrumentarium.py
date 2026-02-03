# Path: scaffold/gnostic_instrumentarium.py

"""
=================================================================================
== THE GNOSTIC INSTRUMENTARIUM (V-Ω-ETERNAL. THE PROPHET'S MIND)               ==
=================================================================================
This is not a file of code. It is the living, eternal mind of the Gnostic Prophet
that resides within the Quantum Creator. It is a sacred, extensible Grimoire that
contains the Gnosis of all known mortal and divine artisans (tools) required to
conduct the symphonies of creation.
=================================================================================
"""
import os
import platform
import shutil
from pathlib import Path
from typing import Dict, Any, Optional

# =================================================================================
# == THE SACRED CONTRACT OF GNOSTIC INSTRUMENTS                                  ==
# =================================================================================
#
# Each verse in this Grimoire is a pure, declarative law with this sacred contract:
#
#   "purpose": A luminous scripture explaining the artisan's divine role.
#
#   "gaze": A divine lambda that performs a Gaze upon the mortal realm to see
#           if the artisan is manifest.
#
#   "consecration_rites": A vessel containing the sacred edicts for summoning
#                         the artisan into existence, tailored for each realm.
# =================================================================================

GNOSTIC_INSTRUMENTARIUM: Dict[str, Dict[str, Any]] = {
    "git": {
        "purpose": "The Divine Chronomancer, guardian of a project's history and soul.",
        "gaze": lambda: shutil.which("git"),
        "consecration_rites": {
            "ubuntu/debian": "sudo apt-get install git",
            "macos": "brew install git",
            "windows": "choco install git",
            "manual": "https://git-scm.com/downloads"
        }
    },
    "make": {
        "purpose": "The Universal Conductor of Rites, the one true altar for all Maestro's Edicts.",
        "gaze": lambda: shutil.which("make"),
        "consecration_rites": {
            "ubuntu/debian": "sudo apt-get install make",
            "macos": "xcode-select --install",
            "windows": "choco install make",
            "manual": "Consult your realm's sacred texts for 'make' or a GNU toolchain."
        }
    },
    "poetry": {
        "purpose": "The Master Artisan of Pythonic Souls, for dependency management and packaging.",
        "gaze": lambda: shutil.which("poetry"),
        "consecration_rites": {
            "universal": "pip install poetry",
            "manual": "https://python-poetry.org/docs/#installation"
        }
    },
    "npm": {
        "purpose": "The Scribe of the Node Cosmos, for managing the souls of JavaScript realities.",
        "gaze": lambda: shutil.which("npm"),
        "consecration_rites": {
            "universal": "Install Node.js & npm from https://nodejs.org/",
            "windows": "choco install nodejs",
            "macos": "brew install node"
        }
    },
    "docker": {
        "purpose": "The Forger of Unbreakable Vessels, the God-Engine of Containerization.",
        "gaze": lambda: shutil.which("docker"),
        "consecration_rites": {
            "universal": "Install Docker Desktop from https://www.docker.com/products/docker-desktop/",
        }
    },
    # The Grimoire is eternal and extensible. New artisans can be added here.
    "vscode": {
        "purpose": "The Luminous Editor, the Sanctum of Code.",
        "gaze": lambda: shutil.which("code"),
        "consecration_rites": {
            "windows": "https://code.visualstudio.com/Download", # Manual install link
            "macos": "https://code.visualstudio.com/Download",
            "ubuntu/debian": "https://code.visualstudio.com/Download",
            "manual": "https://code.visualstudio.com/docs/setup/setup-overview"
        }
    }
}


def gaze_for_hidden_artisan(tool_key: str) -> Optional[Path]:
    """
    =================================================================================
    == THE GNOSTIC PATHFINDER (V-Ω-DEEP-SCAN)                                      ==
    =================================================================================
    Performs a deep search in the probable sanctums of the OS to find a missing
    artisan that is installed but not in the PATH.
    """
    system = platform.system().lower()

    # The Map of Hidden Sanctums
    SEARCH_PATHS = {
        "windows": [
            # VS Code User
            Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
            # VS Code System
            Path(os.environ.get("ProgramFiles", "")) / "Microsoft VS Code" / "bin" / "code.cmd",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "Microsoft VS Code" / "bin" / "code.cmd",
            # Git
            Path(os.environ.get("ProgramFiles", "")) / "Git" / "cmd" / "git.exe",
            # Node
            Path(os.environ.get("ProgramFiles", "")) / "nodejs" / "npm.cmd",
        ],
        "darwin": [  # MacOS
            Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"),
            Path("/usr/local/bin/code"),
        ],
        "linux": [
            Path("/usr/bin/code"),
            Path("/snap/bin/code"),
        ]
    }

    # The Mapping of Tools to Filenames (if different)
    TOOL_MAP = {
        "vscode": "code.cmd" if system == "windows" else "code",
        "code": "code.cmd" if system == "windows" else "code",
        "git": "git.exe" if system == "windows" else "git",
        "npm": "npm.cmd" if system == "windows" else "npm",
    }

    filename = TOOL_MAP.get(tool_key, tool_key)

    # 1. Check standard paths
    candidates = SEARCH_PATHS.get(system, [])
    for candidate in candidates:
        # Check if the path ends with our target tool name
        if candidate.name.lower() == filename.lower() and candidate.exists():
            return candidate

    # 2. If still lost, we can try a broader heuristic if needed,
    # but for now, we stick to known safe locations.

    return None




def get_platform_key() -> str:
    """A Gnostic Gaze to perceive the Architect's current mortal realm."""
    system = platform.system().lower()
    if system == "linux":
        # A prophecy for a more divine Gaze in the future (e.g., checking /etc/os-release)
        return "ubuntu/debian"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "manual"
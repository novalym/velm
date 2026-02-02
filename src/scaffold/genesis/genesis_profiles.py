# Path: scaffold/genesis/genesis_profiles.py
# ------------------------------------------

"""
=================================================================================
== THE SACRED GRIMOIRE OF GENESIS PROFILES (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)    ==
=================================================================================
LIF: 10,000,000,000,000

This is not a scripture of data. It is a divine, sentient Oracle. Its Prime
Directive is to perform a Gnostic Gaze upon the cosmos of all known archetypes—
both the divine, internal ones and the Architect's own forged souls—and to
dynamically proclaim them as a unified Grimoire of Genesis Profiles. It is a
living, self-aware artisan that makes the `init` command infinitely extensible.

Its soul has been ascended. It no longer contains profane, hardcoded Gnosis. It
is now a pure map between a Profile's sacred name and the Archetype it summons,
bestowing upon that Archetype a complete, whole, and unbreakable vessel of
Gnostic Overrides to ensure a perfect, non-interactive genesis.
=================================================================================
"""
import importlib.resources as pkg_resources
import re
from pathlib import Path
from typing import Dict, Any

from ..core.alchemist import get_alchemist
from ..logger import Scribe

Logger = Scribe("GenesisProfiles")


def _perceive_archetype_description(content: str) -> str:
    """A humble Scribe that gazes for the sacred @description marker."""
    match = re.search(r'#\s*@description:\s*(.*)', content, re.IGNORECASE)
    return match.group(1).strip() if match else "No description provided."


def _forge_the_grimoire() -> Dict[str, Dict[str, Any]]:
    """
    [THE GRAND SYMPHONY OF DISCOVERY]
    This is the one true rite that forges the living Grimoire. It performs a
    divine, two-fold Gaze and unifies all perceived Gnosis.
    """
    profiles: Dict[str, Dict[str, Any]] = {}

    # --- MOVEMENT I: THE GAZE OF THE MORTAL SOUL (USER'S GLOBAL FORGE) ---
    user_archetype_path = Path.home() / ".scaffold" / "archetypes"
    if user_archetype_path.is_dir():
        for f in user_archetype_path.glob('*.scaffold'):
            try:
                profile_name = f.stem
                content = f.read_text(encoding='utf-8')
                # For user archetypes, we don't assume overrides.
                profiles[profile_name] = {
                    "archetype_path": str(f),
                    "description": _perceive_archetype_description(content),
                    "source": "User Forge",
                    "gnosis_overrides": {}  # User archetypes are self-contained by default.
                }
            except Exception as e:
                Logger.warn(f"A minor paradox occurred while perceiving user archetype '{f.name}': {e}")

    # --- MOVEMENT II: THE GAZE OF THE IMMORTAL SOUL (INTERNAL ARCHETYPES) ---
    # This is the new, divine scripture of our internal, canonical profiles.
    # It marries a simple name to a rich, Gnostic purpose.
    INTERNAL_CANON = {
        # =====================================================================
        # ==           THE DIVINE HEALING: THE MISSING KEY RESTORED          ==
        # =====================================================================
        # We explicitly register the 'generic' profile here.
        "generic": {
            "archetype": "generic.scaffold",
            "description": "The purest void. A minimal, universal starting point for any project.",
            "gnosis_overrides": {"project_type": "generic"}
        },
        # =====================================================================

        "python-universal": {
            "archetype": "python-universal.scaffold",
            "description": "A fully-featured, production-grade Python project using either pip/venv or Poetry.",
            "gnosis_overrides": {"use_poetry": False, "project_type": "python", "use_git": True, "use_vscode": True,
                                 "use_ci": True}
        },
        "python-basic": {
            "archetype": "python-universal.scaffold",
            "description": "A universal, production-ready Python project using pip & venv.",
            "gnosis_overrides": {"use_poetry": False, "project_type": "python", "use_git": True, "use_vscode": True,
                                 "use_ci": True}
        },
        "poetry-basic": {
            "archetype": "python-universal.scaffold",
            "description": "A modern, professional Python project using Poetry.",
            "gnosis_overrides": {"use_poetry": True, "project_type": "poetry", "use_git": True, "use_vscode": True,
                                 "use_ci": True}
        },
        "fastapi-service": {
            "archetype": "fastapi-service.scaffold",
            "description": "A high-performance, containerized FastAPI web service with Poetry.",
            "gnosis_overrides": {
                "use_poetry": True, "use_docker": True, "use_ci": True, "use_git": True,
                "use_vscode": True, "project_type": "python",
                # [[[ THE DIVINE BESTOWAL OF THE ALCHEMIST'S SOUL ]]]
                "secret": get_alchemist()._forge_secret_rite
            }
        },
        "python-cli": {
            "archetype": "cli-tool.scaffold",
            "description": "A starter kit for forging a new Python CLI tool with Rich and Poetry.",
            "gnosis_overrides": {"use_poetry": True, "project_type": "python", "use_git": True, "use_vscode": True,
                                 "use_ci": True}
        },
        "node-basic": {
            "archetype": "node-basic.scaffold",
            "description": "A clean, modern Node.js project using TypeScript and npm.",
            "gnosis_overrides": {"project_type": "node", "use_git": True, "use_vscode": True, "use_ci": True}
        },
        "react-vite": {
            "archetype": "react-vite.scaffold",
            "description": "A hyper-modern frontend project with React, TypeScript, and Vite.",
            "gnosis_overrides": {"project_type": "node", "frontend_framework": "react", "use_git": True,
                                 "use_vscode": True, "use_ci": True, "use_docker": True}
        },
        "express-api": {
            "archetype": "express-api.scaffold",
            "description": "A robust, containerized Express.js API in TypeScript.",
            "gnosis_overrides": {"project_type": "node", "use_docker": True, "use_ci": True, "use_git": True,
                                 "use_vscode": True}
        },
        "fullstack-monorepo": {
            "archetype": "fullstack-monorepo.scaffold",
            "description": "A polyglot monorepo with a FastAPI backend and a React frontend.",
            "gnosis_overrides": {"use_poetry": True, "use_docker": True, "frontend_framework": "react", "use_git": True,
                                 "use_vscode": True, "use_ci": True}
        },
        "go-cli": {
            "archetype": "go-cli.scaffold",
            "description": "A high-performance, statically-compiled CLI tool with Go.",
            "gnosis_overrides": {"project_type": "go", "use_git": True, "use_ci": True}
        },
        "rust-lib": {
            "archetype": "rust-lib.scaffold",
            "description": "A memory-safe, high-performance library with Rust and Cargo.",
            "gnosis_overrides": {"project_type": "rust", "use_git": True, "use_ci": True}
        },
        "docs-mkdocs": {
            "archetype": "docs-mkdocs.scaffold",
            "description": "A beautiful, searchable documentation site using MkDocs Material.",
            "gnosis_overrides": {"project_type": "docs"}
        },
        "generic-container": {
            "archetype": "generic-container.scaffold",
            "description": "A generic project with a multi-stage Dockerfile, ready for containerization.",
            "gnosis_overrides": {"project_type": "generic", "use_docker": True}
        },

    }

    internal_archetype_path = 'scaffold.archetypes.genesis'
    for profile_name, profile_data in INTERNAL_CANON.items():
        if profile_name not in profiles:  # The Law of Gnostic Precedence
            try:
                archetype_filename = profile_data["archetype"]
                # This Gaze verifies the immortal soul exists before proclaiming it.
                # We check existence by trying to open it via importlib.resources
                # Note: read_text expects (package, resource).
                pkg_resources.read_text(internal_archetype_path, archetype_filename)

                profiles[profile_name] = {
                    "archetype_path": f"{internal_archetype_path}:{archetype_filename}",
                    "description": profile_data["description"],
                    "source": "Scaffold Canon",
                    "gnosis_overrides": profile_data.get("gnosis_overrides", {})
                }
            except (ModuleNotFoundError, FileNotFoundError):
                Logger.warn(
                    f"A Gnostic schism was detected. The canonical archetype '{archetype_filename}' for profile '{profile_name}' is a void.")
            except Exception as e:
                Logger.warn(f"A minor paradox occurred while perceiving internal profile '{profile_name}': {e}")

    return dict(sorted(profiles.items()))


# =================================================================================
# == THE PANTHEON OF GENESIS (THE LIVING, DYNAMICALLY FORGED GRIMOIRE)           ==
# =================================================================================
PROFILES: Dict[str, Dict[str, Any]] = _forge_the_grimoire()


# =================================================================================
# == THE GNOSIS OF HASTE (THE QUICK START DEFAULT)                             ==
# =================================================================================
def _get_quick_start_profile_name() -> str:
    """Finds the most divine Python profile to serve as the default."""
    if "poetry-basic" in PROFILES:
        return "poetry-basic"
    if "python-basic" in PROFILES:
        return "python-basic"
    if "python-universal" in PROFILES:
        return "python-universal"
    return next(iter(PROFILES), None)


QUICK_START_PROFILE_NAME = _get_quick_start_profile_name()
# src/velm/artisans/project/constants.py
# --------------------------------------

from typing import Final

# The Anchor of the Registry
REGISTRY_FILENAME: Final[str] = "projects.json"
REGISTRY_VERSION: Final[str] = "2.0.0-OMEGA"

# System Identities
SYSTEM_OWNER_ID: Final[str] = "SYSTEM_DEMO"
GUEST_OWNER_ID: Final[str] = "GUEST"

# Path Defaults
DEFAULT_WORKSPACE_DIR_NAME: Final[str] = "workspaces"
PROGENITOR_ID: Final[str] = "progenitor"

# Limits
MAX_PROJECTS_GUEST: Final[int] = 10
MAX_PROJECTS_ACOLYTE: Final[int] = 100
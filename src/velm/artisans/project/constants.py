# Path: src/velm/artisans/project/constants.py
# --------------------------------------------
# LIF: ∞ | ROLE: ARCHITECTURAL_CONSTITUTION | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONSTANTS_V205_PROGENITOR_SUTURE_2026_FINALIS

from typing import Final
import uuid

# =============================================================================
# == STRATUM-0: IDENTITY & VERSIONING (THE LAW)                             ==
# =============================================================================
# These constants define the soul and versioning of the Multiversal Registry.

REGISTRY_FILENAME: Final[str] = "projects.json"
REGISTRY_VERSION: Final[str] = "2.0.0-OMEGA"

# [ASCENSION]: THE DETERMINISTIC NAMESPACE
# Used for UUIDv5 generation to ensure System Archetypes have identical
# coordinates across every machine and browser substrate.
GNOSTIC_NAMESPACE: Final[uuid.UUID] = uuid.NAMESPACE_DNS
SEED_NAMESPACE_PREFIX: Final[str] = "novalym.seed."


# =============================================================================
# == STRATUM-1: THE PROGENITOR ANCHOR (THE AXIS MUNDI)                      ==
# =============================================================================
# [THE CURE]: ABSOLUTE IDENTITY HARMONIZATION.
# This value is the mathematical result of:
# uuid.uuid5(uuid.NAMESPACE_DNS, "novalym.seed.progenitor")
#
# HARD-CODING RATIONALE:
# This serves as the 'Genesis Root' for the entire ecosystem. By hard-coding
# this coordinate, we allow the Ocular UI to possess 'Precognitive Awareness'
# of the Progenitor Law before the Python Kernel has finished its initial
# Census. It is the immutable anchor of the Novalym multiverse.
# [THE ANCHOR]: uuid.uuid5(uuid.NAMESPACE_DNS, "novalym.seed.progenitor")
PROGENITOR_ID: Final[str] = "9af8880f-f3a8-5fa3-a167-b9165c7c5039"


# =============================================================================
# == STRATUM-2: SOVEREIGNTY & OWNERSHIP (THE CASTES)                        ==
# =============================================================================
# Defines the hierarchy of existence within the Multiverse.

SYSTEM_OWNER_ID: Final[str] = "SYSTEM_DEMO"
GUEST_OWNER_ID: Final[str] = "GUEST"
ADMIN_OWNER_ID: Final[str] = "ARCHITECT_PRIME"

# Identity Labeling
GUEST_PROJECT_NAME_DEFAULT: Final[str] = "Untitled Reality"
SYSTEM_PROJECT_DESCRIPTION: Final[str] = "System Reference Architecture."


# =============================================================================
# == STRATUM-3: PHYSICS & TOPOGRAPHY (THE SANCTUM)                          ==
# =============================================================================
# Defines the physical anchoring of projects on the substrate.

DEFAULT_WORKSPACE_DIR_NAME: Final[str] = "workspaces"
VAULT_ROOT: Final[str] = "/vault"

# The DNA keys used to identify core archetypes in the SEED_VAULT.
DNA_KEY_PROGENITOR: Final[str] = "progenitor"
DNA_KEY_BLANK: Final[str] = "blank"

# Shadow Directory for Transactions
CHRONOS_STAGING_DIR: Final[str] = ".scaffold/chronos"
CHRONICLE_BACKUP_DIR: Final[str] = ".scaffold/chronicles"


# =============================================================================
# == STRATUM-4: METABOLISM & THRESHOLDS (THE VIGIL)                         ==
# =============================================================================
# Defines the metabolic tax and resource boundaries for each reality.

# Project Limits
MAX_PROJECTS_GUEST: Final[int] = 10
MAX_PROJECTS_ACOLYTE: Final[int] = 100
MAX_PROJECTS_SOVEREIGN: Final[int] = 9999

# Mass Limits (in Megabytes)
MAX_PROJECT_SIZE_GUEST: Final[int] = 50
MAX_PROJECT_SIZE_ACOLYTE: Final[int] = 500

# Temporal Vows (Time-To-Live)
GUEST_IDLE_TTL_SECONDS: Final[int] = 1800 # 30 Minutes (The Amnesia Protocol)
METABOLIC_PULSE_INTERVAL: Final[int] = 5   # Heartbeat rate in seconds


# =============================================================================
# == STRATUM-5: CHROMATIC RESONANCE (THE AURA)                             ==
# =============================================================================
# Harmonizes the UI visual frequency with the Backend status.

# High-Status UI Tints
COLOR_RESONANT: Final[str] = "#64ffda"  # Sovereign Teal
COLOR_WILL: Final[str] = "#a855f7"      # Gnostic Purple
COLOR_LOGIC: Final[str] = "#3b82f6"     # Logic Blue
COLOR_FRACTURED: Final[str] = "#ef4444" # Heresy Red
COLOR_WARM: Final[str] = "#fbbf24"      # Metabolic Amber

# Sigil Mappings
SIGIL_GENESIS: Final[str] = "Zap"
SIGIL_ARCHETYPE: Final[str] = "LayoutGrid"
SIGIL_LOCKED: Final[str] = "Lock"
SIGIL_GHOST: Final[str] = "Fingerprint"


# =============================================================================
# == THE FINALITY VOW                                                        ==
# =============================================================================
# The Physics of the Multiverse are now sealed. No drift is possible.
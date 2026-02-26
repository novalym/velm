# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge/sieve.py
# ---------------------------------------------------------------------------

from typing import Set, Final, Tuple
from pathlib import Path


class EntropySieve:
    """
    =============================================================================
    == THE OMNISCIENT ENTROPY SIEVE (V-Ω-TOTALITY-V24-ABYSS-WARD)              ==
    =============================================================================
    LIF: ∞ | ROLE: MATTER_CLASSIFIER | RANK: OMEGA_GUARDIAN

    Adjudicates which matter is worthy of replication (The True Architecture)
    and which is mere Metabolic Waste or Immutable Scripture.
    """

    ABYSS_PATTERNS: Final[Set[str]] = {
        # --- VCS & Metadata ---
        '.git', '.hg', '.svn', '.scaffold', '.heartbeat', '.scaffold_internal',
        '.DS_Store', 'Thumbs.db', 'desktop.ini',

        # --- Virtual Environments & Runtimes ---
        '__pycache__', '.venv', 'venv', 'env', 'node_modules', '.npm', '.yarn',
        '.pnpm-store', '.turbo', '.next', '.cache', '.parcel-cache',

        # --- Build Artifacts & Mass ---
        'dist', 'build', 'target', 'out', 'bin', 'obj', 'release', 'debug',

        # --- IDE Artifacts ---
        '.idea', '.vscode', '.project', '.settings', '.history'
    }

    ABYSS_SUFFIXES: Final[Tuple[str, ...]] = (
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.tmp', '.swp'
    )

    HOLY_SUFFIXES: Final[Tuple[str, ...]] = (
        '.scaffold',
        '.symphony',
        '.arch',
        '.patch.scaffold',
        '.trait.scaffold',
        '.kit.scaffold'
    )

    @classmethod
    def is_profane(cls, name: str) -> bool:
        """True if the item is metabolic waste and should be ignored."""
        if name in cls.ABYSS_PATTERNS:
            return True
        if name.endswith(cls.ABYSS_SUFFIXES):
            return True
        return False

    @classmethod
    def is_holy_scripture(cls, file_path: Path) -> bool:
        """
        True if the item is the 'Word of the Architect'.
        Holy scriptures are warded against duplication to prevent the 'Infinite Echo' paradox.
        """
        name = file_path.name.lower()
        return name.endswith(cls.HOLY_SUFFIXES)
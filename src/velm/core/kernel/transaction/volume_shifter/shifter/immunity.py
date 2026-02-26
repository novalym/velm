# Path: src/velm/core/kernel/transaction/volume_shifter/shifter/immunity.py
# -------------------------------------------------------------------------

import os
from pathlib import Path
from typing import Set, Final


class ImmunityMatrix:
    """
    =================================================================================
    == THE IMMUNITY MATRIX: OMEGA (V-Ω-TOTALITY-V64-PHALANX-SUTURED)               ==
    =================================================================================
    LIF: ∞ | ROLE: SPATIAL_IMMUNITY_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

    This rite performs a deep-tissue scan of a path to determine if it is "Holy
    Ground". If immunity is granted, the Hand of Matter is stayed.
    """

    CROWN_JEWELS: Final[Set[str]] = {
        '.scaffold',
        '.git',  # Protected! But Absolute Immunity Lift handles initial creation.
        '.hg',
        '.svn',
        'transaction.lock',
        'daemon.pulse',
        'daemon.pid',
        'scaffold.sock',
        'scaffold.lock',
        'gnosis.db',
        'gnosis.db-shm',
        'gnosis.db-wal',
        'commit.journal'
    }

    HOLY_SUFFIXES: Final[Set[str]] = {
        '.scaffold',
        '.symphony',
        '.arch',
        '.patch.scaffold',
        '.trait.scaffold',
        '.kit.scaffold'
    }

    def __init__(self, logger):
        self.Logger = logger

    def is_immune(self, path: Path) -> bool:
        """
        Returns True if the path represents Holy Ground that must not be overwritten
        by the Volume Shifter.
        """
        if path is None:
            return True

        name = path.name

        if os.name == 'nt':
            name = name.lower()
            crown_jewels = {j.lower() for j in self.CROWN_JEWELS}
            holy_suffixes = {s.lower() for s in self.HOLY_SUFFIXES}
        else:
            crown_jewels = self.CROWN_JEWELS
            holy_suffixes = self.HOLY_SUFFIXES

        # 1. THE CENSUS OF ORGANS
        if name in crown_jewels:
            return True

        # 2. THE CENSUS OF THE WORD
        for sfx in holy_suffixes:
            if name.endswith(sfx):
                return True

        # 3. RECURSIVE HIERARCHICAL WARD
        for part in path.parts:
            p_name = part.lower() if os.name == 'nt' else part
            if p_name in crown_jewels:
                return True

        return False
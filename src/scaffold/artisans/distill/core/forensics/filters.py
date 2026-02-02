# Path: scaffold/artisans/distill/core/oracle/forensics/filters.py
# ----------------------------------------------------------------

from pathlib import Path
from typing import Set


class ApophaticWards:
    """
    The filter that separates Signal (User Code) from Noise (Library Code).
    """

    # The Realms of Noise
    NOISE_DIRS: Set[str] = {
        'node_modules', 'site-packages', 'dist-packages',
        'venv', '.venv', 'env',
        'dist', 'build', 'target', 'bin', 'obj',
        'vendor', 'gems', 'anaconda', 'miniconda',
        'usr/lib', 'usr/include', 'Program Files'
    }

    @classmethod
    def is_noise(cls, path_str: str) -> bool:
        """
        Adjudicates if a path belongs to the Profane Realm of libraries.
        """
        # Normalize slashes for the check
        clean = path_str.replace('\\', '/')

        # Check if any noise dir is a component of the path
        for noise in cls.NOISE_DIRS:
            if f"/{noise}/" in clean or clean.startswith(f"{noise}/"):
                return True

        return False


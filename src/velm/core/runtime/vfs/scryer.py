# Path: src/velm/core/runtime/vfs/alchemist.py
# ------------------------------------------
import os
from pathlib import Path
from typing import Union


class MatterAlchemist:
    """
    =============================================================================
    == THE MATTER ALCHEMIST (V-Ω-RECALL-ENGINE)                                ==
    =============================================================================
    Distills physical bytes into Gnostic souls (strings) or Binary Husks.
    """

    @staticmethod
    def read_soul(path_str: str) -> str:
        """Reads a file and determines if its soul is printable."""
        path = Path(path_str).resolve()
        if not path.exists():
            return "[VOID] Scripture unmanifest."

        try:
            # 1. PEAK AT MATTER (Check for Binary)
            with open(path, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:
                    return "[BINARY_MATTER_REDACTED]"

            # 2. RESURRECT TEXT
            return path.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            return f"[HERESY] Recall failed: {str(e)}"


def vfs_read_scripture(path: str) -> str:
    """Universal interface for the WASM Worker's READ rite."""
    return MatterAlchemist.read_soul(path)
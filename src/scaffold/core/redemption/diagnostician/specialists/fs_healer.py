# Path: scaffold/core/redemption/diagnostician/specialists/fs_healer.py
# ---------------------------------------------------------------------

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any
from ..contracts import Diagnosis


class FilesystemHealer:
    """The Specialist of the Mortal Realm."""

    @staticmethod
    def heal(exc: BaseException, context: Dict[str, Any]) -> Optional[Diagnosis]:

        # 1. The Gaze of the Void (FileNotFound)
        if isinstance(exc, FileNotFoundError):
            filename = exc.filename
            if not filename: return None
            path = Path(filename)

            if path.name == "scaffold.scaffold":
                return Diagnosis(
                    heresy_name="MissingBlueprint",
                    cure_command="scaffold init",
                    advice="The Master Blueprint is missing. Initiate Genesis.",
                    confidence=1.0,
                    metadata={}
                )

            if path.name in ["daemon.json", "daemon.lock"]:
                return Diagnosis(
                    heresy_name="MissingDaemonInfo",
                    cure_command="scaffold daemon start",
                    advice="Daemon configuration missing. Awaken the Daemon.",
                    confidence=0.9,
                    metadata={}
                )

        # 2. The Gaze of Authority (PermissionError)
        if isinstance(exc, PermissionError):
            # Windows File Lock (WinError 32)
            if getattr(exc, 'winerror', 0) == 32:
                return Diagnosis(
                    heresy_name="WindowsLock",
                    cure_command=None,
                    advice=f"The file '{exc.filename}' is held by another process. Release it.",
                    confidence=1.0,
                    metadata={}
                )

            # Unix Permission
            if sys.platform != "win32" and exc.filename:
                return Diagnosis(
                    heresy_name="PermissionDenied",
                    cure_command=f"chmod +w {exc.filename}",
                    advice="Write permission denied. Consecrate the file.",
                    confidence=0.9,
                    metadata={}
                )

        # 3. The Encoding Alchemist
        if isinstance(exc, UnicodeDecodeError):
            return Diagnosis(
                heresy_name="BinarySoul",
                cure_command=None,
                advice="Attempted to read a binary soul as text. Specify encoding or ignore.",
                confidence=0.9,
                metadata={}
            )

        return None
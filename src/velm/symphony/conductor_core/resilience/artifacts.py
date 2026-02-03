# Path: scaffold/symphony/conductor_core/resilience/artifacts.py
# --------------------------------------------------------------

import json
import time
import traceback
from pathlib import Path
from typing import Any

from ....logger import Scribe
from ....contracts.symphony_contracts import Edict, ActionResult

Logger = Scribe("ArtifactKeeper")


class ArtifactKeeper:
    """
    =============================================================================
    == THE KEEPER OF ARTIFACTS (V-Ω-FORENSIC-SCRIBE)                           ==
    =============================================================================
    Responsible for crystallizing the state of a failure into a file for later analysis.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.crash_dir = self.root / ".scaffold" / "crashes"
        self.crash_dir.mkdir(parents=True, exist_ok=True)

    def hoard(self, result: 'ActionResult', edict: 'Edict', exception: Exception) -> Path:
        """Saves the crash dump to disk."""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"crash_{timestamp}_{edict.type.name}.json"
        path = self.crash_dir / filename

        data = {
            "timestamp": time.time(),
            "edict": edict.model_dump(mode='json'),
            "error": str(exception),
            "traceback": traceback.format_exc(),
            "output": result.output if result else "N/A",
            "return_code": result.returncode if result else -1
        }

        try:
            path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            Logger.verbose(f"Crash artifact secured at: {path}")
            return path
        except Exception as e:
            Logger.warn(f"Failed to save crash artifact: {e}")
            return path
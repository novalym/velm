# Path: core/runtime/engine/resilience/forensics.py
# -------------------------------------------------

import json
import time
import os
import traceback
from pathlib import Path


class ForensicLab:
    """
    =============================================================================
    == THE FORENSIC LAB (V-Ω-BLACK-BOX-RECORDER)                               ==
    =============================================================================
    Captures the final moments of a dying process.
    """

    @staticmethod
    def capture_crash(error: Exception, context: dict = None):
        """
        Writes a crash report to .scaffold/crash_reports/
        """
        try:
            report_dir = Path(".scaffold/crash_reports")
            report_dir.mkdir(parents=True, exist_ok=True)

            timestamp = int(time.time())
            filename = f"crash_{timestamp}_{type(error).__name__}.json"

            report = {
                "timestamp": timestamp,
                "error_type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(),
                "context": context or {},
                "env": {k: v for k, v in os.environ.items() if k.startswith("SCAFFOLD_")}
            }

            with open(report_dir / filename, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

        except Exception:
            # If forensics fail, print to stderr as last resort
            traceback.print_exc()
# Path: scaffold/core/kernel/archivist/manifest.py
# ------------------------------------------------

import json
import platform
import getpass
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

class ManifestScribe:
    """
    =============================================================================
    == THE SCRIBE OF PROVENANCE (V-Ω-METADATA-INJECTOR)                        ==
    =============================================================================
    Forges the internal passport that travels within the time capsule.
    """

    @staticmethod
    def forge(reason: str, file_hashes: Dict[str, str], skipped: List[str]) -> bytes:
        meta = {
            "schema_version": "2.0",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "epoch": time.time(),
            "reason": reason,
            "architect": getpass.getuser(),
            "host_machine": platform.node(),
            "os_system": platform.system(),
            "python_version": platform.python_version(),
            "stats": {
                "total_files": len(file_hashes),
                "skipped_count": len(skipped)
            },
            "files": file_hashes,
            "skipped_log": skipped
        }
        return json.dumps(meta, indent=2).encode('utf-8')
# Path: scaffold/utils/dossier_scribe/constellation/crystal.py
# ------------------------------------------------------------

import json
from pathlib import Path
from typing import Dict, Any, List
from ....interfaces.base import Artifact
from ....utils import hash_file


class CrystalMemory:
    """
    =================================================================================
    == THE CRYSTAL MEMORY (V-Ω-DETERMINISTIC-SNAPSHOT)                             ==
    =================================================================================
    LIF: 10,000,000,000

    Transmutes the chaotic, time-bound reality of the filesystem into a
    pure, deterministic JSON crystal. This artifact serves as the "Golden Master"
    for automated verification rites (tests).

    It ignores volatile properties (timestamps, permissions on Windows) to ensure
    that Truth remains constant across space and time.
    """

    @staticmethod
    def crystallize(project_root: Path, artifacts: List[Artifact]) -> str:
        """
        Forges the Golden JSON.
        """
        # We build a flat map of the expected reality based on artifacts + disk state
        snapshot = {
            "root": project_root.name,
            "structure": {}
        }

        # We sort artifacts to ensure deterministic JSON output
        sorted_artifacts = sorted(artifacts, key=lambda a: str(a.path))

        for art in sorted_artifacts:
            # We calculate the relative key
            try:
                key = str(art.path.relative_to(project_root)).replace("\\", "/")
            except ValueError:
                key = art.path.name  # External

            entry = {
                "type": art.type,
                "action": art.action
            }

            # If it's a file, we capture its eternal soul (Hash), not its timestamp.
            if art.type == "file" and art.path.exists():
                entry["hash"] = hash_file(art.path)
                entry["size"] = art.path.stat().st_size

            # [ASCENSION] Include Metadata for deeper verification
            if art.metadata:
                # Filter out volatile metadata if necessary, but keep diffs
                clean_meta = {k: v for k, v in art.metadata.items() if k != 'duration_ms'}
                if clean_meta:
                    entry["meta"] = clean_meta

            snapshot["structure"][key] = entry

        return json.dumps(snapshot, indent=2, sort_keys=True)
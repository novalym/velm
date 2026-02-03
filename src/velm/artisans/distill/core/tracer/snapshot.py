# Path: scaffold/artisans/distill/core/oracle/tracer/snapshot.py
# --------------------------------------------------------------

import json
from pathlib import Path
from .contracts import RuntimeState, TracePoint, VariableGnosis
from ......contracts.heresy_contracts import ArtisanHeresy


class SnapshotReader:
    """
    =============================================================================
    == THE MEMORY READER (V-Ω-JSON-PARSER)                                     ==
    =============================================================================
    Reads standardized JSON snapshots of runtime state.
    """

    def __init__(self, root: Path):
        self.root = root

    def load(self, path: Path) -> RuntimeState:
        if not path.exists():
            raise ArtisanHeresy(f"Snapshot file not found: {path}")

        try:
            data = json.loads(path.read_text(encoding='utf-8'))
            state = RuntimeState()

            # Schema: List of TracePoints
            # [ { "path": "src/main.py", "line": 10, "vars": {"x": "1"}, "error": "Boom" } ]

            for entry in data:
                # Normalize path relative to root
                raw_path = entry.get('path', '')
                # Handle absolute paths in snapshot
                if str(self.root) in raw_path:
                    clean_path = raw_path.replace(str(self.root), "").lstrip("/\\")
                else:
                    clean_path = raw_path

                vars_dict = {}
                for k, v in entry.get('vars', {}).items():
                    vars_dict[k] = VariableGnosis(name=k, type="unknown", value=str(v))

                point = TracePoint(
                    file_path=clean_path,
                    line_no=entry.get('line'),
                    function_name=entry.get('func', 'unknown'),
                    variables=vars_dict,
                    event_type="exception" if entry.get('error') else "line",
                    error_message=entry.get('error')
                )
                state.add_point(point)

            return state

        except json.JSONDecodeError as e:
            raise ArtisanHeresy(f"Snapshot corrupted: {e}")
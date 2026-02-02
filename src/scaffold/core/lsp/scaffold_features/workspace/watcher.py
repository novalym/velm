# Path: core/lsp/scaffold_features/workspace/watcher.py
# -----------------------------------------------------
from typing import List
from ...base.features.workspace.models import FileEvent, FileChangeType
from ....base.utils.uri import UriUtils


class ScaffoldFluxProvider:
    """
    [THE CAUSAL EYE]
    Reacts to changes in specific Scaffold files to keep the Cortex warm.
    """

    def __init__(self, server: Any):
        self.server = server

    def on_file_events(self, events: List[FileEvent]):
        for event in events:
            path = UriUtils.to_fs_path(event.uri)

            # [ASCENSION 1]: BLUEPRINT SENSITIVITY
            if path.suffix in ('.scaffold', '.arch', '.splane'):
                if event.type == FileChangeType.Changed:
                    # Trigger a re-analysis if the law has changed
                    self.server.diagnostics.schedule_validation(event.uri, 0, priority=True)

            # [ASCENSION 5]: LOCKFILE RESONANCE
            if path.name == "scaffold.lock":
                # Reality has shifted externally (e.g. Git pull)
                # Proclaim to the UI that a "Global Survey" is recommended
                pass
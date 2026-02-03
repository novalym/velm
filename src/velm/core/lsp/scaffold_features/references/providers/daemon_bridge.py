# Path: core/lsp/scaffold_features/references/providers/daemon_bridge.py
# -------------------------------------------------------------------------
from typing import List, Any
from ....base.features.references.contracts import ReferenceProvider
from ....base.features.references.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo
from ....base.utils.uri import UriUtils


class DaemonCortexProvider(ReferenceProvider):
    """[THE CORTEX BRIDGE] Siphons project-wide references from the Hive."""

    @property
    def name(self) -> str:
        return "DaemonCortex"

    @property
    def priority(self) -> int:
        return 50

    def find_references(self, doc: TextDocument, info: WordInfo, context: Any) -> List[Location]:
        # [ASCENSION 3]: ADRENALINE REQUISITION
        if not hasattr(self.server, 'relay_request'): return []

        # Request the Daemon to scan the Global Gnostic Index
        params = {
            "file_path": str(UriUtils.to_fs_path(doc.uri)),
            "symbol": info.text.replace("{", "").replace("}", "").replace("$", "").strip(),
            "project_root": str(self.server.project_root),
            "include_declaration": context.includeDeclaration,
            "metadata": {"source": "LSP_REFERENCES", "trace_id": getattr(self.server, 'current_trace_id', 'tr-ref')}
        }

        try:
            # Synchronous plea across the Silver Cord portal
            response = self.server.relay_request("references", params)
            if response and response.get('success'):
                raw_data = response.get('data', [])
                locations = []
                for item in raw_data:
                    # [ASCENSION 2]: ISOMORPHIC URI SUTURE
                    uri = item["uri"]
                    if not uri.startswith("file:"):
                        uri = UriUtils.to_uri(uri)

                    locations.append(Location(
                        uri=uri,
                        range=Range.model_validate(item["range"])
                    ))
                return locations
        except:
            pass

        return []
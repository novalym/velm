# Path: core/lsp/scaffold_features/definition/rules/global_symbols.py
# ------------------------------------------------------------------
import logging
from typing import Optional, Union, List
from ....base.features.definition.contracts import DefinitionRule
from ....base.features.definition.models import Location, Range, Position
from ....base.document import TextDocument
from ....base.utils.text import WordInfo
from ....base.utils.uri import UriUtils


class GlobalCortexRule(DefinitionRule):
    """[THE CORTEX BRIDGE] Interrogates the Daemon for cross-file symbols."""

    @property
    def name(self) -> str:
        return "GlobalCortex"

    @property
    def priority(self) -> int:
        return 50

    def matches(self, info: WordInfo) -> bool:
        return info.kind in ('variable', 'generic')

    def resolve(self, doc: TextDocument, info: WordInfo) -> Optional[Location]:
        # [ASCENSION 5]: ADRENALINE BRIDGE
        if not hasattr(self.server, 'relay_request'): return None

        params = {
            "file_path": str(UriUtils.to_fs_path(doc.uri)),
            "content": doc.text,
            "position": info.position.model_dump(),
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_DEFINITION", "symbol": info.text}
        }

        try:
            # Synchronous plea through the Silver Cord portal
            response = self.server.relay_request("definition", params)

            if response and response.get('success'):
                data = response.get('data')
                if data and "uri" in data and "range" in data:
                    # [ASCENSION 1]: URI SUTURE
                    # Ensure path is formatted correctly for Monaco
                    uri = data["uri"]
                    if not uri.startswith("file:"):
                        uri = UriUtils.to_uri(uri)

                    return Location(
                        uri=uri,
                        range=Range.model_validate(data["range"])
                    )
        except:
            pass
        return None
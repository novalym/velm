# Path: core/lsp/scaffold_features/inline_completion/providers/muse.py
# --------------------------------------------------------------------

import logging
from typing import List
from ....base.features.inline_completion.contracts import InlineCompletionProvider
from ....base.features.inline_completion.models import InlineCompletionItem, InlineCompletionParams
from ....base.utils.uri import UriUtils

Logger = logging.getLogger("MuseProphet")


class MuseProphet(InlineCompletionProvider):
    """
    [THE MUSE]
    Siphons predictive intelligence from the Daemon.
    """

    @property
    def name(self) -> str:
        return "Muse"

    @property
    def priority(self) -> int:
        return 90

    def prophesy(self, params: InlineCompletionParams) -> List[InlineCompletionItem]:
        # [ASCENSION 1]: RELAY CHECK
        if not hasattr(self.server, 'relay_request'): return []

        uri = str(params.text_document.uri)
        pos = params.position

        # [ASCENSION 2]: FORGE THE PLEA
        payload = {
            "file_path": str(UriUtils.to_fs_path(uri)),
            "position": {"line": pos.line, "character": pos.character},
            "project_root": str(self.server.project_root or "."),
            "metadata": {"source": "LSP_GHOST_TEXT"}
        }

        try:
            # [ASCENSION 3]: SYNCHRONOUS RELAY
            # The Daemon must respond fast (< 300ms) or we timeout.
            # This requires the Daemon to use a fast local model or cached prediction.
            response = self.server.relay_request("muse", payload)

            if response and response.get('success'):
                raw_items = response.get('data', {}).get('predictions', [])
                return [
                    InlineCompletionItem(
                        insertText=item['text'],
                        filterText=item.get('filter_text'),
                        range=item.get('range')  # Optional range replacement
                    ) for item in raw_items
                ]
        except Exception as e:
            Logger.debug(f"Muse Silence: {e}")

        return []
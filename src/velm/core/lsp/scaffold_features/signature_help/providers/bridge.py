# Path: core/lsp/scaffold_features/signature_help/providers/bridge.py
# -----------------------------------------------------------------------
from typing import List, Any
from ....base.features.signature_help.contracts import SignatureProvider, InvocationContext
from ....base.features.signature_help.models import SignatureInformation, ParameterInformation
from ....base.utils.uri import UriUtils


class DaemonSignatureProvider(SignatureProvider):
    """[THE CORTEX BRIDGE] Siphons deep signatures from the Hive."""

    @property
    def name(self) -> str:
        return "DaemonCortex"

    @property
    def priority(self) -> int:
        return 50

    def provide_signatures(self, ctx: InvocationContext) -> List[SignatureInformation]:
        # [ASCENSION 4]: ADRENALINE REQUISITION
        if not hasattr(self.server, 'relay_request'): return []

        params = {
            "file_path": str(UriUtils.to_fs_path(ctx.uri)),
            "symbol": ctx.symbol_name.replace('{', '').replace('}', '').replace('@call', '').strip(),
            "project_root": str(self.server.project_root),
            "metadata": {"source": "LSP_SIGNATURE", "trace_id": ctx.trace_id}
        }

        try:
            # Synchronous plea across the Silver Cord portal
            response = self.server.relay_request("signature", params)
            if response and response.get('success'):
                raw_sigs = response.get('data', [])
                # Transmute into our models
                return [SignatureInformation.model_validate(s) for s in raw_sigs]
        except:
            pass

        return []
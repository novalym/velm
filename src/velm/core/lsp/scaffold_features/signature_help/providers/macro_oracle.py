# Path: core/lsp/scaffold_features/signature_help/providers/macro_oracle.py
# --------------------------------------------------------------------------
import re
from typing import List, Optional
from ....base.features.signature_help.contracts import SignatureProvider, InvocationContext
from ....base.features.signature_help.models import SignatureInformation, ParameterInformation


class MacroSignatureProvider(SignatureProvider):
    """[THE MACRO ORACLE] Scries local @macro definitions."""

    @property
    def name(self) -> str:
        return "MacroOracle"

    @property
    def priority(self) -> int:
        return 100

    # Matches: @macro name(p1, p2="val")
    DEF_PATTERN = re.compile(r'^\s*@macro\s+([a-zA-Z_]\w*)\s*\((.*?)\)')

    def provide_signatures(self, ctx: InvocationContext) -> List[SignatureInformation]:
        # 1. Clean the name
        # e.g., @call my_macro -> my_macro
        name = ctx.symbol_name.replace('@call', '').strip()

        # 2. Scan current buffer for definition
        # We fetch the full document text from the server
        doc = self.server.documents.get(ctx.uri)
        if not doc: return []

        for match in self.DEF_PATTERN.finditer(doc.text):
            m_name, m_params = match.groups()

            if m_name == name:
                # [ASCENSION 1]: Extract Parameters
                param_list = [p.strip() for p in m_params.split(',') if p.strip()]
                params = [ParameterInformation(label=p) for p in param_list]

                return [SignatureInformation(
                    label=f"{m_name}({', '.join(param_list)})",
                    documentation=f"### Gnostic Macro: `{m_name}`\nLocal definition found in scripture.",
                    parameters=params
                )]

        return []
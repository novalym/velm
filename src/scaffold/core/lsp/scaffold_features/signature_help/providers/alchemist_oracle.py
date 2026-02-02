# Path: core/lsp/scaffold_features/signature_help/providers/alchemist_oracle.py
# -----------------------------------------------------------------------------
from typing import List, Optional, Dict
from ....base.features.signature_help.contracts import SignatureProvider, InvocationContext
from ....base.features.signature_help.models import SignatureInformation, ParameterInformation


class AlchemistSignatureProvider(SignatureProvider):
    """[THE ALCHEMIST ORACLE] Constant-time guidance for built-ins."""

    @property
    def name(self) -> str: return "AlchemistOracle"

    @property
    def priority(self) -> int: return 90

    # [ASCENSION 2]: THE SACRED GRIMOIRE
    GRIMOIRE: Dict[str, Dict] = {
        "env": {
            "label": "env(key: string, default: any = None)",
            "doc": "Summons a value from the host environment.",
            "params": ["key", "default"]
        },
        "now": {
            "label": "now(format: string = '%Y-%m-%d')",
            "doc": "Returns the current temporal coordinate.",
            "params": ["format"]
        },
        "secret": {
            "label": "secret(length: int, type: string = 'hex')",
            "doc": "Generates a cryptographically secure random string.",
            "params": ["length", "type"]
        },
        "read_file": {
            "label": "read_file(path: string)",
            "doc": "Reads the soul of a physical file as a string.",
            "params": ["path"]
        }
    }

    def provide_signatures(self, ctx: InvocationContext) -> List[SignatureInformation]:
        # Strip Jinja braces if present
        name = ctx.symbol_name.replace('{', '').replace('}', '').strip()

        if name in self.GRIMOIRE:
            g = self.GRIMOIRE[name]
            params = [ParameterInformation(label=p) for p in g["params"]]

            return [SignatureInformation(
                label=g["label"],
                documentation=f"### Built-in: `{name}`\n{g['doc']}",
                parameters=params
            )]

        return []
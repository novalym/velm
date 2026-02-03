# Path: core/lsp/scaffold_features/hover/providers/alchemy.py
# -----------------------------------------------------------

import re
import logging
from typing import Optional, Any
from ....base.features.hover.contracts import HoverProvider, HoverContext

Logger = logging.getLogger("AlchemyProvider")

class AlchemyProvider(HoverProvider):
    """
    =============================================================================
    == THE STATE SCRYER (V-Ω-LOCAL-VALUE-INFERENCE)                            ==
    =============================================================================
    [CAPABILITIES]:
    1. Scans the current buffer for variable assignments.
    2. Projects the "Shadow Truth" (inferred value) next to usages.
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "Alchemy"

    @property
    def priority(self) -> int:
        return 90

    def provide(self, ctx: HoverContext) -> Optional[str]:
        try:
            # [ASCENSION 1]: TOKEN PURIFICATION
            # Clean the token: {{ var }} -> var
            clean_name = ctx.word.replace("{{", "").replace("}}", "").replace("$$", "").strip()
            if not clean_name: return None

            # [ASCENSION 2]: HEURISTIC INTERPOLATION
            # Scan for: $$ var = val OR let var = val
            # Matches keys with quotes or without
            pattern = re.compile(
                rf'^\s*(?:\$\$|let|def|const)\s*{re.escape(clean_name)}\s*(?::\s*[^=]+)?\s*=\s*(.*)',
                re.MULTILINE
            )

            match = pattern.search(ctx.full_content)
            if match:
                value = match.group(1).strip().strip("\"'")
                # Calculate line number by counting newlines up to the match
                line_idx = ctx.full_content[:match.start()].count('\n') + 1

                return (
                    f"### 💎 Alchemical Truth\n"
                    f"**Variable:** `{clean_name}`\n"
                    f"**Current Value:** `{value}`\n\n"
                    f"---\n"
                    f"Defined in local scripture at **Line {line_idx}**"
                )
            return None

        except Exception as e:
            Logger.error(f"Alchemical Scry Fractured: {e}")
            return None
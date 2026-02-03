# Path: core/lsp/scaffold_features/hover/providers/mentor.py
# ----------------------------------------------------------

import logging
from typing import Optional, Any
from ....base.features.hover.contracts import HoverProvider, HoverContext

Logger = logging.getLogger("MentorProvider")

class MentorProvider(HoverProvider):
    """
    =============================================================================
    == THE ARCHITECTURAL VOICE (V-Ω-SOCRATIC-GUIDANCE)                         ==
    =============================================================================
    [CAPABILITIES]:
    1. Provides real-time Socratic guidance based on patterns.
    2. Warns against destructive commands (rm -rf).
    3. Suggests Gnostic best practices (Vows, Safety).
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "Mentor"

    @property
    def priority(self) -> int:
        return 40

    def provide(self, ctx: HoverContext) -> Optional[str]:
        try:
            # [ASCENSION 1]: KINETIC ACTION AUDIT
            if ">>" in ctx.word or ">>" in ctx.line_text:
                return (
                    "### 💡 Gnostic Mentor\n"
                    "**Pattern:** Kinetic Action (`>>`)\n"
                    "**Advice:** Every action should be followed by a Vow (`??`) to verify reality."
                    "\n\n[Add Vow of Success](command:scaffold.heal?%7B%22type%22:%22add_vow%22%7D)"
                )

            # [ASCENSION 2]: ANNIHILATION WARD
            if "rm -rf" in ctx.line_text:
                return (
                    "### 💀 ANNIHILATION WARNING\n"
                    "**Gnosis:** This command will return its target to the true void. "
                    "Ensure the path is warded."
                )

            # [ASCENSION 3]: SUDO CHECK
            if "sudo " in ctx.line_text:
                return (
                    "### 🛡️ PRIVILEGE ESCALATION\n"
                    "**Gnosis:** usage of `sudo` breaks hermetic seals in CI/CD. "
                    "Prefer running the entire container as root or using capabilities."
                )

            return None

        except Exception as e:
            Logger.error(f"Mentor Voice Fractured: {e}")
            return None
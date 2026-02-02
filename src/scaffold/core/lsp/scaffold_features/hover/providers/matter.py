# Path: core/lsp/scaffold_features/hover/providers/matter.py
# ----------------------------------------------------------

import os
import logging
from pathlib import Path
from typing import Optional, Any
from ....base.features.hover.contracts import HoverProvider, HoverContext
from ....base.utils.uri import UriUtils

Logger = logging.getLogger("MatterProvider")


class MatterProvider(HoverProvider):
    """
    =============================================================================
    == THE GEOMETRIC READER (V-Ω-FILESYSTEM-AWARENESS)                         ==
    =============================================================================
    [CAPABILITIES]:
    1. Confirms physical existence of referenced files.
    2. Scries the Shadow Vault for ephemeral files.
    3. Calculates file mass (size).
    """

    def __init__(self, server: Any):
        self.server = server

    @property
    def name(self) -> str:
        return "Matter"

    @property
    def priority(self) -> int:
        return 80

    def provide(self, ctx: HoverContext) -> Optional[str]:
        try:
            # [ASCENSION 1]: CONTEXT TRIAGE
            # Is this a path context?
            is_path_op = any(s in ctx.line_text for s in ("::", "<<", "->", "@include"))
            is_path_char = '/' in ctx.word

            if not (is_path_op or is_path_char):
                return None

            path_str = ctx.word.strip("\"'")
            if not path_str: return None

            # [ASCENSION 2]: ROOT RESOLUTION
            root = ctx.workspace_root or self.server.project_root or Path.cwd()

            # Handle absolute vs relative
            if os.path.isabs(path_str):
                # Unsafe to hover absolute paths generally, but we check if it's inside root
                try:
                    physical_path = Path(path_str).resolve()
                except OSError:
                    return None
            else:
                physical_path = (root / path_str).resolve()

            # [ASCENSION 3]: SHADOW GAZE
            # Check if the file is dreaming in the staging area
            shadow_path = root / ".scaffold" / "staging" / path_str

            res = []
            if physical_path.exists():
                kind = 'Sanctum' if physical_path.is_dir() else 'Scripture'
                size = physical_path.stat().st_size if physical_path.is_file() else 0
                res.append(
                    f"### 🏗️ Manifested Form\n"
                    f"**Nature:** {kind}\n"
                    f"**State:** ✅ Physically Stable\n"
                    f"**Mass:** `{size} bytes`"
                )
            elif shadow_path.exists():
                res.append(f"### 👻 Shadow Projection\n**Nature:** Scripture\n**State:** 🔮 Dreaming in Staging")

            if not res and (is_path_op or is_path_char):
                return f"### 🌑 Void Path\n**Target:** `{path_str}`\n**Gnosis:** This path is currently a non-reality."

            if not res:
                return None

            return "\n\n".join(res)

        except Exception as e:
            Logger.error(f"Matter Scan Fractured: {e}")
            return None
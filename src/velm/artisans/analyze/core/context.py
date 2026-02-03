# Path: artisans/analyze/core/context.py
# --------------------------------------

import os
from pathlib import Path
from typing import Optional, Tuple, Any

from ....logger import Scribe


class AnalysisContext:
    """
    =============================================================================
    == THE CONTEXT ANCHOR (V-Ω-SPATIAL-REALITY)                                ==
    =============================================================================
    Responsible for resolving the physical and logical location of scriptures.
    It bridges the gap between the Disk (Matter) and the Shadow Vault (Mind).
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = Scribe("AnalysisContext")

    def resolve_target_root(self, request_root: Optional[Any]) -> Path:
        """Divines the true root of the project for the duration of the rite."""
        initial_engine_root = self.engine.project_root
        if isinstance(initial_engine_root, str):
            initial_engine_root = Path(initial_engine_root)

        if request_root:
            return Path(str(request_root)).resolve()
        elif initial_engine_root:
            return initial_engine_root.resolve()
        else:
            return Path(os.getcwd()).resolve()

    def resolve_multiversal_content(
            self,
            manual_content: Optional[str],
            physical_path: Path,
            session_id: str = "global"
    ) -> Tuple[Optional[str], bool, Optional[str]]:
        """
        Adjudicates the 'Soul' of a scripture by scrying across the Editor, the
        Shadow Layer, and the Physical Disk.
        """
        # --- PHASE I: THE EDITOR'S WILL (Highest Precedence) ---
        if manual_content is not None:
            return manual_content, False, None

        # --- PHASE II: THE SHADOW REALITY (The AI's Dream) ---
        shadow_content = self._get_content_from_shadow(physical_path, session_id)
        if shadow_content is not None:
            is_bin = b'\0' in shadow_content[:8192]
            try:
                decoded = shadow_content.decode('utf-8', errors='replace')
                return decoded, is_bin, None
            except Exception as e:
                return None, True, f"Shadow Decoding Error: {e}"

        # --- PHASE III: THE MORTAL REALM (Physical Disk) ---
        if not physical_path.exists():
            return None, False, "Scripture is a void in all known realities."

        try:
            # Binary Diviner
            with open(physical_path, 'rb') as f:
                peek = f.read(8192)
                is_bin = b'\0' in peek

            if is_bin:
                return None, True, "Scripture possesses a binary soul."

            content = physical_path.read_text(encoding='utf-8', errors='replace')
            return content, False, None

        except PermissionError:
            return None, False, "Access Denied by Host Reality."
        except Exception as e:
            return None, False, f"Physical I/O Paradox: {e}"

    def is_path_in_shadow(self, physical_path: Path, session_id: str) -> bool:
        """Checks if a file exists in the Shadow Vault."""
        return self._get_content_from_shadow(physical_path, session_id) is not None

    def _get_content_from_shadow(self, physical_path: Path, session_id: str) -> Optional[str]:
        """Scries the .scaffold/staging area."""
        if not self.engine: return None
        try:
            raw_root = self.engine.project_root or os.getcwd()
            anchor = Path(raw_root).resolve()

            try:
                rel_path = physical_path.relative_to(anchor)
            except ValueError:
                return None

            if session_id and session_id != "global":
                staging_root = anchor / ".scaffold" / "staging" / session_id
                shadow_file = staging_root / rel_path

                if shadow_file.exists() and shadow_file.is_file():
                    return shadow_file.read_text(encoding='utf-8', errors='replace')
            return None
        except Exception:
            return None


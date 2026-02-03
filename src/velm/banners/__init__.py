# Path: scaffold/banners/__init__.py
# ----------------------------------
import os
import sys
from pathlib import Path
from rich.align import Align
from rich.text import Text
from rich.panel import Panel


def get_project_sigil() -> Align:
    """
    =================================================================================
    == THE GNOSTIC BRIDGE (V-Ω-PRIORITY-FIXED)                                     ==
    =================================================================================
    The Oracle of the Sigil.

    HIERARCHY OF TRUTH:
    1. The Raw Scripture (`.scaffold/banner.txt`) - The Architect's Explicit Will.
    2. The Low Gaze (Windows/CI) - The Safe Text Fallback.
    3. The High Gaze (`sigil.py`) - The Luminous Image (Only if safe).
    """

    # --- 1. THE SIMPLE GAZE (The Architect's Will) ---
    # We look for a custom banner.txt first. If it exists, it IS the sigil.
    search_paths = [
        Path.cwd() / ".scaffold" / "banner.txt",
        Path.home() / ".scaffold" / "banner.txt"
    ]

    for path in search_paths:
        if path.exists():
            try:
                # We read the soul and wrap it in a luminous Text object
                raw_art = path.read_text(encoding='utf-8')
                # We render it bold and centered
                return Align.center(Text(raw_art, style="bold blue"))
            except Exception:
                pass

    # --- 2. THE WINDOWS WARD (The Safe Fallback) ---
    # If we are on Windows, or MSYS, or Cygwin, we strictly forbid the High Gaze
    # to prevent the "Garbled Text" heresy.
    if os.name == 'nt' or sys.platform.startswith('win') or sys.platform == 'cygwin' or sys.platform == 'msys':
        try:
            from .fallback import get_fallback_sigil
            return get_fallback_sigil()
        except (ImportError, Exception):
            return Align.center(Text("SCAFFOLD", style="bold red"))

    # --- 3. THE HIGH GAZE (The Computed Image) ---
    # Only attempted if no banner exists AND we are on a capable OS.
    try:
        from .sigil import get_sigil
        return Align.center(get_sigil())
    except (ImportError, AttributeError):
        pass

    # --- 4. THE ULTIMATE FALLBACK ---
    try:
        from .fallback import get_fallback_sigil
        return get_fallback_sigil()
    except Exception:
        return Align.center(Text("SCAFFOLD", style="bold cyan"))


__all__ = ["get_project_sigil"]
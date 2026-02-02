# Path: scaffold/banners/fallback.py
# ----------------------------------
from rich.align import Align
from rich.text import Text
from rich.panel import Panel


def get_fallback_sigil() -> Align:
    """
    =================================================================================
    == THE ETERNAL WORD (V-Ω-TEXTUAL-MAJESTY)                                      ==
    =================================================================================
    This artisan is the failsafe voice of the God-Engine.

    If the image-based Sigil cannot be summoned (missing dependencies or OS limits),
    and no custom `banner.txt` exists, this artisan proclaims the name "SCAFFOLD"
    in the sacred ASCII tongue.
    """

    # The "Standard" Font representation of SCAFFOLD.
    # Hardcoded to ensure zero-dependency beauty.
    raw_art = r"""
   _____            __  __       _     _ 
  / ____|          / _|/ _|     | |   | |
 | (___   ___ __ _| |_| |_ ___  | | __| |
  \___ \ / __/ _` |  _|  _/ _ \ | |/ _` |
  ____) | (_| (_| | | | || (_) || | (_| |
 |_____/ \___\__,_|_| |_| \___/ |_|\__,_|
    """

    # We render it in a bold, cyan hue to signify Gnostic clarity.
    fallback_text = Text(raw_art, style="bold cyan", justify="left")

    # We align it to the center of the terminal for maximum gravity.
    return Align.center(fallback_text)
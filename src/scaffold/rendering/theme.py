# Path: rendering/theme.py
# ------------------------

from dataclasses import dataclass, field
from typing import Dict, List

from rich.style import Style
from rich.text import Text


@dataclass
class GnosticTheme:
    """
    =================================================================================
    == THE SACRED GRIMOIRE OF GNOSTIC AESTHETICS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++) ==
    =================================================================================
    LIF: 10,000,000

    This is the final, eternal, and ultra-definitive soul of the `GnosticTheme`. It
    is a complete, self-aware palette of architectural aesthetics, infused with the
    very **symbols of our Gnostic faith**. Its purpose is to provide a universal,
    luminous, and context-aware voice for all visual proclamations, ensuring the
    Architect's Gaze is instantly drawn to truth and guided away from heresy.

    Its soul is now a pantheon of profound, game-changing faculties:

    1.  **The Law of the Canonical Symbol:** It centralizes all core icons and
        sigils, ensuring a unified visual language across the entire cosmos.
    2.  **The Grimoire of Git Sigils:** It contains the divine map for Git status
        symbols, infusing version control status with immediate, color-coded Gnosis.
    3.  **The Codex of Sacred Suffixes:** It explicitly defines the extensions of
        our sacred blueprint scriptures, allowing for dedicated, luminous styling.
    4.  **The Voice of Heat (Complexity):** It defines the color spectrum for
        architectural complexity, transforming raw metrics into intuitive visual cues.
    5.  **The Beacon of Activity:** It proclaims the symbol for an active/dirty file.
    6.  **The Pantheon of Origin Sigils:** It explicitly defines all symbols used to
        proclaim a file's content origin (inline, seed, binary, secret, forge).
    =================================================================================
    """

    # --- I. THE PURE PALETTE (Colors for all Gnostic Revelation) ---
    directory_color: str = "bold #87CEEB"  # LightSkyBlue
    file_color: str = "#E0E0E0"  # Light Grey
    link_color: str = "cyan"
    metadata_color: str = "dim"
    secret_color: str = "yellow"
    binary_color: str = "red"
    forge_color: str = "dim cyan"  # For files from Template Forge or inline blocks
    git_color: str = "dim #2E8B57"  # SeaGreen
    permission_color: str = "magenta"
    sacred_scripture_color: str = "bold cyan"  # For .scaffold, .symphony, .arch files

    # === THE VOICE OF HEAT (COMPLEXITY) ===
    heat_colors: Dict[str, str] = field(default_factory=lambda: {
        "Critical": "#ff0000",  # Volcanic Red
        "High": "#ff8c00",  # Blazing Orange
        "Medium": "#ffd700",  # Warning Yellow
        "Low": "#00ff7f",  # Serene Green
    })

    # --- II. THE CANONICAL SYMBOLS (Icons & Sigils for Visual Gnosis) ---
    dir_icon: str = "📁"
    file_icon: str = "📄"
    active_file_sigil: str = "▶"  # Symbol for the currently active file in the editor.
    warning_sigil: str = "⚠️"  # Universal warning symbol.

    # === THE GRIMOIRE OF GIT SIGILS ===
    git_sigil_grimoire: Dict[str, Text] = field(default_factory=lambda: {
        'M': Text(" M ", Style(color="yellow")),  # Modified
        'A': Text(" A ", Style(color="green")),  # Added
        'D': Text(" D ", Style(color="red")),  # Deleted
        'R': Text(" R ", Style(color="cyan")),  # Renamed
        'C': Text(" C ", Style(color="bright_magenta")),  # Copied
        'U': Text(" ? ", Style(color="magenta")),  # Untracked/Unmerged
        '?': Text(" ? ", Style(color="magenta")),  # Untracked (explicitly as '?')
        'I': Text(" I ", Style(color="grey50")),  # Ignored
    })

    # === THE CODEX OF SACRED SUFFIXES ===
    sacred_scripture_suffixes: List[str] = field(default_factory=lambda: [".scaffold", ".symphony", ".arch"])

    # === THE PANTHEON OF ORIGIN SIGILS (The Corrected List) ===
    inline_soul_sigil: str = "✍️"  # For content provided directly
    seed_soul_sigil: str = "🌱"  # For content from an external file (<<)
    forge_soul_sigil: str = "🔥"  # For content from Template Forge
    binary_soul_sigil: str = "💿"  # For detected binary files
    secret_soul_sigil: str = "🔑"  # For files like .env
    permission_sigil: str = "🛡️"   # [THE FIX] The Shield of Execution
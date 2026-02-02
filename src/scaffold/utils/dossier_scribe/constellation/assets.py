# Path: scaffold/utils/dossier_scribe/constellation/assets.py
# -----------------------------------------------------------

from typing import Dict, Any


class GnosticAssets:
    """
    The Sacred Symbols and Orders of the Orrery.
    Now ascended with the Gnostic Differential (Action States).
    """

    # --- The Visual Language of File Types ---
    ICON_MAP: Dict[str, str] = {
        # Code
        '.py': '🐍', '.pyi': '🐍', '.pyc': '🐍',
        '.js': '⚡', '.jsx': '⚛️', '.ts': '📘', '.tsx': '⚛️',
        '.vue': '🟢', '.svelte': '🔥',
        '.go': '🐹', '.rs': '🦀', '.rb': '💎', '.java': '☕',
        '.c': '🇨', '.cpp': '🇨', '.h': '🇨',

        # Scripts
        '.sh': '🐚', '.bash': '🐚', '.zsh': '🐚', '.ps1': '📜',

        # Web
        '.html': '🌐', '.css': '🎨', '.scss': '🎀', '.sass': '🎀', '.less': '🎀',

        # Config & Data
        '.json': '📦', '.yml': '🔧', '.yaml': '🔧', '.toml': '⚙️',
        '.xml': '📰', '.ini': '⚙️', '.csv': '📊', '.sql': '💾',

        # Environment & Secrets
        '.env': '🔑', '.gitignore': '👁️', '.dockerignore': '🐳',

        # Sacred Filenames
        'dockerfile': '🐳', 'makefile': '🛠️', 'gemfile': '💎',
        'package.json': '📦', 'pyproject.toml': '🐍', 'cargo.toml': '🦀', 'go.mod': '🐹',
        'license': '⚖️', 'readme.md': '📖', 'changelog.md': '📅',
        'scaffold.scaffold': '🏗️', 'scaffold.lock': '🔒', 'architecture.md': '🏛️',

        # Images
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️',
        '.svg': '📐', '.ico': '🖼️',

        # Fonts
        '.ttf': '🔤', '.otf': '🔤', '.woff': '🔤', '.woff2': '🔤',

        # Generic
        'dir': '📂', 'file': '📄', 'link': '🔗', 'vault': '🛡️', 'lock': '🔒', 'exec': '⚙️',
        'workspace': '🌌'
    }

    # --- The Gnostic Differential (Visualizing Change) ---
    ACTION_MAP: Dict[str, Dict[str, str]] = {
        'CREATED': {'icon': '✨', 'style': 'bold green'},
        'TRANSFIGURED': {'icon': '⚡', 'style': 'bold yellow'},
        'MODIFIED': {'icon': '⚡', 'style': 'bold yellow'},
        'MOVED': {'icon': '➡️', 'style': 'bold blue'},
        'DELETED': {'icon': '💀', 'style': 'strike red'},
        'SKIPPED': {'icon': '🛡️', 'style': 'dim white'},
        'ALREADY_MANIFEST': {'icon': '🛡️', 'style': 'dim white'},
        'UNKNOWN': {'icon': '❓', 'style': 'dim'}
    }

    SACRED_ORDER: Dict[str, int] = {
        'readme.md': 0,
        'architecture.md': 1,
        'package.json': 2,
        'pyproject.toml': 3,
        'cargo.toml': 4,
        'go.mod': 5,
        'dockerfile': 6,
        'makefile': 7
    }
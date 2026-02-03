# scaffold/symphony/renderers/rich_renderer/theme.py

from typing import Tuple, Dict


class GnosticTheme:
    """
    =============================================================================
    == THE GNOSTIC THEME (V-Ω-CYBER-AESTHETICS)                                ==
    =============================================================================
    The Visual Soul of the Renderer. Maps commands to Sigils and Colors.
    """

    # The Grimoire of Icons
    ICONS: Dict[str, str] = {
        'npm': '📦',
        'node': '⬢',
        'yarn': '🧶',
        'pnpm': '📦',
        'bun': '🥟',
        'python': '🐍',
        'pip': '🧪',
        'poetry': '📜',
        'docker': '🐳',
        'docker-compose': '🐙',
        'git': '🌲',
        'go': '🐹',
        'rustc': '🦀',
        'cargo': '📦',
        'terraform': '🏗️',
        'kubectl': '☸️',
        'aws': '☁️',
        'make': '🔨',
        'sh': '🐚',
        'bash': '🐚',
        'echo': '📢',
        'rm': '🔥',
        'mkdir': '📂',
        'touch': '📄',
        'scaffold': '🏗️',
        'default': '⚙️'
    }

    # The Palette of Power (Command Headers)
    STYLES: Dict[str, str] = {
        'npm': 'bold red',
        'node': 'bold green',
        'python': 'bold blue',
        'pip': 'bold yellow',
        'poetry': 'bold cyan',
        'docker': 'bold cyan',
        'git': 'dim white',
        'go': 'bold cyan',
        'rust': 'bold orange3',
        'terraform': 'bold magenta',
        'echo': 'bold white',
        'default': 'white'
    }

    # --- NEW: The Luminous Log Palette ---
    # These map to the regex groups in StreamScribe
    LOG_STYLES = {
        "log.success": "bold green",  # DONE, SUCCESS
        "log.warning": "bold yellow",  # WARN, WARNING
        "log.error": "bold red",  # ERR, ERROR, Failed
        "log.path": "cyan underline",  # /path/to/file.js
        "log.number": "bold magenta",  # 10ms, 5.2s, 100%
        "log.url": "blue underline",  # https://...
        "log.quote": "italic bright_white",  # "quoted strings"
        "log.bracket": "dim white",  # [text]
        "log.key": "cyan",  # key=
        "log.uuid": "orange3"  # a1b2...
    }

    # Spinner types for the Living Stream
    SPINNER_DEFAULT = 'dots'
    SPINNER_INSTALL = 'bouncingBar'
    SPINNER_BUILD = 'star'
    SPINNER_NETWORK = 'earth'
    SPINNER_WAIT = 'clock'

    @classmethod
    def get_icon_and_style(cls, command_text: str) -> Tuple[str, str]:
        """Divines the correct sigil and color for a command."""
        cmd_start = command_text.strip().split(' ')[0]
        # Handle "python -m" etc
        if cmd_start == "python" or cmd_start == "python3":
            return cls.ICONS['python'], cls.STYLES['python']

        icon = cls.ICONS.get(cmd_start, cls.ICONS['default'])
        style = cls.STYLES.get(cmd_start, cls.STYLES['default'])
        return icon, style

    @classmethod
    def get_spinner(cls, command_text: str) -> str:
        """Divines the appropriate animation for the wait."""
        cmd = command_text.lower()
        if "install" in cmd or "download" in cmd or "fetch" in cmd:
            return cls.SPINNER_INSTALL
        if "build" in cmd or "compile" in cmd or "transmute" in cmd:
            return cls.SPINNER_BUILD
        if "network" in cmd or "connect" in cmd or "ssh" in cmd:
            return cls.SPINNER_NETWORK
        if "wait" in cmd or "sleep" in cmd:
            return cls.SPINNER_WAIT
        return cls.SPINNER_DEFAULT
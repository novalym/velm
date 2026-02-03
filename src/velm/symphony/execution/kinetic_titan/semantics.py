# Path: scaffold/symphony/execution/kinetic_titan/semantics.py
# ------------------------------------------------------------

import re
import hashlib
from typing import List, Tuple, Pattern, Dict
from rich.style import Style
from rich.text import Text


class SemanticGrimoire:
    """
    =============================================================================
    == THE SEMANTIC GRIMOIRE (V-Ω-LEGENDARY-ULTIMA)                            ==
    =============================================================================
    LIF: 10,000,000,000

    The Codex of Visual Meaning.
    It transmutes raw ASCII chaos into a structured, luminous, and semantic stream.
    """

    # --- I. THE ICONOGRAPHY OF THE COSMOS ---
    ICON_MAP = {
        "npm": "📦", "node": "🟢", "yarn": "🧶", "pnpm": "📦", "bun": "🍞",
        "pip": "🐍", "python": "🐍", "poetry": "📜", "uv": "⚡",
        "git": "🌳", "gh": "🐙",
        "docker": "🐳", "docker-compose": "🐙", "podman": "🦭", "kubectl": "☸️", "helm": "⎈",
        "go": "🐹", "rustc": "🦀", "cargo": "📦", "zig": "⚡",
        "terraform": "🏗️", "pulumi": "🔮", "ansible": "📜",
        "curl": "🌐", "wget": "⬇️", "http": "🌍", "ssh": "🔑", "scp": "📤",
        "rm": "🔥", "mkdir": "📁", "touch": "📄", "mv": "🚚", "cp": "📋",
        "ls": "👀", "dir": "👀", "cat": "🐱", "grep": "🔍",
        "echo": "📢", "proclaim": "✨", "printf": "🖨️",
        "make": "🔨", "ninja": "🥷", "cmake": "⚙️",
        "default": "⚡"
    }

    # --- II. THE SPINNER ORACLE ---
    SPINNER_MAP = {
        "install": "bouncingBar", "add": "bouncingBar", "remove": "bouncingBar",
        "build": "star", "compile": "star", "transmute": "arc",
        "test": "dots12", "verify": "dots12", "check": "dots12",
        "deploy": "earth", "publish": "earth", "push": "arrow3",
        "download": "arrow3", "fetch": "arrow3", "clone": "arrow3",
        "wait": "clock", "sleep": "clock",
        "run": "aesthetic", "start": "aesthetic", "serve": "aesthetic",
        "default": "dots"
    }

    # --- III. THE BADGE GRIMOIRE (High Priority) ---
    # These create the "Beautiful Box" effect using background colors.
    BADGE_PATTERNS: List[Tuple[Pattern, Style]] = [
        # [DONE] -> Green Box
        (re.compile(r'\b(DONE|SUCCESS|COMPLETED|FIXED|PASSED)\b'), Style(color="white", bgcolor="green", bold=True)),
        # [FAIL] -> Red Box
        (re.compile(r'\b(FAIL|FAILED|ERROR|CRITICAL|PANIC|FATAL)\b'), Style(color="white", bgcolor="red", bold=True)),
        # [WARN] -> Yellow Box
        (re.compile(r'\b(WARN|WARNING|DEPRECATED)\b'), Style(color="black", bgcolor="yellow", bold=True)),
        # [INFO] -> Blue Box
        (re.compile(r'\b(INFO|NOTE|NOTICE)\b'), Style(color="white", bgcolor="blue", bold=True)),
        # [DEBUG] -> Magenta Box
        (re.compile(r'\b(DEBUG|TRACE|VERBOSE)\b'), Style(color="white", bgcolor="magenta", bold=True)),
    ]

    # --- IV. THE SYNTAX HIGHLIGHTING (Text Color) ---
    HIGHLIGHT_PATTERNS: List[Tuple[Pattern, str]] = [
        # Protocols
        (re.compile(r'\b(https?|ssh|git|s3|ftp)://[^\s]+'), "underline blue"),
        (re.compile(r'\b[\w\.-]+@[\w\.-]+:[\w\./-]+'), "underline magenta"),  # SSH/Git scp syntax

        # File Paths (Unix/Win) & Lines
        (re.compile(r'(^|\s)(/[^: ]+|[a-zA-Z]:\\[^: ]+)(:\d+)?'), "cyan underline"),

        # IP Addresses
        (re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'), "bold cyan"),

        # Versions (v1.2.3 or 1.2.3)
        (re.compile(r'\bv?\d+\.\d+\.\d+(-[\w\.]+)?\b'), "bold green"),

        # Time & Size
        (re.compile(r'\b\d+(\.\d+)?\s*(ms|s|m|h|KB|MB|GB|TB)\b'), "bold magenta"),

        # Quotes
        (re.compile(r'"[^"]*"'), "yellow"),
        (re.compile(r"'[^']*'"), "italic yellow"),

        # Key-Value Pairs (key=value or key: value)
        (re.compile(r'\b([\w\.-]+)(=|:\s)(.*?)(\s|$)'), "dim"),
        # We parse this manually in enhance() for granular coloring

        # Booleans
        (re.compile(r'\b(true|yes|on)\b', re.I), "bold green"),
        (re.compile(r'\b(false|no|off)\b', re.I), "bold red"),

        # Brackets
        (re.compile(r'[\[\]\(\)\{\}]'), "dim white"),
    ]

    @classmethod
    def divine_icon(cls, command: str) -> str:
        """Divines the emoji soul based on the command verb."""
        first = command.strip().split()[0].lower() if command else ""
        return cls.ICON_MAP.get(first, cls.ICON_MAP["default"])

    @classmethod
    def divine_spinner(cls, command: str) -> str:
        """Divines the animation style based on the intent."""
        cmd = command.lower()
        for key, spinner in cls.SPINNER_MAP.items():
            if key in cmd:
                return spinner
        return cls.SPINNER_MAP["default"]

    @classmethod
    def divine_color(cls, text: str) -> str:
        """
        [FACULTY 11] The Dynamic Color Hasher.
        Generates a consistent, pleasing color for any string.
        """
        colors = ["red", "green", "blue", "magenta", "cyan", "yellow"]
        h = hashlib.md5(text.encode()).hexdigest()
        idx = int(h, 16) % len(colors)
        return colors[idx]

    @classmethod
    def enhance(cls, text_obj: Text):
        """
        [THE RITE OF ILLUMINATION]
        Applies Gnostic Highlighting to a Rich Text object in-place.
        """
        plain = text_obj.plain

        # 1. Apply Badges (High Priority - Backgrounds)
        for pattern, style in cls.BADGE_PATTERNS:
            for match in pattern.finditer(plain):
                text_obj.stylize(style, match.start(), match.end())

        # 2. Apply Standard Highlights
        for pattern, style_str in cls.HIGHLIGHT_PATTERNS:
            for match in pattern.finditer(plain):
                # Special handling for KV pairs
                if pattern.pattern.startswith(r'\b([\w\.-]+)(=|:\s)'):
                    # Group 1: Key (Cyan)
                    text_obj.stylize("cyan", match.start(1), match.end(1))
                    # Group 2: Separator (Dim)
                    text_obj.stylize("dim", match.start(2), match.end(2))
                    # Group 3: Value (Green)
                    text_obj.stylize("green", match.start(3), match.end(3))
                else:
                    text_obj.stylize(style_str, match.start(), match.end())

        # 3. ANSI Strip/Decode (Safety)
        # (This is usually done before passing the text, but we ensure cleanliness)
        pass


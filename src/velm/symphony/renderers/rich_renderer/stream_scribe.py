# Path: scaffold/symphony/renderers/rich_renderer/stream_scribe.py
# ----------------------------------------------------------------
import re
import json
import time
import hashlib
from typing import Optional, Tuple, Any
from rich.console import Console, RenderableType
from rich.text import Text
from rich.style import Style
from rich.json import JSON
from rich.ansi import AnsiDecoder
from rich.padding import Padding
from rich.markup import escape
from .theme import GnosticTheme


class StreamScribe:
    """
    =================================================================================
    == THE WRITER OF THE SCROLL (V-Ω-OMNISCIENT-RENDERER)                          ==
    =================================================================================
    LIF: ∞ (THE EYES OF THE GOD-ENGINE)

    The Divine Scribe. It consumes raw output from the kinetic realm (subprocess),
    transmutes it through 12 layers of Gnostic processing, and inscribes it into
    the eternal stream as Luminous Truth.
    """

    # --- THE GRIMOIRE OF REGEX (THE ALL-SEEING EYE) ---

    # Matches ANSI OSC escape sequences used for setting window titles (Noise).
    TITLE_SEQUENCE_REGEX = re.compile(r'\x1b][0-2];.*?(?:\x07|\x1b\\)')

    # Matches high-entropy strings that look like secrets.
    SECRET_REGEX = re.compile(r'(api_key|token|secret|password|passwd|key)[\s=:"\']+(\S{8,})', re.IGNORECASE)

    # Matches "Key: Value" patterns for alignment.
    KV_REGEX = re.compile(r'^\s*([a-zA-Z0-9\-_]+):\s+(.*)$')

    # Matches Prompts.
    PROMPT_REGEX = re.compile(r'(\?|:|\[y/n\])\s*$', re.IGNORECASE)

    # The Palette of Meaning
    HIGHLIGHTS = [
        # Critical States
        (r'(?i)\b(critical dependency|fatal error|panic|crash|exception)\b', 'bold white on red'),
        (r'(?i)\b(fail|failed|failure|error|err|broken)\b', 'bold red'),

        # Warnings & Attention
        (r'(?i)\b(warn|warning|deprecated)\b', 'bold yellow'),

        # Success & Completion
        (r'(?i)\b(success|succeeded|done|finished|completed|ok|upheld|fixed)\b', 'bold green'),

        # HTTP Verbs
        (r'\b(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\b', 'bold magenta'),

        # File Paths (POSIX/Windows) with Line Numbers
        # Captures: path, line, col. e.g. /src/main.py:10:5
        (r'(?P<link_path>(?:[\.]{0,2}/|[a-zA-Z]:\\)[\w\.\-_/\\]+\.\w+)(?::(?P<line>\d+))?(?::(?P<col>\d+))?',
         'cyan underline'),

        # URLs
        (r'https?://\S+', 'blue underline'),

        # Metrics & Units
        (r'\b\d+(\.\d+)?(ms|s|m|KB|MB|GB|%)\b', 'bold magenta'),

        # Quotes & Brackets (Structure)
        (r"'.*?'|\".*?\"", 'italic bright_white'),
        (r'\[.*?\]', 'dim white'),

        # UUIDs / Hashes / IPs
        (r'\b[a-f0-9]{7,40}\b', 'orange3'),
        (r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', 'bold blue'),
    ]

    def __init__(self, console: Console):
        self.console = console
        self.decoder = AnsiDecoder()
        self.width = console.size.width

        # State Tracking for The Mood Engine
        self.highest_severity = 0  # 0: Info, 1: Success, 2: Warning, 3: Error
        self.last_line_time = time.time()

        # Pre-compiled styles for performance
        self.border_style = Style(color="bright_black", dim=True)

    def _hash_secret(self, secret: str) -> str:
        """[FACULTY 3] The Deterministic Secret Hasher."""
        # We show the first 4 chars of the sha256 hash to allow tracing without revealing.
        h = hashlib.sha256(secret.encode()).hexdigest()[:4]
        return f"[SECRET:{h}]"

    def _sanitize_and_transmute(self, text: str) -> str:
        """
        Purifies the raw text of terminal control sequences and secrets.
        """
        # 1. Annihilate Window Title sequences
        text = self.TITLE_SEQUENCE_REGEX.sub('', text)

        # 2. Transmute Secrets (The Hasher)
        def replace_secret(match):
            key = match.group(1)
            secret = match.group(2)
            return f"{key} {self._hash_secret(secret)}"

        text = self.SECRET_REGEX.sub(replace_secret, text)
        return text

    def _apply_gnostic_highlights(self, text_obj: Text):
        """
        [FACULTY 9] Layers Gnostic semantic meaning onto the text.
        """
        text_str = text_obj.plain

        # 1. Regex Highlights
        for pattern, style in self.HIGHLIGHTS:
            # We iterate matches to handle complex groups (like links)
            for match in re.finditer(pattern, text_str):
                # If it's a file link, we forge the Hyperlink
                if 'link_path' in match.groupdict() and match.group('link_path'):
                    path = match.group('link_path')
                    line = match.group('line') or "1"
                    col = match.group('col') or "1"
                    # VS Code / Modern Terminal Link Format
                    url = f"file://{path}"  # Simplified, ideally needs absolute path resolution
                    text_obj.stylize(style, match.start(), match.end())
                    # Note: Rich Text doesn't support adding hyperlinks via regex easily in one pass
                    # without complex span manipulation, so we stick to visual styling for now.
                else:
                    text_obj.stylize(style, match.start(), match.end())

        # 2. [FACULTY 6] Markdown Projection
        # Detect backticks `code`
        for match in re.finditer(r'`([^`]+)`', text_str):
            text_obj.stylize("bold white on black", match.start(), match.end())

    def _render_rich_content(self, text: str) -> RenderableType:
        """
        [FACULTY 1] The JSON Diviner & [FACULTY 10] Markdown Projector.
        Decides if the line is complex data or simple text.
        """
        stripped = text.strip()

        # Try JSON
        if (stripped.startswith('{') and stripped.endswith('}')) or \
                (stripped.startswith('[') and stripped.endswith(']')):
            try:
                # We ensure it's valid JSON
                json.loads(stripped)
                return JSON(stripped)
            except ValueError:
                pass

        # Return Text object
        return None

    def print_header(self, command: str):
        """
        Inscribes the Luminous Header.
        ╭── 📦 command ───...
        """
        self.highest_severity = 0  # Reset mood
        self.last_line_time = time.time()

        max_len = self.width - 10
        display_cmd = command if len(command) < max_len else command[:max_len - 3] + "..."
        icon, style_name = GnosticTheme.get_icon_and_style(command)

        prefix = "╭── "
        # Calculate suffix length to fill the line
        suffix_len = max(0, self.width - len(prefix) - len(display_cmd) - 3 - 2)
        suffix = " " + ("─" * suffix_len)

        header_text = Text.assemble(
            (prefix, self.border_style),
            (f"{icon} ", "default"),
            (f"{display_cmd}", "bold white"),
            (suffix, self.border_style)
        )
        self.console.print(header_text)

    def print_log(self, content: str):
        """
        [THE CORE RITE]
        Inscribes a line of the process output.
        """
        clean_content = self._sanitize_and_transmute(content)

        # Update Mood Engine
        lower_content = clean_content.lower()
        if "error" in lower_content or "fail" in lower_content:
            self.highest_severity = 3
        elif "warn" in lower_content:
            self.highest_severity = max(self.highest_severity, 2)

        # [FACULTY 4] Chronometric Delta
        now = time.time()
        delta = now - self.last_line_time
        self.last_line_time = now
        delta_str = f"+{delta:.2f}s" if delta > 0.01 else ""
        delta_style = "dim" if delta < 1.0 else "bold yellow" if delta < 5.0 else "bold red"

        # Check for Rich Content (JSON)
        rich_renderable = self._render_rich_content(clean_content)

        if rich_renderable:
            # If JSON, we render it inside a padded block
            self.console.print(Text("│  ", style=self.border_style), end="")
            self.console.print(rich_renderable)
            return

        # Decode ANSI (Faculty 8)
        text_obj = self.decoder.decode_line(clean_content.rstrip('\n'))

        # [FACULTY 5] Key-Value Alchemy
        # If line matches "Key: Value", bold the key
        kv_match = self.KV_REGEX.match(text_obj.plain)
        if kv_match:
            key_span = kv_match.span(1)
            text_obj.stylize("bold cyan", key_span[0], key_span[1])

        # [FACULTY 7] Interactive Sentinel
        if self.PROMPT_REGEX.search(text_obj.plain):
            text_obj.stylize("bold yellow blink")

        # Apply Gnostic Highlights
        self._apply_gnostic_highlights(text_obj)

        # Assemble final line with Border and Delta
        final_line = Text.assemble(
            ("│  ", self.border_style),
            text_obj,
            (" " * max(1, self.width - len("│  ") - len(text_obj) - len(delta_str) - 1), ""),
            (delta_str, delta_style)
        )

        self.console.print(final_line)

    def print_footer(self, success: bool, duration: float):
        """
        [FACULTY 10] The Mood Engine determines the footer color.
        """
        # Determine final mood
        if not success:
            self.highest_severity = 3
        elif self.highest_severity == 0:
            self.highest_severity = 1  # Success if no errors seen

        mood_styles = {
            0: "dim",  # Info only
            1: "bold green",  # Success
            2: "bold yellow",  # Warnings
            3: "bold red"  # Errors
        }
        mood_style = mood_styles.get(self.highest_severity, "dim")

        status_icon = "✔" if success else "✘"
        status_text = "Done" if success else "Failed"

        prefix = "╰──── "

        footer_text = Text.assemble(
            (prefix, self.border_style),
            (f"{status_icon} {status_text}", mood_style),
            (f" ({duration:.2f}s)", "dim")
        )
        self.console.print(footer_text)

    def print_vow(self, message: str, success: bool):
        """Inscribes a Vow Adjudication."""
        icon = "✔" if success else "✘"
        style = "bold green" if success else "bold red"

        # Vows break the vertical line to stand out
        self.console.print(Text.assemble(
            ("├─ ", self.border_style),
            (f"{icon} ", style),
            (message, "white")
        ))

    def print_state(self, key: str, value: str):
        """Inscribes a Metaphysical State Change."""
        self.console.print(Text.assemble(
            ("│  ", self.border_style),
            ("⚡ ", "yellow"),
            ("State: ", "dim"),
            (key, "cyan"),
            (" = ", "dim"),
            (value, "bold white")
        ))

    def print_system_message(self, message: str, style: str = "dim italic white"):
        """Inscribes a meta-message from the Engine."""
        self.console.print(Text.assemble(
            ("│  ", self.border_style),
            (f"[{message}]", style)
        ))
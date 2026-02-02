# Path: scaffold/symphony/execution/kinetic_titan/titan/visuals.py
# ----------------------------------------------------------------

import re
from rich.style import Style
from rich.text import Text
from rich.ansi import AnsiDecoder
from ..security import StreamSentinel


class VisualCortex:
    """
    =============================================================================
    == THE PRISMATIC VISUAL CORTEX (V-Ω-REGEX-STYLER)                          ==
    =============================================================================
    LIF: 10,000,000,000

    The artistic soul of the Titan. It holds the Grimoires of Style and performs
    the transmutation of raw strings into luminous Rich Text.
    """

    _DECODER = AnsiDecoder()

    # --- THE BADGE GRIMOIRE ---
    BADGE_MAP = [
        (re.compile(r'\b(DONE|SUCCESS|COMPLETED|FINISHED|UPHELD|PURE|OK)\b', re.IGNORECASE),
         Style(color="white", bgcolor="green", bold=True)),
        (re.compile(r'\b(WARNING|WARN|DEPRECATED|SKIPPED)\b', re.IGNORECASE),
         Style(color="black", bgcolor="yellow", bold=True)),
        (re.compile(r'\b(INFO|NOTE|NOTICE|PROCLAIM|VERSION)\b', re.IGNORECASE),
         Style(color="white", bgcolor="blue", bold=True)),
        (re.compile(r'\b(CRITICAL|FATAL|PANIC|CATASTROPHE|EMERGENCY)\b', re.IGNORECASE),
         Style(color="white", bgcolor="red", blink=True, bold=True)),
        (re.compile(r'\b(ERROR|FAIL|FAILED|FAILURE|HERESY|BROKEN|EXCEPTION)\b', re.IGNORECASE),
         Style(color="white", bgcolor="red", bold=True)),
    ]

    # --- THE HIGHLIGHT GRIMOIRE ---
    SEMANTIC_HIGHLIGHTS = [
        (re.compile(r'(https?://[^\s`\'"]+)'), "underline blue"),
        (re.compile(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b'), "bold cyan"),
        (re.compile(r'"[^"]*"'), "italic green"),
        (re.compile(r"'[^']*'"), "italic green"),
        (re.compile(r'\b\d+(\.\d+)?\s*(ms|s|m|KB|MB|GB|%)\b'), "bold magenta"),
        (re.compile(r'\[\d+/\d+\]'), "bold cyan"),
        (re.compile(r'\b[a-f0-9]{7,40}\b'), "orange3")
    ]

    @classmethod
    def transmute(cls, raw_line: str, stream_type: str) -> Text:
        """Transmutes a raw string into a Badge-Enriched Rich Text object."""
        # 1. Redact Secrets
        clean_text = StreamSentinel.redact(raw_line)

        # 2. Decode ANSI
        text_obj = cls._DECODER.decode_line(clean_text)

        # 3. Apply Error Tint
        if stream_type == "stderr":
            text_obj.stylize("bold red")

        # 4. Apply Badge Styles
        plain = text_obj.plain
        for pattern, style in cls.BADGE_MAP:
            for match in pattern.finditer(plain):
                text_obj.stylize(style, match.start(), match.end())

        # 5. Apply Semantic Highlights
        for pattern, style_str in cls.SEMANTIC_HIGHLIGHTS:
            for match in pattern.finditer(plain):
                text_obj.stylize(style_str, match.start(), match.end())

        return text_obj
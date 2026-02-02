# Path: scaffold/rendering/text_renderer/content_previewer.py
# -----------------------------------------------------------
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from rich.rule import Rule

from .config import RendererConfig
from ...contracts.data_contracts import ScaffoldItem


class ContentPreviewer:
    """
    [EVOLUTION 4] The Inline Soul Renderer.
    Responsible for rendering syntax-highlighted previews of file content
    inline within the terminal output.
    """

    def __init__(self, config: RendererConfig):
        self.config = config

    def render_soul(self, item: ScaffoldItem, path_str: str) -> Panel:
        """Forges a luminous panel for the file's soul."""
        if not item.content:
            return Panel("Void", title="Empty Soul")

        file_suffix = item.path.suffix.lstrip('.') if item.path else "text"

        # Use 'text' fallback if suffix is empty
        lexer = file_suffix if file_suffix else "text"

        soul_syntax = Syntax(
            item.content,
            lexer,
            theme="monokai",
            line_numbers=True,
            word_wrap=True
        )

        return Panel(
            soul_syntax,
            title=Text.from_markup(
                f"Soul for: [{self.config.theme.file_color}]📄 {path_str}[/{self.config.theme.file_color}]"),
            border_style="dim green",
            padding=(1, 2)
        )

    def get_separator(self) -> Rule:
        return Rule("[bold green]Chronicle of Inlined Souls[/bold green]", style="green")
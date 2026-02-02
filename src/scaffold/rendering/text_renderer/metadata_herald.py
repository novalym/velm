# Path: scaffold/rendering/text_renderer/metadata_herald.py
# ---------------------------------------------------------
from rich.text import Text
from pathlib import Path

from .config import RendererConfig
from .telemetry import RenderTelemetry
from ...contracts.data_contracts import _GnosticNode
from ...constants import SECRET_FILENAMES
from ...utils import is_binary


class MetadataHerald:
    """
    [EVOLUTION 5] The Metadata Herald.
    Generates the aligned metadata string (the Gnosis displayed to the right of the tree nodes).
    Handles complexity heatmaps, permissions, and origin sigils.
    """

    def __init__(self, config: RendererConfig, telemetry: RenderTelemetry):
        self.config = config
        self.telemetry = telemetry
        self.theme = config.theme

    def forge_gnosis_text(self, child: _GnosticNode) -> Text:
        # [PURE STRUCTURE PROTOCOL]
        # If pure, the herald is silent.
        if self.config.pure_structure:
            return Text()

        gnosis_text = Text()
        if not child.item: return gnosis_text

        item = child.item

        # --- Origin Sigils ---
        origin_type = 'Forge'
        if item.name in SECRET_FILENAMES:
            origin_type = 'Secret'
        elif item.content:
            origin_type = 'Block' if '\n' in item.content.strip() else 'Inline'
        elif item.seed_path:
            origin_type = 'Seed'
        elif item.path and is_binary(item.path):  # Use utility check
            origin_type = 'Binary'

        sigil_map = {
            'Secret': (self.theme.secret_soul_sigil, self.theme.secret_color),
            'Binary': (self.theme.binary_soul_sigil, self.theme.binary_color),
            'Inline': (self.theme.inline_soul_sigil, self.theme.forge_color),
            'Block': (self.theme.inline_soul_sigil, self.theme.forge_color),
            'Seed': (self.theme.seed_soul_sigil, self.theme.link_color),
            'Forge': (self.theme.forge_soul_sigil, self.theme.forge_color)
        }

        # Fallback for unknown types
        sigil, color = sigil_map.get(origin_type, ('?', 'dim white'))

        gnosis_text.append(f" {sigil} {origin_type}", style=color)
        separator = Text(" | ", style="dim")

        # --- Facts & Complexity ---
        if child.complexity:
            heat = child.complexity.get('heat_level', 'Low')
            color = self.theme.heat_colors.get(heat, "white")
            gnosis_text.append(separator)
            gnosis_text.append(f"CC:{child.complexity.get('cyclomatic_complexity', 1)}", style=color)

            if heat in ("Critical", "High"):
                gnosis_text.append(f" {self.theme.warning_sigil}", style="bold red")
                self.telemetry.record_warning()

        # --- Permissions ---
        if item.permissions:
            gnosis_text.append(separator)
            gnosis_text.append(f"🛡️ {item.permissions}", style=self.theme.permission_color)

        # --- Inline Preview (Single Line) ---
        if origin_type == 'Inline' and item.content:
            gnosis_text.append(separator)
            # Sanitize for display
            preview = item.content.strip().replace('\n', ' ')[:30]
            # Escape markup in content to prevent rendering errors
            from rich.markup import escape
            gnosis_text.append(f"\"{escape(preview)}...\"", style="dim italic")

        return gnosis_text
# Path: scaffold/rendering/text_renderer/tree_weaver.py
# -----------------------------------------------------
from typing import List, Tuple, Any
from rich.text import Text
from rich.style import Style
from rich.markup import escape

from .config import RendererConfig
from .telemetry import RenderTelemetry
from .metadata_herald import MetadataHerald
from ...contracts.data_contracts import _GnosticNode, GnosticLineType


class TreeWeaver:
    """
    [EVOLUTION 3] The Luminous Tree Builder.
    Recursively builds the visual tree lines (Rich Text objects) representing the structure.
    """

    def __init__(self, config: RendererConfig, telemetry: RenderTelemetry):
        self.config = config
        self.telemetry = telemetry
        self.herald = MetadataHerald(config, telemetry)

    def weave(self, node: _GnosticNode, connector_state: Tuple[bool, ...], target_list: List[Any]):
        """
        Recursive weave function.
        """
        # Filter: The Gaze of Reality
        if self.config.pure_structure:
            if node.item and node.item.line_type != GnosticLineType.FORM:
                return

        # Sort: Logic similar to BlueprintScribe for consistency
        sorted_children = sorted(
            node.children,
            key=lambda n: (0 if n.is_dir else 1, 0 if n.name.startswith('.') else 1, n.name.lower())
        )

        if self.config.pure_structure:
            sorted_children = [
                c for c in sorted_children
                if c.item and c.item.line_type == GnosticLineType.FORM
            ]

        current_line_text = Text()
        connector_style = Style(dim=True)

        # Node Type Gnosis
        is_logic_node = node.item and node.item.line_type == GnosticLineType.JINJA_CONSTRUCT
        is_variable_node = node.item and node.item.line_type == GnosticLineType.VARIABLE

        # 1. Indentation
        pipe_char = '│'
        for is_last_ancestor in connector_state:
            if is_last_ancestor:
                current_line_text.append("    ")
            else:
                current_line_text.append(pipe_char, style=connector_style)
                current_line_text.append("   ")

        # 2. Connector
        connector_char = '└── ' if not sorted_children else '├── '
        current_line_text.append(connector_char, style=connector_style)

        # 3. Icons & Colors (The Bifurcation)
        if self.config.pure_structure:
            path_style = "bold blue" if node.is_dir else "default"
            display_name = escape(node.name)
            if node.is_dir: display_name += "/"
            current_line_text.append(display_name, style=path_style)
        else:
            path_color = self.config.theme.directory_color
            path_icon = self.config.theme.dir_icon

            if is_logic_node:
                path_color = "bold magenta"
                path_icon = "λ" if node.name.lower().startswith('@if') else "§"
            elif is_variable_node:
                path_color = "bold yellow"
                path_icon = "🔩"
            elif not node.is_dir:
                path_color = self.config.theme.file_color
                path_icon = self.config.theme.file_icon

            node_name_text = Text(escape(node.name), style=path_color)

            # Dynamic Styling (Lint/Git)
            if node.item:
                # Heresy Highlight
                if self.config.app_state and hasattr(self.config.app_state,
                                                     'lint_cache') and self.config.app_state.lint_cache:
                    lint_dossier = self.config.app_state.lint_cache.get(node.item.content_hash)
                    if lint_dossier and lint_dossier.get('heresies'):
                        node_name_text.stylize(Style(color="red", bold=True))
                        path_icon = "❌"
                        self.telemetry.record_error()

                # Git Status
                if node.item.git_status and node.item.git_status in self.config.theme.git_sigil_grimoire:
                    current_line_text.append(self.config.theme.git_sigil_grimoire[node.item.git_status])
                    current_line_text.append(" ")

            current_line_text.append(f"{path_icon} ")
            current_line_text.append(node_name_text)
            current_line_text.append('/' if node.is_dir else '')

            # 4. Aligned Gnosis (Metadata)
            gnosis_text = self.herald.forge_gnosis_text(node)

            # Visual Alignment Logic
            max_path_len = 50
            path_segment_length = len(str(current_line_text.plain.strip()))
            if gnosis_text:
                padding_needed = max_path_len - path_segment_length + 2
                if padding_needed > 0:
                    current_line_text.append(" " * padding_needed)
                current_line_text.append(gnosis_text)

        target_list.append(current_line_text)

        # [EVOLUTION 11] Recursive Limit Ward (Implicit via recursion, can add depth check)
        for i, child in enumerate(sorted_children):
            self.weave(
                child,
                connector_state + (i == len(sorted_children) - 1,),
                target_list
            )
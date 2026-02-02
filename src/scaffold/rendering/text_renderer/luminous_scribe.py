# Path: scaffold/rendering/text_renderer/luminous_scribe.py
# ---------------------------------------------------------
from typing import List, Tuple, Any
from rich.console import Group as RenderableGroup
from rich.panel import Panel

from .config import RendererConfig
from .telemetry import RenderTelemetry
from .tree_weaver import TreeWeaver
from .content_previewer import ContentPreviewer
from .diagnostic_scribe import DiagnosticScribe
from ...contracts.data_contracts import _GnosticNode, ScaffoldItem


class LuminousScribe:
    """
    [EVOLUTION 12] The Luminous Scribe.
    Orchestrates the rich rendering process using the sub-artisans.
    """

    def __init__(self, root: _GnosticNode, config: RendererConfig):
        self.root = root
        self.config = config
        self.telemetry = RenderTelemetry()

        self.tree_weaver = TreeWeaver(config, self.telemetry)
        self.content_previewer = ContentPreviewer(config)
        self.diagnostic_scribe = DiagnosticScribe(config)

        self.renderables: List[Any] = []
        self.inlined_souls: List[Tuple[ScaffoldItem, str]] = []

    def transcribe(self) -> List[Any]:
        """The Grand Rite of Visual Proclamation."""
        self.renderables = []
        self.inlined_souls = []

        if self.config.verbose and not self.config.pure_structure:
            self._proclaim_full_diagnostic_dossier()
        else:
            self._proclaim_structural_scripture()

        return self.renderables

    def _proclaim_full_diagnostic_dossier(self):
        # 1. Context
        vars_table = self.diagnostic_scribe.forge_context_table()

        # 2. Tree
        tree_renderables = []
        # Delegate root handling: Iterate children of ROOT
        for child in sorted(self.root.children, key=lambda n: (0 if n.is_dir else 1, n.name.lower())):
            self.tree_weaver.weave(child, tuple(), target_list=tree_renderables)
            self._capture_inline_souls(child)

        tree_panel = Panel(
            RenderableGroup(*tree_renderables),
            title="[bold green]II. The Gnostic Tree of Form[/bold green]",
            border_style="green"
        )

        # 3. Commands
        will_table = self.diagnostic_scribe.forge_maestro_scroll()

        # 4. Assembly
        final_view = RenderableGroup(vars_table, tree_panel, will_table)
        self.renderables.append(
            Panel(final_view, title="[bold]Dossier of Gnostic Perception (Hyper-Diagnostic)[/bold]",
                  border_style="white")
        )

    def _proclaim_structural_scripture(self):
        # 1. Tree
        for child in sorted(self.root.children, key=lambda n: (0 if n.is_dir else 1, n.name.lower())):
            self.tree_weaver.weave(child, tuple(), target_list=self.renderables)
            # Capture inlined souls for later
            self._capture_inline_souls(child)

        # 2. Content Previews (if luminous and not pure)
        if not self.config.pure_structure and self.inlined_souls:
            self.renderables.append(self.content_previewer.get_separator())
            for item, path_str in self.inlined_souls:
                panel = self.content_previewer.render_soul(item, path_str)
                self.renderables.append(panel)

    def _capture_inline_souls(self, node: _GnosticNode):
        """Recursively collects inline content for rendering."""
        if not self.config.pure_structure and node.item and node.item.content and '\n' in node.item.content.strip():
            # Build full path name for display
            self.inlined_souls.append((node.item, node.name))
        for child in node.children:
            self._capture_inline_souls(child)
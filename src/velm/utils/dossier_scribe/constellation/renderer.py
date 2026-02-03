# Path: scaffold/utils/dossier_scribe/constellation/renderer.py
# -------------------------------------------------------------

from pathlib import Path
from typing import Dict, Any, Union, List
from rich.tree import Tree
from rich.text import Text
from rich.filesize import decimal
from rich.style import Style

# --- THE DIVINE SUMMONS ---
from ....interfaces.base import Artifact
from .assets import GnosticAssets
from .hyperlinks import HyperlinkNexus
from .xray import GnosticXRay

# [ASCENSION] The Inquisitors
from ....creator.io_validators import SyntaxInquisitor
from ....creator.writer.security import SecretSentinel


class ConstellationRenderer:
    """
    =================================================================================
    == THE LUMINOUS RENDERER (V-Ω-FORENSIC-ENABLED)                                ==
    =================================================================================
    Builds the Rich Tree structure.
    Now endowed with the Forensic Overlay (Deltas) and Heresy Overlay (Validation).
    """

    def __init__(self, project_root: Path, nexus: HyperlinkNexus):
        self.root = project_root
        self.nexus = nexus

    def render(self, soul_map: Dict[str, Any], artifacts: List[Artifact]) -> Tree:
        # --- THE ROOT PORTAL ---
        root_name = self.root.name
        root_style = self.nexus.get_style(self.root, "bold cyan", intent="ACTIVATE")

        root_text = Text()
        root_text.append(f"📂 ", style="default")
        root_text.append(f"{root_name}", style=root_style)
        root_text.append(f"  {self.root}", style="dim")

        tree = Tree(root_text, guide_style="dim")

        if not artifacts:
            return tree

        self._weave_branches(tree, soul_map, self.root)
        self._append_footer(tree, artifacts)

        return tree

    def _weave_branches(self, tree_node: Tree, soul_map: Dict[str, Any], current_phys_path: Path):
        items = sorted(soul_map.items(), key=lambda item: (
            not isinstance(item[1], dict),
            GnosticAssets.SACRED_ORDER.get(item[0].lower(), 999),
            item[0].lower()
        ))

        for name, soul in items:
            child_path = current_phys_path / name
            self._render_single_node(tree_node, name, soul, child_path)

    def _render_single_node(self, tree_node: Tree, name: str, soul: Union[Dict, Artifact], parent_path: Path):
        """Renders a single node with Deep Gnosis."""
        label = Text()

        if isinstance(soul, dict):
            # --- DIRECTORY ---
            icon = GnosticAssets.ICON_MAP['dir']
            style = self.nexus.get_style(parent_path, "bold cyan")

            label.append(f"{icon} ")
            label.append(name, style=style)

            branch = tree_node.add(label)
            self._weave_branches(branch, soul, parent_path)
        else:
            # --- FILE ---
            artifact = soul
            action_meta = GnosticAssets.ACTION_MAP.get(artifact.action, GnosticAssets.ACTION_MAP['UNKNOWN'])

            ext = parent_path.suffix.lower()
            icon = GnosticAssets.ICON_MAP.get(name.lower(),
                                              GnosticAssets.ICON_MAP.get(ext, GnosticAssets.ICON_MAP['file']))

            # Base Label
            label.append(f"{action_meta['icon']} ", style="bold")
            label.append(f"{icon} ")
            name_style = self.nexus.get_style(parent_path, action_meta['style'])
            label.append(name, style=name_style)

            # [ASCENSION 2] The Forensic Overlay (Delta Metrics)
            if artifact.metadata and 'diff_summary' in artifact.metadata:
                # e.g. (+12/-4)
                diff_stats = artifact.metadata['diff_summary']
                label.append(f" {diff_stats}", style="italic cyan")

            # Metadata: Size
            if artifact.size_bytes > 0:
                label.append(f" ({decimal(artifact.size_bytes)})", style="dim")

            # [ASCENSION 3] The Heresy Overlay (Inline Validation)
            # We only perform this gaze on created/modified files that exist
            if parent_path.exists() and parent_path.is_file() and artifact.action in ("CREATED", "TRANSFIGURED",
                                                                                      "MODIFIED"):
                try:
                    # We read the first 8KB for a quick scan
                    content_head = parent_path.read_text(encoding='utf-8', errors='ignore')

                    # A. Secret Sentinel
                    # Use filename for context
                    secrets = SecretSentinel.scan(content_head, name)
                    if secrets:
                        label.append(f" 💀 LEAK", style="bold red reverse")

                    # B. Syntax Inquisitor
                    # Check the whole file for syntax if it's code
                    if ext in ['.py', '.json', '.yaml', '.toml']:
                        content_full = parent_path.read_text(encoding='utf-8', errors='ignore')
                        is_pure, error = SyntaxInquisitor.adjudicate(content_full, ext)
                        if not is_pure:
                            label.append(f" ⚠️ SYNTAX", style="bold yellow reverse")
                except Exception:
                    pass

            # [LEGACY] Semantic X-Ray (if space allows and no heresy)
            if parent_path.exists() and not label.plain.endswith("LEAK") and not label.plain.endswith("SYNTAX"):
                xray_gnosis = GnosticXRay.scan(parent_path)
                if xray_gnosis:
                    label.append(f"  {xray_gnosis}", style="italic dim cyan")

            tree_node.add(label)

    def _append_footer(self, tree: Tree, artifacts: List[Artifact]):
        """[THE WORKSPACE BEACON]"""
        count = len(artifacts)
        if count > 0:
            tree.add(Text(f"Delta: +{count}", style="bold green italic"))

        workspace_file = next(self.root.glob("*.code-workspace"), None)
        hint_text = Text("\nActivation Command:", style="dim")
        cmd_style = Style(color="white", bgcolor="black", bold=True)

        if workspace_file:
            cmd = f"code {workspace_file.name}"
            target_path = workspace_file
        else:
            cmd = f"code {self.root.name}"
            target_path = self.root

        hint_text.append(f"  $ {cmd}  ", style=cmd_style)

        activation_style = self.nexus.get_style(
            target_path,
            style_def="bright_cyan bold",
            intent="ACTIVATE"
        )
        hint_text.append(" (Ctrl+Click to Open Project)", style=activation_style)

        tree.add(hint_text)
# Path: scaffold/utils/dossier_scribe/constellation/scribe.py
# ---------------------------------------------------------

from pathlib import Path
from typing import List, Optional, Dict, Any

from rich.tree import Tree
from ....interfaces.base import Artifact

# --- THE DIVINE SUMMONS ---
from .hyperlinks import HyperlinkNexus
from .renderer import ConstellationRenderer
from .arch_scribe import ArchitectureScribe
from .crystal import CrystalMemory


class ConstellationScribe:
    """
    =================================================================================
    == THE GNOSTIC ORRERY (V-Ω-MODULAR-FACADE-ASCENDED)                            ==
    =================================================================================
    The High Priest of Visualization.
    Orchestrates Visuals, Documentation, and now, Deterministic Verification.
    """

    def __init__(
            self,
            artifacts: Optional[List[Artifact]],
            project_root: Path,
            generate_arch_doc: bool = True,
            snapshot_path: Optional[Path] = None
    ):
        self.artifacts = artifacts or []
        self.project_root = project_root.resolve()
        self.generate_arch_doc = generate_arch_doc
        self.snapshot_path = snapshot_path

        # Forge the Pantheon
        self.nexus = HyperlinkNexus()
        self.renderer = ConstellationRenderer(self.project_root, self.nexus)

    def forge(self) -> Tree:
        """The Grand Rite."""
        # 1. Weave the Visual Tree
        soul_map = self._build_nested_soul_map()
        tree = self.renderer.render(soul_map, self.artifacts)

        # 2. The Cartographer's Covenant (Documentation)
        if self.generate_arch_doc and self.artifacts:
            ArchitectureScribe.inscribe(tree, self.project_root, self.artifacts)

        # 3. [ASCENSION 1] The Crystal Memory (Deterministic Snapshot)
        if self.snapshot_path:
            self._forge_crystal_memory()

        return tree

    def _forge_crystal_memory(self):
        """Freezes the current reality into a JSON artifact for testing."""
        from ....logger import Scribe as LoggerScribe
        logger = LoggerScribe("ConstellationScribe")

        try:
            content = CrystalMemory.crystallize(self.project_root, self.artifacts)
            # Ensure the path is absolute or relative to CWD, not project root (usually passed from CLI)
            target = self.snapshot_path.resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
            logger.info(f"Crystal Memory inscribed at [cyan]{target.name}[/cyan] (Test Artifact).")
        except Exception as e:
            logger.warn(f"Failed to forge Crystal Memory: {e}")

    def _safe_relative_to(self, target: Path, base: Path) -> Path:
        """The Relativity Healer."""
        try:
            return target.relative_to(base)
        except ValueError:
            import os
            if os.name == 'nt':
                t_str = str(target.resolve()).lower()
                b_str = str(base.resolve()).lower()
                if t_str.startswith(b_str):
                    rel_str = t_str[len(b_str):].lstrip(os.sep)
                    return Path(rel_str)
            return Path(target.name)

    def _build_nested_soul_map(self) -> Dict[str, Any]:
        """Transmutes the flat artifact list into a hierarchical soul map."""
        soul_map = {}

        for artifact in self.artifacts:
            try:
                rel_path = self._safe_relative_to(artifact.path.resolve(), self.project_root)
                parts = rel_path.parts
            except ValueError:
                parts = (artifact.path.name,)

            current_level = soul_map
            for part in parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
                if not isinstance(current_level, dict):
                    current_level = {}

            current_level[parts[-1]] = artifact

        return soul_map
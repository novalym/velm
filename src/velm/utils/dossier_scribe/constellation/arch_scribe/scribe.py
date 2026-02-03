# Path: scaffold/utils/dossier_scribe/constellation/arch_scribe/scribe.py
# -----------------------------------------------------------------------

import os
import re
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.tree import Tree

from .....utils import atomic_write
from .....logger import Scribe
from .....interfaces.base import Artifact
from .dna import ProjectDNA
from .markdown import MarkdownForge

Logger = Scribe("ArchScribe")


class ArchitectureScribe:
    """
    =================================================================================
    == THE CARTOGRAPHER'S COVENANT (V-Ω-PURIFIED-EDITION)                          ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    The Sovereign Conductor. It orchestrates the DNA Sequencer, the Graph Weaver,
    and the Markdown Forge to produce the Masterwork.

    [ASCENSION]: Now wields the 'Textual Exorcist' to cleanse the visual tree of
    terminal-specific artifacts before inscription.
    """

    FILENAME = "ARCHITECTURE.md"

    @staticmethod
    def inscribe(tree: Tree, project_root: Path, artifacts: List[Artifact]):
        """
        Captures the visual soul and deep Gnosis of the project.
        """
        try:
            # 1. Capture Visual Tree (The Silent Rite)
            # We enforce UTF-8 to prevent the Curse of the Charmap on Windows.
            with open(os.devnull, "w", encoding="utf-8") as void:
                console = Console(file=void, width=100, record=True, no_color=True)
                console.print(tree)
                raw_tree_text = console.export_text()

            # 2. The Rite of Purification (The Exorcism)
            # We strip the ephemeral UI artifacts to leave only the eternal structure.
            tree_text = ArchitectureScribe._purify_tree_text(raw_tree_text)

            # 3. Sequence the Genome (The Deep Gaze)
            dna = ProjectDNA(project_root, artifacts)

            # 4. Forge the Scripture (The Proclamation)
            content = MarkdownForge.forge_document(project_root.name, dna, tree_text)

            # 5. Atomic Inscription
            target = project_root / ArchitectureScribe.FILENAME
            atomic_write(target, content, Logger, project_root, verbose=False)

            Logger.info(f"Updated architectural masterwork at [cyan]{ArchitectureScribe.FILENAME}[/cyan]")

        except Exception as e:
            Logger.warn(f"Failed to inscribe Architecture map: {e}")

    @staticmethod
    def _purify_tree_text(raw_text: str) -> str:
        """
        [THE TEXTUAL EXORCIST]
        Cleanses the tree of ephemeral artifacts (absolute paths, UI hints)
        to forge a timeless static representation.
        """
        lines = raw_text.splitlines()
        clean_lines = []

        for i, line in enumerate(lines):
            # 1. Purify Root (First Line)
            # The root line often contains the absolute path (e.g., "📂 name  C:\path").
            # We strip everything after the double space separator.
            if i == 0:
                # Regex matches 2+ spaces followed by a path indicator (/ or Drive:)
                line = re.sub(r'\s{2,}(?:/|[a-zA-Z]:[\\/]).*$', '', line)

            # 2. Filter Footer Artifacts (The UI Noise)
            # We remove lines that are purely instructions for the interactive terminal.
            if "Activation Command:" in line: continue
            if "(Ctrl+Click" in line: continue
            if line.strip().startswith("$ code"): continue

            clean_lines.append(line)

        # Remove trailing empty lines that might result from filtering
        result = "\n".join(clean_lines).strip()
        return result
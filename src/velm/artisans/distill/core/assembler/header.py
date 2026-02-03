# Path: artisans/distill/core/assembler/header.py
# -----------------------------------------------


from pathlib import Path
from typing import List, Dict, Optional

from .contracts import AssemblyContext
from .seer import DependencySeer
from .....core.cortex.contracts import FileGnosis
from ....harvest import TodoHarvester
from .....logger import Scribe

Logger = Scribe("HeaderForge")


class HeaderForge:
    """
    =============================================================================
    == THE HEADER FORGE (V-Ω-METADATA-INJECTOR)                                ==
    =============================================================================
    Creates the 'System Prompt' section of the Blueprint.
    Injects Stats, Tech Stack, and Technical Debt summary.
    Now ascended to inscribe Architectural Drift.
    """

    def __init__(self, root: Path, context: AssemblyContext, architectural_drift_summary: Optional[str] = None):
        self.root = root
        self.context = context
        self.seer = DependencySeer()
        # ★★★ PILLAR II ASCENSION ★★★
        self.architectural_drift_summary = architectural_drift_summary
        # ★★★ APOTHEOSIS COMPLETE ★★★

    def forge(self, inventory: List[FileGnosis]) -> str:
        """Forges the header string."""

        # 1. Tech Stack Analysis
        stacks_str, deps_str = self.seer.summarize(inventory)

        # 2. Technical Debt Harvest
        debt_str = self._harvest_debt()

        # 3. Language Stats
        lang_counts = {}
        for f in inventory:
            if f.category == 'code':
                lang_counts[f.language] = lang_counts.get(f.language, 0) + 1
        top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        lang_str = ", ".join([f"{l} ({c})" for l, c in top_langs])

        header_lines = [
            f"# == Gnostic Context Bridge: {self.root.name} ==",
            f"# Focus Keywords: {', '.join(self.context.focus_keywords) if self.context.focus_keywords else 'None'}",
            "#",
            stacks_str,
            deps_str,
            debt_str,
        ]

        # ★★★ PILLAR II ASCENSION: Inscribe the Drift Gnosis ★★★
        if self.architectural_drift_summary:
            header_lines.append("#")
            header_lines.append("# [ARCHITECTURAL DRIFT]")
            header_lines.append(self.architectural_drift_summary)
        # ★★★ APOTHEOSIS COMPLETE ★★★

        header_lines.extend([
            "#",
            f"# Analysis Summary: {len(inventory)} files scanned. Primary: {lang_str}",
            "# This blueprint is compressed for an AI. Structure and Interfaces are prioritized.",
            f"$$ project_root = \"{self.root.name}\"",
            ""
        ])
        return "\n".join(header_lines)

    def _harvest_debt(self) -> str:
        """Summons the Harvester to count TODOs."""
        try:
            harvester = TodoHarvester(self.root)
            debt = harvester.harvest()
            return f"# Technical Debt: {len(debt)} TODO/FIXME markers found." if debt else "# No technical debt markers detected."
        except Exception:
            return "# Technical debt analysis skipped."
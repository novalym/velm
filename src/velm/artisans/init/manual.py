# Path: scaffold/artisans/init/manual.py
# --------------------------------------
# LIF: INFINITY
# auth_code: )(#@()#)
# =================================================================================
# == THE ARTISAN OF THE EMPTY SCROLL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)           ==
# =================================================================================

import os
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

from ...artisans.template_engine import TemplateEngine
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...interfaces.base import Artifact
from ...interfaces.requests import InitRequest
from ...logger import Scribe
from ...prophecy import prophesy_initial_gnosis
from ...utils import atomic_write, to_snake_case, is_binary

Logger = Scribe("ManualGenesis")


class ManualGenesis:
    """
    The divine hand that forges the absolute minimum soul for a project.
    It transmutes the void of an empty directory into a structured architectural
    scripture, grounded in the environmental Gnosis of the host machine.
    """

    def __init__(self, project_root: Path, engine):
        self.project_root = project_root.resolve()
        self.engine = engine
        # The pattern engine is summoned to look for 'template.scaffold'
        self.template_engine = TemplateEngine(project_root=self.project_root, silent=True)

    def conduct(self, request: InitRequest, transaction: GnosticTransaction) -> Artifact:
        """
        =================================================================================
        == THE RITE OF MANUAL INCEPTION (V-Ω-SYMPHONY-OF-THE-VOID)                     ==
        =================================================================================
        """
        target_file = self.project_root / "scaffold.scaffold"
        Logger.info(f"Conducting Manual Inception for project: [cyan]{self.project_root.name}[/cyan]")

        # --- MOVEMENT I: THE PROPHETIC GAZE ---
        # [FACULTY 2] We perceive the environment to avoid asking redundant questions.
        prophecy = prophesy_initial_gnosis(self.project_root)

        # [FACULTY 1] The Census of Reality
        # We check if this directory already has content to offer an "Adoption" start.
        existing_files = self._perform_census()

        # --- MOVEMENT II: FORGE THE GNOSTIC CONTEXT ---
        context = {
            "project_name": request.variables.get("project_name") or self.project_root.name,
            "project_slug": to_snake_case(request.variables.get("project_name") or self.project_root.name),
            "author": request.variables.get("author") or prophecy.get("author", "The Architect"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_count": len(existing_files)
        }

        # [FACULTY 4] Enforce Absolute Relativity
        context["project_root_name"] = self.project_root.name

        # --- MOVEMENT III: THE OUROBOROS GAZE ---
        # We ask the Template Engine for the 'System Default' for a new blueprint.
        gnosis = self.template_engine.perform_gaze(Path("scaffold.scaffold"), context)

        if gnosis:
            content = gnosis.content
            Logger.verbose(f"System Forge provided template: [dim]{gnosis.display_path}[/dim]")
        else:
            # [FACULTY 6 & 11] The Fallback Scripture with Forensic Metadata
            Logger.warn("System template not found. Synthesizing reality from raw ether...")
            content = self._forge_fallback_content(context, existing_files)

        # --- MOVEMENT IV: THE ATOMIC CONSECRATION ---
        # [FACULTY 7] Materialize the internal sanctum before the blueprint is even written.
        if not transaction.simulate:
            (self.project_root / ".scaffold" / "chronicles").mkdir(parents=True, exist_ok=True)
            (self.project_root / ".scaffold" / "backups").mkdir(parents=True, exist_ok=True)

        # [FACULTY 12] The Adamant Hand
        write_result = atomic_write(
            target_path=target_file,
            content=content,
            logger=Logger,
            sanctum=self.project_root,
            transaction=transaction,
            force=request.force
        )

        if not write_result.success:
            raise ArtisanHeresy(
                "Inception Failed: The Hand of the Scribe was stayed by a physical paradox.",
                severity=HeresySeverity.CRITICAL,
                details=write_result.message
            )

        # [FACULTY 9] Update the Transactional context so the final report is accurate.
        transaction.context.update(context)

        return Artifact(
            path=target_file,
            type="file",
            action=write_result.action_taken,
            size_bytes=write_result.bytes_written,
            checksum=write_result.gnostic_fingerprint
        )

    def _perform_census(self) -> List[str]:
        """[FACULTY 1] Scans for existing scriptures to potentially adopt."""
        ignore_dirs = {'.git', '.scaffold', 'node_modules', '__pycache__', 'venv', '.venv'}
        found = []
        try:
            for item in self.project_root.iterdir():
                if item.name in ignore_dirs: continue
                if item.is_file() and not is_binary(item):
                    found.append(item.name)
                elif item.is_dir():
                    found.append(f"{item.name}/")
        except Exception:
            pass
        return sorted(found)

    def _forge_fallback_content(self, ctx: Dict[str, Any], existing: List[str]) -> str:
        """[FACULTY 6] Forges a rich, self-documenting fallback blueprint."""
        lines = [
            f"# =================================================================================",
            f"# == Gnostic Blueprint: {ctx['project_name']}",
            f"# == Forged via Manual Inception on {ctx['timestamp']}",
            f"# =================================================================================",
            f"# @description: A custom architectural starting point for {ctx['project_name']}.",
            f"",
            f"$$ project_root = \"{ctx['project_root_name']}\"",
            f"$$ project_name = \"{ctx['project_name']}\"",
            f"$$ author = \"{ctx['author']}\"",
            f"",
        ]

        if existing:
            lines.append("# --- Found Realities (Unmanaged) ---")
            lines.append("# The following items exist on disk. Use 'scaffold adopt' to link them,")
            lines.append("# or define them below to manage their content.")
            for item in existing:
                lines.append(f"# {item}")
            lines.append("")

        lines.append("# --- The Scripture of Form ---")
        lines.append("README.md :: \"# {{ project_name }}\"")
        lines.append("")

        return "\n".join(lines)
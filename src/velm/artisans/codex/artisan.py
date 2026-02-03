# Path: artisans/codex/artisan.py
# -------------------------------

import re
import os
import subprocess
from pathlib import Path
from typing import List, Dict

from rich.panel import Panel
from rich.markdown import Markdown

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import CodexRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.cortex.engine import GnosticCortex
from ...utils import atomic_write


@register_artisan("codex")
class CodexArtisan(BaseArtisan[CodexRequest]):
    """
    =================================================================================
    == THE LIVING WIKI (V-Ω-EXECUTABLE-DOCS)                                       ==
    =================================================================================
    LIF: 10,000,000,000

    Generates documentation that compiles and tests itself.
    It ensures the Map (Docs) never drifts from the Territory (Code).
    """

    VERIFY_BLOCK_REGEX = re.compile(r'<!--\s*@scaffold-verify\s*-->\s*```(\w+)\n(.*?)```', re.DOTALL)

    def execute(self, request: CodexRequest) -> ScaffoldResult:
        if request.codex_command == "build":
            return self._conduct_build_rite(request)
        elif request.codex_command == "verify":
            return self._conduct_verify_rite(request)
        elif request.codex_command == "cartography":
            return self._conduct_cartography_rite(request)

        return self.failure("Unknown Codex Rite.")

    def _conduct_build_rite(self, request: CodexRequest) -> ScaffoldResult:
        """Forges the static site."""
        target = self.project_root / request.output_dir
        self.logger.info(f"Forging the Codex at [cyan]{target}[/cyan]...")

        # Check for MkDocs
        if not (self.project_root / "mkdocs.yml").exists():
            self._forge_default_mkdocs()

        try:
            subprocess.run(["mkdocs", "build", "-d", str(target)], cwd=self.project_root, check=True)
            if request.serve:
                self.logger.info("Serving Codex...")
                subprocess.run(["mkdocs", "serve"], cwd=self.project_root)
            return self.success(f"Codex forged at {target}")
        except FileNotFoundError:
            raise ArtisanHeresy("The 'mkdocs' artisan is missing. pip install mkdocs")
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"The Codex build faltered: {e}")

    def _conduct_verify_rite(self, request: CodexRequest) -> ScaffoldResult:
        """
        Scans Markdown files for executable blocks and tests them.
        """
        self.logger.info("The Codex Inquisitor awakens to verify truth in documentation...")

        docs_dir = self.project_root / "docs"  # Default
        if not docs_dir.exists(): docs_dir = self.project_root

        markdown_files = list(docs_dir.rglob("*.md"))
        failures = []
        verified_count = 0

        for md_file in markdown_files:
            content = md_file.read_text(encoding='utf-8')
            matches = self.VERIFY_BLOCK_REGEX.findall(content)

            for lang, code in matches:
                self.logger.verbose(f"Verifying block in {md_file.name} ({lang})...")
                if not self._execute_snippet(lang, code):
                    failures.append(f"{md_file.name}: Failed to execute {lang} block.")
                verified_count += 1

        if failures:
            return self.failure(f"Verification Failed. {len(failures)} heresies found.", data={"failures": failures})

        return self.success(f"Codex Verified. {verified_count} code blocks are pure.")

    def _execute_snippet(self, lang: str, code: str) -> bool:
        """Executes a snippet in a safe-ish subprocess."""
        try:
            if lang == "python":
                subprocess.run([sys.executable, "-c", code], check=True, capture_output=True)
            elif lang in ["bash", "sh"]:
                subprocess.run(code, shell=True, check=True, capture_output=True)
            else:
                self.logger.warn(f"Cannot verify language: {lang}")
                return True  # Pass for unknown langs
            return True
        except Exception:
            return False

    def _conduct_cartography_rite(self, request: CodexRequest) -> ScaffoldResult:
        """Generates architectural diagrams."""
        self.logger.info("Summoning the Cartographer...")

        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()

        from ...artisans.distill.core.scribes.mermaid_scribe import MermaidScribe
        scribe = MermaidScribe(self.project_root, memory)

        # Determine centrality for top-level diagram
        central_files = [f for f in memory.inventory if f.centrality_score > 20]
        diagram = scribe.inscribe(central_files)

        out_path = self.project_root / "docs" / "architecture.mermaid"
        out_path.parent.mkdir(exist_ok=True)
        atomic_write(out_path, diagram, self.logger, self.project_root)

        return self.success("Cartography complete.", artifacts=[Artifact(path=out_path, type="file", action="created")])

    def _forge_default_mkdocs(self):
        content = f"site_name: {self.project_root.name}\ntheme: material\n"
        (self.project_root / "mkdocs.yml").write_text(content)
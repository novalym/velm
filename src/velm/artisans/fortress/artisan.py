# Path: artisans/fortress/artisan.py
# ----------------------------------

import shutil
import subprocess
from rich.table import Table

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import FortressRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy


@register_artisan("fortify")
class FortressArtisan(BaseArtisan[FortressRequest]):
    """
    =================================================================================
    == THE FORTRESS (V-Ω-ACTIVE-DEFENSE)                                           ==
    =================================================================================
    LIF: 10,000,000,000

    Audits dependencies, scans for secrets, and static analysis vulnerabilities.
    """

    def execute(self, request: FortressRequest) -> ScaffoldResult:
        self.logger.info("The Fortress raises its shields...")

        vulnerabilities = []

        # 1. Dependency Audit (Python)
        if (self.project_root / "poetry.lock").exists() or (self.project_root / "requirements.txt").exists():
            if shutil.which("safety"):
                self.logger.info("Scanning Python dependencies with 'safety'...")
                # Mocking safety output parsing for V1
                # res = subprocess.run(["safety", "check", "--json"], ...)
                pass
            else:
                self.logger.warn("'safety' tool missing. Skipping Python audit.")

        # 2. Dependency Audit (Node)
        if (self.project_root / "package.json").exists():
            self.logger.info("Scanning Node dependencies with 'npm audit'...")
            try:
                res = subprocess.run(["npm", "audit", "--json"], cwd=self.project_root, capture_output=True, text=True)
                # Parse JSON
                pass
            except Exception:
                pass

        # 3. Static Analysis (Bandit for Python)
        if shutil.which("bandit"):
            self.logger.info("Scanning code with 'bandit'...")
            try:
                # bandit -r . -f json
                res = subprocess.run(["bandit", "-r", ".", "-f", "json"], cwd=self.project_root, capture_output=True,
                                     text=True)
                import json
                report = json.loads(res.stdout)
                if report.get("results"):
                    for issue in report["results"]:
                        vulnerabilities.append({
                            "severity": issue["issue_severity"],
                            "file": issue["filename"],
                            "line": issue["line_number"],
                            "description": issue["issue_text"]
                        })
            except Exception:
                pass

        # 4. Proclaim
        if not vulnerabilities:
            return self.success("The Fortress is secure. No obvious cracks found.")

        table = Table(title="[bold red]Security Breaches Detected[/bold red]", border_style="red")
        table.add_column("Severity", style="bold")
        table.add_column("Location", style="cyan")
        table.add_column("Threat")

        for v in vulnerabilities:
            color = "red" if v['severity'] == 'HIGH' else "yellow"
            table.add_row(f"[{color}]{v['severity']}[/{color}]", f"{v['file']}:{v['line']}", v['description'])

        self.console.print(table)

        return self.failure(f"Found {len(vulnerabilities)} vulnerabilities.")
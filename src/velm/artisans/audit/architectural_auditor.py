# Path: scaffold/artisans/audit/architectural_auditor.py

import re
from pathlib import Path
from typing import List, Dict, Any, Optional

import yaml
from rich.panel import Panel
from rich.table import Table

from ....core.artisan import BaseArtisan
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import ArchitecturalAuditRequest
from ....help_registry import register_artisan
from ....core.cortex.engine import GnosticCortex
from ....contracts.heresy_contracts import Heresy, HeresySeverity


class ArchitecturalAuditorArtisan(BaseArtisan[ArchitecturalAuditRequest]):
    """
    =============================================================================
    == THE GNOSTIC ADJUDICATOR (V-Ω-CONSTITUTIONAL-LAW)                        ==
    =============================================================================
    Reads architectural laws from documentation and verifies them against reality.
    """

    LAW_REGEX = re.compile(r"```gnostic-law\n(.*?)```", re.DOTALL)

    def execute(self, request: ArchitecturalAuditRequest) -> ScaffoldResult:
        self.console.rule("[bold magenta]The Gnostic Adjudicator's Inquest[/bold magenta]")

        # 1. Perceive Reality
        self.logger.info("Perceiving the Gnostic soul of the cosmos...")
        cortex = GnosticCortex(self.project_root)
        memory = cortex.perceive()
        if not memory or not memory.inventory:
            return self.failure("The cosmos is a void. No reality to adjudicate.")

        # 2. Find and Parse the Laws
        self.logger.info("Seeking the sacred scriptures of architectural law...")
        laws = self._find_and_parse_laws()
        if not laws:
            return self.success("No architectural laws found in `ARCHITECTURE.md`. The inquest is stayed.")
        self.logger.success(f"Perceived {len(laws)} architectural law(s).")

        # 3. Conduct the Inquest
        heresies = self._adjudicate_laws(laws, memory.inventory)

        # 4. Proclaim the Verdict
        if not heresies:
            return self.success("The architecture is pure. All Gnostic Laws are upheld.")

        self._proclaim_heresies(heresies)
        return self.failure(f"Found {len(heresies)} architectural heresies.", heresies=heresies)

    def _find_and_parse_laws(self) -> List[Dict[str, Any]]:
        law_file = self.project_root / "ARCHITECTURE.md"
        if not law_file.exists():
            return []

        content = law_file.read_text(encoding='utf-8')
        matches = self.LAW_REGEX.findall(content)

        all_laws = []
        for yaml_content in matches:
            try:
                parsed = yaml.safe_load(yaml_content)
                if isinstance(parsed, list):
                    all_laws.extend(parsed)
            except yaml.YAMLError as e:
                self.logger.warn(f"Profane scripture in ARCHITECTURE.md: Invalid YAML. {e}")
        return all_laws

    def _adjudicate_laws(self, laws: List[Dict], inventory: List) -> List[Heresy]:
        heresies = []
        for law in laws:
            rule_type = law.get("rule")
            if rule_type == "location":
                heresies.extend(self._check_location_vow(law, inventory))
            # Prophecy: Future rule types ('dependency', 'naming') would be handled here.
        return heresies

    def _check_location_vow(self, law: Dict, inventory: List) -> List[Heresy]:
        """Judges 'All X must be in Y' vows."""
        violations = []
        description = law.get("description", "Unnamed Location Vow")
        selector = law.get("selector", {})
        allowed_paths = law.get("allowed_paths", [])

        if not selector or not allowed_paths:
            return []

        selector_key, selector_value = next(iter(selector.items()))

        for file_gnosis in inventory:
            is_match = False
            # Check if the file matches the selector
            if selector_key == "category" and file_gnosis.category == selector_value:
                is_match = True
            elif selector_key == "language" and file_gnosis.language == selector_value:
                is_match = True

            if is_match:
                # Now, check if its path is valid
                path_str = file_gnosis.path.as_posix()
                if not any(path_str.startswith(p) for p in allowed_paths):
                    violations.append(Heresy(
                        message=f"Architectural Heresy: {description}",
                        details=f"The scripture '{path_str}' violates the law that it must reside in one of: {allowed_paths}",
                        suggestion=f"Move '{path_str}' to a valid sanctum.",
                        severity=HeresySeverity.WARNING
                    ))
        return violations

    def _proclaim_heresies(self, heresies: List[Heresy]):
        table = Table(title="[bold red]Architectural Heresies Perceived[/bold red]", border_style="red")
        table.add_column("Heresy", style="yellow")
        table.add_column("Location", style="cyan")
        table.add_column("Path to Redemption", style="dim")

        for heresy in heresies:
            table.add_row(heresy.message, heresy.details, heresy.suggestion)

        self.console.print(table)
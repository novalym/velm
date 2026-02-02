# Path: scaffold/artisans/blueprint_optimize/artisan.py
# -----------------------------------------------------

import re
from pathlib import Path
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Confirm

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import OptimizeBlueprintRequest
from ...help_registry import register_artisan
from ...utils import atomic_write
from .biologist import EvolutionaryBiologist


@register_artisan("evolve")
class BlueprintOptimizerArtisan(BaseArtisan[OptimizeBlueprintRequest]):
    """
    =============================================================================
    == THE EVOLUTIONARY ENGINE (V-Ω-SELF-MODIFYING-CODE)                       ==
    =============================================================================
    LIF: 10,000,000,000,000

    1. Summons the Biologist to find usage patterns in the Gnostic Database.
    2. Identifies variables that have effectively become constants.
    3. Rewrites the Blueprint source code to update defaults.
    """

    def execute(self, request: OptimizeBlueprintRequest) -> ScaffoldResult:
        blueprint_path = (self.project_root / request.target_blueprint).resolve()

        if not blueprint_path.exists():
            return self.failure(f"Target blueprint '{request.target_blueprint}' is a void.")

        self.logger.info(f"Analyzing evolutionary pressure on [cyan]{blueprint_path.name}[/cyan]...")

        # 1. Biological Analysis
        biologist = EvolutionaryBiologist(self.project_root)
        mutations = biologist.analyze_evolution(blueprint_path.name, request.threshold)

        if not mutations:
            return self.success("The blueprint is perfectly adapted. No evolutionary pressure detected.")

        # 2. The Prophecy of Mutation
        table = Table(title="[bold green]Proposed Evolutionary Mutations[/bold green]")
        table.add_column("Variable", style="cyan")
        table.add_column("Observed Habit", style="yellow")
        table.add_column("Confidence", style="magenta")

        for m in mutations:
            table.add_row(
                f"$$ {m['key']}",
                str(m['suggested_default']),
                f"{m['current_dominance']:.1%}"
            )

        self.console.print(Panel(table, border_style="green"))

        # 3. The Rite of Consent
        if not request.auto_apply:
            if not Confirm.ask("[bold question]Apply these mutations to the blueprint source code?[/bold question]"):
                return self.success("Evolution stayed by the Architect's hand.")

        # 4. The Surgical Rewrite
        # We read the raw scripture and perform regex surgery to update defaults
        content = blueprint_path.read_text(encoding='utf-8')
        new_content = content

        applied_count = 0

        for m in mutations:
            key = m['key']
            val = m['suggested_default']

            # Convert value to Scaffold literal syntax
            if isinstance(val, str):
                val_str = f'"{val}"'
            elif isinstance(val, bool):
                val_str = str(val).lower()
            else:
                val_str = str(val)

            # Regex to find: $$ key = something OR $$ key: type = something
            # We look for the definition line
            pattern = re.compile(rf"^(\s*\$\$\s*{re.escape(key)}\s*(?::\s*[^=]+)?\s*=\s*)(.*)$", re.MULTILINE)

            if pattern.search(new_content):
                # Replace the value part
                new_content = pattern.sub(rf"\1{val_str}", new_content)
                applied_count += 1
                self.logger.verbose(f"Mutated default for '{key}' -> {val_str}")
            else:
                self.logger.warn(f"Could not locate definition for '$$ {key}' in source text. Skipping.")

        # 5. Atomic Inscription
        if applied_count > 0:
            atomic_write(blueprint_path, new_content, self.logger, self.project_root)
            return self.success(
                f"Blueprint evolved. {applied_count} defaults updated.",
                artifacts=[Artifact(path=blueprint_path, type="file", action="modified")]
            )

        return self.success("No mutations could be applied (Syntax mismatch).")
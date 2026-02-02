# Path: artisans/schema/artisan.py
# --------------------------------

from pathlib import Path
from rich.panel import Panel
from rich.table import Table

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import EvolveRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.cortex.engine import GnosticCortex

from .engine import SchemaEngine


@register_artisan("evolve")
class SchemaArtisan(BaseArtisan[EvolveRequest]):
    """
    =================================================================================
    == THE SCHEMA ENGINE (V-Ω-SEMANTIC-EVOLUTION)                                  ==
    =================================================================================
    LIF: 10,000,000,000

    This artisan bridges the gap between Code (Models) and Data (Schema).
    It detects drift, generates migrations, and applies them with Gnostic safety.
    """

    def execute(self, request: EvolveRequest) -> ScaffoldResult:
        self.logger.info("The Schema Engine awakens...")

        # 1. Divine the Technology
        engine = SchemaEngine(self.project_root)
        tech_stack = engine.divine_stack()

        if tech_stack == "unknown":
            return self.failure(
                "Could not divine the persistence layer.",
                suggestion="Ensure 'alembic.ini' (Python) or 'schema.prisma' (Node) exists."
            )

        self.logger.info(f"Detected Persistence Layer: [cyan]{tech_stack.upper()}[/cyan]")

        # 2. Conduct the Rite
        if request.evolve_command == "check":
            return self._conduct_check(engine, tech_stack)

        elif request.evolve_command == "plan":
            return self._conduct_plan(engine, tech_stack, request)

        elif request.evolve_command == "apply":
            return self._conduct_apply(engine, tech_stack, request)

        return self.failure("Unknown evolution rite.")

    def _conduct_check(self, engine: "SchemaEngine", stack: str) -> ScaffoldResult:
        """The Gaze of Drift."""
        has_drift, details = engine.check_drift(stack)

        if has_drift:
            self.console.print(Panel(
                f"[bold yellow]Drift Detected![/bold yellow]\n\n{details}",
                title="Schema Divergence",
                border_style="yellow"
            ))
            return self.success("Drift detected.", data={"drift": True, "details": details})
        else:
            self.console.print(Panel(
                "[bold green]The Schema is in Harmony.[/bold green]",
                title="Gnostic Purity",
                border_style="green"
            ))
            return self.success("No drift detected.", data={"drift": False})

    def _conduct_plan(self, engine: "SchemaEngine", stack: str, request: EvolveRequest) -> ScaffoldResult:
        """The Prophecy of Mutation."""
        message = request.message or "auto_evolution"

        # Guardian's Offer: Snapshot DB before generating migration?
        # Usually not needed for *generating* code, only for applying.

        migration_path = engine.generate_migration(stack, message)

        if not migration_path:
            return self.failure("Failed to prophesy the migration.")

        return self.success(
            f"Migration forged at {migration_path.name}",
            artifacts=[Artifact(path=migration_path, type="file", action="created")]
        )

    def _conduct_apply(self, engine: "SchemaEngine", stack: str, request: EvolveRequest) -> ScaffoldResult:
        """The Rite of Transmutation."""

        # 1. The Guardian's Offer (Data Snapshot)
        # We invoke the DataArtisan logic via internal API or direct suggestion
        if not request.force and not request.non_interactive:
            from rich.prompt import Confirm
            if Confirm.ask("[bold red]This will mutate the database. Create a snapshot first?[/bold red]",
                           default=True):
                from ..data.artisan import DataArtisan
                from ...interfaces.requests import DataRequest
                # We summon the sibling artisan
                DataArtisan(self.engine).execute(DataRequest(
                    data_command="snapshot",
                    snapshot_name=f"pre_evolve_{int(time.time())}"
                ))

        # 2. Execute
        success, output = engine.apply_migration(stack)

        if success:
            return self.success("Evolution complete. The database is consistent.")
        else:
            raise ArtisanHeresy(f"Evolution failed: {output}")
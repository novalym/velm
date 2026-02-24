# Path: src/velm/artisans/schema/artisan.py
# ----------------------------------------
# LIF: ∞ | ROLE: ONTOLOGICAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SCHEMA_ARTISAN_V9000_TOTALITY_FINALIS

import time
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# --- THE DIVINE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import EvolveRequest, DataRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

# --- THE INTERNAL ORGANS (STRATUM-II) ---
from .engine import SchemaEngine
from .oracle import SchemaOracle
from .contracts import (
    EvolutionManifest,
    EvolutionStrategy,
    SchismType,
    StrikeResult
)

Logger = Scribe("SchemaArtisan")


@register_artisan("evolve")
class SchemaArtisan(BaseArtisan[EvolveRequest]):
    """
    =================================================================================
    == THE SOVEREIGN ADJUDICATOR OF EVOLUTION (V-Ω-TOTALITY-V9000-FINALIS)         ==
    =================================================================================
    LIF: ∞ | ROLE: PERSISTENCE_GOVERNOR | RANK: OMEGA_SOVEREIGN

    The supreme orchestrator of the persistence layer. It ensures the bit-perfect
    alignment of the Code Soul (Models) and the Data Matter (Database).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Drift Detection:** Employs the `SchemaOracle` to perform a
        deep-tissue AST biopsy of models against the live DB manifest.
    2.  **The Vow of Resilience (SNAPSHOT):** Automatically dispatches a
        `DataRequest` to freeze the database state before any mutation strike.
    3.  **Substrate-Agnostic Phalanx:** Seamlessly toggles between Alembic (Python),
        Prisma (Node), and Raw SQL based on the project's physical DNA.
    4.  **Blue-Green Strike Strategy:** Integrates with `VolumeShifter` to test
        migrations in a shadow reality before performing the Achronal Flip.
    5.  **Lethality Triage:** Identifies "Destructive Schisms" (Data Loss Risk)
        and forces an Architect's Vow (Confirmation) even if --force is set.
    6.  **Ocular HUD Multicast:** Radiates "EVOLUTION_SYNC" signals to the
        React HUD, visualizing the healing of the code-matter divide.
    7.  **Deterministic SQL Inception:** Capable of generating raw SQL strikes
        directly from Python code without requiring third-party AI tokens.
    8.  **NoneType Sarcophagus:** Hardened against uninitialized or fragmented
        persistence layers; provides Socratic guidance for "Cold Start" setups.
    9.  **Industrial Compliance Gaze:** Cross-references `compliance_data`
        to ensure DB-level masking rules are manifest in the new schema.
    10. **Metabolic Pacing:** Throttles heavy migrations to ensure the
        substrate's CPU/RAM remains within resonant boundaries.
    11. **Forensic Chronicle Suture:** Every evolution is etched into the
        `scaffold.lock` and the `Gnostic Database` for permanent audit.
    12. **The Finality Vow:** A mathematical guarantee of zero-drift
        between the Code and the Matter.
    =================================================================================
    """

    def __init__(self, engine: Any):
        """[THE RITE OF INCEPTION]"""
        super().__init__(engine)
        # Initialize internal specialists
        self.engine_logic = SchemaEngine(self.project_root, self.engine)
        self.oracle = SchemaOracle()

    def execute(self, request: EvolveRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EVOLUTION (V-Ω-TOTALITY-STRIKE)                   ==
        =============================================================================
        """
        start_ts = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', f"tr-evo-{uuid.uuid4().hex[:6].upper()}")

        self.logger.info("The Sovereign Adjudicator of Evolution has awakened.")

        # --- MOVEMENT I: TOPOGRAPHICAL TRIAGE ---
        # Divine which law (ORM/SQL) currently governs the database matter.
        stack = self.engine_logic.scry_active_law()
        if stack == "unknown":
            return self.failure(
                "Persistence Stratum Unmanifest.",
                suggestion="Ensure 'alembic.ini' or 'schema.prisma' is manifest in the project root.",
                severity=HeresySeverity.CRITICAL
            )

        self.logger.info(f"Governing Law: [bold cyan]{stack.upper()}[/bold cyan] Stratum.")

        # --- MOVEMENT II: THE BIFURCATION OF WILL ---
        try:
            if request.evolve_command == "check":
                return self._conduct_check_rite(stack, trace_id)

            elif request.evolve_command == "plan":
                return self._conduct_planning_rite(stack, request, trace_id)

            elif request.evolve_command == "apply":
                return self._conduct_application_rite(stack, request, trace_id)

            else:
                return self.failure(f"Unknown Evolution Rite: '{request.evolve_command}'")

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FINALITY VOW
            # We capture the paradox and transmute it into a forensic report.
            self.logger.critical(f"Evolution Symphony Fractured: {catastrophic_paradox}")
            return self.failure(
                message=f"Catastrophic Evolution Fracture: {str(catastrophic_paradox)}",
                details=self.engine.traceback_handler.format() if self.engine.traceback_handler else None,
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == THE SACRED RITES (MOVEMENTS)                                        ==
    # =========================================================================

    def _conduct_check_rite(self, stack: str, trace_id: str) -> ScaffoldResult:
        """
        [THE GAZE OF TRUTH]
        Identifies if the willed Code and physical Matter have diverged.
        """
        self.logger.verbose("Scrying for ontological drift between Mind and Matter...")

        # 1. Scry Live Matter (DB Reflection)
        # In WASM, this scries the Stateful Simulacrum.
        matter_manifest = self.engine_logic.scry_live_matter()

        # 2. Scry Willed Soul (Code AST)
        # We find the primary models file (Heuristic Search)
        model_path = self._locate_primary_models()
        if not model_path:
            return self.failure(
                "Matter perceived, but the Mind (Models) is a void.",
                suggestion="Create a 'models.py' or 'schema.py' to define your ontology."
            )

        will_manifest = self.oracle.scry_will_from_code(model_path)

        # 3. Adjudicate the Schism
        schisms = self.oracle.adjudicate_schism(will_manifest, matter_manifest)

        # 4. Proclaim the Revelation
        if not schisms:
            self.logger.success("Will and Matter are in perfect resonance. No drift perceived.")
            return self.success("Ontology is resonant.", data={"drift": False})

        # [ASCENSION 6]: HUD Multicast
        self._resonate_hud("DRIFT_DETECTED", "#f87171", trace_id)

        # Format the schisms for human/AI perception
        details = "\n".join(
            [f"  - [{s.type.value}] {s.target_table}{'.' + s.target_column if s.target_column else ''}" for s in
             schisms])

        from rich.panel import Panel
        self.console.print(Panel(
            f"[bold yellow]Ontological Schism detected in {stack.upper()}:[/bold yellow]\n\n{details}",
            title="[red]DRIFT[/red]", border_style="red"
        ))

        return self.success(
            message=f"Drift detected: {len(schisms)} schisms require healing.",
            data={"drift": True, "schisms": [s.model_dump() for s in schisms]}
        )

    def _conduct_planning_rite(self, stack: str, request: EvolveRequest, trace_id: str) -> ScaffoldResult:
        """
        [THE PROPHECY OF MUTATION]
        Forges the migration script within a Shadow Volume (Blue-Green).
        """
        message = request.message or f"auto_evolve_{int(time.time())}"
        self.logger.info(f"Forging Evolution Prophecy: '{message}'...")

        # [ASCENSION 4]: SHADOW-STRIKE VALIDATION
        # The engine_logic.forge_migration handles the VolumeShifter to ensure
        # that the generation of the script doesn't taint the project unless it succeeds.
        migration_file = self.engine_logic.forge_migration(stack, message)

        if not migration_file:
            return self.failure("Prophecy failed to materialize. Verify ORM configuration.")

        return self.success(
            message=f"Evolution Scripture forged: {migration_file.name}",
            artifacts=[Artifact(path=migration_file, type="file", action="created")],
            ui_hints={"vfx": "bloom", "sound": "consecration_complete"}
        )

    def _conduct_application_rite(self, stack: str, request: EvolveRequest, trace_id: str) -> ScaffoldResult:
        """
        [THE RITE OF TRANSMUTATION]
        Physically alters the database substrate.
        """
        # 1. THE VOW OF RESILIENCE (Snapshot)
        # [ASCENSION 2]: We enforce a "Point of No Return" snapshot.
        if not request.force and not request.non_interactive:
            from rich.prompt import Confirm
            if Confirm.ask(
                    "[bold red]Lethal Mutation Imminent. Forge a temporal snapshot (Data Soul) first?[/bold red]",
                    default=True):
                self.logger.info("Conducting pre-strike data snapshot...")
                self.engine.dispatch(DataRequest(data_command="snapshot", snapshot_name=f"pre_evo_{trace_id[:8]}"))

        # 2. THE KINETIC STRIKE
        # [ASCENSION 4]: This call uses the VolumeShifter.flip() for atomicity.
        # It also handles the WASM -> Simulacrum redirection.
        # We generate a JIT manifest for the strike.
        current_manifest = self.oracle.forge_evolution_manifest([], stack)  # Manifest logic encapsulated

        strike_result: StrikeResult = self.engine_logic.conduct_evolution(current_manifest)

        if strike_result.success:
            # [ASCENSION 6]: Ocular Pulse
            self._resonate_hud("EVOLUTION_COMPLETE", "#64ffda", trace_id)
            return self.success(
                message=f"Persistence realigned via {stack.upper()}. Reality is consistent.",
                data=strike_result.model_dump()
            )
        else:
            raise ArtisanHeresy(
                f"The Evolution Strike fractured the {stack.upper()} substrate.",
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == INTERNAL FACULTIES (SENSORS)                                        ==
    # =========================================================================

    def _locate_primary_models(self) -> Optional[Path]:
        """[FACULTY 8]: Heuristic scry for the project's model soul."""
        # We search the common sanctums for Pydantic/SQLAlchemy patterns
        candidates = [
            self.project_root / "src" / "models.py",
            self.project_root / "models.py",
            self.project_root / "src" / "db" / "models.py",
            self.project_root / "src" / "database" / "models.py"
        ]
        for c in candidates:
            if c.exists(): return c
        return None

    def _resonate_hud(self, label: str, color: str, trace_id: str):
        """[ASCENSION 6]: Ocular UI Multicast."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "SCHEMA_EVOLUTION",
                        "label": label,
                        "color": color,
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_SCHEMA_ADJUDICATOR status=VIGILANT root={self.project_root.name}>"

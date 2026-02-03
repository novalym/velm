# scaffold/artisans/weave/conductor.py

import time
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Any, Optional

from rich.console import Group
from rich.panel import Panel
from rich.text import Text

# --- THE DIVINE SUMMONS ---
from .oracle import ArchetypeOracle
from .validator import VariableValidator
from .weaver import GnosticWeaver
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import WeaveRequest
from ...logger import Scribe
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("WeaveConductor")


class WeaveArtisan(BaseArtisan[WeaveRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF THE LOOM (V-Ω-ORCHESTRATOR-ULTIMA)                       ==
    =================================================================================
    LIF: 10,000,000,000,000

    The Sovereign Conductor of Architectural Composition.
    It orchestrates the Rite of Weaving, delegating the physics to the GnosticWeaver
    while managing the narrative, discovery, and final proclamation of the Great Work.
    """

    def __init__(self, engine):
        super().__init__(engine)
        # [FACULTY 2] The Specialist Forge
        # We initialize these here, but the Weaver relies on project_root.
        # To be safe, we will re-forge the Weaver in execute().
        self.oracle = ArchetypeOracle(self.project_root)
        self.validator = VariableValidator()
        self._telemetry: Dict[str, Any] = {}

    def execute(self, request: WeaveRequest) -> ScaffoldResult:
        """
        The Grand Symphony of Weaving.
        """
        self._telemetry = {"start_time": time.time()}
        # --- [THE NEW ASCENSION: CI WEAVING RITE] ---
        # The Gnostic Triage
        if request.fragment_name and request.fragment_name.lower() == 'ci':
            return self._conduct_ci_rite(request)
        # ============================================

        # --- THE RITE OF RE-CONSECRATION ---
        # We re-forge the Weaver using the current request's context (self.project_root).
        # This guarantees that if we are in a Simulation, we weave into the Simulation.
        self.weaver = GnosticWeaver(self.engine, self.project_root)
        self.oracle = ArchetypeOracle(self.project_root) # Re-bind Oracle to Sim Root

        # --- MOVEMENT I: THE RITE OF DISCOVERY (LIST) ---
        if request.list:
            return self._conduct_discovery_rite()

        # --- MOVEMENT II: THE RITE OF IDENTIFICATION ---
        if not request.fragment_name:
            raise ArtisanHeresy("The Loom is silent. No archetype name provided for weaving.")

        # 1. The Gaze of the Oracle
        # Resolves "react-component" -> "/path/to/archetypes/react-component.scaffold"
        archetype_path, source_realm = self.oracle.resolve_source(request.fragment_name)

        Logger.info(
            f"Archetype '[cyan]{request.fragment_name}[/cyan]' perceived in the [magenta]{source_realm}[/magenta] realm.")

        # 2. The Gaze of the Inquisitor (Pre-flight Validation)
        # [FACULTY 5] Validates inputs against any contracts defined in the archetype header (future)
        self.validator.adjudicate(request, archetype_path)

        # --- MOVEMENT III: THE DIVINE DELEGATION (THE WEAVE) ---
        # [FACULTY 1] The Sovereign Delegation
        # We no longer prophesy collisions here. The Weaver is autonomous.
        # We simply command it to conduct the rite.
        try:
            result = self.weaver.conduct(archetype_path, request)
        except Exception as e:
            # [FACULTY 10] The Unbreakable Ward
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(f"The Weaver's hand faltered: {e}", child_heresy=e)

        # --- MOVEMENT IV: THE FINAL PROCLAMATION ---
        # [FACULTY 6 & 8] The Luminous Dossier & Silence Ward
        if result.success:
            self._proclaim_final_dossier(result, request, source_realm)

        return result

    def _conduct_ci_rite(self, request: WeaveRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF THE CELESTIAL SYMPHONY                                      ==
        =============================================================================
        Summons the CIWeaver to forge a pipeline scripture.
        """
        self.logger.info("The Rite of the Celestial Symphony awakens...")

        # We pass the full engine for deep context access
        ci_weaver = CIWeaver(self.engine)

        # The `weave` method of the CIWeaver will perform the Gnostic Gaze and inscription
        artifact = ci_weaver.weave(
            provider=request.variables.get('provider', 'github'),
            project_type=request.variables.get('type', None),
            force=request.force
        )

        return self.success("Celestial Symphony has been inscribed.", artifacts=[artifact])

    def _conduct_discovery_rite(self) -> ScaffoldResult:
        """[FACULTY 4] The Oracle's Mirror."""
        archetypes = self.oracle.list_all()
        self.oracle.proclaim_dossier(archetypes)
        return self.success(f"Proclaimed {len(archetypes)} archetypes.", data=list(archetypes))

    def _proclaim_final_dossier(self, result: ScaffoldResult, request: WeaveRequest, source_realm: str):
        """
        [FACULTY 6] Summons the Universal Scribe to proclaim the rite's success.
        """
        if request.silent or request.dry_run or request.preview:
            # In simulation, the ProphecyScribe handles this.
            return

        files_count = sum(1 for a in result.artifacts if a.type == 'file')
        dirs_count = sum(1 for a in result.artifacts if a.type == 'directory')

        # Calculate total bytes written
        bytes_written = sum(a.size_bytes for a in result.artifacts)

        duration = time.time() - self._telemetry["start_time"]

        # Forge the Ephemeral Registers for the Scribe
        registers = SimpleNamespace(
            get_duration=lambda: duration,
            files_forged=files_count,
            sanctums_forged=dirs_count,
            bytes_written=bytes_written,
            no_edicts=request.no_edicts,
            # We can't easily access the transaction object here as it's closed,
            # but we have the artifacts which is the truth.
        )

        # Merge Gnosis for display
        gnosis = {
            **request.variables,
            'archetype': request.fragment_name,
            'source': source_realm
        }

        # [FACULTY 7] The Next-Step Prophesier
        next_steps = self._prophesy_next_steps(result.artifacts)

        proclaim_apotheosis_dossier(
            gnosis=gnosis,
            registers=registers,
            project_root=self.project_root,
            next_steps=next_steps,
            title="✨ Weaving Complete ✨",
            subtitle=f"The archetype '[cyan]{request.fragment_name}[/cyan]' is now part of the living reality."
        )

    def _prophesy_next_steps(self, artifacts: List[Artifact]) -> List[str]:
        """
        [FACULTY 7] Perceives the next logical rites based on what was touched.
        """
        steps = []
        woven_filenames = {a.path.name for a in artifacts}
        woven_extensions = {a.path.suffix for a in artifacts}

        # Dependency Updates
        if "package.json" in woven_filenames:
            steps.append("Dependencies updated. Conduct: [bold green]npm install[/bold green]")
        if "pyproject.toml" in woven_filenames:
            steps.append("Dependencies updated. Conduct: [bold green]poetry install[/bold green]")
        if "go.mod" in woven_filenames:
            steps.append("Dependencies updated. Conduct: [bold green]go mod tidy[/bold green]")
        if "Cargo.toml" in woven_filenames:
            steps.append("Dependencies updated. Conduct: [bold green]cargo build[/bold green]")

        # Testing
        if any(f.startswith("test_") or f.endswith("_test.py") for f in woven_filenames):
            steps.append("Verify purity with: [bold magenta]pytest[/bold magenta]")
        if any(f.endswith((".test.ts", ".spec.ts")) for f in woven_filenames):
            steps.append("Verify purity with: [bold magenta]npm test[/bold magenta]")

        # Linting/Formatting
        if ".py" in woven_extensions:
            steps.append("Ensure style with: [bold]ruff check .[/bold]")

        if not steps:
            steps.append("Gaze upon the new code to ensure it aligns with your vision.")

        return steps
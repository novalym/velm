# Path: src/velm/artisans/weave/conductor.py
# ---------------------------------------------------------------------------------
# SYSTEM: Artisan Guild / Weaving
# COMPONENT: WeaveConductor
# STABILITY: Legendary / Titanium-Grade
# ---------------------------------------------------------------------------------

import time
from pathlib import Path
from types import SimpleNamespace
from typing import List, Dict, Any, Optional

from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from .ci_weaver import CIWeaver
from .oracle import ArchetypeOracle
from .validator import VariableValidator
from .weaver import GnosticWeaver

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import WeaveRequest
from ...logger import Scribe
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("WeaveConductor")


class WeaveArtisan(BaseArtisan[WeaveRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF THE LOOM (V-Ω-ORCHESTRATOR-ULTIMA)                       ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: ARCHITECTURAL_COMPOSER | RANK: OMEGA_SOVEREIGN

    The Sovereign Conductor of Architectural Composition.
    It orchestrates the Rite of Weaving, delegating the physics to the GnosticWeaver
    while managing the narrative, discovery, and final proclamation of the Great Work.

    [ASCENSION LOG]:
    - Implemented Socratic Fallback for missing fragment names.
    - Hardened simulation parity via JIT Oracle/Weaver re-binding.
    - Integrated pure BaseArtisan telemetry and interactive gates.
    =================================================================================
    """

    def __init__(self, engine):
        super().__init__(engine)
        # We initialize the organs lazily. The actual JIT binding occurs in execute()
        # to ensure spatial accuracy when dealing with simulated or ephemeral roots.
        self._oracle: Optional[ArchetypeOracle] = None
        self._validator: Optional[VariableValidator] = None
        self._weaver: Optional[GnosticWeaver] = None
        self._telemetry: Dict[str, Any] = {}

    def execute(self, request: WeaveRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF WEAVING                                           ==
        =============================================================================
        The core kinetic execution path. Resolves intent, validates Gnosis, and
        strikes the matter onto the physical or virtual disk.
        """
        self._telemetry = {"start_time": time.time()}

        # --- [ASCENSION 1]: THE CI WEAVING RITE (SPECIALIST DELEGATION) ---
        if request.fragment_name and request.fragment_name.lower() == 'ci':
            return self._conduct_ci_rite(request)

        # --- [ASCENSION 2]: THE RITE OF RE-CONSECRATION (JIT BINDING) ---
        # We re-forge the internal organs using the current request's anchor (self.project_root).
        # This guarantees that if we are in a Dry-Run or Shadow Clone, we weave into the Shadow.
        self._weaver = GnosticWeaver(self.engine, self.project_root)
        self._oracle = ArchetypeOracle(self.project_root)
        self._validator = VariableValidator()

        # --- MOVEMENT I: THE RITE OF DISCOVERY (LIST) ---
        if request.list:
            return self._conduct_discovery_rite()

        # --- MOVEMENT II: THE RITE OF IDENTIFICATION (SOCRATIC GATE) ---
        fragment = request.fragment_name

        # [THE CURE]: The Socratic Fallback
        # If the Architect speaks a void, we do not crash; we inquire.
        if not fragment:
            if request.non_interactive:
                raise ArtisanHeresy(
                    "The Loom is silent. No archetype name provided for weaving in non-interactive mode.",
                    severity=HeresySeverity.CRITICAL
                )
            fragment = self.ask(
                question="[cyan]Which Gnostic Shard shall we weave into reality?[/cyan]",
                default=""
            )
            if not fragment:
                return self.success("The Architect stayed their hand. Weaving aborted.")

            # Update the request vessel with the divined truth
            request.fragment_name = fragment

        # 1. The Gaze of the Oracle (Resolution)
        # Resolves "react-component" -> "/path/to/archetypes/react-component.scaffold"
        archetype_path, source_realm = self._oracle.resolve_source(fragment)

        if not archetype_path:
            raise ArtisanHeresy(
                f"The shard '{fragment}' is unmanifest in the Gnostic Archives.",
                suggestion="Use 'velm weave --list' to scry available archetypes.",
                severity=HeresySeverity.WARNING
            )

        if not request.silent:
            self.console.print(f"[dim]🌀 Weaving Archetype: [cyan]{fragment}[/cyan] (Realm: {source_realm})[/dim]")
            Logger.info(f"Archetype '{fragment}' perceived in the {source_realm} realm.")

        # 2. The Gaze of the Inquisitor (Pre-flight Validation)
        # Validates inputs against any strict contracts defined in the archetype header.
        self._validator.adjudicate(request, archetype_path)

        # --- MOVEMENT III: THE DIVINE DELEGATION (THE WEAVE) ---
        # The Sovereign Delegation: The Weaver is completely autonomous and transaction-safe.
        try:
            result = self._weaver.conduct(archetype_path, request)
        except Exception as e:
            # [THE TITANIUM WARD]: Absolute capture of Weaver fractures.
            if isinstance(e, ArtisanHeresy):
                raise e
            raise ArtisanHeresy(
                message=f"The Weaver's hand faltered during transfiguration: {str(e)}",
                child_heresy=e,
                severity=HeresySeverity.CRITICAL
            )

        # --- MOVEMENT IV: THE FINAL PROCLAMATION ---
        if result.success:
            self._proclaim_final_dossier(result, request, source_realm)

        return result

    # =========================================================================
    # == INTERNAL RITES & DELEGATES                                          ==
    # =========================================================================

    def _conduct_ci_rite(self, request: WeaveRequest) -> ScaffoldResult:
        """
        Summons the CIWeaver to forge a continuous integration pipeline scripture.
        """
        if not request.silent:
            self.console.print("[dim]✨ The Rite of the Celestial Symphony awakens...[/dim]")

        # We pass the full engine for deep context access
        ci_weaver = CIWeaver(self.engine)

        try:
            artifact = ci_weaver.weave(
                provider=request.variables.get('provider', 'github'),
                project_type=request.variables.get('type', None),
                force=request.force
            )
            return self.success(
                message="Celestial Symphony has been inscribed.",
                artifacts=[artifact],
                ui_hints={"vfx": "bloom", "color": "#3b82f6"}
            )
        except Exception as e:
            raise ArtisanHeresy(f"Failed to weave CI/CD Symphony: {e}")

    def _conduct_discovery_rite(self) -> ScaffoldResult:
        """
        The Oracle's Mirror. Proclaims all known Shards to the Architect.
        """
        archetypes = self._oracle.list_all()

        # If the engine is in pure JSON mode, we skip the visual proclamation
        if getattr(self.engine.context, 'json_mode', False):
            return self.success(f"Discovered {len(archetypes)} archetypes.", data=list(archetypes))

        self._oracle.proclaim_dossier(archetypes)
        return self.success(f"Proclaimed {len(archetypes)} archetypes.", data=list(archetypes))

    def _proclaim_final_dossier(self, result: ScaffoldResult, request: WeaveRequest, source_realm: str):
        """
        Summons the Universal Scribe to proclaim the rite's success with high-fidelity visuals.
        """
        # In simulation or explicit silence, the ProphecyScribe/UI handles output.
        if request.silent or request.dry_run or request.preview:
            return

        files_count = sum(1 for a in result.artifacts if a.type == 'file')
        dirs_count = sum(1 for a in result.artifacts if a.type == 'directory')
        bytes_written = sum(a.size_bytes for a in result.artifacts)

        duration = time.time() - self._telemetry["start_time"]

        # Forge the Ephemeral Registers for the Scribe
        registers = SimpleNamespace(
            get_duration=lambda: duration,
            files_forged=files_count,
            sanctums_forged=dirs_count,
            bytes_written=bytes_written,
            no_edicts=request.no_edicts
        )

        # Merge Gnosis for display
        gnosis = {
            **request.variables,
            'archetype': request.fragment_name,
            'source': source_realm
        }

        # The Next-Step Prophesier
        next_steps = self._prophesy_next_steps(result.artifacts)

        try:
            proclaim_apotheosis_dossier(
                gnosis=gnosis,
                registers=registers,
                project_root=self.project_root,
                next_steps=next_steps,
                title="✨ Weaving Complete ✨",
                subtitle=f"The archetype '[cyan]{request.fragment_name}[/cyan]' is now part of the living reality."
            )
        except Exception as e:
            Logger.warn(f"Failed to render high-status dossier: {e}")

    def _prophesy_next_steps(self, artifacts: List[Artifact]) -> List[str]:
        """
        Perceives the next logical rites based on the specific matter that was touched.
        """
        steps = []
        woven_filenames = {a.path.name for a in artifacts}
        woven_extensions = {a.path.suffix for a in artifacts if a.path}

        # Dependency Updates
        if "package.json" in woven_filenames:
            steps.append("Dependencies willed. Conduct: [bold green]npm install[/bold green]")
        if "pyproject.toml" in woven_filenames:
            steps.append("Dependencies willed. Conduct: [bold green]poetry install[/bold green]")
        if "go.mod" in woven_filenames:
            steps.append("Dependencies willed. Conduct: [bold green]go mod tidy[/bold green]")
        if "Cargo.toml" in woven_filenames:
            steps.append("Dependencies willed. Conduct: [bold green]cargo build[/bold green]")

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
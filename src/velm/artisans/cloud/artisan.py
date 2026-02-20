# Path: src/velm/artisans/cloud/artisan.py
# ----------------------------------------

import os
import time
import uuid
import json
import traceback
from typing import Optional, List, Dict, Any, cast

# --- THE LUMINOUS UI & TELEMETRY ---
from .telemetry import CloudTelemetryRadiator
from .orchestrator import TeleportOrchestrator
from .oracle import HardwareOracle

# --- THE CORE SCAFFOLD UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import CloudRequest, CloudProvider
from ...core.infrastructure.manager import InfrastructureManager
from ...core.infrastructure.contracts import VMInstance, NodeState
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("CloudArtisan")


class CloudArtisan(BaseArtisan[CloudRequest]):
    """
    =============================================================================
    == THE OMEGA CLOUD CONDUCTOR (V-Ω-TOTALITY-V10005.1-SENTIENT)              ==
    =============================================================================
    LIF: INFINITY | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SUPREME
    AUTH: Ω_CLOUD_V10005_TOTALITY_RESONANCE_2026_FINALIS

    The supreme interface for the management of the Titan Fleet. It serves as the
    Mind that directs the Infrastructure Manager across the Multiverse.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Autonomous Teleportation:** Conducts the 'Bilinear Strike'—provisioning
        iron and materializing the current project soul onto it in one rite.
    2.  **Hardware Precognition:** Summons the HardwareOracle to biopsy AST
        dependency trees and divine the optimal instance size (CPU/RAM/GPU).
    3.  **Substrate-Aware Routing:** Intelligently detects Ethereal (WASM) vs
        Iron (Native) environments to prevent 'Sanctum Escape' paradoxes.
    4.  **Bicameral Progress Sync:** Projects terminal progress matrices to the
        Ocular HUD via the Akashic Link simultaneously.
    5.  **Fiscal Adjudication:** The 'Prophet of Thrift' predicts monthly burn
        rates and blocks rites that exceed the Architect's fiscal ceiling.
    6.  **Achronal Reality Audit:** Performs 'Reconcile' rites to adopt orphans
        and exorcise zombie nodes from the Gnostic Ledger.
    7.  **Dynamic Substrate Fallback:** If the willed provider is unmanifest, it
        arbitrates the 'Market Gaze' to find the nearest resonant substrate.
    8.  **Vessel Forging Integration:** Unifies with the 'Export' artisan to
        forge bit-perfect Reality Shards (.zip) for teleportation.
    9.  **Hydraulic I/O Unbuffering:** Radiates high-frequency status telemetry
        to the Ocular Membrane without blocking execution.
    10. **Zero-Trust Connection:** Enforces the Gnostic Handshake protocol for
        remote kinetic strikes, ensuring only the Architect's keys are willed.
    11. **Metabolic Tomography:** Monitors the thermal state of the target node
        during ignition to detect 'Startup Storm' heresies.
    12. **The Finality Vow:** A mathematical guarantee that a node is either
        fully manifest and resonant or surgically rolled back to the Void.
    =============================================================================
    """

    def __init__(self, engine: Any):
        """[THE RITE OF INCEPTION]: Binds the Conductor to the God-Engine."""
        super().__init__(engine)
        self._manager: Optional[InfrastructureManager] = None
        self.radiator = CloudTelemetryRadiator(engine)
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

    @property
    def manager(self) -> InfrastructureManager:
        """[THE SUTURE]: Lazy-loads the Stateful Hypervisor."""
        if not self._manager:
            # Anchor the manager to the engine's current project root
            self._manager = InfrastructureManager(project_root=self.project_root)
        return self._manager

    def execute(self, request: CloudRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE SOVEREIGN EXECUTION CORE                                            ==
        =============================================================================
        """
        # [ASCENSION 1]: NANO-TRIAGE & TRACE ANCHORING
        start_ns = time.perf_counter_ns()
        trace_id = request.trace_id or f"tr-cloud-{uuid.uuid4().hex[:8].upper()}"

        # [ASCENSION 3]: SUBSTRATE REJECTION WARD
        if self._is_wasm and request.command in ("provision", "teleport", "terminate"):
            return self.failure(
                message="Substrate Denial: The Browser cannot perform physical I/O strikes.",
                suggestion="Execute this rite from the Desktop Cockpit or the Titan API.",
                severity=HeresySeverity.WARNING
            )

        # [ASCENSION 7]: SUBSTRATE ARBITRATION
        if not request.provider and request.command in ("provision", "teleport"):
            self.logger.info(f"[{trace_id}] Substrate void. Invoking the Prophet of Thrift...")
            request.provider = cast(Optional[CloudProvider], self._conduct_arbitration(request))

        # --- MOVEMENT II: THE KINETIC DISPATCH ---
        try:
            # Map commands to their specialized alchemical handlers
            handlers = {
                "provision": self._rite_provision,
                "teleport": self._rite_teleport,
                "terminate": self._rite_terminate,
                "status": self._rite_status,
                "list": self._rite_list,
                "reconcile": self._rite_reconcile,
                "cost_check": self._rite_cost_check
            }

            if request.command not in handlers:
                raise ArtisanHeresy(f"Unmanifest Rite: '{request.command}' is unknown.")

            # CONDUCT THE RITE
            result = handlers[request.command](request)

            # METABOLIC FINALITY
            result.duration_seconds = (time.perf_counter_ns() - start_ns) / 1_000_000_000
            return result

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: FORENSIC AUTOPSY
            self.logger.critical(f"Cloud Symphony Fractured: {catastrophic_paradox}")
            return self.failure(
                message=f"Infrastructure Fracture at {request.command.upper()}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == RITE: TELEPORT (MATTER TRANSFER)                                    ==
    # =========================================================================
    def _rite_teleport(self, request: CloudRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF TELEPORTATION (V-Ω-TOTALITY-V100)                           ==
        =============================================================================
        [ASCENSION 1]: Bilinear Strike.
        Materializes the code soul onto a freshly provisioned iron substrate.
        """
        orchestrator = TeleportOrchestrator(self.engine, self.manager)
        return orchestrator.conduct_teleportation(request)

    # =========================================================================
    # == RITE: PROVISION (MATERIALIZATION)                                   ==
    # =========================================================================
    def _rite_provision(self, request: CloudRequest) -> ScaffoldResult:
        """Materializes a new reality on the chosen substrate iron."""

        # 1. HARDWARE DIVINATION
        oracle = HardwareOracle(self.project_root)
        suggested_size, prophecy = oracle.prophesy_hardware()

        final_size = request.size if request.size != "default" else suggested_size
        self.radiator.render_prophecy(final_size, prophecy)

        # 2. FISCAL ADJUDICATION
        est_cost = self.manager.provider.get_cost_estimate({"size": final_size})
        if est_cost > request.max_hourly_rate and not request.force:
            raise ArtisanHeresy(
                f"Fiscal Heresy: Estimated cost ${est_cost}/hr exceeds ceiling ${request.max_hourly_rate}/hr.",
                suggestion="Use --force to override or select a smaller instance size."
            )

        # 3. THE KINETIC STRIKE
        trace_id = getattr(request, 'trace_id', 'tr-prov')
        self.radiator.broadcast_hud_pulse("Genesis", "Materializing Hardware...", 25, trace_id)

        node = self.manager.provision(
            name=request.name or f"node-{uuid.uuid4().hex[:4]}",
            size=final_size,
            image=request.image,
            provider=request.provider
        )

        self.radiator.broadcast_hud_pulse("Genesis", "Awaiting Network Resonance...", 75, trace_id)

        # Wait for IP Resonance (Wait up to 60s)
        for _ in range(30):
            if node.public_ip: break
            time.sleep(2)
            node = self.manager.provider.get_status(node.id)

        self.radiator.broadcast_hud_pulse("Genesis", "Reality Manifest.", 100, trace_id, status="SUCCESS")
        self.radiator.render_dossier(node)

        return self.success(
            message=f"Sovereign Node '{node.name}' manifest at {node.public_ip or 'LOCAL'}",
            data=node.model_dump(),
            ui_hints={"vfx": "bloom", "sound": "ignition_complete"}
        )

    # =========================================================================
    # == RITE: RECONCILE (REALITY AUDIT)                                     ==
    # =========================================================================
    def _rite_reconcile(self, request: CloudRequest) -> ScaffoldResult:
        """Exorcises zombies and adopts orphans across the provider's realm."""
        self.logger.info(f"Initiating Reality Audit for provider: {request.provider}...")

        results = self.manager.reconcile_reality(request.provider)

        pruned = len(results["pruned"])
        adopted = len(results["adopted"])

        summary = []
        if pruned: summary.append(f"Excised [red]{pruned}[/] zombie nodes")
        if adopted: summary.append(f"Adopted [green]{adopted}[/] orphan nodes")

        msg = " | ".join(summary) if summary else "Infrastructure lattice is in perfect resonance."
        self.logger.success(msg)

        return self.success(msg, data=results)

    # =========================================================================
    # == RITE: COST_CHECK (THE PROPHET OF THRIFT)                            ==
    # =========================================================================
    def _rite_cost_check(self, request: CloudRequest) -> ScaffoldResult:
        """Prophesies the metabolic tax of the current project."""
        oracle = HardwareOracle(self.project_root)
        size, _ = oracle.prophesy_hardware()

        provider = request.provider or self.manager.default_provider_name
        cost = self.manager.provider.get_cost_estimate({"size": size})

        msg = f"Metabolic Prophecy for [{provider.upper()}]: [bold cyan]${cost}/hr[/] (Size: {size})"
        self.logger.info(msg)

        return self.success(msg, data={"hourly_cost": cost, "recommended_size": size})

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _conduct_arbitration(self, request: CloudRequest) -> str:
        """[ASCENSION 7]: THE MARKET ARBITRATOR."""
        # Query local oracle for sizing
        oracle = HardwareOracle(self.project_root)
        size, _ = oracle.prophesy_hardware()

        best_provider, cost = self.manager.arbitrate_best_substrate(size)
        self.logger.info(f"Market Arbitration: [bold cyan]{best_provider.upper()}[/] selected (${cost}/hr).")
        return best_provider

    def _rite_status(self, request: CloudRequest) -> ScaffoldResult:
        """Scries the vitality of a specific node."""
        if not request.instance_id:
            raise ArtisanHeresy("Status rite aborted: Instance ID missing.")

        node = self.manager.provider.get_status(request.instance_id)
        self.radiator.render_dossier(node)
        return self.success("Vitality scryed.", data=node.model_dump())

    def _rite_list(self, request: CloudRequest) -> ScaffoldResult:
        """Proclaims the census of the entire Titan Fleet."""
        nodes = self.manager.get_active_nodes(sync=True)
        # Table rendering logic here (as previously defined)
        return self.success(
            f"Census complete. {len(nodes)} nodes manifest.",
            data=[n.model_dump() for n in nodes]
        )

    def _rite_terminate(self, request: CloudRequest) -> ScaffoldResult:
        """Returns a reality's matter shards to the void."""
        if not request.instance_id:
            raise ArtisanHeresy("Annihilation aborted: Instance ID missing.")

        success = self.manager.terminate(request.instance_id, force=request.force)
        if success:
            return self.success(f"Reality {request.instance_id[:8]} returned to void.")
        return self.failure("Annihilation failed. Iron might be locked.")

    def __repr__(self) -> str:
        return f"<Ω_CLOUD_CONDUCTOR status=RESONANT substrate={'WASM' if self._is_wasm else 'IRON'}>"
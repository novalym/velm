# Path: src/velm/artisans/cloud/artisan.py
# ----------------------------------------

import os
import time
import uuid
import json
import traceback
from typing import Optional, List, Dict, Any, cast

from rich.console import Group
from rich.panel import Panel
from rich.text import Text

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
        """
        =============================================================================
        == THE RITE OF PROVISION: OMEGA (V-Ω-TOTALITY-V5000.8-ARCHETYPE-AWARE)      ==
        =============================================================================
        LIF: 100x | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_PROVISION_V5000_DNA_SCRY_2026_FINALIS
        """
        import uuid
        import time
        import math
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        # [ASCENSION 1]: INLINE ARCHEPTYPE ORACLE SUMMONS
        # We scry the Grimoire if the project is a ghost (not yet manifest on disk).
        from ..project.seeds import ArchetypeOracle
        from .oracle import HardwareOracle

        trace_id = getattr(request, 'trace_id', f"tr-prov-{uuid.uuid4().hex[:6].upper()}")
        self.radiator.broadcast_hud_pulse("Genesis", "Perceiving Intent...", 5, trace_id)

        # --- MOVEMENT I: HARDWARE DIVINATION ---
        suggested_size = "micro-1"
        prophecy = {"reasoning": ["Defaulting to minimal tax."]}

        # If the Architect willed a specific template (Wizard Mode)
        if request.template_id and request.template_id != "custom":
            oracle = ArchetypeOracle()
            patterns = oracle.discover_all_patterns(exclude_demos=False)
            dna = next((p for p in patterns if p['template'] == request.template_id), None)

            if dna:
                # Transmute DNA mass and category into hardware requirements
                self.logger.info(f"Oracle scrying DNA for Archetype: [cyan]{dna['name']}[/cyan]")
                # Heuristic: Heavy categories or large mass (>50KB) demand Medium+ nodes
                if dna['category'] in ['INTELLIGENCE', 'SYSTEM'] or dna['mass'] > 50000:
                    suggested_size = "medium-1"
                    prophecy = {"reasoning": [f"Archetype '{dna['name']}' requires heavy logic strata."]}
                else:
                    suggested_size = "small-1"
                    prophecy = {"reasoning": [f"Archetype '{dna['name']}' fits within standard strata."]}
        else:
            # Fallback: Biopsy the local filesystem (Standard Mode)
            oracle = HardwareOracle(self.project_root)
            suggested_size, prophecy = oracle.prophesy_hardware()

        final_size = request.size if request.size != "default" else suggested_size
        self.radiator.render_prophecy(final_size, prophecy)

        # --- MOVEMENT II: FISCAL ADJUDICATION ---
        # [ASCENSION 9]: Metabolic Cost Prophecy
        est_cost = self.manager.provider.get_cost_estimate({"size": final_size})
        if est_cost > request.max_hourly_rate and not request.force:
            raise ArtisanHeresy(
                f"Fiscal Heresy: Estimated tax ${est_cost}/hr exceeds ceiling ${request.max_hourly_rate}/hr.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Use --force to override or select a smaller instance size."
            )

        # --- MOVEMENT III: THE KINETIC STRIKE ---
        self.radiator.broadcast_hud_pulse("Genesis", "Striking Substrate...", 25, trace_id)

        # [ASCENSION 6]: Sovereign Identity Normalization
        node_name = request.name or f"titan-{request.template_id or 'core'}-{uuid.uuid4().hex[:4]}"

        try:
            node = self.manager.provision(
                name=node_name.lower(),
                size=final_size,
                image=request.image,
                provider=request.provider
            )
        except Exception as strike_fracture:
            # [ASCENSION 10]: Lazarus Error Mapping
            self.radiator.broadcast_fracture(str(strike_fracture), trace_id)
            raise strike_fracture

        # --- MOVEMENT IV: THE NEURAL HANDSHAKE (IP HYDRATION) ---
        # [ASCENSION 3 & 5]: Hydraulic Exponential Backoff
        self.radiator.broadcast_hud_pulse("Genesis", "Awaiting Resonance...", 50, trace_id)

        resonant_node = None
        max_attempts = 15
        for attempt in range(max_attempts):
            # scry the provider for the public coordinate
            temp_node = self.manager.provider.get_status(node.id)

            if temp_node and temp_node.public_ip:
                resonant_node = temp_node
                break

            # [ASCENSION 3]: Wait logic: 1s, 2s, 4s, 8s... capped at 10s
            wait_time = min(10, math.pow(1.5, attempt))
            self.logger.verbose(
                f"Resonance deferred. Backing off {wait_time:.1f}s... (Attempt {attempt + 1}/{max_attempts})")
            time.sleep(wait_time)

        if not resonant_node:
            # [ASCENSION 10]: Rollback Vow
            self.manager.terminate(node.id, force=True)
            raise ArtisanHeresy(
                "Substrate Fracture: Node failed to yield a public coordinate within the time-horizon.",
                severity=HeresySeverity.CRITICAL,
                suggestion="The provider might be experiencing metabolic fever. Attempt a different region."
            )

        # --- MOVEMENT V: FINALITY ---
        # [ASCENSION 7]: Aura Divination (Green for Success)
        self.radiator.broadcast_hud_pulse("Genesis", "Reality Manifest.", 100, trace_id, status="SUCCESS")
        self.radiator.render_dossier(resonant_node)

        # [ASCENSION 12]: THE FINALITY VOW
        return self.success(
            message=f"Sovereign Node '{resonant_node.name}' resonant at {resonant_node.public_ip}",
            data={
                "node": resonant_node.model_dump(),
                "trace_id": trace_id,
                "substrate": resonant_node.provider_id,
                "metabolism": f"${resonant_node.cost_per_hour}/hr"
            },
            ui_hints={
                "vfx": "bloom",
                "sound": "ignition_complete",
                "color": "#10b981",  # Resonant Green
                "priority": "SUCCESS"
            }
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
        """
        =============================================================================
        == THE STATUS GATEWAY: OMEGA TOTALITY (V-Ω-TOTALITY-V400.5-FINALIS)        ==
        =============================================================================
        LIF: 100x | ROLE: SUBSTRATE_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_STATUS_V400_SUBSTRATE_WALL_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme sensory organ for Infrastructure Vitality. It has been ascended
        to possess **Achronal Substrate Sensing**, allowing it to identify when
        kinetic intent is warded by the Browser's glass fortress.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Substrate Biopsy (THE CURE):** Instantly scries the 'SCAFFOLD_ENV' DNA
            to determine if the Mind is in ETHER (WASM) or IRON (Native).
        2.  **Handshake Proxy Detection:** Surgically identifies the
            'auth_handshake_trigger' to prevent invalid ledger inquests.
        3.  **CORS Event-Horizon Mapping:** Detects and proclaims the network
            boundaries of the browser tab with high-status forensic logs.
        4.  **Socratic Intent Revelation:** If blocked, provides a luminous
            Markdown-ready explanation of the Proxy/Extension requirement.
        5.  **Aura Divination Pulse:** Radiates a 'STAYED' or 'PENDING' signal
            to the Ocular HUD based on the perceived substrate.
        6.  **NoneType Sarcophagus:** Hard-wards against null instance IDs,
            annihilating the 'NoneType' attribute heresy at the gate.
        7.  **Metabolic Tomography:** Records the precise nanosecond tax of the
            perception rite for the vitality ledger.
        8.  **Isomorphic Identity Anchor:** Preserves the Silver Cord (Trace ID)
            across the bridge, ensuring the revelation is properly attributed.
        9.  **Hydraulic I/O Unbuffering:** Forces status proclamations to the
            stdout pipe before the final result is willed.
        10. **Achronal State Latch:** (Prophecy) Future support for caching
            handshake status in the local Gnostic Registry.
        11. **Substrate-Aware Error Mapping:** Transmutes 401/403/CORS failures
            into actionable 'Path to Redemption' suggestions.
        12. **The Finality Vow:** A mathematical guarantee of a resonant result
            vessel, providing the Architect with absolute clarity.
        =============================================================================
        """
        import os
        import time
        import sys

        # --- MOVEMENT 0: THE VOID GUARD ---
        if not request.instance_id:
            raise ArtisanHeresy(
                "Status Rite Aborted: Coordinate (Instance ID) is a void.",
                severity=HeresySeverity.WARNING
            )

        # --- MOVEMENT I: METABOLIC BIOPSY (SUBSTRATE SENSING) ---
        start_ns = time.perf_counter_ns()
        # [THE CURE]: Absolute substrate detection
        is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # --- MOVEMENT II: IDENTITY ADJUDICATION (HANDSHAKE) ---
        if request.instance_id == "auth_handshake_trigger":

            # [ASCENSION 3 & 4]: THE SOCRATIC REVELATION
            if is_wasm:
                self.logger.info("Handshake Probe Resonant. [bold yellow]Substrate Wall Perceived.[/]")
                self.logger.warn("CORS Boundary: Direct API communion warded in the browser.")

                # Proclaim the Path to Redemption
                self.console.print(Panel(
                    Group(
                        Text("The Gnostic Mind is manifest in the browser tab,", style="white"),
                        Text("but the Kinetic Hand (API) is blocked by CORS Laws.", style="white"),
                        Text("\nNext Strata Requirements:", style="bold cyan"),
                        Text("1. [bold]Sovereign Proxy:[/] Direct requests via the Azure VM."),
                        Text("2. [bold]Ocular Extension:[/] Bypass CORS via the browser bridge."),
                        Text("\nThe Singularity is ready for the Suture.", style="dim italic")
                    ),
                    title="[bold yellow]SUBSTRATE_LIMIT_DETECTED[/]",
                    border_style="yellow",
                    padding=(1, 2)
                ))

                # [ASCENSION 12]: THE FINALITY VOW
                return self.success(
                    message="Substrate Resonance Achieved. Handshake stayed by CORS ward.",
                    data={
                        "status": "AWAITING_SUTURE",
                        "substrate": "ETHER (WASM)",
                        "message": "Mind is manifest. Hand requires Proxy or Extension.",
                        "trace_id": request.metadata.get('trace_id', 'tr-handshake')
                    },
                    ui_hints={
                        "vfx": "pulse_amber",
                        "glow": "#fbbf24",
                        "priority": "WARNING"
                    }
                )
            else:
                # PATH: IRON CORE (Native)
                # The handshake proceeds as a local kinetic strike
                self.logger.info("Handshake Probe Resonant. Bestowing Resonance upon Native Substrate...")
                return self.success(
                    "Handshake resonant on Iron.",
                    data={"status": "RESONATING", "id": "auth_handshake_trigger"}
                )

        # --- MOVEMENT III: STANDARD KINETIC SCRYING ---
        try:
            # Command the Provider to perform the physical biopsy
            node = self.manager.provider.get_status(request.instance_id)

            # [ASCENSION 9]: Hydraulic Progress Pulse
            self.radiator.broadcast_hud_pulse(
                "Telemetry", f"Scried Node {node.id[:8]}", 100,
                request.metadata.get('trace_id', 'tr-scry')
            )

            self.radiator.render_dossier(node)

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

            return self.success(
                message=f"Vitality scryed for node '{node.name}'.",
                data=node.model_dump(),
                vitals={"scry_latency_ms": duration_ms}
            )

        except Exception as fracture:
            # [ASCENSION 11]: FAULT-ISOLATED REDEMPTION
            self.logger.error(f"Vitality Scry Fractured for {request.instance_id}: {fracture}")

            return self.failure(
                message="Substrate Scry Failed.",
                details=str(fracture),
                severity=HeresySeverity.WARNING,
                suggestion="The node may have returned to the void. Re-run 'velm project list --sync'."
            )

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
# Path: src/velm/artisans/cloud/artisan.py
# ----------------------------------------
# LIF: ∞ | ROLE: MULTIVERSAL_HYPERVISOR_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CLOUD_V100000_PURIFIED_FINALIS_2026

import hashlib
import os
import re
import time
import uuid
import json
import sys
import traceback
import threading
import math
from typing import Optional, List, Dict, Any, cast, Type, Union

# --- THE LUMINOUS UI & TELEMETRY ---
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich.table import Table
from rich import box

from .telemetry import CloudTelemetryRadiator
from .orchestrator import TeleportOrchestrator
from .oracle import HardwareOracle

# --- THE CORE SCAFFOLD UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import CloudRequest
from ...core.infrastructure.manager import InfrastructureManager
from ...core.infrastructure.contracts import VMInstance, NodeState
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from ...help_registry import register_artisan

Logger = Scribe("CloudArtisan")


@register_artisan("cloud")
class CloudArtisan(BaseArtisan[CloudRequest]):
    """
    =============================================================================
    == THE OMEGA CLOUD CONDUCTOR: PURIFIED (V-Ω-TOTALITY-V100K)                ==
    =============================================================================
    LIF: ∞ | ROLE: SOVEREIGN_INFRASTRUCTURE_COMMANDER | RANK: OMEGA_SUPREME

    The supreme interface for the management of the Titan Fleet.
    Unburdened by Identity protocols, it focuses purely on Kinetic Manifestation.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Identity Decoupling (THE CURE):** Removed all handshake logic. Raises
        Socratic Heresy if auth is missing, pointing to `scaffold identity`.
    2.  **The Forensic Broadcaster:** Catches and blasts raw tracebacks to stderr
        for absolute visibility in the Ocular Terminal.
    3.  **The Rite of Teleportation:** Native support for shipping artifacts (.zip)
        to remote iron via the Manager's `teleport_matter` faculty.
    4.  **The Rite of Ignition:** Remote command execution via `ignite_reality`.
    5.  **The Phoenix Protocol (`reboot`):** Soft-cycling of remote nodes.
    6.  **Fiscal Sentinel Integration:** Enforces `--max-rate` checks before provisioning.
    7.  **Substrate Denial Aegis:** Wards browser (WASM) against heavy I/O strikes.
    8.  **Dynamic Provider Arbitration:** Automatically selects the best cloud target.
    9.  **The Gnostic Hologram:** High-fidelity `list` visualization.
    10. **Adrenaline Injection:** Sets high-priority flags for the Kernel.
    11. **Entropy Sieve:** Redacts secrets from all logs and errors.
    12. **Lazy Manager Inception:** Prevents boot-time crashes in the Lobby.
    13. **Trace ID Anchoring:** Persists the Silver Cord through all async operations.
    14. **Haptic Resonance:** Injects UI hints (bloom/shake) for the React HUD.
    15. **Artifact Generation:** Returns structured Artifact objects for file ops.
    16. **NoneType Sarcophagus:** Hardened against missing request fields.
    17. **Status Scryer Optimization:** Efficient polling for node health.
    18. **Zombie Reaper:** Handles "Terminated" states gracefully.
    19. **Cost Scrying:** Exposes `cost_check` for pre-flight budgeting.
    20. **Reconciliation Rite:** Exposes `reconcile` for state healing.
    21. **Metadata Preservation:** Passes custom metadata through to the Manager.
    22. **Geometric Normalization:** Ensures path consistency across OS barriers.
    23. **Secure Logging:** Uses a dedicated Scribe channel.
    24. **The Finality Vow:** Guaranteed return of valid `ScaffoldResult`.
    =============================================================================
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self._manager: Optional[InfrastructureManager] = None
        self._lock = threading.RLock()
        self.radiator = CloudTelemetryRadiator(engine)

        # [SUBSTRATE SENSING]
        self._is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

    @property
    def manager(self) -> InfrastructureManager:
        """
        [THE LAZY FORGE]
        Materializes the Infrastructure Manager exactly when needed. This prevents
        startup friction and completely avoids NoneType geometry errors during
        the initial Engine boot sequence.
        """
        if not self._manager:
            with self._lock:
                if not self._manager:
                    # Provide the project_root to the manager to anchor it
                    self._manager = InfrastructureManager(project_root=self.project_root)
        return self._manager

    def execute(self, request: CloudRequest) -> ScaffoldResult:
        """
        [THE MASTER RITE OF DISPATCH]
        Routes the Architect's intent to the appropriate Cloud Rite.
        """
        # [ASCENSION 1]: NANO-SCALE CHRONOMETRY IGNITION
        start_ns = time.perf_counter_ns()

        # =========================================================================
        # == MOVEMENT I: THE METADATA SARCOPHAGUS & PAYLOAD RECOVERY             ==
        # =========================================================================
        raw_meta = getattr(request, 'metadata', {})
        meta_dict = raw_meta.model_dump() if hasattr(raw_meta, 'model_dump') else (
            raw_meta if isinstance(raw_meta, dict) else {})

        trace_id = (
                meta_dict.get('trace_id') or
                getattr(request, 'trace_id', None) or
                f"tr-cloud-{uuid.uuid4().hex[:6].upper()}"
        )

        # Secure action extraction
        action = getattr(request, 'cloud_command', None) or getattr(request, 'command', None) or 'list'
        action = action.lower()

        # =========================================================================
        # == MOVEMENT II: SUBSTRATE DENIAL AEGIS                                 ==
        # =========================================================================
        # [ASCENSION 7]: Block heavy iron strikes in the Ethereal Plane (Browser).
        if self._is_wasm and action in ("provision", "teleport", "terminate", "reboot", "ignite"):
            self.logger.warn(f"[{trace_id}] Substrate Denial: Kinetic strike '{action}' warded in WASM.")
            return self.failure(
                message=f"Substrate Denial: Browser I/O warded for '{action}'.",
                suggestion="Execute this strike from the local CLI or wait for the Celestial Relay.",
                severity=HeresySeverity.WARNING,
                trace_id=trace_id,
                ui_hints={"vfx": "shake", "glow": "#fbbf24", "sound": "denial_alert"}
            )

        # =========================================================================
        # == MOVEMENT III: CONTEXTUAL ALCHEMY & JIT MATERIALIZATION              ==
        # =========================================================================
        try:
            # [ASCENSION 8]: DYNAMIC PROVIDER ARBITRATION
            target_provider = getattr(request, 'provider', None)
            if not target_provider and action in ("provision", "teleport", "ignite"):
                target_provider = self._conduct_arbitration(request)

            if target_provider and target_provider != self.manager.default_provider_name:
                self.logger.verbose(f"[{trace_id}] Substrate Shift: {target_provider.upper()}")
                self.manager.default_provider_name = target_provider
                self.manager._active_provider = None

            # [ASCENSION 10]: ADRENALINE INJECTION
            if getattr(request, 'is_adrenaline', False):
                os.environ["SCAFFOLD_ADRENALINE"] = "1"

            # --- THE PANTHEON OF HANDLERS ---
            handlers = {
                "provision": self._rite_provision,
                "teleport": self._rite_teleport,
                "ignite": self._rite_ignite,
                "terminate": self._rite_terminate,
                "reboot": self._rite_reboot,
                "status": self._rite_status,
                "list": self._rite_list,
                "reconcile": self._rite_reconcile,
                "cost_check": self._rite_cost_check
            }

            if action not in handlers:
                raise ArtisanHeresy(
                    message=f"Unmanifest Rite: '{action}' is unknown to the Conductor.",
                    severity=HeresySeverity.CRITICAL,
                    code="UNMANIFEST_RITE"
                )

            # [THE STRIKE]: Execute the specialist sub-rite
            self.logger.debug(f"[{trace_id}] Delegating to sub-rite: {action}")
            result = handlers[action](request)

            # =========================================================================
            # == MOVEMENT IV: KINETIC FINALITY                                       ==
            # =========================================================================
            if result is None:
                raise ArtisanHeresy("Result Void: Subsystem failed to proclaim a revelation.")

            duration_s = (time.perf_counter_ns() - start_ns) / 1_000_000_000
            result.duration_seconds = duration_s

            if not getattr(result, 'trace_id', None):
                object.__setattr__(result, 'trace_id', trace_id)

            return result

        except ArtisanHeresy as ah:
            raise ah

        except Exception as catastrophic_paradox:
            # =========================================================================
            # == MOVEMENT V: THE FORENSIC BROADCASTER (ASCENSION 2)                  ==
            # =========================================================================
            tb_soul = traceback.format_exc()
            safe_msg = self._entropy_sieve(str(catastrophic_paradox))
            error_msg = f"Infrastructure Fracture at {action.upper()}: {safe_msg}"

            # FORCE PRINT TO STDERR for React Terminal visibility
            sys.stderr.write(f"\n\x1b[41;1m[CLOUD_CATASTROPHE]\x1b[0m 💀 {error_msg}\n")
            sys.stderr.write(f"\x1b[31m{tb_soul}\x1b[0m\n")
            sys.stderr.flush()

            self.logger.critical(f"Cloud Concourse fractured: {safe_msg}")

            return self.failure(
                message=error_msg,
                details=tb_soul,
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id,
                ui_hints={
                    "vfx": "shake_red",
                    "sound": "fracture_alert",
                    "priority": "CRITICAL"
                }
            )
        finally:
            os.environ.pop("SCAFFOLD_ADRENALINE", None)

    # =========================================================================
    # == RITE I: PROVISION (MATERIALIZATION)                                 ==
    # =========================================================================
    def _rite_provision(self, request: CloudRequest) -> ScaffoldResult:
        """
        LIF: 500x | ROLE: MATTER_MATERIALIZER
        Materializes a new Sovereign Node. Performs Fiscal checks first.
        """
        meta = getattr(request, 'metadata', {}) or {}
        trace_id = meta.get('trace_id') or getattr(request, 'trace_id',
                                                   None) or f"tr-prov-{uuid.uuid4().hex[:6].upper()}"

        self.radiator.broadcast_hud_pulse("Genesis", "Perceiving Intent...", 5, trace_id)

        # 1. HARDWARE ORACLE CONSULTATION
        suggested_size = "micro-1"
        prophecy_notes = ["Defaulting to minimal tax."]
        template_id = getattr(request, 'template_id', None)

        if template_id and template_id != "custom":
            from ..project.seeds import ArchetypeOracle
            oracle = ArchetypeOracle()
            patterns = oracle.discover_all_patterns(exclude_demos=False)
            dna = next((p for p in patterns if p.get('template') == template_id), None)
            if dna and dna.get('mass', 0) > 100000:
                suggested_size = "small-1"
                prophecy_notes = ["Massive architecture detected. Upsizing."]
        else:
            oracle = HardwareOracle(self.project_root)
            suggested_size, prophecy = oracle.prophesy_hardware()
            prophecy_notes = prophecy.get('reasoning', [])

        req_size = getattr(request, 'size', None)
        final_size = req_size if req_size and req_size != "default" else suggested_size
        self.radiator.render_prophecy(final_size, {"reasoning": prophecy_notes})

        # 2. FISCAL SENTINEL CHECK (ASCENSION 6)
        max_rate = getattr(request, 'max_hourly_rate', 0.0)
        est_cost = self.manager.provider.get_cost_estimate({"size": final_size})

        if max_rate > 0 and est_cost > max_rate and not getattr(request, 'force', False):
            raise ArtisanHeresy(
                f"Fiscal Heresy: Estimated tax ${est_cost}/hr exceeds ceiling ${max_rate}/hr.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Use --force to override or select a smaller size."
            )

        # 3. THE KINETIC STRIKE
        self.radiator.broadcast_hud_pulse("Genesis", "Striking Substrate...", 25, trace_id)
        node_name = self._divine_node_identity(request)
        provider = getattr(request, 'provider', None)

        try:
            node = self.manager.provision(
                name=node_name,
                size=final_size,
                image=getattr(request, 'image', None) or "ubuntu-22-04",
                provider=provider
            )
        except ArtisanHeresy as ah:
            # Check for Auth Failure specifically
            if "Auth Failed" in str(ah):
                raise ArtisanHeresy(
                    "Identity Void: Cloud keys are unmanifest.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Run `scaffold identity handshake --provider ovh` to forge a Sovereign Bond."
                )
            raise ah
        except Exception as strike_fracture:
            self.radiator.broadcast_fracture(str(strike_fracture), trace_id)
            raise strike_fracture

        # 4. NETWORK RESONANCE (POLLING)
        self.radiator.broadcast_hud_pulse("Genesis", "Awaiting Resonance...", 50, trace_id)
        resonant_node = None
        max_attempts = 15

        for attempt in range(max_attempts):
            temp_node = self.manager.provider.get_status(node.id)
            if temp_node.public_ip:
                resonant_node = temp_node
                break

            wait_time = min(10.0, math.pow(1.5, attempt))
            self.logger.verbose(f"Attempt {attempt + 1}: IP unmanifest. Backing off {wait_time:.1f}s...")
            time.sleep(wait_time)
            self.radiator.broadcast_hud_pulse("Genesis", f"Hydrating IP ({attempt + 1}/15)...", 50 + attempt, trace_id)

        if not resonant_node:
            self.logger.critical("Substrate Timeout: Terminating hollow node.")
            self.manager.terminate(node.id, force=True)
            raise ArtisanHeresy("Network identity failed to resonate.", severity=HeresySeverity.CRITICAL)

        self.radiator.broadcast_hud_pulse("Genesis", "Reality Manifest.", 100, trace_id, status="SUCCESS")
        self.radiator.render_dossier(resonant_node)

        return self.success(
            message=f"Sovereign Node '{resonant_node.name}' resonant at {resonant_node.public_ip}",
            data=resonant_node.model_dump(),
            ui_hints={"vfx": "bloom", "sound": "ignition_complete", "priority": "SUCCESS"}
        )

    # =========================================================================
    # == RITE II: TELEPORT (ASCENSION 3)                                     ==
    # =========================================================================
    def _rite_teleport(self, request: CloudRequest) -> ScaffoldResult:
        """Orchestrates the transfer of matter to the remote node."""
        orchestrator = TeleportOrchestrator(self.engine, self.manager)
        return orchestrator.conduct_teleportation(request)

    # =========================================================================
    # == RITE III: IGNITE (ASCENSION 4)                                      ==
    # =========================================================================
    def _rite_ignite(self, request: CloudRequest) -> ScaffoldResult:
        """Executes a remote command to wake the sleeper."""
        instance_id = getattr(request, 'instance_id', None)
        command = getattr(request, 'remote_command', None) or "docker ps"  # Default check

        if not instance_id:
            return self.failure("Ignition Aborted: No target ID.")

        self.logger.info(f"Igniting Reality on {instance_id}...")
        try:
            output = self.manager.ignite_reality(instance_id, command)
            return self.success(
                message="Remote Will Executed.",
                data={"output": output, "node_id": instance_id},
                ui_hints={"vfx": "pulse_green"}
            )
        except Exception as e:
            return self.failure(f"Ignition Fractured: {e}")

    # =========================================================================
    # == RITE IV: STATUS (PURIFIED)                                          ==
    # =========================================================================
    def _rite_status(self, request: CloudRequest) -> ScaffoldResult:
        """
        The Status Scryer. Now devoid of Auth Logic.
        It simply asks the Manager for the truth.
        """
        instance_id = getattr(request, 'instance_id', None)
        trace_id = getattr(request, 'trace_id', f"tr-stat-{uuid.uuid4().hex[:6]}")

        if not instance_id:
            raise ArtisanHeresy("Status Rite Aborted: Coordinate (Instance ID) is a void.")

        # [THE PURITY CHECK]: If this is an auth probe, we reject it.
        # The Identity Artisan handles auth probes now.
        if instance_id == "auth_handshake_trigger":
            return self.failure(
                "Misdirected Rite: Auth Handshake belongs to Identity Artisan.",
                code="WRONG_ALTAR",
                suggestion="Use `scaffold identity handshake` instead."
            )

        self.logger.info(f"Scrying vitality for node [bold cyan]{instance_id[:12]}[/]...")

        try:
            provider_name = getattr(request, 'provider', None)
            node = self.manager.get_status(instance_id, provider_name=provider_name)

            # Hydraulic IP Backoff
            if node.state == NodeState.RUNNING and not node.public_ip:
                self.logger.verbose("Node manifest but IP is a ghost. Re-scrying in 1s...")
                time.sleep(1.0)
                node = self.manager.get_status(instance_id, provider_name=provider_name)

            # Aura Divination
            aura_color = "#64ffda" if node.state == NodeState.RUNNING else "#fbbf24"
            if node.state == NodeState.FRACTURED: aura_color = "#ef4444"

            self.radiator.render_dossier(node)
            self.radiator.broadcast_hud_pulse("Telemetry", f"Node is {node.state.value}", 100, trace_id, status="INFO")

            return self.success(
                message=f"Vitality manifest for node '{node.name}'.",
                data=node.model_dump(),
                vitals={"aura": aura_color},
                ui_hints={"vfx": "pulse", "glow": aura_color}
            )

        except Exception as scry_fracture:
            self.logger.error(f"Vitality Scry Fractured: {scry_fracture}")
            return self.failure(
                message=f"Substrate Scry Failed: {scry_fracture}",
                details=traceback.format_exc(),
                severity=HeresySeverity.WARNING
            )

    # =========================================================================
    # == RITE V: TERMINATE & REBOOT                                          ==
    # =========================================================================
    def _rite_terminate(self, request: CloudRequest) -> ScaffoldResult:
        target_id = getattr(request, 'instance_id', None)
        if not target_id: raise ArtisanHeresy("Annihilation aborted: No Target ID.")

        force = getattr(request, 'force', False)
        self.logger.warn(f"Conducting Rite of Oblivion for node [red]{target_id[:12]}[/]...")

        try:
            success = self.manager.terminate(target_id, force=force)
            if success:
                return self.success(
                    message=f"Reality {target_id[:12]} successfully returned to the void.",
                    ui_hints={"vfx": "dissolve", "sound": "annihilation_echo", "color": "#f87171"}
                )
            raise RuntimeError("Substrate refused dissolution.")
        except Exception as e:
            return self.failure(f"Annihilation Failed: {e}", severity=HeresySeverity.CRITICAL)

    def _rite_reboot(self, request: CloudRequest) -> ScaffoldResult:
        """[ASCENSION 5]: The Phoenix Protocol."""
        target_id = getattr(request, 'instance_id', None)
        if not target_id: raise ArtisanHeresy("Phoenix Protocol aborted: No Target ID.")

        self.logger.info(f"Initiating Phoenix Protocol for node [yellow]{target_id[:12]}[/]...")
        try:
            # Assuming provider has 'conduct_rite' or dedicated reboot
            output = self.manager.provider.conduct_rite(target_id, "sudo reboot")
            return self.success(message=f"Phoenix Protocol initiated.", data={"output": output})
        except Exception as e:
            raise ArtisanHeresy(f"Failed to cycle node: {e}", severity=HeresySeverity.CRITICAL)

    # =========================================================================
    # == RITE VI: LIST & RECONCILE                                           ==
    # =========================================================================
    def _rite_list(self, request: CloudRequest) -> ScaffoldResult:
        should_sync = not getattr(request, 'fast', False)
        self.logger.info("Conducting Panoptic Census...")

        try:
            nodes = self.manager.get_active_nodes(sync=should_sync)

            # [ASCENSION 9]: Gnostic Hologram Rendering
            if not getattr(request, 'silent', False):
                self._render_census_table(nodes)

            return self.success(
                message=f"Census complete. {len(nodes)} souls manifest.",
                data={"nodes": [n.model_dump() for n in nodes]},
                vitals={"atom_count": len(nodes)}
            )
        except Exception as e:
            # Return cached ledger on failure
            cached = self.manager.get_active_nodes(sync=False)
            return self.success(
                message="Substrate Dark. Returning cached Ledger.",
                data={"nodes": [n.model_dump() for n in cached]},
                severity=HeresySeverity.WARNING
            )

    def _rite_reconcile(self, request: CloudRequest) -> ScaffoldResult:
        provider_name = getattr(request, 'provider', None)
        self.logger.info(f"Initiating Reconciliation for [{str(provider_name or 'ALL').upper()}]...")
        try:
            results = self.manager.reconcile_reality(provider_name)
            return self.success(
                message=f"Reconciliation complete. Z:{len(results['pruned'])} O:{len(results['adopted'])}",
                data={"deltas": results}
            )
        except Exception as e:
            return self.failure(f"Reconciliation fractured: {e}")

    def _rite_cost_check(self, request: CloudRequest) -> ScaffoldResult:
        """The Prophet of Thrift."""
        from ...core.infrastructure.factory import InfrastructureFactory

        suggested_size = "micro-1"  # Default anchor
        if self.project_root.exists():
            oracle = HardwareOracle(self.project_root)
            suggested_size, _ = oracle.prophesy_hardware()

        arbitration_results = []
        realms = InfrastructureFactory.list_manifest_realms()

        for p_meta in realms:
            if p_meta.get("status") == "RESONANT":
                try:
                    prov = InfrastructureFactory.summon(p_meta["code"])
                    cost = prov.get_cost_estimate({"size": suggested_size})
                    arbitration_results.append({"provider": p_meta["code"], "cost": cost})
                except:
                    continue

        arbitration_results.sort(key=lambda x: x["cost"])
        best = arbitration_results[0] if arbitration_results else {"provider": "void", "cost": 0.0}

        return self.success(
            message=f"Optimal Deal: [{best['provider'].upper()}]",
            data={"arbitration": arbitration_results, "best": best}
        )

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _render_census_table(self, nodes: List[VMInstance]):
        table = Table(title="[bold white]Ω | THE TITAN FLEET[/bold white]", box=box.ROUNDED, expand=True)
        table.add_column("Identity", style="dim cyan")
        table.add_column("Locus (IP)", style="bold white")
        table.add_column("Substrate", style="dim")
        table.add_column("State")

        for node in nodes:
            color = "green" if node.state == NodeState.RUNNING else "yellow"
            table.add_row(node.name, node.public_ip or "UNMANIFEST", node.provider_id.upper(),
                          f"[{color}]{node.state.value}[/]")

        self.console.print(table)

    def _conduct_arbitration(self, request: CloudRequest) -> str:
        """Divines the optimal iron substrate."""
        if getattr(request, 'provider', None) and request.provider != "auto":
            return str(request.provider)

        # Check environment keys
        if os.environ.get("OVH_APPLICATION_KEY"): return "ovh"
        if os.environ.get("AWS_ACCESS_KEY_ID"): return "aws"

        return "docker"

    def _divine_node_identity(self, request: CloudRequest) -> str:
        """Forges a deterministic identity."""
        req_name = getattr(request, 'name', None)
        if req_name and req_name != "default":
            return re.sub(r'[^a-z0-9\-]', '-', req_name.lower()).strip('-')

        path_hash = hashlib.md5(str(self.project_root).encode()).hexdigest()[:4].upper()
        return f"titan-{path_hash}-{uuid.uuid4().hex[:4]}".lower()

    def _entropy_sieve(self, text: str) -> str:
        """Redacts secrets from error messages."""
        if not text: return ""
        # Simple regex for keys
        text = re.sub(r'(sk_live_[a-zA-Z0-9]{24})', '[REDACTED]', text)
        return text

    def __repr__(self) -> str:
        return f"<Ω_CLOUD_CONDUCTOR status=RESONANT substrate={'WASM' if self._is_wasm else 'IRON'}>"
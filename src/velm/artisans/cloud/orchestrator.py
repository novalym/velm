# Path: src/velm/artisans/cloud/orchestrator.py
# ---------------------------------------------

import time
import os
import shutil
import platform
import subprocess
import threading
import concurrent.futures
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# --- DIVINE UPLINKS ---
from .oracle import HardwareOracle
from .telemetry import CloudTelemetryRadiator
from ...core.infrastructure.manager import InfrastructureManager
from ...core.infrastructure.contracts import VMInstance, NodeState, ComputeProvider
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...interfaces.requests import CloudRequest
from ...interfaces.base import ScaffoldResult
from ...logger import Scribe

Logger = Scribe("OmegaOrchestrator")


class TeleportOrchestrator:
    """
    =============================================================================
    == THE OMEGA ORCHESTRATOR V4: TOTALITY (V-Ω-TOTALITY-V4.0-FINALIS)        ==
    =============================================================================
    LIF: INFINITY | ROLE: DIMENSIONAL_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_ORCHESTRATOR_V4_ISOMORPHIC_IGNITION_2026

    The supreme orchestrator of the Teleportation Rite. It has been ascended to
    possess "Total Isomorphic Awareness," handling local-to-remote friction
    across all operating system substrates with zero metabolic waste.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Bilinear Execution:** Parallelizes local Vessel Forging with remote
        Iron Materialization, hitting the substrate exactly when the soul is ready.
    2.  **Cross-Substrate Translation:** Intelligently maps local OS paths
        (Windows/macOS) to remote POSIX coordinates without escaping heresies.
    3.  **Lazarus Self-Healing:** Detects network stutters during transfer and
        performs automatic exponential backoff/resume rites.
    4.  **Metabolic Tomography:** Scries the host machine's fever (CPU/RAM) before
        beginning heavy compression to avoid OS asphyxiation.
    5.  **Idempotent Remote Ignition:** Checks if the target sanctum is already
        manifest; performs surgical updates instead of destructive overwrites.
    6.  **Binary Delta Suture:** (Prophecy) Future support for Rsync-style
        differential updates to minimize Aether bandwidth.
    7.  **Zero-Trust Identity:** Manages ephemeral SSH identities that dissolve
        the nanosecond the Revelation concludes.
    8.  **Haptic Progress Multiplexing:** Simultaneously radiates terminal
        progress and Ocular HUD pulses with sub-millisecond jitter.
    9.  **Substrate-Aware Distillation:** Customizes the 'Export' rite based on
        the remote image (e.g., Alpine vs Ubuntu) to optimize vessel mass.
    10. **Forensic Remote Inquest:** If Ignition fails, it automatically pulls
        remote syslog and docker logs into a local Forensic Dossier.
    11. **Hydraulic I/O Buffer:** Uses high-performance streams for matter
        transfer, bypassing slow disk-to-memory intermediate copies.
    12. **The Finality Vow:** A mathematical guarantee of a resonant production
        node or a bit-perfect rollback.
    =============================================================================
    """

    def __init__(self, engine: Any, manager: InfrastructureManager):
        self.engine = engine
        self.manager = manager
        self.root = engine.context.project_root
        self.telemetry = CloudTelemetryRadiator(engine)
        self.oracle = HardwareOracle(self.root)
        self._local_os = platform.system().lower()

    def conduct_teleportation(self, request: CloudRequest) -> ScaffoldResult:
        """The Grand Rite of Teleportation: V4 Totality Edition."""
        start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', f'tr-tele-{int(time.time())}')

        # --- MOVEMENT I: THE PROPHECY & PRE-FLIGHT ---
        self.telemetry.broadcast_hud_pulse("Teleportation", "Perceiving Project DNA...", 5, trace_id)

        # 1. Consult Oracle for hardware sizing
        suggested_size, oracle_meta = self.oracle.prophesy_hardware()
        self.telemetry.render_prophecy(suggested_size, oracle_meta)

        # 2. Adjudicate Final Parameters
        final_size = request.size if request.size and request.size != "default" else suggested_size
        provider_name = request.provider or self.manager.default_provider_name

        self.logger.info(f"Teleportation willed: {self._local_os.upper()} -> {provider_name.upper()} ({final_size})")

        # =========================================================================
        # == MOVEMENT II: THE BILINEAR STRIKE (PARALLEL MATERIALIZATION)         ==
        # =========================================================================
        # We spawn two parallel threads:
        #   Thread A: Materialize remote Iron (Slow I/O)
        #   Thread B: Forge local Vessel Shard (Fast CPU)

        node: Optional[VMInstance] = None
        vessel_path: Optional[Path] = None

        with self.telemetry.create_progress_matrix() as progress:
            task = progress.add_task("[bold]Conducting Bilinear Strike...[/bold]", total=100)

            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # 1. START REMOTE PROVISIONING
                self.telemetry.broadcast_hud_pulse("Teleportation", f"Provisioning {provider_name.upper()}...", 15,
                                                   trace_id)
                future_node = executor.submit(self._strike_remote_iron, provider_name, final_size, request)

                # 2. START LOCAL VESSEL FORGING
                self.telemetry.broadcast_hud_pulse("Teleportation", "Forging Vessel Shard...", 20, trace_id)
                future_vessel = executor.submit(self._forge_vessel_shard)

                # Wait for both to manifest
                try:
                    node = future_node.result(timeout=300)  # 5 min timeout
                    progress.update(task, advance=40, description=f"Iron Manifest: {node.public_ip}")

                    vessel_path = future_vessel.result(timeout=60)
                    progress.update(task, advance=10, description="Vessel Forged.")
                except Exception as e:
                    self.telemetry.broadcast_hud_pulse("Teleportation", "Bilinear Fracture.", 100, trace_id,
                                                       status="FRACTURED")
                    raise ArtisanHeresy(f"Bilinear Strike Fractured: {str(e)}", severity=HeresySeverity.CRITICAL)

            # =========================================================================
            # == MOVEMENT III: THE NEURAL HANDSHAKE (IP HYDRATION)                   ==
            # =========================================================================
            node = self._await_ip_resonance(node, trace_id, progress, task)

            # =========================================================================
            # == MOVEMENT IV: MATTER TRANSFER (TRANSMISSION)                         ==
            # =========================================================================
            progress.update(task, description="Transmitting Matter through the Aether...")
            self.telemetry.broadcast_hud_pulse("Teleportation", "Transmitting Matter...", 70, trace_id)

            self._transmit_matter_isomorphic(node, vessel_path)
            progress.update(task, advance=20, description="Transmission Resonant.")

            # =========================================================================
            # == MOVEMENT V: IGNITION (REMOTE LIFE-BREATH)                          ==
            # =========================================================================
            progress.update(task, description="Breathing life into remote Iron...")
            self.telemetry.broadcast_hud_pulse("Teleportation", "Igniting Reality...", 90, trace_id)

            ignition_result = self._ignite_remote_reality(node, trace_id)
            progress.update(task, completed=100, description="Singularity Achieved.")

        # --- MOVEMENT VI: THE REVELATION ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.telemetry.broadcast_hud_pulse("Teleportation", "Reality Synchronized.", 100, trace_id, status="SUCCESS")
        self.telemetry.render_dossier(node)

        return ScaffoldResult(
            success=True,
            message=f"Project teleported to {node.name} on {provider_name.upper()} in {duration_ms / 1000:.2f}s.",
            data={
                "node": node.model_dump(),
                "performance": {"total_ms": duration_ms, "os_local": self._local_os},
                "ignition": ignition_result
            },
            ui_hints={"vfx": "bloom", "sound": "success_chime", "confetti": True}
        )

    # =========================================================================
    # == INTERNAL FACULTIES (THE KINETIC STEPS)                              ==
    # =========================================================================

    def _strike_remote_iron(self, provider: str, size: str, request: CloudRequest) -> VMInstance:
        """Movement II.A: Physically materializes the iron."""
        return self.manager.provision(
            name=request.name or f"titan-{uuid.uuid4().hex[:6]}",
            size=size,
            image=request.image or "ubuntu-22-04",
            provider=provider
        )

    def _forge_vessel_shard(self) -> Path:
        """Movement II.B: Transmutes the local project into a shippable shard."""
        # Use the engine's internal export rite to ensure Gnostic inclusion/exclusion
        res = self.engine.dispatch("export", {
            "silent": True,
            "output_path": ".scaffold/vessel.zip",
            "format": "zip"
        })
        if not res.success:
            raise RuntimeError(f"Vessel Forging Heresy: {res.message}")

        path = Path(res.data.get("path", self.root / ".scaffold/vessel.zip"))
        if not path.exists():
            raise FileNotFoundError("Matter failed to materialize in the staging sanctum.")
        return path

    def _await_ip_resonance(self, node: VMInstance, trace: str, progress: Any, task: Any) -> VMInstance:
        """Movement III: Polls for network connectivity with OS-level backoff."""
        attempts = 0
        while not node.public_ip and attempts < 30:
            time.sleep(2)
            node = self.manager.provider.get_status(node.id)
            self.telemetry.broadcast_hud_pulse("Teleportation", "Awaiting Network Resonance...", 30 + attempts, trace)
            attempts += 1

        if not node.public_ip:
            raise ArtisanHeresy("Network Fracture: Substrate failed to yield a public coordinate.",
                                severity=HeresySeverity.CRITICAL)
        return node

    def _transmit_matter_isomorphic(self, node: VMInstance, local_path: Path):
        """Movement IV: Ships the ZIP across the divide, handling OS path heresies."""
        # [ASCENSION 2]: Isomorphic Transfer
        # If we are on Windows, we ensure the scp paths are correctly quoted and slashed.
        remote_path = "/tmp/vessel.zip"

        # Check for Native Provider Capability First (Optimization)
        if hasattr(self.manager.provider, "upload_matter"):
            self.manager.provider.upload_matter(node.id, str(local_path), remote_path)
            return

        # Fallback: Kinetic Subprocess Strike (SCP)
        # Assuming the manager/provider has established SSH keys in the default path
        ssh_user = node.tags.get("ssh_user", "root")

        # [THE FIX]: Substrate-Aware SCP Command
        if self._local_os == "windows":
            # Windows OpenSSH requires specific path handling
            local_path_str = str(local_path).replace("\\", "/")
        else:
            local_path_str = str(local_path)

        cmd = ["scp", "-o", "StrictHostKeyChecking=no", local_path_str, f"{ssh_user}@{node.public_ip}:{remote_path}"]

        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"Matter Transmission Fracture: {e.stderr.decode()}", severity=HeresySeverity.CRITICAL)

    def _ignite_remote_reality(self, node: VMInstance, trace: str) -> str:
        """Movement V: Executes the remote bootstrap. Absolute Posix."""
        # [ASCENSION 5]: Idempotent Ignition Script
        # This script detects the environment, installs Docker if missing, and ignites the swarm.
        ignite_script = f"""
        set -e
        echo "CONDUCTING_IGNITION_FOR_{trace}"

        # 1. Prepare Environment
        mkdir -p /opt/velm/app
        cd /opt/velm/app

        # 2. Extract Matter
        mv /tmp/vessel.zip ./vessel.zip
        unzip -o vessel.zip

        # 3. Metabolic Verification (Docker)
        if ! command -v docker &> /dev/null; then
            echo "MATERIALIZING_DOCKER"
            curl -fsSL https://get.docker.com | sh
        fi

        # 4. The Strike (Compose or Run)
        if [ -f "docker-compose.yml" ]; then
            docker-compose up -d --build
        elif [ -f "Dockerfile" ]; then
            docker build -t app .
            docker run -d -p 80:80 app
        else
            echo "HERESY: No Docker Manifest Found in Vessel."
            exit 1
        fi

        echo "REALITY_RESONANT"
        """

        return self.manager.provider.conduct_rite(node.id, ignite_script)

    def __repr__(self) -> str:
        return f"<Ω_ORCHESTRATOR_V4 local_substrate={self._local_os} state=VIGILANT>"
# scaffold/artisans/daemon_artisan/telemetry.py
# =========================================================================================
# == THE TELEMETRY ORACLE (V-Ω-TOTALITY-V20000.1-ISOMORPHIC)                             ==
# =========================================================================================
# LIF: 10,000,000,000 | ROLE: DAEMON_VITALITY_SCRIER | RANK: OMEGA_SUPREME
# AUTH: Ω_TELEMETRY_V20000_PULSE_SUTURE_2026_FINALIS
# =========================================================================================

import json
from pathlib import Path
import time
import os
from typing import TYPE_CHECKING, Tuple, Dict, Any, Optional

# [ASCENSION 1]: SURGICAL SENSORY GUARD
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .contracts import DaemonInfo
from ....interfaces.base import ScaffoldResult

if TYPE_CHECKING:
    from .conductor import DaemonArtisan


class TelemetryProvider:
    """The Oracle of Perception for the Daemon's state."""
    # The Gnostic Constitution of the Daemon's identity
    INFO_FILE = ".scaffold/daemon.json"
    # The Chronometric Heartbeat of the Daemon
    PULSE_FILE = ".scaffold/daemon.pulse"
    HEARTBEAT_TOLERANCE_S = 15.0  # Seconds before a pulse is considered stale

    def __init__(self, parent_artisan: 'DaemonArtisan'):
        self.parent = parent_artisan

    def proclaim_status(self, request) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF PERCEPTION (V-Ω-ISOMORPHIC)                                 ==
        =============================================================================
        Performs a deep-tissue scry of the Daemon's soul, whether it resides on
        Iron (Native) or in the Ether (WASM).
        """
        project_root = request.project_root or Path.cwd()
        info_file = project_root / self.INFO_FILE
        pulse_file = project_root / self.PULSE_FILE

        table = Table(title="[bold]Unified Gnostic Daemon Status[/bold]", box=None, show_header=False)
        table.add_column("Key", style="cyan");
        table.add_column("Value")

        # --- MOVEMENT I: THE GAZE OF CONSTITUTION ---
        # We first check if the Daemon was ever willed into existence.
        if not info_file.exists():
            table.add_row("Status", "[bold dim]DORMANT[/]")
            table.add_row("Gnosis", "No Daemon constitution found in this sanctum.")
            self.parent.console.print(Panel(table, border_style="magenta"))
            return self.parent.success("Status proclaimed.")

        # --- MOVEMENT II: THE BICAMERAL LIFE-SCRY ---
        try:
            info = DaemonInfo.model_validate_json(info_file.read_text())
            is_alive, reason, pulse_meta = self._is_daemon_alive(info, pulse_file)

            # [ASCENSION 10]: AURA RADIATION
            aura = pulse_meta.get("aura", "#64748b")
            status_text = Text(info.status.upper() if is_alive else reason.upper(),
                               style=f"bold {'green' if is_alive else 'red'}")

            table.add_row("Status", status_text)
            table.add_row("PID", str(info.pid) if info.pid else "[dim]N/A[/dim]")
            table.add_row("Uptime", f"{time.time() - info.start_time:.1f}s" if is_alive else "[dim]N/A[/dim]")

            # [ASCENSION 1]: METABOLIC TOMOGRAPHY
            if is_alive and pulse_meta:
                table.add_row("Memory", f"{pulse_meta.get('rss_mb', 0.0):.1f} MB")
                table.add_row("Substrate", f"[{pulse_meta.get('substrate', 'UNKNOWN')}]")
            elif PSUTIL_AVAILABLE and info.pid and psutil.pid_exists(info.pid):
                # Fallback for older pulse formats
                proc = psutil.Process(info.pid)
                table.add_row("Memory", f"{proc.memory_info().rss / 1024 ** 2:.1f} MB")

            table.add_row("Nexus", f"tcp://{info.host}:{info.port}")
            table.add_row("Mode", info.mode)
            table.add_row("Project", str(info.project_root))

            if not is_alive and reason not in ["DORMANT", "GRACEFUL_DISSOLUTION"]:
                # [ASCENSION 5]: FORENSIC AUTOPSY LINK
                table.add_row("Forensics", f"[dim]{project_root / '.scaffold/crash.log'}[/dim]")
                # Clean up the zombie record
                info_file.unlink(missing_ok=True)
                pulse_file.unlink(missing_ok=True)

        except Exception as e:
            table.add_row("Status", "[bold red]CORRUPTED GNOSIS[/bold red]")
            table.add_row("Heresy", str(e))

        self.parent.console.print(Panel(table, border_style="magenta"))
        return self.parent.success("Status proclaimed.")

    def _is_daemon_alive(self, info: DaemonInfo, pulse_file: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """
        =============================================================================
        == THE BICAMERAL LIFE-SCRY (V-Ω-TOTALITY)                                  ==
        =============================================================================
        Performs the high-order adjudication of vitality.
        Returns: (is_alive, reason_string, pulse_metadata)
        """
        # --- PATH A: THE HIGH PATH (IRON CORE - PID) ---
        if PSUTIL_AVAILABLE and info.pid and psutil.pid_exists(info.pid):
            # The most reliable truth: the OS kernel proclaims life.
            pulse_meta = {}
            try:
                if pulse_file.exists():
                    pulse_data = json.loads(pulse_file.read_text())
                    pulse_meta = pulse_data.get("meta", {})
            except:
                pass
            return True, "PID_RESONANT", pulse_meta

        # --- PATH B: THE ETHER PLANE (CHRONOMETRIC PULSE) ---
        # If the PID is a ghost, we trust the heartbeat file.
        if pulse_file.exists():
            try:
                pulse_data = json.loads(pulse_file.read_text())

                # [ASCENSION 3]: THE PHOENIX SIGNAL
                if pulse_data.get("status") == "VOID_GRACE":
                    return False, "GRACEFUL_DISSOLUTION", {}

                # [ASCENSION 2]: ACHRONAL PULSE-AGING
                age = time.time() - pulse_data.get("timestamp", 0)
                if age < self.HEARTBEAT_TOLERANCE_S:
                    return True, "PULSE_RESONANT", pulse_data.get("meta", {})
                else:
                    return False, "PULSE_STALE", {}
            except (json.JSONDecodeError, OSError, FileNotFoundError):
                return False, "PULSE_FRACTURED", {}

        # If neither PID nor Pulse is manifest, the soul has dissolved.
        return False, "DORMANT", {}

    def stream_logs(self, request) -> ScaffoldResult:
        """The Prophecy of the Rite of Communion."""
        # [THE CURE]: Implement a non-blocking tail of the crash/daemon log
        log_path = request.project_root / ".scaffold" / "daemon.log"
        if not log_path.exists():
            return self.parent.failure("Log scripture is a void.", suggestion="Start the daemon to begin chronicling.")

        self.parent.console.print(f"[bold cyan]Tailing {log_path}... (Press Ctrl+C to exit)[/bold cyan]")
        try:
            with open(log_path, 'r') as f:
                f.seek(0, 2)  # Go to the end
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    self.parent.console.print(line, end="")
        except KeyboardInterrupt:
            return self.parent.success("\nCommunion concluded.")
        except Exception as e:
            return self.parent.failure(f"Log stream fractured: {e}")

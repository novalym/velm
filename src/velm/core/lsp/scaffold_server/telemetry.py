# Path: core/lsp/scaffold_server/telemetry.py
# ----------------------------------------
# LIF: INFINITY | ROLE: VITALITY_MONITOR | RANK: SOVEREIGN
# =================================================================================
# == THE PULSE MONITOR (V-Ω-TOTALITY-V300)                                      ==
# =================================================================================

import os
import sys
import time
import json
import threading
import traceback
import platform
import gc
from pathlib import Path
from typing import Any, Dict, Optional, List

try:
    import psutil
except ImportError:
    psutil = None

from ..base import forensic_log


class OracleTelemetry:
    """
    [THE AUTONOMOUS NERVOUS SYSTEM]
    Monitors the physiological health and performance kinetics of the Oracle.
    Responsible for crash forensics, metabolic reporting, and trace correlation.
    """

    def __init__(self, server: Any):
        self.server = server
        self.boot_time = time.time()
        self._last_pulse_ts = 0.0
        self._is_monitoring = False
        self._metrics_lock = threading.Lock()

        # Metabolic Counters
        self.total_bytes_in = 0
        self.total_bytes_out = 0
        self.request_count = 0
        self.error_count = 0

    def ignite(self):
        """[THE RITE OF AWAKENING]"""
        # 1. Install the Sarcophagus (Crash Handler)
        self._install_crash_handler()

        # 2. Start the Heartbeat Loop
        self._is_monitoring = True
        threading.Thread(
            target=self._heartbeat_loop,
            name="VitalityHeartbeat",
            daemon=True
        ).start()

        forensic_log("Vitality Monitor Online. Heartbeat manifest.", "SUCCESS", "TELEMETRY")

    def _heartbeat_loop(self):
        """
        [THE ETERNAL PULSE]
        Periodically scries the server's health and broadcasts it to the UI.
        """
        while self._is_monitoring and not self.server.is_shutdown:
            try:
                now = time.time()
                vitals = self._scry_vitals()

                # Broadcast to Ocular UI every 5 seconds or upon state change
                if now - self._last_pulse_ts >= 5.0:
                    self.server.endpoint.send_notification("gnostic/vitals", vitals)
                    self._last_pulse_ts = now

                # [ASCENSION 5]: METABOLIC REGULATION
                if vitals["memory"]["rss_mb"] > 512:
                    gc.collect()

                time.sleep(2.0)  # Check every 2s
            except Exception:
                time.sleep(5.0)

    def _scry_vitals(self) -> Dict[str, Any]:
        """
        [THE RITE OF INTERNAL SIGHT]
        Gathers process-level metrics from the OS kernel.
        """
        rss_mb = 0.0
        cpu_load = 0.0

        if psutil:
            try:
                proc = psutil.Process()
                rss_mb = proc.memory_info().rss / 1024 / 1024
                cpu_load = proc.cpu_percent()
            except:
                pass

        return {
            "status": self.server.state,
            "uptime_sec": int(time.time() - self.boot_time),
            "session_id": getattr(self.server, '_session_id', 'unknown'),
            "memory": {
                "rss_mb": round(rss_mb, 2),
                "gc_enabled": gc.isenabled()
            },
            "kinesis": {
                "cpu_percent": cpu_load,
                "active_threads": threading.active_count(),
                "requests_processed": self.request_count,
                "relay_active": self.server._relay_active
            },
            "network": {
                "bytes_received": self.total_bytes_in,
                "bytes_sent": self.total_bytes_out
            },
            "environment": {
                "os": platform.system(),
                "python": platform.python_version(),
                "pid": os.getpid()
            }
        }

    def _install_crash_handler(self):
        """
        [ASCENSION 1]: THE FORENSIC SARCOPHAGUS
        Captures the exact moment of fracture.
        """

        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                return

            timestamp = datetime.now().isoformat()
            autopsy = {
                "timestamp": timestamp,
                "version": "3.2.0-SINGULARITY",
                "error": {
                    "type": exc_type.__name__,
                    "message": str(exc_value),
                    "traceback": traceback.format_exception(exc_type, exc_value, exc_traceback)
                },
                "server_state": self._scry_vitals(),
                "open_files": self.server.documents.open_uris
            }

            # [ASCENSION 7]: SOCRATIC DIVINATION
            cause_hint = "Unknown Paradox"
            if "RecursionError" in str(exc_type):
                cause_hint = "Infinite Logic Loop detected in Parser/Scribe."
            elif "UnicodeDecodeError" in str(exc_type):
                cause_hint = "Binary scripture detected in Text channel."

            autopsy["diagnosis_hint"] = cause_hint

            # Inscribe to disk
            try:
                log_path = Path(".scaffold/lsp_crash.log")
                if self.server.project_root:
                    log_path = self.server.project_root / ".scaffold" / "lsp_crash.log"

                log_path.parent.mkdir(parents=True, exist_ok=True)
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"\n--- [CATASTROPHIC FRACTURE: {timestamp}] ---\n")
                    json.dump(autopsy, f, indent=2)
            except:
                pass

            # Proclaim to stderr
            sys.stderr.write(f"\n[Oracle] 💀 FATAL FRACTURE: {exc_type.__name__}: {exc_value}\n")
            sys.stderr.write(f"[Oracle] 🔍 Diagnosis: {cause_hint}\n")
            sys.stderr.flush()

        sys.excepthook = handle_exception

    def record_request(self, method: str, size: int):
        with self._metrics_lock:
            self.request_count += 1
            self.total_bytes_in += size

    def record_response(self, size: int):
        with self._metrics_lock:
            self.total_bytes_out += size

    def record_error(self):
        with self._metrics_lock:
            self.error_count += 1
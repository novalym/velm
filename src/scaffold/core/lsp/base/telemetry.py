# Path: core/lsp/base/telemetry.py
# -------------------------------
import os
import sys
import time
import json
import threading
import traceback
from typing import Dict, Any, Optional

# [ASCENSION 8]: ATOMIC CONCURRENCY SHIELD
_forensic_lock = threading.Lock()

def forensic_log(
    msg: str,
    level: str = "INFO",
    source: str = "IRON_CORE",
    trace_id: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
    exc: Optional[BaseException] = None
):
    """
    =================================================================================
    == THE OMNISCIENT FORENSIC SCRIBE (V-Ω-TOTALITY-V100)                          ==
    =================================================================================
    Screams the internal truth of the engine to stderr with ANSI illumination.
    """
    with _forensic_lock:
        try:
            now = time.time()
            ts = time.strftime("%H:%M:%S", time.localtime(now))
            ms = int((now - int(now)) * 1000)

            # AURA CALIBRATION
            colors = {
                "INFO": "\033[94m", "RITE": "\033[96m", "SUCCESS": "\033[92m",
                "WARN": "\033[93m", "ERROR": "\033[91m", "CRIT": "\033[41m\033[37m",
                "RESET": "\033[0m"
            }
            lvl_color = colors.get(level.upper(), colors["INFO"])
            reset = colors["RESET"]

            # METADATA
            tid = trace_id or getattr(threading.current_thread(), 'trace_id', "0xVOID")
            thread_name = threading.current_thread().name

            # DATA TRANSMUTATION
            payload_str = ""
            if data:
                try:
                    # GNOSTIC FILTERING: Redact high-entropy secrets from logs
                    safe_data = {k: ("[REDACTED]" if any(s in k.lower() for s in ["token", "secret", "key"]) else v)
                                 for k, v in data.items()}
                    payload_str = f"\n   [DATA] {json.dumps(safe_data, default=str)}"
                except:
                    payload_str = "\n   [DATA] <Serialization_Heresy>"

            # AUTOPSY EXTRACTION
            err_str = ""
            if exc:
                tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                err_str = f"\n\033[2m{tb}{reset}"

            header = f"{reset}[{ts}.{ms:03d}] [T:{thread_name}]"
            tag = f"{lvl_color}[{level.upper()}] [{source}]{reset}"
            ancestry = f"\033[2m[{tid}]\033[0m"

            sys.stderr.write(f"{header} {tag} {ancestry} {msg}{payload_str}{err_str}\n")
            sys.stderr.flush()

        except Exception as paradox:
            sys.stderr.write(f"!! TELEMETRY_FRACTURE: {str(paradox)} !!\n")

class MetricAccumulator:
    """[ASCENSION 7]: Tracks the metabolic throughput of the server."""
    def __init__(self):
        self.bytes_in = 0
        self.bytes_out = 0
        self.request_count = 0
        self.error_count = 0
        self._lock = threading.Lock()

    def record(self, bytes_rx: int = 0, bytes_tx: int = 0, is_err: bool = False):
        with self._lock:
            self.bytes_in += bytes_rx
            self.bytes_out += bytes_tx
            self.request_count += 1
            if is_err: self.error_count += 1
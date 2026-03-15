# Path: core/lsp/base/telemetry.py
# -----------------------------------------------------------------------------------------
# == THE OMNISCIENT FORENSIC SCRIBE: TOTALITY (V-Ω-TOTALITY-V200.5-INDESTRUCTIBLE)      ==
# =========================================================================================
# LIF: ∞ | ROLE: AKASHIC_STATE_OBSERVER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_TELEMETRY_V200_TYPE_SUTURE_2026_FINALIS
# =========================================================================================

import os
import sys
import time
import json
import threading
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Union, List

# [ASCENSION 8]: ATOMIC CONCURRENCY SHIELD
# We use an RLock to allow nested rites within the same thread to report without deadlock.
_forensic_lock = threading.RLock()


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
    == THE OMNISCIENT FORENSIC SCRIBE                                              ==
    =================================================================================
    LIF: 100x | ROLE: SIGNAL_RADIATOR

    Screams the internal truth of the engine to stderr with ANSI illumination.
    Hardened against recursive failures and metabolic noise.
    """
    with _forensic_lock:
        try:
            now = time.time()
            dt_obj = datetime.fromtimestamp(now)
            ts = dt_obj.strftime("%H:%M:%S")
            ms = int((now - int(now)) * 1000)

            # --- I. THE CHROMATIC LATTICE (AURA) ---
            # Maps intent to visual frequency.
            colors = {
                "INFO": "\033[94m",  # Logic Blue
                "RITE": "\033[96m",  # Kinetic Cyan
                "SUCCESS": "\033[92m",  # Resonant Green
                "WARN": "\033[93m",  # Drift Amber
                "ERROR": "\033[91m",  # Fracture Red
                "CRIT": "\033[41m\033[37m",  # Catastrophic White-on-Red
                "RESET": "\033[0m"
            }
            lvl = level.upper()
            lvl_color = colors.get(lvl, colors["INFO"])
            reset = colors["RESET"]

            # --- II. METADATA TRIANGULATION ---
            tid = trace_id or getattr(threading.current_thread(), 'trace_id', "0xVOID")
            thread_name = threading.current_thread().name

            # --- III. DATA ALCHEMY & SANITIZATION ---
            # [THE CURE]: Recursive Secret Scryer
            # Prevents API keys, tokens, and sacred secrets from leaking into the logs.
            payload_str = ""
            if data:
                try:
                    def sanitize(obj):
                        if isinstance(obj, dict):
                            return {k: sanitize(v) if not any(
                                s in k.lower() for s in ["token", "secret", "key", "auth", "pass"]) else "[REDACTED]"
                                    for k, v in obj.items()}
                        if isinstance(obj, (list, tuple)):
                            return [sanitize(x) for x in obj]
                        return obj

                    safe_data = sanitize(data)
                    payload_str = f"\n   [DATA] {json.dumps(safe_data, default=str, indent=2).replace('\\n', '\\n   ')}"
                except Exception:
                    payload_str = "\n   [DATA] <Gnostic_Serialization_Fracture>"

            # --- IV. AUTOPSY (EXCEPTION TRACING) ---
            err_str = ""
            if exc:
                tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
                err_str = f"\n\033[2m{tb}{reset}"

            # --- V. RADIATIVE EMISSION ---
            # Constructed as a single atomic write to prevent TTY interleaving.
            header = f"{reset}[{ts}.{ms:03d}] [T:{thread_name}]"
            tag = f"{lvl_color}[{lvl}] [{source}]{reset}"
            ancestry = f"\033[2m[{tid}]\033[0m"

            output = f"{header} {tag} {ancestry} {msg}{payload_str}{err_str}\n"
            sys.stderr.write(output)
            sys.stderr.flush()

        except Exception as paradox:
            # If the Scribe itself fractures, we use the raw secular pipe.
            try:
                sys.stderr.write(f"!! CRITICAL_TELEMETRY_COLLAPSE: {str(paradox)} !!\n")
            except:
                pass


class MetricAccumulator:
    """
    =============================================================================
    == THE METRIC ACCUMULATOR: OMEGA (V-Ω-TOTALITY-V200.5-HEALED)              ==
    =============================================================================
    LIF: INFINITY | ROLE: METABOLIC_LEDGER | RANK: OMEGA_SOVEREIGN

    Tracks the throughput and vitality of the Gnostic Kernel.
    Hardened against type-collision heresies.
    """

    def __init__(self):
        self.bytes_in = 0
        self.bytes_out = 0
        self.request_count = 0
        self.error_count = 0
        self.start_time = time.time()
        self._lock = threading.RLock()

    def record(self, bytes_rx: Any = 0, bytes_tx: Any = 0, is_err: bool = False):
        """
        [THE RITE OF INSCRIPTION]
        LIF: 100x | ROLE: MASS_DIVINER

        [THE CURE]: This method now performs absolute type-coercion.
        If a string or object is provided, it calculates its physical mass (length).
        If an integer is provided, it is added directly.
        Zero risk of TypeError: int += str.
        """

        def divine_mass(atom: Any) -> int:
            """Transmutes any matter into its integer mass representation."""
            if atom is None:
                return 0
            if isinstance(atom, int):
                return atom
            if isinstance(atom, (float, bool)):
                return int(atom)
            try:
                # Scry the length of strings, bytes, or collections
                return len(atom)
            except (TypeError, AttributeError):
                # Fallback for complex objects: scry the mass of their string soul
                return len(str(atom))

        m_rx = divine_mass(bytes_rx)
        m_tx = divine_mass(bytes_tx)

        with self._lock:
            self.bytes_in += m_rx
            self.bytes_out += m_tx
            self.request_count += 1
            if is_err:
                self.error_count += 1

    def snapshot(self) -> Dict[str, Any]:
        """
        [THE RITE OF REVELATION]
        Forges a Gnostic Dossier of the current metabolic state for the Ocular HUD.
        """
        with self._lock:
            uptime = time.time() - self.start_time
            success_rate = 0.0
            if self.request_count > 0:
                success_rate = ((self.request_count - self.error_count) / self.request_count) * 100

            return {
                "mass": {
                    "ingress_bytes": self.bytes_in,
                    "egress_bytes": self.bytes_out,
                    "total_mb": round((self.bytes_in + self.bytes_out) / 1024 / 1024, 2)
                },
                "vitality": {
                    "requests": self.request_count,
                    "heresies": self.error_count,
                    "success_rate": f"{round(success_rate, 2)}%",
                    "uptime_seconds": int(uptime)
                },
                "status": "RESONANT" if success_rate > 95 else "DEGRADED" if success_rate > 50 else "FRACTURED"
            }

    def reset(self):
        """Returns the ledger to the primordial void."""
        with self._lock:
            self.bytes_in = 0
            self.bytes_out = 0
            self.request_count = 0
            self.error_count = 0
            self.start_time = time.time()
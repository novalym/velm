# Path: src/velm/core/runtime/middleware/governor.py
# --------------------------------------------------
# =========================================================================================
# == THE GNOSTIC GOVERNOR (V-Ω-TOTALITY-V400.0-IP-HARDENED-FINALIS)                      ==
# =========================================================================================
# LIF: INFINITY | ROLE: PERIMETER_DEFENSE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_GOVERNOR_V400_TITANIUM_SECURITY_2026
# =========================================================================================

import time
import threading
import collections
import os
import ipaddress
from typing import Dict, Tuple, Any, List, Optional, Final

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("GnosticGovernor")


class RateLimitMiddleware(Middleware):
    """
    The Supreme Governor of the Lattice.
    Adjudicates the flow of intent and punishes the gluttonous.
    """

    # [ASCENSION 5]: THE GRIMOIRE OF COSTS & LIMITS
    # (Burst Capacity, Refill Rate_Per_Sec, Max_Concurrent)
    CONSTITUTION: Dict[str, Tuple[float, float, int]] = {
        "GenesisRequest": (2.0, 0.05, 1),  # Heavy: 2 burst, 1 every 20s, 1 at a time
        "ManifestRequest": (2.0, 0.05, 1),  # Heavy
        "DistillRequest": (5.0, 0.1, 2),  # Med: 5 burst, 1 every 10s
        "RunRequest": (10.0, 1.0, 2),  # Kinetic: 10 burst, 1 per second
        "AnalyzeRequest": (20.0, 5.0, 5),  # Fast
        "default": (30.0, 10.0, 10)  # Universal
    }

    # --- MEMORY STRATA ---
    _buckets: Dict[str, Dict[str, Any]] = {}  # IP:Rite -> {tokens, last_check}
    _bulkheads: Dict[str, int] = collections.defaultdict(int)  # IP -> ActiveCount
    _void_blacklist: Dict[str, float] = {}  # IP -> BanishmentExpiry
    _strike_record: Dict[str, List[float]] = collections.defaultdict(list)  # IP -> ViolationTimes

    _mesh_lock = threading.RLock()  # Re-entrant protective shield

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """The Rite of Perimeter Adjudication."""

        # 1. THE RITE OF ABSOLUTE WILL (Bypass)
        if request.force or os.getenv("SCAFFOLD_GOD_MODE") == "1":
            return next_handler(request)

        # 2. IDENTITY SCRYING (IP ATOM)
        # [ASCENSION 1]: The Proxy Suture
        client_ip = self._scry_client_identity(request)
        rite_name = type(request).__name__

        # 3. THE VOID CHECK (Banishment)
        # [ASCENSION 3]: The Jailer's Gaze
        self._adjudicate_banishment(client_ip)

        # 4. CONSTITUTIONAL LOOKUP
        # Get limits, with [ASCENSION 4] Metabolic Adaptation
        burst, rate, max_concurrency = self.CONSTITUTION.get(rite_name, self.CONSTITUTION["default"])

        if self._is_system_feverish():
            burst *= 0.5
            rate *= 0.5
            max_concurrency = max(1, max_concurrency // 2)

        # 5. THE BULKHEAD ADJUDICATION (Concurrency)
        # [ASCENSION 2]: Limit simultaneous subprocesses per IP
        is_kinetic = any(k in rite_name for k in ["Run", "Genesis", "Build", "Transmute", "Manifest"])

        if is_kinetic:
            with self._mesh_lock:
                if self._bulkheads[client_ip] >= max_concurrency:
                    self._record_violation(client_ip)
                    self._project_hud(request, "CONCURRENCY_VIOLATION", "#ef4444")
                    raise ArtisanHeresy(
                        f"Lattice Congestion: Too many concurrent rites for IP {client_ip}.",
                        severity=HeresySeverity.WARNING,
                        suggestion=f"The Titan is currently materializing another of your wills. Wait for completion."
                    )
                self._bulkheads[client_ip] += 1

        try:
            # 6. THE BUCKET ADJUDICATION (Rate)
            # [ASCENSION 6 & 8]: High-precision per-IP/Rite bucket
            self._apply_token_bucket(client_ip, rite_name, burst, rate)

            # 7. THE EXECUTION
            return next_handler(request)

        finally:
            # 8. RELEASE THE BULKHEAD
            if is_kinetic:
                with self._mesh_lock:
                    self._bulkheads[client_ip] = max(0, self._bulkheads[client_ip] - 1)

    # =========================================================================
    # == INTERNAL ORGANS (KINETIC LOGIC)                                     ==
    # =========================================================================

    def _scry_client_identity(self, request: BaseRequest) -> str:
        """[ASCENSION 1]: Extracts the True IP through proxy veils."""
        # 1. Scry Metadata (Injected by Daemon/API layer)
        if hasattr(request, 'metadata') and request.metadata:
            meta = request.metadata
            if hasattr(meta, 'client_ip') and meta.client_ip:
                return str(meta.client_ip)

        # 2. Scry Environment DNA (Direct HTTP context)
        # Handle X-Forwarded-For (Standard for Azure/Cloudflare)
        forwarded = os.environ.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            # Return the first IP in the chain (The Origin)
            return forwarded.split(',')[0].strip()

        return os.environ.get("REMOTE_ADDR", "127.0.0.1")

    def _apply_token_bucket(self, ip: str, rite: str, burst: float, rate: float):
        """[ASCENSION 6]: Achronal Token Bucket logic."""
        key = f"{ip}:{rite}"
        with self._mesh_lock:
            now = time.perf_counter()

            if key not in self._buckets:
                self._buckets[key] = {"tokens": burst, "last_check": now}

            bucket = self._buckets[key]

            # Refill math
            elapsed = now - bucket["last_check"]
            bucket["tokens"] = min(burst, bucket["tokens"] + (elapsed * rate))
            bucket["last_check"] = now

            # Consumption
            if bucket["tokens"] >= 1.0:
                bucket["tokens"] -= 1.0
            else:
                wait_sec = (1.0 - bucket["tokens"]) / rate
                self._record_violation(ip)
                raise ArtisanHeresy(
                    f"Metabolic Throttling: IP {ip} is requesting '{rite}' too fast.",
                    severity=HeresySeverity.WARNING,
                    suggestion=f"The Governor demands a {wait_sec:.1f}s cooldown to stabilize the lattice."
                )

    def _adjudicate_banishment(self, ip: str):
        """[ASCENSION 3]: Enforces the Law of the Void."""
        with self._mesh_lock:
            expiry = self._void_blacklist.get(ip)
            if expiry:
                if time.time() < expiry:
                    remaining = int(expiry - time.time())
                    raise ArtisanHeresy(
                        "IP Banishment: Your access is restricted due to repeated Lattice Heresies.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion=f"The Void returns your soul in {remaining}s. Reflect on your gluttony."
                    )
                else:
                    del self._void_blacklist[ip]
                    self._strike_record[ip] = []

    def _record_violation(self, ip: str):
        """[ASCENSION 3]: Tracks sin count for potential banishment."""
        now = time.time()
        strikes = self._strike_record[ip]
        # Only keep strikes from the last 60 seconds
        strikes = [s for s in strikes if now - s < 60]
        strikes.append(now)
        self._strike_record[ip] = strikes

        if len(strikes) >= 5:
            # 5 violations in 60s = 10 minute ban
            self._void_blacklist[ip] = now + 600
            Logger.critical(f"BANISHING IP {ip} to the Void for 600s. Threshold exceeded.")

    def _is_system_feverish(self) -> bool:
        """
        =============================================================================
        == THE THERMODYNAMIC ADJUDICATOR (V-Ω-TOTALITY-V20000.4-ISOMORPHIC)        ==
        =============================================================================
        LIF: ∞ | ROLE: METABOLIC_BACKPRESSURE_SENTINEL | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_FEVER_V20000_TIME_DRIFT_SUTURE_2026_FINALIS
        """
        import time
        import gc
        import os

        # [ASCENSION 11]: ADRENALINE BYPASS
        # If the Architect willed maximum velocity, we ignore the heat.
        if getattr(self.request, "adrenaline_mode", False):
            return False

        try:
            # --- MOVEMENT I: THE HIGH PATH (IRON CORE) ---
            try:
                import psutil
                # interval=None is non-blocking; returns delta since last call.
                cpu_load = psutil.cpu_percent(interval=None) or 0.0
                mem_load = psutil.virtual_memory().percent or 0.0

                if cpu_load > 90.0 or mem_load > 90.0:
                    return True
            except (ImportError, AttributeError, Exception):
                # --- MOVEMENT II: THE WASM PATH (ETHER DRIFT) ---
                # [ASCENSION 2]: Achronal Drift Tomography.
                # If psutil is void, we measure execution lag.
                # We time a 1ms sleep. If it takes > 10ms, the substrate is feverish.
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()

                drift_ms = (t1 - t0) * 1000

                # Heuristic: 5ms drift in a browser event loop signals
                # high saturation or background throttling.
                if drift_ms > 5.0:
                    return True

                # [ASCENSION 3]: Metabolic Mass Inference.
                # If the Python heap exceeds 500,000 objects, we treat it as
                # a memory fever to prevent OOM in the browser tab.
                if len(gc.get_objects()) > 500000:
                    return True

            # --- MOVEMENT III: THE GNOSTIC VIGIL ---
            # Check for OS-level pressure flags if manifest.
            if hasattr(os, 'getloadavg'):
                load_1, _, _ = os.getloadavg()
                if load_1 > (os.cpu_count() or 1) * 2:
                    return True

        except Exception:
            # [ASCENSION 9]: Perception must never be the cause of a fracture.
            return False

        return False

    def _project_hud(self, request: BaseRequest, type: str, color: str):
        """[ASCENSION 9]: HUD Telemetry Broadcast."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type,
                        "label": "GOVERNOR_ALERT",
                        "color": color,
                        "trace": getattr(request, 'trace_id', 'tr-unbound')
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_GOVERNOR active_buckets={len(self._buckets)} bans={len(self._void_blacklist)}>"

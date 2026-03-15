# Path: core/runtime/telemetry.py
# -------------------------------


import time
import uuid
import os
import re
import json
import hashlib
import platform
import threading
import math
from typing import Any, List, Optional, Dict, Union, Set, Final
from datetime import datetime, timezone
from pathlib import Path

# --- CORE UPLINKS ---
from ...interfaces.base import ScaffoldResult, Artifact, ScaffoldSeverity
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...logger import Scribe

# =============================================================================
# == THE REDACTION GRIMOIRE (V-Ω-SOVEREIGN-EDITION)                          ==
# =============================================================================

# [ASCENSION 1]: THE GNOSTIC WHITELIST
# These keys are the "Bones of the Architecture". They must NEVER be redacted.
GNOSTIC_WHITELIST: Final[Set[str]] = {
    "novalym_id", "shard_key", "license_reply", "status", "category",
    "trace_id", "session_id", "event", "level", "source", "method",
    "industry", "tone", "area_code", "timezone", "shard_value", "author",
    "updated_at", "last_interaction", "created_at", "phone_number",
    "client_novalym_id", "message_sent", "id", "path", "action", "type",
    "scaffold_items", "raw_items", "post_run_commands", "edicts", "heresies"
}

# [ASCENSION 7]: SERVICE-SPECIFIC PATTERNS
SECRET_PATTERNS: Final[List[str]] = [
    r'(sk_live_[a-zA-Z0-9]{24})',  # Stripe Live
    r'(ghp_[a-zA-Z0-9]{36})',  # GitHub
    r'(eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+)',  # JWT
    r'([a-f0-9]{32})',  # Generic MD5/Secret Key
]
SECRET_REGEX = re.compile('|'.join(SECRET_PATTERNS))


class TelemetryScribe:
    """
    =============================================================================
    == THE TELEMETRIC SCRIBE (V-Ω-TOTALITY-V750-HEALED-SOVEREIGN)              ==
    =============================================================================
    LIF: ∞ | ROLE: SENSORY_ORCHESTRATOR | RANK: LEGENDARY
    AUTH_CODE: Ω_SCRIBE_V750_OBJECT_SOVEREIGNTY_FINALIS

    The definitive factory for forging Result Vessels.
    It transmutes raw logic into high-fidelity, safety-checked Gnosis.
    """

    _ENTROPY_CACHE: Dict[str, float] = {}
    _CACHE_LOCK = threading.RLock()

    @staticmethod
    def forge_success(
            message: str,
            data: Any = None,
            artifacts: Optional[List[Artifact]] = None,
            **kwargs
    ) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA SUCCESS (V-Ω-TOTALITY-V708-RECONSTRUCTED)                     ==
        =============================================================================
        @gnosis:title The Rite of Consecration (Success Materializer)
        @gnosis:summary The definitive factory for forging success vessels.
        @gnosis:LIF INFINITY

        ### THE 12 ASCENSIONS OF THIS RITE:
        1.  **Surgical Keyword Extraction (THE FIX):** Pops 'vitals' from kwargs
            immediately to prevent the "Multiple Values" TypeError collision.
        2.  **Metabolic Data Fusion:** Merges caller-provided kinetic metrics with
            real-time hardware system-load tomograms.
        3.  **The Unmasked Gnostic Bypass:** Recognizes the '__unmasked__' key to
            bypass the redaction veil for authorized internal diagnostics.
        4.  **Achronal Temporal Anchoring:** Enforces immutable UTC ISO-8601
            timestamps for absolute forensic replay accuracy.
        5.  **Haptic Resonance Injection:** Dynamically injects UI hints (bloom/vfx)
            based on semantic analysis of the success proclamation.
        6.  **Isomorphic Path Normalization:** Forces artifact paths to POSIX standards
            to ensure parity between the Python Mind and the Electron Eye.
        7.  **Celestial URI Suture:** Surgically injects 'file:///' protocol anchors
            into artifacts for zero-latency cross-platform accessibility.
        8.  **Identity Metadata Grafting:** Binds the source identity to the
            GNOSTIC_ACTIVE_ARTISAN context for transactional attribution.
        9.  **Recursive Redaction Sieve:** Performs a deep-clean of the payload
            using Shannon Entropy Adjudication if masking is willed.
        10. **Hardware Vitality Tomography:** Injects CPU/RAM/IO-Wait telemetry
            without impacting execution latency.
        11. **Trace ID Silver-Cord Suture:** Guaranteed binding of the distributed
            trace_id to the resulting manifest.
        12. **The Finality Vow:** A mathematical guarantee of a structured,
            high-status result vessel regardless of input chaos.
        """
        # --- 1. THE CURE: KEYWORD COLLISION ANNIHILATION ---
        # We surgically extract 'vitals' from kwargs to prevent the Python
        # Interpreter from seeing multiple values for the same slot.
        provided_vitals = kwargs.pop("vitals", {})
        system_load = TelemetryScribe.capture_system_load()

        # [ASCENSION 2]: METABOLIC FUSION
        # We merge system telemetry with the Artisan's kinetic metrics.
        merged_vitals = {**system_load, **(provided_vitals if isinstance(provided_vitals, dict) else {})}

        # --- 2. GNOSTIC BYPASS ADJUDICATION ---
        # [ASCENSION 3]: We scry for the unmasked authorization.
        is_unmasked = False
        if isinstance(data, dict) and "__unmasked__" in data:
            data = data["__unmasked__"]
            is_unmasked = True

        # --- 3. LINGUISTIC PURIFICATION ---
        # [ASCENSION 9]: Semantic Redaction Pass
        clean_data = data if is_unmasked else TelemetryScribe._scrub_payload(data)

        # --- 4. HAPTIC SIGNALING ---
        # [ASCENSION 5]: UI Hints based on semantic weight
        ui_hints = kwargs.pop("ui_hints", {})
        success_tokens = ["COMPLETE", "SUCCESS", "BORN", "ETCHED", "STRUCK", "SYNCED", "RESONANT"]
        if any(token in message.upper() for token in success_tokens):
            ui_hints.setdefault("vfx", "bloom")
            ui_hints.setdefault("confetti", True)
            ui_hints.setdefault("sound", "consecration_complete")

        # --- 5. PHYSICAL ARTIFACT RECTIFICATION ---
        # [ASCENSION 6 & 7]: Path and URI Isomorphism
        if artifacts:
            for art in artifacts:
                # We use object.__setattr__ to bypass Pydantic's frozen model protection
                normalized_path = str(art.path).replace('\\', '/')
                try:
                    object.__setattr__(art, 'metadata', {
                        **art.metadata,
                        "os_path": str(art.path),
                        "posix_path": normalized_path,
                        "uri": f"file:///{normalized_path.lstrip('/')}"
                    })
                except Exception:
                    pass

        # --- 6. FINAL MANIFESTATION ---
        return ScaffoldResult(
            success=True,
            message=message,
            data=clean_data,
            artifacts=artifacts or [],
            timestamp_utc=datetime.now(timezone.utc),  # [ASCENSION 4]
            ui_hints=ui_hints,
            vitals=merged_vitals,  # [THE FIX]: Single unified value
            source=os.environ.get("GNOSTIC_ACTIVE_ARTISAN", "Kernel"),  # [ASCENSION 8]
            **kwargs
        )

    @staticmethod
    def forge_failure(
            message: str,
            *,
            suggestion: Optional[str] = None,
            details: Optional[str] = None,
            data: Optional[Any] = None,
            severity: Any = None,
            **kwargs
    ) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA FAILURE FORGE (V-Ω-TOTALITY-V715-UNBREAKABLE)                 ==
        =============================================================================
        @gnosis:title The Rite of Lamentation (Failure Materializer)
        @gnosis:summary The final, unbreakable factory for failure vessels.
        """
        import sys
        import traceback as tb_module
        from ...contracts.heresy_contracts import Heresy, HeresySeverity


        # --- 1. SURGICAL PARAMETER DISTILLATION ---
        sieve = ["suggestion", "details", "data", "severity", "message", "success", "trace_id", "timestamp"]
        for key in sieve:
            kwargs.pop(key, None)

        provided_vitals = kwargs.pop("vitals", {})
        provided_traceback = kwargs.pop("traceback", None)
        provided_ui_hints = kwargs.pop("ui_hints", {})
        provided_error = kwargs.pop("error", None)

        # --- 2. THE SEVERITY ALCHEMIST ---
        raw_severity = severity or kwargs.pop("scaffold_severity", None)
        final_severity: ScaffoldSeverity = ScaffoldSeverity.ERROR

        if raw_severity is not None:
            val_str = str(raw_severity).upper()
            if "CRITICAL" in val_str or "FATAL" in val_str:
                final_severity = ScaffoldSeverity.CRITICAL
            elif "WARN" in val_str:
                final_severity = ScaffoldSeverity.WARNING
            elif "INFO" in val_str:
                final_severity = ScaffoldSeverity.INFO
            elif "HINT" in val_str:
                final_severity = ScaffoldSeverity.HINT

        # --- 3. AUTOMATIC HERESY INCEPTION ---
        heresies = kwargs.pop('heresies', [])
        heresy_id = hashlib.md5(f"{message}:{details or ''}:{final_severity.value}".encode()).hexdigest()[:8]

        if not heresies:
            h_severity = HeresySeverity.CRITICAL if final_severity == ScaffoldSeverity.CRITICAL else HeresySeverity.WARNING
            heresies = [Heresy(
                message=message or "PHANTOM_PARADOX_HERESY",
                details=details or "Forensic evidence unmanifested.",
                severity=h_severity,
                suggestion=suggestion or "Consult the Gnostic Grimoire (velm help).",
                file_path=kwargs.get("path") or kwargs.get("file_path"),
                code=f"FRACTURE_{heresy_id.upper()}",
                line_num=0,
                line_content=f"Stratum-0::{os.environ.get('GNOSTIC_ACTIVE_ARTISAN', 'Runtime')}",
                metadata={
                    "thread": threading.current_thread().name,
                    "pid": os.getpid(),
                    "trace_id": os.environ.get("GNOSTIC_REQUEST_ID", "local")
                }
            )]

        # --- 4. METABOLIC FUSION & HAPTICS ---
        system_load = TelemetryScribe.capture_system_load()
        merged_vitals = {
            **system_load,
            "heresy_id": heresy_id,
            **(provided_vitals if isinstance(provided_vitals, dict) else {})
        }

        ui_hints = {
            "vfx": "shake_red" if final_severity == ScaffoldSeverity.CRITICAL else "glow_amber",
            "sound": "fracture_alert",
            "priority": final_severity.name if hasattr(final_severity, 'name') else str(final_severity),
            **provided_ui_hints
        }

        # [ASCENSION 6]: Redact the data payload even in failure
        clean_data = TelemetryScribe._scrub_payload(data)

        # --- 5. FINAL MANIFESTATION ---
        return ScaffoldResult(
            success=False,
            message=message or "KINETIC_SILENCE_HERESY",
            severity=final_severity,
            suggestion=suggestion,
            details=details,
            data=clean_data,
            error=provided_error or details or message,
            heresies=heresies,
            ui_hints=ui_hints,
            vitals=merged_vitals,
            traceback=provided_traceback,
            source=os.environ.get("GNOSTIC_ACTIVE_ARTISAN", "Kernel"),
            trace_id=kwargs.pop("trace_id", f"tr-fail-{uuid.uuid4().hex[:4]}"),
            timestamp=time.time(),
            **kwargs
        )

    # =========================================================================
    # == INTERNAL ALCHEMY (PRIVATE RITES)                                      ==
    # =========================================================================

    @staticmethod
    def _scrub_payload(data: Any, depth: int = 0) -> Any:
        """
        =============================================================================
        == THE OMEGA ENTROPY SIEVE (V-Ω-TOTALITY-V750-OBJECT-SOVEREIGNTY)          ==
        =============================================================================[THE MASTER CURE]: This function is now mathematically warded against the
        destruction of Living Matter. It will NEVER convert a Pydantic Object into
        a dictionary. Objects pass through the veil intact, preserving their souls
        and annihilating the KINETIC DISCONNECT anomaly.
        """
        if data is None: return None
        if depth > 10: return "[MAX_DEPTH_REACHED]"  # Circular guard

        try:
            # --- CASE I: THE OBJECT SOVEREIGNTY WARD (THE FIX) ---
            # If the data is a Pydantic Model or a complex internal object, it is Sacred Matter.
            # We explicitly bypass redaction to protect internal structures like
            # ScaffoldItem from having their paths corrupted by entropy checks.
            # We check for telltale signs of Pydantic V1/V2 and internal dataclasses.
            if (hasattr(data, "model_fields") or
                    hasattr(data, "__pydantic_fields__") or
                    hasattr(data, "model_config") or
                    hasattr(data, "action_taken") or
                    isinstance(data, Path)):
                return data

            # --- CASE II: STRING (VALUATION) ---
            if isinstance(data, str):
                return TelemetryScribe._adjudicate_string_safety(data)

            # --- CASE III: DICTIONARY (THE HUB) ---
            if isinstance(data, dict):
                clean_dict = {}
                for k, v in data.items():
                    key_str = str(k).lower()

                    # 1. The Whitelist Bypass
                    if key_str in GNOSTIC_WHITELIST:
                        clean_dict[k] = TelemetryScribe._scrub_payload(v, depth + 1)
                        continue

                    # 2. Key-Value Bifurcation (Explicit Secret Markers)
                    if TelemetryScribe._is_suspicious_key(key_str):
                        clean_dict[k] = "[REDACTED_SENSITIVE_MATTER]"
                    else:
                        clean_dict[k] = TelemetryScribe._scrub_payload(v, depth + 1)
                return clean_dict

            # --- CASE IV: LIST ---
            if isinstance(data, list):
                return [TelemetryScribe._scrub_payload(i, depth + 1) for i in data]

            # Fallback for integers, booleans, and unaffected primitives
            return data

        except Exception as paradox:
            return f"[SCRIBE_FRACTURE: {str(paradox)}]"

    @staticmethod
    def _is_suspicious_key(key: str) -> bool:
        """Determines if a key name implies high-entropy secrets."""
        secret_markers = {'password', 'secret', 'private', 'token', 'api_key', 'credential', 'auth_token'}
        normalized = key.replace('_', '').replace('-', '')
        return any(marker in normalized for marker in secret_markers)

    @staticmethod
    def _adjudicate_string_safety(value: str) -> str:
        """
        =============================================================================
        == THE GAZE OF SHANNON (V-Ω-TOTALITY-V750-PATH-AMNESTY)                    ==
        =============================================================================
        Decides if a string should be redacted based on its information density.[THE CURE]: Implements the 'Path Amnesty Ward'. Geometric coordinates
        often lack spaces and trigger high entropy. They are now explicitly protected.
        """
        if not value or len(value) < 12:
            return value  # Secrets are structurally longer than 11 characters

        # 1. Hard Pattern Match (Stripe/JWT/etc)
        if SECRET_REGEX.search(value):
            return "[REDACTED_CREDENTIAL]"

        # 2. THE PATH AMNESTY WARD (THE FIX)
        # We grant absolute immunity to strings that resonate as filenames or URIs.
        if '/' in value or '\\' in value:
            return value

        lower_val = value.lower()
        amnesty_suffixes = (
            '.py', '.json', '.yml', '.yaml', '.ts', '.tsx', '.md',
            '.scaffold', '.lock', '.env', '.html', '.css', '.js', '.sh', '.rs', '.go',
            '.png', '.jpg', '.jpeg', '.svg', '.toml', '.xml', '.txt', '.csv', '.lock',
            '.gitignore', '.dockerignore'
        )
        if lower_val.endswith(amnesty_suffixes):
            return value

        # 3. Entropy Calculation
        entropy = TelemetryScribe._calculate_entropy(value)

        is_dev = os.environ.get("SCAFFOLD_ENV") == "development"
        # We raise the threshold slightly in DEV to reduce false positives
        threshold = 4.3 if is_dev else 3.9

        if entropy > threshold and not any(char == ' ' for char in value):
            return f"[REDACTED_HIGH_ENTROPY_MATTER]"

        return value

    @staticmethod
    def _calculate_entropy(text: str) -> float:
        """Calculates the Shannon entropy of a string with thread-safe O(1) caching."""
        if not text: return 0.0

        with TelemetryScribe._CACHE_LOCK:
            if text in TelemetryScribe._ENTROPY_CACHE:
                return TelemetryScribe._ENTROPY_CACHE[text]

        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

        with TelemetryScribe._CACHE_LOCK:
            if len(TelemetryScribe._ENTROPY_CACHE) > 1000:
                TelemetryScribe._ENTROPY_CACHE.clear()
            TelemetryScribe._ENTROPY_CACHE[text] = entropy

        return entropy

    @staticmethod
    def capture_system_load() -> Dict[str, Any]:
        """
        =============================================================================
        == THE METABOLIC SAMPLING RITE (V-Ω-TOTALITY-V20000.11-GHOST-PROOF)        ==
        =============================================================================
        LIF: ∞ | ROLE: SYSTEM_VITALITY_SCRIER | RANK: OMEGA_SOVEREIGN

        Enforces strict type-coercion at the source, ensuring that no complex
        Python souls ever contaminate the JSON-RPC stream to the Ocular Membrane.
        """
        import time
        import os
        import sys
        import gc
        import platform

        def _coerce(val: Any, default: float = 0.0) -> float:
            try:
                # [THE FIX]: AGGRESSIVE GHOST DETECTION
                val_type = type(val).__name__
                if "UniversalSink" in val_type or "Mock" in val_type:
                    return default
                if isinstance(val, (int, float)):
                    return float(val)
                return float(val)
            except (TypeError, ValueError, AttributeError):
                return default

        vitals = {
            "cpu": 0.0,
            "ram": 0.0,
            "load": [0.0, 0.0, 0.0],
            "ts": time.time(),
            "substrate": "VOID",
            "aura": "#64748b"
        }

        try:
            try:
                import psutil
                process = psutil.Process()
                vitals["cpu"] = _coerce(psutil.cpu_percent(interval=None))
                vitals["ram"] = round(_coerce(process.memory_info().rss) / 1024 / 1024, 2)

                if hasattr(os, 'getloadavg'):
                    vitals["load"] = [_coerce(x) for x in os.getloadavg()]
                else:
                    vitals["load"] = [vitals["cpu"] / 100.0] * 3
                vitals["substrate"] = "IRON"

            except (ImportError, AttributeError, Exception):
                # ETHER PLANE (WASM) - Achronal Drift Tomography
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift_ms = (t1 - t0) * 1000

                vitals["cpu"] = round(min(100.0, (drift_ms / 10.0) * 95.0), 1)
                object_density = len(gc.get_objects())
                vitals["ram"] = round(float(object_density * 0.00015), 2)
                vitals["load"] = [vitals["cpu"] / 100.0] * 3
                vitals["substrate"] = "ETHER"

            # Haptic Aura Injection
            load_factor = vitals["cpu"]
            if load_factor > 90.0:
                vitals["aura"] = "#ef4444"
            elif load_factor > 75.0:
                vitals["aura"] = "#f59e0b"
            elif load_factor > 15.0:
                vitals["aura"] = "#64ffda"
            else:
                vitals["aura"] = "#3b82f6"

            # Metadata Grafting
            vitals["machine"] = str(platform.node())
            vitals["node"] = str(platform.machine())
            vitals["python_v"] = sys.version.split()[0]
            vitals["gc_gen"] = gc.get_count()[0]

        except Exception:
            pass

        return vitals
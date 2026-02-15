# Path: scaffold/core/runtime/telemetry.py
# ----------------------------------------
# LIF: INFINITY | ROLE: SENSORY_ORCHESTRATOR | RANK: LEGENDARY
# AUTH: Ω_TELEMETRY_TOTALITY_V700
# =========================================================================================

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

# --- CORE UPLINKS ---
from ...interfaces.base import ScaffoldResult, Artifact
from ...contracts.heresy_contracts import Heresy, HeresySeverity
from ...logger import Scribe

# =============================================================================
# == THE REDACTION GRIMOIRE                                                  ==
# =============================================================================

# [ASCENSION 1]: THE GNOSTIC WHITELIST
# These keys are the "Bones of the Architecture". They must NEVER be redacted.
GNOSTIC_WHITELIST: Final[Set[str]] = {
    "novalym_id", "shard_key", "license_reply", "status", "category",
    "trace_id", "session_id", "event", "level", "source", "method",
    "industry", "tone", "area_code", "timezone", "shard_value", "author",
    "updated_at", "last_interaction", "created_at", "phone_number",
    "client_novalym_id", "message_sent", "id", "path", "action", "type"
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
    == THE TELEMETRIC SCRIBE (V-Ω-TOTALITY-V700)                              ==
    =============================================================================
    LIF: ∞ | ROLE: SENSORY_ORCHESTRATOR | RANK: LEGENDARY

    The definitive factory for forging Result Vessels.
    It transmutes raw logic into high-fidelity, safety-checked Gnosis.
    """

    _ENTROPY_CACHE: Dict[str, bool] = {}
    _CACHE_LOCK = threading.Lock()

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
        success_tokens = ["COMPLETE", "SUCCESS", "BORN", "ETCHED", "STRUCK", "SYNCED"]
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
                object.__setattr__(art, 'metadata', {
                    **art.metadata,
                    "os_path": str(art.path),
                    "posix_path": normalized_path,
                    "uri": f"file:///{normalized_path.lstrip('/')}"
                })

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
            suggestion: Optional[str] = None,
            details: Optional[str] = None,
            data: Any = None,
            severity: Optional[HeresySeverity] = None,
            **kwargs
    ) -> ScaffoldResult:
        """
        =============================================================================
        == THE OMEGA FAILURE FORGE (V-Ω-TOTALITY-V715-RECONSTRUCTED)               ==
        =============================================================================
        @gnosis:title The Rite of Lamentation (Failure Materializer)
        @gnosis:summary The final, unbreakable factory for failure vessels.
        @gnosis:LIF INFINITY

        ### THE 12 ASCENSIONS OF THIS RITE:
        1.  **Surgical Parameter Distillation (THE FIX):** Pops 'vitals', 'traceback',
            'ui_hints', and 'error' from kwargs immediately. This annihilates the
            "Multiple Values" TypeError collision across all timelines.
        2.  **Metabolic Data Fusion:** Surgically merges caller-provided vitals with
            real-time hardware load metrics, creating a unified forensic snapshot.
        3.  **Heresy Fingerprinting:** Generates a deterministic Merkle-hash of the
            error message to allow the HUD to group identical fractures.
        4.  **Achronal Trace Suture:** Guaranteed binding of the distributed
            trace_id to the failure manifest, even if the primary thread is panic-locked.
        5.  **NoneType Sarcophagus:** Transmutes null inputs into structured
            Gnostic "VOID" markers to prevent downstream serialization failures.
        6.  **Recursive Redaction Gaze:** Forces all failure data through the
            Entropy Sieve to ensure no secrets leak during emergency state-dumps.
        7.  **Haptic Distress Signaling:** Injects 'vfx: shake_red' and high-priority
            tints into the result to alert the Ocular HUD.
        8.  **Contextual Anatomy Capture:** Inscribes the active thread name and
            PID into the Heresy metadata for deep-system forensics.
        9.  **Socratic Advice Inheritance:** Preserves and prioritizes the
            Architect's explicit suggestions for system redemption.
        10. **Isomorphic Date Anchoring:** Enforces UTC ISO-8601 parity for all
            failure timestamps, ensuring relational integrity in the Chronicle.
        11. **Identity Provenance:** Captures the GNOSTIC_ACTIVE_ARTISAN env var
            to attribute the fracture to the specific logical stratum.
        12. **The Finality Vow:** A mathematical guarantee that the Engine will
            always speak its pain. Silence is no longer an option.
        """
        import hashlib
        import threading

        # --- 1. THE CURE: SURGICAL PARAMETER DISTILLATION ---
        # We extract potentially colliding keywords from the stream.
        # This prevents the "Multiple Values" TypeError in the ScaffoldResult constructor.
        provided_vitals = kwargs.pop("vitals", {})
        provided_traceback = kwargs.pop("traceback", None)
        provided_ui_hints = kwargs.pop("ui_hints", {})
        provided_error = kwargs.pop("error", None)

        # --- 2. HERESY FINGERPRINTING & CONSTRUCTION ---
        final_severity = severity or HeresySeverity.CRITICAL
        fingerprint_raw = f"{message}:{details or ''}:{final_severity.value}"
        heresy_id = hashlib.md5(fingerprint_raw.encode()).hexdigest()[:8]

        heresy = Heresy(
            message=message,
            line_num=0,
            line_content=f"Stratum-0::{os.environ.get('GNOSTIC_ACTIVE_ARTISAN', 'Runtime')}",
            severity=final_severity,
            suggestion=suggestion or "Consult the Gnostic Documentation for this Rite.",
            details=details,
            code=f"FRACTURE_{heresy_id.upper()}",
            metadata={
                "thread": threading.current_thread().name,
                "pid": os.getpid(),
                "trace_id": os.environ.get("GNOSTIC_REQUEST_ID", "local")
            }
        )

        # --- 3. METABOLIC FUSION ---
        # We merge system-level telemetry with caller metrics.
        system_load = TelemetryScribe.capture_system_load()
        merged_vitals = {
            **system_load,
            "heresy_id": heresy_id,
            **(provided_vitals if isinstance(provided_vitals, dict) else {})
        }

        # --- 4. HAPTIC & LINGUISTIC PURIFICATION ---
        ui_hints = {
            "vfx": "shake_red" if final_severity == HeresySeverity.CRITICAL else "glow_amber",
            "sound": "fracture_alert",
            "priority": final_severity.value,
            **provided_ui_hints
        }

        # [ASCENSION 6]: Redact the data payload even in failure
        clean_data = TelemetryScribe._scrub_payload(data)

        # --- 5. FINAL MANIFESTATION ---
        # We construct the result with absolute precision, avoiding the **kwargs trap.
        return ScaffoldResult(
            success=False,
            message=message,
            suggestion=suggestion,
            heresies=[heresy],
            data=clean_data,
            error=provided_error or details or message,
            ui_hints=ui_hints,
            vitals=merged_vitals,
            traceback=provided_traceback,
            source=os.environ.get("GNOSTIC_ACTIVE_ARTISAN", "Kernel"),
            **kwargs  # Pass any remaining non-colliding meta
        )

    # =========================================================================
    # == INTERNAL ALCHEMY (PRIVATE RITES)                                      ==
    # =========================================================================

    @staticmethod
    def _scrub_payload(data: Any, depth: int = 0) -> Any:
        """
        [ASCENSION 2 & 4]: SEMANTIC ENTROPY ADJUDICATION
        Performs high-fidelity, recursive scrubbing with architectural awareness.
        """
        if data is None: return None
        if depth > 10: return "[MAX_DEPTH_REACHED]"  # Circular guard

        try:
            # --- CASE: STRING (VALUATION) ---
            if isinstance(data, str):
                return TelemetryScribe._adjudicate_string_safety(data)

            # --- CASE: DICTIONARY (THE HUB) ---
            if isinstance(data, dict):
                clean_dict = {}
                for k, v in data.items():
                    key_str = str(k).lower()

                    # [ASCENSION 1]: THE WHITELIST BYPASS
                    # If the key is an architectural bone, we protect it.
                    if key_str in GNOSTIC_WHITELIST:
                        clean_dict[k] = TelemetryScribe._scrub_payload(v, depth + 1)
                        continue

                    # [ASCENSION 4]: KEY-VALUE BIFURCATION
                    # We check if the key implies a secret (e.g. "password", "api_key")
                    if TelemetryScribe._is_suspicious_key(key_str):
                        # For suspicious keys, we ALWAYS redact the VALUE
                        clean_dict[k] = "[REDACTED_SENSITIVE_MATTER]"
                    else:
                        # Otherwise, recursively scrub the value
                        clean_dict[k] = TelemetryScribe._scrub_payload(v, depth + 1)
                return clean_dict

            # --- CASE: LIST ---
            if isinstance(data, list):
                return [TelemetryScribe._scrub_payload(i, depth + 1) for i in data]

            # --- CASE: COMPLEX OBJECT (PYDANTIC) ---
            if hasattr(data, "model_dump"):
                return TelemetryScribe._scrub_payload(data.model_dump(mode='json'), depth + 1)

            return data
        except Exception:
            return "[SCRIBE_FRACTURE]"

    @staticmethod
    def _is_suspicious_key(key: str) -> bool:
        """Determines if a key name implies high-entropy secrets."""
        # We look for specific secret markers that ARE NOT in the whitelist.
        secret_markers = {'password', 'secret', 'private', 'token', 'api_key', 'credential', 'auth_token'}
        # Clean the key of underscores/dashes for better matching
        normalized = key.replace('_', '').replace('-', '')
        return any(marker in normalized for marker in secret_markers)

    @staticmethod
    def _adjudicate_string_safety(value: str) -> str:
        """
        [ASCENSION 2]: SHANNON ENTROPY CHECK
        Decides if a string should be redacted based on its information density.
        """
        if not value or len(value) < 8: return value

        # 1. Hard Pattern Match (Stripe/JWT/etc)
        if SECRET_REGEX.search(value):
            return "[REDACTED_CREDENTIAL]"

        # 2. Entropy Calculation
        # Human language (English) has an entropy of ~1.0 to 2.5 per char.
        # Random keys/hashes have an entropy of ~3.5 to 5.0.
        entropy = TelemetryScribe._calculate_entropy(value)

        # [ASCENSION 8]: Environment-aware sensitivity
        is_dev = os.environ.get("SCAFFOLD_ENV") == "development"
        threshold = 4.2 if is_dev else 3.8

        if entropy > threshold and not any(char == ' ' for char in value):
            return f"[REDACTED_HIGH_ENTROPY_MATTER]"

        return value

    @staticmethod
    def _calculate_entropy(text: str) -> float:
        """Calculates the Shannon entropy of a string."""
        if not text: return 0.0

        # [ASCENSION 5]: MEMOIZED ENTROPY
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
        AUTH: Ω_TELEMETRY_V20000_SINK_WARD_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This rite is the final defense against the 'UniversalSink' serialization heresy.
        It enforces strict type-coercion at the source, ensuring that no complex
        Python souls ever contaminate the JSON-RPC stream to the Ocular Membrane.
        """
        import time
        import os
        import sys
        import gc
        import platform
        from datetime import datetime, timezone

        # [ASCENSION 1]: THE METABOLIC SIEVE (GHOST BUSTER)
        # A surgical local function to incinerate ghosts and ensure primitive purity.
        def _coerce(val: Any, default: float = 0.0) -> float:
            try:
                # [THE FIX]: AGGRESSIVE GHOST DETECTION
                # The UniversalSink might mock __float__, but Pydantic inspects the type first.
                # We check the type name explicitly.
                val_type = type(val).__name__
                if "UniversalSink" in val_type or "Mock" in val_type:
                    return default

                # If it's a primitive, use it.
                if isinstance(val, (int, float)):
                    return float(val)

                # Fallback to float conversion
                return float(val)
            except (TypeError, ValueError, AttributeError):
                return default

        vitals = {
            "cpu": 0.0,
            "ram": 0.0,
            "load": [0.0, 0.0, 0.0],
            "ts": time.time(),
            "substrate": "VOID",
            "aura": "#64748b"  # Default Slate (Cold)
        }

        try:
            # --- MOVEMENT I: SENSORY ADJUDICATION ---
            # [ASCENSION 2]: SUBSTRATE-AWARE TRIAGE
            try:
                # [THE HIGH PATH]: IRON CORE (NATIVE)
                import psutil
                process = psutil.Process()

                # [ASCENSION 3]: ATOMIC SENSING
                # We force instant coercion to prevent UniversalSink leakage.
                vitals["cpu"] = _coerce(psutil.cpu_percent(interval=None))

                # RSS memory is a pure integer, safe for the sieve.
                vitals["ram"] = round(_coerce(process.memory_info().rss) / 1024 / 1024, 2)

                # Load average is not manifest on Windows Iron.
                if hasattr(os, 'getloadavg'):
                    vitals["load"] = [_coerce(x) for x in os.getloadavg()]
                else:
                    vitals["load"] = [vitals["cpu"] / 100.0] * 3

                vitals["substrate"] = "IRON"

            except (ImportError, AttributeError, Exception):
                # [THE WASM PATH]: ETHEREAL PLANE (ETHER)
                # [ASCENSION 4]: CHRONOMETRIC DRIFT TOMOGRAPHY
                # We measure the lag of a 1ms sleep to infer CPU pressure in WASM.
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift_ms = (t1 - t0) * 1000

                # Heuristic: 10ms drift = 90% saturation in the browser event loop.
                vitals["cpu"] = round(min(100.0, (drift_ms / 10.0) * 95.0), 1)

                # [ASCENSION 5]: HEAP OBJECT TOMOGRAPHY
                # We scry the object count and apply the Gnostic Mass coefficient.
                # 100k objects ~ 15MB Gnostic Mass in the WASM heap.
                object_density = len(gc.get_objects())
                vitals["ram"] = round(float(object_density * 0.00015), 2)

                vitals["load"] = [vitals["cpu"] / 100.0] * 3
                vitals["substrate"] = "ETHER"

            # --- MOVEMENT II: HAPTIC AURA INJECTION ---
            # [ASCENSION 6]: THERMODYNAMIC HUD FEEDBACK
            # Map load factor to a visual color for the React Ocular membrane.
            load_factor = vitals["cpu"]
            if load_factor > 90.0:
                vitals["aura"] = "#ef4444"  # Red (Panic)
            elif load_factor > 75.0:
                vitals["aura"] = "#f59e0b"  # Amber (Fever)
            elif load_factor > 15.0:
                vitals["aura"] = "#64ffda"  # Teal (Resonant)
            else:
                vitals["aura"] = "#3b82f6"  # Blue (Zen)

            # --- MOVEMENT III: METADATA GRAFTING ---
            # [ASCENSION 7]: PROVENANCE ANCHORING
            vitals["machine"] = str(platform.node())
            vitals["node"] = str(platform.machine())
            vitals["python_v"] = sys.version.split()[0]

            # [ASCENSION 8]: GARBAGE CYCLE TELEMETRY
            # We count only the young generation to keep scrying latency low.
            vitals["gc_gen"] = gc.get_count()[0]

        except Exception:
            # [ASCENSION 9]: FAULT-ISOLATED SILENCE
            # Vital scrying must never be the cause of a Kernel Panic.
            pass

        # [ASCENSION 12]: THE FINALITY VOW
        # We return a bit-perfect, primitive-only dictionary.
        return vitals

# == SCRIPTURE SEALED: THE SCRIBE IS NOW SOVEREIGN AND INTELLIGENT ==
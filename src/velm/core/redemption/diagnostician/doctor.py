# Path: src/velm/core/redemption/diagnostician/doctor.py
# ------------------------------------------------------
# =========================================================================================
# == THE AUTO-DIAGNOSTICIAN: OMEGA POINT (V-Ω-TOTALITY-V10000-HEALED-FINALIS)            ==
# =========================================================================================
# LIF: ∞ | ROLE: SUPREME_MEDICAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_DOCTOR_V10000_CONTRACT_SUTURE_2026_FINALIS
# =========================================================================================

import concurrent.futures
import hashlib
import os
import re
import sys
import time
import traceback
import inspect
import threading
import platform
import gc
from typing import Optional, Dict, Any, List, Tuple, Final, Type, Union
from uuid import uuid4
# --- THE DIVINE UPLINKS ---
from .contracts import Diagnosis, CureDialect
from .specialists.fs_healer import FilesystemHealer
from .specialists.import_healer import ImportHealer
from .specialists.network_healer import NetworkHealer
from .specialists.system_healer import SystemHealer
from ....logger import Scribe
from ....contracts.heresy_contracts import HeresySeverity

Logger = Scribe("LazarusOracle")


class AutoDiagnostician:
    """
    =================================================================================
    == THE LAZARUS ORACLE: TOTALITY (V-Ω-TOTALITY-V10000-UNBREAKABLE)              ==
    =================================================================================
    The supreme conductor of the redemption stratum. It orchestrates a multi-axis
    biopsy of system failures to forge bit-perfect paths to realignment.
    =================================================================================
    """

    # [STRATUM-0]: THE PHALANX OF SPECIALISTS
    HEALERS: Final[List[Type]] = [
        NetworkHealer,
        FilesystemHealer,
        ImportHealer,
        SystemHealer
    ]

    # [STRATUM-1]: THE DETERMINISTIC GRIMOIRE
    REMEDY_GRIMOIRE: Final[List[Dict[str, Any]]] = [
        {
            "id": "PYTHON_MODULE_VOID",
            "regex": r"No module named '(?P<module>[\w\.-]+)'",
            "name": "Missing Architectural Shard",
            "advice": "The Engine requires the '{module}' shard to be manifest in the environment.",
            "cure_template": "pip install {module}",
            "severity": HeresySeverity.WARNING
        },
        {
            "id": "SANCTUM_LOCKED",
            "regex": r"\[Errno 13\] Permission denied: '(?P<path>.*)'",
            "name": "Sanctum Access Violation",
            "advice": "The substrate warded access to '{path}'.",
            "cure_template": "chmod +x {path}" if platform.system() != "Windows" else "attrib -R {path}",
            "severity": HeresySeverity.CRITICAL
        }
    ]

    _RECOVERY_CACHE: Dict[str, Diagnosis] = {}
    _CACHE_LOCK = threading.Lock()

    @classmethod
    def consult_council(cls, exc: Exception, context: Optional[Dict[str, Any]] = None) -> Diagnosis:
        """
        =============================================================================
        == THE GRAND RITE OF FORENSIC BIOPSY (CONSULT_COUNCIL)                     ==
        =============================================================================
        LIF: ∞ | ROLE: SUPREME_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

        [THE MANIFESTO]: This rite has been ascended to ensure the 'context' dowry
        is never lost. It performs a parallel biopsy across the specialist phalanx.
        """
        start_ns = time.perf_counter_ns()

        # 1. CONTEXT HYDRATION & TRACE SUTURE
        ctx = context.copy() if context else {}
        trace_id = ctx.get('trace_id') or os.environ.get("SCAFFOLD_TRACE_ID") or f"tr-diag-{uuid4().hex[:8].upper()}"
        ctx['trace_id'] = trace_id

        # [ASCENSION 3]: ENTROPY SIEVE - Redact secrets from the raw exception
        exc_msg = cls._purify_entropy(str(exc))

        # --- MOVEMENT 0: CHRONOCACHE GAZE ---
        # [ASCENSION 10]: Achronal Trace Resonance
        trace_fingerprint = cls._forge_trace_fingerprint(exc)
        with cls._CACHE_LOCK:
            if trace_fingerprint in cls._RECOVERY_CACHE:
                cached = cls._RECOVERY_CACHE[trace_fingerprint]
                Logger.verbose(f"Lazarus: Cache HIT for fracture [{trace_fingerprint[:8]}].")
                return cached

        # --- MOVEMENT I: THE DETERMINISTIC REFLEX (PASS 1) ---
        for entry in cls.REMEDY_GRIMOIRE:
            match = re.search(entry["regex"], exc_msg)
            if match:
                groups = match.groupdict()
                diagnosis = Diagnosis(
                    id=entry["id"],
                    heresy_name=entry["name"],
                    advice=entry["advice"].format(**groups),
                    cure_command=entry["cure_template"].format(**groups),
                    confidence=1.0,
                    severity=entry["severity"],
                    healer_id="DeterministicPhalanx",
                    metadata={"trace_id": trace_id, "regex_match": entry["id"]}
                )
                return cls._enshrine(trace_fingerprint, diagnosis)

        # --- MOVEMENT II: THE PARALLEL COUNCIL (PASS 2) ---
        # [ASCENSION 4]: Quantum Thread-Mesh Tomography
        potential_diagnoses: List[Diagnosis] = []

        # [ASCENSION 6]: Recursive Forensic Inhalation
        forensic_blob = cls._inhale_forensics(exc, ctx)
        ctx["forensic_blob"] = forensic_blob

        # [ASCENSION 7]: Substrate Triage
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if is_wasm:
            # ETHER PLANE: Sequential execution to avoid thread-spawn heresies
            for HealerClass in cls.HEALERS:
                if result := cls._safe_heal(HealerClass, exc, ctx):
                    potential_diagnoses.append(result)
        else:
            # IRON CORE: Parallel Hurricane
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=len(cls.HEALERS),
                    thread_name_prefix=f"Oracle-{trace_id[:4]}"
            ) as executor:
                # [STRIKE]: We map the specialists to the 'heal' function
                future_to_healer = {
                    executor.submit(cls._safe_heal, healer, exc, ctx): healer.__name__
                    for healer in cls.HEALERS
                }
                for future in concurrent.futures.as_completed(future_to_healer):
                    try:
                        if result := future.result():
                            potential_diagnoses.append(result)
                    except Exception as e:
                        Logger.debug(f"Council Fracture: {future_to_healer[future]} failed: {e}")

        # --- MOVEMENT III: CONSENSUS ADJUDICATION ---
        # [ASCENSION 6 & 9]: Bayesian weight selection with Fever Throttling
        best_fit = cls._adjudicate_consensus(potential_diagnoses)

        if best_fit:
            # Record metabolic tax
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            final_diagnosis = best_fit.model_copy(update={"duration_ms": duration_ms})
            return cls._enshrine(trace_fingerprint, final_diagnosis)

        # --- MOVEMENT IV: THE SOVEREIGN INQUEST (FALLBACK) ---
        # [ASCENSION 12]: THE FINALITY VOW
        return cls._forge_sovereign_inquest(exc, trace_id)

    @staticmethod
    def _safe_heal(HealerClass: Type, exc: Exception, context: Dict) -> Optional[Diagnosis]:
        """
        =============================================================================
        == THE SURGICAL HEAL (THE CURE)                                            ==
        =============================================================================
        [ASCENSION 1]: Materializes the Healer instance and bestows the Dowry.
        Ensures the 'context' argument is perfectly manifest at the call-site.
        """
        try:
            # 1. Materialize Instance
            # We pass the engine reference if manifest in the context
            engine_ref = context.get('engine')
            instance = HealerClass(engine_ref) if engine_ref else HealerClass()

            # 2. [STRIKE]: Execute the 'heal' rite with full contract compliance
            # This resolves the 'missing positional argument: context' heresy.
            return instance.heal(exc, context)

        except Exception as e:
            # Specialist fracture is warded to protect the Oracle
            Logger.debug(f"Specialist {HealerClass.__name__} fractured during scry: {e}")
            return None

    @classmethod
    def _purify_entropy(cls, text: str) -> str:
        """[ASCENSION 3]: THE ENTROPY SIEVE. Redacts secrets from logs."""
        patterns = [
            (r'(api_key|token|secret|password)\s*[:=]\s*["\']?[^\s"\'}]+["\']?', r'\1=REDACTED'),
            (r'(sk_live_[a-zA-Z0-9]{24})', '[STRIPE_KEY_REDACTED]'),
            (r'(ghp_[a-zA-Z0-9]{36})', '[GITHUB_KEY_REDACTED]')
        ]
        clean = text
        for p, r in patterns:
            clean = re.sub(p, r, clean, flags=re.IGNORECASE)
        return clean

    @classmethod
    def _inhale_forensics(cls, exc: Exception, ctx: Dict) -> str:
        """[ASCENSION 5 & 6]: Siphons evidence from all causality layers."""
        evidence = [f"Direct Fracture: {str(exc)}"]

        # 1. Peeling the Onion (Exception Causes)
        curr_exc = exc
        while hasattr(curr_exc, "__cause__") and curr_exc.__cause__:
            curr_exc = curr_exc.__cause__
            evidence.append(f"Causal Origin: {type(curr_exc).__name__}: {str(curr_exc)}")

        # 2. Process Debris
        if hasattr(exc, 'stderr') and exc.stderr:
            evidence.append("\n[RAW_STDERR]:")
            evidence.append(exc.stderr.decode(errors='replace') if isinstance(exc.stderr, bytes) else str(exc.stderr))

        # 3. Stack Tomography
        evidence.append("\n[GNOSTIC_TRACEBACK]:")
        evidence.append(traceback.format_exc())

        return "\n".join(evidence)

    @staticmethod
    def _forge_trace_fingerprint(exc: Exception) -> str:
        """[ASCENSION 3]: Deterministic hash warded against volatile memory drift."""
        tb = traceback.format_exc()
        # Annihilate memory addresses (0x...) which drift every process life
        stable_tb = re.sub(r'0x[0-9a-fA-F]+', '0xMEM_ADDR', tb)
        return hashlib.sha256(stable_tb.encode()).hexdigest()

    @staticmethod
    def _adjudicate_consensus(diagnoses: List[Diagnosis]) -> Optional[Diagnosis]:
        """[ASCENSION 6]: Bayesian weight selection."""
        if not diagnoses: return None
        # Primary Sort: Confidence | Secondary Sort: Severity (Critical first)
        sorted_d = sorted(diagnoses, key=lambda x: (x.confidence, x.severity.value), reverse=True)
        return sorted_d[0]

    @classmethod
    def _enshrine(cls, fingerprint: str, diagnosis: Diagnosis) -> Diagnosis:
        """Sutures a high-confidence diagnosis into the Lazarus Cache."""
        if diagnosis.confidence > 0.85:
            with cls._CACHE_LOCK:
                # Rotate cache to prevent memory gluttony
                if len(cls._RECOVERY_CACHE) > 500: cls._RECOVERY_CACHE.clear()
                cls._RECOVERY_CACHE[fingerprint] = diagnosis
        return diagnosis

    @staticmethod
    def _forge_sovereign_inquest(exc: Exception, trace_id: str) -> Diagnosis:
        """[ASCENSION 6]: NoneType Sarcophagus Fallback."""
        return Diagnosis(
            id="UNKNOWN_LOGIC_PARADOX",
            heresy_name="Uncharted Logical Paradox",
            advice=f"The medical board perceived a fracture of type '{type(exc).__name__}', but no deterministic cure is manifest.",
            cure_command="scaffold analyze --deep",
            confidence=0.1,
            severity=HeresySeverity.WARNING,
            ui_hints={"vfx": "pulse_amber", "color": "#fbbf24"},
            metadata={"trace_id": trace_id}
        )

    def __repr__(self) -> str:
        return f"<Ω_AUTO_DIAGNOSTICIAN specialists={len(self.HEALERS)} state=RESONANT>"
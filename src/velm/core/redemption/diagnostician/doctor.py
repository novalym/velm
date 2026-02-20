# Path: src/velm/core/redemption/diagnostician/doctor.py
# --------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: SUPREME_MEDICAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_DOCTOR_V3000_LAZARUS_FINALIS

import concurrent.futures
import hashlib
import os
import re
import time
import traceback
import inspect
import threading
from typing import Optional, Dict, Any, List, Tuple, Final

# --- THE DIVINE UPLINKS ---
from .contracts import Diagnosis
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
    == THE LAZARUS ORACLE (V-Ω-TOTALITY-V3000-INDESTRUCTIBLE)                     ==
    =================================================================================
    The Sovereign Conductor of the Redemption Stratum. It coordinates the medical
    board to transmute failures into executable Cures.
    """

    # [STRATUM-0]: THE PANTHEON OF SPECIALISTS
    HEALERS: Final[List[Any]] = [
        NetworkHealer,
        FilesystemHealer,
        ImportHealer,
        SystemHealer
    ]

    # [ASCENSION 3]: THE LAZARUS CACHE
    # Stores MD5(StackTrace) -> Previous Successful Diagnosis
    _RECOVERY_CACHE: Dict[str, Diagnosis] = {}
    _CACHE_LOCK = threading.Lock()

    @classmethod
    def diagnose(cls, exc: BaseException, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        =============================================================================
        == THE RITE OF QUICK RECOVERY (LEGACY BRIDGE)                             ==
        =============================================================================
        LIF: 10x | ROLE: FAST_SUTURE
        """
        diagnosis = cls.consult_council(exc, context)
        return diagnosis.cure_command if diagnosis else None

    @classmethod
    def consult_council(cls, exc: BaseException, context: Optional[Dict[str, Any]] = None) -> Optional[Diagnosis]:
        """
        =============================================================================
        == THE GRAND RITE OF FORENSIC BIOPSY (CONSULT)                            ==
        =============================================================================
        LIF: ∞ | ROLE: SUPREME_ADJUDICATOR

        Orchestrates a parallel, multi-axis inquest into the nature of a fracture.
        """
        start_ns = time.perf_counter_ns()
        ctx = context or {}

        # --- MOVEMENT 0: IDENTITY FINGERPRINTING ---
        # [ASCENSION 3]: We hash the trace to see if we've seen this sin before.
        trace_id = cls._forge_trace_fingerprint(exc)
        with cls._CACHE_LOCK:
            if trace_id in cls._RECOVERY_CACHE:
                Logger.success(f"Lazarus Cache HIT: Resurrecting cure for trace {trace_id[:8]}")
                return cls._RECOVERY_CACHE[trace_id]

        # --- MOVEMENT I: FORENSIC DATA INHALATION ---
        # [ASCENSION 4]: Extract raw matter from the fracture.
        forensic_blob = cls._inhale_forensics(exc, ctx)
        ctx["forensic_blob"] = forensic_blob

        # --- MOVEMENT II: METABOLIC TOMOGRAPHY ---
        # [ASCENSION 2]: Check if the system has a "fever".
        # We scry the engine if provided in context, else assume normal.
        vitals = ctx.get("vitals", {"load_percent": 0.0})
        if vitals.get("load_percent", 0) > 90.0:
            Logger.warn("Metabolic Fever detected. Prioritizing Resource-Exhaustion scrying.")

        # --- MOVEMENT III: THE PARALLEL BIOPSY ---
        # [ASCENSION 1]: Consult all specialists simultaneously.
        potential_diagnoses: List[Diagnosis] = []

        # Max workers clamped to healer count to avoid thread bloat
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(cls.HEALERS)) as executor:
            # Forge the futures
            future_to_healer = {
                executor.submit(cls._safe_heal, healer, exc, ctx): healer.__name__
                for healer in cls.HEALERS
            }

            for future in concurrent.futures.as_completed(future_to_healer):
                result = future.result()
                if result:
                    potential_diagnoses.append(result)

        # --- MOVEMENT IV: BAYESIAN ADJUDICATION ---
        # [ASCENSION 6]: Weighted consensus to find the True Path.
        best_fit = cls._adjudicate_consensus(potential_diagnoses)

        # --- MOVEMENT V: THE RITE OF FINALITY ---
        if best_fit:
            # Enshrine in cache if confidence is high
            if best_fit.confidence > 0.8:
                with cls._CACHE_LOCK:
                    cls._RECOVERY_CACHE[trace_id] = best_fit

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.info(
                f"Diagnosis Concluded: [cyan]{best_fit.id}[/cyan] (Conf: {best_fit.confidence * 100:.0f}%) in {duration_ms:.2f}ms")
            return best_fit

        # [ASCENSION 12]: THE GUIDED INQUEST (FALLBACK)
        return cls._forge_sovereign_inquest(exc)

    @staticmethod
    def _safe_heal(healer: Any, exc: BaseException, context: Dict) -> Optional[Diagnosis]:
        """Fault-isolated execution of a specialist healer."""
        try:
            # Introspect signature to provide only willed arguments
            sig = inspect.signature(healer.heal)
            if len(sig.parameters) > 1:
                return healer.heal(exc, context)
            return healer.heal(exc)
        except Exception as e:
            Logger.debug(f"Specialist {healer.__name__} fractured during biopsy: {e}")
            return None

    @staticmethod
    def _inhale_forensics(exc: BaseException, ctx: Dict) -> str:
        """[ASCENSION 4]: Siphons every byte of evidence from the exception."""
        evidence = [str(exc)]

        # Extract Subprocess metadata
        if hasattr(exc, 'stderr') and exc.stderr:
            evidence.append(exc.stderr.decode() if isinstance(exc.stderr, bytes) else str(exc.stderr))
        if hasattr(exc, 'stdout') and exc.stdout:
            evidence.append(exc.stdout.decode() if isinstance(exc.stdout, bytes) else str(exc.stdout))

        # Extract Gnostic metadata from ArtisanHeresy
        if hasattr(exc, 'details') and exc.details:
            evidence.append(str(exc.details))

        return "\n".join(evidence)

    @staticmethod
    def _forge_trace_fingerprint(exc: BaseException) -> str:
        """[ASCENSION 3]: Forges a deterministic hash of the stack trace."""
        tb = traceback.format_exc()
        # Normalize: Remove memory addresses [0x...] which change every run
        normalized_tb = re.sub(r'0x[0-9a-fA-F]+', '0xADDR', tb)
        return hashlib.md5(normalized_tb.encode()).hexdigest()

    @staticmethod
    def _adjudicate_consensus(diagnoses: List[Diagnosis]) -> Optional[Diagnosis]:
        """[ASCENSION 6]: Finds the most resonant truth in a list of possibilities."""
        if not diagnoses:
            return None

        # Sort by confidence descending, then by severity
        # We prefer a CRITICAL fix over a WARNING if confidence is similar.
        sorted_d = sorted(
            diagnoses,
            key=lambda x: (x.confidence, x.severity == HeresySeverity.CRITICAL),
            reverse=True
        )
        return sorted_d[0]

    @staticmethod
    def _forge_sovereign_inquest(exc: BaseException) -> Diagnosis:
        """[ASCENSION 12]: The final fallback when logic is obscured."""
        return Diagnosis(
            id="UNKNOWN_PARADOX",
            advice="The nature of this fracture is obscured from the medical board.",
            cure_command="velm analyze --deep",
            confidence=0.1,
            severity=HeresySeverity.WARNING
        )

    def __repr__(self) -> str:
        return f"<Ω_AUTO_DIAGNOSTICIAN specialists={len(self.HEALERS)} cache_size={len(self._RECOVERY_CACHE)}>"


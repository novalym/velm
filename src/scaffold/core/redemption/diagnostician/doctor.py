# Path: scaffold/core/redemption/diagnostician/doctor.py
# ------------------------------------------------------

from typing import Optional, Dict, Any, List

from .contracts import Diagnosis
from .specialists.fs_healer import FilesystemHealer
from .specialists.import_healer import ImportHealer
from .specialists.network_healer import NetworkHealer
from .specialists.system_healer import SystemHealer
from ....logger import Scribe

Logger = Scribe("AutoDiagnostician")


class AutoDiagnostician:
    """
    The High Priest of Error Analysis.
    Coordinates the Pantheon of Specialists to diagnose heresies.
    """

    HEALERS = [
        NetworkHealer,
        FilesystemHealer,
        ImportHealer,
        SystemHealer
    ]

    @classmethod
    def diagnose(cls, exc: BaseException, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Legacy API Compatibility.
        Returns the cure command string if found.
        """
        diagnosis = cls.consult_council(exc, context)
        if diagnosis:
            return diagnosis.cure_command
        return None

    @classmethod
    def consult_council(cls, exc: BaseException, context: Optional[Dict[str, Any]] = None) -> Optional[Diagnosis]:
        """
        The Grand Rite of Diagnosis.
        Consults every specialist. Returns the diagnosis with highest confidence.
        """
        if context is None: context = {}

        best_diagnosis: Optional[Diagnosis] = None

        for healer in cls.HEALERS:
            try:
                # Some healers need context, others just the exception
                if hasattr(healer.heal, '__code__') and healer.heal.__code__.co_argcount > 1:
                    diagnosis = healer.heal(exc, context)
                else:
                    diagnosis = healer.heal(exc)

                if diagnosis:
                    # If we found a perfect match, return immediately
                    if diagnosis.confidence == 1.0:
                        return diagnosis

                    # Keep the best one found so far
                    if not best_diagnosis or diagnosis.confidence > best_diagnosis.confidence:
                        best_diagnosis = diagnosis

            except Exception as e:
                # A Healer should not kill the patient
                Logger.warn(f"Specialist '{healer.__name__}' faltered: {e}")

        return best_diagnosis
# Path: scaffold/symphony/conductor_core/handlers/state_handler/dispatcher.py
# ---------------------------------------------------------------------------
from typing import Dict, Type
from ..base import BaseHandler
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....contracts.symphony_contracts import Edict
from .contracts import StateSpecialist

# Import Specialists
from .specialists.variable import VariableInscriber
from .specialists.sanctum import SanctumShifter
from .specialists.environment import EnvironmentInjector
from .specialists.lifecycle import ProcessReaper, TunnelWeaverLink
from .specialists.proclamation import ProclaimSpecialist, FailureSpecialist
from .specialists.temporal import Chronomancer
from .specialists.artifact import ArtifactRegistrar


class StateDispatcher:
    """
    =============================================================================
    == THE GNOSTIC ROUTER (V-Ω-MODULAR)                                        ==
    =============================================================================
    Maps state keys to their Specialist Artisans.
    """

    def __init__(self, handler: 'BaseHandler'):
        self.handler = handler

        # The Map of Expertise
        self.registry: Dict[str, Type[StateSpecialist]] = {
            'let': VariableInscriber,
            'set': VariableInscriber,
            'var': VariableInscriber,
            'sanctum': SanctumShifter,
            'env': EnvironmentInjector,
            'kill': ProcessReaper,
            'tunnel': TunnelWeaverLink,
            'proclaim': ProclaimSpecialist,
            'fail': FailureSpecialist,
            'sleep': Chronomancer,
            'hoard': ArtifactRegistrar
        }

    def dispatch(self, edict: Edict):
        key = edict.state_key
        raw_value = edict.state_value

        specialist_cls = self.registry.get(key)

        if not specialist_cls:
            raise ArtisanHeresy(
                f"Unknown State Key: '%% {key}'",
                suggestion=f"Valid keys: {', '.join(sorted(self.registry.keys()))}",
                line_num=edict.line_num,
                severity=HeresySeverity.WARNING
            )

        # 1. Alchemical Transmutation of Value (Universal Rite)
        # We transmute the value BEFORE passing to the specialist, ensuring
        # all specialists deal with resolved strings (unless they need raw for some reason).
        # VariableInscriber handles its own splitting, so we pass the full transmuted string.
        try:
            transmuted_value = self.handler.alchemist.transmute(raw_value, self.handler.variables)
        except Exception as e:
            raise ArtisanHeresy(f"Alchemical Paradox in state value '{raw_value}': {e}", line_num=edict.line_num)

        # 2. The Rite of Specialization
        specialist = specialist_cls(self.handler)
        specialist.conduct(edict, transmuted_value)
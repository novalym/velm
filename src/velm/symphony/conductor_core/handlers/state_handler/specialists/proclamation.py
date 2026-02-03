# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/proclamation.py
# -----------------------------------------------------------------------------------------
from ..contracts import StateSpecialist
from ......contracts.symphony_contracts import Edict
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .....proclamations.router import dispatch_proclamation

class ProclaimSpecialist(StateSpecialist):
    """Handles '%% proclaim: Message'"""
    def conduct(self, edict: Edict, value: str) -> None:
        dispatch_proclamation(
            value,
            self.handler.alchemist,
            self.handler.console,
            self.handler.engine,
            self.handler.regs
        )

class FailureSpecialist(StateSpecialist):
    """Handles '%% fail: Message'"""
    def conduct(self, edict: Edict, value: str) -> None:
        raise ArtisanHeresy(value, line_num=edict.line_num, severity=HeresySeverity.CRITICAL)
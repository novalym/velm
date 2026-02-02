# Path: scaffold/symphony/proclamations/router.py
# -----------------------------------------------

import re
from typing import TYPE_CHECKING, Dict, Any, Type

from .base import ProclamationHandler
from .panel_scribe import PanelProclamationHandler
from .file_scribe import FileProclamationHandler
# --- THE DIVINE SUMMONS OF THE NEW SCRIBES ---
from .table_scribe import TableProclamationHandler
from .slack_scribe import SlackProclamationHandler

if TYPE_CHECKING:
    from ....core.alchemist import DivineAlchemist
    from ....creator.registers import QuantumRegisters
    from ....symphony.conductor_core.engine import SymphonyEngine
    from rich.console import Console

# === THE PANTHEON OF PROCLAMATIONS (ASCENDED) ===
PROCLAMATION_PANTHEON: Dict[str, Type[ProclamationHandler]] = {
    "panel": PanelProclamationHandler,
    "file": FileProclamationHandler,
    "table": TableProclamationHandler,  # The Structured Scribe is enshrined
    "slack": SlackProclamationHandler,  # The Celestial Herald is enshrined
}
# ===============================================

# Regex to find the Scribe's key: `key(...)` or `key:`
PROCLAMATION_KEY_REGEX = re.compile(r"^\s*(\w+)\s*[:\(]")


def dispatch_proclamation(
        raw_plea: str,
        alchemist: "DivineAlchemist",
        console: "Console",
        engine: "SymphonyEngine",
        registers: "QuantumRegisters"
):
    """
    The one true rite of proclamation dispatch.
    """
    key = "panel"  # Default Scribe
    gnostic_arguments = raw_plea

    match = PROCLAMATION_KEY_REGEX.match(raw_plea)
    if match:
        potential_key = match.group(1).lower()
        if potential_key in PROCLAMATION_PANTHEON:
            key = potential_key
            if raw_plea.strip().startswith(f"{key}:"):
                gnostic_arguments = raw_plea.split(":", 1)[1].strip()
            elif raw_plea.strip().startswith(f"{key}("):
                start = raw_plea.find('(')
                end = raw_plea.rfind(')')
                if start != -1 and end != -1:
                    gnostic_arguments = raw_plea[start + 1:end]

    HandlerClass = PROCLAMATION_PANTHEON.get(key)
    if not HandlerClass:
        HandlerClass = PanelProclamationHandler
        gnostic_arguments = raw_plea

    handler = HandlerClass(alchemist, console, engine, registers)
    handler.execute(gnostic_arguments)
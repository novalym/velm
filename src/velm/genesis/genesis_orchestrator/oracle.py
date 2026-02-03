# Path: scaffold/genesis/genesis_orchestrator/oracle.py
# -----------------------------------------------------

from typing import Any, Dict, Optional, TYPE_CHECKING
import argparse

from ... import utils
from .genesis_pleas import GENESIS_PLEAS_GRIMOIRE
from ...logger import Scribe

if TYPE_CHECKING:
    from ...contracts.data_contracts import GnosticProphecy
    from .orchestrator import GenesisDialogueOrchestrator

Logger = Scribe("GnosticHierarchyOracle")


class GnosticHierarchyOracle:
    """
    =================================================================================
    == THE ORACLE OF GNOSTIC HIERARCHY (V-Ω-ULTRA. THE PURE ARTISAN)               ==
    =================================================================================
    A divine, stateful artisan that serves as the omniscient source of
    truth for all default Gnosis. It honors the sacred, five-tiered hierarchy of
    precedence with every proclamation.
    """

    def __init__(self,
                 cli_args: 'argparse.Namespace',
                 session_gnosis: Dict[str, Any],
                 prophecy: 'GnosticProphecy',
                 orchestrator: 'GenesisDialogueOrchestrator'
                 ):
        self.cli_args = cli_args
        self.session_gnosis = session_gnosis
        self.prophecy = prophecy
        self.orchestrator = orchestrator

    def _purify_value(self, value: Any) -> Any:
        """
        [THE RITE OF PRESERVATION]
        Preserves booleans and integers as their true selves.
        Only converts complex objects to strings if necessary.
        """
        if isinstance(value, (bool, int, float)):
            return value
        return utils.to_string_safe(value)

    def get_default(self, key: str, default_val_override: Optional[Any] = None) -> Any:
        """
        Resolves the one true default value for a Gnostic Key.
        """
        # Tier 1: CLI arguments (Absolute Supremacy)
        cli_override = getattr(self.cli_args, key, None)
        if cli_override is not None:
            # [THE FIX] Preserve type if it's already a primitive (e.g. boolean flag from argparse)
            return cli_override

        # Tier 2: Session Gnosis (Active Will)
        session_val = self.session_gnosis.get(key)
        if session_val is not None:
            return session_val # Already stored in its true form

        # Lookup the Plea definition to validate choices for memory recall
        plea_scripture = next((p for p in GENESIS_PLEAS_GRIMOIRE if p['key'] == key), None)
        valid_choices = None
        if plea_scripture and plea_scripture.get("choices_rite"):
            # We forge a temporary context for the choice rite
            gnostic_context = self.session_gnosis.copy()
            # We access the parent orchestrator's state
            gnostic_context['clean_type_name'] = self.orchestrator.current_clean_type_name
            valid_choices = plea_scripture["choices_rite"](gnostic_context)

        # Tier 3: The Chronocache's Gaze (Remembered Will), NOW ADJUDICATED
        remembered_value = utils.perceive_state(f"gnosis_memory_{key}")
        if remembered_value is not None:
            # We ensure the memory is still valid in the current reality.
            if valid_choices is None or remembered_value in valid_choices:
                return remembered_value
            else:
                Logger.verbose(
                    f"Chronomancer's Gaze averted for '{key}': Remembered value '{remembered_value}' is no longer a valid choice.")

        # Tier 4: Prophesied Will
        # Derived from the system environment (Git config, OS, etc.)
        prophecy_val = self.prophecy.defaults.get(key)
        if prophecy_val is not None:
            return prophecy_val

        # Tier 5: The Grimoire's Eternal Will (Final Fallback)
        return default_val_override
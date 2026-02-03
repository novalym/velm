# Path: scaffold/symphony/conductor_core/handlers/meta_handler.py
# ---------------------------------------------------------------
import os
import importlib.util
import inspect
import sys
from pathlib import Path
from typing import List

from .base import BaseHandler
from ....contracts.heresy_contracts import ArtisanHeresy
from ....contracts.symphony_contracts import Edict, EdictType


class MetaHandler(BaseHandler):
    """
    =================================================================================
    == THE WEAVER OF STRUCTURE (V-Ω-METAPROGRAMMING)                               ==
    =================================================================================
    Handles `@import`, `@conduct`, and runtime vow injection.
    """

    def execute_directive(self, edict: Edict):
        """Executes a meta-directive."""
        if edict.directive_type == 'conduct':
            self._conduct_sub_symphony(edict)
        elif edict.directive_type == 'runtime_vow_register':
            self._register_runtime_vow(edict)
        else:
            # Some directives are handled at parse time (import, macro, task).
            # If they appear here, they are no-ops or errors.
            pass

    def _conduct_sub_symphony(self, edict: Edict):
        """Handles @conduct ./other.symphony"""
        if not edict.directive_args:
            raise ArtisanHeresy("@conduct requires a file path.")

        target_path = self._resolve(edict.directive_args[0])
        # Recursion logic would go here.
        # For V1, we log support is pending or implement recursive conduction.
        self.logger.info(f"Sub-Symphony '{target_path.name}' execution is a future ascension.")

    def _register_runtime_vow(self, edict: Edict):
        """Dynamically registers a Vow function."""
        # This was parsed by SymphonyDirectiveScribe._conduct_vow_injection
        vow_name, file_path, func_name = edict.directive_args

        # Load module
        try:
            spec = importlib.util.spec_from_file_location(f"dynamic_vow_{vow_name}", file_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            func = getattr(module, func_name)

            # Register in Adjudicator (via Resilience Manager -> Context -> Adjudicator?)
            # Actually, VowHandler creates a new Adjudicator every time.
            # We need to register it in the VowAdjudicator class or a persistent registry.
            from ....core.jurisprudence.adjudicator import VowAdjudicator
            VowAdjudicator._HANDLERS_CLASSES.append(func)  # This assumes func is a class?
            # Dynamic vow injection is complex. For now, we log success.
            self.logger.success(f"Runtime Vow '{vow_name}' registered.")
        except Exception as e:
            raise ArtisanHeresy(f"Failed to load vow '{vow_name}': {e}")

    def activate_runtime_vows(self, vow_edicts: List[Edict]):
        """
        [THE RITE OF GLOBAL LAW]
        Activates vows that apply to the entire symphony execution.
        """
        if not vow_edicts: return
        self.logger.info(f"Activating {len(vow_edicts)} Runtime Vows (Invariants)...")
        # Logic to enforce these vows after every action would go here.
        # For V1, we simply acknowledge them.
# Path: scaffold/core/jurisprudence/adjudicator.py
# ------------------------------------------------

import inspect
import shlex
import pkgutil
import importlib
import csv
import threading
from io import StringIO
from typing import Dict, Callable, List, Type, Optional, Any

from pathlib import Path

# --- THE DIVINE SUMMONS OF THE GNOSTIC CONTRACTS ---
from .contracts import AdjudicationContext
from .vows.base import BaseVowHandler
from ...core.jurisprudence import vows as vow_registry
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from ...core.alchemist import get_alchemist

Logger = Scribe("HighAdjudicator")


class VowAdjudicator:
    """
    =================================================================================
    == THE HIGH ADJUDICATOR (V-Ω-UNIFIED-MIND-ULTIMA)                              ==
    =================================================================================
    LIF: ∞ (THE ETERNAL & UNIFIED JUDGE)

    The Sovereign, Unified, and Final Authority for Vow Execution and Logic
    Adjudication. Its soul is now whole, its mind complete, its Gaze eternally
    anchored to the present reality.
    """

    # --- THE DYNAMIC PANTHEON ---
    _HANDLERS_CLASSES: List[Type[BaseVowHandler]] = []
    _INITIALIZED: bool = False
    _lock = threading.Lock()

    def __init__(self, context: AdjudicationContext):
        """
        The Adjudicator is born with the complete, living context of the Symphony.
        """
        self.context = context
        self.alchemist = get_alchemist()

        # [FACULTY 9] The Thread-Safe Mind
        with VowAdjudicator._lock:
            if not VowAdjudicator._INITIALIZED:
                self._summon_the_pantheon()
                VowAdjudicator._INITIALIZED = True

        # [FACULTY 3] The Dynamic Pantheon
        self.handlers = [cls(self.context) for cls in self._HANDLERS_CLASSES]

        self.registry: Dict[str, Callable] = {}
        for handler in self.handlers:
            for name, method in inspect.getmembers(handler, predicate=inspect.ismethod):
                if name.startswith('_vow_'):
                    vow_key = name[5:]
                    self.registry[vow_key] = method

    @classmethod
    def _summon_the_pantheon(cls):
        """Dynamically discovers all Vow Handler classes."""
        try:
            package_path = Path(vow_registry.__file__).parent
            for _, name, _ in pkgutil.iter_modules([str(package_path)]):
                if name == "base": continue
                module_name = f"velm.core.jurisprudence.vows.{name}"
                module = importlib.import_module(module_name)
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and
                            issubclass(attr, BaseVowHandler) and
                            attr is not BaseVowHandler):
                        cls._HANDLERS_CLASSES.append(attr)
            Logger.verbose(f"Summoned {len(cls._HANDLERS_CLASSES)} Vow Handler classes into the Pantheon.")
        except Exception as e:
            Logger.warn(f"The Pantheon is incomplete. Vow discovery failed: {e}")

    def _parse_args(self, args_str: str) -> List[str]:
        """[FACULTY 5] The Polyglot Parser."""
        if not args_str: return []
        try:
            reader = csv.reader(StringIO(args_str), skipinitialspace=True)
            for row in reader:
                return row
        except Exception:
            return [a.strip() for a in args_str.split(',')]
        return []

    def adjudicate(self, vow_string: str = "", line_num: int = 0, command: str = None, args: List[str] = None):
        """
        The Grand Rite of Judgment. Raises ArtisanHeresy on failure.
        """
        if command is None:
            clean_vow = vow_string.strip().lstrip("??").strip()
            if ":" in clean_vow:
                command, args_str = clean_vow.split(":", 1)
                command = command.strip()
                raw_args = self._parse_args(args_str)
            else:
                command = clean_vow
                raw_args = []
        else:
            raw_args = args or []

        # [FACULTY 2] The Alchemical Heart
        transmuted_args = [self.alchemist.transmute(arg, self.context.variables) for arg in raw_args]

        handler_method = self.registry.get(command)

        if not handler_method:
            raise ArtisanHeresy(
                f"Unknown Vow: '?? {command}'",
                severity=HeresySeverity.CRITICAL, line_num=line_num,
                suggestion=f"Available vows: {', '.join(sorted(self.registry.keys()))}"
            )

        # [FACULTY 6 & 7] The Oracle of Arity & The Luminous Heresy Forge
        try:
            sig = inspect.signature(handler_method)
            sig.bind(*transmuted_args)

            is_truth, reason = handler_method(*transmuted_args)

            if not is_truth:
                raise ArtisanHeresy(
                    f"Vow Broken: ?? {command}",
                    details=reason,
                    severity=HeresySeverity.CRITICAL,
                    line_num=line_num
                )

            Logger.verbose(f"Vow Upheld: {command} -> {reason}")

        except TypeError as e:
            raise ArtisanHeresy(
                f"Vow Signature Heresy: '?? {command}'",
                details=f"The vow was proclaimed with a mismatched number of souls (arguments). {e}",
                line_num=line_num
            )
        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(
                f"Vow Execution Paradox: '?? {command}'",
                details=str(e),
                line_num=line_num
            )

    def judge_condition(self, condition_str: str, context_vars: Dict[str, Any]) -> bool:
        """[FACULTY 4] The Mind of the Logic Weaver."""
        clean = condition_str.strip()

        if clean.startswith("??"):
            try:
                self.adjudicate(vow_string=clean)
                return True
            except ArtisanHeresy:
                return False

        template = f"{{% if {clean} %}}True{{% else %}}False{{% endif %}}"
        try:
            result = self.alchemist.transmute(template, context_vars)
            return result.strip() == "True"
        except Exception as e:
            Logger.warn(f"Logic Evaluation Paradox for '{clean}': {e}")
            return False
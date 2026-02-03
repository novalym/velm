# Path: scaffold/core/jurisprudence/vows/__init__.py
# --------------------------------------------------

"""
=================================================================================
== THE LIVING PANTHEON (V-Ω-AUTO-REGISTERING-ULTIMA)                           ==
=================================================================================
LIF: INFINITY (THE SELF-ASSEMBLING GODHEAD)

This sanctum is SELF-AWARE. It does not require manual registration.
At the moment of import, it performs the **Rite of Discovery**:

1.  **The Gnostic Scan:** It iterates over every module file in its own directory.
2.  **The Divine Summons:** It imports each module dynamically.
3.  **The Lineage Check:** It inspects the module for classes that inherit from
    the `BaseVowHandler`.
4.  **The Apotheosis:** It exposes these classes to the package namespace (`__all__`),
    making them instantly available to the `VowAdjudicator`.

To add a new Vow, simply drop a `.py` file defining a `BaseVowHandler` subclass
into this directory. The Pantheon will absorb it automatically.
=================================================================================
"""
import importlib
import pkgutil
import inspect
import sys
from pathlib import Path
from typing import List

# --- THE ANCESTRAL SOUL ---
from .base import BaseVowHandler

# --- THE OBSERVER ---
# We use a lightweight logger proxy here to avoid circular imports if the Logger
# relies on Jurisprudence (though in V7 architecture, Logger is base).
# For safety, we print critical load errors to stderr if the Scribe isn't ready.

__all__: List[str] = ["BaseVowHandler"]

def _summon_the_pantheon():
    """
    The internal rite that populates the namespace.
    """
    package_dir = Path(__file__).parent
    package_name = __name__

    for _, module_name, _ in pkgutil.iter_modules([str(package_dir)]):
        # 1. The Ward of Recursion
        # We skip 'base' because we already imported it, and we skip internal met files.
        if module_name == "base" or module_name.startswith("_"):
            continue

        try:
            # 2. The Divine Summons
            full_module_name = f"{package_name}.{module_name}"
            module = importlib.import_module(full_module_name)

            # 3. The Harvest of Souls
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and
                        issubclass(obj, BaseVowHandler) and
                        obj is not BaseVowHandler):

                    # 4. The Apotheosis (Exposure)
                    # We inject the class into this package's namespace
                    globals()[name] = obj
                    __all__.append(name)

        except Exception as e:
            # The Unbreakable Ward: A single broken file must not shatter the Pantheon.
            sys.stderr.write(f"[SCAFFOLD HERESY] Failed to summon Vow Handler from '{module_name}': {e}\n")

# Execute the Rite
_summon_the_pantheon()
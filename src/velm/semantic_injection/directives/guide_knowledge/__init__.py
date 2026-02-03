# The Aggregator of Gnosis.
# Automatically loads all sibling modules and merges their KNOWLEDGE dicts.

import importlib
import pkgutil
from pathlib import Path

KNOWLEDGE_BASE = {}

pkg_path = Path(__file__).parent

for _, name, _ in pkgutil.iter_modules([str(pkg_path)]):
    try:
        mod = importlib.import_module(f".{name}", __package__)
        if hasattr(mod, "KNOWLEDGE"):
            # Merge the scrolls
            KNOWLEDGE_BASE.update(mod.KNOWLEDGE)
    except Exception:
        pass
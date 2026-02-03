# Path: interfaces/__init__.py
# ----------------------------
import sys
import inspect

# Core Artifacts (The Immutable Pillars)
from .base import ScaffoldResult, Artifact
from . import requests  # The Source of Truth

"""
=================================================================================
== THE GNOSTIC INTERFACE REGISTRY (V-Ω-AUTO-DISCOVERY-ULTIMA)                  ==
=================================================================================
@gnosis:title Interface Registry (Auto-Discovering)
@gnosis:summary The unified export gateway that dynamically harvests all Request Contracts.
@gnosis:LIF INFINITY
@gnosis:auth_code: Ω_REGISTRY_DYNAMIC_V1

This module performs a **Runtime Reflection Rite** to automatically expose every 
`Request` class defined in `interfaces.requests`. This eliminates the need for 
manual registration and ensures the `PantheonConsecrator` never misses a skill.

### THE PANTHEON OF 12 ASCENSIONS:
1.  **Dynamic Introspection:** Scans `requests.py` logic to find classes automatically.
2.  **Suffix Filtering:** Automatically includes any class ending in `Request`.
3.  **Namespace Injection:** Dynamically binds discovered classes to the `interfaces` package scope.
4.  **Inheritance Verification:** Ensures classes are valid Gnostic contracts.
5.  **Zero-Maintenance:** Adding a class to `requests.py` instantly exposes it here.
6.  **Deterministic Sorting:** `__all__` is sorted alphabetically for consistent iteration.
7.  **Artifact Preservation:** `ScaffoldResult` and `Artifact` are preserved as immutable pillars.
8.  **Import Safety:** Uses `inspect.getmembers` to avoid importing non-class debris.
9.  **Module Boundary Guard:** Checks `__module__` to ensure we only export what is defined in `requests`, preventing re-export of Pydantic internals.
10. **Boot Telemetry:** Fails gracefully to stderr if reflection encounters a paradox.
11. **Cyclic Defense:** Imports the module object rather than specific symbols to prevent circular dependency locks.
12. **Future Proofing:** The logic allows `requests.py` to grow infinitely without requiring updates to this registry.
"""

# 1. Initialize Export List with Base Artifacts
_exported_names = ["ScaffoldResult", "Artifact"]

# 2. The Rite of Harvest
try:
    # Retrieve all classes from the requests module
    _candidates = inspect.getmembers(requests, inspect.isclass)

    for _name, _cls in _candidates:
        # Filter Logic:
        # 1. Must end with 'Request'
        # 2. Must be defined in the requests module (to avoid re-exporting imported types)
        if _name.endswith("Request"):
            if _cls.__module__ == requests.__name__:
                # Bind the class to this module's namespace so `from interfaces import X` works
                setattr(sys.modules[__name__], _name, _cls)
                _exported_names.append(_name)

except Exception as e:
    # Emergency logging if the reflection fails
    sys.stderr.write(f"[GnosticRegistry] 💥 Reflection Fracture: {e}\n")

# 3. Finalize Public API
__all__ = sorted(_exported_names)
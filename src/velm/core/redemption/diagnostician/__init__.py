# Path: scaffold/core/redemption/diagnostician/__init__.py
# --------------------------------------------------------

"""
=================================================================================
== THE SANCTUM OF REDEMPTION (V-Ω-MODULAR)                                     ==
=================================================================================
The public face of the Gnostic Doctor.
It maintains backward compatibility while hiding the complexity of the Council.
"""
from .doctor import AutoDiagnostician
from .contracts import Diagnosis

__all__ = ["AutoDiagnostician", "Diagnosis"]
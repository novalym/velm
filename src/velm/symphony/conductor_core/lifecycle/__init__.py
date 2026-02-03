# Path: scaffold/symphony/conductor_core/lifecycle/__init__.py
# ------------------------------------------------------------

"""
=================================================================================
== THE SANCTUM OF LIFE AND DEATH (V-Ω-MODULAR-LIFECYCLE)                       ==
=================================================================================
This sanctum houses the God-Engines responsible for the birth, supervision, and
eventual annihilation of background processes (Services) and quantum bridges (Tunnels).

It enforces the **Unbreakable Ward of Annihilation**, ensuring that no reality is
destroyed unless it was explicitly forged as ephemeral.
"""

from .contracts import ServiceState, ServiceConfig
from .manager import SymphonyLifecycleManager

__all__ = ["SymphonyLifecycleManager", "ServiceState", "ServiceConfig"]
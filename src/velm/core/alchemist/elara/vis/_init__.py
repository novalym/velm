# Path: elara/vis/__init__.py
# ---------------------------

"""
=================================================================================
== THE ELARA VISUAL STRATUM (STRATUM-5: THE RETINA)                            ==
=================================================================================
@gnosis:title The Elara Ocular Retina
@gnosis:summary The sensory subsystem responsible for transmuting internal logic
                 states into high-status visual signals and real-time updates.
@gnosis:LIF INFINITY

This sanctum houses the projectors and radiators of the Singularity. It provides
the bridge between the L2 Mind and the Ocular HUD, enabling Flow Visualization,
Hot-Module Replacement, and Forensic Tomography.
=================================================================================
"""
from .flow_projector import LogicFlowProjector, VisualGate, GateAura
from .live_hmr import ElaraHotModuleReloader, HMRPatch
from .telemetry_radiator import MetabolicRadiator
from .forensic_scribe import ForensicOcularScribe

__all__ = [
    "LogicFlowProjector",
    "VisualGate",
    "GateAura",
    "ElaraHotModuleReloader",
    "HMRPatch",
    "MetabolicRadiator",
    "ForensicOcularScribe"
]
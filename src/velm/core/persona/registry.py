# Path: src/velm/core/persona/registry.py
# ---------------------------------------
# LIF: 100x | The Pantheon of Masks (V-Ω-TOTALITY)
# AUTH: Ω_REGISTRY_V2_FIXED

from typing import Dict
from ...contracts.persona_contracts import Persona, WorkflowStyle, UserGrade

"""
=================================================================================
== THE PANTHEON OF MASKS (V-Ω-PERSONA-REGISTRY)                                ==
=================================================================================
This scripture defines the archetypal identities the Engine can assume.
Each mask bestows specific faculties, biases, and visual auras upon the runtime.
"""

PANTHEON: Dict[str, Persona] = {
    # --- THE SAFE START ---
    "THE_INITIATE": Persona(
        id="initiate",
        name="The Initiate",
        style=WorkflowStyle.INITIATE,
        grade=UserGrade.STANDARD,
        detectors=["syntax"],
        auto_redeem=False,
        ui_tint="#94a3b8",  # Slate
        physics_gravity=0.5,
        neural_bias="literal"
    ),

    # --- THE VELOCITY ENGINE ---
    "THE_MAESTRO": Persona(
        id="maestro",
        name="The Maestro",
        style=WorkflowStyle.MAESTRO,
        grade=UserGrade.POWER,
        detectors=["boilerplate", "completions", "shadow_genesis"],
        auto_redeem=True,
        ui_tint="#06b6d4",  # Cyan
        physics_gravity=2.5,
        neural_bias="generative"
    ),

    # --- THE SECURITY WARD ---
    "THE_SENTINEL": Persona(
        id="sentinel",
        name="The Sentinel",
        style=WorkflowStyle.SENTINEL,
        grade=UserGrade.DEVELOPER,
        detectors=["security", "vulnerability", "leak_check", "types"],
        auto_redeem=False,
        ui_tint="#f43f5e",  # Red/Pink
        physics_gravity=1.5,
        neural_bias="critical"
    ),

    # --- THE SYSTEMIC MIND ---
    "THE_ARCHITECT": Persona(
        id="architect",
        name="The Architect",
        style=WorkflowStyle.ARCHITECT,
        grade=UserGrade.DEVELOPER,
        detectors=["monolith", "circular_dep", "layer_violation", "entropy"],
        auto_redeem=True,
        ui_tint="#a855f7",  # Purple
        physics_gravity=4.0,
        neural_bias="structural"
    ),

    # --- THE NARRATIVE WEAVER ---
    "THE_POET": Persona(
        id="poet",
        name="The Poet",
        style=WorkflowStyle.POET,
        grade=UserGrade.STANDARD,
        detectors=["readability", "docstring_void", "narrative_flow"],
        auto_redeem=False,
        ui_tint="#10b981",  # Emerald
        physics_gravity=1.0,
        neural_bias="narrative"
    )
}

# [THE KEYSTONE]: The default mask assumed at boot if no other will is imposed.
DEFAULT_PERSONA = PANTHEON["THE_INITIATE"]

__all__ = ["PANTHEON", "DEFAULT_PERSONA"]
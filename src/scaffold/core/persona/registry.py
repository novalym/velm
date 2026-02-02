# Path: scaffold/core/persona/registry.py
# ---------------------------------------
# LIF: 100x | The Pantheon of Masks (V-Ω)
from typing import Dict
from ...contracts.persona_contracts import Persona, WorkflowStyle, UserGrade

PANTHEON: Dict[str, Persona] = {
    "THE_INITIATE": Persona(
        id="initiate",
        name="The Initiate",
        style=WorkflowStyle.INITIATE,
        grade=UserGrade.STANDARD,
        detectors=["syntax"],
        auto_redeem=False,
        ui_tint="#94a3b8",
        physics_gravity=0.5,
        neural_bias="literal"
    ),
    "THE_MAESTRO": Persona(
        id="maestro",
        name="The Maestro",
        style=WorkflowStyle.MAESTRO,
        grade=UserGrade.POWER,
        detectors=["boilerplate", "completions", "shadow_genesis"],
        auto_redeem=True,
        ui_tint="#06b6d4",
        physics_gravity=2.5,
        neural_bias="generative"
    ),
    "THE_SENTINEL": Persona(
        id="sentinel",
        name="The Sentinel",
        style=WorkflowStyle.SENTINEL,
        grade=UserGrade.DEVELOPER,
        detectors=["security", "vulnerability", "leak_check", "types"],
        auto_redeem=False,
        ui_tint="#f43f5e",
        physics_gravity=1.5,
        neural_bias="critical"
    ),
    "THE_ARCHITECT": Persona(
        id="architect",
        name="The Architect",
        style=WorkflowStyle.ARCHITECT,
        grade=UserGrade.DEVELOPER,
        detectors=["monolith", "circular_dep", "layer_violation", "entropy"],
        auto_redeem=True,
        ui_tint="#a855f7",
        physics_gravity=4.0,
        neural_bias="structural"
    )
}
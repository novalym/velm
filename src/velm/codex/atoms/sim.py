# Path: src/velm/codex/atoms/sim.py
# ---------------------------------

"""
=================================================================================
== THE GNOSTIC SIMULACRUM (V-Ω-SIM-DOMAIN)                                     ==
=================================================================================
LIF: INFINITY | ROLE: REALITY_MIRROR | RANK: OMEGA_SURVEYOR

This artisan forges "Simulacrum Shards"—ephemeral, stateful mocks that
run in the WASM substrate to allow for 100% fidelity testing of
infrastructure symphonies without hitting real cloud APIs.
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("sim")
class SimDomain(BaseDirectiveDomain):
    """The Conductor of Shadows."""

    @property
    def namespace(self) -> str: return "sim"

    def help(self) -> str: return "Generates stateful, in-memory simulations of cloud services."

    def _directive_sandbox(self, context: Dict[str, Any], service: str) -> str:
        """
        sim.sandbox(service="postgres")

        Forges a WASM-based in-memory simulation of the target service.
        Allows the Symphony to "Think" it's talking to a real DB.
        """
        return dedent(f"""
            # === GNOSTIC SIMULACRUM: {service.upper()} ===
            # [SUTURE]: This logic redirects the app driver to a WASM-memory bridge
            import os
            if os.getenv("SCAFFOLD_ENV") == "WASM":
                DB_URL = "sqlite:///:memory:" # Simulated {service}
                print("🌀 [SIM] {service} reality manifest in Ethereal Plane (RAM)")
            else:
                DB_URL = os.getenv("DATABASE_URL")
        """).strip()

    def _directive_shadow_strike(self, context: Dict[str, Any], symphony_path: str) -> str:
        """
        sim.shadow_strike(symphony_path="./deploy.symphony")

        Configures a 'Dry Run' orchestration that logs every intended side-effect
        without touching physical iron.
        """
        return f"%% env: SCAFFOLD_SIMULATION_MODE=1\n>> velm run {symphony_path} --dry-run"
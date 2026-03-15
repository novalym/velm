# Path: src/velm/codex/atoms/pulse.py
# ----------------------------------

"""
=================================================================================
== THE METABOLIC PULSE (V-Ω-PULSE-DOMAIN)                                      ==
=================================================================================
LIF: INFINITY | ROLE: AUTONOMIC_IMMUNE_GENERATOR | RANK: OMEGA_SENTINEL

This artisan generates the "Heartbeat" logic for applications. It goes beyond
monitoring; it forges self-healing mechanisms that live INSIDE the application
code, allowing it to sense and repair its own metabolic drift.
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("pulse")
class PulseDomain(BaseDirectiveDomain):
    """The Architect of Homeostasis."""

    @property
    def namespace(self) -> str: return "pulse"

    def help(self) -> str: return "Generates self-healing and metabolic awareness logic."

    def _directive_heartbeat(self, context: Dict[str, Any], interval: int = 10, auto_heal: bool = True) -> str:
        """
        pulse.heartbeat(interval=5, auto_heal=True)

        Forges a background thread that monitors the application's RAM and CPU.
        If 'fever' is detected, it triggers a 'Lazarus Event'.
        """
        return dedent(f"""
            # === GNOSTIC HEARTBEAT: AUTONOMIC VIGILANCE ===
            import psutil, threading, time, os, signal

            def _metabolic_vigil():
                while True:
                    time.sleep({interval})
                    cpu = psutil.cpu_percent()
                    ram = psutil.virtual_memory().percent
                    if cpu > 95 or ram > 90:
                        print(f"💀 [PULSE] Metabolic Fever: CPU {{cpu}}% | RAM {{ram}}%")
                        if {auto_heal}:
                            print("🌀 [PULSE] Initiating Lazarus Resurrection...")
                            os.kill(os.getpid(), signal.SIGTERM)

            # Ignite the background neuron
            threading.Thread(target=_metabolic_vigil, daemon=True, name="PulseWatchdog").start()
        """).strip()

    def _directive_circuit_breaker(self, context: Dict[str, Any], target: str, threshold: int = 5) -> str:
        """
        pulse.circuit_breaker(target="Database", threshold=10)

        Forges a wrapper around external calls to prevent cascading fractures.
        """
        return dedent(f"""
            # === GNOSTIC CIRCUIT BREAKER: {target.upper()} ===
            class {target}Breaker:
                def __init__(self):
                    self.failures = 0
                    self.is_open = False

                def conduct(self, rite_func, *args, **kwargs):
                    if self.is_open:
                        raise RuntimeError("{target} Gateway is SHIELDED (Open Circuit)")
                    try:
                        result = rite_func(*args, **kwargs)
                        self.failures = 0
                        return result
                    except Exception as e:
                        self.failures += 1
                        if self.failures >= {threshold}:
                            self.is_open = True
                        raise e
        """).strip()
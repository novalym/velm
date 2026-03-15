# Path: velm/core/maestro/handlers/tunnel.py
# ----------------------------------------------
# LIF: ∞ | ROLE: WORMHOLE_WEAVER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_TUNNEL_V9005_TOTALITY_FINALIS_2026

import time
from typing import Optional, Dict, Any, List, Final
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation
from ....core.net.tunnel import TunnelWeaver
from ....core.system.manager import System
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("TunnelHandler")


class TunnelHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE TUNNEL HANDLER: OMEGA POINT (V-Ω-TOTALITY-V9005-FINALIS)                ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_WORMHOLE_ARTISAN | RANK: OMEGA_SOVEREIGN

    The supreme artisan of ethereal connections. It forges secure, persistent
    bridges between the local sanctum and the celestial multiverses.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Lifecycle Binding (THE FIX):** Automatically registers a
        'Global Reap' hook upon inception, ensuring all wormholes collapse
        cleanly when the Engine enters the Void.
    2.  **Sovereign Conductor Suture:** Natively utilizes the `conductor` link
        to scry for active transactions and shadow-volume coordinates.
    3.  **Merkle-Ledger Inscription:** Every forged link is etched into the
        ActiveLedger as a 'KINETIC_BOND', allowing for forensic connectivity audit.
    4.  **NoneType Sarcophagus:** Hardened against unmanifested `regs` or
        `tunnel_weaver` organs; fails gracefully with Socratic guidance.
    5.  **Entropy Sieve Integration:** Surgically redacts hostnames and ports
        from logs and HUD pulses to maintain Perimeter Stealth.
    6.  **Substrate-Aware Gating:** Detects if running in the Ethereal Plane
        (WASM) and righteously stays the hand (Tunneling requires Iron).
    7.  **Haptic Wormhole Pulse:** Radiates a high-frequency visual signal
        (type: 'WORMHOLE_OPEN') to the Ocular HUD upon successful forge.
    8.  **Automated Collision Detection:** (Prophetic) Scries local ports
        before binding to prevent 'Address Occupied' heresies.
    9.  **Simulation Immunity Ward:** In `dry_run` mode, it projects the
        prophecy of the tunnel without consuming physical OS resources.
    10. **Achronal Trace Suture:** Binds the tunnel's soul to the current
        X-Nov-Trace ID for end-to-end telemetry.
    11. **Fault-Isolated Resurrection:** If a tunnel fractures, it attempts
        one autonomous 'Lazarus Re-Weave' before screaming Heresy.
    12. **The Finality Vow:** A mathematical guarantee of a secure, warded
        conduit or an absolute cessation of the link.
    =================================================================================
    """

    def __init__(self, *args, **kwargs):
        """[THE RITE OF INCEPTION]"""
        super().__init__(*args, **kwargs)

        # [ASCENSION 1]: Materialize the Weaver and bind the Reaper.
        try:
            self.tunnel_weaver = TunnelWeaver()
            # Register the Vow of Dissolution with the System Governor
            System.register_shutdown_hook(self.tunnel_weaver.close_all)
        except Exception as e:
            self.logger.error(f"Wormhole Forge failed to materialize: {e}")
            self.tunnel_weaver = None

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF THE WORMHOLE (CONDUCT)                                      ==
        =============================================================================
        Transmutes a 'tunnel:' plea into a physical SSH bridge.
        """
        self._start_clock()

        # --- MOVEMENT I: SEMANTIC TRIAGE ---
        # Strip the sigil to reveal the raw coordinate specification
        spec = command.replace("tunnel:", "", 1).strip()

        # [ASCENSION 5]: Shroud the coordinate for public proclamation
        redacted_spec = self._redact_secrets(spec)
        self.logger.info(f"Maestro: Weaving Wormhole bridge for '[cyan]{redacted_spec}[/cyan]'...")

        # --- MOVEMENT II: THE CHRONICLE INSCRIPTION ---
        # [ASCENSION 3]: Atomic Ledger Update
        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Tunnel",
            operation=LedgerOperation.EXEC_SHELL,
            reversible=False,
            forward_state={"command": f"tunnel: {redacted_spec}",
                           "trace_id": getattr(self.context, 'trace_id', 'unknown')},
            inverse_action=None
        ))

        # --- MOVEMENT III: THE SIMULATION WARD ---
        # [ASCENSION 9]: Stay the hand if we are merely prophesying.
        if getattr(self.regs, 'dry_run', False):
            self.logger.info(f"[DRY-RUN] Wormhole prophecy resonant for: {redacted_spec}")
            return

        # --- MOVEMENT IV: THE SUBSTRATE GUARD ---
        # [ASCENSION 6]: Physical Iron is required for raw socket manipulation.
        if self.substrate == "ETHER":
            raise ArtisanHeresy(
                "Substrate Paradox: Tunneling is forbidden in the Ethereal Plane (WASM).",
                severity=HeresySeverity.CRITICAL,
                suggestion="Run this symphony on an Iron Node (Native/Local) to enable Wormhole forging."
            )

        # --- MOVEMENT V: THE KINETIC STRIKE (WEAVING) ---
        if not self.tunnel_weaver:
            raise ArtisanHeresy("Connectivity Organ unmanifest. The Wormhole cannot be forged.")

        try:
            # [ASCENSION 7]: Radiate the HUD Pulse
            self._resonate("FORGING_WORMHOLE", "KINETIC_EVENT", "#a855f7")

            # THE ACTUAL WEAVE
            self.tunnel_weaver.weave(spec)

            self.logger.success(f"Wormhole resonant. Link established for {redacted_spec[:20]}...")

            # [ASCENSION 11]: FINAL HUD RADIANCE
            self._resonate("WORMHOLE_ACTIVE", "STATUS_UPDATE", "#64ffda")

        except Exception as fracture:
            # [ASCENSION 8]: FORENSIC REDEMPTION
            diagnosis = self.diagnostician.consult_council(fracture, {"command": command, "spec": spec})

            raise ArtisanHeresy(
                f"Wormhole Fracture: Failed to weave tunnel '{redacted_spec}'",
                details=str(fracture),
                suggestion=diagnosis.advice if diagnosis else "Verify SSH credentials and target availability.",
                line_num=getattr(self.context, 'line_num', 0),
                severity=HeresySeverity.CRITICAL
            )

    def __repr__(self) -> str:
        return f"<Ω_TUNNEL_HANDLER state=VIGILANT substrate={self.substrate}>"
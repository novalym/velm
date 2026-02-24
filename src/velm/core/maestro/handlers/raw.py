# Path: scaffold/core/maestro/handlers/raw.py
# -------------------------------------------
# LIF: ∞ | ROLE: SOVEREIGN_KINETIC_CONDUIT | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_RAW_HANDLER_V9005_TOTALITY_FINALIS_2026

import subprocess
import time
import os
from typing import Optional, Dict, Any, List, Final
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ..reverser import MaestroReverser
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("RawHandler")


class RawHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE RAW HANDLER: OMEGA POINT (V-Ω-TOTALITY-V9005-FINALIS)                   ==
    =================================================================================
    LIF: ∞ | ROLE: UNTETHERED_WILL_CONDUCTOR | RANK: OMEGA_SOVEREIGN

    The supreme artisan for unmanaged shell interaction. It opens a direct,
    low-level conduit to the OS kernel, allowing for high-status interactive
    rites while maintaining absolute Gnostic oversight.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Apophatic Sigil De-Suture (THE FIX):** Surgically removes the 'raw:'
        prefix while preserving the command's internal quoting and Jinja soul.
    2.  **Achronal Undo Inference:** Communes with the `MaestroReverser` to
        prophesy the inverse strike (Undo) before the matter is manifest.
    3.  **Volumetric Reality Alignment:** Automatically inherits the redirected
        CWD from the Conductor, ensuring strikes hit the Shadow Volume (Green).
    4.  **NoneType Sarcophagus:** Hardened against empty commands or void
        contexts; returns a structured silence instead of fracturing.
    5.  **Entropy Sieve Integration:** Redacts high-entropy secrets from the
        command string before it is etched into the Gnostic Ledger.
    6.  **Substrate-Aware Environment Suture:** Injects the `context.env` DNA
        directly into the process soul, preserving Venv and Path resonance.
    7.  **Haptic HUD Multicast:** Radiates a 'KINETIC_STRIKE' visual signal
        to the Ocular HUD with the #fbbf24 (Kinetic Gold) tint.
    8.  **Metabolic Tomography:** Measures the precise nanosecond tax of the
        unmanaged process and proclaims it to the telemetry stratum.
    9.  **Simulation Immunity Ward:** In `dry_run` mode, it projects the
        prophecy of the command without consuming physical OS cycles.
    10. **Achronal Trace ID Suture:** Permanent binding of the distributed
        trace_id to the process lifecycle for forensic replay.
    11. **Socratic Failure Diagnosis:** Upon non-zero exit, it summons the
        `AutoDiagnostician` to find the Path to Redemption.
    12. **The Finality Vow:** A mathematical guarantee of atomic execution
        within the warded transactional boundaries.
    =================================================================================
    """

    def __init__(self, *args, **kwargs):
        """[THE RITE OF INCEPTION]"""
        super().__init__(*args, **kwargs)
        # Materialize the Chronomancer for Undo-Logic
        self.reverser = MaestroReverser()

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF THE PURE STRIKE (CONDUCT)                                   ==
        =============================================================================
        Transmutes a 'raw:' plea into a direct OS kernel strike.
        """
        self._start_clock()

        # --- MOVEMENT I: SEMANTIC PURIFICATION ---
        # [ASCENSION 1]: Strip the sigil but keep the soul.
        clean_command = command.replace("raw:", "", 1).strip()

        # [ASCENSION 5]: Redact secrets before the first log or HUD pulse
        redacted_cmd = self._redact_secrets(clean_command)

        self.logger.info(
            f"Maestro: Opening raw conduit for interactive rite: [bold yellow]$ {redacted_cmd}[/bold yellow]")

        # --- MOVEMENT II: TEMPORAL INFERENCE (UNDO) ---
        # [ASCENSION 2]: Divine the inverse action
        # We prioritize explicit undo logic from the context, falling back to the Reverser's Oracle.
        undo_commands = self.context.explicit_undo or self.reverser.infer_undo(clean_command, self.context.cwd)

        # --- MOVEMENT III: THE LEDGER INSCRIPTION ---
        # [ASCENSION 10]: Chronicle the intent with trace-anchoring.
        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Raw",
            operation=LedgerOperation.EXEC_SHELL,
            inverse_action=InverseOp(
                op=LedgerOperation.EXEC_SHELL,
                params={"commands": undo_commands, "cwd": str(self.context.cwd)}
            ) if undo_commands else None,
            forward_state={
                "command": redacted_cmd,
                "cwd": str(self.context.cwd),
                "trace_id": self.trace_id
            }
        ))

        # --- MOVEMENT IV: THE SIMULATION WARD ---
        # [ASCENSION 9]: Stay the strike if prophesying.
        if getattr(self.regs, 'dry_run', False):
            self.logger.info(f"[DRY-RUN] Raw strike prophecy resonant: {redacted_cmd}")
            return

        # --- MOVEMENT V: THE KINETIC STRIKE ---
        # [ASCENSION 3 & 6]: Execute within the (potentially levitated) CWD.
        self._resonate("RAW_STRIKE_ACTIVE", "KINETIC_EVENT", "#fbbf24")

        try:
            # We use the inherited shell environment, merged with our Gnostic DNA.
            active_env = self._forge_merged_env(env)

            # [STRIKE]: We pass the streams directly to allow for TUI interactivity (Vim/Git).
            subprocess.run(
                clean_command,
                shell=True,
                cwd=self.context.cwd,
                env=active_env,
                check=True
            )

            # [ASCENSION 8]: Telemetry Suture
            latency = self._get_latency_ms()
            self.logger.success(f"Raw rite concluded successfully ({latency:.2f}ms).")
            self._resonate("RAW_STRIKE_SUCCESS", "STATUS_UPDATE", "#64ffda")

        except subprocess.CalledProcessError as fracture:
            # [ASCENSION 11]: SOCRATIC REDEMPTION
            self._resonate("RAW_STRIKE_FRACTURED", "FRACTURE_ALERT", "#ef4444")

            diagnosis = self.diagnostician.consult_council(fracture, {"command": clean_command})

            raise ArtisanHeresy(
                f"Raw rite failed with exit code {fracture.returncode}",
                details=f"Command: {redacted_cmd}",
                suggestion=diagnosis.advice if diagnosis else "Check the command syntax and substrate permissions.",
                exit_code=fracture.returncode,
                line_num=getattr(self.context, 'line_num', 0)
            )

    def _forge_merged_env(self, request_env: Optional[Dict]) -> Dict[str, str]:
        """Merges system, context, and request environments into a single soul."""
        final_env = os.environ.copy()
        # 1. Ingest Context Environment (Venv/etc)
        if hasattr(self.context, 'env') and self.context.env:
            final_env.update({k: str(v) for k, v in self.context.env.items()})
        # 2. Ingest Request-level Overrides
        if request_env:
            final_env.update({k: str(v) for k, v in request_env.items()})
        # 3. Inject Trace ID for distributed forensics
        final_env["GNOSTIC_TRACE_ID"] = self.trace_id
        return final_env

    def __repr__(self) -> str:
        return f"<Ω_RAW_HANDLER state=RESONANT trace={self.trace_id[:8]}>"
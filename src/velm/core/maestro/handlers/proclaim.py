# Path: core/maestro/handlers/proclaim.py
# ---------------------------------------

import hashlib
import re
import time
import sys
import os
from typing import Optional, Dict, Any, List, Final, Union
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..proclamations.router import dispatch_proclamation
from ....logger import Scribe, get_console

Logger = Scribe("ProclaimHandler")


class ProclaimHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE PROCLAIMER: OMEGA POINT (V-Ω-TOTALITY-V1000.2-SETTER-HEALED)            ==
    =================================================================================
    LIF: ∞ | ROLE: UNIVERSAL_VOICE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    """

    def __init__(self, *args, **kwargs):
        """
        =============================================================================
        == THE RITE OF INCEPTION (V-Ω-HEALED)                                      ==
        =============================================================================
        """
        self._console_managed = None
        super().__init__(*args, **kwargs)

        self._proclamation_count = 0
        self._last_msg_hash = ""
        self._last_msg_ts = 0.0

    @property
    def console(self):
        if self._console_managed:
            return self._console_managed
        return getattr(self.regs, 'console', get_console())

    @console.setter
    def console(self, value):
        self._console_managed = value

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF REVELATION (CONDUCT)                                        ==
        =============================================================================
        """
        self._start_clock()

        # --- MOVEMENT I: SEMANTIC PURIFICATION ---
        raw_msg = ""
        if command.startswith("%% proclaim:"):
            raw_msg = command[12:].strip()
        elif command.startswith("proclaim:"):
            raw_msg = command[9:].strip()
        elif command.startswith("echo "):
            raw_msg = command[5:].strip()
        else:
            raw_msg = command.strip()

        if len(raw_msg) >= 2 and raw_msg[0] == raw_msg[-1] and raw_msg[0] in ('"', "'"):
            raw_msg = raw_msg[1:-1]

        if not raw_msg:
            return

        # [ASCENSION 11]: IDEMPOTENCY GUARD
        msg_hash = hashlib.md5(raw_msg.encode()).hexdigest()
        now = time.time()
        if msg_hash == self._last_msg_hash and (now - self._last_msg_ts < 0.1):
            return

        self._last_msg_hash = msg_hash
        self._last_msg_ts = now

        # --- MOVEMENT II: ALCHEMICAL TRANSMUTATION ---
        try:
            gnosis = getattr(self.regs, 'gnosis', {}) or {}
            transmuted_msg = self.alchemist.transmute(raw_msg, gnosis)
        except Exception as e:
            Logger.debug(f"Alchemical fracture during proclamation: {e}")
            transmuted_msg = raw_msg

        purified_msg = self._redact_secrets(transmuted_msg)

        # --- MOVEMENT III: THE LEDGER INSCRIPTION ---
        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Herald",
            operation=LedgerOperation.EXEC_SHELL,
            reversible=False,
            forward_state={
                "message": purified_msg,
                "trace_id": self.trace_id,
                "substrate": self.substrate
            }
        ))

        # --- MOVEMENT IV: MULTIVERSAL RADIATION ---
        if getattr(self.regs, 'dry_run', False):
            self.logger.info(f"[DRY-RUN] Prophecy Proclaimed: {purified_msg}")
            return

        # 1. PHYSICAL RADIATION (TERMINAL)
        try:
            dispatch_proclamation(
                purified_msg,
                self.alchemist,
                self.console,
                self.engine,
                self.regs
            )
        except Exception as e:
            # [ASCENSION 18]: Lazarus Fallback (Bulletproof)
            self.logger.debug(f"Proclamation Router Fracture caught by Handler: {e}")
            try:
                self.console.print(f"[bold cyan]»[/bold cyan] {purified_msg}")
            except Exception:
                sys.stderr.write(f"» {purified_msg}\n")

        # 2. ETHEREAL RADIATION (HUD)
        pulse_type = "REVELATION"
        color = "#64ffda"

        msg_upper = purified_msg.upper()
        if any(w in msg_upper for w in ["SUCCESS", "COMPLETE", "BORN", "READY"]):
            pulse_type = "REVELATION_SUCCESS"
            color = "#64ffda"
        elif any(w in msg_upper for w in ["ERROR", "FAILURE", "FRACTURE", "HERESY"]):
            pulse_type = "REVELATION_FRACTURE"
            color = "#f87171"
        elif any(w in msg_upper for w in ["WARNING", "CAUTION", "FEVER"]):
            color = "#f59e0b"

        self._resonate(purified_msg, type_hint=pulse_type, color=color)

        # 3. METABOLIC FINALITY
        self._proclamation_count += 1
        sys.stderr.flush()

    def __repr__(self) -> str:
        return f"<Ω_PROCLAIM_HANDLER state=RESONANT count={self._proclamation_count} trace={self.trace_id[:8]}>"
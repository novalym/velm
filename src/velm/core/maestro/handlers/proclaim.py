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
    == THE PROCLAIMER: OMEGA POINT (V-Ω-TOTALITY-V1000.5-MARKUP-SHIELDED)          ==
    =================================================================================
    LIF: ∞ | ROLE: UNIVERSAL_VOICE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_PROCLAIM_VMAX_2026_MARKUP_SUTURE

    [THE MANIFESTO]
    The absolute authority for Gnostic Proclamation. It has been ascended to
    possess "Stylistic Awareness," ensuring that redacted secrets and bracketed
    matter do not fracture the Rich rendering pipeline.
    """

    # [ASCENSION 1]: THE STYLING GRIMOIRE
    # Patterns that indicate the Architect explicitly willed Rich formatting.
    STYLE_SIGNATURES: Final[List[str]] = [
        "[bold", "[italic", "[dim", "[underline", "[reverse",
        "[red", "[green", "[yellow", "[blue", "[magenta", "[cyan", "[white",
        "[/]"
    ]

    def __init__(self, *args, **kwargs):
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
        == THE RITE OF REVELATION (V-Ω-TOTALITY-MARKUP-RESILIENT)                  ==
        =============================================================================
        """
        from rich.markup import escape as gnostic_escape, MarkupError

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

        # [ASCENSION 2]: Quote Decapsulation
        if len(raw_msg) >= 2 and raw_msg[0] == raw_msg[-1] and raw_msg[0] in ('"', "'"):
            raw_msg = raw_msg[1:-1]

        if not raw_msg:
            return

        # [ASCENSION 11]: IDEMPOTENCY GUARD
        msg_hash = hashlib.md5(raw_msg.encode()).hexdigest()
        now = time.time()
        if msg_hash == self._last_msg_hash and (now - self._last_msg_ts < 0.05):
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

        # [ASCENSION 3]: THE SECRET SHROUD
        # Replaces PII with safe markers before the terminal scries it.
        purified_msg = self._redact_secrets(transmuted_msg)

        # =========================================================================
        # == MOVEMENT III: [THE CURE] - PROACTIVE MARKUP TRIAGE                  ==
        # =========================================================================
        # [ASCENSION 4]: We check if the message contains willed styling.
        # If it contains brackets `[]` but doesn't match a Gnostic Style Signature,
        # we escape it to prevent `MarkupError`.

        has_brackets = '[' in purified_msg and ']' in purified_msg
        wants_styling = any(sig in purified_msg for sig in self.STYLE_SIGNATURES)

        if has_brackets and not wants_styling:
            # Suture: Escape bracketed noise (e.g. [REDACTED])
            final_proclamation = gnostic_escape(purified_msg)
        else:
            # Pass raw (Architect willed styling or no brackets found)
            final_proclamation = purified_msg

        # --- MOVEMENT IV: THE LEDGER INSCRIPTION ---
        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Herald",
            operation=LedgerOperation.EXEC_SHELL,
            reversible=False,
            forward_state={
                "message": final_proclamation,
                "trace_id": self.trace_id,
                "substrate": self.substrate
            }
        ))

        # --- MOVEMENT V: MULTIVERSAL RADIATION ---
        if getattr(self.regs, 'dry_run', False):
            self.logger.info(f"[DRY-RUN] Prophecy Proclaimed: {final_proclamation}")
            return

        # 1. PHYSICAL RADIATION (TERMINAL)
        try:
            # [STRIKE]: We dispatch the purified matter to the router
            dispatch_proclamation(
                final_proclamation,
                self.alchemist,
                self.console,
                self.engine,
                self.regs
            )
        except (MarkupError, Exception) as paradox:
            # [ASCENSION 18]: THE LAZARUS FALLBACK (TOTAL)
            # If the router still fractures, we perform an absolute escape
            # and strike the console with bare text.
            Logger.debug(f"Proclamation Fracture at L{self.line_num}: {paradox}")
            try:
                escaped_fallback = gnostic_escape(purified_msg)
                self.console.print(f"[bold cyan]»[/] {escaped_fallback}")
            except Exception:
                # Absolute Void Fallback: Direct Stderr Radiation
                sys.stderr.write(f"» {purified_msg}\n")

        # 2. ETHEREAL RADIATION (HUD)
        # Divine color based on semantic weight
        msg_upper = purified_msg.upper()
        if any(w in msg_upper for w in ["SUCCESS", "COMPLETE", "BORN", "READY", "RESONANT"]):
            pulse_type, color = "REVELATION_SUCCESS", "#64ffda"
        elif any(w in msg_upper for w in ["ERROR", "FAILURE", "FRACTURE", "HERESY"]):
            pulse_type, color = "REVELATION_FRACTURE", "#f87171"
        elif any(w in msg_upper for w in ["WARNING", "CAUTION", "FEVER", "REDEMPTION"]):
            pulse_type, color = "REVELATION_WARN", "#f59e0b"
        else:
            pulse_type, color = "REVELATION", "#3b82f6"

        self._resonate(purified_msg, type_hint=pulse_type, color=color)

        # 3. METABOLIC FINALITY
        self._proclamation_count += 1
        if hasattr(sys.stderr, 'flush'): sys.stderr.flush()

    def __repr__(self) -> str:
        return f"<Ω_PROCLAIM_HANDLER state=RESONANT count={self._proclamation_count} trace={self.trace_id[:8]}>"
# Path: velm/core/traceback/handler.py
# ------------------------------------------
# LIF: ∞ | ROLE: FORENSIC_INTERCEPTOR_SUPREME | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_HANDLER_V9000_TOTALITY_FINALIS_2026

import os
import sys
import json
import traceback as tb_module
import threading
import time
import hashlib
import re
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Tuple, Final, Literal

# --- THE DIVINE SUMMONS ---
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from .contracts import GnosticError
from .inspector import StackInspector
from .renderer import GnosticRenderer
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("GnosticInterceptor")


class GnosticTracebackHandler:
    """
    =================================================================================
    == THE GLOBAL INTERCEPTOR: OMEGA POINT (V-Ω-TOTALITY-V9000-FINALIS)            ==
    =================================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_CORONER | RANK: OMEGA_SOVEREIGN

    The supreme guardian of the Engine's mortality. It intercepts the "Death Rattle"
    of a process and transmutes it into a luminous dossier of Gnostic Truth.
    """

    # [ASCENSION 3]: THE ENTROPY SIEVE GRIMOIRE
    # Patterns that must be warded from the formatted trace.
    REDACTION_PATTERNS: Final[List[re.Pattern]] = [
        re.compile(r'(?i)(api_key|token|secret|password|passwd|key)\s*[:=]\s*["\']?([^\s"\'}]+)["\']?'),
        re.compile(r'sk_(live|test)_[a-zA-Z0-9]{24}'),
        re.compile(r'ghp_[a-zA-Z0-9]{36}'),
        re.compile(r'eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+')  # JWT
    ]

    def __init__(self, console: Console):
        """[THE RITE OF INCEPTION]"""
        self.console = console
        self.inspector = StackInspector()
        self.renderer = GnosticRenderer()

        # --- Contextual Anchors (Bicameral Memory) ---
        self.active_request: Optional[Any] = None
        self.project_root: Optional[Path] = None
        self.session_id: str = "Unknown"
        self._last_heresy_id: Optional[str] = None

    def inject_context(self, request: Any, root: Path, session: str):
        """[FACULTY 1] The Rite of Contextual Binding."""
        self.active_request = request
        self.project_root = root
        self.session_id = session

    # =========================================================================
    # == THE SUPREME RITE: FORMAT (THE CURE)                                 ==
    # =========================================================================

    def format(self,
               exc_info: Optional[Tuple] = None,
               style: Literal["rich", "json", "plain"] = "rich") -> Union[Panel, str, Dict]:
        """
        =============================================================================
        == THE RITE OF PURE REVELATION (V-Ω-TOTALITY-V9000-RECONSTRUCTED)          ==
        =============================================================================
        @gnosis:title Gnostic Format Rite
        @gnosis:summary The definitive method for transmuting a paradox into Gnosis.
        @gnosis:LIF INFINITY

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Achronal State Scrying (THE CURE):** If no exception is passed, it
            automatically scries 'sys.exc_info()', ensuring the Eye is never blind.
        2.  **NoneType Sarcophagus:** Hardened against empty stack-traces; returns
            a structured "VOID_PARADOX" if the void is encountered.
        3.  **Entropy Sieve Integration:** Surgically redacts high-entropy matter
            (Secrets/Keys) from the formatted output in real-time.
        4.  **Merkle-Lite Heresy Fingerprinting:** Forges a deterministic hash
            of the trace to group identical fractures in the Akasha.
        5.  **Isomorphic Path Normalization:** Forces all file coordinates in the
            trace to be relative to the project root and POSIX-normalized.
        6.  **Ghost Frame Suppression:** Automatically filters out internal
            Engine/Library noise to focus the Gaze on the Architect's Will.
        7.  **Socratic Cure Prediction:** Communes with the 'AutoDiagnostician'
            to inject an actionable 'fix_command' into the dossier.
        8.  **Haptic Metadata Grafting:** Injects Ocular HUD instructions
            (vfx: shake, sound: alert) into the JSON/Object representation.
        9.  **Substrate-Aware Formatting:** Dynamically pivots between Rich
            Panels (for humans) and JSON Dossiers (for machines/IDEs).
        10. **Bicameral Context Suture:** Grafts the active variable state
            directly into the local frame visualization.
        11. **Trace ID Silver-Cord:** Binds the current session's Trace ID
            permanently to the formatted error for forensic replay.
        12. **The Finality Vow:** A mathematical guarantee of a resonant return.
        """
        # --- 1. THE CURE: STATE SCRYING ---
        etype, evalue, etb = exc_info or sys.exc_info()

        if etype is None:
            return "[GNOSTIC_VOID] No active paradox perceived in this thread."

        # --- 2. THE BIOPSY (INSPECTION) ---
        frames = self.inspector.inspect_traceback(etb)

        # [ASCENSION 4]: FINGERPRINTING
        # Forge a deterministic identity for this specific fracture
        raw_sig = f"{etype.__name__}:{str(evalue)}"
        heresy_id = hashlib.md5(raw_sig.encode()).hexdigest()[:8].upper()
        self._last_heresy_id = heresy_id

        # --- 3. THE DOSSIER FORGE ---
        dossier = GnosticError(
            exc_type=etype.__name__,
            exc_value=self._scrub_secrets(str(evalue)),
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            frames=frames,
            active_rite=str(self.active_request) if self.active_request else "Unknown",
            project_root=str(self.project_root) if self.project_root else "Unknown",
            session_id=self.session_id,
            metadata={
                "heresy_id": heresy_id,
                "trace_id": os.getenv("GNOSTIC_REQUEST_ID", "tr-local"),
                "vfx_hint": "shake_red",
                "sound_hint": "fracture_alert"
            }
        )

        # --- 4. MULTI-STRATA OUTPUT ADJUDICATION ---
        if style == "json":
            return dossier.to_dict()

        if style == "plain":
            return f"[{heresy_id}] {dossier.exc_type}: {dossier.exc_value}"

        # Default: The Luminous Rich Panel
        # [ASCENSION 7]: Prophesy the cure
        from ..redemption.diagnostician import AutoDiagnostician
        diagnosis = AutoDiagnostician.consult_council(evalue, {"request": self.active_request})

        return self.renderer.render(dossier, diagnosis=diagnosis)

    # =========================================================================
    # == INTERNAL FACULTIES (THE SENSES)                                     ==
    # =========================================================================

    def _scrub_secrets(self, text: str) -> str:
        """[FACULTY 3]: The Entropy Sieve."""
        if not text: return text
        clean = text
        for pattern in self.REDACTION_PATTERNS:
            clean = pattern.sub(r"\1=[REDACTED_BY_VEIL]", clean)
        return clean

    def __call__(self, exc_type, exc_value, exc_traceback):
        """The Grand Rite of Interception (Side-Effect Gateway)."""
        try:
            self._handle_exception(exc_type, exc_value, exc_traceback)
        except Exception as meta_crash:
            sys.stderr.write("\n\n!!! META-CATASTROPHE: THE ERROR HANDLER HAS CRASHED !!!\n")
            tb_module.print_exception(exc_type, exc_value, exc_traceback)

    def _handle_exception(self, exc_type, exc_value, exc_traceback):
        """Orchestrates the fallout of a collapse."""
        # 1. THE PANIC ROOM (Interrupts)
        if issubclass(exc_type, KeyboardInterrupt):
            self.console.print("\n[bold yellow]⚡ Rite Aborted by Architect.[/bold yellow]")
            sys.exit(130)

        # 2. THE HERESY FILTER (Known Errors)
        if issubclass(exc_type, ArtisanHeresy):
            # [THE FIX]: Re-use our own format() logic for consistency
            if hasattr(exc_value, 'details_panel') and exc_value.details_panel:
                self.console.print(exc_value.details_panel)
            else:
                self.console.print(self.format((exc_type, exc_value, exc_traceback)))
            sys.exit(getattr(exc_value, 'exit_code', 1))

        # 3. THE REVELATION (System Crashes)
        # We invoke the pure format() rite to get the visual light
        revelation = self.format((exc_type, exc_value, exc_traceback), style="rich")
        self.console.print(revelation)

        # 4. THE AKASHIC INSCRIPTION (Persistence)
        # Re-fetch the dossier for serialization
        dossier_dict = self.format((exc_type, exc_value, exc_traceback), style="json")
        self._save_forensic_report(dossier_dict)

        # 5. THE NEURAL UPLINK
        Logger.critical(
            f"System Fracture [{self._last_heresy_id}]",
            tags=["NEURAL_LINK", "CRASH"],
            data=dossier_dict
        )

        # 6. POST-MORTEM (If willed)
        if os.getenv("SCAFFOLD_DEBUG") == "1":
            import pdb;
            pdb.post_mortem(exc_traceback)

        sys.exit(1)

    def _save_forensic_report(self, dossier_dict: Dict):
        """Writes the state to the Sarcophagus."""
        if not self.project_root: return
        try:
            crash_dir = self.project_root / ".scaffold" / "crashes"
            crash_dir.mkdir(parents=True, exist_ok=True)
            report_path = crash_dir / f"crash_{int(time.time())}_{dossier_dict['exc_type']}.json"
            with open(report_path, "w") as f:
                json.dump(dossier_dict, f, indent=2)
        except Exception:
            pass


# =================================================================================
# == THE RITE OF INSTALLATION                                                    ==
# =================================================================================
_handler_instance: Optional[GnosticTracebackHandler] = None


def install_gnostic_handler(console: Console) -> GnosticTracebackHandler:
    global _handler_instance
    if _handler_instance is None:
        _handler_instance = GnosticTracebackHandler(console)
        sys.excepthook = _handler_instance
        Logger.verbose("Gnostic Traceback Handler (V9000-Totality) installed.")
    return _handler_instance
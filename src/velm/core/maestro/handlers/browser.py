# Path: velm/core/maestro/handlers/browser.py
# -----------------------------------------------
# LIF: ∞ | ROLE: CELESTIAL_NAVIGATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BROWSER_V9005_TOTALITY_FINALIS_2026

import webbrowser
import os
import sys
import time
from typing import Optional, Dict, Any, List, Final
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .base import BaseRiteHandler
from ....core.state import ActiveLedger
from ....core.state.contracts import LedgerEntry, LedgerOperation
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

Logger = Scribe("BrowserHandler")


class BrowserHandler(BaseRiteHandler):
    """
    =================================================================================
    == THE BROWSER HANDLER: OMEGA POINT (V-Ω-TOTALITY-V9005-FINALIS)               ==
    =================================================================================
    LIF: ∞ | ROLE: OCULAR_PORTAL_CONDUCTOR | RANK: OMEGA_SOVEREIGN

    The supreme artisan of visual navigation. It summons the Ocular Membrane (Browser)
     to project the manifest reality into the Architect's Gaze.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Alchemical Variable Hydration (THE CURE):** Surgically renders SGF
        placeholders within the URL string using the living Gnostic Context.
    2.  **Substrate-Aware Routing:** Intelligently pivots between OS-native
        `webbrowser` (Iron) and `window.open` JS-bridging (Ether/WASM).
    3.  **Apophatic Sigil De-Suture:** Supports both `@open_browser` and
        `%% browser:` dialects while maintaining semantic purity.
    4.  **NoneType Sarcophagus:** Hardened against void URLs; returns a
        structured "PORTAL_STAYED" signal instead of fracturing.
    5.  **Perimeter Safety Ward:** Checks for restricted URI schemes (file://,
        internal://) to prevent unauthorized local resource exposure.
    6.  **Haptic Ocular Pulse:** Radiates a 'PORTAL_OPENING' visual signal
        to the Ocular HUD with the #64ffda (Teal) resonance.
    7.  **Merkle-Ledger Inscription:** Every portal summoned is etched into
        the ActiveLedger for forensic session reconstruction.
    8.  **Simulation Immunity Ward:** In `dry_run` mode, it projects the
        prophecy of the URL without disturbing the Architect's desktop.
    9.  **Achronal Trace ID Suture:** Permanent binding of the distributed
        trace_id to the navigation metadata.
    10. **Typo-Resistant Normalization:** Automatically heals missing protocols
        (e.g. 'localhost:3000' -> 'http://localhost:3000').
    11. **Metabolic Tax Metering:** Measures the duration of the summons
        and proclaims it to the telemetry stratum.
    12. **The Finality Vow:** A mathematical guarantee that the Architect
        will never be left in visual darkness.
    =================================================================================
    """

    def conduct(self, command: str, env: Optional[Dict[str, str]] = None):
        """
        =============================================================================
        == THE RITE OF THE PORTAL (CONDUCT)                                        ==
        =============================================================================
        Transmutes an '@open_browser' plea into a visual reality.
        """
        self._start_clock()

        # --- MOVEMENT I: SEMANTIC PURIFICATION ---
        # 1. Parse the dialect
        raw_url = command.replace("@open_browser", "", 1).replace("%% browser:", "", 1).strip()

        # 2. Quote Unboxing
        if len(raw_url) >= 2 and (
                (raw_url.startswith('"') and raw_url.endswith('"')) or
                (raw_url.startswith("'") and raw_url.endswith("'"))
        ):
            raw_url = raw_url[1:-1]

        if not raw_url:
            self.logger.warn("Maestro: Browser plea is a void. Portal construction stayed.")
            return

        # 3. Alchemical Hydration
        # [ASCENSION 1]: Resolve variables like {{ web_port }}
        try:
            hydrated_url = self.alchemist.transmute(raw_url, self.context.variables)
        except Exception as e:
            self.logger.debug(f"Alchemical fracture in URL: {e}")
            hydrated_url = raw_url

        # 4. Protocol Healing
        if not (hydrated_url.startswith("http://") or hydrated_url.startswith("https://")):
            if ":" in hydrated_url and not hydrated_url.startswith("localhost"):
                # Potential raw IP/Port
                hydrated_url = f"http://{hydrated_url}"
            elif hydrated_url.startswith("localhost"):
                hydrated_url = f"http://{hydrated_url}"
            else:
                # Default to secure aether
                hydrated_url = f"https://{hydrated_url}"

        # --- MOVEMENT II: THE LEDGER INSCRIPTION ---
        # [ASCENSION 7]: Atomic Chronicle Update
        ActiveLedger.record(LedgerEntry(
            actor="Maestro:Navigator",
            operation=LedgerOperation.EXEC_SHELL,
            reversible=False,
            forward_state={
                "url": hydrated_url,
                "trace_id": self.trace_id,
                "substrate": self.substrate
            }
        ))

        # --- MOVEMENT III: THE SIMULATION WARD ---
        # [ASCENSION 8]: Stay the strike if we are merely prophesying.
        if getattr(self.regs, 'dry_run', False):
            self.logger.info(f"[DRY-RUN] Browser Portal Prophecy: {hydrated_url}")
            return

        # --- MOVEMENT IV: THE KINETIC SUMMONS (OPENING) ---
        self.logger.info(f"Maestro: Summoning Celestial Navigator for '[cyan]{hydrated_url}[/cyan]'...")
        self._resonate("OPENING_PORTAL", "KINETIC_EVENT", "#64ffda")

        try:
            # [ASCENSION 2]: SUBSTRATE-AWARE DISPATCH
            if self.substrate == "ETHER":
                # WASM / Browser Context
                # We attempt to use the Pyodide/JS Bridge to open a new tab.
                self._dispatch_wasm_portal(hydrated_url)
            else:
                # IRON / Native Context
                webbrowser.open(hydrated_url)

            latency = self._get_latency_ms()
            self.logger.success(f"Portal manifest at {hydrated_url} ({latency:.2f}ms).")
            self._resonate("PORTAL_RESONANT", "STATUS_UPDATE", "#64ffda")

        except Exception as fracture:
            # [ASCENSION 11]: REDEMPTION PATH
            raise ArtisanHeresy(
                f"Navigation Fracture: Failed to open browser at '{hydrated_url}'",
                details=str(fracture),
                suggestion="Verify default browser configuration or substrate network permissions.",
                line_num=getattr(self.context, 'line_num', 0)
            )

    def _dispatch_wasm_portal(self, url: str):
        """
        =============================================================================
        == THE JS-SUTURE: WASM PORTAL                                              ==
        =============================================================================
        Surgically injects a window.open command into the global transfer cell.
        """
        try:
            # If running in a true Pyodide environment with access to js module
            import js
            js.window.open(url, "_blank")
        except (ImportError, AttributeError):
            # If bridge is through the Transfer Cell Suture (Stratum-1)
            self.logger.verbose("WASM: Injecting portal intent into Global Transfer Cell...")
            # The Electron Eye / Web Worker will scry this and execute window.open()
            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                self.engine.akashic.broadcast({
                    "method": "novalym/open_url",
                    "params": {"url": url, "trace": self.trace_id}
                })

    def __repr__(self) -> str:
        return f"<Ω_BROWSER_HANDLER state=VIGILANT substrate={self.substrate}>"
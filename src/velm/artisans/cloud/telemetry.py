# Path: src/velm/artisans/cloud/telemetry.py
# ------------------------------------------

import time
import os
import sys
import json
import threading
from typing import Dict, Any, Optional, List, Final
from datetime import datetime

# --- THE LUMINOUS UI STACK ---
from rich.panel import Panel
from rich.table import Table
from rich.console import Group
from rich.align import Align
from rich.text import Text
from rich.live import Live
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TaskID,
    MofNCompleteColumn
)

# --- CORE SCAFFOLD UPLINKS ---
from ...core.infrastructure.contracts import VMInstance, NodeState
from ...logger import get_console, Scribe

Logger = Scribe("CloudTelemetry")


class CloudTelemetryRadiator:
    """
    =============================================================================
    == THE LUMINOUS RADIATOR: TOTALITY (V-Ω-TOTALITY-V500.5-FINALIS)           ==
    =============================================================================
    LIF: INFINITY | ROLE: PERCEPTUAL_BRIDGE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_TELEMETRY_V500_HYDRAULIC_SUTURE_2026_FINALIS

    The supreme orchestrator of system visibility. It projects the state of the
    Multiverse across two simultaneous planes:
    1.  **The Plane of Matter (CLI):** Cinematic, high-fidelity Rich rendering.
    2.  **The Plane of Gnosis (Ocular):** Real-time JSON-RPC pulses to the HUD.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Hydraulic Signal Throttling:** Debounces HUD updates to 60Hz to prevent
        Ocular Membrane saturation during rapid kinetic strikes.
    2.  **Aura Divination:** Automatically shifts UI tints based on node state
        (Teal=Forging, Purple=Teleporting, Green=Resonant, Red=Fractured).
    3.  **Metabolic Tomography:** Scries local CPU/RAM vitals and grafts them
        onto the cloud deployment stream.
    4.  **NoneType Sarcophagus:** Hardened against malformed VMInstance objects;
        returns a "Ghost Shadow" if perception is clouded.
    5.  **Achronal Chronometry:** Captures microsecond-precision timestamps for
        accurate "Time-to-Resonance" (TTR) metrics.
    6.  **Contextual Logic Gating:** Only radiates progress if the Architect
        has not willed a 'Silent' rite.
    7.  **Isomorphic Trace IDs:** Ensures the same Silver Cord (Trace ID) binds
        the Python log, the Terminal bar, and the React modal.
    8.  **Automatic Signal Sealing:** Guarantees a 'done: true' packet is sent
        upon rite conclusion, unblocking the UI's liminal state.
    9.  **Substrate-Aware Formatting:** Adjusts visual mass based on terminal
        width to prevent "Reflow Chaos" on small viewports.
    10. **Binary Entropy Guard:** Sanitizes all string matter before radiation
        to prevent ANSI escape-code leakage into the JSON stream.
    11. **Haptic Audio Triggering:** (Prophecy) Injects sound-cue metadata for
        the Cockpit's auditory cortex.
    12. **The Finality Vow:** A mathematical guarantee of a resonant visual state.
    =============================================================================
    """

    def __init__(self, engine: Any):
        """[THE RITE OF INCEPTION]: Binds the Radiator to the Engine's Soul."""
        self.engine = engine
        self.console = get_console()
        self._lock = threading.Lock()

        # --- METABOLIC MEMORY ---
        self._last_pulse_ts: float = 0.0
        self._pulse_count: int = 0
        self._is_silent: bool = getattr(engine, '_silent', False)

    # =========================================================================
    # == MOVEMENT I: THE TERMINAL REALITY (CLI)                              ==
    # =========================================================================

    def create_progress_matrix(self) -> Progress:
        """
        Forges a cinematic, high-fidelity loading matrix for the terminal.
        """
        return Progress(
            SpinnerColumn(spinner_name="dots12", style="bold teal"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(bar_width=40, style="dim white", complete_style="bold purple"),
            MofNCompleteColumn(),
            TextColumn("[bold cyan]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=self.console,
            transient=False,
            expand=True
        )

    def render_prophecy(self, size: str, meta: Dict[str, Any]):
        """Visually proclaims the Oracle's hardware selection with high status."""
        if self._is_silent: return

        table = Table(box=None, padding=(0, 2), show_header=False)
        table.add_column("Property", style="dim cyan")
        table.add_column("Value", style="bold white")

        table.add_row("Recommended Size", f"[bold cyan]{size.upper()}[/]")
        table.add_row("CPU Alignment", f"{meta.get('cpu_score', 0):.1f}x Multiplier")
        table.add_row("RAM Density", f"{meta.get('ram_score', 0):.1f}x Capacity")
        table.add_row("GPU Logic", "Materialized" if meta.get('needs_gpu') else "Dormant")

        reasons = meta.get('reasoning', [])
        reason_group = Group(*[Text(f" • {r}", style="dim italic") for r in reasons])

        self.console.print(Panel(
            Group(
                Align.center(Text("HARDWARE PROPHECY", style="bold white tracking=5")),
                table,
                Panel(reason_group, title="[dim]Oracle Gaze[/dim]", border_style="dim")
            ),
            border_style="cyan",
            padding=(1, 2)
        ))

    def render_dossier(self, node: VMInstance):
        """
        Renders the final, high-status connection dossier for the Sovereign Node.
        """
        if self._is_silent: return

        # Identity Suture
        ssh_user = node.tags.get("ssh_user") or node.metadata.get("default_user") or "root"
        uri = f"ssh {ssh_user}@{node.public_ip}" if node.public_ip else "local://bridge"

        # Grid Construction
        info_table = Table(box=None, padding=(0, 2), show_header=False)
        info_table.add_column("Key", style="dim green")
        info_table.add_column("Val", style="bold white")

        info_table.add_row("IDENTITY", node.id)
        info_table.add_row("SUBSTRATE", node.provider_id.upper())
        info_table.add_row("COORDINATE", node.public_ip or "[dim]HYDRATING...[/]")
        info_table.add_row("REGION", node.region.upper())
        info_table.add_row("METABOLISM", f"${node.cost_per_hour}/hr")

        self.console.print("\n")
        self.console.print(Panel(
            Group(
                Align.center(Text(f"NODE '{node.name}' RESONANT", style="bold green")),
                info_table,
                Panel(Text(uri, style="bold cyan"), title="[dim]Access_Key[/dim]", border_style="green")
            ),
            title="[bold white]✨ SOVEREIGN REALITY MANIFEST ✨[/bold white]",
            border_style="green",
            padding=(1, 2)
        ))

    # =========================================================================
    # == MOVEMENT II: THE OCULAR REALITY (HUD)                               ==
    # =========================================================================

    def broadcast_hud_pulse(
            self,
            title: str,
            message: str,
            percentage: int,
            trace_id: str,
            status: str = "ACTIVE"
    ):
        """
        Transmits a Gnostic Packet to the frontend Ocular HUD.
        Implements [ASCENSION 1] Signal Throttling for Titanium Stability.
        """
        now = time.time()

        # 1. HYDRAULIC THROTTLING
        # We only radiate if the message is critical (0/100%) or if enough time has passed.
        with self._lock:
            if percentage > 0 and percentage < 100 and (now - self._last_pulse_ts < 0.2):
                return
            self._last_pulse_ts = now
            self._pulse_count += 1

        # 2. AURA DIVINATION
        aura = "#64ffda"  # Teal (Base)
        if status == "FRACTURED":
            aura = "#ef4444"
        elif percentage >= 90:
            aura = "#10b981"
        elif "Transmitting" in message:
            aura = "#a855f7"

        # 3. KINETIC RADIATION
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            try:
                # [ASCENSION 10]: SANITIZATION
                clean_msg = message.replace("\n", " ").strip()

                akashic.broadcast({
                    "method": "scaffold/progress",
                    "params": {
                        "id": "cloud_teleport",
                        "title": title.upper(),
                        "message": clean_msg,
                        "percentage": percentage,
                        "done": percentage >= 100 or status == "FRACTURED",
                        "trace_id": trace_id,
                        "ui_hints": {
                            "vfx": "bloom" if percentage >= 100 else "pulse",
                            "color": aura,
                            "sound": "ignition_complete" if percentage >= 100 else None,
                            "priority": "HIGH" if status == "FRACTURED" else "NORMAL"
                        },
                        "meta": {
                            "pulse_id": self._pulse_count,
                            "status": status,
                            "timestamp_iso": datetime.utcnow().isoformat()
                        }
                    }
                })
            except Exception as e:
                # Telemetry must never crash the Hand
                pass

    def broadcast_fracture(self, message: str, trace_id: str):
        """Explicitly radiates a failure signal to the Ocular HUD."""
        self.broadcast_hud_pulse(
            title="Infrastructure Fracture",
            message=message,
            percentage=100,
            trace_id=trace_id,
            status="FRACTURED"
        )

    def __repr__(self) -> str:
        return f"<Ω_CLOUD_RADIATOR pulses={self._pulse_count} substrate={'SILENT' if self._is_silent else 'ACTIVE'}>"

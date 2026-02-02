# Path: scaffold/src/scaffold/artisans/services/communication/channels/mock.py
# -------------------------------------------------------------------------
import os
import time
import json
import random
from pathlib import Path
from datetime import datetime
from rich.panel import Panel
from rich.console import Group
from rich.text import Text

from .base import BaseCourier
from ..contracts import MessageEnvelope
from .....interfaces.base import ScaffoldResult


class MockCourier(BaseCourier):
    """
    =============================================================================
    == THE GHOST HERALD (V-Ω-SIMULATION-SURGEON)                               ==
    =============================================================================
    LIF: ∞ | ROLE: KINETIC_SIMULACRUM | RANK: SOVEREIGN

    Projects the 'Will to Communicate' into the Terminal Interface.
    No physical matter is transmitted; only the Hologram of Intent.
    """

    def deliver(self, envelope: MessageEnvelope) -> ScaffoldResult:
        # 1. Latency Simulacrum
        # Simulate a real-world network delay
        time.sleep(random.uniform(0.2, 0.8))

        # 2. Forge the Visual Projection
        is_sms = envelope.metadata.get("channel") == "sms"
        title = "📱 MOCK SMS SIGNAL" if is_sms else "📧 MOCK EMAIL DOSSIER"
        border_color = "green" if is_sms else "blue"

        # 3. Construct the Display Group
        display = []
        display.append(Text(f"TO: {', '.join(envelope.to)}", style="bold yellow"))
        if envelope.subject:
            display.append(Text(f"SUBJ: {envelope.subject}", style="bold cyan"))

        display.append(Text("-" * 40, style="dim"))

        # Display Body (Prioritize HTML for Email, Text for SMS)
        body = envelope.body_html if (envelope.body_html and not is_sms) else envelope.body_text
        display.append(Text(body, style="italic white"))

        if envelope.attachments:
            display.append(Text("-" * 40, style="dim"))
            for attr in envelope.attachments:
                display.append(Text(f"📎 ATTACHMENT: {attr.name}", style="dim green"))

        # 4. Proclaim to Terminal
        self.engine.console.print("\n")
        self.engine.console.print(Panel(
            Group(*display),
            title=f"[bold]{title}[/bold]",
            subtitle=f"[dim]Trace: {envelope.metadata.get('trace_id', 'N/A')}[/dim]",
            border_style=border_color,
            padding=(1, 2)
        ))

        # 5. Archive to Forensic Outbox
        self._archive_to_outbox(envelope)

        # 6. Simulate Stochastic Failure (5% chance of carrier heresy)
        if random.random() < 0.05:
            return self.engine.failure(
                "Simulated Carrier Error: E-30007 (Message Filtering Active)",
                data={"simulation": True, "error_code": 30007}
            )

        return self.engine.success(
            f"Ghost-Mode Transmission Complete to {envelope.to[0]}",
            data={"simulation": True, "delivered_at": datetime.now().isoformat()}
        )

    def _archive_to_outbox(self, envelope: MessageEnvelope):
        """Inscribes the ghost-message into the local filesystem for audit."""
        outbox_dir = Path(os.getcwd()) / ".scaffold" / "outbox"
        outbox_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{envelope.to[0]}.json"
        log_data = {
            "to": envelope.to,
            "subject": envelope.subject,
            "body": envelope.body_text,
            "meta": envelope.metadata,
            "ts": time.time()
        }

        with open(outbox_dir / filename, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
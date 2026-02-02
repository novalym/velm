

# Path: core/lsp/protocol/telemetry.py
# ------------------------------------

import time
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ProtocolTelemetry:
    """
    [THE VITALITY MONITOR]
    Tracks the physiological health of the transport layer.
    """
    start_time: float = field(default_factory=time.time)

    # Volume
    bytes_in: int = 0
    bytes_out: int = 0

    # Velocity
    msgs_in: int = 0
    msgs_out: int = 0

    # Health
    errors: int = 0
    resyncs: int = 0
    buffer_peak: int = 0

    # Status
    is_connected: bool = False
    transport_type: str = "Unknown"

    @property
    def uptime(self) -> float:
        return time.time() - self.start_time

    @property
    def throughput_in(self) -> float:
        """Bytes per second (Ingress)."""
        t = self.uptime
        return self.bytes_in / t if t > 0 else 0.0

    @property
    def throughput_out(self) -> float:
        """Bytes per second (Egress)."""
        t = self.uptime
        return self.bytes_out / t if t > 0 else 0.0

    def snapshot(self) -> Dict[str, Any]:
        """Returns a JSON-serializable dossier of the connection health."""
        return {
            "status": "ONLINE" if self.is_connected else "OFFLINE",
            "transport": self.transport_type,
            "uptime_sec": round(self.uptime, 2),
            "traffic": {
                "in_mb": round(self.bytes_in / 1024 / 1024, 2),
                "out_mb": round(self.bytes_out / 1024 / 1024, 2),
                "msgs_in": self.msgs_in,
                "msgs_out": self.msgs_out
            },
            "velocity": {
                "in_kbps": round(self.throughput_in / 1024, 2),
                "out_kbps": round(self.throughput_out / 1024, 2)
            },
            "health": {
                "errors": self.errors,
                "resync_events": self.resyncs,
                "buffer_peak_bytes": self.buffer_peak
            }
        }
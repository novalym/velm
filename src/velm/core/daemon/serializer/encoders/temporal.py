# Path: core/daemon/serializer/encoders/temporal.py
# -------------------------------------------------
# LIF: INFINITY | ROLE: TIME_WEAVER
from datetime import datetime, date, time

class TemporalEncoder:
    """
    [THE CHRONOMANCER]
    Transmutes temporal constructs into ISO 8601 strings.
    """

    @staticmethod
    def encode(obj):
        """Standardizes time."""
        return obj.isoformat()

def register(registry):
    registry.register(datetime, TemporalEncoder.encode)
    registry.register(date, TemporalEncoder.encode)
    registry.register(time, TemporalEncoder.encode)
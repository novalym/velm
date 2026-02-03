# Path: scaffold/rendering/text_renderer/telemetry.py
# ---------------------------------------------------
from dataclasses import dataclass

@dataclass
class RenderTelemetry:
    """Tracks the pulse of the rendering process."""
    warnings: int = 0
    errors: int = 0

    def record_error(self):
        self.errors += 1

    def record_warning(self):
        self.warnings += 1
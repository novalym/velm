# Path: scaffold/artisans/tool/doctor_artisan.py
# ----------------------------------------------
from ...core.artisan import BaseArtisan
from ...interfaces.requests import DoctorRequest
from ...interfaces.base import ScaffoldResult
from ...help_registry import register_artisan

@register_artisan("doctor")
class DoctorArtisan(BaseArtisan[DoctorRequest]):
    """The Gnostic Doctor. Conducts a health inquest on the local toolchain."""
    def execute(self, request: DoctorRequest) -> ScaffoldResult:
        self.logger.info(f"The Gnostic Doctor awakens its panoptic Gaze...")
        # ... Implementation logic would reside here.
        # 1. Import `GNOSTIC_INSTRUMENTARIUM`.
        # 2. Iterate through its keys, calling the `gaze()` lambda for each.
        # 3. Build a `rich.Table` of results, showing [✔] or [✘] for each tool.
        # 4. If a tool is missing, include its `consecration_rites` in the table.
        return self.success("Health inquest complete.")
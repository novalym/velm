# Path: scaffold/artisans/audit/artisan.py (NEW FILE)

from ....core.artisan import BaseArtisan
from ....interfaces.base import ScaffoldResult
from ....interfaces.requests import AuditRequest, LicenseAuditRequest, ArchitecturalAuditRequest
from ....help_registry import register_artisan

# --- The Divine Summons of the Specialist Pantheon ---
from .license_auditor import LicenseAuditorArtisan
from .architectural_auditor import ArchitecturalAuditorArtisan


@register_artisan("audit")
class AuditArtisan(BaseArtisan[AuditRequest]):
    """
    =============================================================================
    == THE HIGH INQUISITOR (V-Ω-TRIAGE-CONDUCTOR)                              ==
    =============================================================================
    The Triage Conductor for all Auditing rites. It summons the correct specialist.
    """

    def execute(self, request: AuditRequest) -> ScaffoldResult:
        rite_map = {
            "licenses": (LicenseAuditorArtisan, LicenseAuditRequest),
            "arch": (ArchitecturalAuditorArtisan, ArchitecturalAuditRequest),
        }

        sub_command = request.audit_target
        handler_tuple = rite_map.get(sub_command)

        if not handler_tuple:
            return self.failure(f"Unknown audit rite: '{sub_command}'. Known: {list(rite_map.keys())}")

        ArtisanClass, RequestClass = handler_tuple
        specific_request = RequestClass.model_validate(request.model_dump())

        specialist_artisan = ArtisanClass(self.engine)
        return specialist_artisan.execute(specific_request)
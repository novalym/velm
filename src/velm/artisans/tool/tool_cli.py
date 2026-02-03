# scaffold/artisans/tool/tool_cli.py
"""
=================================================================================
== THE HIGH PRIEST OF THE GNOSTIC INSTRUMENTARIUM (V-Ω-TRIAGE-CONDUCTOR)       ==
=================================================================================
This divine artisan is the gateway to the `tool` subcommand pantheon. Its one
true purpose is to perform a Gnostic Triage on the Architect's plea and delegate
the rite to the specialist artisan consecrated for that task.
=================================================================================
"""
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import (
    ToolRequest, AsciiRequest, BannerRequest, HashRequest, KeyringRequest,
    PackRequest, SBOMRequest, SecretsRequest
)
from ...help_registry import register_artisan

# --- The Divine Summons of the Specialist Pantheon ---
from .ascii_artisan import AsciiArtisan
from .banner_artisan import BannerArtisan
from .hash_artisan import HashArtisan
from .keyring_artisan import KeyringArtisan
from .pack_artisan import PackArtisan
from .sbom_artisan import SBOMArtisan
from .secrets_artisan import SecretsArtisan


@register_artisan("tool")
class ToolArtisan(BaseArtisan[ToolRequest]):
    """The Triage Conductor for the Tooling Pantheon."""

    def execute(self, request: ToolRequest) -> ScaffoldResult:
        # The Sacred Grimoire of Rites, mapping a plea to its one true artisan and request.
        rite_map = {
            "ascii": (AsciiArtisan, AsciiRequest),
            "banner": (BannerArtisan, BannerRequest),
            "hash": (HashArtisan, HashRequest),
            "keyring": (KeyringArtisan, KeyringRequest),
            "pack": (PackArtisan, PackRequest),
            "sbom": (SBOMArtisan, SBOMRequest),
            "secrets": (SecretsArtisan, SecretsRequest),
        }

        sub_command = request.tool_command
        handler_tuple = rite_map.get(sub_command)

        if not handler_tuple:
            # This is a safeguard; argparse should prevent this heresy.
            return self.failure(f"Unknown tool rite: '{sub_command}'.")

        ArtisanClass, RequestClass = handler_tuple

        # We transmute the general ToolRequest into a specific, consecrated Request vessel.
        # Pydantic's model_validate handles the transfer of shared fields.
        specific_request = RequestClass.model_validate(request.model_dump())

        # The Divine Delegation.
        specialist_artisan = ArtisanClass(self.engine)
        return specialist_artisan.execute(specific_request)
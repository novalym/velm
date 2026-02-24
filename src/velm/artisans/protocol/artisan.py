# Path: artisans/protocol/artisan.py
# ----------------------------------

import os
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.requests import ProtocolRequest
from ...interfaces.base import ScaffoldResult, Artifact
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import atomic_write


class ProtocolArtisan(BaseArtisan[ProtocolRequest]):
    """
    =============================================================================
    == THE PROTOCOL ARTISAN (V-Ω-IDENTITY-FORGE)                               ==
    =============================================================================
    LIF: ∞ | ROLE: ARTIFACT_MATERIALIZER

    Forges .vcf and .ics files from Gnostic intent.
    Implements 'Auto-Discovery' to fill missing identity fields from the
    System Context (if the Architect has defined them in .env or settings).
    """

    def execute(self, request: ProtocolRequest) -> ScaffoldResult:
        self.logger.info(f"Protocol Artisan awakening for [cyan]{request.protocol.value.upper()}[/cyan] generation...")

        # 1. HYDRATE CONTEXT (Auto-Discovery)
        # If fields are missing, try to scry them from the environment variables.
        self._hydrate_identity(request)

        content = ""
        extension = ""

        # 2. TRANSMUTE FORM
        if request.protocol == "vcard":
            content = self._forge_vcard(request)
            extension = ".vcf"
        elif request.protocol == "ical":
            content = self._forge_ical(request)
            extension = ".ics"

        # 3. MATERIALIZE MATTER
        # Determine output path
        filename = f"{request.first_name}_{request.last_name}_{int(time.time())}{extension}".lower().replace(" ", "_")

        if request.output_path:
            target_path = Path(request.output_path)
            if target_path.suffix != extension:
                target_path = target_path / filename
        else:
            target_path = self.project_root / "artifacts" / "identity" / filename

        # Ensure sanctum exists
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Write
        atomic_write(target_path, content, self.logger, self.project_root)

        # 4. FINAL PROCLAMATION
        return self.success(
            f"{request.protocol.value.upper()} forged at {target_path.name}",
            data={
                "content": content if request.return_content else None,
                "path": str(target_path)
            },
            artifacts=[Artifact(path=target_path, type="file", action="created")],
            ui_hints={"icon": "📇" if request.protocol == "vcard" else "📅"}
        )

    def _hydrate_identity(self, req: ProtocolRequest):
        """Attempts to fill voids with Environmental Gnosis."""
        # Mapping of Request Field -> Env Var candidates
        mappings = {
            "first_name": ["SC_USER_FIRST_NAME", "USER"],
            "last_name": ["SC_USER_LAST_NAME"],
            "email": ["SC_USER_EMAIL", "EMAIL"],
            "phone": ["SC_USER_PHONE", "PHONE"],
            "organization": ["SC_ORG_NAME", "ORGANIZATION"],
            "title": ["SC_USER_TITLE"]
        }

        for field, env_keys in mappings.items():
            if not getattr(req, field):
                for key in env_keys:
                    val = os.getenv(key) or self.engine.variables.get(key.lower())
                    if val:
                        setattr(req, field, val)
                        break

    def _forge_vcard(self, req: ProtocolRequest) -> str:
        """
        [THE VCARD SUTURE]
        Generates a VCF 3.0 compliant string.
        Zero-dependency implementation for maximum portability.
        """
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"N:{req.last_name or ''};{req.first_name or ''};;;",
            f"FN:{req.first_name or ''} {req.last_name or ''}".strip(),
        ]

        if req.organization: lines.append(f"ORG:{req.organization}")
        if req.title: lines.append(f"TITLE:{req.title}")
        if req.phone: lines.append(f"TEL;TYPE=CELL:{req.phone}")
        if req.email: lines.append(f"EMAIL;TYPE=WORK:{req.email}")
        if req.url: lines.append(f"URL:{req.url}")
        if req.note: lines.append(f"NOTE:{req.note}")

        # [ASCENSION]: Unique Revision ID
        lines.append(f"REV:{time.strftime('%Y-%m-%dT%H:%M:%SZ')}")
        lines.append(f"UID:urn:uuid:{uuid.uuid4()}")
        lines.append("END:VCARD")

        return "\n".join(lines)

    def _forge_ical(self, req: ProtocolRequest) -> str:
        """
        [THE TEMPORAL SUTURE]
        Generates a basic ICS string.
        """
        if not req.event_start:
            raise ArtisanHeresy("iCal requires event_start.")

        fmt = "%Y%m%dT%H%M%SZ"
        start_str = req.event_start.strftime(fmt)
        end_str = req.event_end.strftime(fmt) if req.event_end else start_str

        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Novalym//Scaffold//EN",
            "BEGIN:VEVENT",
            f"UID:{uuid.uuid4()}",
            f"DTSTAMP:{time.strftime(fmt)}",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
            f"SUMMARY:{req.event_summary or 'Meeting'}",
        ]

        if req.location: lines.append(f"LOCATION:{req.location}")

        lines.append("END:VEVENT")
        lines.append("END:VCALENDAR")

        return "\n".join(lines)
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

from .base import BaseCourier
from ..contracts import MessageEnvelope
from .....interfaces.base import ScaffoldResult
from .....contracts.heresy_contracts import ArtisanHeresy


class SMTPCourier(BaseCourier):
    """
    [THE OLD WAYS]
    Universal SMTP logic. Compatible with Gmail, Yahoo, Zoho, Outlook, and self-hosted Postfix.
    """

    # The Grimoire of Presets
    PRESETS = {
        "gmail": ("smtp.gmail.com", 587),
        "yahoo": ("smtp.mail.yahoo.com", 587),
        "outlook": ("smtp.office365.com", 587),
        "zoho": ("smtp.zoho.com", 587),
        "icloud": ("smtp.mail.me.com", 587),
    }

    def deliver(self, envelope: MessageEnvelope) -> ScaffoldResult:
        # 1. Divine Configuration
        provider = envelope.metadata.get("provider", "custom")
        host, port = self.PRESETS.get(provider, (os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT", 587))))

        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASS")

        if not host or not user or not password:
            raise ArtisanHeresy(f"SMTP Credentials void. Provider: {provider}")

        # 2. Forge the MIME Vessel
        msg = MIMEMultipart("alternative")
        msg["Subject"] = envelope.subject
        msg["From"] = user
        msg["To"] = ", ".join(envelope.to)
        if envelope.cc: msg["Cc"] = ", ".join(envelope.cc)

        # 3. Inscribe Content
        msg.attach(MIMEText(envelope.body_text, "plain"))
        if envelope.body_html:
            msg.attach(MIMEText(envelope.body_html, "html"))

        # 4. Attach Matter (Files)
        for path in envelope.attachments:
            if not path.exists(): continue
            try:
                with open(path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename= {path.name}")
                msg.attach(part)
            except Exception as e:
                self.engine.logger.warn(f"Failed to attach {path.name}: {e}")

        # 5. The Rite of Transmission
        try:
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(user, password)

                recipients = envelope.to + envelope.cc + envelope.bcc
                server.sendmail(user, recipients, msg.as_string())

            return self.engine.success(f"SMTP Transmission to {len(recipients)} targets complete via {host}.")
        except Exception as e:
            return self.engine.failure(f"SMTP Fracture: {e}")
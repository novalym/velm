# Path: scaffold/artisans/services/twilio/client.py
# -------------------------------------------------

import os
import logging
from threading import Lock
from typing import Optional
from twilio.rest import Client
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = logging.getLogger("TwilioFactory")


class ClientFactory:
    """[THE CONNECTION FORGE]"""
    _instance: Optional[Client] = None
    _lock = Lock()

    @classmethod
    def get_client(cls, simulation_mode: bool = False) -> Optional[Client]:
        with cls._lock:
            if cls._instance: return cls._instance

            sid = os.environ.get("TWILIO_ACCOUNT_SID")
            token = os.environ.get("TWILIO_AUTH_TOKEN")

            if not (sid and token):
                if simulation_mode:
                    Logger.warning("Credentials void. Operating in Phantom Mode.")
                    return None
                else:
                    raise ArtisanHeresy(
                        "Telephonic Credentials Missing.",
                        severity=HeresySeverity.CRITICAL,
                        suggestion="Inject TWILIO_ACCOUNT_SID/AUTH_TOKEN."
                    )

            try:
                # [ASCENSION] Region awareness could be injected here
                cls._instance = Client(sid, token)
                return cls._instance
            except Exception as e:
                raise ArtisanHeresy(f"Failed to forge Client: {e}")
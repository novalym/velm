import os
import stripe
from threading import Lock
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class StripeMint:
    """
    [THE MINT]
    A thread-safe singleton for the Stripe Sovereign Connection.
    Enforces API versioning and key presence.
    """
    _instance = None
    _lock = Lock()

    @classmethod
    def get_client(cls):
        with cls._lock:
            if cls._instance:
                return cls._instance

            api_key = os.environ.get("STRIPE_SECRET_KEY")
            if not api_key:
                raise ArtisanHeresy(
                    "The Treasury is locked. STRIPE_SECRET_KEY not found.",
                    severity=HeresySeverity.CRITICAL
                )

            stripe.api_key = api_key
            stripe.api_version = os.environ.get("STRIPE_API_VERSION", "2023-10-16")

            # Optional: Configure custom HTTP client here for proxy/logging
            cls._instance = stripe
            return cls._instance
# Path: core/daemon/registry/guard.py
from typing import Any, Type
from ....logger import Scribe

Logger = Scribe("RegistryGuard")


class SentinelGuard:
    """[FACULTY]: Adjudicates the purity of an Artisan-Request pair."""

    @staticmethod
    def validate(request_class: Type, artisan_class: Type) -> bool:
        # [ASCENSION 6]: Contractual Purity Check
        # Verify that the Request is a Pydantic model and Artisan has an execute method
        if not hasattr(request_class, "model_validate"):
            Logger.warn(f"Heresy: {request_class.__name__} lacks a Gnostic Contract (Pydantic).")
            return False

        if not hasattr(artisan_class, "execute"):
            Logger.warn(f"Heresy: {artisan_class.__name__} is mute (missing execute method).")
            return False

        return True


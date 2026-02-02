# Path: scaffold/artisans/services/twilio/domains/base.py
# -------------------------------------------------------

from abc import ABC, abstractmethod
from typing import Any
from twilio.rest import Client
from .....interfaces.requests import TwilioRequest
from .....interfaces.base import ScaffoldResult
from ..utils import TelephonicAlchemist

class BaseTwilioDomain(ABC):
    """
    [THE COVENANT OF THE DOMAIN]
    Abstract base for specific Twilio capability sets.
    """
    def __init__(self, client: Client, engine: Any):
        self.client = client
        self.engine = engine
        self.alchemist = TelephonicAlchemist()

    @abstractmethod
    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        pass
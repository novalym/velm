from abc import ABC, abstractmethod
from typing import Any
from ..contracts import MessageEnvelope
from .....interfaces.base import ScaffoldResult


class BaseCourier(ABC):
    """[THE COVENANT OF DELIVERY]"""

    def __init__(self, engine: Any):
        self.engine = engine

    @abstractmethod
    def deliver(self, envelope: MessageEnvelope) -> ScaffoldResult:
        pass
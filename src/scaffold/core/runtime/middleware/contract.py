# Path: scaffold/core/runtime/middleware/contract.py
# --------------------------------------------------

from abc import ABC, abstractmethod
from typing import Callable, Any
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult

# The Next Link in the Chain
NextHandler = Callable[[BaseRequest], ScaffoldResult]


class Middleware(ABC):
    """
    The Sacred Contract of Interception.
    A Middleware sits between the Architect's Will and the Engine's Hand.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.logger = engine.logger

    @abstractmethod
    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        """
        Intercepts the plea.
        Can return a Result immediately (blocking the rite),
        or call next_handler(request) to proceed.
        """
        pass
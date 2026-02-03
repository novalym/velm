from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProcessor(ABC):
    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger

    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass


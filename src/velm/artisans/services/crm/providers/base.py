from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .....interfaces.base import ScaffoldResult


class BaseCRMProvider(ABC):
    """
    [THE COVENANT OF RELATIONSHIPS]
    Every CRM implementation must sign this contract.
    It enforces normalization of Create, Read, Update, Delete, and Link operations.
    """

    def __init__(self, engine: Any):
        self.engine = engine

    @abstractmethod
    def create(self, entity: str, data: Dict) -> Any:
        pass

    @abstractmethod
    def update(self, entity: str, entity_id: str, data: Dict) -> Any:
        pass

    @abstractmethod
    def get(self, entity: str, entity_id: str, properties: List[str] = None) -> Any:
        pass

    @abstractmethod
    def search(self, entity: str, field: str, value: str, properties: List[str] = None) -> Any:
        pass

    @abstractmethod
    def associate(self, from_entity: str, from_id: str, to_entity: str, to_id: str) -> Any:
        pass

    # --- THE AUTOMATED RITES (Default Implementations) ---

    def upsert(self, entity: str, match_key: str, match_value: str, data: Dict) -> Any:
        """
        [THE RITE OF IDEMPOTENCY]
        Checks if the soul exists. If so, transfigures it. If not, births it.
        """
        existing = self.search(entity, match_key, match_value)

        # Unify search results (list vs single)
        target = existing[0] if isinstance(existing, list) and existing else existing

        if target:
            # Update
            # Assuming target has an 'id' field, which most CRMs respect
            t_id = target.get('id')
            return self.update(entity, t_id, data)
        else:
            # Create
            # Inject the match key into data if missing, to ensure consistency
            if match_key not in data:
                data[match_key] = match_value
            return self.create(entity, data)
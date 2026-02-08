# Path: src/velm/core/infrastructure/contracts.py
# -----------------------------------------------
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
import time


class VMInstance(BaseModel):
    """The materialized soul of a compute node."""
    id: str
    provider_id: str
    ip_address: Optional[str]
    state: str  # PENDING, RUNNING, STOPPED, TERMINATED
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: float = Field(default_factory=time.time)


class ComputeProvider(ABC):
    """
    The High Interface for Materializing Compute.
    Any cloud (Oracle, AWS, Hetzner) must honor this contract.
    """

    @abstractmethod
    def authenticate(self) -> bool:
        """Verify credentials are manifest."""
        pass

    @abstractmethod
    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """
        The Kinetic Strike.
        Materializes a server from the void.
        Should handle retries, backoff, and 'Void Sensing' internally.
        """
        pass

    @abstractmethod
    def get_status(self, instance_id: str) -> VMInstance:
        """Scries the health of a specific node."""
        pass

    @abstractmethod
    def terminate(self, instance_id: str) -> bool:
        """Returns the node to the void."""
        pass
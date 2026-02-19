# Path: src/velm/core/infrastructure/contracts.py
# -----------------------------------------------
# LIF: ∞ | ROLE: ARCHITECTURAL_CONSTITUTION | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_INFRA_CONTRACTS_V200_TOTALITY_2026_FINALIS

from __future__ import annotations
import time
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Final

from pydantic import BaseModel, Field, ConfigDict, computed_field


# =============================================================================
# == STRATUM-0: THE TAXONOMY OF STATES                                       ==
# =============================================================================

class NodeState(str, Enum):
    """
    =============================================================================
    == THE ONTOLOGY OF BEING (V-Ω-STATES)                                     ==
    =============================================================================
    Defines the physiological phase of a compute node's existence.
    """
    PENDING = "PENDING"  # Reality is being forged
    RUNNING = "RUNNING"  # Matter is resonant and breathing
    STOPPED = "STOPPED"  # Soul is dormant, matter persists
    TERMINATED = "TERMINATED"  # Matter returned to the void
    FRACTURED = "FRACTURED"  # A heresy has occurred (Error)
    GHOST = "GHOST"  # Prophesied in the ledger, but unmanifest
    UNKNOWN = "UNKNOWN"  # Perception is clouded


# =============================================================================
# == STRATUM-1: THE GNOSTIC VESSELS (DATA MODELS)                            ==
# =============================================================================

class VMInstance(BaseModel):
    """
    =============================================================================
    == THE GNOSTIC VESSEL: VM_INSTANCE (V-Ω-TOTALITY)                          ==
    =============================================================================
    The bit-perfect representation of a compute node manifest in the multiverse.
    """
    model_config = ConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        populate_by_name=True
    )

    # --- I. IDENTITY STRATUM ---
    id: str = Field(..., description="The physical ID assigned by the Provider.")
    name: str = Field(..., description="The human-readable label of the reality.")
    provider_id: str = Field(..., description="The slug of the forge (aws, oracle, etc).")
    trace_id: str = Field(default_factory=lambda: f"tr-{uuid.uuid4().hex[:8].upper()}",
                          description="The Silver Cord linking this node to an Intent.")

    # --- II. SPATIAL COORDINATES ---
    region: str = Field("universal", description="The geographic or virtual locus.")
    public_ip: Optional[str] = None
    private_ip: Optional[str] = None

    # --- III. VITALITY & FORM ---
    state: NodeState = NodeState.PENDING
    size: str = "default"
    image: str = "default"

    # --- IV. FISCAL TELEMETRY ---
    cost_per_hour: float = 0.0
    currency: str = "USD"

    # --- V. THE AKASHIC METADATA ---
    tags: Dict[str, str] = Field(default_factory=dict, description="Semantic labels.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="The Bag of Holding for Provider Gnosis.")

    # --- VI. CHRONOMETRY ---
    created_at: float = Field(default_factory=time.time)
    last_scried_at: float = Field(default_factory=time.time)

    @computed_field
    @property
    def connection_uri(self) -> str:
        """
        [ASCENSION 5]: THE UNIVERSAL URI.
        Forges the access string based on the node's protocol and IP.
        """
        user = self.tags.get("ssh_user") or self.metadata.get("default_user") or "root"
        if not self.public_ip:
            return f"local://{self.id}"
        return f"ssh://{user}@{self.public_ip}"

    @computed_field
    @property
    def uptime_seconds(self) -> float:
        """Calculates the temporal age of the node since inception."""
        if self.state == NodeState.TERMINATED:
            return 0.0
        return time.time() - self.created_at

    def is_alive(self) -> bool:
        """Adjudicates if the node is currently capable of logic."""
        return self.state == NodeState.RUNNING


# =============================================================================
# == STRATUM-2: THE ARTISAN INTERFACE (THE LAW)                             ==
# =============================================================================

class ComputeProvider(ABC):
    """
    =============================================================================
    == THE HIGH INTERFACE: COMPUTE PROVIDER (V-Ω-HYPERVISOR)                   ==
    =============================================================================
    LIF: ∞ | ROLE: REALITY_TRANSMUTER

    The unbreakable contract that every cloud driver must honor.
    """

    @property
    @abstractmethod
    def provider_code(self) -> str:
        """The canonical identifier (e.g., 'azure', 'hetzner')."""
        pass

    @abstractmethod
    def authenticate(self) -> bool:
        """
        The Rite of Keys.
        Ensures the Architect possesses the authority to command this cloud.
        """
        pass

    @abstractmethod
    def provision(self, config: Dict[str, Any]) -> VMInstance:
        """
        The Kinetic Strike.
        Materializes a new reality from the void.
        """
        pass

    @abstractmethod
    def get_status(self, instance_id: str) -> VMInstance:
        """
        The Scrying Rite.
        Perceives the current state and metadata of a specific node.
        """
        pass

    @abstractmethod
    def list_nodes(self, tag_filter: Optional[Dict[str, str]] = None) -> List[VMInstance]:
        """
        The Census Rite.
        Returns a list of all living nodes warded by VELM in this realm.
        """
        pass

    @abstractmethod
    def terminate(self, instance_id: str) -> bool:
        """
        The Rite of Annihilation.
        Returns the node's matter to the void and ceases all metabolic tax.
        """
        pass

    @abstractmethod
    def scry_market(self, size_query: str) -> Dict[str, Any]:
        """
        [ASCENSION 10]: THE FISCAL PROPHET.
        Returns current pricing and availability data for arbitration.
        """
        pass

    @abstractmethod
    def conduct_rite(self, instance_id: str, command: str) -> str:
        """
        [ASCENSION 9]: REMOTE_KINETICS.
        Executes a shell command directly on the remote node.
        """
        pass

    def get_cost_estimate(self, config: Dict[str, Any]) -> float:
        """
        The Prophecy of Economy.
        Provides an estimated hourly burn rate for the proposed config.
        """
        return 0.0


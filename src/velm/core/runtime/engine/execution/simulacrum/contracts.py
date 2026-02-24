# Path: core/runtime/engine/execution/simulacrum/contracts.py
# ---------------------------------------------------------

from enum import Enum, auto
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
import time


class ShardType(str, Enum):
    MATTER = "MATTER"  # Object Storage (S3, Files)
    PERSISTENCE = "DB"  # Relational/NoSQL (Postgres, Redis)
    SIGNAL = "SIGNAL"  # Communication (Twilio, SendGrid)
    COMMERCE = "COMMERCE"  # Fiscal (Stripe, Billing)
    COMPUTE = "COMPUTE"  # Serverless/Instance (Lambda, EC2)


class SimulationIntent(BaseModel):
    """The Will of the Architect applied to the Void."""
    model_config = ConfigDict(frozen=True)

    domain: str
    action: str
    payload: Dict[str, Any]
    trace_id: str
    timestamp: float = Field(default_factory=time.time)


class RealityShard(BaseModel):
    """A single atom of simulated infrastructure."""
    id: str
    type: ShardType
    state: Dict[str, Any] = Field(default_factory=dict)
    merkle_hash: str = "0xVOID"
    last_mutation: float = Field(default_factory=time.time)

    # [ASCENSION]: Temporal Decay
    ttl: Optional[int] = None  # Seconds until entropy reclaims this shard
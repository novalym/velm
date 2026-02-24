# Path: src/velm/artisans/schema/contracts.py
# ------------------------------------------
# LIF: ∞ | ROLE: ONTOLOGICAL_GRIMOIRE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTRACTS_V9000_TOTALITY_FINALIS

from enum import Enum, auto
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
import time


class SchismType(str, Enum):
    """The nature of the divergence between Mind and Matter."""
    PRIMORDIAL_VOID = "VOID"  # Table/Collection missing entirely
    MATTER_DEFICIENCY = "MISSING"  # Column/Field missing
    ONTOLOGICAL_DRIFT = "DRIFT"  # Type mismatch (e.g., Integer -> BigInt)
    CONSTRAINT_FRACTURE = "WARD"  # Index/Unique/FK mismatch
    GHOST_MATTER = "GHOST"  # Matter exists in DB but is unmanifest in Code


class EvolutionStrategy(str, Enum):
    """The method of realignment."""
    SURGICAL = "SURGICAL"  # Raw SQL ALTER/CREATE strike
    MIGRATE = "MIGRATE"  # Tool-assisted (Alembic/Prisma)
    SIMULATED = "SIMULATED"  # Inscribed in the Gnostic Simulacrum (WASM)
    REBUILD = "REBUILD"  # Drop and Forge (Dangerous/Dev only)


class SubstrateIdentity(BaseModel):
    """The physical DNA of the target database."""
    dialect: str = Field(..., pattern=r"^(postgres|sqlite|mysql|mongodb|redis)$")
    version: Optional[str] = None
    host: str = "local"
    is_ephemeral: bool = False  # True for WASM/Simulacrum


class SchemaSchism(BaseModel):
    """A single point of divergence."""
    model_config = ConfigDict(frozen=True)

    type: SchismType
    target_table: str
    target_column: Optional[str] = None
    willed_state: Dict[str, Any]
    manifest_state: Optional[Dict[str, Any]] = None
    severity: int = Field(1, ge=1, le=3)  # 3 = Data Loss Risk


class EvolutionManifest(BaseModel):
    """The complete plan for reality realignment."""
    tx_id: str
    stack: str
    substrate: SubstrateIdentity
    schisms: List[SchemaSchism]
    suggested_strategy: EvolutionStrategy
    sql_strike: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)


class StrikeResult(BaseModel):
    """The forensic chronicle of a completed evolution."""
    success: bool
    latency_ms: float
    schisms_healed: int
    applied_scripture: str
    vitals_delta: Dict[str, Any] = Field(default_factory=dict)
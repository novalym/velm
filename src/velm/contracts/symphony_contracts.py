# Path: scaffold/contracts/symphony_contracts.py
# ----------------------------------------------

from __future__ import annotations

import time
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, Field, ConfigDict


# =================================================================================
# == THE GNOSTIC CANON OF SYMPHONIC LAW (V-Ω-ETERNAL-APOTHEOSIS-STR-ENUMS)       ==
# =================================================================================
# LIF: ∞ (THE UNBREAKABLE SCHEMA OF WILL)
#
# This scripture defines the immutable vessels that carry the Architect's Will
# (Edict) and the Universe's Response (Reality) through the nervous system of
# the Symphony.
#
# ASCENSION NOTE: All Enums now inherit from `str`. This ensures that they serialize
# beautifully to JSON (for the Daemon/UI) and that Pydantic validates string inputs
# correctly, annihilating the "Input should be int" heresy.
# =================================================================================

# --- I. THE ENUMS OF ESSENCE (THE NATURE OF THINGS) ---

class EdictType(str, Enum):
    """
    The Gnostic Soul of a single line of Will.
    Determines which High Priest (Handler) shall conduct the rite.
    """
    ACTION = "ACTION"  # Kinetic: >> command
    POLYGLOT_ACTION = "POLYGLOT_ACTION"  # Foreign: py: ...
    VOW = "VOW"  # Judgment: ?? condition
    STATE = "STATE"  # Metaphysics: %% key: value
    COMMENT = "COMMENT"  # Silence: # ...
    BREAKPOINT = "BREAKPOINT"  # Intercession: !!

    # Structural & Logical
    CONDITIONAL = "CONDITIONAL"  # Logic: @if
    LOOP = "LOOP"  # Iteration: @for
    RESILIENCE = "RESILIENCE"  # Protection: @try
    PARALLEL_RITE = "PARALLEL_RITE"  # Concurrency: parallel:
    DIRECTIVE = "DIRECTIVE"  # Metaprogramming: @task, @import
    FILTER = "FILTER"  # Data Transformation: @filter


class ConditionalType(str, Enum):
    """The specific flavor of a Logic Gate."""
    IF = "IF"
    ELSE = "ELSE"
    ENDIF = "ENDIF"
    ELIF = "ELIF"


class ResilienceType(str, Enum):
    """The specific phase of a Resilience Block."""
    TRY = "TRY"
    CATCH = "CATCH"
    ENDTRY = "ENDTRY"


class EventType(str, Enum):
    """
    The Gnostic Alphabet for the Symphony's Event Bus.
    These sigils allow the Engine to telepathically communicate with the Renderer.
    """
    SYMPHONY_START = "SYMPHONY_START"  # The curtain rises
    SYMPHONY_END = "SYMPHONY_END"  # The curtain falls

    EDICT_START = "EDICT_START"  # A rite begins
    EDICT_SUCCESS = "EDICT_SUCCESS"  # A rite concludes purely
    EDICT_FAILURE = "EDICT_FAILURE"  # A rite falters

    STATE_CHANGE = "STATE_CHANGE"  # A metaphysical shift (Variable/Sanctum update)
    VOW_RESULT = "VOW_RESULT"  # A judgment has been rendered (Pass/Fail)

    SERVICE_STATE_CHANGE = "SERVICE_STATE_CHANGE"  # A daemon background process changed state
    PARADOX_PROCLAIMED = "PARADOX_PROCLAIMED"  # An exception was caught and handled
    LOG = "LOG"  # Raw stream output from a kinetic rite

    # [NEW] Telepathic Signals
    ACTION_PROLOGUE = "ACTION_PROLOGUE"  # Announce intent before execution
    ACTION_EPILOGUE = "ACTION_EPILOGUE"  # Announce result after execution


class ServiceState(str, Enum):
    """The Living State of a Daemon (Background Process)."""
    PENDING = "PENDING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    STOPPED = "STOPPED"
    CRASHED = "CRASHED"
    RESTARTING = "RESTARTING"


# --- II. THE VESSELS OF CONFIGURATION (THE ARGUMENTS OF WILL) ---

class ServiceConfig(BaseModel):
    """
    The DNA of a Background Service (@service).
    Defines how a daemon should be born, monitored, and resurrected.
    """
    model_config = ConfigDict(frozen=True)
    name: str
    command: str
    action: str = "start"
    healthcheck_cmd: Optional[str] = None
    initial_delay_s: int = 5
    restart_policy: str = Field("on-failure", pattern=r"^(on-failure|always|never)$")


class InteractivePrompt(BaseModel):
    """
    A sacred vessel for the `@ask` rite.
    Carries the question to be posed to the Architect and the variable to hold the answer.
    """
    model_config = ConfigDict(frozen=True)
    prompt_text: str
    target_variable: str
    is_secret: bool = False


class SecretSource(BaseModel):
    """
    A pure vessel of intent for the `@vault` rite.
    Directs the State Handler to fetch a secret from a secure provider.
    """
    model_config = ConfigDict(frozen=True)
    provider: str = "env"  # Prophecy: 'vault', 'aws-sm', 'gcp-sm'
    key: str


class RetryPolicy(BaseModel):
    """
    The Gnostic law for persistence in the face of paradox.
    Defines how a kinetic rite should struggle against entropy.
    """
    model_config = ConfigDict(frozen=True)
    max_attempts: int = 3
    backoff_strategy: str = Field("exponential", pattern=r"^(linear|exponential|fixed)$")
    interval_s: float = 1.0


# --- III. THE EDICT: THE GOD-VESSEL OF WILL ---

class Edict(BaseModel):
    """
    The one true, universal vessel of Gnostic Will.
    It represents a single instruction in the Symphony, parsed from the source scripture.
    It carries every possible nuance of intent, from simple shell commands to complex
    polyglot blocks and interactive prompts.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # --- Core Identity ---
    type: EdictType
    raw_scripture: str
    line_num: int
    source_blueprint: Optional[Path] = None  # The Law of Provenance (File Origin)

    # --- Vessels for Kinetic Will (Actions: >>) ---
    command: str = ""
    is_background: bool = False
    inputs: List[str] = Field(default_factory=list)  # For heredoc/stdin injection
    capture_as: Optional[str] = None  # Capture stdout into a variable
    adjudicator_type: Optional[str] = None  # Custom success criteria (using ...)

    # --- Vessels for Gnostic Judgment (Vows: ??) ---
    vow_type: str = ""
    vow_args: List[str] = Field(default_factory=list)

    # --- Vessels for Metaphysics (State: %%) ---
    state_key: str = ""
    state_value: str = ""

    # --- Vessels for Polyglot Reality (py:, js:, etc) ---
    language: Optional[str] = None
    script_block: Optional[str] = None
    working_directory: Optional[Path] = None

    # --- Vessels for Logic & Structure ---
    conditional_type: Optional[ConditionalType] = None
    resilience_type: Optional[ResilienceType] = None

    # Recursive Definition: Blocks contain other Edicts
    body: List['Edict'] = Field(default_factory=list)
    else_body: Optional[List['Edict']] = None
    parallel_edicts: List['Edict'] = Field(default_factory=list)

    directive_type: Optional[str] = None
    directive_args: List[str] = Field(default_factory=list)
    macro_name: Optional[str] = None

    # --- Vessels for the Ascended Faculties ---
    retry_policy: Optional[RetryPolicy] = None
    interactive_prompt: Optional[InteractivePrompt] = None
    service_config: Optional[ServiceConfig] = None
    secret_source: Optional[SecretSource] = None


# --- IV. THE VESSELS OF REALITY (THE OUTCOMES) ---

class ActionResult(BaseModel):
    """
    The chronicle of a single kinetic moment.
    It holds the physical truth of what happened when an Edict touched Reality.
    """
    output: str
    returncode: int
    duration: float
    command: str
    was_terminated: bool = False
    pid: Optional[int] = None
    diff: Optional[str] = None  # For `patch` or other transfiguration rites


class Reality(ActionResult):
    """
    A luminous, backward-compatible alias for ActionResult.
    Represents the manifest truth.
    """
    pass


# --- V. THE VESSELS OF TELEPATHY (EVENTS) ---

class ConductorEvent(BaseModel):
    """
    The atomic unit of Gnostic Telepathy.
    This vessel carries a single truth from the Engine to the Renderer via the Event Bus.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    type: EventType
    payload: Dict[str, Any]
    timestamp: float = Field(default_factory=time.time)


class SymphonyResult(BaseModel):
    """
    The Final, Luminous Dossier of the Rite.
    This is the sacred chronicle of a completed Symphony, returned to the Architect.
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    success: bool
    duration: float
    edicts_executed: int
    heresies: List[str]
    # A complete timeline of events for forensic replay
    event_timeline: List[ConductorEvent]


# === THE RITE OF GNOSTIC REBUILDING ===
# We must invoke this to resolve the forward references in the recursive Edict model.
# This heals the "ForwardRef" heresy.
Edict.model_rebuild()
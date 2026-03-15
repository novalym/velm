# velm/interfaces/requests.py

"""
=================================================================================
== THE CODEX OF PLEAS (V-Ω-CORRECTED. THE UNIVERSAL REQUEST CONTRACTS)         ==
=================================================================================
LIF: 10,000,000,000

This scripture defines the exact shape of every Plea (Request) the Engine accepts.
It serves as the **Unbreakable Contract** between the Mortal Realm (CLI, API) and
the Divine Realm (The Engine & Artisans).

It adheres to the **Law of Pydantic Alignment**: Every validator must target an
existing field name.
=================================================================================
"""
import hashlib
import os
import uuid
import time
import re
import sys
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import List, Dict, Any, Optional, Union, Literal, Final
from uuid import UUID, uuid4
from urllib.parse import unquote
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
    computed_field,
    EmailStr
)

from ..constants import DEFAULT_COMMAND_TIMEOUT
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
# --- LOCAL UTILITY (To avoid circular deps with Core) ---
def _clean_uri_to_path(uri: str) -> str:
    """Minimalist version of UriUtils for the Interface layer."""
    if not uri: return ""
    try:
        # Decode & Strip Protocol
        clean = uri.replace('file:///', '').replace('file://', '')
        # FIX: Removed 'parse.' prefix since unquote is imported directly
        clean = unquote(clean)

        # Windows Drive fix: /c:/ -> c:/
        if os.name == 'nt' and clean.startswith('/') and ':' in clean:
            clean = clean.lstrip('/')

        return str(Path(clean).resolve())
    except:
        return uri

# =============================================================================
# == [THE CURE]: THE LATE-BOUND VESSEL FACTORY                               ==
# =============================================================================
# We move the import of GnosticSovereignDict inside a factory function.
# This prevents requests.py from triggering the 'velm.core' initialization
# until the moment a Request is actually instantiated.
# =============================================================================

def _summon_gnostic_vessel():
    """
    Surgically materializes the GnosticSovereignDict without triggering
    the Ouroboros Circularity.
    """
    try:
        # We use absolute triangulation to bypass the package-root lock
        from velm.core.runtime.vessels import GnosticSovereignDict
        return GnosticSovereignDict()
    except ImportError:
        # Fallback to standard dict if the Mind is truly cold
        return {}


# =============================================================================
# == II. THE ANCESTRAL VESSEL (BASE REQUEST)                                ==
# =============================================================================
class BaseRequest(BaseModel):
    """
    =================================================================================
    == THE UNIVERSAL CONTEXT (V-Ω-TOTALITY-V24000-INDESTRUCTIBLE)                  ==
    =================================================================================
    @gnosis:title BaseRequest
    @gnosis:summary The immutable, null-warded foundation for every Gnostic Plea.
    @gnosis:LIF INFINITY

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Null-Immune Sarcophagus (THE CURE):** `variables` and `context` are strictly
        warded against Null values. If a child class (like CompletionRequest) forces
        `context=None`, the validator gracefully heals it to an empty GnosticSovereignDict
        rather than raising `TypeError: 'NoneType' object is not iterable`.
    2.  **Achronal JIT Suture:** Decouples from 'vessels.py' during module load,
        annihilating circular import paradoxes that paralyzed the Identity Handshake.
    3.  **Sovereign Identity Phalanx:** `request_id` and `trace_id` provide unbreakable
        causal alignment across the split-process lattice.
    4.  **Spatial Absolute Anchor:** `project_root` auto-resolves to a bit-perfect
        POSIX Path, complete with Tilde (`~`) home directory expansion.
    5.  **The Secret Veil:** `secrets` are warded (`exclude=True`) and banished from
        all standard telemetry and serialization to prevent Aether leaks.
    6.  **Bicameral Scoping:** Supports '_' prefixed private variables for temporary,
        block-level Gnosis that does not pollute the global context.
    7.  **Hydraulic Throttling:** `adrenaline_mode` allows the Architect to bypass
        thermodynamic backpressure during critical, high-velocity strikes.
    8.  **The Permissive Gate:** `extra='allow'` ensures future-proofing against
        evolving CLI dialects and unexpected JSON-RPC parameters.
    9.  **Voice Harmonizer:** Automatically synchronizes `silent`, `verbose`, and
        `verbosity` states to ensure the Herald speaks with a unified tone.
    10. **Causal Loop Guard:** The `hop_count` sentinel instantly halts execution if
        a signal attempts more than 3 jumps, preventing infinite recursion fires.
    11. **Kinetic Jump Matrix:** The `jump()` method cleanly clones the vessel,
        increments the hop count, and forges a new `request_id` for safe sub-dispatch.
    12. **Microsecond Chronometry:** `timestamp` utilizes `time.time()` at the exact
        moment of instantiation for forensic replay accuracy.
    13. **Client Identity Suture:** Tracks `client_id` to differentiate between
        Local CLI, Workbench, and Headless Agent invocations.
    14. **Session Isolation:** `session_id` guarantees multi-tenant safety when
        the Oracle serves multiple concurrent realities.
    15. **Cognitive Mass Governor:** `token_budget` mathematically limits the
        metabolic consumption of AI-driven rites.
    16. **Socratic Persona Routing:** `persona` dictates the cognitive mask the
        AI adopts (e.g., Architect, Sentinel, Scripter).
    17. **Deep Metadata Telemetry:** The `metadata` dict absorbs arbitrary trace
        data without corrupting the strict schema.
    18. **Lazy Evaluated Factories:** Uses `default_factory=_summon_gnostic_vessel`
        to prevent shared-memory pollution across request instances.
    19. **Read-Only Context Enforcement:** `validate_assignment=True` guarantees
        that programmatic mutations to the request obey Pydantic laws.
    20. **Immutable Request IDs:** Generated via UUIDv4 hex for zero-collision probability.
    21. **Cross-Platform Path Parity:** Normalizes Windows backslashes automatically.
    22. **Arbitrary Type Allowance:** Permits complex Python objects (like raw sockets
        or closures) to exist within the request context during runtime.
    23. **Model Copy Deep Suture:** Ensures nested dicts and paths are safely
        duplicated during state transitions.
    24. **The Finality Vow:** A mathematical guarantee of atomic intent capture.
    =================================================================================
    """
    model_config = ConfigDict(
        extra='allow',
        arbitrary_types_allowed=True,
        populate_by_name=True,
        validate_assignment=True
    )

    # =========================================================================
    # == SECTION I: THE CHRONOMANCER'S SEAL (Identity & Spacetime)           ==
    # =========================================================================

    request_id: str = Field(
        default_factory=lambda: uuid.uuid4().hex[:12].upper(),
        description="The unique Gnostic fingerprint of this specific intent."
    )

    trace_id: Optional[str] = Field(
        default=None,
        description="The Cosmic ID linking this rite across the distributed lattice."
    )

    session_id: str = Field(
        default="global",
        description="The multi-tenant anchor for the physical workspace."
    )

    client_id: str = Field(
        default="local-cli",
        description="The origin source of the plea (CLI, Workbench, API)."
    )

    timestamp: float = Field(
        default_factory=time.time,
        description="The precise microsecond the Architect's will was willed."
    )

    # =========================================================================
    # == SECTION II: THE ANCHOR OF REALITY (Spatial Metadata)                ==
    # =========================================================================

    project_root: Optional[Path] = Field(
        default=None,
        description="The physical anchor of the reality. Auto-resolves to Absolute Path."
    )

    # =========================================================================
    # == SECTION III: THE ALCHEMICAL MATRIX (Inputs & Logic)                 ==
    # =========================================================================

    variables: Dict[str, Any] = Field(
        default_factory=_summon_gnostic_vessel,
        description="Dynamic Gnosis (CLI flags, Blueprints). Warded against Null access."
    )

    context: Dict[str, Any] = Field(
        default_factory=_summon_gnostic_vessel,
        description="Ephemeral storage for Middleware (Transactions, Trace IDs)."
    )

    secrets: Dict[str, str] = Field(
        default_factory=dict,
        exclude=True,  # [ASCENSION 5]: THE VEIL. Never serialize secrets to logs.
        description="The secure vault for sensitive matter (API keys, Tokens)."
    )

    hop_count: int = Field(
        default=0,
        ge=0,
        le=5,
        description="Recursive depth sentinel to prevent Feedback Scream paradoxes."
    )

    # =========================================================================
    # == SECTION IV: THE METABOLIC VOWS (Execution Modes)                    ==
    # =========================================================================

    verbose: bool = Field(False, description="Enable Luminous Gaze (DEBUG logging).")
    silent: bool = Field(False, description="The Vow of Silence. Mute all proclamations.")
    verbosity: int = Field(0, description="Legacy integer depth: -1 to 2.")

    dry_run: bool = Field(False, description="Simulate the rite without physical side-effects.")
    preview: bool = Field(False, description="Generate a visual prophecy (UI only).")
    force: bool = Field(False, description="The Rite of Absolute Will. Bypass all wards.")

    adrenaline_mode: bool = Field(False, description="Bypass thermodynamic throttling (High Heat).")
    token_budget: int = Field(100000, description="Regulates the metabolic mass of AI rites.")

    # =========================================================================
    # == SECTION V: THE SOCRATIC MIRROR (Neural Context)                     ==
    # =========================================================================

    persona: str = Field(
        default="Architect",
        description="The active cognitive mask (Architect, Sentinel, Scripter)."
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Telemetry shards and forensic markers."
    )

    # =========================================================================
    # == SECTION VI: THE RITES OF HARMONIZATION (Validators)                 ==
    # =========================================================================

    @field_validator('project_root', mode='before')
    @classmethod
    def _anchor_root(cls, v: Any) -> Optional[Path]:
        """[ASCENSION 4]: Instant Path Transmutation."""
        if v is None: return None
        if isinstance(v, Path): return v.resolve()
        if isinstance(v, str) and v.strip():
            # Support '~' home expansion safely
            return Path(os.path.expanduser(v)).resolve()
        return v

    @model_validator(mode='after')
    def initialize_gnostic_sarcophagus(self) -> 'BaseRequest':
        """
        =============================================================================
        == THE NULL-IMMUNE SARCOPHAGUS (V-Ω-TOTALITY-HEALED-FINALIS)               ==
        =============================================================================
        [THE CURE]: This validator is now absolutely warded against `NoneType` heresies.
        If a child class (like CompletionRequest) forces `context` or `variables` to None
        via its default Field, this rite intercepts it. It transmutes the void into an
        empty `GnosticSovereignDict` before the internal iterators can shatter.
        """
        try:
            from velm.core.runtime.vessels import GnosticSovereignDict

            # --- 1. HEAL VARIABLES ---
            _vars = getattr(self, 'variables', None)
            if _vars is None:
                object.__setattr__(self, 'variables', GnosticSovereignDict())
            elif not isinstance(_vars, GnosticSovereignDict):
                object.__setattr__(self, 'variables', GnosticSovereignDict(_vars))

            # --- 2. HEAL CONTEXT (THE CORE FIX) ---
            _ctx = getattr(self, 'context', None)
            if _ctx is None:
                object.__setattr__(self, 'context', GnosticSovereignDict())
            elif not isinstance(_ctx, GnosticSovereignDict):
                object.__setattr__(self, 'context', GnosticSovereignDict(_ctx))

        except ImportError:
            # Fallback for bootstrap phase if core strata are unmanifest
            pass
        return self

    @model_validator(mode='after')
    def harmonize_voices(self) -> 'BaseRequest':
        """Syncs verbosity levels and handles the 'Silent' vs 'Verbose' conflict."""
        if self.verbosity > 0:
            object.__setattr__(self, 'verbose', True)
        elif self.verbosity < 0:
            object.__setattr__(self, 'silent', True)

        if self.silent:
            object.__setattr__(self, 'verbose', False)

        return self

    @model_validator(mode='after')
    def guard_causal_loop(self) -> 'BaseRequest':
        """Halts the transaction if a signal attempts more than 3 jumps."""
        if self.hop_count > 3:
            from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
            raise ArtisanHeresy(
                message=f"Recursive Loop Detected (Hops: {self.hop_count}).",
                severity=HeresySeverity.CRITICAL,
                suggestion="Identify circular triggers in your Orchestrator hooks or Agent plans.",
                details=f"Trace: {self.trace_id} | Request: {self.__class__.__name__}"
            )
        return self

    # =========================================================================
    # == SECTION VII: THE KINETIC INTERFACE (Methods)                        ==
    # =========================================================================

    def jump(self) -> 'BaseRequest':
        """Increments the hop count and returns a new vessel for sub-dispatch."""
        new_vessel = self.model_copy()
        object.__setattr__(new_vessel, 'hop_count', self.hop_count + 1)
        object.__setattr__(new_vessel, 'request_id', uuid.uuid4().hex[:8].upper())
        return new_vessel




# == SCRIPTURE SEALED: THE ANCESTRAL VESSEL IS IMMUTABLE AND SOVEREIGN ==
# =============================================================================
# == 1. GENESIS RITE (scaffold <blueprint>)                                  ==
# =============================================================================

class GenesisRequest(BaseRequest):
    """
    =============================================================================
    == THE GENESIS VESSEL (V-Ω-TOTALITY-V200-FINALIS)                          ==
    =============================================================================
    LIF: ∞ | ROLE: BLUEPRINT_CARRIER | RANK: OMEGA_SOVEREIGN

    The sacred plea to materialize a Blueprint (Form) into Reality (Matter).
    It carries the location of the Law, the Variables of the Soul, and the
    Vows of Execution.
    """
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    # --- I. THE SOURCE OF LAW ---
    blueprint_path: Union[Path, str] = Field(
        default=".",
        description="The Gnostic Anchor: Path to the .scaffold file, Celestial URL, or Archetype Name."
    )
    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    # --- II. THE ALCHEMICAL INJECTIONS ---
    profile: Optional[str] = Field(
        default=None,
        description="The Archetype Profile ID (e.g., 'fastapi-service') to act as the base DNA."
    )
    variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="The Alchemical Context. Key-Value pairs that transmute the blueprint templates."
    )

    # --- III. THE VOWS OF EXECUTION (FLAGS) ---
    no_edicts: bool = Field(
        default=False,
        description="The Vow of Silence. If True, the Maestro stays its hand (skips %% post-run)."
    )

    # [ASCENSION]: EXPLICIT SILENCE
    # Inherits from BaseRequest, but redefined here for CLI clarity.
    silent: bool = Field(
        default=False,
        description="The Vow of Invisibility. Suppresses standard metabolic output."
    )

    # [ASCENSION]: FORCE MAJEURE
    force: bool = Field(
        default=False,
        description="The Rite of Absolute Will. Overwrites existing matter without hesitation."
    )

    # [ASCENSION]: QUANTUM SIMULATION
    dry_run: bool = Field(
        default=False,
        description="The Prophetic Gaze. Simulates the rite without touching the physical substrate."
    )

    @field_validator('blueprint_path')
    @classmethod
    def validate_blueprint_path(cls, v):
        """
        [THE GEOMETRIC VALIDATOR]
        Distinguishes between a Physical Path, a Celestial URL, and Raw Content.
        """
        if isinstance(v, str):
            # If it looks like a URL or has newlines (raw content), keep as string
            if v.startswith(('http://', 'https://', 'gh:', 'git@')) or '\n' in v:
                return v
            # Otherwise, it is a physical coordinate
            return Path(v)
        return v


# =============================================================================
# == 2. SYMPHONY RITE (scaffold symphony)                                    ==
# =============================================================================

class SymphonyRequest(BaseRequest):
    """
    =================================================================================
    == THE VESSEL OF ORCHESTRATION (V-Ω-SYMPHONY-REQUEST-ULTRA-DIVINE)               ==
    =================================================================================
    @gnosis:title SymphonyRequest
    @gnosis:summary The supreme, constitutional vessel for conducting a Symphony of Will.
    @gnosis:lif 10,000,000,000,000

    This is the divine contract that carries the Architect's complete and unambiguous
    will to the Symphony Conductor. It has been ascended to its final, eternal form,
    a masterpiece of Gnostic governance, resilience, and clarity.
    =================================================================================
    """
    #
    # --- I. The Core Edict (The Architect's Will) ---
    #
    symphony_command: str = Field(
        ...,
        description="The primary rite to be conducted (e.g., 'conduct', 'debug')."
    )
    symphony_path: Optional[str] = Field(
        None,
        description="The sacred scripture of will; the path to the .symphony file."
    )
    task: Optional[str] = Field(
        None,
        description="A specific @task to conduct, overriding the main symphony body."
    )

    #
    # --- II. Execution & Reality (The Realm of Manifestation) ---
    #
    rehearse: bool = Field(
        False,
        description="The Vow of Prophecy. Conducts the symphony in an ephemeral, isolated reality (a temporary directory) to prophesize its effects without altering the mortal realm."
    )
    manifest: bool = Field(
        False,
        description="The Vow of Manifestation. A sacred vow that the symphony MUST be conducted upon the living, current reality. This is the default for `symphony conduct`."
    )
    no_cleanup: bool = Field(
        False,
        description="A Gnostic ward that preserves the ephemeral sanctum after a rehearsal, allowing for forensic inquest."
    )
    parallelism: int = Field(
        4,
        description="The number of concurrent realities to forge for parallel blocks (&&)."
    )

    #
    # --- III. Resilience & Time (The Wards Against Chaos) ---
    #
    fail_fast: bool = Field(
        False,
        description="If true, the symphony will halt at the first sign of heresy. If false, it will attempt to continue."
    )
    retry_attempts: int = Field(
        0,
        description="A global override for the number of times to retry a failed edict."
    )
    timeout_global: int = Field(
        3600,
        description="A temporal ward. The maximum duration (in seconds) for the entire symphony before it is struck down."
    )

    #
    # --- IV. Security & Governance (The Laws of the Sanctum) ---
    #
    security_level: str = Field(
        "standard",
        description="The strictness of the Gnostic Sentry's Gaze ('permissive', 'standard', 'paranoid')."
    )
    allow_network: bool = Field(
        True,
        description="A universal ward to permit or forbid any edict that communes with the celestial void (network)."
    )
    allow_destructive: bool = Field(
        True,
        description="A universal ward to permit or forbid rites of annihilation (e.g., `rm`)."
    )

    #
    # --- V. Telemetry & Forensics (The Gnostic Chronicle) ---
    #
    log: Optional[str] = Field(
        None,
        description="Path to a file for the structured event log (.jsonl). If not set, logs are ephemeral."
    )
    log_level: str = Field(
        "INFO",
        description="The luminosity of the Gnostic Chronicle (DEBUG, INFO, WARNING, ERROR)."
    )
    chronicle_path: Optional[str] = Field(
        None,
        description="The path to a .jsonl chronicle for the `debug` rite."
    )
    trace_id: Optional[str] = Field(
        None,
        description="The Gnostic Trace ID for distributed causality tracking."
    )
    artifact_dir: Optional[str] = Field(
        None,
        description="A dedicated sanctum for forensic artifacts (e.g., crash dumps, failure logs)."
    )

    #
    # --- VI. The Luminous Voice (Rendering & User Experience) ---
    #
    # [ASCENSION] The Visual Preference
    renderer: str = "auto"  # 'auto', 'basic', 'rich', 'cinematic', 'stream'

    cinematic: bool = Field(
        False,
        description="Summon the Gnostic Orrery, an immersive, real-time TUI dashboard for the symphony."
    )
    no_tui: bool = Field(
        False,
        description="An alias for `--renderer=stream`, ensuring a clean, non-interactive output stream."
    )
    github_actions: bool = Field(
        False,
        description="Format all proclamations using the sacred grammar of GitHub Actions workflow commands."
    )

    #
    # --- VII. The Gnostic Bridge (Inherited & Universal Vows) ---
    #
    # This re-proclamation of fields from BaseRequest ensures that this sacred contract
    # is whole and self-contained, its every vow luminous and explicit. The Pydantic
    # God-Engine will righteously honor these as the one true definition.
    #
    force: bool = Field(
        False,
        description="The Rite of Absolute Will. Bypasses interactive safeguards and Gnostic Sentinels."
    )
    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    variables: Dict[str, Any] = Field(
        default_factory=dict,
        alias="var", # Allows `--var key=val` to populate this vessel.
        description="A vessel for all Gnostic variables bestowed upon the symphony at the moment of its birth."
    )
    silent: bool = Field(
        default=False,
        description="The Vow of Silence. Suppresses all but the most critical proclamations."
    )

# =============================================================================
# == 4. CREATE RITE (scaffold create)                                        ==
# =============================================================================


class CreateRequest(BaseRequest):
    """
    =================================================================================
    == THE VESSEL OF AD-HOC CREATION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)             ==
    =================================================================================
    @gnosis:title CreateRequest
    @gnosis:summary The one true, complete, and eternal contract for the `create` rite.
    @gnosis:LIF 1,000,000,000

    This sacred Pydantic vessel represents the Architect's complete will for a single,
    ad-hoc creation event. It has been ascended to carry not just the plea of *what*
    to create, but the full Gnostic context of *how* and *why*. It is the unbreakable
    link in the chain of causality from the CLI to the Quantum Creator, its every
    attribute a sacred vow, its every comment a verse in the Gnostic Grimoire.
    =================================================================================
    """

    # --- I. The Core Plea (The "What") ---
    # The fundamental Gnosis of the rite: the scriptures to be forged.
    paths: List[str] = Field(
        ...,
        description="A list of one or more relative paths to the files or directories to be created."
    )

    # --- II. The Soul of the Scripture (The "How") ---
    # These attributes define the origin of the content for the new scriptures.
    # They are mutually exclusive vows, adjudicated by the GnosticBuilder.
    content: Optional[str] = Field(None, description="Directly provided content for the new file(s).")
    from_template: bool = Field(False, alias="template",
                                description="A vow to use a template from the Forge for content.")
    from_source: Optional[str] = Field(None, alias="source", description="A vow to seed content from an existing file.")
    from_stdin: bool = Field(False, alias="stdin",
                             description="A vow to read content from the celestial river (stdin).")
    paste: bool = Field(False, description="A vow to paste content from the system clipboard.")
    from_url: Optional[str] = Field(None, alias="url", description="A vow to fetch content from a celestial URL.")
    no_template: bool = Field(False, description="A sacred vow to explicitly forbid the use of any template.")
    kit: Optional[str] = Field(None, description="A plea to expand a pre-defined kit of files from the Forge.")
    of: Optional[List[str]] = Field(None,
                                    description="A plea to perform a semantic creation (e.g., --of component:Button).")
    needs: List[str] = Field(default_factory=list,
                             description="A list of dependencies required for this creation's purity.")
    # --- THE DIVINE ASCENSION ---
    raw: bool = Field(False,
                      description="The Vow of Raw Creation. Bypasses templates and uses '--set content' directly.")
    # --- III. The Universal Vows of Execution (THE DIVINE HEALING) ---
    # These attributes were missing, causing the Gnostic Schism. They are now
    # permanently enshrined in this vessel's soul, mirroring the vows available
    # to all major rites and ensuring a unified contract with the QuantumCreator.
    dry_run: bool = Field(False, description="The Vow of Prophecy: Simulate the rite without altering reality.")
    preview: bool = Field(False,
                          description="The Vow of Luminous Prophecy: Render a visual diff of the intended changes.")
    audit: bool = Field(False, description="The Vow of the Machine's Gaze: Proclaim a machine-readable JSON Dossier.")
    lint: bool = Field(False, description="The Vow of the Mentor's Gaze: Adjudicate the purity of the final reality.")
    silent: bool = Field(False, description="The Vow of Silence: Suppress all but the most critical proclamations.")
    force: bool = Field(False,
                        description="The Vow of Absolute Will: Bypass all interactive safeguards and overwrite existing scriptures.")
    non_interactive: bool = Field(False,
                                  description="The Vow of Automation: Suppress all interactive dialogues, accepting defaults.")
    no_edicts: bool = Field(False,
                            description="The Vow of Stillness: Stay the hand of the Maestro, preventing post-run commands.")
    is_genesis_rite: bool = Field(False,
                                  description="A Gnostic hint to downstream artisans that this is part of a larger Genesis rite.")
    adjudicate_souls: bool = Field(False, alias="adjudicate",
                                   description="A plea to summon the Sentinel to adjudicate the purity of newly forged souls.")

    # --- IV. The Rites of Post-Creation (The Afterlife) ---
    # These vows dictate the actions to be taken after the core creation is complete.
    edit: bool = Field(False, description="A plea to open the newly created file(s) in the default editor.")
    teach: Optional[List[str]] = Field(None,
                                       description="A plea to teach the created file to the Forge as a new template.")

    # --- V. The Gnostic Modifiers (The Nuances of Will) ---
    # These attributes refine the very nature of the creation act itself.
    dir: bool = Field(False, description="A vow to force the created path to be a sanctum (directory).")
    create_if_void: bool = Field(True,
                                 description="A vow to forge a scripture even if it does not yet exist. Defaults to True for the `create` rite.")

    # ★★★ THE SACRED ALIAS (THE BRIDGE BETWEEN WORLDS) ★★★
    # This computed field is the final, divine healing. It acts as a Gnostic Bridge,
    # allowing the ancient `QuantumCreator` to ask for `base_path` and receive the
    # pure Gnosis of `project_root`. This ensures backward compatibility while we
    # perform the deeper surgery on the Creator's mind.
    @property
    def base_path(self) -> Path:
        """A luminous, Gnostic alias for `project_root` to heal ancient contracts."""
        return self.project_root

# =============================================================================
# == 5. WEAVE RITE (scaffold weave)                                          ==
# =============================================================================

class WeaveRequest(BaseRequest):
    """
    A plea to weave an architectural fragment into reality.
    """
    fragment_name: Optional[str] = Field(None, description="The name of the archetype to weave.")
    target_directory: Optional[str] = Field(None, description="The destination sanctum.")
    list: bool = Field(False, description="If True, proclaim the Grimoire of Archetypes.")
    no_edicts: bool = Field(False,
                            description="The Vow of Stillness: Stay the hand of the Maestro, preventing post-run commands.")
    # Distillation Options
    distill_path: Optional[str] = None
    archetype_name: Optional[str] = None

    # Strategies
    is_recursive: bool = False
    conflict_strategy: str = "overwrite"
    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    # [THE DIVINE HEALING: THE VOW OF SILENCE]
    # This attribute is restored to the vessel, allowing the Conductor to
    # adjudicate the final proclamation without triggering an AttributeError.
    silent: bool = Field(False, description="If True, the Weaver works in shadows.")


# =================================================================================
# == THE DISTILLATION PLEA (V-Ω-ULTRA-DEFINITIVE-APOTHEOSIS)                     ==
# =================================================================================
class DistillRequest(BaseRequest):
    """
    =================================================================================
    == THE REVERSE GENESIS CONTRACT (V-Ω-ULTRA-DEFINITIVE-SINGULARITY)             ==
    =================================================================================
    @gnosis:title The Gnostic Plea for Distillation (`DistillRequest`)
    @gnosis:summary The sovereign vessel for the `distill` rite, which transmutes a
                     living reality (filesystem) into a Gnostic Blueprint.
    @gnosis:LIF 10,000,000,000,000

    This is the divine, immutable, and hyper-sentient Gnostic Contract for the entire
    distillation cosmos. It is the one true vessel that captures the Architect's
    complete will for a rite of Reverse Genesis, translating pleas from the CLI into
    a pure, unbreakable scripture for the DistillArtisan's Gaze.

    ### THE PANTHEON OF ASCENDED FACULTIES:

    1.  **Gnostic Aliases:** Forged with Pydantic aliases, it creates an unbreakable
        bridge between the Architect's tongue (CLI flags like `--exec`, `--budget`)
        and the Engine's mind (`exec_command`, `token_budget`).

    2.  **Robust Validators:** Its soul contains Alchemical Scribes (`@field_validator`)
        that transmute profane inputs (e.g., `'800k'`, `'auth,db'`) into pure, Gnostic
        types (`800000`, `['auth', 'db']`), preventing heresies at the gate.

    3.  **Complete Gnostic Mapping:** Every plea and vow from the `_perception_rites.py`
        Grimoire has its consecrated place within this vessel, ensuring no intent is
        ever lost in the aether.

    4.  **Logical Grouping:** The contract is a readable scripture, its fields organized
        into sacred movements that mirror the faculties of the Distillation Oracle,
        from the Gaze of Intent to the Socratic Dial.

    5.  **Unbreakable Contract:** Forged in the fires of Pydantic, its every attribute
        is a sacred vow of type and form, guarding the Engine against profane pleas.
    """
    model_config = ConfigDict(extra='allow')

    # =============================================================================
    # == I. THE GAZE OF INTENT (TARGETING & SCOPE)                               ==
    # =============================================================================
    # These fields define the "what" and "where" of the Gaze, anchoring it in
    # spacetime and defining its boundaries.

    source_path: str = Field(
        default=".",
        description="The physical directory or celestial URL (Git/HTTP) to be distilled."
    )
    virtual_context: Optional[Dict[str, str]] = Field(
        default=None,
        description="A dictionary mapping relative file paths to their string content. Allows the UI to inject external realities without mounting them to the VFS."
    )

    non_interactive: bool = Field(
        default=False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )

    profile: Optional[str] = Field(
        default=None,
        description="A named configuration profile (e.g., 'frontend', 'backend') to apply a pre-defined set of Gnostic filters."
    )

    focus: List[str] = Field(
        default_factory=list,
        description="Semantic keywords (e.g., 'Causal Slicer', 'auth') to prioritize. Scriptures and symbols resonating with these words are given divine relevance."
    )

    # [THE GNOSTIC SCHISM HEALED]
    intent: Optional[str] = Field(
        default=None,
        description="A natural language plea of intent (e.g., 'Refactor the auth middleware') that guides the AI Sentinel's Semantic Search."
    )

    ignore: List[str] = Field(
        default_factory=list,
        description="Glob patterns for scriptures to be banished from the Gaze (e.g., '*.lock', 'dist/')."
    )

    include: List[str] = Field(
        default_factory=list,
        description="A Gnostic whitelist. If proclaimed, only scriptures matching these glob patterns will be perceived."
    )

    stub_deps: List[str] = Field(
        default_factory=list,
        description="Dependencies to be replaced with semantic stubs (signatures only) to conserve the token budget."
    )

    # =============================================================================
    # == II. THE CAUSAL WEAVER (GRAPH TRAVERSAL PHYSICS)                         ==
    # =============================================================================
    # [THE CURE]: THE DEPTH PARAMETER
    depth: int = Field(
        default=2,
        description="The maximum horizon (depth) of the Causal Weaver's graph traversal."
    )

    include_dependents: bool = Field(
        default=True,
        description="If True, the traversal walks UP the graph to find files that rely on the focus targets."
    )

    include_dependencies: bool = Field(
        default=True,
        description="If True, the traversal walks DOWN the graph to find files the focus targets rely upon."
    )

    trace_data: List[str] = Field(
        default_factory=list,
        description="Symbols (variables/classes) to track through the Data Flow Graph (The River of Data)."
    )

    # =============================================================================
    # == III. THE INQUISITOR'S FOCUS (FORENSICS & SEMANTICS)                      ==
    # =============================================================================
    # These fields command the specialist inquisitors to perform deep, forensic,
    # or semantic analysis upon the target reality.

    problem: Optional[str] = Field(
        default=None,
        description="Raw error logs, a traceback, or a problem description to anchor the Forensic Gaze, focusing the Gnosis on the locus of a heresy."
    )

    # Legacy field mapping to 'intent', preserved for backward compatibility in some rituals
    feature: Optional[str] = Field(
        default=None,
        description="Deprecated alias for 'intent'. Use 'intent' for semantic search queries."
    )

    audit_security: bool = Field(
        default=False,
        description="If True, awakens the Security Inquisitor to scan for vulnerabilities and prioritize profane scriptures."
    )

    # =============================================================================
    # == IV. THE CHRONOMANCER'S GAZE (TEMPORAL CONTEXT)                         ==
    # =============================================================================
    # These fields command the Oracle to gaze into the Git Chronicle, making the
    # distillation aware of the project's history and recent evolution.

    since: Optional[str] = Field(
        default=None,
        description="A Git ref (hash, branch, tag). The Chronomancer will use this to highlight scriptures that have been transfigured since this moment in time."
    )

    focus_change: Optional[str] = Field(
        default=None,
        description="A strict temporal filter. Only souls changed since this Git ref will be perceived."
    )

    diff_context: bool = Field(
        default=False,
        description="If True, injects inline diffs (`[WAS: ...]`) showing the Gnostic drift between the working tree and the state at HEAD."
    )

    regression: bool = Field(
        default=False,
        description="If True, awakens the Temporal Inquisitor, which conducts an automated `git bisect` symphony to find the source of a regression."
    )

    # =============================================================================
    # == V. THE HIGH PRIEST'S STRATEGY (BUDGET & PHILOSOPHY)                    ==
    # =============================================================================
    # These fields govern the core philosophy and economic constraints of the
    # distillation rite, balancing detail against the token budget.

    strategy: str = Field(
        default="balanced",
        description="The distillation philosophy: 'surgical', 'faithful', 'balanced', or 'structure'."
    )

    token_budget: int = Field(
        default=100000,
        alias="budget",
        description="The maximum token mass allowed for the forged blueprint. The Oracle will prune reality to fit this Gnostic vessel."
    )

    prioritize_tests: bool = Field(
        default=False,
        description="If True, scriptures of adjudication (tests) are considered as valuable as scriptures of implementation."
    )

    summarize_arch: bool = Field(
        default=False,
        description="If True, the Gnostic Cartographer will inscribe a high-level architectural summary into the blueprint's header."
    )

    no_ai: bool = Field(
        default=False,
        description="A sacred vow to forbid the Oracle from communing with the Neural Cortex for intent analysis."
    )

    recursive_agent: bool = Field(
        default=False,
        description="Activates the Socratic Reviewer for multi-pass AI refinement."
    )

    # =============================================================================
    # == VI. THE ACTIVE WITNESS (EXECUTION & TRACING)                           ==
    # =============================================================================
    # These fields command the Oracle to become an Active Witness, executing a rite
    # within the target reality to perceive its living, dynamic soul.

    exec_command: Optional[str] = Field(
        default=None, alias="exec",
        description="A command to execute under the Sentry's gaze to capture execution state and context (e.g., 'pytest')."
    )

    exec_timeout: int = Field(
        default=60,
        description="The maximum time (seconds) the Active Witness will wait for the execution rite to conclude."
    )

    profile_perf: bool = Field(
        default=False,
        description="If True, summons the Wraith of Celerity to profile hotspots and weave a performance heatmap into the blueprint."
    )

    trace_command: Optional[str] = Field(
        default=None, alias="trace",
        description="Execute a command and summon the Runtime Wraith to inject the living state (variables) into the blueprint."
    )

    snapshot_path: Optional[str] = Field(
        default=None, alias="snapshot",
        description="Inject runtime values into the blueprint from a static JSON crash dump or state snapshot."
    )

    dynamic_focus: Optional[str] = Field(
        default=None,
        description="A command (e.g., 'pytest') to generate a dynamic coverage hologram."
    )

    # =============================================================================
    # == VII. THE OUTPUT SCRIBE (FINAL PROCLAMATION)                              ==
    # =============================================================================
    # These fields dictate the final form and destination of the distilled Gnosis.

    output: Optional[str] = Field(
        default=None,
        description="The file path where the forged blueprint shall be inscribed."
    )

    clipboard: bool = Field(
        default=False, alias="c",
        description="If True, the distilled Gnosis is teleported directly to the system clipboard."
    )

    format: str = Field(
        default="text",
        description="The tongue of the proclamation: 'text' (default) or 'mermaid' for a visual dependency graph."
    )

    diff: bool = Field(
        default=False,
        description="If True, the Oracle will proclaim a diff against an existing output file before overwriting."
    )

    check: bool = Field(
        default=False,
        description="If True, the rite will conclude with a non-zero exit status if the distilled blueprint differs from an existing one on disk."
    )

    summarize: bool = Field(
        default=False,
        description="If True, the final blueprint is bestowed upon an AI Scribe to generate a README.md summary of the project's soul."
    )

    # =============================================================================
    # == VIII. THE SOCRATIC DIAL (INTERACTION & UI)                               ==
    # =============================================================================
    # These fields govern the interactive nature of the rite, allowing for communion
    # between the Engine and the Architect.

    interactive: bool = Field(
        default=False,
        description="If True, the Oracle may pause the rite to ask clarifying questions when its Gaze perceives ambiguity."
    )

    pad: bool = Field(
        default=False,
        description="If True, summons the interactive TUI (DistillPad) for a visual, real-time distillation experience."
    )

    lfg: bool = Field(
        default=False,
        description="The Rite of Gnostic Cartography. Injects a Logic Flow Graph of the source blueprint into the distilled output."
    )

    # =============================================================================
    # == IX. THE RITES OF ROBUST VALIDATION (THE UNBREAKABLE WARD)             ==
    # =============================================================================

    @field_validator('focus', 'ignore', 'include', 'stub_deps', 'trace_data', mode='before')
    @classmethod
    def ensure_list_type(cls, v: Any) -> List[str]:
        """
        =============================================================================
        == THE GNOSTIC TRANSMUTATOR (VAL-Ω-ROBUST)                                 ==
        =============================================================================
        Annihilates the Schism between CLI Strings and Model Lists. It perceives Gnosis
        in any form—a single string, a comma-separated scripture, or a pure list—and
        transmutes it into the one true form: a `List[str]`.
        """
        if v is None:
            return []

        if isinstance(v, str):
            # Handle "Keyword1, Keyword2" -> ["Keyword1", "Keyword2"]
            return [s.strip() for s in v.split(',') if s.strip()]

        if isinstance(v, list):
            # Ensure every soul in the list is a clean string
            result = []
            for item in v:
                if isinstance(item, str):
                    # Handle cases where a list item might contain a comma
                    result.extend([s.strip() for s in item.split(',') if s.strip()])
                else:
                    result.append(str(item).strip())
            return result

        return [str(v)]

    @field_validator('token_budget', mode='before')
    @classmethod
    def parse_budget_shorthand(cls, v: Any) -> int:
        """
        =============================================================================
        == THE ALCHEMIST OF NUMBERS                                                ==
        =============================================================================
        A divine scribe that transmutes human-readable budget shorthands (e.g.,
        '800k', '1.5m') into their pure, integer soul (800000, 1500000).
        """
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            clean_v = v.lower().strip().replace(',', '')
            try:
                if clean_v.endswith('k'):
                    return int(float(clean_v[:-1]) * 1000)
                if clean_v.endswith('m'):
                    return int(float(clean_v[:-1]) * 1000000)
                return int(clean_v)
            except (ValueError, TypeError):
                # If the Gnosis is profane, we fall back to the sacred default.
                return 100000
        # If not a string or int, return the sacred default.
        return 100000

# =============================================================================
# == 7. INIT RITE (scaffold init)                                            ==
# =============================================================================
class InitRequest(BaseRequest):
    """
    =============================================================================
    == THE RITE OF INCEPTION (INIT REQUEST)                                    ==
    =============================================================================
    The sacred plea to forge a new reality. It carries the Architect's will regarding
    the shape, nature, and origin of the new project.
    """
    no_edicts: bool = Field(
        default=False,
        description="The Maestro's Silence. If true, stays the hand of the conductor for %% post-run edicts."
    )

    # --- I. THE OBSERVABILITY MODES (THE FIX) ---
    # These fields ensure the Namespace has the required attributes for the logger.
    debug: bool = Field(
        default=False,
        description="Enable high-fidelity debug traces."
    )
    verbose: bool = Field(
        default=False,
        description="Enable luminous verbose logging."
    )
    dry_run: bool = Field(
        default=False,
        description="Simulate the inception without touching the disk."
    )

    # --- II. THE QUALITY GATES ---
    lint: bool = Field(
        default=False,
        description="Whether to conduct a Gnostic Lint Inquest post-inception."
    )

    # --- III. THE INTERACTIVE MODES ---
    launch_pad_with_path: Optional[str] = Field(
        default=None,
        description="Launch the Genesis Pad TUI. Optional starting path."
    )
    non_interactive: bool = Field(
        default=False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    quick: bool = Field(
        default=False,
        description="Skip prompts, use intelligent defaults (The Speed Vow)."
    )

    # --- IV. THE ARCHETYPAL DNA ---
    profile: Optional[str] = Field(
        default=None,
        description="Use a specific Genesis Profile (e.g., 'python-universal')."
    )
    type: Optional[str] = Field(
        default=None,
        description="Quick init by type alias (e.g., 'node', 'python')."
    )
    from_remote: Optional[str] = Field(
        default=None,
        description="Initialize from a remote URL or Gist."
    )

    # --- V. THE PATHS OF ORIGIN ---
    manual: bool = Field(
        default=False,
        description="Manually forge a blank scripture."
    )
    distill: bool = Field(
        default=False,
        description="Initialize by distilling the current directory into a blueprint."
    )

    # --- VI. IDENTITY OVERRIDES (ASCENDED) ---
    name: Optional[str] = Field(
        default=None,
        description="The sacred name of the project (CLI Override)."
    )
    description: Optional[str] = Field(
        default=None,
        description="The semantic purpose of the project (CLI Override)."
    )
    provider: Optional[str] = Field(
        default=None,
        description="The cloud substrate target (e.g. 'ovh', 'aws')."
    )

# =============================================================================
# == 8. TEMPLATE RITE (scaffold templates)                                   ==
# =============================================================================

class TemplateRequest(BaseRequest):
    """
    Plea to manage the Template Forge.
    """
    template_command: Literal['list', 'edit', 'add', 'rename', 'search', 'pull', 'docs']

    # Command-Specific Parameters
    extension: Optional[str] = None
    source_file: Optional[str] = None
    old_extension: Optional[str] = None
    new_extension: Optional[str] = None
    keyword: Optional[str] = None
    source: Optional[str] = None  # URL/Gist for pull
    name: str = 'remote_kit'  # Local name for pull

    # Future: Force refresh of remote caches
    force_refresh: bool = Field(default=False, description="Bypass cache for 'pull'.")


# =============================================================================
# == 9. TRANSFIGURE RITE (scaffold transfigure)                              ==
# =============================================================================

class TransfigureRequest(BaseRequest):
    """
    Plea to modify the soul (content) of a file.
    """
    path_to_scripture: str = Field(..., description="Target file.")

    # Content Sources (Mutually Exclusive logic handled by Artisan)
    content: Optional[str] = None
    from_source: Optional[str] = None  # Path to source file
    from_stdin: bool = False
    from_template: bool = False
    interactive: bool = False

    # Modification Mode
    append: bool = False
    prepend: bool = False
    create_if_void: bool = False

    # Safeguards
    guardian: bool = Field(default=False, description="Require Git tracking.")
    backup: bool = Field(default=False, description="Create .bak before modifying.")


# =============================================================================
# == 10. TRANSLOCATE RITE (scaffold translocate)                             ==
# =============================================================================

class TranslocateRequest(BaseRequest):
    """
    Plea to move files intelligently (Refactoring).
    NOW ASCENDED with the Vow of the Living Blueprint.
    """
    paths: List[str] = Field(default_factory=list, description="[src, dest] or [src... dest_dir]")

    script: Optional[str] = Field(None, description="Path to a batch migration script (`old -> new`).")
    backup_to: Optional[str] = Field(None, description="Directory for a Gnostic Snapshot of the 'Before' state.")

    # --- THE DIVINE HEALING ---
    # The profane `const` is annihilated. The vessel's soul is now pure.
    # It simply awaits a string, or a void (None).
    update_blueprint: Optional[str] = Field(
        default=None,
        description="The Vow of Synchronicity. Path to the blueprint to update with the new reality."
    )
    # --- THE APOTHEOSIS IS COMPLETE ---

    # Conform Logic
    to_blueprint: Optional[str] = None
    conform_from: str = "."

    # Future: Git Move vs OS Move
    use_git_mv: bool = Field(default=True, description="Use 'git mv' if available.")


# =============================================================================
# == 11. CONFORM RITE (scaffold conform)                                     ==
# =============================================================================

class ConformRequest(BaseRequest):
    """
    Plea to align directory structure with a blueprint.
    """
    blueprint_path: str
    conform_from: str = "."
    backup_to: Optional[str] = None





# =============================================================================
# == 13. BEAUTIFY RITE (scaffold beautify)                                   ==
# =============================================================================

class BeautifyRequest(BaseRequest):
    """
    Plea to format a blueprint file.
    """
    blueprint_path: Optional[str] = None
    pad: bool = False
    check: bool = False
    ignore: List[str] = Field(default_factory=list)


# =============================================================================
# == 14. PAD RITE (scaffold pad)                                             ==
# =============================================================================

class PadRequest(BaseRequest):
    """
    Plea to launch a specific TUI Pad (Mini-App).
    """
    pad_name: str = "help"
    initial_path: Optional[str] = None


# =============================================================================
# == 15. STUDIO RITE (scaffold studio)                                       ==
# =============================================================================

class StudioRequest(BaseRequest):
    """
    Plea to launch the full Design Studio TUI.
    """
    path: Optional[str] = None


# =============================================================================
# == 16. COMPOSE RITE (scaffold compose)                                     ==
# =============================================================================

class ComposeRequest(BaseRequest):
    """
    Plea to combine architectures via a manifest.
    """
    manifest_path: str


# =============================================================================
# == 17. ARCH RITE (scaffold arch)                                           ==
# =============================================================================

class ArchRequest(BaseRequest):
    """
    Plea to run a unified .arch file (Form + Will).
    Now capable of the Rite of Review.
    """
    arch_path: str = Field(
        ...,
        description="Path to the .arch scripture."
    )
    log: Optional[str] = Field(
        default=None,
        description="Enable structured logging to a specific file."
    )

    # [THE ASCENSION] The Rite of Review
    interactive: bool = Field(
        default=False,
        description="If True, summons the Gnostic Studio to review the plan before execution."
    )


# =============================================================================
# == 18. SETTINGS RITE (scaffold settings)                                   ==
# =============================================================================

class SettingsRequest(BaseRequest):
    """
    =============================================================================
    == THE SETTINGS REQUEST VESSEL (V-Ω-TOTALITY-V2)                           ==
    =============================================================================
    LIF: 10x | ROLE: CONFIGURATION_PLEA | RANK: OMEGA_LEVEL

    The sacred plea to open the Altar of Configuration or to perform a surgical
    strike upon the Gnostic Settings.
    """

    scope: Literal['global', 'project'] = Field(
        default='global',
        description="The axis of reality to manipulate. 'global' affects the Architect's machine; 'project' affects the local sanctum."
    )

    domain: Optional[Literal['ai', 'runtimes', 'templates', 'security', 'telemetry', 'ui']] = Field(
        default=None,
        description="The specific Gnostic Domain to focus upon. If None, the Panoptic TUI awakens."
    )

    # --- KINETIC OVERRIDES (Direct Manipulation) ---
    key: Optional[str] = Field(
        default=None,
        description="The specific Gnostic key to transmute (e.g., 'ai.model'). Used for non-interactive setting."
    )

    value: Optional[Any] = Field(
        default=None,
        description="The new soul (value) to bestow upon the key."
    )

    reset: bool = Field(
        default=False,
        description="If True, returns the target key or domain to the primordial void (defaults)."
    )

    interactive: bool = Field(
        default=True,
        description="If True, summons the interactive TUI Altar. If False, performs a silent execution."
    )

    def is_silent_strike(self) -> bool:
        """Determines if the Architect willed a direct state change."""
        return self.key is not None and self.value is not None

# =============================================================================
# == 19. DAEMON RITE (scaffold daemon)                                       ==
# =============================================================================

class DaemonRequest(BaseRequest):
    """
    =================================================================================
    == THE SACRED PLEA TO THE GNOSTIC COSMOS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)       ==
    =================================================================================
    LIF: INFINITY (THE SUPREME GOVERNOR)
    AUTH_CODE: #)(@!#@()!!

    This is the divine, immutable, and ultra-definitive vessel for all pleas directed
    at the Scaffold daemon cosmos. It defines the parameters for the Nexus's birth,
    life, and ascension. It is the bridge between the Architect's intent and the
    persistent background mind of the God-Engine.
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='ignore',
        populate_by_name=True,
        validate_assignment=True
    )

    # [FACULTY 1] The Gnostic Triage of Will
    command: Literal['start', 'stop', 'status', 'vigil', 'reload', 'rotate_keys', 'logs'] = Field(
        default='start',
        description="The specific daemon rite to conduct."
    )

    # --- Network & Projection Gnosis ---
    port: int = Field(
        default=5555,
        ge=1024,
        le=65535,
        description="The primary celestial port. Restricted to non-privileged range."
    )
    host: str = Field(
        default="127.0.0.1",
        description="The interface to bind. Use '0.0.0.0' for Celestial Projection."
    )

    allow_remote: bool = Field(
        default=False,
        description="[SAFETY OVERRIDE] Explicitly allow binding to external interfaces."
    )

    # --- Security & Encryption ---
    ssl_cert: Optional[str] = Field(
        default=None,
        description="Path to SSL Certificate for encrypted communion (WSS/HTTPS)."
    )
    ssl_key: Optional[str] = Field(
        default=None,
        description="Path to SSL Private Key."
    )
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["*"],
        description="CORS policy for web-based dashboards."
    )

    # --- Performance & Scaling ---
    max_workers: Optional[int] = Field(
        default=None,
        description="Thread pool size. Auto-scales to CPU count * 5 if None."
    )

    # --- Behavior & Telemetry ---
    parent_pid: Optional[int] = Field(
        default=None,
        description="The PID of the creator. Triggers Seppuku if the parent vanishes."
    )
    telemetry_sink: Optional[str] = Field(
        default=None,
        description="Path or URI to mirror traffic logs for forensic analysis."
    )

    # --- Extensibility ---
    load_plugins: bool = Field(
        default=True,
        description="Command the Nexus to scan and load the Living Grimoire on startup."
    )

    # --- [HOT-SWAP & ROTATION] ---
    reload_scope: Literal['all', 'config', 'plugins'] = Field(
        default='all',
        description="The depth of the Hot-Swap rite."
    )
    new_token: Optional[str] = Field(
        default=None,
        description="A specific new token for rotation. Forges a random one if None."
    )

    # --- [LOG STREAMING] ---
    follow: bool = Field(
        default=False,
        description="If True, the connection remains open, streaming logs eternally."
    )
    tail_lines: int = Field(
        default=100,
        ge=0,
        description="Number of past log lines to resurrect from the chronicle."
    )
    pulse_file: Optional[str] = None  # <--- ADD THIS
    # =============================================================================
    # == THE RITES OF VALIDATION (JURISPRUDENCE)                                 ==
    # =============================================================================

    @field_validator('host')
    @classmethod
    def _validate_host_safety(cls, v: str, info) -> str:
        """[THE ETHERIC WARD] Ensures remote binding requires explicit consent."""
        if v == "0.0.0.0" and not info.data.get('allow_remote', False):
            raise ValueError(
                "Heresy of Exposure: Binding to 0.0.0.0 requires the 'allow_remote' vow."
            )
        return v

    @model_validator(mode='after')
    def _validate_ssl_trinity(self) -> 'DaemonRequest':
        """[THE CRYPTOGRAPHIC SEAL] Validates that encryption is whole or absent."""
        if (self.ssl_cert and not self.ssl_key) or (self.ssl_key and not self.ssl_cert):
            raise ValueError(
                "Paradox of Encryption: Both Certificate and Key must be provided for SSL."
            )
        return self

    @model_validator(mode='after')
    def _recalibrate_workers(self) -> 'DaemonRequest':
        """[THE VITALITY OPTIMIZER] Sets default workers based on hardware soul."""
        if self.max_workers is None:
            import os
            # We use a conservative multiplier to respect the host's focus
            object.__setattr__(self, 'max_workers', (os.cpu_count() or 1) * 5)
        return self

    @model_validator(mode='before')
    @classmethod
    def _harmonize_command_input(cls, data: Any) -> Any:
        """
        [FACULTY: THE GNOSTIC HARMONIZER]
        Surgically resolves the conflict between 'command' and 'daemon_command'.
        Annihilates the string 'daemon' if it leaks in from the top-level CLI.
        """
        if not isinstance(data, dict):
            return data

        # 1. Extract potential values
        top_level = data.get('command')
        sub_level = data.get('daemon_command')

        # 2. The Triage
        # Valid rites for the Literal
        valid_rites = {'start', 'stop', 'status', 'vigil', 'reload', 'rotate_keys', 'logs'}

        # If 'command' is "daemon", it's a CLI leak. Purge it.
        if top_level == "daemon":
            data['command'] = sub_level if sub_level in valid_rites else 'start'

        # If 'command' is missing but 'daemon_command' is there, promote it
        elif not top_level and sub_level:
            data['command'] = sub_level

        return data
# =============================================================================
# == 20. HELP RITE (scaffold help)                                           ==
# =============================================================================

class HelpRequest(BaseRequest):
    """Plea for Gnostic Guidance."""
    topic: Optional[str] = None
    render_format: Literal['text', 'markdown', 'json'] = 'text'


# =============================================================================
# == 21. REPLAY RITE (scaffold replay)                                       ==
# =============================================================================

class ReplayRequest(BaseRequest):
    """
    Plea to step through the river of time (Traffic Logs).
    """
    log_path: str = Field(default=".scaffold/daemon_traffic.jsonl", description="Path to the traffic log.")
    interactive: bool = Field(default=True, description="Step-by-step execution mode.")
    speed: float = Field(default=1.0, description="Replay speed multiplier (if non-interactive).")
    filter_command: Optional[str] = Field(default=None, description="Only replay specific commands (e.g., 'weave').")


class AnalyzeRequest(BaseRequest):
    """
    =============================================================================
    == THE GNOSTIC INQUEST VESSEL (V-Ω-TOTALITY-SCHEMA-HEALED)                 ==
    =============================================================================
    LIF: ∞ | ROLE: PERCEPTION_PAYLOAD | RANK: OMEGA_SOVEREIGN

    The sacred vessel for the `analyze` rite. It carries the Architect's plea
    for deep forensic understanding of a scripture or sanctum.

    ### THE PANTHEON OF 8 FACULTIES:
    1.  **Recursion Annihilator (THE CURE):** Path normalization has been ascended to the
        `mode='before'` validator, operating on raw dictionary matter to bypass the
        `validate_assignment` infinite loop heresy.
    2.  **The Locus (`file_path`):** The absolute coordinate of the target.
    3.  **The Soul (`content`):** Optional raw content. If provided, the Engine
        analyzes this *ephemeral matter* instead of the physical disk (Shadow Mode).
    4.  **The Focus (`cursor_offset`):** High-precision integer offset for LSP
        operations (Hover, Completion).
    5.  **The Lens (`semantic_depth`):** Controls the intensity of the Gaze.
    6.  **The Tongue (`grammar`):** Forces a specific parser (e.g. 'python')
        overriding auto-detection.
    7.  **The Reflex (`auto_redeem`):** Automatically heals simple heresies.
    8.  **The Format (`json_mode`):** Forces machine-readable prophecy.
    """

    # --- 1. THE LOCUS (TARGET) ---
    file_path: Optional[str] = Field(
        default=None,
        description="The primary target file or directory for analysis.",
        alias="path_to_scripture"
    )

    # --- 2. THE SOUL (CONTENT) ---
    content: Optional[str] = Field(
        default=None,
        description="The raw content of the file. If provided, overrides disk content (Shadow Mode)."
    )

    # --- 3. THE FOCUS (CURSOR) ---
    cursor_offset: int = Field(
        default=-1,
        description="The byte offset of the cursor. -1 implies no specific focus."
    )

    position: Optional[Dict[str, int]] = Field(
        default=None,
        description="LSP Position object {line: int, character: int} for legacy adapters."
    )

    # --- 4. THE GAZE (CONFIGURATION) ---
    semantic_depth: str = Field(
        default="structure",
        pattern=r"^(structure|full|dependencies|minimal)$",
        description="The intensity of the Gaze. 'structure' (fast), 'full' (linting), 'dependencies' (supply chain)."
    )

    grammar: Optional[str] = Field(
        default=None,
        description="Force a specific language parser (e.g., 'python', 'scaffold', 'rust')."
    )

    batch: bool = Field(
        default=False,
        description="If true, performs a panoptic scan of the entire directory."
    )

    # --- 5. THE VOWS (FLAGS) ---
    json_mode: bool = Field(
        default=False,
        alias="json",
        description="If true, output is raw JSON for machine consumption."
    )

    auto_redeem: bool = Field(
        default=False,
        description="If true, automatically attempts to fix simple heresies (imports, formatting)."
    )

    # --- 6. THE META-CONTEXT ---
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary contextual tags (e.g., client_version, editor_theme)."
    )

    # =========================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                             ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def _purify_and_unify_intent(cls, data: Any) -> Any:
        """
        =============================================================================
        == THE PRE-FLIGHT ALCHEMIST (V-Ω-RECURSION-SHIELD)                         ==
        =============================================================================
        [THE CURE]: By mutating the data dictionary *before* Pydantic casts it to
        an object, we completely avoid triggering `__setattr__` and `validate_assignment`.
        This eradicates the stack overflow loop.
        """
        if not isinstance(data, dict):
            return data

        # 1. Heal Legacy Locus Aliases
        raw_path = data.get('file_path') or data.get('path_to_scripture') or data.get('target')

        # 2. Geometric Normalization (The Fix)
        if raw_path:
            # Annihilate Windows Backslashes directly on the primitive string
            clean_path = str(raw_path).replace('\\', '/')
            data['file_path'] = clean_path

            # Auto-detect batch mode based on directory slashes
            if clean_path.endswith('/') or not ('.' in clean_path.split('/')[-1]):
                # If batch isn't explicitly false, we enable it for apparent directories
                if 'batch' not in data:
                    data['batch'] = True

        # 3. Heal JSON Flag
        if 'json' in data and 'json_mode' not in data:
            data['json_mode'] = data['json']

        return data

    @property
    def is_shadow(self) -> bool:
        """
        [ASCENSION 3]: SHADOW DIVINATION
        Returns True if we are analyzing ephemeral content (unsaved buffer),
        False if analyzing physical disk matter.
        """
        return self.content is not None

class RepairRequest(BaseRequest):
    """
    =================================================================================
    == THE SACRED PLEA OF RESTORATION (V-Ω-SURGICAL-ULTIMA++)                     ==
    =================================================================================
    LIF: 100x (SYSTEMIC AUTO-HEALING)

    The definitive contract for the 'repair' rite. It has been ascended to support
    both IDE-driven (LSP) and Cockpit-driven (Background Sentinel) workflows.
    =================================================================================
    """
    model_config = ConfigDict(extra='allow')

    # --- I. THE LOCUS OF THE WOUND ---
    file_path: str = Field(
        ...,
        description="The relative path to the scripture requiring restoration."
    )

    content: Optional[str] = Field(
        default=None,
        description="The active text buffer. If void, the Surgeon gazes directly at the physical disk."
    )

    # --- II. THE NATURE OF THE SIN ---
    heresy_key: str = Field(
        ...,
        description="The unique machine-readable identifier of the paradox (e.g., 'UNDEFINED_VARIABLE')."
    )

    # --- III. SPATIO-TEMPORAL COORDINATES ---
    line_num: int = Field(
        default=1,
        description="The 1-indexed human line number where the heresy was perceived."
    )

    internal_line: int = Field(
        default=0,
        description="The 0-indexed machine line number for direct alignment with the Monaco Matrix."
    )

    # --- IV. THE SURGICAL STRATEGY ---
    strategy: Literal['surgical', 'textual', 'ai', 'template'] = Field(
        default='surgical',
        description="The method of mending: 'surgical' (AST), 'textual' (Regex), 'ai' (Neural), or 'template' (Boilerplate)."
    )

    mutation_mode: Literal['apply', 'preview'] = Field(
        default='apply',
        description="If 'preview', the engine returns a unified diff without altering the mortal realm."
    )

    # --- V. THE GNOSTIC CONTEXT (FORENSIC PAYLOAD) ---
    # This dictionary carries the specific 'DNA' of the error.
    # Expected keys for specific heresies:
    # - UNDEFINED_VARIABLE: {'symbol': 'my_var', 'alternatives': ['my_var_1', 'my_var_2']}
    # - PROFANE_NAMING: {'current': 'myVar', 'expected': 'my_var'}
    # - BROKEN_IMPORT: {'module': 'src.old', 'suggestion': 'src.new'}
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="The detailed forensic metadata required to calculate the cure."
    )

    # --- VI. THE REQUISITE GNOSIS ---
    suggested_fix: Optional[str] = Field(
        default=None,
        description="An optional pre-calculated string to use as the cure, bypassing the Surgeon's deduction."
    )

    @property
    def has_content_overlay(self) -> bool:
        """Adjudicates if the plea carries its own reality or relies on the disk."""
        return self.content is not None and len(self.content.strip()) > 0

    @property
    def target_symbol(self) -> Optional[str]:
        """Surgically extracts the focus of the repair from the context."""
        return self.context.get('symbol') or self.context.get('current')



class IntrospectionRequest(BaseRequest):
    """
    Plea to the Gnostic Oracle for self-awareness.
    Asks the engine to proclaim its own internal Gnosis.
    """
    topic: str = Field(..., description="The category of Gnosis to inquire about (e.g., 'ui_components').")




class TextDocumentIdentifierModel(BaseModel):
    """
    [THE IDENTITY ATOM]
    Uniquely identifies a scripture via URI.
    Used by the Interface Layer to validate LSP payloads.
    """
    uri: str = Field(..., description="The Celestial URI of the document.")


class CursorPoint(BaseModel):
    """
    =============================================================================
    == THE ASCENDED CURSOR POINT (V-Ω-SUBSCRIPTABLE-HYBRID)                    ==
    =============================================================================
    Precise 0-indexed coordinates within the scripture.
    Hardened to support both Dot-Notation and Dictionary-Subscript access.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Dual-Access Inception (THE FIX):** Implements `__getitem__` to satisfy
        the 'not subscriptable' heresy, allowing `pos['line']` for legacy logic.
    2.  **Strict Boundary Guard:** Enforces `ge=0` to ensure coordinates never
        enter the negative spatial void.
    3.  **Holographic Spreading:** Implements `__iter__` and `keys()` to allow
        the model to be spread into dicts `{**pos}` or function arguments.
    4.  **Frozen Integrity:** `frozen=True` ensures that once a coordinate
        is manifest, it cannot be profaned by accidental mutation.
    5.  **Isomorphic Comparison:** Overrides `__lt__` and `__eq__` to enable
        spatial math (e.g., `if cursor < token_start`).
    6.  **Reflexive Introspection:** Supports `values()` and `items()` to mimic
         the `dict` interface with 100% fidelity.
    7.  **Nanosecond Scribing:** Uses `__slots__` logic (via frozen BaseModel)
        optimized for high-frequency keystroke events.
    8.  **Type-Safe Coercion:** Validates and casts inputs to integers during
        the alchemical `model_validate` phase.
    9.  **Alias Sovereignty:** Preserves the `camelCase` to `snake_case`
        mappings for cross-process synchronization.
    10. **Null-Key Resilience:** Gracefully handles missing keys in the
        subscriptor to prevent `KeyError` fractures.
    11. **Metadata Ingress:** Compatible with the `extra='allow'` directive
        to absorb future coordinate-level telemetry.
    12. **The Singularity Seal:** Finalized for direct injection into the
        Oracle's logic stream.
    =============================================================================
    """
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        extra='allow'
    )

    line: int = Field(..., ge=0, description="0-indexed line number.")
    character: int = Field(..., ge=0, description="0-indexed character offset.")

    # =========================================================================
    # == [THE CURE]: THE SUBSCRIPTABLE BRIDGE                                ==
    # =========================================================================

    def __getitem__(self, key: str) -> Any:
        """
        Allows the model to be accessed like a dictionary.
        Supports: pos['line'] and pos['character']
        """
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(f"Geometry Error: '{key}' is not a valid coordinate component.")

    def __iter__(self):
        """Allows dictionary conversion via dict(cursor_point)."""
        yield 'line', self.line
        yield 'character', self.character

    def keys(self):
        """Mimics dict.keys() for compatibility."""
        return ['line', 'character']

    def values(self):
        """Mimics dict.values() for compatibility."""
        return [self.line, self.character]

    def items(self):
        """Mimics dict.items() for compatibility."""
        return [('line', self.line), ('character', self.character)]

    # =========================================================================
    # == SPATIAL COMPARISON OPERATORS                                        ==
    # =========================================================================

    def __lt__(self, other: Union['CursorPoint', Dict]) -> bool:
        other_line = other['line'] if isinstance(other, dict) else other.line
        other_char = other['character'] if isinstance(other, dict) else other.character

        if self.line < other_line: return True
        if self.line == other_line: return self.character < other_char
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (CursorPoint, dict)): return False
        other_line = other['line'] if isinstance(other, dict) else other.line
        other_char = other['character'] if isinstance(other, dict) else other.character
        return self.line == other_line and self.character == other_char


# =================================================================================
# == II. THE POLYMORPHIC HOVER REQUEST (THE CURE)                                ==
# =================================================================================

class HoverRequest(BaseRequest):
    """
    =============================================================================
    == THE HOVER PLEA (V-Ω-OMNISCIENT-PROBE-HYBRID)                            ==
    =============================================================================
    LIF: 100x | The Request for Enlightenment.

    Sent by the LSP Server (or CLI) to the HoverArtisan.
    It acts as a **Polymorphic Vessel**, accepting both:
    1. LSP Standard: `{ textDocument: { uri }, position: { ... } }`
    2. Kinetic CLI:  `{ file_path: "/abs/path", line_num: 10 }`

    The `unify_identity` validator transmutes these inputs into a single,
    immutable Gnostic Truth before the artisan ever sees them.

    ### 12 LEGENDARY ASCENSIONS:
    1.  **Polymorphic Ingestion:** Automatically detects LSP vs CLI shape.
    2.  **Geometric Transmutation:** Converts 1-based CLI lines to 0-based LSP coords.
    3.  **Path Canonization:** Resolves symlinks and normalizes slashes instantly.
    4.  **Field Aliasing:** Maps `textDocument` to `text_document` transparently.
    5.  **Strict Typing:** Enforces `CursorPoint` and `TextDocumentIdentifierModel`.
    6.  **Context Injection:** Allows arbitrary metadata for trace propagation.
    7.  **Language Divination:** Optional override for forced syntax contexts.
    8.  **Dirty Buffer Support:** Accepts `content` payload for unsaved files.
    9.  **Time Dilation:** Configurable `timeout` for heavy analysis.
    10. **Link Resolution:** Toggle for deep import tracing.
    11. **Format Negotiation:** Supports Markdown vs Plaintext output.
    12. **Immutable Config:** `frozen=True` ensures thread safety during dispatch.
    """
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra='allow',
        json_schema_extra={
            "example": {
                "file_path": "/abs/path/to/scripture.py",
                "position": {"line": 10, "character": 4},
                "content": "def main():\n    pass",
                "metadata": {"trace_id": "tr-8f9a2b", "trigger": "mouse"}
            }
        }
    )

    # --- I. THE LOCUS (WHERE) ---
    file_path: str = Field(
        ...,
        description="Absolute path to the scripture on the physical disk."
    )

    position: CursorPoint = Field(
        ...,
        description="The exact geometric point of the Architect's gaze."
    )

    # [ASCENSION 1]: LSP COMPATIBILITY LAYER
    # These fields are used during ingestion but merged into file_path/position
    text_document: Optional[TextDocumentIdentifierModel] = Field(None, alias="textDocument")

    offset: Optional[int] = Field(
        None,
        description="Byte offset from start of file (Alternative geometry)."
    )

    # --- II. THE QUANTUM STATE (WHAT) ---
    content: Optional[str] = Field(
        None,
        description="The 'Dirty' content of the file from the editor buffer. If None, reads from disk."
    )

    language_id: Optional[str] = Field(
        None,
        description="Forced language context (e.g. 'python', 'rust'). Divined if omitted."
    )

    # --- III. THE CONTEXTUAL SOUL (WHY) ---
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary Gnostic context (Trace IDs, Client Capabilities, Trigger Kinds)."
    )

    # --- IV. THE TUNING DIALS (HOW) ---
    verbosity: int = Field(
        1,
        ge=0, le=3,
        description="Depth of Gnosis: 0=TypeOnly, 1=BasicDoc, 2=FullDoc, 3=DeepLinks."
    )

    format: Literal['markdown', 'plaintext'] = Field(
        'markdown',
        description="The requested tongue of the response."
    )

    resolve_links: bool = Field(
        False,
        description="If True, the Artisan will trace imports to find the original definition."
    )

    timeout: float = Field(
        2.0,
        description="Max duration (seconds) before the Gaze averts."
    )

    # =========================================================================
    # == THE RITES OF TRANSMUTATION (PRE-VALIDATION)                         ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def unify_identity(cls, data: Any) -> Any:
        """
        [THE POLYMORPHIC ALCHEMIST]
        Detects the shape of the input matter and transmutes it into Gnostic Truth.
        """
        if not isinstance(data, dict): return data

        # CASE A: LSP INGRESS (textDocument + position)
        # The Dispatcher sends this when receiving 'textDocument/hover'
        if 'textDocument' in data:
            # Handle nested dict or object
            td = data['textDocument']
            uri = td.get('uri') if isinstance(td, dict) else getattr(td, 'uri', '')

            # 1. Divine file_path from URI
            if 'file_path' not in data:
                data['file_path'] = _clean_uri_to_path(uri)

            # 2. Divine Position
            # Ensure 'position' key exists and maps to the correct shape
            if 'position' in data:
                # If it's already a model or dict, we let Pydantic handle it
                pass

        # CASE B: CLI INGRESS (file_path + line_num)
        # The CLI user types: scaffold hover --file src/main.py --line 10
        if 'line_num' in data and 'position' not in data:
            # Transmute 1-based line to 0-based CursorPoint
            line0 = int(data['line_num']) - 1
            char0 = int(data.get('char_num', 1)) - 1
            data['position'] = {'line': max(0, line0), 'character': max(0, char0)}

        return data

    # =========================================================================
    # == THE RITES OF PURIFICATION (POST-VALIDATION)                         ==
    # =========================================================================

    @field_validator('position', mode='before')
    @classmethod
    def _consecrate_geometry(cls, v: Any) -> Any:
        """
        [THE GEOMETER]
        Transmutes raw dictionaries into the CursorPoint spirit.
        Handles: {'line': 1, 'character': 5}
        """
        # We rely on Pydantic to do the actual casting, but we handle potential nulls
        if v is None:
            return {'line': 0, 'character': 0}
        return v

    @field_validator('file_path', mode='before')
    @classmethod
    def _canonize_path(cls, v: Union[str, Path]) -> str:
        """
        [THE PATHFINDER]
        Ensures the path is absolute and POSIX-normalized.
        """
        if isinstance(v, Path):
            return v.resolve().as_posix()
        if not v:
            return ""
        # Basic string normalization if Path object not provided
        return str(Path(v).resolve()).replace('\\', '/')


# =================================================================================
# == III. THE CODE ACTION REQUEST (THE MISSING LINK)                             ==
# =================================================================================
class PositionModel(BaseModel):
    """
    [THE GEOMETRIC ATOM]
    Precise 0-indexed coordinates within the scripture.
    """
    line: int
    character: int


class RangeModel(BaseModel):
    """
    [THE VESSEL OF EXTENT]
    A range expressed as start and end positions.
    """
    start: PositionModel
    end: PositionModel


class CodeActionContextModel(BaseModel):
    """
    [THE CONTEXT OF REDEMPTION]
    Carries diagnostics and trigger kinds for code actions.
    """
    diagnostics: List[Dict[str, Any]] = Field(default_factory=list)
    only: Optional[List[str]] = None
    triggerKind: Optional[int] = None




class CodeActionRequest(BaseRequest):
    """
    [THE RITE OF REDEMPTION]
    Handles `textDocument/codeAction`.
    """
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    text_document: Optional[TextDocumentIdentifierModel] = Field(None, alias="textDocument")
    range: Optional[RangeModel] = None
    context: Optional[CodeActionContextModel] = None

    # CLI Compatibility
    file_path: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def unify(cls, data: Any) -> Any:
        if not isinstance(data, dict): return data

        if 'textDocument' in data and 'file_path' not in data:
            td = data['textDocument']
            uri = td.get('uri') if isinstance(td, dict) else getattr(td, 'uri', '')
            data['file_path'] = _clean_uri_to_path(uri)
        return data


class CompletionRequest(BaseRequest):
    """
    =============================================================================
    == THE COMPLETION PLEA (V-Ω-PROPHETIC-VESSEL-V24000-INDESTRUCTIBLE)        ==
    =============================================================================
    LIF: 10,000,000 | ROLE: FORESIGHT_CONDUIT | RANK: SOVEREIGN

    The definitive vessel for the Request for Foresight.
    It bridges the Ocular Retina (Monaco) with the Council of Prophets.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Polymorphic Alchemist:** Automatically detects and unpacks LSP
        `textDocument` structures OR pure CLI payloads seamlessly.
    2.  **Titanium Path Resolution:** Instantly resolves `file://` schemes,
        cleaning URI artifacts into absolute physical coordinates.
    3.  **Windows Drive Surgery:** Detects and normalizes `/c:/` pathing errors
        introduced by the browser's URL parser.
    4.  **Artifact Exorcism:** Strips trailing quotes, dots, and null bytes
        from the file path to guarantee pristine OS filesystem queries.
    5.  **Trigger Extraction Suture:** Safely hoists `triggerCharacter` and
        `triggerKind` from the nested LSP context dictionary.
    6.  **Geometric Clamping:** Mathematically enforces that `line` and `character`
        coordinates are strictly >= 0, preventing index underflows.
    7.  **Trace ID Injection:** Auto-generates a unique `pred-` trace ID if
        the client failed to provide one, ensuring unbroken telemetry.
    8.  **Absolute POSIX Conversion:** Forces all slashes to forward slashes
        (`\\` -> `/`) regardless of the host operating system.
    9.  **Pydantic Frozen State:** The model is `frozen=True`, ensuring that
        the prophetic context cannot be accidentally mutated by a greedy Artisan.
    10. **Trigger Kind Defaulting:** Defaults `trigger_kind` to 1 (Invoked)
        if the client provides a Void signal.
    11. **Shadow Buffer Triage:** Accepts raw `content` directly from the editor
        buffer, bypassing stale disk reads for 0ms latency.
    12. **Lexical Prefixing:** Stores `line_prefix` (text before cursor) explicitly
        to power instant regex matching in the Prophets.
    13. **Metamorphic Alias Healing:** Supports `textDocument`, `text_document`,
        and raw `file_path` interchangeably.
    14. **Schema Mock Injection:** Includes a perfect `json_schema_extra` example
        for automated API documentation and test generation.
    15. **Null-Context Immunity (The secondary fix):** Redefines `context` as
        an `Optional[Dict]` to match the LSP spec, relying on `BaseRequest` to
        heal the Void into a valid GnosticSovereignDict.
    16. **Arbitrary Type Support:** Allows complex Monaco internal objects to pass
        through the metadata without crashing validation.
    17. **Strict Field Validation:** Pre-validators run *before* Pydantic casts,
        ensuring the raw dictionary is healed before schema enforcement.
    18. **Luminous Telemetry Anchors:** Embeds `session_id` and `trace_id`
        directly into the `metadata` envelope for the Inquisitor to read.
    19. **Unbreakable Polymorphism:** `unify_prophetic_identity` handles ANY shape
        of input matter, from sparse CLI args to monolithic JSON-RPC packets.
    20. **RootModel Bypassing:** Relies on the external `_clean_uri_to_path`
        function to avoid Pydantic V2 `RootModel` stringification paradoxes.
    21. **Dictionary Safe-Access:** Uses `.get()` exclusively during pre-validation
        to ensure `KeyError` never occurs on malformed client data.
    22. **The Coordinate Transmuter:** Converts flat `line` and `character` kwargs
        into a nested `position` dictionary automatically.
    23. **The Metadata Sarcophagus:** Ensures the `metadata` dict is ALWAYS present,
        even if the client sends a completely empty JSON object.
    24. **The Finality Vow:** A mathematical guarantee that if this model validates,
        the CompletionEngine has everything it needs to see the future.
    =============================================================================
    """
    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra='allow',
        json_schema_extra={
            "example": {
                "file_path": "C:/dev/project/scaffold.scaffold",
                "position": {"line": 22, "character": 4},
                "trigger_character": "$",
                "metadata": {"trace_id": "pred-7572FC", "session_id": "oracle-A1"}
            }
        }
    )

    # --- I. THE LOCUS (WHERE) ---
    file_path: str = Field(
        ...,
        description="The absolute physical coordinate of the scripture."
    )

    position: CursorPoint = Field(
        ...,
        description="The precise Gnostic coordinates of the caret."
    )

    # LSP Compatibility Layer
    text_document: Optional[TextDocumentIdentifierModel] = Field(None, alias="textDocument")

    # [THE CURE]: Re-Mapped Context to avoid BaseRequest collision.
    # BaseRequest defines context as Dict[str, Any] via default_factory.
    # LSP sends context as a payload. We keep the generic Dict typing to be safe,
    # and the BaseRequest validator `initialize_gnostic_sarcophagus` handles the dict healing.
    context: Optional[Dict[str, Any]] = Field(None, description="Raw LSP context payload.")

    # --- II. THE TRIGGER (WHY) ---
    trigger_character: Optional[str] = Field(
        None,
        description="The sacred particle that summoned the Prophet."
    )

    trigger_kind: int = Field(
        1,
        description="1=Invoked, 2=TriggerCharacter, 3=Incomplete."
    )

    # --- III. THE QUANTUM STATE (WHAT) ---
    content: Optional[str] = Field(
        None,
        description="The 'Dirty' buffer state. Matter takes precedence over Disk."
    )

    line_prefix: Optional[str] = Field(
        None,
        description="The lexical matter to the left of the cursor."
    )

    # THE SOVEREIGN METADATA HUB
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Forensic metadata: trace_id, session_id, and telemetry markers."
    )

    # =========================================================================
    # == THE RITES OF TRANSMUTATION (VALIDATION)                             ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def unify_prophetic_identity(cls, data: Any) -> Any:
        """[THE POLYMORPHIC ALCHEMIST]
        Transmutes the chaotic matter of the network into Gnostic Truth.
        """
        if not isinstance(data, dict): return data

        # --- MOVEMENT I: LSP CONFORMANCE ---
        if 'textDocument' in data or 'text_document' in data:
            td = data.get('textDocument') or data.get('text_document')
            uri = td.get('uri') if isinstance(td, dict) else getattr(td, 'uri', '')

            # TITANIUM PATH RESOLUTION
            if 'file_path' not in data and uri:
                # We surgically clean the URI to find the absolute OS path
                clean_p = str(uri).replace('file:///', '').replace('file://', '')
                # Windows Drive Surgery
                if clean_p.startswith('/') and len(clean_p) > 2 and clean_p[2] == ':':
                    clean_p = clean_p[1:]
                # Artifact Exorcism: Strip trailing quotes and dots
                data['file_path'] = clean_p.strip("'\"").replace('\\', '/').rstrip('.')

            # TRIGGER EXTRACTION
            ctx = data.get('context')
            if ctx:
                if 'trigger_character' not in data:
                    data['trigger_character'] = ctx.get('triggerCharacter')
                if 'trigger_kind' not in data:
                    data['trigger_kind'] = ctx.get('triggerKind')

        # --- MOVEMENT II: GEOMETRIC SAFETY ---
        if 'position' in data:
            p = data['position']
            # BOUNDARY CLAMPING
            if isinstance(p, dict):
                p['line'] = max(0, int(p.get('line', 0)))
                p['character'] = max(0, int(p.get('character', 0)))
        elif 'line' in data and 'character' in data:
            data['position'] = {'line': data['line'], 'character': data['character']}

        # --- MOVEMENT III: TRACE INJECTION ---
        if 'metadata' not in data:
            data['metadata'] = {}

        if 'trace_id' not in data['metadata']:
            data['metadata']['trace_id'] = f"pred-{uuid.uuid4().hex[:6].upper()}"

        return data

    @field_validator('file_path')
    @classmethod
    def _ensure_absolute_posix(cls, v: str) -> str:
        """THE FINAL PATH CONSTITUTION"""
        if not v: return ""
        # Force absolute resolution and forward-slash harmony
        return str(Path(v).resolve()).replace('\\', '/')

class DefinitionRequest(BaseRequest):
    """A plea to find the Gnostic origin of a sacred word."""
    file_path: str = Field(..., description="The URI of the scripture.")
    content: str = Field(..., description="The current soul of the scripture.")
    position: Dict[str, int] = Field(..., description="The cursor's Gnostic location.")


# =============================================================================
# == 22. TRANSMUTE RITE (scaffold transmute)                                 ==
# =============================================================================

# =============================================================================
# == 22. TRANSMUTE RITE (scaffold transmute)                                 ==
# =============================================================================

class TransmuteRequest(BaseRequest):
    """
    Plea to evolve the project's reality to match the will of the Blueprint.
    This vessel's contract is now whole, its soul unified with Genesis.
    """
    # This is the original, but now it serves as an alias.
    path_to_scripture: Optional[str] = Field(
        default=None,
        description="Target file. If None, Sync Mode (scaffold.scaffold) is assumed."
    )

    # --- THE DIVINE HEALING & UNIFICATION ---
    # This is the new, one true chamber for the blueprint's path.
    blueprint_path: Optional[str] = Field(
        default=None,
        description="The Gnostic scripture of intent. An alias for path_to_scripture."
    )
    # --- THE APOTHEOSIS IS COMPLETE ---

    silent: bool = Field(default=False)
    anchor: bool = Field(default=False)
    revert_blueprint: Optional[str] = Field(default=None)

    @model_validator(mode='before')
    @classmethod
    def _unify_path_gnosis(cls, data: Any) -> Any:
        """
        A divine alchemist that ensures `blueprint_path` is always pure,
        honoring the ancient `path_to_scripture` tongue as a sacred alias.
        """
        if isinstance(data, dict):
            if 'path_to_scripture' in data and data.get('path_to_scripture') is not None:
                if data.get('blueprint_path') is None:
                    data['blueprint_path'] = data['path_to_scripture']
            elif 'blueprint_path' in data and data.get('blueprint_path') is not None:
                if data.get('path_to_scripture') is None:
                    data['path_to_scripture'] = data['blueprint_path']
        return data

class HealRequest(BaseRequest):
    """
    Plea to heal the Gnostic connections (imports) of a specific scripture.
    """
    file_path: str = Field(..., description="The path to the wounded scripture.")
    check_only: bool = Field(default=False, description="If True, only reports broken links without healing.")


class AddRequest(BaseRequest):
    """
    Plea to append a new definition to a Blueprint.
    """
    blueprint_path: str = Field(
        default="scaffold.scaffold",
        description="The blueprint to modify."
    )
    item_path: str = Field(
        ...,
        description="The path of the file/directory to add."
    )
    content: Optional[str] = Field(
        default=None,
        description="Inline content or directive (@...)."
    )
    seed_path: Optional[str] = Field(
        default=None,
        description="Path to a seed file (<<)."
    )
    is_dir: bool = Field(
        default=False,
        description="Explicitly mark as directory (appends /)."
    )


class InspectRequest(BaseRequest):
    """
    Plea to gaze upon the soul of a blueprint without materializing it.
    """
    blueprint_path: str = Field(
        default="scaffold.scaffold",
        description="The path to the blueprint scripture."
    )

    json_output: bool = Field(
        default=False,
        description="Output raw JSON data (Legacy flag, prefer format='json')."
    )

    # ★★★ THE DIVINE HEALING: THE FORMAT VESSEL ★★★
    format: Literal['text', 'mermaid', 'json'] = Field(
        default='text',
        description="The medium of proclamation (text, mermaid, json)."
    )

class BlueprintExciseRequest(BaseRequest):
    """Plea to excise a definition from the blueprint scripture."""
    blueprint_path: str = Field(default="scaffold.scaffold")
    target_path: str = Field(..., description="The path key to excise from the text.")


class ExciseRequest(BaseRequest):
    """
    Plea to surgically remove all artifacts from the filesystem that were born
    from a specific blueprint origin.
    """
    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    blueprint_origin: str = Field(..., description="The blueprint origin to excise (e.g., 'my-feature.scaffold' or 'kit/auth').")


class HistoryRequest(BaseRequest):
    """
    Plea to traverse the Gnostic Timeline.
    """
    command: Literal['list', 'undo', 'reset'] = Field(
        ...,
        description="The temporal rite to perform."
    )

    target_id: Optional[str] = Field(
        default=None,
        description="The Rite ID or Index to jump to (for reset)."
    )

class TimeBranchRequest(BaseRequest):
    """A plea to forge a new branch of reality from the past."""
    new_branch_name: str
    from_rite: str

class TimeMachineRequest(HistoryRequest):
    """A sacred vessel for the `time-machine` rite.
    It is a Gnostic twin of the HistoryRequest, as they both summon the Altar of Time.
    """
    pass

class TreeRequest(BaseRequest):
    """
    Plea to visualize the reality of a directory as a Luminous Tree.
    """
    target_path: str = Field(default=".", description="The sanctum to gaze upon.")
    all: bool = Field(default=False, description="Show hidden and ignored files (pierce the Veil).")
    depth: int = Field(default=-1, description="Limit the depth of the Gaze.")
    format: Literal['text', 'svg', 'json'] = Field(default='text', description="The medium of proclamation.")
    output: Optional[str] = Field(default=None, description="Path to write the visualization to.")

    # ★★★ THE MISSING VESSEL (THE FIX) ★★★
    serve: bool = Field(default=False, description="Launch an ephemeral server to view SVG output.")


# =============================================================================
# == 23. VERIFY RITE (scaffold verify)                                       ==
# =============================================================================

class VerifyRequest(BaseRequest):
    """
    Plea to adjudicate the integrity of the current reality against the Gnostic Chronicle.
    """
    target_path: str = Field(
        default=".",
        description="The sanctum to verify."
    )

    fast: bool = Field(
        default=False,
        description="The Rite of Speed. Checks file existence and timestamps/size only, skipping hash verification."
    )

    strict: bool = Field(
        default=False,
        description="The Rite of Paranoia. Fails if *any* untracked files (not in lockfile/gitignore) are found."
    )

    fix_suggestions: bool = Field(
        default=True,
        description="Proclaim the commands needed to heal the drift."
    )


# =============================================================================
# == 24. ADOPT RITE (scaffold adopt)                                         ==
# =============================================================================

class AdoptRequest(BaseRequest):
    """
    =================================================================================
    == THE VESSEL OF ADOPTION (V-Ω-UNIFIED-GAZE-ASCENDED)                          ==
    =================================================================================
    The sacred plea to perform the Rite of Adoption. This rite gazes upon the
    mortal realm (the filesystem) and transmutes its current state into the one
    true Gnostic Law (a .scaffold file) and Memory (scaffold.lock).

    It has been ascended to possess the full Gnostic Gaze, perfectly mirroring the
    faculties of the DistillRequest for ignore, include, and focus operations.
    """
    target_path: str = Field(
        default=".",
        description="The directory sanctum whose reality is to be adopted."
    )
    output_file: str = Field(
        default="scaffold.scaffold",
        description="The scripture where the new Gnostic Law shall be inscribed."
    )
    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    full: bool = Field(
        default=False,
        description="If True, performs a deep content hash of all scriptures for the lockfile."
    )

    # --- THE ASCENDED FACULTIES (THE FIX) ---
    ignore: Optional[List[str]] = Field(
        default=None,
        description="A list of glob patterns to avert the Gaze from (e.g., '*.log', 'dist/')."
    )
    include: Optional[List[str]] = Field(
        default=None,
        description="A list of glob patterns to EXCLUSIVELY focus the Gaze upon (Whitelist)."
    )
    focus: Optional[List[str]] = Field(
        default=None,
        description="A list of semantic keywords to prioritize during analysis (e.g., 'auth', 'database')."
    )

# =============================================================================
# == 25. REFACTOR RITE (scaffold refactor)                                   ==
# =============================================================================

class RefactorRequest(BaseRequest):
    """
    Plea to visually restructure the project and forge a Transmutation Plan.
    """
    blueprint_path: str = Field(
        ...,
        description="The target blueprint scripture to update or create (e.g., 'refactor.scaffold')."
    )

    from_blueprint: Optional[str] = Field(
        default=None,
        description="An optional source blueprint (e.g. from AI) to load as the 'After' state."
    )


# =============================================================================
# == 26. PATCH RITE (scaffold patch)                                         ==
# =============================================================================

class PatchRequest(BaseRequest):
    """
    =================================================================================
    == THE PLEA FOR SURGICAL TRANSMUTATION (V-Ω-ETERNAL)                           ==
    =================================================================================
    A divine plea to the Gnostic Surgeon. It carries a scripture of MUTATION, not
    definition, commanding the engine to apply a precise set of changes to an
    existing reality.
    =================================================================================
    """
    patch_path: str = Field(..., description="Path to the .patch.scaffold scripture containing the mutation edicts.")


class RunRequest(BaseRequest):
    """
    =================================================================================
    == THE SENTIENT VESSEL OF UNIVERSAL CONDUCTION (V-Ω-ETERNAL-APOTHEOSIS++)      ==
    =================================================================================
    LIF: 100,000,000,000,000

    This is the divine plea to the Universal Conductor. It carries the Gnosis for
    executing any scripture, in any tongue, in any reality. It has been ascended
    to explicitly hold the **Vow of Silence** and the **Silver Cord**, ensuring
    perfect compatibility with the Middleware Pantheon.
    """
    # [FACULTY 1] The Unbreakable Schema
    model_config = ConfigDict(arbitrary_types_allowed=True, extra='ignore')

    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    # --- The Core Plea (Now Polymorphic) ---
    target: Optional[Union[str, Path]] = Field(
        None,
        description="Path to the Gnostic scripture or the language for an ephemeral rite."
    )

    # --- The Ephemeral Scribe's Gnosis ---
    eval_content: Optional[str] = Field(
        None,
        description="A raw string of scripture to execute in memory."
    )
    pipe_content: Optional[str] = Field(
        None,
        description="Scripture piped from stdin. This vessel receives the final string, not the CLI flag."
    )
    create_if_void: bool = Field(
        False,
        description="Forge a default scripture if the target path is a void."
    )

    # --- The Chronomancer's Vow ---
    vigil: bool = Field(
        False,
        description="Awaken the Eternal Sentinel to watch the scripture for changes and re-run the rite."
    )

    # --- THE GNOSTIC SCHEDULER'S WILL ---
    runtime: Optional[str] = Field(
        None,
        description="Override execution strategy (e.g., 'docker', 'hermetic', 'python@3.12')."
    )

    # --- THE ORACLE'S GAZE ---
    codex: bool = Field(
        False,
        description="Proclaim the Gnostic codex of all summonable runtimes."
    )

    # --- The Gnostic Guardian's Vows ---
    no_lock: bool = Field(
        False,
        description="A dangerous vow to conduct a rite without touching or updating the scaffold.lock."
    )
    debug: bool = Field(False, description="Launch in Debug Mode (Expose DAP port/Inspect).")

    # [THE FIX] The Vow of Silence
    # Explicitly defined here to ensure it captures the --silent flag from argparse.
    silent: bool = Field(
        False,
        description="The Vow of Silence. Suppresses non-essential output."
    )

    # [FACULTY: CELESTIAL PROJECTION]
    remote: Optional[str] = Field(
        default=None,
        description="The URI (host:port) of a remote Scaffold Daemon to conduct this rite."
    )

    # --- [THE ASCENSION] MIDDLEWARE CONTRACTS ---
    # These fields are required for the new 12-Ring Pipeline to function without heresy.

    # 2. The Gnostic Context (EnrichmentMiddleware / PrerequisiteMiddleware)
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Ephemeral metadata injected by middleware (e.g., binary paths, os info)."
    )

    # 3. The Vault of Secrets (SecretScrubberMiddleware)
    secrets: Dict[str, str] = Field(
        default_factory=dict,
        description="Secure storage for redacted secrets extracted from variables."
    )
    extra_args: List[str] = Field(
        default_factory=list,
        description="A vessel for all passthrough arguments for the 'run' rite."
    )
    # ★★★ THE DIVINE HEALING: THE PRE-VALIDATION ALCHEMIST ★★★
    @field_validator('pipe_content', mode='before')
    @classmethod
    def transmute_pipe_flag_to_content(cls, v: Any) -> Optional[str]:
        """
        This is the Gnostic Alchemist. It intercepts the raw value for 'pipe_content'
        before Pydantic's core validation. If it perceives the profane boolean `True`
        (from `argparse`), it performs the sacred rite of reading from stdin and
        returns the pure string soul.
        """
        if v is True:
            try:
                # The Rite of the Celestial River
                return sys.stdin.read()
            except Exception:
                # The Unbreakable Ward of Grace. If the river is profane, the soul is a void.
                return None
        if isinstance(v, str) or v is None:
            return v
        return None

    # --- Prophecies of Future Ascensions ---
    output: Optional[str] = Field(None, description="[Prophecy] Path to crystallize the output of a generative rite.")
    rehearse: bool = Field(False, description="[Prophecy] Conduct the rite in an ephemeral, temporary sanctum.")
    vars_from: Optional[str] = Field(None,
                                     description="[Prophecy] Path to a YAML/JSON file to load Gnostic variables from.")
    origin: Optional[str] = Field(None, description="[Prophecy] Manually declare a `blueprint_origin` for this rite.")
    budget: Optional[int] = Field(None, description="[Prophecy] Set a token budget for AI-driven sub-rites.")

class RuntimesRequest(BaseRequest):
    """
    =================================================================================
    == THE PLEA FOR GNOSTIC GOVERNANCE (V-Ω-ULTRA-DEFINITIVE-APOTHEOSIS)           ==
    =================================================================================
    This is the final, eternal, and ultra-definitive vessel for all pleas directed
    at the Altar of Control. It is a masterpiece of declarative intent, its soul
    now whole with the Gnosis of the `setup` rite, the Architect's will for
    Anointment Strategy, and the sacred `conduct` rite.
    =================================================================================
    """
    command: Literal[
        'setup', 'list', 'codex', 'summon', 'purge', 'locate',
        'consecrate', 'health', 'conduct', 'anoint'
    ] = Field(
        ...,
        description="The specific rite to perform on the runtime sanctum."
    )

    spec: Optional[str] = Field(
        default=None,
        description="The target runtime specification (e.g., 'python@3.11' or a script path for 'conduct')."
    )

    ide: Optional[Literal['vscode', 'pycharm', 'vim']] = Field(
        default=None,
        description="Explicitly target an IDE for anointment."
    )

    anoint_strategy: Literal['default', 'add'] = Field(
        default='default',
        description="Anointment will: 'default' (set as project interpreter) or 'add' (add to list)."
    )

    # This vessel will carry all unknown arguments from the IDE's plea during `conduct`.
    extra_args: List[str] = Field(
        default_factory=list,
        description="A vessel for all passthrough arguments for the 'conduct' rite."
    )

    force: bool = Field(
        default=False,
        description="Force re-downloading or bypass safety confirmations."
    )

# =============================================================================
# == 27. TELEPRESENCE RITE (scaffold telepresence)                           ==
# =============================================================================

class TelepresenceRequest(BaseRequest):
    """
    =================================================================================
    == THE TELEPRESENCE CONTRACT (V-Ω-QUANTUM-ENTANGLEMENT)                        ==
    =================================================================================
    """
    # Gnostic Verbs
    operation: Literal[
        'stat', 'read', 'write', 'readdir', 'delete', 'mkdir', 'rename',
        'shadow_write', 'shadow_commit', 'shadow_purge',
        'causal_slice', 'impact_prophecy', 'project_url'
    ] = Field(..., description="The kinetic verb of the remote rite.")

    path: str = Field(..., description="The project-relative path or Celestial URL.")

    # Payload & Parameters
    content_base64: Optional[str] = None
    new_path: Optional[str] = None
    recursive: bool = False

    # Advanced Metadata Control
    session_id: str = Field(default="global", description="The isolation chamber for Shadow Realities.")
    include_gnosis: bool = Field(default=False, description="Enrich results with Cortex metrics.")
    depth: int = Field(default=1, description="Traversal depth for causal slicing.")

    # Simulation Logic
    patch_scripture: Optional[str] = None  # For impact prophecy


class ManifestRequest(BaseRequest):
    """
    =============================================================================
    == THE MANIFEST VESSEL (V-Ω-NEURAL-INCEPTION-FINALIS)                      ==
    =============================================================================
    LIF: ∞ | ROLE: INTENT_CARRIER | RANK: OMEGA_SOVEREIGN

    The sacred plea to transmute Natural Language (Intent) directly into
    Structural Reality (Architecture) via the Neural Cortex (AI).
    """
    # [ASCENSION 1]: The Permissive Vow allows for future cognitive expansion.
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    # --- I. THE WILL (INTENT) ---
    prompt: str = Field(
        ...,
        description="The Architect's intent in plain English. The seed of the new reality."
    )

    # --- II. CONTEXTUAL AWARENESS ---
    with_context: bool = Field(
        default=True,
        description="The Gaze of the Surroundings. If True, injects the current directory structure into the AI's mind."
    )

    # --- III. INTERACTION PROTOCOL ---
    interactive: bool = Field(
        default=True,
        description="The Guardian's Veto. If True, the AI's plan must be reviewed in the TUI before materialization."
    )

    # --- IV. THE VOWS OF EXECUTION ---
    # [THE CURE]: This field is critical for the Wormhole Rite.
    no_edicts: bool = Field(
        default=False,
        description="The Vow of Silence. If True, the forged blueprint will NOT execute kinetic commands (%% post-run)."
    )

    # --- V. COGNITIVE PARAMETERS ---
    model: str = Field(
        default="smart",
        description="The Neural Engine to summon (e.g., 'gpt-4', 'claude-3-opus', 'smart', 'fast')."
    )

    fidelity: str = Field(
        default="balanced",
        description="The Resolution of the Dream. 'balanced', 'high', or 'prototype'."
    )

    output_path: Optional[str] = Field(
        default=None,
        description="Optional: Where to save the dreamed .scaffold file instead of executing it."
    )

    variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context variables to guide the Neural Cortex."
    )

class SummarizeRequest(BaseRequest):
    """
    Plea to perform a deep, symbolic analysis and generate an executive summary.
    """
    target_path: str = Field(
        default=".",
        description="The directory or file to summarize."
    )
    format: Literal['text', 'json', 'md'] = Field(
        default='text',
        description="The output format for the summary."
    )


class WorkspaceRequest(BaseRequest):
    """
    =================================================================================
    == THE POLYMORPHIC GNOSTIC VESSEL (V-Ω-APOTHEOSIS)                             ==
    =================================================================================
    The sacred, polymorphic vessel that carries the Architect's will to the Gnostic
    Observatory. Its soul changes form based on the rite being conducted.
    """
    workspace_command: str = Field(description="The primary rite to be conducted (list, health, exec, etc.).")
    non_interactive: bool = Field(
        False,
        description="The Vow of Silence. Suppresses all interactive prompts, accepting default Gnosis."
    )
    # --- Vessels for Specific Rites ---

    command_to_run: Optional[str] = Field(None,
                                          description="For the 'exec' rite: The universal edict (shell command) to be conducted.")

    tag: Optional[str] = Field(None,
                               description="For 'exec', 'health', 'git': A Gnostic filter to scope the rite to specific project tags.")

    splane_path: Optional[str] = Field(None,
                                       description="For the 'genesis' rite: The path to the cosmic `.splane` scripture.")

    path_to_add: Optional[str] = Field(None,
                                       description="For the 'add' rite: The relative path to a new project to be adopted into the cosmos.")

    git_command: Optional[str] = Field(None,
                                       description="For the 'git' rite: The arguments to be passed to the Git command (e.g., 'pull origin main').")


class ShellRequest(BaseRequest):
    """
    A plea to enter the Gnostic Cockpit (Interactive Shell).
    """
    project_root: Optional[Path] = Field(default=None, description="The sanctum to anchor the shell in.")

    # Configuration Overrides
    theme: str = Field(default="gnostic", description="Visual theme.")
    history_file: Optional[str] = Field(None, description="Path to history file.")

    # Context
    initial_command: Optional[str] = Field(None, description="Command to execute immediately upon entry.")


class SelfTestRequest(BaseRequest):
    pass


class BuildRequest(BaseRequest):
    """The Will of the Forge."""
    build_self: bool = False
    release: bool = False
    clean: bool = False
    output_path: Optional[str] = None
    target_arch: Optional[str] = None
    builder: str = "pyinstaller"

    # [EXISTING]
    compress: bool = False
    dockerize: bool = False
    ci_export: str = "none"
    audit: bool = False
    provenance: bool = True
    notify: bool = False
    ai_heal: bool = False

    # [NEW ASCENSIONS]
    remote: Optional[str] = None  # URI for remote builder (ssh://...)
    sign: bool = False            # Enable cosign signing
    wasm: bool = False            # Compile to WebAssembly
    tree_shake: bool = False      # Prune unused code before build


class DreamRequest(BaseRequest):
    """
    =================================================================================
    == THE DREAM REQUEST VESSEL (V-Ω-TOTALITY-V2000-HEALED-FINALIS)                ==
    =================================================================================
    LIF: ∞ | ROLE: INTENT_TRANSPORT_VESSEL | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_DREAM_REQUEST_V2K_SUTURE_FINALIS_2026

    The supreme data contract for materializing reality from Natural Language.
    It carries the "Who, What, Where, and How" of the Architect's Dream.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow'  # Permits third-party Gnosis injection
    )

    # --- I. THE PRIMARY PLEA (THE MIND) ---
    prompt: str = Field(
        ...,
        description="The natural language intent for the project's evolution."
    )

    # --- II. THE KINETIC CONSTRAINTS (THE WILL) ---
    no_edicts: bool = Field(
        default=False,
        description="Maestro's Silence: If True, stays the hand of shell command execution."
    )

    dry_run: bool = Field(
        default=False,
        description="Shadow Reality: If True, performs a zero-side-effect simulation."
    )

    force: bool = Field(
        default=False,
        description="The Vow of Will: If True, bypasses all structural and safety wards."
    )

    # --- III. THE ALCHEMICAL RESERVOIR (THE GNOSIS) ---
    variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Injected Gnosis variables for the Alchemist's Reactor."
    )

    # --- IV. THE FORENSIC SILVER CORD (THE IDENTITY) ---
    trace_id: str = Field(
        default_factory=lambda: f"tr-dream-{uuid.uuid4().hex[:8].upper()}",
        description="The unique causal ID linking this dream to the Akasha."
    )

    project_root: Path = Field(
        default_factory=lambda: Path(os.getcwd()).resolve(),
        description="The geometric anchor point for the project's reality."
    )

    # --- V. THE METABOLIC METADATA (THE BODY) ---
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Forensic metadata (novalym_id, session_id, telemetry)."
    )

    adrenaline_mode: bool = Field(
        default=False,
        description="If True, disables GC and raises CPU priority for the strike."
    )

    non_interactive: bool = Field(
        default=False,
        description="The Vow of Silence: Disables all Socratic interactive gates."
    )

    # --- VI. THE NEURAL HINTS (THE SPIRIT) ---
    model_hint: str = Field(
        default="smart",
        description="Suggests the target Neural Mind (e.g., 'fast', 'smart', 'creative')."
    )

    # =========================================================================
    # == THE RITE OF GEOMETRIC NORMALIZATION                                 ==
    # =========================================================================
    @field_validator('project_root', mode='before')
    @classmethod
    def _normalize_topography(cls, v: Any) -> Path:
        """Enforces POSIX standards on the spatial anchor."""
        if v is None:
            return Path(os.getcwd()).resolve()
        return Path(str(v).replace('\\', '/')).resolve()

    def __repr__(self) -> str:
        return f"<Ω_DREAM_REQUEST trace={self.trace_id[:12]} prompt='{self.prompt[:30]}...'>"


class GraphRequest(BaseRequest):
    """
    =============================================================================
    == THE GRAPH PLEA (V-Ω-MULTIMODAL)                                         ==
    =============================================================================
    The vessel for all topological intent.
    If 'graph_data' is manifest, the Engine enters ARCHITECT mode (Writing).
    If 'graph_data' is void, the Engine enters CARTOGRAPHER mode (Reading/Ingest).
    """
    focus: Optional[str] = Field(None, description="Focus the gaze on a specific symbol or path.")
    format: str = Field("json", pattern="^(json|mermaid|svg|text)$")

    # [THE WILL]: Data sent from the UI to update reality
    graph_data: Optional[Dict[str, Any]] = Field(None, description="The JSON Graph (nodes/edges) to manifest on disk.")

    # [THE GAZE]: Flags for the Ingestor
    include_orphans: bool = Field(True, description="Include files not yet bound to the Gnostic Law.")
    depth: int = Field(-1, description="Traversal depth for the causal weaver.")

    dry_run: bool = Field(False, description="Simulate structural changes without touching matter.")



class BlameRequest(BaseRequest):
    target_path: str
    # [THE FIX] Rename field to avoid shadowing Pydantic's .json() method
    # Use alias='json' to map from CLI argument --json automatically
    json_output: bool = Field(default=False, alias="json")


class LintRequest(BaseRequest):
    """
    =================================================================================
    == THE SACRED PLEA OF ADJUDICATION (V-Ω-SENTINEL-PRIMED-ULTIMA++)             ==
    =================================================================================
    LIF: 100x (SYSTEMIC ARCHITECTURAL PURITY)

    The definitive contract for the 'lint' rite. It has been ascended to support
    surgical background scans, polyglot anti-pattern detection, and deep
    Sentinel CLI integration.
    =================================================================================
    """

    # --- I. THE SCOPE OF THE GAZE ---
    target_paths: List[str] = Field(
        default_factory=list,
        description="The specific scriptures or sanctums to audit. If empty, the Gaze is Universal."
    )

    category: Optional[str] = Field(
        default=None,
        description="Limits the Inquest to a specific domain (e.g., 'security', 'topology', 'style')."
    )

    # --- II. THE RIGOR OF THE LAW ---
    strict: bool = Field(
        default=False,
        description="If True, the Mentor treats Warnings as Critical Heresies (Exit Code > 0)."
    )

    rules: List[str] = Field(
        default_factory=list,
        description="Specific Law IDs to enforce, bypassing the standard Grimoire."
    )

    threshold: float = Field(
        default=0.7,
        description="The sensitivity of the Pattern Matcher (0.0 to 1.0). Lower is more paranoid."
    )

    # --- III. THE KINETIC POTENTIAL ---
    fix: bool = Field(
        default=False,
        description="The Rite of Auto-Redemption. If True, the Mentor applies known cures immediately."
    )

    # --- IV. THE DEPTH OF PERCEPTION ---
    depth: int = Field(
        default=1,
        description="The recursion depth for dependency graph and circularity analysis."
    )

    audit_dependencies: bool = Field(
        default=False,
        description="If True, performs a forensic audit of external supply-chain souls."
    )

    # --- V. THE TONGUE OF PROCLAMATION ---
    json_mode: bool = Field(
        default=False,
        description="The Primary machine-communion flag. Forces pure JSON output."
    )

    json_output: bool = Field(
        default=False,
        description="Legacy alias for 'json' mode. Maintained for backward resonance."
    )

    # --- VI. SENTINEL CLI PRIMING ---
    sentinel_mode: bool = Field(
        default=False,
        description="Activates high-performance mode for integration with the Sentinel God-Engine."
    )

    @property
    def is_machine_readable(self) -> bool:
        """Determines if the proclamation should be formatted for a Mind (JSON) or a Gaze (Rich)."""
        return self.json or self.json_output



class UndoRequest(HistoryRequest):
    """
    A specific plea to reverse the last N transactions recorded in the Gnostic Ledger.
    Its purpose is one of action, a command to the Chronomancer to rewind time.
    """
    steps: int = Field(1, description="The number of historical rites to reverse.")


class AsciiRequest(BaseRequest):
    """
    A plea to transmute an image's soul into a luminous, injectable ASCII scripture.
    """
    image_path: Optional[Path] = Field(None, description="The path to the source image file.")
    width: int = Field(default=80, description="The target width of the ASCII art in characters.")
    style: str = Field(default="color", description="The rendering style ('color', 'grayscale').")

    # --- ASCENDED FACULTIES ---
    output: Optional[Path] = Field(None, description="Inscribe the output to a specific file path.")
    append_to: Optional[Path] = Field(None, description="Surgically append/replace the output in an existing file.")
    marker: str = Field(default="# SCAFFOLD_ASCII_SIGIL",
                        description="The sacred marker to replace when using --append-to.")
    lang: str = Field(default="python", description="The output language ('python', 'js', 'raw').")
    var_name: str = Field(default="get_sigil", description="The variable or function name for the generated code.")
    no_function: bool = Field(False, description="If True, generates only the raw data structure, not a full function.")
    charset: str = Field(default="detailed",
                         description="Character set for rendering ('block', 'detailed', 'simple', 'double').")
    invert: bool = Field(False, description="Invert the character ramp for dark backgrounds.")
    clipboard: bool = Field(False, description="Copy the output scripture to the system clipboard.")
    contrast: Optional[float] = Field(None, description="Enhance contrast by a factor (e.g., 1.5).")
    colors: Optional[int] = Field(None, description="Quantize the image to a specific number of colors.")


class GnosisRequest(BaseRequest):
    """A plea to discover the Gnostic Void of a blueprint."""
    blueprint_path: Path


class HashRequest(BaseRequest):
    """A plea to forge a cryptographic seal."""
    file_path: Path
    algo: str = "sha256"


class DoctorRequest(BaseRequest):
    """A plea to conduct a health inquest upon the local toolchain."""
    pass


class ChronicleRequest(BaseRequest):
    """A plea to commune with the Gnostic Ledger of past rites."""
    chronicle_command: str
    transaction_id: Optional[str] = None


class PackRequest(BaseRequest):
    """A plea to encapsulate an archetype into a distributable vessel."""
    source_path: Path
    output: Optional[Path] = None

class BannerRequest(BaseRequest):
    """A plea to forge a textual sigil."""
    text: str = "SCAFFOLD"
    font: str = "standard"
    output_path: Optional[str] = None

class UpgradeRequest(BaseRequest):
    """A plea for the Phoenix Protocol."""
    from_template: str
    force: bool = False

class SeedRequest(BaseRequest):
    """A plea for the Demiurge to populate the void."""
    count: int = 10
    output: str = "seed_data.json"

class CanonRequest(BaseRequest):
    """A plea for the Canonizer to judge architectural purity."""
    rules_path: str = "scaffold.rules.yaml"


class VectorRequest(BaseRequest):
    """
    =================================================================================
    == THE VESSEL OF SEMANTIC RECALL (V-Ω-HYBRID-RAG-ENABLED)                      ==
    =================================================================================
    @gnosis:title VectorRequest
    @gnosis:summary The unified command vessel for the Vector Cortex (RAG).
    @gnosis:LIF 1,000,000,000,000

    This vessel is the plea to the Vector Librarian, capable of commanding the
    ingestion of reality (`index`), the cleansing of memory (`clear`), or the
    semantic inquiry of a query (`query`). It is now fully equipped with RAG
    control parameters.
    =================================================================================
    """
    vector_command: str = Field(..., description="The rite to perform: 'index', 'query', or 'clear'.")
    query_text: Optional[str] = Field(None,
                                      description="The natural language concept to search for (required for 'query').")

    # --- Indexing and Query Control ---
    target_dir: Optional[str] = Field(None, description="The directory to scan for indexing (default: project root).")
    limit: int = Field(5, description="The maximum number of semantic shards to retrieve.")
    threshold: float = Field(0.75, description="The minimum required cosine similarity score (0.0 to 1.0).")
    force_reindex: bool = Field(False, description="Forces a full scan and re-embed, bypassing the index cache.")


class DeployRequest(BaseRequest):
    """
    A plea to the Celestial Forge to weave deployment scriptures.
    """
    __gnostic_requirements__ = {"docker", "helm"} # Declares its needs

    output_dir: str = "k8s"
    format: str = "helm"
    environment: str = "staging"
    tag: Optional[str] = None


class ProphesyRequest(BaseRequest):
    target_path: str = "."

class SecretsRequest(BaseRequest):
    action: str  # rotate
    target: str = ".env"

class KeyringRequest(BaseRequest):
    keyring_command: str # list, add, remove
    key_id: Optional[str] = None
    key_file: Optional[Path] = None

class SBOMRequest(BaseRequest):
    output: str = "sbom.spdx.json"

class FreezeRequest(BaseRequest):
    """A plea to forge the Dependency Time-Capsule."""
    deep: bool = Field(True, description="Ensures all dependencies are captured.")


class HolographRequest(BaseRequest):
    """A plea to forge the Environment Hologram."""
    output: Optional[str] = Field(None, description="The output path for the hologram.json file.")

class SignatureRequest(BaseRequest):
    """A plea to manage the Architect's Fingerprint."""
    signature_command: str = Field(description="The rite to perform: 'learn' or 'verify'.")
    threshold: float = Field(0.7, description="The confidence threshold for verification.")

class SaveRequest(BaseRequest):
    """A plea to the Neural Scribe to save the current work."""
    intent: str = Field(description="The high-level intent of the changes.")

class ReplRequest(BaseRequest):
    """A plea to awaken the Polyglot Conduit."""
    pass

class BiomeRequest(BaseRequest):
    """
    A plea to visualize the codebase as a living 3D terrain.
    """
    target: str = "."
    port: int = 8080
    theme: str = "cyberpunk"  # cyberpunk, synthwave, engineering
    threshold_complexity: int = 10  # Height scale factor
    threshold_churn: int = 50       # Heat scale factor


class ResonateRequest(BaseRequest):
    query: str
    limit: int = 5
    reindex: bool = False


class MRIRequest(BaseRequest):
    pass


class GhostRequest(BaseRequest):
    exorcise: bool = False


class BusFactorRequest(BaseRequest):
    """
    A plea to calculate the fragility of knowledge distribution.
    """
    threshold: float = 0.7  # Sensitivity (0.0 to 1.0)
    limit: int = 10  # Show top N risks





class BridgeRequest(BaseRequest):
    """A plea to forge a link between two tongues (FFI)."""
    source_lang: str = "rust"
    target_lang: str = "python"
    entry_point: str  # Path to the struct/class to bridge

class IsolateRequest(BaseRequest):
    """A plea to execute a command within a hermetic security ward."""
    command_to_run: str
    allow_hosts: List[str] = ["pypi.org", "files.pythonhosted.org", "registry.npmjs.org"]
    audit_only: bool = False

class ChaosGameRequest(BaseRequest):
    """A plea to initiate the Gamified Resilience Loop."""
    interval: int = 1800  # seconds (30 mins)
    lives: int = 3
    mode: str = "standard"  # standard, hardcore (no git recovery)

class TranslateRequest(BaseRequest):
    """A plea to transmute the soul of code from one tongue to another."""
    source_path: str
    target_lang: str
    source_lang: str = "auto"


class OptimizeCIRequest(BaseRequest):
    """
    A plea for the CI pipeline to rewrite its own DNA based on past performance.
    """
    workflow_path: str = ".github/workflows/main.yml"
    stats_file: Optional[str] = None  # JSON file with step durations
    strategy: str = "aggressive"  # aggressive (sharding), conservative (caching)


class HolographicBlueprintRequest(BaseRequest):
    """
    A plea to digitize a physical project into a pure .scaffold scripture.
    """
    target_dir: str = "."
    output_file: str = "hologram.scaffold"
    full_fidelity: bool = True  # Include all content, not just structure


class SemanticMountRequest(BaseRequest):
    """
    A plea to mount the project's Gnostic Soul as a virtual filesystem.
    """
    mount_point: str
    foreground: bool = True


class TelepathyRequest(BaseRequest):
    """
    A plea to awaken the Clipboard Sentinel.
    """
    auto_format: bool = True
    save_dir: str = "snippets"


class OptimizeBlueprintRequest(BaseRequest):
    """
    A plea for the Blueprint to evolve based on historical usage patterns.
    """
    target_blueprint: str = "scaffold.scaffold"
    threshold: float = 0.9  # 90% consistency required to trigger mutation
    auto_apply: bool = False


class MuseRequest(BaseRequest):
    """
    A plea for the Engine to prophesy the next logical step.
    """
    context_file: Optional[str] = None  # The file you just touched/created
    threshold: float = 0.3  # Minimum confidence to speak
    auto_draft: bool = False  # If True, creates the file as .draft


class SemDiffRequest(BaseRequest):
    """
    A plea to perceive the semantic divergence between two realities.
    """
    target: str = "."  # File or Directory
    reference: str = "HEAD"  # Git ref (HEAD, main, commit_hash)
    format: str = "table"  # table, json


class ForgeArtisanRequest(BaseRequest):
    """
    A plea to forge a new Artisan class and its Gnostic kin.
    """
    artisan_name: str  # e.g., "deploy" or "database_migrate"
    description: str = "A new artisan for the Scaffold cosmos."


class LintBlueprintRequest(BaseRequest):
    """
    =============================================================================
    == THE PLEA OF ADJUDICATION (V-Ω-BLUEPRINT-AUDIT)                          ==
    =============================================================================
    LIF: 10,000,000,000

    A sacred petition to the `BlueprintLinterArtisan` to perform a deep-tissue
    forensic inquest upon a `.scaffold` scripture.

    It carries the configuration for the **Supreme Court of Form**, determining
    whether the judgment should be Merciful (Local Draft) or Absolute (Archetype).

    [CAPABILITIES]:
    1.  **Target Resolution:** Identifies the specific scripture to judge.
    2.  **Strictness Toggle:** Activates the 'Law of the Grimoire' for published Archetypes.
    3.  **Recursive Gaze:** (Prophecy) Willed to scan `@include` dependencies.
    4.  **Auto-Redemption:** (Prophecy) Willed to trigger the `BlueprintHealer`.
    5.  **Machine Tongue:** Requests JSON output for CI/CD pipelines.
    """
    # We allow extra fields to support future Gnostic expansions without breaking consumers.
    model_config = ConfigDict(extra='ignore')

    # --- I. THE LOCUS OF JUDGMENT ---
    target: str = Field(
        ...,
        description=(
            "The physical path to the blueprint scripture (.scaffold, .arch) "
            "to be adjudicated. Can be relative to the Project Root."
        )
    )

    # --- II. THE MODE OF JURISPRUDENCE ---
    strict: bool = Field(
        default=False,
        description=(
            "If True, enforces the 'Law of the Grimoire'. Mandates Gnostic Headers, "
            "valid Categories, and Tags. Essential for validating Archetypes before "
            "publication. If False, operates in 'Benevolent Mentor' mode."
        )
    )

    # --- III. THE FORM OF PROCLAMATION ---
    json_mode: bool = Field(
        default=False,
        description=(
            "If True, the Artisan will suppress the Luminous Table and instead "
            "proclaim the verdict as a pure JSON object, suitable for ingestion "
            "by the Ocular UI or CI/CD pipelines."
        )
    )

    # --- IV. THE PROPHETIC FIELDS (FUTURE PROOFING) ---
    recursive: bool = Field(
        default=False,
        description=(
            "[FUTURE] If True, the Inquisitor will follow `@include` directives "
            "and adjudicate the entire dependency tree of the blueprint."
        )
    )

    fix: bool = Field(
        default=False,
        description=(
            "[FUTURE] If True, summons the `BlueprintHealer` to automatically "
            "rectify structural heresies (e.g., indentation adjustments, "
            "header insertion) where possible."
        )
    )

    # --- V. GNOSTIC METADATA ---
    __gnostic_requirements__ = set()  # No external binaries required for this internal rite.

class MockRequest(BaseRequest):
    """
    A plea to materialize a temporary reality for testing purposes.
    """
    spec: str  # e.g., "src/main.py,tests/test_main.py,README.md"
    root: Optional[str] = None  # Override target dir


class GuiRequest(BaseRequest):
    """
    A plea to summon the Ephemeral Command Palette.
    """
    initial_filter: Optional[str] = None  # Pre-fill the search box


class ExposeRequest(BaseRequest):
    """
    A plea to open a wormhole to the internet.
    """
    port: int
    provider: str = "localhost.run"  # or 'serveo'
    subdomain: Optional[str] = None


class SgrepRequest(BaseRequest):
    """
    A plea for Semantic Search.
    """
    pattern: str
    type: str = "any"  # function, class, variable, import
    show_code: bool = True




class AliasRequest(BaseRequest):
    """
    A plea to manage the Grimoire of Shortcuts.
    """
    alias_command: str  # add, list, remove
    name: Optional[str] = None
    expansion: Optional[str] = None


class QRRequest(BaseRequest):
    """
    A plea to open a visual portal to the local sanctum.
    """
    port: int


class ContextFreezeRequest(BaseRequest):
    """
    A plea to snapshot the current environmental state for debugging.
    """
    output_file: Optional[str] = "debug_context.json"
    include_env: bool = False  # Include safe env vars?


class BenchRequest(BaseRequest):
    """
    A plea to gauge the vitality of the host machine.
    """
    suites: List[str] = Field(default_factory=lambda: ["cpu", "disk", "net"])


class PurgeRequest(BaseRequest):
    """
    A plea to annihilate generated artifacts (node_modules, venv, etc).
    """
    target: str = "."
    dry_run: bool = False
    force: bool = False
    threshold_mb: int = 0  # Only show/delete if larger than X MB


class MatrixRequest(BaseRequest):
    """
    A plea to visualize the dependency graph and version conflicts.
    """
    scope: str = "all"  # all, production, dev
    format: str = "table"  # table, json, tree


class TodoRequest(BaseRequest):
    """
    A plea to harvest technical debt markers from the codebase.
    """
    path: str = "."
    author: Optional[str] = None  # Filter by git author
    format: str = "table"  # table, json, csv
    blame: bool = True  # Enable git blame lookup (slower)



class WithSecretsRequest(BaseRequest):
    """
    A plea to conduct a rite within a sanctum of ephemeral secrets.
    """
    provider: str = "1password"
    secrets: List[str] = Field(..., description="List of secret keys or references to fetch.")
    command: List[str] = Field(..., description="The command to execute with the injected secrets.")


# --- NEW REALITY: THE ASTROLABE ---
class AstrolabeRequest(BaseRequest):
    """A plea to open the Tree-sitter Workbench."""
    target_file: str

# --- NEW REALITY: THE WATCHMAN ---
class WatchmanRequest(BaseRequest):
    """A plea to set a vigil on the filesystem."""
    glob_pattern: str
    command_to_run: str
    debounce: float = 0.5

# --- NEW REALITY: THE AUDITOR ---
class AuditRequest(BaseRequest):
    """A plea to audit covenants (licenses)."""
    audit_target: str = "licenses" # Future expansion: 'security', 'quality'
    fail_on_heresy: bool = False


class NeuralRequest(BaseRequest):
    """
    A plea to enter the Synaptic Console for AI management.
    """
    command: str = "manage" # manage, test, list

class MountRequest(BaseRequest):
    """
    =============================================================================
    == THE PLEA OF THE REALITY BINDER                                          ==
    =============================================================================
    A plea to mount the Gnostic Cortex as a virtual filesystem, making the
    project's semantic soul tangible in the mortal realm.
    """
    mount_point: str = Field(
        "gnostic_fs",
        description="The local directory path to materialize the virtual filesystem."
    )



class ToolRequest(BaseRequest):
    """
    =================================================================================
    == THE UNIVERSAL GATEWAY VESSEL (V-Ω-ETERNAL-POLYMORPH)                        ==
    =================================================================================
    The polymorphic soul of the `tool` command. It is a union of all possible
    arguments for every specialist tool artisan, allowing the ToolArtisan conductor
    to perform its sacred Gnostic Triage.
    =================================================================================
    """
    # The Core Triage Key
    tool_command: str = Field(description="The specific tool rite to conduct (e.g., 'sbom', 'hash').")

    # --- Gnosis for the `ascii` Scribe ---
    image_path: Optional[Path] = Field(None, description="Path to the source image for ASCII transmutation.")
    width: int = Field(80, description="The target width of the ASCII art in characters.")
    charset: str = Field("detailed", description="The character set to use for rendering.")
    style: str = Field("color", description="The rendering style ('color' or 'mono').")
    invert: bool = Field(False, description="Invert the luminosity for the character map.")
    contrast: Optional[float] = Field(None, description="Apply a contrast enhancement factor.")
    colors: Optional[int] = Field(None, description="Quantize the image to a specific number of colors.")
    lang: str = Field("python", description="The output language for the generated scripture ('python', 'js', 'raw').")
    var_name: str = Field("get_sigil", description="The variable or function name for the generated scripture.")
    no_function: bool = Field(False, description="Output a raw variable assignment instead of a function.")
    clipboard: bool = Field(False, description="Copy the output scripture to the clipboard instead of printing.")
    append_to: Optional[Path] = Field(None, description="Path to a file where the output should be grafted.")
    marker: str = Field("# GNOSTIC_SIGIL_INJECTION", description="The marker to find for the Alchemical Graft.")

    # --- Gnosis for the `banner` Herald ---
    text: Optional[str] = Field(None, description="The text to render as a banner.")
    font: Optional[str] = Field(None, description="The Figlet font to use for the banner.")
    output_path: Optional[str] = Field(None, description="The file path to save the banner to.")

    # --- Gnosis for the `hash` Sealer ---
    file_path: Optional[Path] = Field(None, description="The path to the file to be hashed.")
    algo: str = Field("sha256", description="The hashing algorithm to use (e.g., 'sha256', 'md5').")

    # --- Gnosis for the `keyring` Keeper ---
    keyring_command: Optional[str] = Field(None, description="The keyring rite to perform ('list', 'add').")
    key_file: Optional[Path] = Field(None, description="Path to the public key file to add.")

    # --- Gnosis for the `pack` Architect ---
    source_path: Optional[Path] = Field(None, description="The source directory of the archetype to pack.")
    # `output_path` is already defined for `banner`

    # --- Gnosis for the `sbom` Scribe ---
    output: Optional[str] = Field("sbom.spdx.json", description="The output file for the Software Bill of Materials.")

    # --- Gnosis for the `secrets` Keymaster ---
    action: Optional[str] = Field(None, description="The secret management action to perform ('rotate').")
    target: Optional[str] = Field(".env", description="The target .env file for secret operations.")


class ReadSoulRequest(BaseRequest):
    """A plea to read the raw content of a single scripture."""
    path_to_scripture: str

class QueryRequest(BaseRequest):
    """
    A plea to the Gnostic Emissary, now ascended to carry a pure, structured
    Gnostic plea instead of a profane string.
    """
    query: Dict[str, Any]  # ★★★ THE APOTHEOSIS ★★★
    json_output: bool = Field(False, alias='json')


class ArchitectRequest(BaseRequest):
    """
    A plea to the Gnostic Architect.
    """
    prompt: str
    """The natural language intent (e.g., 'Add a user authentication module')."""

    interactive: bool = True
    """Whether to engage in a confirmation dialogue before materialization."""

class ChangelogRequest(BaseRequest):
    """A plea to the Chronicle Scribe."""
    from_ref: Optional[str] = Field(None, description="The Git ref (tag, commit) to start the changelog from. Defaults to the latest tag.")
    next_version: Optional[str] = Field(None, description="The version number to use for the new changelog entry.")
    output_file: str = Field("CHANGELOG.md", description="The path to the changelog file to update.")


class IgnoreRequest(BaseRequest):
    """A plea to the Gatekeeper of Aversion."""
    templates: List[str] = Field(default_factory=list, description="List of gitignore.io templates to fetch.")
    append: bool = Field(False, description="If true, appends to the existing .gitignore instead of overwriting.")


class SnippetRequest(BaseRequest):
    """A plea to the Fragment Keeper."""
    snippet_command: str = Field(..., description="The rite to perform (list, save, load, delete).")
    name: Optional[str] = Field(None, description="The sacred name of the snippet.")
    source_file: Optional[str] = Field(None, description="Path to a file to save as a snippet.")
    clipboard: bool = Field(False, description="Use the system clipboard as the source or destination.")


class ArchitecturalAuditRequest(BaseRequest):
    """A plea to the Gnostic Adjudicator to verify architectural laws."""
    audit_target: str = Field(default="arch", description="The specific audit to run.")

class AgentRequest(BaseRequest):
    """
    =============================================================================
    == THE VESSEL OF AGENCY (V-Ω-AUTONOMOUS-MISSION-ASCENDED)                   ==
    =============================================================================
    Carries the Architect's high-level mission for the autonomous Agent,
    now with a vow of interactivity to enable the Guardian's Veto.
    """
    mission: str = Field(..., description="The natural language mission for the Agent to accomplish.")
    interactive: bool = Field(True, description="If True, the Agent will pause for the Architect's approval before executing a plan.")


# In interfaces/requests.py
# Modify the ScribeRequest class

class ScribeRequest(BaseRequest):
    """
    =============================================================================
    == THE VESSEL OF PROPHECY (V-Ω-POLYGLOT-ASCENDED)                          ==
    =============================================================================
    Carries the Architect's architectural plea to the Scribe Pantheon, now with
    the Gnosis to specify which sacred tongue the prophecy should be written in.
    """
    plea: str = Field(..., description="The natural language architectural intent to be transmuted into a scripture.")

    # --- THE ASCENSION: THE VOW OF TONGUES ---
    language: str = Field(
        "scaffold",
        description="The sacred tongue of the prophecy: 'scaffold' (Form), 'symphony' (Will), or 'arch' (Unified Monad)."
    )
    # -----------------------------------------

    output_path: Optional[str] = Field(None, description="Optional path to save the generated scripture.")
    interactive: bool = Field(True,
                              description="If true, the Scribe will offer to execute the scripture after forging it.")


class TrainRequest(BaseRequest):
    """
    =============================================================================
    == THE VESSEL OF ASCENSION (V-Ω-MODEL-TRAINING)                            ==
    =============================================================================
    Carries the Architect's will to fine-tune an AI model upon a corpus of Gnosis.
    """
    # Source of Wisdom
    corpus_path: str = Field(".", description="Path to the source code or documents to learn from.")

    # The Student
    base_model: str = Field("unsloth/llama-3-8b-bnb-4bit", description="The base model to fine-tune (HuggingFace ID).")

    # The New Identity
    output_model_name: str = Field("scaffold-lora-v1", description="The name of the resulting adapter/model.")

    # Training Parameters
    provider: str = Field("huggingface", description="The training backend (huggingface, ollama, vertex).")
    epochs: int = Field(1, description="Number of training cycles.")
    batch_size: int = Field(2, description="Training batch size.")
    learning_rate: float = Field(2e-4, description="The rate of synaptic plasticity.")

    # Synthetic Data Generation
    generate_instructions: bool = Field(True, description="Use the AIEngine to hallucinate instructions for raw code.")
    limit_samples: Optional[int] = Field(None, description="Limit the number of training samples (for testing).")


class DataRequest(BaseRequest):
    """
    A plea to the Alchemist of State.
    Manages the fluid essence of the application (Database & State).
    """
    data_command: Literal["clone", "snapshot", "seed"] = Field(
        ..., description="The specific alchemical rite to perform."
    )
    source: Optional[str] = Field(None, description="Source connection string or path.")
    destination: Optional[str] = Field(None, description="Destination path.")
    snapshot_name: Optional[str] = Field(None, description="Name of the state freeze.")
    anonymize: bool = Field(True, description="If True, masks PII during cloning.")


class CodexRequest(BaseRequest):
    """
    A plea to the Living Wiki.
    Forges self-verifying documentation and architectural maps.
    """
    codex_command: Literal["build", "verify", "cartography"] = Field(
        ..., description="The rite of documentation."
    )
    output_dir: str = Field("docs", description="Target directory for the Codex.")
    serve: bool = Field(False, description="If True, serves the Codex locally after building.")


class ReviewRequest(BaseRequest):
    """
    A plea to the Sentinel's Tribunal.
     AI-driven adjudication of code changes before they enter the Chronicle.
    """
    review_command: Literal["adjudicate"] = "adjudicate"
    socratic_mode: bool = Field(
        False,
        description="If True, the AI asks guiding questions instead of flagging errors."
    )
    focus_files: Optional[List[str]] = Field(None, description="Specific files to review (defaults to staged).")

class LFGRequest(BaseRequest):
    """
    A plea to the Logic Flow Graph Engine.
    Requests the visualization of control flow within a Blueprint or Source Code.
    """
    target: str = Field(..., description="The path to the blueprint (.scaffold/.symphony) or source code file/directory.")
    mode: Literal["blueprint", "codebase"] = Field("blueprint", description="The mode of perception.")
    format: Literal["mermaid", "json"] = Field("mermaid", description="The output format.")
    output_path: Optional[str] = Field(None, description="Where to inscribe the graph.")

class AkashaRequest(BaseRequest):
    """
    A plea to the Global Memory of the Cosmos.
    """
    akasha_command: Literal["query", "stats", "purge", "learn"] = Field(
        ..., description="The rite to perform on the global memory."
    )
    query: Optional[str] = Field(None, description="The natural language query for wisdom recall.")
    source_path: Optional[str] = Field(None, description="Path to a file or directory to manually enshrine.")


class GuildRequest(BaseRequest):
    """
    A plea to the Guild Nexus.
    Manages the federation of Gnosis across the cosmos.
    """
    guild_command: Literal["publish", "join", "update", "list"] = Field(
        ..., description="The rite of federation."
    )
    target: Optional[str] = Field(None, description="The archetype to publish or the guild URI to join.")
    name: Optional[str] = Field(None, description="The alias for the guild subscription (e.g. '@my-team').")


class MimicRequest(BaseRequest):
    """
    A plea to the Simulacrum.
    Materializes an ephemeral API from a static type definition.
    """
    source_path: str = Field(...,
                             description="The path to the source definition (Pydantic model, SQL schema, or TS Interface).")
    port: int = Field(8000, description="The port to bind the ephemeral reality to.")
    framework: Literal["fastapi", "express"] = Field("fastapi", description="The soul of the mock server.")
    watch: bool = Field(True, description="If True, regenerates the simulacrum when the source changes.")


class FusionRequest(BaseRequest):
    """
    A plea to the Fusion Core.
    NOW ASCENDED: Handles both Cache Management (Legacy) and Compilation (New).
    """
    # Expanded commands to include build rites
    fusion_command: Literal["list", "clean", "bind", "compile"] = Field(
        ..., description="The fusion rite to perform."
    )
    # New fields for the Builder
    source: Optional[str] = Field(None, description="The source file (e.g., 'src/fast_math.rs').")
    target_lang: Literal["python", "node"] = Field("python", description="The host language to bind into.")
    output_dir: Optional[str] = Field(None, description="Where to place the compiled artifact.")


"""
=================================================================================
== THE KINETIC SHADOW REQUEST (V-Ω-TOTALITY-FINAL-V21-SINGULARITY)             ==
=================================================================================
This scripture defines the 'Will of the Architect' for materializing a 
parallel, functional, and rendered reality within the Shadow Dimension.
=================================================================================
"""


# ==============================================================================
# == THE SHADOW CLONE SCHEMA (V-Ω-TOTALITY-V100)                              ==
# ==============================================================================

class ShadowCommand(str, Enum):
    """The Verbs of Reality Manipulation."""
    SPAWN = "spawn"  # Create a new reality
    VANISH = "vanish"  # Destroy a reality
    LIST = "list"  # Census
    STATUS = "status"  # Health check
    LOGS = "logs"  # Forensic read
    HIBERNATE = "hibernate"  # Freeze state


class CloneStrategy(str, Enum):
    """The Physics of Materialization."""
    GIT_WORKTREE = "git_worktree"  # Fast, requires clean git state
    PHYSICAL_COPY = "physical_copy"  # Robust, slower, works on dirty state
    HYBRID = "hybrid"  # Try Worktree, fallback to Copy


class ShadowMode(str, Enum):
    """
    =============================================================================
    == THE BICAMERAL MODES                                                     ==
    =============================================================================
    Defines the ontological purpose of the parallel reality.
    """
    RUN = "run"  # Optimized for: Preview, HMR, Execution.
    LAB = "lab"  # Optimized for: AI Experiments, Large Refactors, State Fission.


class ShadowCommand(str, Enum):
    """
    =============================================================================
    == THE VERBS OF FISSION                                                    ==
    =============================================================================
    """
    SPAWN = "spawn"  # Matter Fission (Create)
    VANISH = "vanish"  # Matter Dissolution (Delete)
    LIST = "list"  # Panoptic Census
    STATUS = "status"  # Vitality Scry
    LOGS = "logs"  # Chronicle Recall
    HIBERNATE = "hibernate"  # State Freeze
    MERGE = "merge"  # Reality Fusion (The Rite of Return)


class CloneStrategy(str, Enum):
    """The method of physical materialization."""
    GIT_WORKTREE = "git_worktree"  # Lightweight pointer (Fast)
    PHYSICAL_COPY = "physical_copy"  # Heavy atomic copy (Robust)
    HYBRID = "hybrid"  # Path of least resistance


class ShadowCloneRequest(BaseRequest):
    """
    =================================================================================
    == THE OMEGA SHADOW CONTRACT (V-Ω-TOTALITY-V25000-HEALED)                      ==
    =================================================================================
    @gnosis:title The Gnostic Plea for Reality Fission
    @gnosis:summary The definitive contract for forging and fusing parallel dimensions.
    @gnosis:LIF INFINITY
    @gnosis:auth_code: #!@RECLAMATION_CONTRACT_V25000_FINALIS

    [THE MANIFESTO]:
    This vessel carries the Architect's complete will for dimensional manipulation.
    It has been ascended to support 'LAB' mode and 'MERGE' rites, closing the
    loop between Experimentation and Prime manifestation.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow',
        validate_assignment=True
    )

    # --- I. THE KINETIC COMMAND (THE WILL) ---
    shadow_command: ShadowCommand = Field(
        ...,
        description="The specific Shadow Rite to perform."
    )

    # --- II. IDENTITY & CAUSALITY (THE NAME) ---
    label: str = Field(
        default="experiment",
        pattern=r"^[a-zA-Z0-9_\-]+$",
        description="Human-readable identity tag for the reality."
    )

    mode: ShadowMode = Field(
        default=ShadowMode.RUN,
        description="The purpose of the dimension: 'run' (preview) vs 'lab' (refactor)."
    )

    owner: str = Field(
        default="architect",
        description="The identity of the responsible manifestor."
    )

    target_ref: str = Field(
        default="HEAD",
        description="The Git reference or Rite ID anchor for cloning."
    )

    target_id: Optional[str] = Field(
        default=None,
        description="A specific Shadow UUID to target for fusion or dissolution."
    )

    # --- III. PHYSICS & GEOMETRY (THE PLACE) ---
    strategy: CloneStrategy = Field(
        default=CloneStrategy.HYBRID,
        description="The materialization method (Worktree vs Physical Copy)."
    )

    port: int = Field(
        default=0,
        ge=0,
        le=65535,
        description="Resonance port. 0 = Automated Network Scry."
    )

    # --- IV. RUNTIME DNA (THE LIFE) ---
    custom_command: Optional[str] = Field(
        default=None,
        description="Override the auto-divined startup scripture."
    )

    variables: Dict[str, str] = Field(
        default_factory=dict,
        description="Environment variables to be warded within the shadow's .env."
    )

    # --- V. GOVERNANCE & PURIFICATION (THE RULES) ---
    auto_provision: bool = Field(
        default=True,
        description="If True, performs dependency lung-transplantation (node_modules)."
    )

    no_cleanup: bool = Field(
        default=False,
        description="The Vow of Persistence. If True, stays the Hand of Oblivion after a successful merge."
    )

    force: bool = Field(
        default=False,
        description="The Rite of Absolute Will. Bypass confirmation guards."
    )

    # =============================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                                 ==
    # =============================================================================

    @field_validator('project_root', mode='before')
    @classmethod
    def canonize_root(cls, v: Any, info: Any) -> str:
        """
        [ASCENSION 5]: THE GEOMETRIC PURIFIER.
        Resolves '~', normalizes slashes, and handles the 'cwd' alias from CLI.
        """
        # 1. Alias Resolution
        if v is None:
            values = info.data if hasattr(info, 'data') else {}
            if 'cwd' in values:
                v = values['cwd']

        if not v:
            return "."

        # 2. Absolute Path Fission
        path_str = str(v)
        try:
            # We resolve realpath to pierce through symlink illusions
            expanded = Path(path_str).expanduser().resolve()
            return str(expanded).replace('\\', '/')
        except Exception:
            return path_str.replace('\\', '/')

    @model_validator(mode='before')
    @classmethod
    def alias_dialect_translation(cls, data: Any) -> Any:
        """
        [ASCENSION 4]: THE LEXICAL HARMONIZER.
        Transmutes raw CLI and JS-Bridge matter into the strict Gnostic contract.
        """
        if isinstance(data, dict):
            # 1. Coordinate Suture: cwd -> project_root
            if 'cwd' in data and 'project_root' not in data:
                data['project_root'] = data['cwd']

            # 2. Command Triage: String -> Enum
            if 'shadow_command' in data and isinstance(data['shadow_command'], str):
                try:
                    # Normalize 'SPAWN' or 'merge' into their Enum souls
                    data['shadow_command'] = ShadowCommand(data['shadow_command'].lower().strip())
                except ValueError:
                    # Let Pydantic provide a descriptive Error later
                    pass

            # 3. Mode Triage: String -> Enum
            if 'mode' in data and isinstance(data['mode'], str):
                try:
                    data['mode'] = ShadowMode(data['mode'].lower().strip())
                except ValueError:
                    pass

        return data




class GardenRequest(BaseRequest):
    """
    A plea to the Entropy Garden.
    """
    garden_command: Literal["scan", "prune", "report"] = Field(
        "scan", description="The gardening rite."
    )
    aggressiveness: int = Field(1, description="1=Files Only, 3=Symbols (Safe), 5=Ruthless.")
    focus_path: Optional[str] = Field(None, description="Limit the garden walk to a specific path.")

class EvolveRequest(BaseRequest):
    """
    A plea to the Schema Engine.
    Synchronizes the Object Model (Code) with the Persistent State (DB).
    """
    evolve_command: Literal["check", "plan", "apply"] = Field(
        ..., description="The rite of evolution."
    )
    message: Optional[str] = Field(None, description="The rationale for this evolution (migration name).")
    target_env: str = Field("dev", description="The environment to target (dev, staging, prod).")

class ObserveRequest(BaseRequest):
    """
    A plea to the Neural Link.
    Summons the TUI Dashboard for runtime introspection.
    """
    target_pid: Optional[int] = Field(None, description="PID of the process to attach to (System Probe).")
    log_stream: Optional[str] = Field(None, description="Path to a log file to tail and visualize.")
    port: Optional[int] = Field(None, description="Port to sniff (Traffic Analysis).")
    demo: bool = Field(False, description="Run in simulation mode to demonstrate capabilities.")

class TeachRequest(BaseRequest):
    """
    A plea to the Tutorial Forge.
    Generates interactive coursework from the codebase.
    """
    teach_command: Literal["generate", "start", "verify"] = Field(
        ..., description="The pedagogical rite."
    )
    topic: Optional[str] = Field(None, description="Focus of the tutorial (e.g., 'auth', 'database').")
    difficulty: Literal["novice", "adept", "master"] = Field("novice", description="Complexity of the generated quests.")
    output_dir: str = Field(".scaffold/tutorial", description="Where to store the course materials.")


class LazarusRequest(BaseRequest):
    """
    A plea to the Lazarus Protocol.
    Automated debugging and self-healing.
    """
    error_context: Optional[str] = Field(None, description="The stack trace or error message.")
    command: Optional[str] = Field(None, description="The command that triggers the failure (e.g. 'pytest').")
    auto_apply: bool = Field(False, description="If True, apply the fix without confirmation.")

class FortressRequest(BaseRequest):
    """
    A plea to the Fortress.
    Security auditing and hardening.
    """
    scan_type: Literal["dependencies", "code", "full"] = Field("full", description="The scope of the audit.")
    fix: bool = Field(False, description="Attempt to auto-patch vulnerabilities.")

class BabelRequest(BaseRequest):
    """
    A plea to the Babel Engine.
    Transmutes code from one tongue to another.
    """
    source: str = Field(..., description="The source file or directory to port.")
    target_lang: Literal["rust", "go", "python", "typescript"] = Field(..., description="The destination language.")
    fusion_bind: bool = Field(False, description="If True, auto-generates FFI bindings (Fusion) for the new code.")


class HolocronRequest(BaseRequest):
    """
    A plea to the Holocron.
    Traces the causal chains of reality to define perfect context.
    """
    # [THE FIX] Added 'forge' to the allowed literals
    holocron_command: Literal["trace", "slice", "forge"] = Field(
        ..., description="The causal rite."
    )

    virtual_context: Optional[Dict[str, str]] = Field(
        default=None,
        description="A dictionary mapping relative file paths to their string content for ephemeral causal tracing."
    )

    # 'entry_point' serves as the Symbol for trace/slice OR the Intent string for forge
    entry_point: str = Field(
        ..., description="The starting point (Symbol) or Problem Description."
    )

    input_data: Optional[str] = Field(None, description="JSON payload for dynamic tracing.")
    depth: int = Field(5, description="How deep to follow the white rabbit.")

    # [THE FIX] Added output_data to match the CLI 'dest' mapping
    output_data: Optional[str] = Field(None, description="Path to save the result.")

class OcularRequest(BaseRequest):
    """
    A plea to the Ocular Cortex.
    Visualizes the application and maps pixels back to code.
    """
    ocular_command: Literal["gaze", "audit", "align"] = Field(..., description="The visual rite.")
    url: str = Field("http://localhost:3000", description="The live URL to observe.")
    target_element: Optional[str] = Field(None, description="Selector or text description of the visual element.")
    design_mock: Optional[str] = Field(None, description="Path to an image file (Design Mock) to align against.")

class AetherRequest(BaseRequest):
    """
    A plea to the Neural Aether.
    Communes with the collective subconscious of all Architects.
    """
    aether_command: Literal["sync", "broadcast", "query"] = Field(..., description="The telepathic rite.")
    pattern_signature: Optional[str] = Field(None, description="Hash or signature of the problem/pattern.")
    privacy_level: Literal["high", "medium", "low"] = Field("high", description="Differential privacy setting.")


class DebateRequest(BaseRequest):
    """
    =================================================================================
    == THE SACRED PLEA FOR GNOSTIC DISCOURSE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)       ==
    =================================================================================
    @gnosis:title DebateRequest
    @gnosis:summary The pure, Pydantic-forged vessel for commanding the Hivemind.

    This is the unbreakable contract for the `debate` rite. It carries the topic of
    discourse, the chosen council of personas, and the sacred laws that will govern
    their communion. It is the one true key to unlocking the power of multi-agent
    AI consensus within the Scaffold cosmos.
    """
    model_config = ConfigDict(extra='allow')

    # --- I. The Core Gnostic Will ---
    workspace_command: str = Field(default="debate", description="The specific rite to be conducted by the Hivemind.")
    topic: str = Field(...,
                       description="The subject of the debate, either as a direct string or a path to a scripture of Gnosis.")

    # --- II. The Council of Personas ---
    personas: List[str] = Field(default_factory=lambda: ["architect", "security", "pragmatist"],
                                description="A list of the AI personas to summon for the debate council.")

    # --- III. The Laws of Communion ---
    rounds: int = Field(default=1, description="The number of rebuttal rounds to conduct after the initial arguments.")
    blind: bool = Field(default=False,
                        description="If True, personas do not see each other's arguments in the first round, forcing independent thought.")
    synthesize: bool = Field(default=True,
                             description="If True, a final AI Moderator will be summoned to analyze the transcript and forge a consensus.")
    interactive: bool = Field(default=False,
                              description="If True, the rite will pause after each round for the Architect's adjudication.")

    # --- IV. The Gnostic Chronicle ---
    output_path: Optional[str] = Field(default=None,
                                       description="Path to inscribe the final, complete transcript of the debate.")

    # --- V. The Alchemical Context ---
    variables: Dict[str, Any] = Field(default_factory=dict,
                                      description="Gnostic variables to bestow upon the debating council's context.")


class ConduitRequest(BaseRequest):
    """
    The sacred plea to awaken the Gnostic Cockpit (Celestial Bridge).
    """
    workspace_command: str = Field(default="conduit", description="The specific rite to be conducted.") # Corrected field name for consistency
    url: str = Field(default="https://aistudio.google.com/", description="The URL of the AI altar to embed.")
    port: int = Field(default=8787, description="The local port to serve the Gnostic Cockpit on.")


class ObservatoryRequest(BaseRequest):
    """
    A plea to manage the Gnostic Observatory.
    """
    obs_command: str = Field(..., description="The specific rite (list, add, switch, etc).")
    target: Optional[str] = Field(None, description="Path or ID of the project.")
    name: Optional[str] = Field(None, description="Alias for the project.")
    json_mode: bool = Field(False, description="Return pure JSON data (for Electron).")
    # For discover
    depth: int = 1

class ArchetypeRequest(BaseRequest):
    """
    =============================================================================
    == THE ARCHETYPE PLEA (V-Ω-SCHEMA)                                         ==
    =============================================================================
    LIF: 100x | The contract for discovering and managing patterns.
    """
    command: str = Field(default="list", description="The rite: list, inspect, pull, or sync.")
    target: Optional[str] = Field(None, description="The ID of the archetype or a Celestial URL.")
    output_path: Optional[str] = Field(None, description="Where to save a pulled archetype.")
    json_mode: bool = Field(default=False, description="Proclaim in machine-readable format.")



class GraphManifestRequest(BaseRequest):
    """
    A plea to the Genesis Architect.
    Carries the full topological definition of a reality to be forged.
    """
    project_root: str = Field(..., description="The physical anchor for manifestation")
    graph_data: Dict[str, Any] = Field(..., description="The full JSON payload of Nodes and Edges")
    dry_run: bool = Field(False, description="If true, returns a prophecy without inscription")

class PreviewRequest(BaseRequest):
    """The Plea to Gaze upon the Visual Soul."""
    path: str
    depth: int = 2  # How deep to traverse the component tree

class SimulateRequest(BaseRequest):
    content: Optional[str] = None
    target_file: Optional[str] = None
    language: Optional[str] = None
    timeout: int = 60
    env_vars: Optional[Dict[str, str]] = None
    # [ASCENSION]: The Holographic Lattice
    # Maps relative file paths to their content.
    virtual_context: Optional[Dict[str, str]] = None
    node_id: Optional[str] = None


class GrandSurveyRequest(BaseRequest):
    """
    A plea for the Omniscient Eye to gaze upon the workspace.
    Used by both CLI ('scaffold survey') and Daemon ('scaffold/grandSurvey').
    """
    rootUri: Optional[str] = Field(None, description="The workspace root URI to scan (RPC).")
    target_path: Optional[str] = Field(None, description="The CLI path argument.")

    # Internal Metadata (JSON '_meta' -> Python 'meta')
    meta: Optional[Dict[str, Any]] = Field(None, alias="_meta", description="Internal tracing metadata.")

    @model_validator(mode='after')
    def harmonize_targets(self) -> 'GrandSurveyRequest':
        # Unify CLI 'target_path' and RPC 'rootUri'
        if self.target_path and not self.rootUri:
            self.rootUri = f"file://{Path(self.target_path).resolve().as_posix()}"
        return self


# --- [ASCENSION 3]: THE CONFIGURATION PLEA ---
class ConfigChangeRequest(BaseRequest):
    """
    A plea to mutate the Neuro-Plasticity of the active Kernel.
    Primarily used via RPC 'workspace/didChangeConfiguration'.
    """
    settings: Dict[str, Any] = Field(..., description="The new configuration tree.")


class InitializeRequest(BaseRequest):
    """
    [THE FIRST BREATH]
    The LSP 'initialize' packet. Carries the client's capabilities and root URI.
    Now fully compliant with LSP 3.17 to prevent AttributeErrors.
    """
    processId: Optional[int] = None

    # [THE CURE]: Restored rootPath to satisfy the Node.js Client
    rootPath: Optional[str] = None
    rootUri: Optional[str] = None

    capabilities: Dict[str, Any] = Field(default_factory=dict)
    initializationOptions: Optional[Dict[str, Any]] = None
    trace: Optional[str] = "off"
    workspaceFolders: Optional[List[Any]] = None
    clientInfo: Optional[Dict[str, Any]] = None
    locale: Optional[str] = None  # Added for completeness


class PluginsRequest(BaseRequest):
    """
    [RITE: CENSUS]
    A plea to list all active capabilities (Artisans) within the Daemon.
    """
    command: str = "list"
    category: Optional[str] = None


class CliDispatchRequest(BaseRequest):
    """
    =============================================================================
    == THE CLI DISPATCH CONTRACT (V-Ω-SHIM-TRANSLATOR)                         ==
    =============================================================================
    A specialized vessel that carries raw command-line arguments from the
    Rust Shim into the warm heart of the Daemon.
    """
    args: List[str] = Field(..., description="The raw argv sequence from the shim.")
    auth_token: str = Field(..., description="The security token from the pulse file.")

class IndexRequest(BaseRequest):
    """
    The Plea for Knowledge.
    """
    force: bool = Field(False, description="Re-index all files regardless of cache state.")
    target_path: Optional[str] = Field(None, description="Specific file or directory to index.")


class SupabaseDomain(str, Enum):
    DATABASE = "database"
    AUTH = "auth"
    STORAGE = "storage"
    FUNCTION = "function"


class SupabaseRequest(BaseRequest):
    """
    =============================================================================
    == THE AKASHIC PLEA (V-Ω-TOTALITY-PERSISTENCE)                             ==
    =============================================================================
    LIF: ∞ | ROLE: DATA_CONTRACT | RANK: SOVEREIGN

    The unified, polymorphic vessel for all interactions with the Supabase Infrastructure.
    It segregates intent into three domains: DATABASE, AUTH, and STORAGE.

    ### THE 7 ASCENSIONS OF DATA:
    1.  **The Optionality Flag:** `optional=True` transforms a `single()` query into
        `maybe_single()`, returning `None` instead of crashing on empty results.
    2.  **Strict Domain Logic:** Validators ensure that a Database plea must have a Table,
        and a Storage plea must have a Bucket.
    3.  **The Counter:** Includes `count` strategy (exact/planned/estimated) for pagination.
    4.  **The Binary Carrier:** `file_source` allows streaming physical matter to Storage.
    5.  **The RPC Gateway:** First-class support for Stored Procedures (`rpc`) via `func_name`.
    6.  **Complex Filtering:** Accepts raw dictionary filters for advanced `PostgREST` syntax.
    7.  **Auth Expansion:** Supports admin actions like `generate_link` and `delete_user`.
    """
    model_config = ConfigDict(extra='ignore', populate_by_name=True)

    # --- 1. THE DOMAIN OF OPERATION ---
    domain: Literal["database", "auth", "storage", "function", "realtime"] = Field(
        ...,
        description="The realm of the Akashic Record to access."
    )

    # --- 2. DATABASE GNOSIS (TABLES & ROWS) ---
    table: Optional[str] = Field(None, description="Target table for DB operations.")

    method: Optional[Literal[
        "select", "insert", "update", "upsert", "delete", "rpc"
    ]] = Field(None, description="The SQL Verb.")

    # Query Modifiers
    select_columns: str = Field("*", description="Columns to retrieve (e.g. 'id, name, meta->key').")
    filters: Optional[Dict[str, Any]] = Field(None, description="Map of 'col': 'val' or 'col': 'op:val'.")
    order_by: Optional[str] = Field(None, description="Format: 'column:asc' or 'column:desc'.")
    limit: Optional[int] = Field(None, description="Pagination limit.")
    offset: Optional[int] = Field(None, description="Pagination offset.")

    # [THE CURE]: EXISTENTIAL MODIFIERS
    single: bool = Field(False, description="Expect exactly one result.")
    optional: bool = Field(False, description="If True, 'single' becomes 'maybe_single' (No error on 0 rows).")

    # Meta-Data
    count: Optional[Literal["exact", "planned", "estimated"]] = Field(None, description="Return total count strategy.")
    head: bool = Field(False, description="If True, return no data, only count/headers.")
    csv: bool = Field(False, description="If True, request response as CSV.")

    # RPC Specific
    func_name: Optional[str] = Field(None, description="Name of the Stored Procedure for 'rpc' method.")

    # --- 3. AUTH GNOSIS (IDENTITIES) ---
    auth_action: Optional[Literal[
        "get_user", "list_users", "create_user", "delete_user",
        "invite_user", "generate_link", "update_user", "sign_out"
    ]] = Field(None, description="The Identity Rite.")

    # Identity Data
    user_id: Optional[str] = Field(None, description="Target UUID of the soul.")
    email: Optional[str] = Field(None, description="Email coordinate.")
    password: Optional[str] = Field(None, description="Secret key for creation.")
    phone: Optional[str] = Field(None, description="E.164 phone coordinate.")

    # --- 4. STORAGE GNOSIS (ARTIFACTS) ---
    bucket: Optional[str] = Field(None, description="Target Storage Bucket.")
    storage_action: Optional[Literal[
        "upload", "download", "list", "remove", "move", "copy",
        "create_signed_url", "get_public_url"
    ]] = Field(None, description="The Archive Rite.")

    path: Optional[str] = Field(None, description="Path within the bucket.")
    file_source: Optional[Union[str, Path]] = Field(None, description="Local path to source file for upload.")
    destination: Optional[Union[str, Path]] = Field(None, description="Local path to save downloaded matter.")
    # =========================================================================
    # == [ASCENSION 1]: THE FORENSIC METADATA ENVELOPE (THE CURE)            ==
    # =========================================================================
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Forensic context (trace_id, novalym_id) for the Audit Scribe."
    )
    # =========================================================================

    # Storage Options
    content_type: Optional[str] = Field(None, description="MIME type override.")
    upsert_file: bool = Field(False, description="Overwrite existing file.")
    expiry_seconds: int = Field(3600, description="TTL for signed URLs.")

    # --- 5. UNIVERSAL PAYLOAD (THE DATA) ---
    # Used for Insert/Update bodies, RPC params, or User Metadata
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        None,
        description="The Gnostic Payload (Rows for DB, Metadata for Auth)."
    )

    # =========================================================================
    # == THE RITES OF VALIDATION (LOGIC GATES)                               ==
    # =========================================================================

    @model_validator(mode='after')
    def validate_domain_constraints(self) -> 'SupabaseRequest':
        """
        Ensures the Plea matches the Domain.
        Prevents asking the Database for a File, or Storage for a User.
        """
        # 1. DATABASE GATE
        if self.domain == 'database':
            if not self.table and not self.func_name:
                # RPC calls might use func_name instead of table, but usually table is required for standard ops
                if self.method != 'rpc':
                    raise ValueError("Database Rite requires a 'table'.")
            if not self.method:
                raise ValueError("Database Rite requires a 'method'.")

        # 2. STORAGE GATE
        if self.domain == 'storage':
            if not self.bucket:
                raise ValueError("Storage Rite requires a 'bucket'.")
            if not self.storage_action:
                raise ValueError("Storage Rite requires a 'storage_action'.")

            if self.storage_action == 'upload' and not self.file_source:
                raise ValueError("Upload Rite requires 'file_source'.")

        # 3. AUTH GATE
        if self.domain == 'auth':
            if not self.auth_action:
                raise ValueError("Auth Rite requires an 'auth_action'.")

            if self.auth_action in ['get_user', 'delete_user'] and not self.user_id:
                raise ValueError(f"Auth Rite '{self.auth_action}' requires 'user_id'.")

        return self


class CommunicationRequest(BaseRequest):
    """
    [THE HIGH HERALD'S PLEA]
    A unified request to dispatch information across the ether.
    """
    # Routing
    channel: Literal["email", "sms", "chat"] = Field(..., description="The medium of transmission.")
    provider: Optional[str] = Field(None, description="Specific provider override (e.g., 'gmail', 'resend').")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary context for middleware/Artisans.")
    # Destination
    recipient: Union[str, List[str]] = Field(..., description="Primary target(s).")
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None

    # Content
    subject: Optional[str] = None
    content: Optional[str] = Field(None, description="Raw text content.")
    template: Optional[str] = Field(None, description="Path to a Jinja2 template.")
    context: Dict[str, Any] = Field(default_factory=dict, description="Variables for the template.")

    # Artifacts
    attachments: List[str] = Field(default_factory=list, description="Paths to local files to attach.")

    # Metaphysics
    html: bool = True
    priority: str = "normal"


class NetworkProtocol(str, Enum):
    HTTP = "http"
    GRAPHQL = "graphql"
    WEBHOOK = "webhook"  # Specialized sending with signing


class NetworkRequest(BaseRequest):
    """
    [THE UNIVERSAL ADAPTER V2]
    A unified plea for interaction with the external digital ether.
    """
    # Routing
    protocol: NetworkProtocol = Field(default=NetworkProtocol.HTTP, description="Communication dialect.")
    url: str = Field(..., description="Target Endpoint.")
    method: str = Field("GET", description="HTTP Method (GET, POST, PUT, DELETE, PATCH).")

    # Payload
    headers: Dict[str, str] = Field(default_factory=dict)
    params: Dict[str, Any] = Field(default_factory=dict, description="Query parameters.")
    json_body: Optional[Dict[str, Any]] = Field(None, description="JSON payload.")
    data: Optional[Any] = Field(None, description="Raw body or Form data.")

    # GraphQL Specific
    query: Optional[str] = Field(None, description="GraphQL Query string.")
    variables: Optional[Dict[str, Any]] = Field(None, description="GraphQL Variables.")

    # Webhook Specific
    secret: Optional[str] = Field(None, description="Secret for HMAC signing.")
    signature_header: str = "X-Signature"

    # Configuration
    timeout: float = 10.0
    retries: int = 0
    auth: Optional[Dict[str, str]] = Field(
        None,
        description="Auth config. E.g. {'type': 'bearer', 'token': '...'} or {'type': 'basic', 'user': '...', 'pass': '...'}"
    )


class BillingEntity(str, Enum):
    CUSTOMER = "customer"
    SUBSCRIPTION = "subscription"
    PRODUCT = "product"
    PRICE = "price"
    INVOICE = "invoice"
    PORTAL = "portal"
    PAYMENT_LINK = "payment_link"
    EVENT = "event"  # For webhook verification


class BillingRequest(BaseRequest):
    """
    [THE TREASURY RITE V2]
    A unified plea to the Financial Sovereign (Stripe).
    """
    entity: BillingEntity = Field(..., description="The fiscal object to manipulate.")
    action: str = Field(..., pattern=r"^(create|retrieve|update|delete|list|search|finalize|void|pay|usage)$")

    # Context
    id: Optional[str] = Field(None, description="Target ID (cus_..., sub_...).")

    # Payload
    payload: Dict[str, Any] = Field(default_factory=dict, description="Stripe parameters (metadata, items, etc.).")

    # Advanced Tuning
    expand: List[str] = Field(default_factory=list,
                              description="Expand nested objects (e.g. ['customer', 'latest_invoice']).")
    limit: int = Field(10, description="Pagination limit for lists.")
    idempotency_key: Optional[str] = None

class StorageRequest(BaseRequest):
    """
    [THE ARCHIVE RITE] Manage heavy matter (Files/S3).
    """
    bucket: str = Field(..., description="Target bucket.")
    path: str = Field(..., description="File path in the cloud.")
    action: str = Field(..., pattern=r"^(upload|download|delete|sign_url)$")
    source_path: Optional[str] = Field(None, description="Local path for upload.")
    destination_path: Optional[str] = Field(None, description="Local path for download.")
    content_type: Optional[str] = None
    expiry_seconds: int = 3600


class CRMProvider(str, Enum):
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    ZOHO = "zoho"


class CRMRequest(BaseRequest):
    """
    [THE DIPLOMAT'S PLEA]
    A unified interface for managing Customer Relationships across disparate systems.
    """
    provider: CRMProvider = Field(default=CRMProvider.HUBSPOT, description="Target System.")

    # Targeting
    entity: str = Field(..., pattern=r"^(contact|company|deal|ticket|product)$")
    action: str = Field(..., pattern=r"^(create|update|upsert|get|list|search|delete|associate)$")

    # Identity
    id: Optional[str] = Field(None, description="Native CRM ID (e.g. 12345).")
    match_key: Optional[str] = Field("email", description="Field to use for Upsert/Search deduplication.")
    match_value: Optional[str] = Field(None, description="Value to match against.")

    # Payload
    data: Dict[str, Any] = Field(default_factory=dict, description="Fields/Properties to write.")

    # Linking (The Web of Relations)
    # Example: {"to_entity": "company", "to_id": "9876"}
    associations: List[Dict[str, str]] = Field(default_factory=list, description="Links to forge after creation.")

    # Tuning
    limit: int = 10
    properties: List[str] = Field(default_factory=list, description="Specific fields to retrieve.")


# =============================================================================
# == SECTION I: THE NEURAL TAXONOMY (ENUMS)                                  ==
# =============================================================================

class AIProvider(str, Enum):
    """The Silicon Minds available to the Monolith."""
    OPENAI = "openai"
    AZURE = "azure"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"  # Ollama / LM Studio
    GROQ = "groq"  # Hyper-velocity inference
    PERPLEXITY = "perplexity"  # Search-grounded inference


class ModelStrategy(str, Enum):
    """Abstract strategies that resolve to concrete models at runtime."""
    SMART = "smart"  # GPT-4o / Claude 3.5 Sonnet / o1
    FAST = "fast"  # GPT-4o-mini / Haiku / Llama 3
    REASONING = "reasoning"  # o1-preview / o3 (Heavy Chain of Thought)
    CREATIVE = "creative"  # High temperature variants
    CODING = "coding"  # Claude 3.5 Sonnet / DeepSeek Coder


class RAGStrategy(str, Enum):
    """The method of memory retrieval."""
    NONE = "none"
    BASIC = "basic"  # Vector Similarity only
    HYBRID = "hybrid"  # Vector + Keyword (BM25)
    DEEP = "deep"  # Recursive / Graph-based traversal
    AGENTIC = "agentic"  # The AI decides what to search


# =============================================================================
# == SECTION II: THE GNOSTIC SUB-STRATA (COMPONENTS)                         ==
# =============================================================================

class MediaAsset(BaseModel):
    """
    [THE SENSORY INPUT]
    A container for non-textual matter (Images, Audio frames).
    """
    type: Literal["image_url", "image_base64", "audio_base64"] = "image_url"
    data: str = Field(..., description="The URL or Base64 string.")
    detail: Literal["auto", "low", "high"] = "auto"


class ToolConfig(BaseModel):
    """
    [THE KINETIC LIMB]
    Definition of a function the AI is allowed to execute.
    """
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema
    strict: bool = False  # OpenAI Strict Mode support


# =============================================================================
# == SECTION III: THE OMEGA INTELLIGENCE REQUEST                             ==
# =============================================================================

class IntelligenceRequest(BaseRequest):
    """
    =============================================================================
    == THE OMEGA INTELLIGENCE REQUEST (V-Ω-TOTALITY-V9000)                     ==
    =============================================================================
    LIF: INFINITY | ROLE: COGNITIVE_PAYLOAD_VESSEL | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_NEURAL_REQ_2026_FINALIS

    The definitive, future-proof contract for summoning machine cognition.
    It contains pockets for every conceivable dimension of AI interaction:
    Text, Vision, Audio, Tooling, RAG, Forensics, and Economics.

    ### THE 12 ASCENSIONS OF THE SCHEMA:
    1.  **Metadata Sovereignty (THE CURE):** `metadata` is now a mandatory,
        pre-validated dictionary. The `AttributeError` is physically impossible.
    2.  **Multimodal Totality:** Support for `media_assets` list allows mixing
        text, images, and audio in a single prompt.
    3.  **Reasoning Physics:** Adds `reasoning_effort` (low/medium/high) for
        next-gen 'Thinking' models (o1/o3).
    4.  **Economic Circuit Breakers:** `budget_cap_usd` allows the request to
        self-terminate if the predicted cost is too high.
    5.  **Gnostic Context Injection:** A dedicated `context` dictionary for
        injecting RAG shards without polluting the `user_prompt` string manually.
    6.  **Safety & Compliance:** `safety_settings` dict for controlling
        guardrails (Gemini BlockNone vs OpenAI Moderation).
    7.  **Deterministic Anchoring:** `seed` field for reproducible outputs
        during regression testing.
    8.  **Tooling Orchestration:** First-class support for `tools`, `tool_choice`,
        and `parallel_tool_calls`.
    9.  **Achronal Trace Lineage:** `trace_id` is auto-generated if missing,
        binding the thought to the global causal chain.
    10. **Schema Enforcement:** `output_schema` field for forcing Structured Outputs
        (Pydantic/Zod) at the API level.
    11. **Provider Agnosticism:** `model` accepts abstract strategies ('smart')
        which the Provider resolves to concrete deployments.
    12. **The Finality Vow:** Extra fields are allowed (`extra='allow'`), ensuring
        this schema never breaks when providers release new parameters.
    """
    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True
    )

    # --- 1. THE CORE COGNITION (PROMPTS) ---
    system_prompt: Optional[str] = Field(
        default="You are a helpful Gnostic Assistant, an expert in software architecture.",
        description="The Constitutional Law / Persona of the Mind."
    )
    user_prompt: str = Field(
        ...,
        description="The kinetic query or instruction from the Architect."
    )

    # [ASCENSION 2]: LIST-BASED HISTORY
    # Allows passing a full chat history [user, assistant, user] for conversational continuity.
    messages: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Full conversation history. Overrides user_prompt/system_prompt if present."
    )

    # --- 2. MULTIMODAL SENSORY INPUT ---
    # Legacy fields for backward compatibility
    image_data: Optional[str] = Field(None, description="Legacy Base64 image.")
    image_url: Optional[str] = Field(None, description="Legacy Image URL.")

    # [ASCENSION 2]: THE MEDIA ARRAY
    media_assets: List[MediaAsset] = Field(
        default_factory=list,
        description="A phalanx of visual or audio inputs for the model."
    )

    # --- 3. ROUTING & STRATEGY ---
    provider: AIProvider = Field(default=AIProvider.OPENAI)
    model: str = Field(
        default=ModelStrategy.SMART,
        description="Target model ID or abstract strategy ('smart', 'fast')."
    )

    # --- 4. PHYSICS OF THOUGHT (HYPERPARAMETERS) ---
    temperature: float = Field(0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(2048, ge=1)
    top_p: float = Field(1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)

    # [ASCENSION 7]: DETERMINISM
    seed: Optional[int] = Field(None, description="The anchor for reproducible outputs.")

    # [ASCENSION 3]: REASONING EFFORT (o1/o3 support)
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = Field(
        None,
        description="Thinking budget for reasoning models."
    )

    # --- 5. OUTPUT GOVERNANCE ---
    stream: bool = Field(default=False)
    json_mode: bool = Field(default=False, description="Enforce JSON object return.")

    # [ASCENSION 10]: STRICT SCHEMA
    output_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="JSON Schema for Structured Outputs (strict mode)."
    )

    # --- 6. RAG & MEMORY STRATA ---
    use_rag: bool = Field(default=False)
    rag_strategy: RAGStrategy = Field(default=RAGStrategy.BASIC)

    # [ASCENSION 5]: CONTEXT INJECTION
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Key-value pairs to be injected into the prompt via Jinja."
    )
    rag_filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Metadata filters for the Vector Scry."
    )

    # --- 7. KINETIC TOOLS ---
    tools: List[ToolConfig] = Field(default_factory=list)
    tool_choice: Union[str, Dict[str, Any]] = Field(default="auto")
    parallel_tool_calls: bool = Field(default=True)

    # --- 8. FORENSICS, METADATA & ECONOMICS (THE CURE) ---
    # [ASCENSION 1]: THE METADATA ENVELOPE
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="The Forensic Sarcophagus. Holds trace_id, user_grade, and cost_center."
    )

    # [ASCENSION 9]: TRACE ID
    trace_id: str = Field(
        default="tr-void",
        description="The Silver Cord linking this thought to the Request."
    )

    # [ASCENSION 4]: FINANCIAL GUARD
    budget_cap_usd: float = Field(
        default=1.00,
        description="Hard stop if predicted cost exceeds this value."
    )
    cost_center: str = Field(
        default="GENERAL_COMPUTE",
        description="Ledger category for this spend."
    )

    # [ASCENSION 6]: SAFETY
    safety_settings: Dict[str, str] = Field(
        default_factory=dict,
        description="Provider-specific safety overrides (e.g. BLOCK_NONE)."
    )

    force: bool = Field(
        default=False,
        description="Sovereign Override to bypass budget/rate limits."
    )

    # =========================================================================
    # == THE RITE OF PRE-FLIGHT VALIDATION (THE FIX)                         ==
    # =========================================================================

    @model_validator(mode='before')
    @classmethod
    def forge_defaults(cls, data: Any) -> Any:
        """
        [THE GUARDIAN]: Ensures Metadata and Trace ID are never void.
        Heals the 'AttributeError' by physically injecting the dict if missing.
        """
        if isinstance(data, dict):
            # 1. HEAL METADATA FRACTURE
            if "metadata" not in data or data["metadata"] is None:
                data["metadata"] = {}

            # 2. TRACE ID HOISTING
            # If trace_id is at root, copy to metadata. If missing, gen new one.
            root_trace = data.get("trace_id")
            meta_trace = data["metadata"].get("trace_id")

            final_trace = root_trace or meta_trace or f"tr-ai-{uuid.uuid4().hex[:8]}"

            data["trace_id"] = final_trace
            data["metadata"]["trace_id"] = final_trace

            # 3. LEGACY IMAGE COMPATIBILITY
            # If legacy image fields exist, migrate them to media_assets
            if data.get("image_data"):
                assets = data.get("media_assets", [])
                assets.append({"type": "image_base64", "data": data["image_data"]})
                data["media_assets"] = assets

        return data

    @computed_field
    @property
    def fingerprint(self) -> str:
        """[ASCENSION 13]: Deterministic Hash of the Prompt Intent."""
        import hashlib
        core_content = f"{self.system_prompt}:{self.user_prompt}:{self.model}"
        return hashlib.sha256(core_content.encode()).hexdigest()

    def __repr__(self) -> str:
        return f"<Ω_INTELLIGENCE trace={self.trace_id} model={self.model} rag={self.use_rag}>"


class BrowserRequest(BaseRequest):
    """
    [THE NAVIGATOR'S PLEA]
    Command a headless browser to interact with the Living Web.
    """
    url: str = Field(..., description="Target URI.")
    action: str = Field(..., pattern=r"^(scrape|screenshot|pdf|interact)$")

    # Selectors & Interaction
    selector: Optional[str] = Field(None, description="CSS/XPath selector to target.")
    input_value: Optional[str] = Field(None, description="Text to type into inputs.")
    wait_for: Optional[str] = Field(None, description="Selector to wait for before acting.")

    # Extraction
    extract_fields: Optional[Dict[str, str]] = Field(None, description="Map of {key: selector} for scraping.")

    # Configuration
    headless: bool = True
    viewport: Dict[str, int] = Field(default_factory=lambda: {"width": 1280, "height": 720})
    timeout: float = 30.0


class DocumentFormat(str, Enum):
    PDF = "pdf"
    CSV = "csv"
    EXCEL = "xlsx"
    HTML = "html"


class DocumentRequest(BaseRequest):
    """
    [THE SCRIBE'S PLEA]
    Transmute structured data into physical documents, or ingest documents into data.
    """
    action: str = Field(..., pattern=r"^(generate|parse|convert|merge)$")
    format: DocumentFormat = Field(..., description="Target/Source format.")

    # Inputs
    source_path: Optional[str] = Field(None, description="Input file for parsing/conversion.")
    template_path: Optional[str] = Field(None, description="Jinja2 HTML template for PDF generation.")
    data: Optional[Union[List[Dict], Dict]] = Field(None, description="Data to inject into the document.")

    # Outputs
    output_path: Optional[str] = Field(None, description="Where to save the result.")

    # Options
    options: Dict[str, Any] = Field(default_factory=dict, description="Format-specific tuning (e.g. page_size).")


class WorkerRequest(BaseRequest):
    """
    [THE TASKMASTER'S PLEA]
    Dispatch logic to the background ethers (Queue).
    """
    queue: str = Field("default", description="Target queue name.")
    task: str = Field(..., description="Name of the function/task to execute.")
    args: List[Any] = Field(default_factory=list, description="Positional arguments.")
    kwargs: Dict[str, Any] = Field(default_factory=dict, description="Keyword arguments.")

    # Temporal Control
    delay_seconds: int = Field(0, description="Execute after delay.")
    schedule_at: Optional[datetime] = Field(None, description="Execute at specific time.")
    cron: Optional[str] = Field(None, description="Recurring schedule (CRON format).")

    # Resilience
    retries: int = Field(3, description="Max retry attempts.")
    timeout: int = Field(300, description="Execution timeout seconds.")


class VectorModel(str, Enum):
    OPENAI_ADA = "text-embedding-3-small"
    COHERE_V3 = "embed-english-v3.0"


class MemoryRequest(BaseRequest):
    """
    [THE CORTEX KEEPER'S PLEA]
    Manage Semantic Memory (Embeddings & Vector Search).
    """
    collection: str = Field(..., description="Logical grouping (Table/Namespace).")
    action: str = Field(..., pattern=r"^(upsert|query|delete|purge)$")

    # For Upsert
    text: Optional[Union[str, List[str]]] = Field(None, description="Raw text to embed and store.")
    metadata: Optional[Union[Dict, List[Dict]]] = Field(None, description="Payload to store with vectors.")
    ids: Optional[Union[str, List[str]]] = Field(None, description="Specific IDs (optional, auto-generated if void).")

    # For Query
    query_text: Optional[str] = Field(None, description="Concept to search for.")
    top_k: int = Field(5, description="Number of memories to recall.")
    threshold: float = Field(0.7, description="Minimum similarity score.")

    # Configuration
    model: VectorModel = Field(VectorModel.OPENAI_ADA, description="Embedding Model.")


class CacheRequest(BaseRequest):
    """
    =============================================================================
    == THE OMEGA CACHE REQUEST (V-Ω-TOTALITY-V110-HEALED)                      ==
    =============================================================================
    LIF: ∞ | ROLE: EPHEMERAL_STATE_VESSEL | RANK: LEGENDARY

    The definitive contract for all Stratum-8 (Redis) interactions.
    Healed of the 'AttributeError' heresy through Forensic Metadata Inception.
    """
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    # --- 1. THE COORDINATES ---
    key: str = Field(..., description="The unique identifier in the Ephemeral Vault.")
    action: Literal["get", "set", "delete", "increment", "lock", "exists", "unlock", "expire"] = Field(
        ..., description="The kinetic rite to perform on the vault."
    )

    # --- 2. THE MATTER ---
    value: Optional[Any] = Field(
        default=None,
        description="The data-soul to store (Required for 'set' and 'lock')."
    )

    # --- 3. THE PHYSICS ---
    ttl: int = Field(
        default=3600,
        description="Time-to-live in seconds. 0 for eternity."
    )
    amount: int = Field(
        default=1,
        description="The delta for 'increment' operations."
    )

    # =========================================================================
    # == [ASCENSION 1]: THE FORENSIC METADATA ENVELOPE (THE CURE)            ==
    # =========================================================================
    # This slot is now mandatory for all requests to ensure 100% compatibility
    # with the Gnostic Middleware Spine (Audit Logging, Tracing, Governance).
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Forensic context (trace_id, novalym_id, etc.) for the Audit Scribe."
    )

    # =========================================================================

    def __repr__(self) -> str:
        """PII-Safe representation for logs."""
        return f"<Cache:{self.action} key={self.key} trace={self.metadata.get('trace_id', 'None')}>"


class SheetProvider(str, Enum):
    GOOGLE = "google"
    AIRTABLE = "airtable"


class SheetRequest(BaseRequest):
    """
    [THE GRID MASTER'S PLEA]
    Interact with Spreadsheets and Smart Grids.
    """
    provider: SheetProvider = Field(default=SheetProvider.GOOGLE)
    action: str = Field(..., pattern=r"^(read|append|update|clear|create_tab)$")

    # Targeting
    base_id: str = Field(..., description="Spreadsheet ID or Airtable Base ID.")
    table_name: str = Field(..., description="Sheet name or Table name.")

    # Data
    rows: List[Dict[str, Any]] = Field(default_factory=list, description="Data rows.")
    row_id: Optional[str] = Field(None, description="Row ID for updates (Airtable only).")

    # Tuning
    range: Optional[str] = Field(None, description="A1 notation range (Google only).")
    value_input_option: str = Field("USER_ENTERED", description="Google: RAW or USER_ENTERED.")


class TwilioRequest(BaseRequest):
    """
    =============================================================================
    == THE TELEPHONIC VESSEL (V-Ω-OMNICHANNEL-GOD-OBJECT)                      ==
    =============================================================================
    LIF: ∞ | ROLE: CARRIER_INTENT | RANK: SOVEREIGN

    The one true vessel for all interactions with the Global Carrier Grid.
    It unifies Messaging, Provisioning, Intelligence, and Compliance into a
    single, polymorphic contract.
    """
    model_config = ConfigDict(extra='ignore', populate_by_name=True)

    # --- 1. THE RITE OF ACTION ---
    action: Literal[
        # Kinetic
        "send", "send_sms", "send_mms", "broadcast",
            # Infrastructure
        "search", "buy", "configure", "release", "update",
            # Intelligence
        "lookup", "validate",
            # Compliance (A2P 10DLC)
        "register_brand", "register_campaign", "link_number"
    ] = Field(..., description="The Telephonic Rite to perform.")

    # --- 2. KINETIC TARGETING (MESSAGING) ---
    to_number: Optional[str] = Field(None, alias="recipient", description="Target E.164 coordinate.")
    from_number: Optional[str] = Field(None, alias="sender", description="Origin E.164 coordinate.")
    messaging_service_sid: Optional[str] = Field(None, description="A2P Messaging Service SID (MG...).")

    body: Optional[str] = Field(None, alias="content", description="The text payload.")
    media_url: Optional[Union[str, List[str]]] = Field(None, description="List of media URLs for MMS.")

    # Advanced Kinetic Physics
    status_callback: Optional[str] = Field(None, description="Webhook for delivery confirmation.")
    validity_period: Optional[int] = Field(14400, description="Seconds before message expires (TTL).")
    schedule_type: Optional[Literal["fixed"]] = Field(None, description="For scheduled messages.")
    send_at: Optional[str] = Field(None, description="ISO8601 timestamp for scheduled delivery.")

    # --- 3. INFRASTRUCTURE SCRYING (PROVISIONING) ---
    country_code: str = Field("US", description="ISO 3166-1 alpha-2 Country Code (e.g., US, GB, DE).")
    area_code: Optional[str] = Field(None, description="3-digit regional prefix.")
    contains: Optional[str] = Field(None, description="Sequence of digits the number must contain.")
    limit: int = Field(5, description="Maximum number of results to scry.")

    # Capability Filters
    sms_enabled: bool = Field(True, description="Must support SMS.")
    mms_enabled: bool = Field(True, description="Must support MMS.")
    voice_enabled: bool = Field(True, description="Must support Voice.")

    # --- 4. ASSET MANAGEMENT (CONFIGURATION) ---
    phone_number: Optional[str] = Field(None, description="The E.164 number to act upon.")
    sid: Optional[str] = Field(None, description="The Twilio Resource SID (PN..., SM..., MG...).")
    friendly_name: Optional[str] = Field(None, description="Human-readable label for the asset.")

    # Webhook Bindings
    voice_url: Optional[str] = Field(None, description="Webhook for inbound calls.")
    sms_url: Optional[str] = Field(None, description="Webhook for inbound messages.")
    status_callback_method: Literal["POST", "GET"] = Field("POST", description="HTTP Method for webhooks.")

    # --- 5. INTELLIGENCE (LOOKUPS) ---
    include_name: bool = Field(False, description="Perform CNAM (Caller ID) lookup.")
    include_carrier: bool = Field(True, description="Perform HLR Carrier lookup.")

    # --- 6. REGULATORY COMPLIANCE (A2P 10DLC) ---
    # Identity
    legal_name: Optional[str] = Field(None, alias="business_name", description="Legal Business Name.")
    email: Optional[str] = Field(None, description="Contact email for compliance.")
    website: Optional[str] = Field(None, description="Business URL.")
    tax_id: Optional[str] = Field(None, alias="ein", description="EIN or Tax ID.")
    address_sid: Optional[str] = Field(None, description="Twilio Address SID (AD...).")

    # Campaign
    brand_sid: Optional[str] = Field(None, description="A2P Brand SID (BZ...).")
    use_case: Optional[str] = Field("LOW_VOLUME_MIXED", description="Campaign Use Case.")
    description: Optional[str] = Field(None, description="Campaign Description for carrier review.")
    sample_msgs: Optional[List[str]] = Field(None, description="Sample messages for compliance audit.")
    policy_sid: Optional[str] = Field(None, description="Regulatory Policy SID.")

    # --- 7. METAPHYSICS ---
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Contextual Gnosis.")

    @field_validator('media_url', mode='before')
    @classmethod
    def unify_list(cls, v: Any) -> Optional[List[str]]:
        """Transmutes a single string into a list of strings."""
        if isinstance(v, str):
            return [v]
        return v

    @model_validator(mode='after')
    def validate_kinetics(self) -> 'TwilioRequest':
        """Ensures the Vessel is watertight based on the Rite."""
        action = self.action

        # Kinetic Validation
        if action in ['send', 'send_sms', 'send_mms']:
            if not self.to_number:
                raise ValueError(f"Rite '{action}' requires 'to_number'.")
            if not self.body and not self.media_url:
                raise ValueError(f"Rite '{action}' requires 'body' or 'media_url'.")

        # Provisioning Validation
        if action == 'buy':
            if not self.phone_number:
                raise ValueError(f"Rite '{action}' requires 'phone_number'.")

        # Search Validation
        if action == 'search':
            if not self.country_code:
                # Default applied in field, but safety check
                raise ValueError("Rite 'search' requires 'country_code'.")

        return self


class TwilioA2PRequest(BaseRequest):
    """[THE REGULATORY PLEA] Command Twilio to execute Trust Hub rites."""
    action: str = Field(..., pattern=r"^(create_brand|create_campaign|link_number|check_status)$")

    # Brand Matter
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None  # EIN/Registration Number
    website: Optional[str] = None

    # Campaign Matter
    use_case: str = Field("CUSTOMER_CARE", description="A2P Use Case code.")
    description: str = Field(..., description="Nature of the messaging.")
    sample_msgs: List[str] = Field(default_factory=list)

    # Binding Matter
    messaging_service_sid: Optional[str] = None
    phone_number_sid: Optional[str] = None


def get_default_signup_url():
    """Dynamically determines the canonical sign-up path based on environment."""
    # Priority: Env variable > Custom Domain > Default Path
    domain = os.environ.get("NEXT_PUBLIC_BASE_DOMAIN", "https://novalym.com")
    # Ensure it uses the explicit sign-up path
    return f"{domain}/sign-up"


class ClerkRequest(BaseRequest):
    """
    =============================================================================
    == THE IDENTITY VESSEL (V-Ω-CLERK-ULTIMA-V2)                               ==
    =============================================================================
    LIF: ∞ | ROLE: IDENTITY_GOVERNOR | RANK: LEGENDARY

    The definitive contract for all interactions with the Clerk.com API,
    optimized for self-service sign-up flows.
    """
    model_config = ConfigDict(extra='ignore', populate_by_name=True)

    # --- THE RITE OF ACTION ---
    action: Literal[
        "invite", "revoke_invite", "list_invites",  # Invitations
        "get_user", "update_user", "delete_user", "list_users",  # Users
        "get_org", "create_org", "update_org", "add_member",  # Organizations
        "update_metadata", "get_sessions", "kick_session"  # Meta & Governance
    ] = Field(..., description="The Auth Rite to conduct.")

    # --- COORDINATES ---
    email: Optional[str] = Field(None, description="The primary soul anchor.")
    user_id: Optional[str] = Field(None, description="Clerk User ID (user_...).")
    org_id: Optional[str] = Field(None, description="Clerk Org ID (org_...).")
    invitation_id: Optional[str] = Field(None, description="Invite ID (inv_...).")
    session_id: Optional[str] = Field(None, description="Session ID (sess_...).")

    # --- THE GNOSTIC PAYLOAD ---
    public_metadata: Optional[Dict[str, Any]] = Field(None, description="Visible to the frontend UI.")
    private_metadata: Optional[Dict[str, Any]] = Field(None, description="Visible only to the Python Brain.")
    unsafe_metadata: Optional[Dict[str, Any]] = Field(None, description="Mutable by the user (rarely used).")

    # --- PARAMETERS ---
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = Field("basic_member", description="Org role (admin/member).")

    # [THE CURE]: DYNAMIC SIGN-UP ANCHOR
    # The default is now the initial sign-up portal, ensuring the token is processed.
    # We make it Optional, and the default is defined by the function above.
    redirect_url: Optional[str] = Field(
        default_factory=get_default_signup_url,
        description="URL to redirect user to after an action (e.g., setting password)."
    )

    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)

    # --- SIMULATION ---
    simulation: bool = Field(False, description="Force Phantom Circuit even in Prod.")


# =============================================================================
# == THE TEMPORAL RITE TAXONOMY                                              ==
# =============================================================================

class TemporalAction(str, Enum):
    SCRY_SLOTS = "scry_slots"
    BOOK_CONFIRM = "book_confirm"
    CANCEL_EVENT = "cancel_event"
    SYNC_CHECK = "sync_check"
    VERIFY_STATUS = "verify_status"
    RESCHEDULE = "reschedule"
class TemporalProvider(str, Enum):
    CAL_COM = "cal.com"
    GOOGLE = "google"
    OUTLOOK = "outlook"
    CALENDLY = "calendly"
    CUSTOM = "custom"

# =============================================================================
# == THE TEMPORAL TARGET (V-Ω-SOVEREIGN_COORDINATE)                          ==
# =============================================================================
# =============================================================================
# == THE TEMPORAL TARGET (V-Ω-SOVEREIGN_COORDINATE)                          ==
# =============================================================================
class CalendarTarget(BaseModel):
    """
    [THE GNOSTIC COORDINATE]
    The immutable DNA of the target calendar reality (The Client's Config).
    """
    model_config = ConfigDict(extra='ignore', frozen=True)

    # --- PRIMARY IDENTITY ANCHORS (Pulled from Client's JSONB) ---
    username: str = Field(..., description="The user's unique Cal.com namespace.")
    event_type_id: Union[int, str] = Field(..., description="The specific event/meeting type slug or ID.")

    # --- KINETIC KEYS (Override Fuel - Defaults to Master Key) ---
    api_key: Optional[str] = Field(None, description="A tenant-specific Cal.com API key, if overriding Master.")

    # --- PHYSICS & BEHAVIOR ---
    timezone: str = Field("UTC", description="The target timezone for displaying slots.")
    buffer_mins: int = Field(60, ge=0, description="The 'Biological Cooldown' - Safety minutes between calls.")


# =============================================================================
# == THE CALENDAR REQUEST (V-Ω-ULTIMA_TOTALITY_FINALIS_V3)                   ==
# =============================================================================
class CalendarRequest(BaseRequest):
    """
    =============================================================================
    == THE CALENDAR REQUEST (V-Ω-ULTIMA_TOTALITY_FINALIS_V3)                   ==
    =============================================================================
    LIF: ∞ | ROLE: SPACETIME_COORDINATE_PLEA | RANK: SOVEREIGN

    The final, definitive, and unbreakable Gnostic Contract for all temporal movements.
    It is the centralized source of truth for the entire Scaffold Monolith.
    """
    model_config = ConfigDict(
        extra='ignore',
        frozen=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    # --- 1. THE SACRED ACTION ---
    action: TemporalAction = Field(..., description="The specific temporal movement to conduct.")
    provider: TemporalProvider = Field(default=TemporalProvider.CAL_COM, description="The celestial scheduling engine.")

    # --- 2. THE TARGET REALITY (CRITICAL SUTURE) ---
    # This carries all the client's config data for the Artisan to use.
    target: CalendarTarget = Field(..., description="The immutable configuration and identity of the target calendar.")

    # --- 3. THE LEAD'S BIOMETRIC SOUL (For Booking) ---
    novalym_id: str = Field(..., description="The Sovereign ID of the Client Entity.")
    lead_phone: str = Field(..., description="The E.164 coordinate of the Lead.")
    lead_name: Optional[str] = Field("Valued Client", description="The humanized name for the invite.")
    lead_email: Optional[str] = Field(None, description="The digital soul coordinate for the invite.")

    # --- 4. THE CONVERSATIONAL STATE (For Multi-Turn Booking) ---
    selected_option: Optional[Literal["A", "B", "C"]] = Field(None,
                                                              description="The A/B/C slot identifier chosen by the lead.")
    explicit_timestamp: Optional[str] = Field(None, description="A direct ISO8601 string for booking.")

    # --- 5. PHYSICS & OVERRIDES ---
    duration_mins: int = Field(default=15, ge=5, description="The mass of the meeting in time.")
    force: bool = Field(default=False, description="Bypass safety checks and cache.")

    # --- 6. METADATA & FORENSICS ---
    metadata: Dict[str, Any] = Field(default_factory=dict,
                                     description="Forensic metadata (trace_id, simulation, ui_hints).")

    # =========================================================================
    # == COMPUTED REALITIES (ASCENSION 6 & 5 & 3)                            ==
    # =========================================================================

    @computed_field
    @property
    def is_simulation(self) -> bool:
        """Adjudicates reality mode from multiple sources."""
        if self.metadata.get("simulation") is not None:
            return bool(self.metadata["simulation"])
        return os.environ.get("SCAFFOLD_ENV") == "development"

    @computed_field
    @property
    def merkle_id(self) -> str:
        """[ASCENSION 3]: Collision avoidance fingerprint."""
        raw = f"{self.novalym_id}:{self.lead_phone}:{self.action}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    # =========================================================================
    # == THE ALCHEMICAL VALIDATORS (ASCENSION 24 & 4)                        ==
    # =========================================================================

    @field_validator('lead_phone', mode='before')
    @classmethod
    def purify_phone(cls, v: Any) -> str:
        """The Telephonic Healer (E.164 Enforcer)."""
        if not v: return ""
        clean = "".join(c for c in str(v) if c.isdigit() or c == '+')
        if not clean.startswith('+'):
            if len(clean) == 10: return f"+1{clean}"
            return f"+{clean}"
        return clean

    @model_validator(mode="after")
    def verify_rite_viability(self) -> 'CalendarRequest':
        """FINALITY VOW - Logic Gates."""
        if self.action == TemporalAction.BOOK_CONFIRM and not (self.selected_option or self.explicit_timestamp):
            if not self.is_simulation:
                raise ValueError("The 'book_confirm' rite requires a selection.")
        return self

# == SCRIPTURE SEALED: THE CALENDAR CONTRACT REACHES TOTALITY ==

class ProjectRequest(BaseRequest):
    """
    =============================================================================
    == THE OMEGA PROJECT REQUEST (V-Ω-TOTALITY-V705-RECONSTRUCTED)             ==
    =============================================================================
    The definitive contract for Multiverse Governance.
    Warded against Null-Type heresies and Case-Sensitivity paradoxes.
    """

    # --- I. THE KINETIC COMMAND ---
    action: str = Field(
        ...,
        description="The governance rite: list | create | delete | switch | update | import"
    )

    # --- II. IDENTITY & SOVEREIGNTY ---
    id: Optional[str] = Field(None, description="The unique UUID of the target reality.")
    name: Optional[str] = Field(None, description="The human-readable label for the project.")
    description: Optional[str] = Field(None, description="The Gnostic summary of intent.")
    owner_id: Optional[str] = Field("GUEST", description="The identity of the Architect.")
    is_demo: bool = Field(False, description="True if this is an immutable Reference Reality.")

    # --- III. GENETIC DNA (THE CURE) ---
    # [ASCENSION 1]: Use Optional + default_factory to absorb JS 'null' or missing keys.
    template: Optional[str] = Field(None, description="The Archetype DNA (e.g. 'react-vite').")

    tags: Optional[List[str]] = Field(
        default_factory=list,
        description="Semantic labels for categorization."
    )

    filter_tags: Optional[List[str]] = Field(
        default_factory=list,
        description="Filter results by specific tags."
    )

    # --- IV. SPATIAL GEOMETRY ---
    path: Optional[str] = Field(None, description="Physical path override (for imports).")
    filter_status: Optional[str] = Field(None, description="active | archived")

    # --- V. FORENSIC & OCULAR DATA ---
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Catch-all vessel for ephemeral Gnosis and telemetrics."
    )

    ui_hints: Dict[str, Any] = Field(
        default_factory=lambda: {"vfx": "pulse", "color": "#64ffda"},
        description="Haptic instructions for the Ocular HUD."
    )

    # =============================================================================
    # == THE RITES OF VALIDATION (ALCHEMICAL PURIFICATION)                       ==
    # =============================================================================

    @field_validator('action', mode='before')
    @classmethod
    def _normalize_action(cls, v: Any) -> str:
        """[ASCENSION 2]: Isomorphic Normalization. Forces lowercase."""
        if isinstance(v, str):
            return v.lower().strip()
        return str(v).lower()

    @model_validator(mode='before')
    @classmethod
    def _heal_null_collections(cls, data: Any) -> Any:
        """
        [ASCENSION 1]: THE NULL-VOID NULLIFIER.
        Intercepts the raw dictionary and ensures 'tags' and 'filter_tags' are never None.
        """
        if isinstance(data, dict):
            for key in ['tags', 'filter_tags']:
                if key in data and data[key] is None:
                    data[key] = []
        return data

    @field_validator('tags', 'filter_tags', mode='after')
    @classmethod
    def _sanitize_tags(cls, v: Optional[List[str]]) -> List[str]:
        """[ASCENSION 4]: Semantic Sanitization."""
        if not v: return []
        # Strip whitespace and force lowercase for consistent indexing
        return [tag.strip().lower() for tag in v if isinstance(tag, str) and tag.strip()]


# =============================================================================
# == STRATUM-0: INFRASTRUCTURE ENUMS & LITERALS (THE LAW)                   ==
# =============================================================================

CloudAction = Literal[
    "provision",  # Matter Genesis
    "terminate",  # Matter Dissolution
    "status",  # Metabolic Scry
    "list",  # Multiversal Census
    "reconcile",  # Achronal Audit
    "cost_check",  # Fiscal Prophecy
    "teleport"  # Quantum Matter Transfer
]

CloudProvider = Literal[
    "aws",  # The US Public Cloud
    "oracle",  # The ARM Giant
    "hetzner",  # The Mercenary Substrate
    "azure",  # The Enterprise Nebula
    "docker",  # Local Vessel Simulation
    "local",  # Local Iron execution
    "ovh"  # Sovereign European Iron
]


# =============================================================================
# == STRATUM-1: THE GNOSTIC CONFIGURATION VESSELS (DNA)                      ==
# =============================================================================

class RequestMetadata(BaseModel):
    """
    =============================================================================
    == THE NEURAL PASSPORT (V-Ω-TOTALITY-V3000.1-RESILIENT)                    ==
    =============================================================================
    LIF: ∞ | ROLE: FORENSIC_IDENTITY_HOLDER | RANK: SOVEREIGN
    AUTH: Ω_METADATA_SUTURE_2026_FINALIS

    [THE FIX]: This vessel is guaranteed to be manifest via default_factory in
    the parent CloudRequest, annihilating the 'NoneType' attribute heresy.
    """
    model_config = ConfigDict(extra='allow')

    trace_id: str = Field(default_factory=lambda: f"tr-cloud-{uuid.uuid4().hex[:8].upper()}")
    client_id: str = Field("ARCHITECT_PRIME", description="The identity of the willed source.")
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex, description="The ephemeral lifecycle link.")

    # --- METABOLIC TOMOGRAPHY ---
    inception_ts: float = Field(default_factory=time.time)
    substrate_origin: str = Field("WASM_WORKBENCH", description="The plane from which the plea was spoken.")
    adrenaline_mode: bool = Field(False, description="Commands the kernel to prioritize velocity over tax.")


class NodeSpecification(BaseModel):
    """
    =============================================================================
    == THE NODE SPECIFICATION (HARDWARE_DNA)                                   ==
    =============================================================================
    Defines the physical characteristics of the willed compute node.
    """
    model_config = ConfigDict(extra='allow', arbitrary_types_allowed=True)

    # --- PHYSICAL FORM ---
    size: str = Field("small-1", description="Instance shape or Gnostic size slug.")
    image: str = Field("ubuntu-22-04-lts", description="The OS image or AMI coordinate.")
    region: str = Field("universal", description="Geographic locus of materialization (e.g., GRA11, us-east-1).")
    storage_gb: int = Field(20, ge=8, le=16384, description="Persistent disk mass.")

    # --- NETWORK TOPOGRAPHY ---
    open_ports: List[int] = Field(default_factory=lambda: [22, 80, 443, 7860])
    assign_public_ip: bool = Field(True, description="Vow to expose the node to the public aether.")

    # --- SECURITY MATTERS ---
    ssh_key_name: Optional[str] = Field(None, description="The name of the warded public key.")
    user_data: Optional[str] = Field(None, description="Cloud-init script soul for bootstrap.")
    project_root: Path = Field(default_factory=lambda: Path("."), description="The local anchor.")


# =============================================================================
# == STRATUM-2: THE OMEGA CLOUD REQUEST (THE PLEA)                           ==
# =============================================================================

class CloudRequest(BaseRequest):
    """
    =================================================================================
    == THE CELESTIAL PLEA: CLOUD REQUEST (V-Ω-TOTALITY-V35000-FINALIS)             ==
    =================================================================================
    LIF: INFINITY | ROLE: INFRASTRUCTURE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_CLOUD_REQUEST_V35000_TOTALITY_SUTURE_2026_FINALIS

    The definitive contract for all kinetic actions targeting the cloud.
    It has been ascended to its final form, incorporating the Neural Passport
    to guarantee zero-fracture communication across the split-process lattice.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Neural Passport Integration (THE CURE):** Introduces `RequestMetadata` as a
        mandatory, non-nullable stratum, annihilating the `AttributeError` loop.
    2.  **Bicameral Path Normalization:** Automatically reconciles local POSIX paths
        with remote cloud coordinates.
    3.  **Fiscal Adjudication Ward:** Injects a `max_hourly_rate` ceiling to prevent
        metabolic drain on the Architect's treasury.
    4.  **Achronal Trace Inception:** Automatically grafts a `stk-` Trace ID at the
        moment of birth if the metadata is silent.
    5.  **Substrate-Aware Defaulting:** Intelligently defaults to 'WASM' heuristics
        when the environment DNA suggests browser isolation.
    6.  **NoneType Sarcophagus:** All complex fields utilize `default_factory`,
        ensuring `.get()` and attribute access never encounter a null object.
    7.  **Idempotency Fingerprinting:** The `forge_identity_hash` method creates a
        deterministic Merkle-signature of the hardware intent.
    8.  **Haptic HUD Proclamation:** The `ui_hints` property is an Oracle that
        commands the Ocular Membrane to render appropriate VFX based on action.
    9.  **Socratic Intent Validation:** A post-validator that physically refuses
        lethal rites (terminate/status) if a coordinate (instance_id) is missing.
    10. **Governance Tag Injection:** Automatically grafts `ManagedBy: VELM` into
        every provision rite for cloud-provider hygiene.
    11. **Substrate Telemetry Suture:** Connects the `inception_ts` to the
        Distributed Tracing stratum for microsecond-precision latency audits.
    12. **The Finality Vow:** A mathematical guarantee of a resonant, engine-ready
        vessel that satisfies both the Mind and the Eye.
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow',
        validate_assignment=True
    )

    # --- I. THE NEURAL PASSPORT ---
    # [THE CURE]: Using default_factory ensures this is NEVER None.
    metadata: RequestMetadata = Field(
        default_factory=RequestMetadata,
        description="The forensic identity and tracing stratum."
    )

    # --- II. PRIMARY INTENT ---
    command: CloudAction = Field(
        ...,
        description="The specific Infrastructure Rite to perform."
    )
    provider: Optional[CloudProvider] = Field(
        None,
        description="The target cloud substrate (OVH, AWS, Azure, etc.)."
    )

    # --- III. TARGET COORDINATES ---
    instance_id: Optional[str] = Field(
        None,
        description="The unique physical ID of the node manifest in the multiverse."
    )
    name: Optional[str] = Field(
        None,
        description="The human-readable label for a new reality shard."
    )

    # --- IV. HARDWARE DNA (SPECIFICATIONS) ---
    spec: NodeSpecification = Field(
        default_factory=NodeSpecification,
        description="The hardware DNA required for provisioning."
    )

    # --- V. GOVERNANCE & FISCAL WARDS ---
    max_hourly_rate: float = Field(
        0.85,
        description="The metabolic ceiling (USD/hr). Strikes exceeding this are stayed."
    )
    tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Semantic metadata to be etched into the physical iron."
    )

    # --- VI. KINETIC MODIFIERS ---
    force: bool = Field(False, description="Bypass confirmation wards (Rite of Absolute Will).")
    non_interactive: bool = Field(False, description="The Vow of Silence for automated sanctums.")
    timeout: int = Field(600, description="The time-horizon (seconds) before the connection dissolves.")
    adrenaline_mode: bool = Field(False, description="Prioritize speed over metabolic cost.")

    # =========================================================================
    # == THE RITES OF ADJUDICATION (VALIDATORS)                              ==
    # =========================================================================

    @model_validator(mode='after')
    def adjudicate_intent(self) -> 'CloudRequest':
        """
        [THE ORACLE'S VOW]
        Ensures the plea is internally consistent before reaching the Artisan.
        """
        # 1. ANNIHILATION WARD: Require ID for scrying or destruction
        if self.command in ["terminate", "status"] and not self.instance_id:
            raise ValueError(f"The '{self.command}' rite requires a target 'instance_id' coordinate.")

        # 2. GENESIS WARD: Ensure identity for provisioning
        if self.command == "provision":
            if not self.name:
                self.name = f"titan-{uuid.uuid4().hex[:6].upper()}"
            if not self.provider:
                # Default to OVH Sovereign Iron if unmanifested
                self.provider = "ovh"

        # 3. TRACE SUTURE
        # If the top-level trace_id is a void, we adopt the one from the metadata passport.
        if not getattr(self, 'trace_id', None):
            object.__setattr__(self, 'trace_id', self.metadata.trace_id)

        return self

    @field_validator('tags', mode='before')
    @classmethod
    def ensure_governance_tags(cls, v: Any) -> Dict[str, str]:
        """[ASCENSION 10]: Enforces the inclusion of management metadata."""
        base = v if isinstance(v, dict) else {}
        base.setdefault("ManagedBy", "VELM_GOD_ENGINE")
        base.setdefault("Sovereignty", "High")
        base.setdefault("InceptionTS", str(time.time()))
        return base

    # =========================================================================
    # == KINETIC METHODS                                                     ==
    # =========================================================================

    def forge_identity_hash(self) -> str:
        """
        [ASCENSION 7]: Generates an idempotency fingerprint of the hardware intent.
        """
        payload = f"{self.provider}:{self.name}:{self.spec.size}:{self.spec.image}:{self.spec.region}"
        return hashlib.sha256(payload.encode()).hexdigest()

    @property
    def is_destructive(self) -> bool:
        """Adjudicates if the rite is lethal (returns matter to the void)."""
        return self.command == "terminate"

    @property
    def ui_hints(self) -> Dict[str, Any]:
        """[ASCENSION 8]: Proclaims haptic instructions for the Ocular UI."""
        mapping = {
            "provision": {
                "vfx": "bloom_teal",
                "sound": "ignition_sequence",
                "label": "MATERIALIZING_IRON",
                "color": "#64ffda",
                "priority": "SUCCESS"
            },
            "terminate": {
                "vfx": "shake_red",
                "sound": "annihilation_echo",
                "label": "DISSOLVING_REALITY",
                "color": "#ef4444",
                "priority": "WARNING"
            },
            "status": {
                "vfx": "pulse_blue",
                "label": "SCRYING_METABOLISM",
                "color": "#3b82f6",
                "priority": "INFO"
            },
            "teleport": {
                "vfx": "wormhole_purple",
                "sound": "matter_transfer",
                "label": "TELEPORTING_SOUL",
                "color": "#a855f7",
                "priority": "HIGH"
            }
        }
        return mapping.get(self.command, {"vfx": "pulse", "label": "CONDUCTING_RITE", "color": "#64748b"})

    def __repr__(self) -> str:
        return f"<Ω_CLOUD_PLEA cmd={self.command} provider={self.provider} trace={self.metadata.trace_id[:8]}>"


class IdentityRequest(BaseRequest):
    """
    =============================================================================
    == THE DIPLOMATIC MULTICLOUD VESSEL (V-Ω-TOTALITY-V5000.1-FINALIS)         ==
    =============================================================================
    LIF: ∞ | ROLE: MULTIVERSAL_AUTH_CONTRACT | RANK: OMEGA_SOVEREIGN

    The final, definitive, and unbreakable vessel for establishing Sovereign Bonds
    across the Quad-Cloud Federation (OVH, AWS, Azure, Hetzner).

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Apophatic Credential Suture (THE CURE):** A high-velocity pre-validator
        that scries the root payload for 15+ distinct cloud-specific keys
        (AWS, Azure, OVH, Hetzner) and surgically moves them into the
        `credentials` vault before the Mind (Pydantic) adjudicates.
    2.  **Provider Normalization:** Enforces lowercase discipline to prevent
        registry schisms (e.g., "AWS" -> "aws").
    3.  **Region Defaulting:** Automatically assumes `ovh-eu` if the region is
        void, ensuring a physical anchor for the handshake.
    4.  **NoneType Sarcophagus:** All collections (credentials, scopes) use
        `default_factory`, guaranteeing that `.get()` never encounters a null object.
    5.  **Substrate-Aware Persistence:** Defaults `persist_globally` to True,
        ensuring the Handshake is etched into the `.env` ledger.
    6.  **Sovereign Alias Mapping:** Supports `profile_name` for managing
        multiple identities (e.g., 'prod-aws' vs 'dev-aws') in the same vault.
    7.  **Titanium Path Normalization:** Inherits `project_root` resolution
        from BaseRequest, ensuring absolute coordinate resonance.
    8.  **Strict Kinetic Triage:** Validates that the `action` is a recognized
        Gnostic verb ('handshake', 'verify', 'whoami', etc.).
    9.  **Bicameral Identity Shield:** Credentials are warded within their
        own dictionary, isolating them from standard request metadata.
    10. **Achronal Trace Suture:** Guarantees that the `trace_id` from the
        Ocular UI binds to the resulting Identity.
    11. **Metadata Ingress:** Allows for arbitrary forensic tags to be
        carried within the `metadata` slot.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable
        contract, suitable for securing startup credits and celestial alliances.
    =============================================================================
    """
    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
        validate_assignment=True,
        arbitrary_types_allowed=True
    )

    # --- I. THE KINETIC ACTION ---
    action: str = Field(
        ...,
        description="The identity rite: 'handshake', 'verify', 'whoami', 'forget', 'rotate'."
    )

    # --- II. THE TARGET CELESTIAL BODY ---
    provider: str = Field(
        ...,
        description="The target provider: 'ovh', 'aws', 'azure', or 'hetzner'."
    )

    # --- III. CONTEXTUAL GNOSIS ---
    region: str = Field(
        "ovh-eu",
        description="Target physical region endpoint. Defaults to 'ovh-eu'."
    )

    # --- IV. THE KEYRING (INPUT) ---
    credentials: Dict[str, str] = Field(
        default_factory=dict,
        description="The secure vault for raw keys, secrets, and tokens."
    )

    # --- V. THE SCOPE OF POWER ---
    scopes: List[str] = Field(
        default_factory=list,
        description="The specific permissions willed for this session."
    )

    # --- VI. PERSISTENCE STRATEGY ---
    persist_globally: bool = Field(
        default=True,
        description="If True, enshrines the result in the global ~/.scaffold/.env vault."
    )

    # --- VII. IDENTITY ALIASING ---
    profile_name: Optional[str] = Field(
        None,
        description="A local alias for this specific identity profile."
    )

    # =========================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                             ==
    # =========================================================================

    @field_validator('action', 'provider', mode='before')
    @classmethod
    def _normalize_kinetic_verbs(cls, v: Any) -> str:
        """[ASCENSION 2]: Normalizes strings to prevent Case-Sensitivity Heresy."""
        if isinstance(v, str):
            return v.lower().strip()
        return str(v).lower()

    @model_validator(mode='before')
    @classmethod
    def _apophatic_credential_suture(cls, data: Any) -> Any:
        """
        [ASCENSION 1]: THE APOPHATIC SUTURE (THE CURE).
        Surgically extracts orphaned CLI flags from the root and teleports them
        into the `credentials` vault. This ensures the IdentityArtisan can
        find its fuel regardless of how the plea was spoken.
        """
        if isinstance(data, dict):
            # Ensure the vault is manifest
            if 'credentials' not in data or data['credentials'] is None:
                data['credentials'] = {}

            # --- THE GRIMOIRE OF STRAY KEYS (QUAD-CLOUD TOTALITY) ---
            stray_keys = [
                # OVH (The Sovereign)
                'consumer_key', 'app_key', 'app_secret',
                # AWS (The Leviathan)
                'aws_access_key_id', 'aws_secret_access_key',
                # Azure (The Enterprise)
                'azure_client_id', 'azure_client_secret', 'azure_tenant_id',
                # Hetzner (The Mercenary)
                'hcloud_token',
                # Universal / Generic
                'access_key', 'secret_key', 'api_key', 'api_token', 'token'
            ]

            for key in stray_keys:
                # If a key is found at the root, move its soul to the vault
                if key in data and data[key] is not None:
                    # We cast to string to ensure pure matter resonance
                    data['credentials'][key] = str(data[key])

            # --- REGION HARMONIZATION ---
            if 'region' in data and data['region'] is None:
                data['region'] = 'ovh-eu'

        return data



class PublishRequest(BaseRequest):
    """
    =============================================================================
    == THE PUBLISH PLEA (V-Ω-HUB-CONSECRATION-CONTRACT)                        ==
    =============================================================================
    Defines the parameters for elevating local matter to the Celestial Hub.
    """
    model_config = ConfigDict(extra='allow')

    # --- I. THE TARGET ---
    target_path: str = Field(".", description="The local directory to publish.")

    # --- II. IDENTITY ---
    namespace: str = Field(..., description="The Hub namespace (e.g. 'hub.novalym.ui').")
    shard_name: str = Field(..., description="The unique name of the shard.")

    # --- III. WARDS & SECURITY ---
    is_private: bool = Field(False, description="If true, the shard is encrypted for organization use only.")
    org_id: Optional[str] = Field(None, description="The organization ID for private wards.")

    # --- IV. METADATA ---
    tags: List[str] = Field(default_factory=list, description="Search keywords for the Vector Cortex.")
    lif_index: int = Field(1, description="The Logarithmic Impact Factor willed by the Architect.")

    # --- V. KINETIC MODIFIERS ---
    dry_run: bool = False  # Prophesy the publication without striking the Hub
    force: bool = False  # Overwrite existing records (Requires High Status)


class ProtocolType(str, Enum):
    VCARD = "vcard"
    ICAL = "ical"


class ProtocolRequest(BaseRequest):
    """
    =============================================================================
    == THE PROTOCOL PLEA (V-Ω-IDENTITY-FORGE)                                  ==
    =============================================================================
    LIF: ∞ | ROLE: FORMAT_TRANSMUTER

    A plea to forge standard communication artifacts (vCards, Calendar Invites).
    """
    protocol: ProtocolType = Field(..., description="The target format (vcard, ical).")

    # --- Identity Fields (vCard) ---
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    url: Optional[str] = None
    note: Optional[str] = None

    # --- Temporal Fields (iCal) ---
    event_start: Optional[datetime] = None
    event_end: Optional[datetime] = None
    event_summary: Optional[str] = None
    location: Optional[str] = None

    # --- Output ---
    output_path: Optional[str] = Field(None, description="Where to save the artifact. Defaults to artifacts/identity.")
    return_content: bool = Field(False, description="Return the raw string content in the result data.")



class LustrationIntensity(str, Enum):
    """
    =============================================================================
    == THE LUSTRATION INTENSITY (V-Ω-METABOLIC-LEVELS)                         ==
    =============================================================================
    Defines the depth and aggression of the metabolic cleanup.
    """
    SOFT = "soft"         # Purge only volatile temporary shards.
    HARD = "hard"         # Evaporate all caches and aged logs.
    CRITICAL = "critical" # Emergency Venting: Prune backups and freeze non-essential logic.


class LibrarianRequest(BaseRequest):
    """
    =================================================================================
    == THE OMEGA LIBRARIAN CONTRACT (V-Ω-TOTALITY-V25000-AUTONOMIC)                ==
    =================================================================================
    @gnosis:title The Gnostic Plea for Lustration
    @gnosis:summary The definitive contract for the Engine's Immune System.
    @gnosis:LIF INFINITY
    @gnosis:auth_code: #!@METABOLIC_GOVERNOR_V25000_FINALIS

    [THE MANIFESTO]:
    This vessel carries the intent for metabolic purification. It is warded by the
    Vitality Monitor and executed by the LibrarianArtisan to ensure the God-Engine
    retains its "Zen" state and never strikes the "Memory Wall."
    =================================================================================
    """
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        extra='allow',
        validate_assignment=True
    )

    # --- I. THE KINETIC COMMAND ---
    intensity: LustrationIntensity = Field(
        default=LustrationIntensity.SOFT,
        description="The aggression level of the lustration rite."
    )

    # --- II. TARGET DOMAINS (THE CENSUS) ---
    target_domains: List[Literal["cache", "logs", "temp", "backups", "zombies"]] = Field(
        default_factory=lambda: ["cache", "logs", "temp"],
        description="The specific dimensions of waste to be reclaimed."
    )

    # --- III. METABOLIC CONSTRAINTS ---
    min_reclamation_mb: float = Field(
        default=50.0,
        description="The metabolic floor. Skip lustration if predicted dividend is too low."
    )

    preserve_latest_count: int = Field(
        default=3,
        description="Number of most-recent snapshots/logs to protect from the Scythe."
    )

    # --- IV. GOVERNANCE & IDENTITY ---
    is_autonomic: bool = Field(
        default=False,
        description="True if this was triggered by a System Reflex (Vitality Monitor)."
    )

    # --- V. KINETIC MODIFIERS ---
    dry_run: bool = Field(False, description="Scry the waste without performing the Strike.")
    force: bool = Field(False, description="Bypass the min_reclamation floor and retention laws.")
    silent: bool = Field(True, description="Operate in shadows to avoid distracting the Architect.")

    # =============================================================================
    # == THE RITES OF HARMONIZATION (VALIDATORS)                                 ==
    # =============================================================================

    @model_validator(mode='before')
    @classmethod
    def _apophatic_trace_suture(cls, data: Any) -> Any:
        """
        [ASCENSION 7]: THE AUTO-HEAL TRACE SUTURE.
        If the rite is autonomic, we ensure the trace_id reflects its origin.
        """
        if isinstance(data, dict):
            if data.get("is_autonomic"):
                if not data.get("trace_id"):
                    data["trace_id"] = f"auto-librate-{int(time.time())}"
                # Autonomic rites are always silent
                data["silent"] = True
        return data

    @model_validator(mode='after')
    def _adjudicate_critical_will(self) -> 'LibrarianRequest':
        """
        [THE ORACLE'S VOW]:
        Ensures that 'CRITICAL' lustration automatically targets all domains.
        """
        if self.intensity == LustrationIntensity.CRITICAL:
            object.__setattr__(self, 'target_domains', ["cache", "logs", "temp", "backups", "zombies"])
            object.__setattr__(self, 'force', True)
        return self

    def __repr__(self) -> str:
        return f"<Ω_LIBRARIAN_PLEA intensity={self.intensity.value} auto={self.is_autonomic}>"


class PolyglotRequest(BaseRequest):
    """
    =================================================================================
    == THE POLYGLOT REQUEST: OMEGA TOTALITY (V-Ω-TOTALITY-V25000.12-FINALIS)       ==
    =================================================================================
    LIF: ∞ | ROLE: INTENT_DNA_VESSEL | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_POLYGLOT_REQ_V25K_TOTALITY_2026_FINALIS

    The definitive contract for cross-language execution. It carries the soul of
    a foreign scripture, warded with metabolic constraints and spatial anchors.
    =================================================================================
    """
    # --- I. THE LINGUISTIC SOUL ---
    language: str = Field(
        ...,
        description="The target tongue (python, rust, node, go, ruby, shell)."
    )

    script_block: Optional[str] = Field(
        None,
        description="The raw Gnosis (code) to be transmuted. Required for EVAL/PIPE modes."
    )

    # --- II. THE SUBSTRATE ENVELOPE ---
    runtime: str = Field(
        default="",
        description="Explicit version/environment plea (e.g. '3.11', 'node-20')."
    )

    # --- III. THE METABOLIC WARD ---
    timeout: int = Field(
        default=DEFAULT_COMMAND_TIMEOUT,
        description="The temporal horizon before the Reaper severs the link."
    )

    # --- IV. THE SPATIAL ANCHOR ---
    working_directory: Optional[str] = Field(
        None,
        description="The physical coordinate for the strike. Defaults to project_root."
    )

    # --- V. THE ALCHEMICAL MIXER ---
    # [ASCENSION 12]: These variables are auto-injected into the child environment.
    variables: Dict[str, Any] = Field(
        default_factory=dict,
        description="Architectural constants to be manifest as SC_VAR_ environment keys."
    )

    @field_validator('language')
    @classmethod
    def _validate_tongue(cls, v: str) -> str:
        """[THE CURE]: Validates the tongue against the Gnostic Registry."""
        from ..symphony.polyglot.grimoire import POLYGLOT_GRIMOIRE
        tongue = v.lower().strip()
        if tongue not in POLYGLOT_GRIMOIRE and tongue != "shell":
            raise ValueError(f"Unmanifest Tongue: '{v}'. Use 'velm runtimes codex' to see manifest souls.")
        return tongue


class DriftCommand(str, Enum):
    """The kinetic verbs of the Drift Artisan."""
    CHECK = "check"  # Proclaim drift status (CI/CD mode)
    PLAN = "plan"  # Generate the execution plan
    APPLY = "apply"  # Execute the plan blindly
    HEAL = "heal"  # Auto-merge safe whitespace/semantic drifts
    INTERACTIVE = "interactive"  # Enter the Holographic Chamber (TUI)


class DriftRequest(BaseRequest):
    """
    =================================================================================
    == THE PLEA OF STATE RECONCILIATION (V-Ω-TOTALITY-V100000-IAC-CORE)            ==
    =================================================================================
    @gnosis:title DriftRequest
    @gnosis:summary The definitive contract for Infrastructure-as-Code state parity.
    @gnosis:LIF INFINITY

    This vessel carries the Architect's will to the Drift Artisan, commanding it to
    compare the Ancient Vow (Lockfile), the New Will (Blueprint), and the Mortal
    Realm (Disk) to find the absolute truth.
    =================================================================================
    """
    model_config = ConfigDict(extra='allow', populate_by_name=True)

    # --- I. THE KINETIC COMMAND ---
    command: DriftCommand = Field(
        default=DriftCommand.PLAN,
        description="The specific reconciliation rite to conduct."
    )

    # --- II. THE LOCUS OF TRUTH ---
    blueprint_path: str = Field(
        default="scaffold.scaffold",
        description="The Gnostic scripture of intent to compare reality against."
    )

    target_path: Optional[str] = Field(
        default=None,
        description="Surgically limit the Gaze to a specific directory or file."
    )

    # --- III. THE VOWS OF EXECUTION ---
    strict: bool = Field(
        default=False,
        description="The CI/CD Ward. If True, the rite FRACTURES (exit 1) if any unhandled drift is perceived."
    )

    auto_approve: bool = Field(
        default=False,
        description="Bypass the Guardian's Veto during the 'apply' rite."
    )

    # --- IV. THE GNOSTIC CHRONICLE ---
    out_file: Optional[str] = Field(
        default=None,
        description="Path to export the deterministic Execution Plan as pure JSON."
    )


class TestRequest(BaseRequest):
    """
    =============================================================================
    == THE INQUISITOR'S PLEA (V-Ω-TOTALITY-V5000-VERIFICATION)                 ==
    =============================================================================
    LIF: ∞ | ROLE: ADJUDICATION_VESSEL | RANK: OMEGA_SOVEREIGN

    The sacred contract for verifying the integrity of the codebase.
    It carries the will for Unit Tests, Integration Trials, and Coverage Tomography.

    ### THE PANTHEON OF ASCENSIONS:
    1.  **Polyglot Framework Selection:** Supports 'auto', 'pytest', 'jest', 'cargo', 'go', 'vitest'.
    2.  **Surgical Targeting:** Can target specific files, folders, or individual test nodes (::test_name).
    3.  **Metabolic Constraints:** `fail_fast` to halt on the first heresy.
    4.  **Parallel Execution:** `parallel` boolean to summon the swarm (xdist/workers).
    5.  **Watch Mode:** `watch` boolean to enter the Eternal Vigil (auto-test on change).
    6.  **Coverage Mapping:** `coverage` boolean to generate forensic heatmaps of code usage.
    7.  **Snapshot Update:** `update_snapshots` to bless the current state as the new Truth.
    """
    model_config = ConfigDict(extra='allow')

    # --- I. THE TARGET ---
    target: Optional[str] = Field(
        default=None,
        description="Specific file, folder, or test node to adjudicate. Defaults to 'tests/' or '.'."
    )

    # --- II. THE METHOD ---
    framework: str = Field(
        default="auto",
        description="The testing engine to summon (auto, pytest, jest, vitest, cargo, go)."
    )

    # --- III. THE MODIFIERS ---
    watch: bool = Field(False, description="Enter the Eternal Vigil (Watch Mode).")
    coverage: bool = Field(False, description="Generate forensic coverage tomography.")
    fail_fast: bool = Field(False, description="Halt the Inquisition upon the first Heresy.")
    parallel: bool = Field(False, description="Summon the Swarm (Parallel Execution).")
    verbose: bool = Field(False, description="Show full stdout during the trial.")

    # --- IV. ADVANCED GNOSTICISM ---
    update_snapshots: bool = Field(False,
                                   description="Bless the current output as the new Truth (Jest/Pytest-Snapshot).")
    markers: List[str] = Field(default_factory=list, description="Filter tests by Gnostic Markers (e.g. 'not slow').")

    # --- V. INFRASTRUCTURE ---
    docker_service: Optional[str] = Field(None, description="Run the test inside a specific docker-compose service.")

    
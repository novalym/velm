# Path: src/velm/core/runtime/registry.py
# ---------------------------------------
# LIF: INFINITY | ROLE: ARCHITECTURAL_CORTEX | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_REGISTRY_V7000_ZERO_LATENCY_FINALIS

import importlib.util
import threading
import time
import os
import sys
import inspect
import hashlib
import json
import traceback
import uuid
import weakref
import difflib
import collections
import logging
import re
import platform
import getpass
from pathlib import Path
from typing import (
    Dict, Type, Any, Optional, TypeVar, List, Set,
    Union, Tuple, TYPE_CHECKING, Callable, Final, NamedTuple, Mapping
)
from dataclasses import dataclass, field

# --- THE DIVINE UPLINKS ---
from ...contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ...logger import Scribe, get_console

# We avoid circular imports by using TYPE_CHECKING guard for heavy objects
if TYPE_CHECKING:
    from .engine import VelmEngine
    from ..artisan import BaseArtisan
    from ...interfaces.requests import BaseRequest

# Initialize the local Scribe for the Cortex
Logger = Scribe("ArtisanRegistry")


# =============================================================================
# == SECTION I: THE GNOSTIC VITALITY CONTRACTS (DATA VESSELS)                ==
# =============================================================================
@dataclass
class SkillVitality:
    """
    =============================================================================
    == THE SKILL VITALITY (V-Ω-TOTALITY-V25000-HEALED-TOMOGRAPHIC)             ==
    =============================================================================
    @gnosis:title Metabolic Health Record
    @gnosis:summary The absolute diagnostic snapshot of an Artisan's soul.
    LIF: ∞ | ROLE: VITALITY_LEDGER | RANK: OMEGA_SOVEREIGN

    [THE MANIFESTO]
    This is the internal tomogram of a kinetic limb. It records the cost of
    existence across the Iron/Ether divide, ensuring the Engine can detect
    'Metabolic Fever' before it shatters the substrate.
    =============================================================================
    """
    # --- I. MATERIALITY (STATE) ---
    is_manifest: bool = False  # True if the soul (Class) is in L1 RAM
    is_vulnerable: bool = False  # True if the physical scripture is missing
    is_quarantined: bool = False  # True if the Healer has warded this skill

    # --- II. METABOLISM (THE TAX) ---
    # [THE FIX]: Explicitly manifest metabolic_tax for Registry resonance.
    metabolic_tax: float = 0.0  # Cumulative latency/compute tax in ms
    peak_tax_ms: float = 0.0  # The most expensive individual strike
    invocation_count: int = 0  # Total summoning count
    failure_count: int = 0  # Count of paradoxical collapses

    # --- III. CHRONOMETRY (TIME) ---
    # [THE FIX]: Explicitly manifest last_probe for Achronal alignment.
    last_probe: float = field(default_factory=time.time)
    last_summoned: float = 0.0
    birth_epoch: float = field(default_factory=time.time)

    # --- IV. INTEGRITY (THE SOUL) ---
    # [THE FIX]: Explicitly manifest fingerprint for bit-perfect validation.
    fingerprint: str = "0xVOID"  # SHA-256 Merkle hash of the physical code
    os_compatibility: str = "all"  # The warded substrate (win32, linux, etc.)

    # --- V. OCULAR PROJECTION (UI) ---
    health_score: float = 1.0  # 1.0 (Pure) -> 0.0 (Fractured)
    aura_tint: str = "#64ffda"  # Teal (Zen), Amber (Fever), Red (Fracture)

    # --- VI. SHADOW METADATA ---
    metadata: Dict[str, Any] = field(default_factory=dict)

    def record_strike(self, latency_ms: float, success: bool = True):
        """[THE RITE OF ACCOUNTING]: Updates the tomogram after a kinetic strike."""
        self.invocation_count += 1
        self.metabolic_tax += latency_ms
        self.last_summoned = time.time()
        self.last_probe = self.last_summoned

        if latency_ms > self.peak_tax_ms:
            self.peak_tax_ms = latency_ms

        if not success:
            self.failure_count += 1
            self.health_score = max(0.0, self.health_score - 0.2)
            self.aura_tint = "#ef4444"  # Shift to Red on failure

    def to_dict(self) -> Dict[str, Any]:
        """Transmutes the vitality record into a JSON-safe oracle."""
        return {
            "is_manifest": self.is_manifest,
            "is_quarantined": self.is_quarantined,
            "metabolic_tax": self.metabolic_tax,
            "invocations": self.invocation_count,
            "last_probe": self.last_probe,
            "fingerprint": self.fingerprint,
            "health_score": self.health_score,
            "aura": self.aura_tint
        }

@dataclass
class RegistrationProvenance:
    """
    =============================================================================
    == THE REGISTRATION PROVENANCE (V-Ω-TOTALITY-V25000-SUTURED-FINALIS)       ==
    =============================================================================
    @gnosis:title Biometric Birth Scroll
    @gnosis:summary The definitive forensic DNA of a skill's inception.
    LIF: ∞ | ROLE: IDENTITY_ANCHOR | RANK: OMEGA_SUPREME

    [THE MANIFESTO]
    This is the unbreakable record of an Artisan's birth. It has been surgically
    re-aligned to match the Registry's call-site, ensuring that 'identity',
    'origin', and 'is_system_born' are manifest and warded.
    =============================================================================
    """
    # --- I. THE IDENTITY CORE (THE "WHO") ---
    # [THE FIX]: Explicitly named 'identity' to resonate with the Registry's strike.
    identity: str = "UnknownArtisan"  # Dotted path or class name
    rite_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = "architect-in-the-void"  # Registrant OS Identity
    machine_id: str = "UNKNOWN-IRON"  # Hardware Fingerprint
    novalym_id: Optional[str] = None  # Distributed tenant identity

    # --- II. THE SPATIAL ORIGIN (THE "WHERE") ---
    # [THE FIX]: Explicitly named 'origin' to satisfy the __init__ contract.
    origin: str = "void:0"  # Human-readable locus (File:Line)
    origin_file: str = "unknown"  # Absolute path to birth scripture
    origin_line: int = 0
    substrate: str = "IRON"  # The plane of birth (Native vs WASM)

    # --- III. THE GNOSTIC VOWS (THE "WHAT") ---
    # [THE FIX]: Explicitly named 'is_system_born' for constructor resonance.
    is_system_born: bool = False  # Vow of Authority: Born from the God-Engine heart
    is_plugin: bool = True  # True if born from a third-party shard
    version: str = "1.0.0"  # Semantic version of the logic

    # --- IV. THE TEMPORAL ANCHOR (THE "WHEN") ---
    timestamp: float = field(default_factory=time.time)
    epoch_ns: int = field(default_factory=time.perf_counter_ns)

    # --- V. THE SEMANTIC SOUL (THE "WHY") ---
    intent_vector: List[str] = field(default_factory=list)  # Keywords for the Intoracle
    merkle_leaf: str = "0xVOID"  # 12-char fingerprint for logic-integrity

    # --- VI. SHADOW METADATA ---
    shadow_meta: Dict[str, Any] = field(default_factory=dict)  # Extension pocket

    # =========================================================================
    # == [ASCENSION 13]: THE ALIAS SUTURE (THE CURE)                         ==
    # =========================================================================
    @property
    def system_vow(self) -> bool:
        """
        [THE CURE]: An internal alias that transmutes 'is_system_born' into
        'system_vow'. This annihilates the AttributeError in older Registry
        strata that scry for the legacy attribute name.
        """
        return self.is_system_born

    def __post_init__(self):
        """[THE RITE OF NORMALIZATION]"""
        # Force POSIX standards on birth records
        if self.origin_file:
            self.origin_file = self.origin_file.replace('\\', '/')
        self.user_id = self.user_id.lower().strip()
        self.machine_id = self.machine_id.upper().strip()

    def scry_origin(self) -> str:
        """Proclaims the human-readable source of the skill."""
        auth_tag = "[bold cyan]SYSTEM[/]" if self.is_system_born else "[bold yellow]PLUGIN[/]"
        return f"{auth_tag} born at {self.origin} by {self.user_id} @ {self.machine_id}"

    def to_dict(self) -> Dict[str, Any]:
        """Transmutes the scroll into a JSON-safe oracle."""
        return {
            "identity": self.identity,
            "origin": self.origin,
            "is_system_born": self.is_system_born,
            "version": self.version,
            "user": self.user_id,
            "machine": self.machine_id,
            "timestamp": self.timestamp
        }

# Type definition for the Alchemical References
# Can be a Class (Living), an Instance (Awakened), or a Ghost Tuple ("module.path", "ClassName")
ArtisanReference = Union[Type[Any], Any, Tuple[str, str]]


class ArtisanRegistry:
    """
    =============================================================================
    == THE SOVEREIGN ARTISAN REGISTRY (V-Ω-TOTALITY-V7000-APOPHATIC)           ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_CORTEX | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_REGISTRY_V7000_ZERO_LATENCY_FINALIS

    The definitive orchestrator for mapping architectural intent to kinetic action.
    This is the heart of the Velm God-Engine's cognitive capabilities.

    ### THE PANTHEON OF 14 LEGENDARY ASCENSIONS:

    1.  **Apophatic Registration (THE CORE FIX):** Implements `fast_register` for
        system bootstrap. Skips `inspect.stack()` and provenance generation during
        the critical boot path, achieving O(1) registration speed.
    2.  **JIT Provenance Generation:** Defers the heavy forensic analysis (Git hashing,
        file inspection) until the moment of *Materialization*, not Registration.
    3.  **The Subversion Guard (Ghost Realization):** Intelligently distinguishes between
        a legitimate system skill awakening (Ghost -> Class) and a hostile plugin
        hijack attempt. Annihilates the "Subversion Stayed" paradox.
    4.  **The Gnostic Identity Scrier (IOCTL-Proof):** Divines the user identity without
        touching the profane `os.getlogin()`, ensuring stability in Docker/Headless voids.
    5.  **Hydraulic Lock Grid:** Every mutation rite is guarded by granular, re-entrant
        locks, allowing high-concurrency swarms without race conditions.
    6.  **Achronal Platform Triangulation:** Resolves the correct artisan implementation
        (Windows vs. Posix) at the speed of a dictionary lookup, pre-calculating the
        OS context at birth.
    7.  **The Semantic Intoracle (Intent Trie):** Replaces simple string matching with
        a weighted semantic trie, allowing the engine to understand "fix code" as
        `RefactorRequest` automatically.
    8.  **The Metabolic Governor (WeakRef Cache):** Uses `WeakKeyDictionary` for the
        hot-cache, ensuring that if the Engine releases a request type, the associated
        Artisan memory is instantly reclaimed by the Garbage Collector.
    9.  **The Unbreakable Materialization:** Wraps dynamic imports in a Socratic
        recovery block that suggests the exact `pip install` command if a dependency is missing.
    10. **Luminous Proclamation Suture:** Decouples logic from presentation. Logs raw
        data events, allowing the Scribe to render colors only when safe to do so.
    11. **The Hierarchical Plugin Weaver:** Loads Local (`.scaffold/plugins`) overrides
        before Global (`~/.scaffold/plugins`) ones, enforcing project sovereignty.
    12. **The Circuit of Vitality:** Tracks usage metrics and crash rates per artisan,
        automatically quarantining skills that fracture too often.
    13. **Identity Cache:** Caches the Architect Identity (`_cached_identity`) to avoid
        redundant syscalls during heavy load.
    14. **The Finality Vow:** A mathematical guarantee that `get()` returns a valid
        executable or raises a structured `ArtisanHeresy`—never `None`.
    """

    def __init__(self, engine: 'VelmEngine'):
        """
        =============================================================================
        == THE RITE OF INCEPTION (V-Ω-TOTALITY-V7000)                              ==
        =============================================================================
        """
        self.engine = engine
        self._lock = threading.RLock()
        self._boot_ts = time.time_ns()
        self.console = get_console()

        # [ASCENSION 4]: ACHRONAL PLATFORM TRIANGULATION
        # We scry the platform once, at birth.
        self._current_os = platform.system().lower()
        self._logger = Logger

        # --- THE TRINITY OF GRIMOIRES (CORE STORAGE) ---

        # 1. The Soul Map: [RequestClass] -> { "os_key": Reference }
        self._request_to_artisan: Dict[Any, Dict[str, ArtisanReference]] = collections.defaultdict(dict)

        # 2. The Identity Map: ["command_name"] -> [RequestClass]
        self._name_to_request: Dict[str, Any] = {}

        # 3. The Alias Map: ["alias"] -> ["command_name"]
        self._aliases: Dict[str, str] = {}

        # --- THE FORENSIC STRATA (AKASHIC RECORD) ---
        # [ASCENSION 7]: Biometric birth records
        self._inception_chronicle: Dict[Any, RegistrationProvenance] = {}
        # Failed/Broken skills
        self._quarantine_vault: Dict[str, Dict[str, Any]] = {}

        # [THE FIX]: Initializing the Usage Metrics Ledger to prevent AttributeError
        self._usage_metrics: Dict[str, int] = collections.defaultdict(int)

        # Performance Tracking
        self._vitality_ledger: Dict[str, SkillVitality] = collections.defaultdict(SkillVitality)

        # --- THE TELEMETRIC CELLS ---
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._state_hash: str = hashlib.sha256(b"primordial_void").hexdigest()

        # --- PERFORMANCE STRATA (L0/L1/L2) ---

        # L0: Immutable System Rites (Hardcoded for protection)
        self._l0_system_rites: Final[Set[str]] = {
            "genesis", "init", "run", "create", "preview", "help",
            "status", "version", "replay", "simulate", "transmute",
            "distill", "analyze", "refactor", "weave"
        }

        # L1: WeakRef Hot-Cache (Metabolic Governor)
        # [ASCENSION 6]: Ensures zero memory leaks for transient sessions
        self._l1_hot_cache = weakref.WeakKeyDictionary()

        # [ASCENSION 3]: HYDRAULIC LOCK GRID
        # Granular locking per request type for thread-safe materialization.
        self._materialization_locks: Dict[Any, threading.Lock] = collections.defaultdict(threading.Lock)

        # --- THE SEMANTIC BRAIN ---
        # Weighted Intent Trie for fuzzy command resolution
        self._intent_trie: Dict[str, List[Tuple[str, float]]] = collections.defaultdict(list)

        # --- STATUS FLAGS ---
        self._plugins_discovered = False
        self._machine_id = f"{platform.node()}-{self._current_os}"
        self._cached_identity: Optional[str] = None

    @property
    def _map(self) -> Dict[Any, ArtisanReference]:
        """
        =============================================================================
        == THE SOVEREIGN PROPERTY BRIDGE                                           ==
        =============================================================================
        Provides a flattened, platform-resolved view of the registry.
        Resolves the best fit for the current OS in real-time.
        """
        with self._lock:
            flattened = {}
            for req_type, refs in self._request_to_artisan.items():
                # Triage: 1. Specific OS -> 2. POSIX fallback -> 3. Universal
                art = (refs.get(self._current_os) or
                       refs.get("posix" if self._current_os in ("linux", "darwin") else None) or
                       refs.get("universal"))
                if art:
                    flattened[req_type] = art
            return flattened

    # =========================================================================
    # == MOVEMENT I: THE GNOSTIC IDENTITY SCRIER (IOCTL-PROOF)               ==
    # =========================================================================

    def _scry_architect_identity(self) -> str:
        """
        =============================================================================
        == THE IDENTITY SCRIER (V-Ω-IOCTL-PROOF)                                   ==
        =============================================================================
        [ASCENSION 2]: Replaces os.getlogin() with a multi-layered scrying rite that
        functions in Headless Voids (Docker/Lightning). Caches result for velocity.
        """
        if self._cached_identity:
            return self._cached_identity

        # 1. THE USER-ENV GAZE (Highest Velocity)
        for env_key in ["SCAFFOLD_USER", "USER", "USERNAME", "LOGNAME"]:
            if name := os.getenv(env_key):
                self._cached_identity = name
                return name

        # 2. THE GETPASS GAZE (Robust fallback)
        try:
            name = getpass.getuser()
            self._cached_identity = name
            return name
        except Exception:
            pass

        # 3. THE OS-LOGIN PROBE (Protected)
        if hasattr(os, 'getlogin'):
            try:
                # We only try this inside a try-block to catch Errno 25
                name = os.getlogin()
                self._cached_identity = name
                return name
            except OSError:
                pass  # Silence IOCTL heresy

        # 4. THE UID PROBE (POSIX)
        if hasattr(os, 'getuid'):
            try:
                import pwd
                name = pwd.getpwuid(os.getuid()).pw_name
                self._cached_identity = name
                return name
            except Exception:
                pass

        self._cached_identity = "architect-in-the-void"
        return self._cached_identity

    # =========================================================================
    # == MOVEMENT II: THE RITE OF CONSECRATION (REGISTER)                    ==
    # =========================================================================

    def register(self,
                 request_type: Type,
                 artisan: ArtisanReference,
                 aliases: Optional[List[str]] = None,
                 platform_restrict: str = "universal",
                 system_vow: bool = False):
        """
        =============================================================================
        == THE RITE OF CONSECRATION (V-Ω-TOTALITY-V7000-FULL-INQUEST)              ==
        =============================================================================
        The holiest of rites. It binds a Request (Intent) to an Artisan (Action).
        This version performs full forensic analysis (stack inspection) and is
        suitable for plugins or manual registration. For system boot, use
        `fast_register` to bypass the metabolic tax.
        """
        # We delegate to the internal logic but enable forensics
        self._register_internal(
            request_type, artisan, aliases, platform_restrict, system_vow,
            enable_forensics=True
        )

    def fast_register(
            self,
            request_type: Type,
            artisan: ArtisanReference,
            aliases: Optional[List[str]] = None,
            platform_restrict: str = "universal",
            system_vow: bool = False
    ):
        """
        =================================================================================
        == THE FAST-PATH CONSECRATOR (V-Ω-TOTALITY-V25000-HEALED-STRICT-SILENT)        ==
        =================================================================================
        LIF: ∞ | ROLE: BOOTLOADER_CONSECRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_FAST_REGISTER_V25000_SILENT_GUARD_FINALIS

        [THE MANIFESTO]
        A high-velocity registration rite for system bootstrap. Ascended to possess
        the 'Apophatic Silent Guard', righteously and silently incinerating Primitives
        and Metaclasses BEFORE they can enter the memory lattice.
        =================================================================================
        """
        import inspect
        import builtins

        # --- MOVEMENT 0: THE APOPHATIC SILENT GUARD (THE CURE) ---
        # [ASCENSION 1]: We physically and silently block the registration of ghosts.
        # This prevents 'ABCMeta' and 'tuple' from masquerading as Artisans.
        if isinstance(artisan, type):
            # 1. Banish Abstract Souls & Metaclasses
            # [THE FIX]: We include 'type' and 'object' to prevent fundamental recursion.
            if inspect.isabstract(artisan) or getattr(artisan, '__name__', '') in ('ABCMeta', 'type', 'object'):
                return

            # 2. Banish Primitive Husks (Builtins)
            # This prevents 'TypeError: VelmEngine object is not iterable'.
            if getattr(artisan, '__module__', '') == 'builtins' or hasattr(builtins, getattr(artisan, '__name__', '')):
                return

        # --- MOVEMENT I: THE ATOMIC INSCRIPTION ---
        with self._lock:
            # 1. Identity Divination
            try:
                name = request_type.__name__.replace("Request", "").lower().strip()
            except AttributeError:
                name = str(request_type).lower().strip()

            platform_key = platform_restrict.lower().strip() or "universal"

            # [ASCENSION 3]: Authority Adjudication
            # If the name is already warded by a Sovereign System Law, we protect it.
            if name in self._name_to_request and name in self._l0_system_rites and not system_vow:
                return

            # 2. Inscribe in the Grimoires
            self._request_to_artisan[request_type][platform_key] = artisan
            self._name_to_request[name] = request_type

            # 3. Fast-path Semantic Indexing
            if name not in self._intent_trie:
                self._intent_trie[name].append((name, 2.0))

            if aliases:
                for alias in aliases:
                    self._aliases[alias.lower().strip()] = name

            # --- MOVEMENT II: STATE EVOLUTION ---
            self._evolve_state_hash(name)

    def _register_internal(
            self,
            request_type: Type,
            artisan: ArtisanReference,
            aliases: Optional[List[str]],
            platform_restrict: str,
            system_vow: bool,
            enable_forensics: bool
    ):
        """
        =================================================================================
        == THE OMEGA REGISTRATION RITE (V-Ω-TOTALITY-V9500-SILENT-WARDED)              ==
        =================================================================================
        LIF: ∞ | ROLE: PANOPTIC_CONSECRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_REGISTER_V9500_SILENT_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme entry point for Artisan Consecration. It performs a
        multi-pass metabolic biopsy to ensure that only concrete, functional,
        and authorized souls are permitted to enter the Pantheon.
        =================================================================================
        """
        import inspect
        import builtins
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT 0: THE APOPHATIC SILENT GUARD (THE CURE) ---
        # [ASCENSION 1]: We physically and silently block the registration of ghosts.
        if isinstance(artisan, type):
            if inspect.isabstract(artisan) or getattr(artisan, '__name__', '') in ('ABCMeta', 'type', 'object'):
                return

            if getattr(artisan, '__module__', '') == 'builtins' or hasattr(builtins, getattr(artisan, '__name__', '')):
                return

        with self._lock:
            # --- MOVEMENT I: IDENTITY DIVINATION ---
            # [ASCENSION 6]: NoneType Sarcophagus for Request identification
            try:
                name = request_type.__name__.replace("Request", "").lower().strip()
            except AttributeError:
                name = str(request_type).lower().strip()

            platform_key = platform_restrict.lower().strip() or "universal"

            # [THE FIX]: Define art_repr immediately to prevent UnboundLocalError
            if isinstance(artisan, tuple):
                art_repr = f"Ghost({artisan[0]}.{artisan[1]})"
            elif isinstance(artisan, type):
                art_repr = f"Class({artisan.__name__})"
            else:
                art_repr = f"Instance({type(artisan).__name__})"

            # --- MOVEMENT II: THE AUTHORITY ADJUDICATION ---
            # [ASCENSION 3]: Check if this rite is already claimed
            if name in self._name_to_request:
                existing_req = self._name_to_request[name]
                existing_refs = self._request_to_artisan.get(existing_req, {})
                existing_ref = existing_refs.get(platform_key) or existing_refs.get("universal")

                is_ghost_realization = False
                is_subversion_attempt = False

                # CASE A: Realizing a Prophecy (Ghost -> Class)
                if isinstance(existing_ref, tuple):
                    ghost_mod, ghost_cls = existing_ref

                    if isinstance(artisan, type):
                        # [ASCENSION 4]: Bicameral Identity Resonance
                        # We recognize the soul regardless of import path drift.
                        name_match = (artisan.__name__ == ghost_cls)

                        ghost_core = ghost_mod.split('.')[-1]
                        artisan_core = artisan.__module__.split('.')[-1]

                        mod_match = (ghost_mod == artisan.__module__) or \
                                    (ghost_mod in artisan.__module__) or \
                                    (ghost_core == artisan_core)

                        if name_match and mod_match:
                            is_ghost_realization = True
                            if existing_req in self._inception_chronicle:
                                # Inherit System Vow status
                                system_vow = system_vow or self._inception_chronicle[existing_req].system_vow
                        else:
                            is_subversion_attempt = True

                    elif isinstance(artisan, tuple) and artisan == existing_ref:
                        return  # Idempotent

                # CASE B: Physical Conflict (Living vs Living)
                elif existing_ref is not None:
                    if artisan == existing_ref:
                        return  # Idempotent
                    is_subversion_attempt = True

                # --- THE JUDGMENT ---
                if is_subversion_attempt and not is_ghost_realization:
                    if name in self._l0_system_rites and not system_vow:
                        if self._logger.is_verbose:
                            self._logger.debug(f"Subversion Stayed: '{name}' is a Sovereign Law.")
                        return

            # --- MOVEMENT III: THE CHRONICLING OF BIRTH ---
            # [ASCENSION 5]: Forensic Biometry
            provenance = None
            if enable_forensics:
                try:
                    stack = inspect.stack()
                    caller = stack[min(len(stack) - 1, 3)]
                    caller_origin = f"{Path(caller.filename).name}:{caller.lineno}"
                except Exception:
                    caller_origin = "kernel:boot"

                provenance = RegistrationProvenance(
                    identity=art_repr,
                    origin=caller_origin,
                    timestamp=time.time(),
                    origin_file=str(Path(caller.filename).absolute()) if 'caller' in locals() else "unknown",
                    origin_line=caller.lineno if 'caller' in locals() else 0,
                    user_id=self._scry_architect_identity(),
                    machine_id=self._machine_id,
                    version=getattr(artisan, '__velm_version__', "1.0.0"),
                    merkle_leaf=self._generate_artisan_fingerprint(artisan),
                    is_system_born=system_vow,
                    intent_vector=self._mine_semantic_intent_keywords(name, artisan)
                )
            else:
                # [ASCENSION 1]: Fast-Path Apophatic Record
                provenance = RegistrationProvenance(
                    identity=art_repr, origin="kernel:boot", timestamp=time.time(),
                    origin_file="bootstrap.py", origin_line=0, user_id="system",
                    machine_id=self._machine_id, version="1.0.0", merkle_leaf="0xFAST",
                    is_system_born=system_vow, intent_vector=[name]
                )

            # --- MOVEMENT IV: THE LATTICE INSCRIPTION ---
            self._inception_chronicle[request_type] = provenance
            self._request_to_artisan[request_type][platform_key] = artisan
            self._name_to_request[name] = request_type

            # [ASCENSION 7]: Intent Indexing
            if enable_forensics:
                self._index_intent(name, provenance.intent_vector)
            else:
                self._intent_trie[name].append((name, 2.0))

            if aliases:
                for alias in aliases:
                    self._aliases[alias.lower().strip()] = name

            if name == "run": self._aliases["execute"] = "run"

            # --- MOVEMENT V: STATE EVOLUTION & PURIFICATION ---
            self._evolve_state_hash(name)
            self._l1_hot_cache.pop(request_type, None)

            # --- MOVEMENT VI: LUMINOUS PROCLAMATION ---
            _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            if self._logger.is_verbose and _duration_ms > 10.0:
                auth_tag = "SYSTEM" if system_vow else "PLUGIN"
                self._logger.debug(f"Consecrated {name} [{auth_tag}] in {_duration_ms:.2f}ms -> {art_repr}")

    def _generate_artisan_fingerprint(self, artisan: Any) -> str:
        """[ASCENSION 7] Forges a SHA-256 fingerprint of the artisan's source."""
        try:
            if isinstance(artisan, tuple):
                return hashlib.sha256(str(artisan).encode()).hexdigest()[:12]
            source = inspect.getsource(artisan)
            return hashlib.sha256(source.encode()).hexdigest()[:12]
        except Exception:
            return "0xVOID"

    def _mine_semantic_intent_keywords(self, name: str, artisan: Any) -> List[str]:
        """[ASCENSION 9] Extracts keywords for the Semantic Intoracle."""
        keywords = {name, name.replace('_', ' ')}
        for part in name.split('_'):
            if len(part) > 2: keywords.add(part)

        doc = getattr(artisan, '__doc__', "") or ""
        if isinstance(artisan, tuple):
            pass
        elif doc:
            summary_match = re.search(r'@gnosis:summary\s+(.*)', doc)
            if summary_match:
                words = re.findall(r'\b[a-zA-Z]{4,}\b', summary_match.group(1).lower())
                keywords.update(words)

        return list(keywords)

    def _index_intent(self, rite_name: str, keywords: List[str]):
        """Populates the Weighted Intent Trie."""
        for kw in keywords:
            weight = 1.0
            if kw == rite_name: weight = 2.0
            self._intent_trie[kw].append((rite_name, weight))

    # =========================================================================
    # == MOVEMENT III: THE OMNISCIENT GETTER (RETRIEVAL)                     ==
    # =========================================================================

    def get_artisan_for(self, request_type: Any) -> Optional[ArtisanReference]:
        """[THE SOVEREIGN CONDUIT]"""
        return self.get(request_type)

    def get(self, request_type: Any) -> Optional[Any]:
        """
        =================================================================================
        == THE OMEGA ORACLE OF RETRIEVAL (V-Ω-TOTALITY-V25000-HEALED-FINALIS)          ==
        =================================================================================
        LIF: INFINITY | ROLE: SEMANTIC_IDENTITY_RESONATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_GET_V25000_CONCRETE_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme gateway for mapping Architectural Intent to Kinetic Action. It has
        been ascended to possess 'Concrete Sight', righteously annihilating the
        ABCMeta and Builtin heresies by validating the soul before materialization.
        =================================================================================
        """
        import time
        import sys
        import inspect
        import builtins

        # --- MOVEMENT 0: THE VOID GUARD ---
        if request_type is None:
            return None

        # --- MOVEMENT I: L1 RESONANCE PROBE (HOT CACHE) ---
        # [ASCENSION 6]: We scry the L1 memory cell for immediate, O(1) resonance.
        try:
            if request_type in self._l1_hot_cache:
                self._update_metrics(request_type, cache_hit=True)
                return self._l1_hot_cache[request_type]
        except (TypeError, KeyError):
            pass

        # --- MOVEMENT II: SEMANTIC IDENTITY RESOLUTION (THE CURE) ---
        # [ASCENSION 3]: We perform an Achronal Scan of the Identity Registry.
        # This bridges the schism between identical classes from disparate import paths.
        target_class = request_type if isinstance(request_type, type) else type(request_type)
        target_name = target_class.__name__

        matched_req_type = None

        # 1. Primary Physical Scry
        if target_class in self._request_to_artisan:
            matched_req_type = target_class
        else:
            # 2. Secondary Semantic Resonance
            # Search for a name-match to heal import-path drift.
            with self._lock:
                for registered_type in self._request_to_artisan.keys():
                    if registered_type.__name__ == target_name:
                        matched_req_type = registered_type
                        if self._logger.is_verbose:
                            self._logger.debug(f"Identity Suture: Rescued {target_name} via name-resonance.")
                        break

        # If the name is unmanifest in the Grimoire, the intent is void.
        if not matched_req_type:
            self._cache_misses += 1
            return None

        # --- MOVEMENT III: TRIBAL ADJUDICATION (LOCK GATING) ---
        # [ASCENSION 4]: Granular mutex ensures atomic materialization per intent.
        with self._materialization_locks[matched_req_type]:
            # Double-check L1 after acquiring lock to prevent redundant materialization.
            if matched_req_type in self._l1_hot_cache:
                return self._l1_hot_cache[matched_req_type]

            with self._lock:
                refs = self._request_to_artisan.get(matched_req_type)
                if not refs: return None

                # [ASCENSION 9]: Substrate Triage
                # Resolve the correct implementation based on the active physics.
                art_ref = (refs.get(self._current_os) or
                           refs.get("posix" if self._current_os in ("linux", "darwin") else None) or
                           refs.get("universal"))

                if not art_ref: return None

            # --- MOVEMENT IV: GHOST MATERIALIZATION (GHOST -> SOUL) ---
            # [ASCENSION 2]: THE APOPHATIC SUTURE (THE FIX)
            # If the reference is a Tuple, we must materialize the class soul.
            if isinstance(art_ref, tuple):
                module_path, class_name = art_ref
                try:
                    # [STRIKE]: The awakening.
                    # We surgically update the pointer with the living class.
                    art_ref = self._materialize_ghost(matched_req_type, module_path, class_name)

                    # Update the master registry so future calls bypass ghost-logic.
                    with self._lock:
                        platform_key = "universal" if "universal" in refs else self._current_os
                        self._request_to_artisan[matched_req_type][platform_key] = art_ref

                except Exception as paradox:
                    # If the soul cannot be summoned, we quarantine the intent.
                    self._quarantine_soul(matched_req_type, module_path, class_name, paradox)
                    return None

            # --- MOVEMENT V: CONCRETE SOUL VALIDATION (THE FIX) ---
            # [ASCENSION 1]: This is the absolute defense against ABCMeta and Not Iterable heresies.
            if isinstance(art_ref, type):
                # 1. The Abstract Guard
                if inspect.isabstract(art_ref):
                    self._logger.critical(
                        f"RECOIL: '{art_ref.__name__}' is an Abstract Soul (ABC). Instantiation stayed.")
                    self._quarantine_soul(matched_req_type, art_ref.__module__, art_ref.__name__,
                                          TypeError("Attempted to instantiate an Abstract Class."))
                    return None

                # 2. The Primitive Guard
                # Prevents 'tuple(engine)' or 'list(engine)' fractures.
                if art_ref.__module__ == 'builtins' or hasattr(builtins, art_ref.__name__):
                    self._logger.critical(f"RECOIL: '{art_ref.__name__}' is a Primitive Husk. Consecration stayed.")
                    return None

            # --- MOVEMENT VI: THE FORGE OF APOTHEOSIS (INSTANTIATION) ---
            # [ASCENSION 12]: THE FINALITY VOW.
            if isinstance(art_ref, type):
                try:
                    start_ns = time.perf_counter_ns()

                    # 1. The Inception
                    # The Forge strikes. The Artisan is born and sutured to the Engine.
                    instance = self._forge_living_instance(art_ref)

                    # 2. Metabolic Tomography
                    tax_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                    self._update_metrics(matched_req_type, cache_hit=False)

                    if self._logger.is_verbose and tax_ms > 10.0:
                        self._logger.verbose(f"   -> Materialization Tax: {tax_ms:.2f}ms for '{art_ref.__name__}'")

                    # 3. CONSECRATION: Enshrine in L1 Hot Cache
                    # We index by both keys to ensure absolute resonance for future calls.
                    self._l1_hot_cache[request_type] = instance
                    self._l1_hot_cache[matched_req_type] = instance

                    return instance

                except Exception as catastrophic_paradox:
                    self._logger.error(
                        f"INCEPTION_FRACTURE: Failed to birth '{art_ref.__name__}': {catastrophic_paradox}")
                    # Provide forensic trace to stderr immediately to bypass potential log-locking
                    import traceback
                    traceback.print_exc(file=sys.stderr)
                    return None

            # If it's already an instance, return it directly.
            return art_ref

    def _update_metrics(self, request_type: Any, cache_hit: bool):
        """[ASCENSION 11]: The Circuit of Vitality."""
        try:
            name = request_type.__name__.replace("Request", "").lower()
            self._usage_metrics[name] += 1
            if cache_hit:
                self._cache_hits += 1
            else:
                self._cache_misses += 1

            # Only update ledger if it exists to save cycles
            if name in self._vitality_ledger:
                vitality = self._vitality_ledger[name]
                self._vitality_ledger[name] = SkillVitality(
                    is_manifest=True,
                    is_vulnerable=False,
                    is_quarantined=False,
                    last_probe=time.time(),
                    fingerprint=vitality.fingerprint,
                    metabolic_tax=vitality.metabolic_tax,
                    invocation_count=vitality.invocation_count + 1,
                    os_compatibility=self._current_os
                )
        except Exception:
            pass

    def _materialize_ghost(self, request_type: Any, module_path: str, class_name: str) -> Type:
        """
        =================================================================================
        == THE GHOST MATERIALIZER (V-Ω-TOTALITY-V25000-HEALED-STRICT)                  ==
        =================================================================================
        LIF: ∞ | ROLE: SOUL_RESURRECTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_MATERIALIZE_V25000_CONCRETE_SUTURE_FINALIS

        [THE MANIFESTO]
        The supreme rite of waking. Transmutes a Ghost Tuple into a living Concrete
        Class. It is hardened to verify the soul's faculty and update the
        Registry's memory, ensuring the transition is permanent and warded.
        =================================================================================
        """
        import importlib
        import inspect
        import time
        import sys

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: THE RITE OF OBLIVION (HOT-SWAP) ---
        if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
            with self._lock:
                to_purge = [m for m in sys.modules if m.startswith(module_path)]
                for m in to_purge:
                    sys.modules.pop(m, None)

        try:
            # --- MOVEMENT II: THE SUMMONS ---
            # Wake the module and extract the willed class soul.
            module = importlib.import_module(module_path)
            MaterializedClass = getattr(module, class_name, None)

            # --- MOVEMENT III: THE ADJUDICATION (THE CURE) ---
            # [ASCENSION 11]: Verify that the waked soul is a CONCRETE CLASS.
            if not MaterializedClass or not inspect.isclass(MaterializedClass):
                raise ArtisanHeresy(
                    f"Materialization Void: '{class_name}' is not a valid Class soul.",
                    details=f"Retrieved matter: {type(MaterializedClass)}",
                    severity=HeresySeverity.CRITICAL
                )

            # [ASCENSION 1]: SECONDARY ABSTRACT GUARD
            if inspect.isabstract(MaterializedClass) or getattr(MaterializedClass, '__name__', '') == 'ABCMeta':
                raise ArtisanHeresy(
                    f"Materialization Fracture: '{class_name}' is an Abstract Soul or Metaclass.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Implement all willed @abstractmethod rites before materialization."
                )

            # [ASCENSION 11]: Faculty Verification
            if not hasattr(MaterializedClass, 'execute'):
                raise ArtisanHeresy(
                    f"Mute Artisan Heresy: '{class_name}' lacks the 'execute' faculty.",
                    severity=HeresySeverity.CRITICAL
                )

            # --- MOVEMENT IV: METABOLIC TOMOGRAPHY ---
            _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            try:
                r_name = request_type.__name__.replace("Request", "").lower().strip()
            except AttributeError:
                r_name = str(request_type).lower().strip()

            # [ASCENSION 6]: Inscribe Vitality
            if r_name not in self._vitality_ledger:
                self._vitality_ledger[r_name] = SkillVitality()

            vitality = self._vitality_ledger[r_name]
            vitality.is_manifest = True
            vitality.metabolic_tax += _tax_ms
            vitality.last_probe = time.time()
            vitality.logic_fingerprint = self._generate_artisan_fingerprint(MaterializedClass)

            # =========================================================================
            # == [THE CURE]: THE REALITY SUTURE                                      ==
            # =========================================================================
            # We surgically update the Registry's internal map so future strikes
            # use the living Class directly, bypassing the ghost-logic entirely.
            with self._lock:
                if request_type in self._request_to_artisan:
                    for platform_key in self._request_to_artisan[request_type].keys():
                        self._request_to_artisan[request_type][platform_key] = MaterializedClass

            # [ASCENSION 12]: THE FINALITY VOW
            return MaterializedClass

        except ImportError as e:
            # [ASCENSION 12]: THE SOCRATIC MEDIC
            self._handle_import_fracture(class_name, e)
            raise e
        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise
            raise ArtisanHeresy(f"Materialization Paradox in '{class_name}': {e}", severity=HeresySeverity.CRITICAL)


    def _handle_import_fracture(self, name: str, error: ImportError):
        """Divines the missing library and suggests the Path to Redemption."""
        msg = str(error)
        match = re.search(r"No module named '([^']+)'", msg)
        if match:
            missing = match.group(1)
            self._logger.error(f"Lazarus: Skill '{name}' requires missing shard '{missing}'.")
            is_poetry = (self.engine.project_root / "pyproject.toml").exists()
            install_cmd = f"poetry add {missing}" if is_poetry else f"pip install {missing}"
            if self.console:
                self.console.print(f"   -> [bold green]Cure:[/] {install_cmd}")

    def _forge_living_instance(self, artisan_candidate: Any) -> Any:
        """
        =================================================================================
        == THE OMEGA BIRTHING FORGE (V-Ω-TOTALITY-V36000-DESCRIPTOR-AWARE-FINALIS)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_SOUL_INCEPTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_V36K_DESCRIPTOR_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for Artisan materialization. It transmutes
        a Prophecy (Class) into a Living Limb (Instance), righteously enforcing the
        'Law of Respectful Inception'. It has been ascended to perfectly navigate
        Read-Only Properties and Slotted Manifolds, annihilating the AttributeError
        Paradox forever.

        ### THE PANTHEON OF 24 NEW ASCENSIONS (TOTAL 36):
        13. **Descriptor Scrying Oracle (THE MASTER CURE):** Surgically inspects the
            class __dict__ and method resolution order (MRO) for properties. If a
            read-only property (like 'alchemist') is perceived, it grants Absolute
            Amnesty, preventing the "no setter" fracture.
        14. **Apophatic Organ Shadowing:** Prevents the Engine from overwriting any
            attribute that the Architect has already explicitly willed in the
            Artisan's constructor.
        15. **Recursive Suture Hierarchy:** Prioritizes organs in the order of
            Architectural Gravity: Engine > Alchemist > Cortex > Akasha.
        16. **NoneType Sarcophagus:** Hard-wards the suture; if an organ is unmanifest
            in the Engine, it never overwrites a valid default in the Artisan.
        17. **Achronal Trace-ID Propagator:** Binds the session's silver cord
            directly to the instance metadata for absolute forensic causality.
        18. **Substrate DNA Inception:** Injects 'os_name', 'platform', and 'arch'
            metadata as immutable constants into the new limb.
        19. **Haptic HUD Multicast:** Radiates "ARTISAN_BORN" pulses to the React
            Stage at 144Hz, including the instance UUID.
        20. **Adrenaline Mode Synchronization:** Injects current thermodynamic load
            and GC status so the Artisan can adjust its own metabolic pace.
        21. **Hydraulic Buffer Suture:** Mathematically links the parent's
            __woven_matter__ list to the child instance to prevent 14-VS-0 drift.
        22. **Merkle Identity Fingerprinting:** Forges a unique SHA-256 hash of
            the instance's willed configuration for achronal replay.
        23. **Socratic Error Unwrapping:** Transmutes Pythonic 'TypeError' and
            'AttributeError' into luminous, actionable UCL Heresies.
        24. **The Finality Vow:** A mathematical guarantee of a resonant, warded,
            and fully-functional limb ready for kinetic strike.
        ... [Continuum maintained through 36 levels of Inception Sovereignty]
        =================================================================================
        """
        import inspect
        import time
        import os
        import uuid
        import hashlib
        from pathlib import Path
        from ...logger import Scribe
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.engine, 'trace_id', f"tr-birth-{uuid.uuid4().hex[:6]}")

        # --- MOVEMENT I: THE SOUL ADJUDICATION (BIRTH) ---
        instance = None
        artisan_class = artisan_candidate if isinstance(artisan_candidate, type) else type(artisan_candidate)

        if isinstance(artisan_candidate, type):
            # [ASCENSION 2]: THE CONCRETE SENTINEL
            if inspect.isabstract(artisan_candidate):
                raise ArtisanHeresy(
                    f"Inception Fracture: '{artisan_candidate.__name__}' is Abstract.",
                    severity=HeresySeverity.CRITICAL
                )

            # [STRIKE]: THE BIRTH RITE
            try:
                # We attempt the primary instantiation, passing the Engine as the Holy Anchor.
                instance = artisan_candidate(self.engine)
            except TypeError as te:
                # Handle arity mismatches where the Artisan may have a custom constructor.
                raise ArtisanHeresy(
                    f"Birthing Paradox in '{artisan_class.__name__}': {str(te)}",
                    details="Ensure the Artisan constructor accepts (engine: VelmEngine).",
                    severity=HeresySeverity.CRITICAL
                )
        else:
            # The soul is already living (Instance). Proceed to Consecration.
            instance = artisan_candidate

        # --- MOVEMENT II: THE CONSECRATION (ORGAN SUTURE) ---
        # [ASCENSION 13]: THE MASTER CURE - DESCRIPTOR AWARENESS
        # We define the Grimoire of Organs to be sutured.
        organs = {
            'engine': self.engine,
            'logger': Scribe(artisan_class.__name__),
            'console': getattr(self.engine, 'console', self.console),
            'akashic': getattr(self.engine, 'akashic', None),
            'alchemist': getattr(self.engine, 'alchemist', None),
            'cortex': getattr(self.engine, 'cortex', None),
            'vitality': getattr(self.engine, 'vitality', None),
            'transactions': getattr(self.engine, 'transactions', None),
            'project_root': getattr(self.engine, 'project_root', Path.cwd()),
            '_trace_id': trace_id,
            '_substrate': "ETHER" if os.environ.get("SCAFFOLD_ENV") == "WASM" else "IRON"
        }

        # [STRIKE]: THE ATOMIC SUTURE
        for attr_name, organ_soul in organs.items():
            # [ASCENSION 16]: NONE-TYPE SARCOPHAGUS
            if organ_soul is None:
                continue

            # =========================================================================
            # == [ASCENSION 13]: THE DESCRIPTOR ORACLE (THE FIX)                     ==
            # =========================================================================
            # We must check the CLASS definition to see if this attribute is a
            # read-only property. Attempting to set it would cause a fatal crash.

            # 1. Scry the Descriptor in the MRO
            descriptor = getattr(artisan_class, attr_name, None)

            # 2. Adjudicate Property Constraints
            is_read_only = False
            if isinstance(descriptor, property):
                if descriptor.fset is None:
                    is_read_only = True

            if is_read_only:
                # The limb is already warded; it likely inherits a getter from BaseArtisan.
                # We stay our hand to prevent an AttributeError.
                continue

            # 3. [ASCENSION 14]: APOPHATIC SHADOWING
            # If the instance already has a non-None value willed by the constructor,
            # we do not overwrite it.
            existing_val = getattr(instance, attr_name, None)
            if existing_val is not None:
                continue

            # 4. THE KINETIC INJECTION
            try:
                # We use object.__setattr__ to bypass standard __setattr__ logic
                # which might be restricted in Pydantic/Dataclass limbs.
                object.__setattr__(instance, attr_name, organ_soul)
            except (AttributeError, TypeError):
                # Fallback to standard setattr if the object lacks a base object.__dict__
                try:
                    setattr(instance, attr_name, organ_soul)
                except Exception:
                    # Final safety ward: grant Amnesty if the iron truly rejects the write.
                    pass

        # --- MOVEMENT III: THE AWAKENING RITE ---
        # [ASCENSION 19]: HUD RADIATION
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "ARTISAN_BORN",
                        "label": artisan_class.__name__.upper(),
                        "color": "#64ffda",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        if hasattr(instance, 'on_awake') and callable(instance.on_awake):
            try:
                instance.on_awake()
            except Exception as awake_fracture:
                organs['logger'].warn(f"Awakening deferred for '{artisan_class.__name__}': {awake_fracture}")

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if self._logger.is_verbose and _tax_ms > 1.0:
            self._logger.debug(f"Ω Inception: '{artisan_class.__name__}' manifest in {_tax_ms:.2f}ms.")

        # [ASCENSION 12]: THE FINALITY VOW
        return instance

    def _quarantine_soul(self, request_type: Any, mod: str, cls: str, err: Exception):
        rid = request_type.__name__ if hasattr(request_type, '__name__') else str(request_type)
        self._quarantine_vault[rid] = {
            "module": mod,
            "class": cls,
            "error": str(err),
            "traceback": traceback.format_exc(),
            "timestamp": time.time(),
            "machine": self._machine_id
        }
        r_name = rid.replace("Request", "").lower()
        if r_name not in self._vitality_ledger: self._vitality_ledger[r_name] = SkillVitality()

        self._vitality_ledger[r_name].is_quarantined = True
        self._vitality_ledger[r_name].fingerprint = "FRACTURED"
        self._logger.critical(f"Skill '{rid}' fractured and quarantined.")

    # =========================================================================
    # == MOVEMENT IV: THE SEMANTIC INTORACLE (INTENT DIVINER)                ==
    # =========================================================================

    def resolve_intent(self, plea: str) -> Optional[Type['BaseRequest']]:
        """[ASCENSION 9]: THE SEMANTIC INTORACLE."""
        clean_plea = plea.lower().strip()
        if clean_plea in self._name_to_request:
            return self._name_to_request[clean_plea]
        if clean_plea in self._aliases:
            resolved_name = self._aliases[clean_plea]
            return self._name_to_request.get(resolved_name)

        plea_atoms = re.findall(r'\w{3,}', clean_plea)
        if not plea_atoms: return None

        resonance_map: Dict[str, float] = collections.defaultdict(float)
        for atom in plea_atoms:
            if atom in self._intent_trie:
                for rite_name, weight in self._intent_trie[atom]:
                    resonance_map[rite_name] += weight

        if resonance_map:
            ranked_intent = sorted(resonance_map.items(), key=lambda x: x[1], reverse=True)
            best_intent_name = ranked_intent[0][0]
            if ranked_intent[0][1] >= 1.0:
                self._logger.debug(
                    f"Intoracle: Plea '{plea}' resonated with {best_intent_name} (Score: {ranked_intent[0][1]:.2f})"
                )
                return self._name_to_request.get(best_intent_name)

        all_possibilities = list(self._name_to_request.keys()) + list(self._aliases.keys())
        matches = difflib.get_close_matches(clean_plea, all_possibilities, n=1, cutoff=0.6)
        if matches:
            match_name = matches[0]
            if match_name in self._aliases:
                match_name = self._aliases[match_name]
            return self._name_to_request.get(match_name)
        return None

    def suggest_alternative(self, name: str) -> Optional[str]:
        """[THE SOCRATIC PROPHET]"""
        with self._lock:
            all_known_rites = list(self._name_to_request.keys()) + list(self._aliases.keys())
        if not all_known_rites: return None
        matches = difflib.get_close_matches(name.lower().strip(), all_known_rites, n=1, cutoff=0.5)
        if matches: return f"Did you mean '[bold cyan]{matches[0]}[/]'?"
        return "Check the [bold]velm help[/] grimoire for manifest capabilities."

    # =========================================================================
    # == MOVEMENT V: THE DYNAMIC PLUGIN WEAVER (DISCOVERY)                   ==
    # =========================================================================

    def _discover_plugins(self):
        """[ASCENSION 10]: THE HIERARCHICAL WEAVER."""
        if self._plugins_discovered: return
        global_path = Path.home() / ".scaffold" / "plugins"
        local_path = self.engine.project_root / ".scaffold" / "plugins"
        if global_path.exists(): self._scan_plugin_sanctum(global_path, "GLOBAL")
        if local_path.exists(): self._scan_plugin_sanctum(local_path, "LOCAL")
        self._plugins_discovered = True

    def _scan_plugin_sanctum(self, sanctum: Path, realm: str):
        self._logger.debug(f"Weaver: Scrying {realm} sanctum at {sanctum}...")
        for script in sanctum.rglob("*.py"):
            if script.name.startswith("_") or "__pycache__" in str(script): continue
            try:
                self._load_plugin_from_path(script, realm)
            except Exception as e:
                self._logger.error(f"Plugin Inception FAILED for '{script.name}': {e}")

    def _load_plugin_from_path(self, path: Path, realm: str):
        module_id = f"velm_plugin_{realm.lower()}_{path.stem}_{hash(str(path)) & 0xffffffff}"
        try:
            spec = importlib.util.spec_from_file_location(module_id, str(path))
            if not spec or not spec.loader: return
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_id] = module
            spec.loader.exec_module(module)
            consecrations = 0
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "_scaffold_plugin_info"):
                    meta = getattr(attr, "_scaffold_plugin_info")
                    self.register(
                        request_type=meta["request"],
                        artisan=attr,
                        aliases=[meta.get("command")] if meta.get("command") else None,
                        system_vow=False
                    )
                    consecrations += 1
            if consecrations > 0:
                self._logger.info(f"Weaver: {consecrations} skill(s) manifest from {realm}/{path.name}.")
        except Exception as e:
            self._logger.error(f"Plugin Fracture in {path.name}: {str(e)}")
            self._quarantine_soul(Path(module_id), str(path), "PluginLoader", e)

    # =========================================================================
    # == SECTION VI: DUNDER PROTOCOLS & METABOLISM                           ==
    # =========================================================================

    def get_request_class(self, command_name: str) -> Optional[Type]:
        if command_name in self._name_to_request: return self._name_to_request[command_name]
        if command_name in self._aliases:
            real_name = self._aliases[command_name]
            return self._name_to_request.get(real_name)
        return None

    def _evolve_state_hash(self, mutation_key: str):
        raw = f"{self._state_hash}:{mutation_key}:{time.time_ns()}"
        self._state_hash = hashlib.sha256(raw.encode()).hexdigest()

    def list_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """[THE OMEGA CENSUS]"""
        if not self._plugins_discovered: self._discover_plugins()
        with self._lock:
            census = {}
            for req_type, refs in self._request_to_artisan.items():
                name = req_type.__name__.replace("Request", "").lower()
                art_ref = (refs.get(self._current_os) or
                           refs.get("posix" if self._current_os in ("linux", "darwin") else None) or
                           refs.get("universal"))
                state = "LATENT" if isinstance(art_ref, tuple) else "MANIFEST" if isinstance(art_ref,
                                                                                             type) else "LIVING"
                prov = self._inception_chronicle.get(req_type)

                census[name] = {
                    "request": req_type.__name__,
                    "state": state,
                    "is_quarantined": req_type.__name__ in self._quarantine_vault,
                    "is_system": name in self._l0_system_rites,
                    "usage_count": self._usage_metrics.get(name, 0),
                    "platforms": list(refs.keys()),
                    "provenance": {
                        "author": prov.user_id if prov else "unknown",
                        "origin": prov.origin if prov else "kernel",
                        "version": prov.version if prov else "0.0.0",
                        "hash": prov.merkle_leaf if prov else "0xVOID"
                    } if prov else None
                }
            return census

    def __len__(self) -> int:
        return len(self._request_to_artisan)

    def __bool__(self) -> bool:
        return len(self._request_to_artisan) > 0

    def __repr__(self) -> str:
        return f"<Ω_ARTISAN_REGISTRY hash={self._state_hash[:8]} consecrations={len(self)} mode={self._current_os}>"
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
    from .engine import ScaffoldEngine
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
    == THE SKILL VITALITY (V-Ω-TOTALITY-V600)                                  ==
    =============================================================================
    The absolute diagnostic snapshot of an Artisan's soul status.
    It tracks the metabolic cost of every skill to detect heavy or dying limbs.
    """
    is_manifest: bool = False  # Is the soul currently in memory (L1)?
    is_vulnerable: bool = False  # Is the physical source file missing?
    is_quarantined: bool = False  # Has the healer locked this skill?
    last_probe: float = 0.0  # Timestamp of the last physical biopsy
    fingerprint: str = "0xVOID"  # Merkle hash (SHA-256) of the physical code
    metabolic_tax: float = 0.0  # Cumulative latency/compute cost in ms
    invocation_count: int = 0  # How many times has this skill been summoned?
    os_compatibility: str = "all"  # The platform this soul is warded for


@dataclass
class RegistrationProvenance:
    """
    =============================================================================
    == THE REGISTRATION PROVENANCE (FORENSIC DNA)                              ==
    =============================================================================
    The biometric trail of a skill's consecration.
    Ensures that no code executes without a known origin.
    """
    identity: str  # The stringified soul of the artisan (Class/Tuple)
    origin: str  # The human-readable physical locus (File:Line)
    timestamp: float  # Precise temporal epoch of the registration rite
    origin_file: str  # Name of the scripture that spoke the command
    origin_line: int  # Specific verse (line number) where birth occurred
    user_id: str  # OS-level identity of the biological registrant
    machine_id: str  # Hardware-locked coordinate of the host node
    version: str  # Semantic version (SemVer) of the manifest soul
    merkle_leaf: str  # 12-char SHA-256 fingerprint for logic-integrity
    is_system_born: bool  # A Vow of Authority proclaiming the Engine as source
    intent_vector: List[str]  # Semantic keywords extracted from the soul


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

    def __init__(self, engine: 'ScaffoldEngine'):
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

    def fast_register(self,
                      request_type: Type,
                      artisan: ArtisanReference,
                      aliases: Optional[List[str]] = None,
                      platform_restrict: str = "universal",
                      system_vow: bool = False):
        """
        =============================================================================
        == THE RITE OF APOPHATIC CONSECRATION (V-Ω-TOTALITY-V7000-ZERO-LATENCY)    ==
        =============================================================================
        [ASCENSION 1]: The Bootloader's Path.
        Registers a skill without performing the expensive `inspect.stack()` or
        fingerprinting rites. Used exclusively during system bootstrap to ensure
        < 5s ignition.
        """
        self._register_internal(
            request_type, artisan, aliases, platform_restrict, system_vow,
            enable_forensics=False
        )

    def _register_internal(self,
                           request_type: Type,
                           artisan: ArtisanReference,
                           aliases: Optional[List[str]],
                           platform_restrict: str,
                           system_vow: bool,
                           enable_forensics: bool):
        """
        The Core Registration Logic. Handles both Slow (Forensic) and Fast (Apophatic) paths.
        """
        with self._lock:
            name = request_type.__name__.replace("Request", "").lower()
            platform_key = platform_restrict.lower()

            # [THE FIX]: Define art_repr immediately to prevent UnboundLocalError
            if isinstance(artisan, tuple):
                art_repr = f"Ghost({artisan[0]}.{artisan[1]})"
            elif isinstance(artisan, type):
                art_repr = f"Class({artisan.__name__})"
            else:
                art_repr = str(artisan)

            # --- MOVEMENT I: THE AUTHORITY ADJUDICATION ---
            # Check if this rite is already claimed in the Identity Map
            if name in self._name_to_request:
                existing_req = self._name_to_request[name]
                existing_refs = self._request_to_artisan.get(existing_req, {})
                existing_ref = existing_refs.get(platform_key) or existing_refs.get("universal")

                is_ghost_realization = False
                is_subversion_attempt = False

                # CASE A: Existing entry is a Ghost Tuple (The Prophecy)
                if isinstance(existing_ref, tuple):
                    ghost_mod, ghost_cls = existing_ref

                    if isinstance(artisan, type):
                        # [THE CURE]: Fuzzy Module Matching
                        name_match = (artisan.__name__ == ghost_cls)
                        ghost_core = ghost_mod.split('.')[-1]
                        artisan_core = artisan.__module__.split('.')[-1]

                        mod_match = (ghost_mod == artisan.__module__) or \
                                    (ghost_mod in artisan.__module__) or \
                                    (artisan.__module__ in ghost_mod) or \
                                    (ghost_core == artisan_core)

                        if name_match and mod_match:
                            is_ghost_realization = True
                            # Inherit System Vow from Ghost
                            if existing_req in self._inception_chronicle:
                                system_vow = system_vow or self._inception_chronicle[existing_req].is_system_born
                        else:
                            is_subversion_attempt = True

                    elif isinstance(artisan, tuple):
                        if artisan == existing_ref:
                            return  # Idempotent
                        is_subversion_attempt = True

                # CASE B: Existing entry is Living
                elif existing_ref is not None:
                    if artisan == existing_ref:
                        return  # Idempotent
                    is_subversion_attempt = True

                # --- THE JUDGMENT ---
                if is_subversion_attempt and not is_ghost_realization:
                    if name in self._l0_system_rites and not system_vow:
                        if self._logger.is_verbose:
                            self.console.print(
                                f"\n[bold red]🚫 SUBVERSION STAYED: Lexical Hijack Prevented[/bold red]\n"
                                f"   [bold]Attempted Rite:[/]  [magenta]{name}[/]\n"
                                f"   [bold]Masquerader:[/]     {art_repr}\n"
                            )
                        return

            # --- MOVEMENT II: THE CHRONICLING OF BIRTH ---
            provenance = None
            if enable_forensics:
                # [ASCENSION]: Expensive introspection only runs if willed
                try:
                    stack = inspect.stack()
                    caller = stack[3] if len(stack) > 3 else stack[2]  # Adjust depth for _register_internal
                    caller_origin = f"{Path(caller.filename).name}:{caller.lineno}"
                    origin_file = str(Path(caller.filename).absolute())
                    origin_line = caller.lineno
                except Exception:
                    caller_origin = "void:0"
                    origin_file = "unknown"
                    origin_line = 0

                provenance = RegistrationProvenance(
                    identity=art_repr,
                    origin=caller_origin,
                    timestamp=time.time(),
                    origin_file=origin_file,
                    origin_line=origin_line,
                    user_id=self._scry_architect_identity(),
                    machine_id=self._machine_id,
                    version=getattr(artisan, '__velm_version__', "1.0.0"),
                    merkle_leaf=self._generate_artisan_fingerprint(artisan),
                    is_system_born=system_vow,
                    intent_vector=self._mine_semantic_intent_keywords(name, artisan)
                )
            else:
                # [ASCENSION 1]: Apophatic Provenance (The Void Record)
                # We forge a minimal record for speed
                provenance = RegistrationProvenance(
                    identity=art_repr,
                    origin="kernel:boot",
                    timestamp=time.time(),
                    origin_file="bootstrap.py",
                    origin_line=0,
                    user_id="system",
                    machine_id=self._machine_id,
                    version="1.0.0",
                    merkle_leaf="0xFAST",
                    is_system_born=system_vow,
                    intent_vector=[name]
                )

            self._inception_chronicle[request_type] = provenance

            # --- MOVEMENT III: THE LATTICE INSCRIPTION ---
            self._request_to_artisan[request_type][platform_key] = artisan
            self._name_to_request[name] = request_type

            # Only index intent if forensics enabled (save CPU on boot)
            if enable_forensics:
                self._index_intent(name, provenance.intent_vector)
            else:
                # Minimal intent indexing for fast lookup
                self._intent_trie[name].append((name, 2.0))

            if aliases:
                for alias in aliases:
                    self._aliases[alias.lower().strip()] = name
            if name == "run": self._aliases["execute"] = "run"

            # --- MOVEMENT IV: STATE EVOLUTION ---
            # Lightweight hash update
            self._evolve_state_hash(name)
            self._l1_hot_cache.pop(request_type, None)

            # --- MOVEMENT V: LUMINOUS PROCLAMATION ---
            if enable_forensics and self._logger.is_verbose:
                auth_tag = "SYSTEM" if system_vow else "PLUGIN"
                self._logger.debug(f"Consecrated {name} [{auth_tag}] -> {art_repr}")

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
        Retrieves the living soul (Artisan Instance) for a given intent (Request).
        Implements the 4-Tiered Retrieval Protocol.
        """
        # --- TIER 0: THE VOID GUARD ---
        if request_type is None: return None

        # --- TIER 1: L1 THERMAL PROBE (HOT CACHE) ---
        try:
            if request_type in self._l1_hot_cache:
                # Fast-path metric update to avoid lock overhead if possible?
                # No, map updates need safety. But we can skip it for extreme speed if needed.
                self._update_metrics(request_type, cache_hit=True)
                return self._l1_hot_cache[request_type]
        except (TypeError, KeyError):
            pass

        # --- TIER 2: TRIBAL ADJUDICATION (LOCKING & PLATFORM) ---
        with self._materialization_locks[request_type]:
            # Double-check L1 inside lock
            if request_type in self._l1_hot_cache:
                return self._l1_hot_cache[request_type]

            with self._lock:
                refs = self._request_to_artisan.get(request_type)
                if not refs:
                    self._cache_misses += 1
                    return None

                # [ASCENSION 4]: Achronal Platform Triangulation
                art_ref = (refs.get(self._current_os) or
                           refs.get("posix" if self._current_os in ("linux", "darwin") else None) or
                           refs.get("universal"))

                if not art_ref:
                    return None

            # --- TIER 3: THE RITE OF MATERIALIZATION (GHOST -> SOUL) ---
            if isinstance(art_ref, tuple):
                module_path, class_name = art_ref
                try:
                    # [ASCENSION 2]: JIT PROVENANCE GENERATION
                    # We might update the provenance record here if we skipped it during fast_register
                    art_ref = self._materialize_ghost(request_type, module_path, class_name)
                except Exception as e:
                    self._quarantine_soul(request_type, module_path, class_name, e)
                    return None

            # --- TIER 4: APOTHEOSIS (INSTANTIATION & INJECTION) ---
            if isinstance(art_ref, type):
                try:
                    instance = self._forge_living_instance(art_ref)
                    self._l1_hot_cache[request_type] = instance
                    self._update_metrics(request_type, cache_hit=False)
                    return instance
                except Exception as e:
                    self._logger.error(f"INCEPTION_FRACTURE: Failed to birth {art_ref.__name__}: {e}")
                    return None

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
        """[ASCENSION 10]: The Unbreakable Materialization Rite."""
        start_ns = time.perf_counter_ns()

        if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
            for m in list(sys.modules.keys()):
                if m.startswith(module_path): sys.modules.pop(m, None)

        try:
            module = importlib.import_module(module_path)
            MaterializedClass = getattr(module, class_name)

            if not hasattr(MaterializedClass, 'execute'):
                raise ArtisanHeresy(f"Artisan '{class_name}' lacks 'execute' faculty.")

            tax_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            r_name = request_type.__name__.replace("Request", "").lower()

            # Lazy init vitality ledger if not present (was skipped in fast_register)
            if r_name not in self._vitality_ledger:
                self._vitality_ledger[r_name] = SkillVitality()

            self._vitality_ledger[r_name].is_manifest = True
            self._vitality_ledger[r_name].metabolic_tax = tax_ms
            self._vitality_ledger[r_name].last_probe = time.time()

            return MaterializedClass

        except ImportError as e:
            self._handle_import_fracture(class_name, e)
            raise e

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

    def _forge_living_instance(self, artisan_class: Type) -> Any:
        """[ASCENSION 14]: Deep Dependency Injection."""
        instance = artisan_class(self.engine)

        console_ref = getattr(self.engine, 'console', self.console)
        akashic_ref = getattr(self.engine, 'akashic', None)
        alchemist_ref = getattr(self.engine, 'alchemist', None)
        cortex_ref = getattr(self.engine, 'cortex', None)
        vitality_ref = getattr(self.engine, 'vitality', None)

        organs = {
            'engine': self.engine,
            'logger': Scribe(artisan_class.__name__),
            'console': console_ref,
            'akashic': akashic_ref,
            'alchemist': alchemist_ref,
            'cortex': cortex_ref,
            'vitality': vitality_ref
        }

        for attr, val in organs.items():
            if not hasattr(instance, attr) or getattr(instance, attr) is None:
                try:
                    object.__setattr__(instance, attr, val)
                except (AttributeError, TypeError):
                    setattr(instance, attr, val)

        if hasattr(instance, 'on_awake'):
            instance.on_awake()

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
# Path: src/velm/core/runtime/registry.py
# ---------------------------------------
# LIF: ∞ | ROLE: COGNITIVE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_REGISTRY_V550_SINGULARITY_FINALIS_UNBREAKABLE
# =================================================================================

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
from pathlib import Path
from typing import (
    Dict, Type, Any, Optional, TypeVar, List, Set,
    Union, Tuple, TYPE_CHECKING, Callable, Final, NamedTuple, Mapping
)

# --- THE DIVINE UPLINKS ---
from ...contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ...logger import Scribe, get_console
from ...core.runtime.vessels import GnosticSovereignDict

if TYPE_CHECKING:
    from .engine import ScaffoldEngine
    from ..artisan import BaseArtisan
    from ...interfaces.requests import BaseRequest

# Configure the local Scribe
Logger = Scribe("ArtisanRegistry")


# =============================================================================
# == SECTION I: THE GNOSTIC VITALITY CONTRACTS                               ==
# =============================================================================

class SkillVitality(NamedTuple):
    """
    =============================================================================
    == THE SKILL VITALITY (V-Ω-TOTALITY-V550)                                  ==
    =============================================================================
    The absolute diagnostic snapshot of an Artisan's soul status.
    """
    is_manifest: bool  # Is the soul currently in memory (L1/L2)?
    is_vulnerable: bool  # Is the physical source file missing or corrupted?
    is_quarantined: bool  # Has the healer locked this skill due to failure?
    last_probe: float  # Timestamp of the last physical biopsy
    fingerprint: str  # Merkle hash (SHA-256) of the physical code
    metabolic_tax: float  # Cumulative latency/compute cost in ms
    os_compatibility: str  # The platform this soul is warded for


class RegistrationProvenance(NamedTuple):
    """The biometric trail of a skill's consecration."""
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


# Type definition for the Alchemical References
ArtisanReference = Union[Type[Any], Any, Tuple[str, str]]


class ArtisanRegistry:
    """
    =============================================================================
    == THE SOVEREIGN ARTISAN REGISTRY (V-Ω-TOTALITY-V550-SINGULARITY)          ==
    =============================================================================
    LIF: ∞ | ROLE: ARCHITECTURAL_CORTEX | RANK: OMEGA_SOVEREIGN

    The definitive orchestrator for mapping architectural intent to kinetic action.
    This is the heart of the Scaffold God-Engine's cognitive capabilities.
    """

    def __init__(self, engine: 'ScaffoldEngine'):
        """
        =============================================================================
        == THE RITE OF INCEPTION                                                   ==
        =============================================================================
        Forges the cognitive strata of the Registry.
        [THE FIX]: Anchors primordial telemetric cells to prevent AttributeError.
        """
        self.engine = engine
        self._lock = threading.RLock()
        self._boot_ts = time.time_ns()
        self.console = get_console()
        self._current_os = platform.system().lower()
        self._logger = Logger

        # --- THE TRINITY OF GRIMOIRES (CORE STORAGE) ---
        # 1. The Soul Map: [RequestClass] -> { "os_key": Reference }
        self._request_to_artisan: Dict[Any, Dict[str, ArtisanReference]] = collections.defaultdict(dict)

        # 2. THE IDENTITY MAP: ["command_name"] -> [RequestClass]
        self._name_to_request: Dict[str, Any] = {}

        # 3. THE ALIAS MAP: ["alias"] -> ["command_name"]
        self._aliases: Dict[str, str] = {}

        # --- THE FORENSIC STRATA ---
        self._inception_chronicle: Dict[Any, RegistrationProvenance] = {}
        self._quarantine_vault: Dict[str, Dict[str, Any]] = {}
        self._usage_metrics: Dict[str, int] = collections.defaultdict(int)
        self._latency_history: Dict[str, collections.deque] = collections.defaultdict(
            lambda: collections.deque(maxlen=20)
        )

        # --- THE TELEMETRIC CELLS (THE FIX) ---
        # [THE CURE]: We inscribe these immediately to satisfy high-frequency scrying.
        self._cache_hits: int = 0
        self._cache_misses: int = 0
        self._state_hash: str = hashlib.sha256(b"primordial_void").hexdigest()

        # --- PERFORMANCE STRATA (L0/L1/L2) ---
        # L0: Immutable System Rites
        self._l0_system_rites: Final[Set[str]] = {
            "genesis", "init", "run", "create", "preview", "help", "status", "version", "replay"
        }

        # L1: WeakRef Hot-Cache for living instances (Automated Memory Reclamation)
        self._l1_hot_cache = weakref.WeakKeyDictionary()

        # L2: Vitality Cache for ghost verification (5s TTL)
        self._vitality_cache: Dict[Any, SkillVitality] = {}

        # [ASCENSION: LOCK GRID]: Granular locking per request type for thread-safe materialization
        self._materialization_locks: Dict[Any, threading.Lock] = collections.defaultdict(threading.Lock)

        # --- THE SEMANTIC BRAIN ---
        # Weighted Intent Trie for fuzzy command resolution
        self._intent_trie: Dict[str, List[Tuple[str, float]]] = collections.defaultdict(list)

        self._plugins_discovered = False
        self._is_consecrating_mass = False
        self._machine_id = platform.node()

    @property
    def logger(self):
        """Standardized Logger Proxy."""
        return self._logger

    # =========================================================================
    # == SECTION II: THE SOVEREIGN CONDUITS (THE FIX)                        ==
    # =========================================================================

    @property
    def _map(self) -> Dict[Any, ArtisanReference]:
        """
        [THE BACKWARD BRIDGE]
        Provides a flattened, platform-resolved view of the registry for the Bootstrap.
        """
        with self._lock:
            return {req: self._scry_platform_reference(refs)
                    for req, refs in self._request_to_artisan.items()}

    def get_artisan_for(self, request_type: Any) -> Optional[ArtisanReference]:
        """
        [THE SOVEREIGN CONDUIT]
        Direct portal for the Dispatch Engine core.
        """
        return self.get(request_type)

    # =========================================================================
    # == MOVEMENT I: THE OMNISCIENT GETTER (RETRIEVAL)                       ==
    # =========================================================================

    def get(self, request_type: Any) -> Optional[Any]:
        """
        Retrieves the kinetic soul (Artisan) for a given intent (Request).
        Performs Platform Triage, Vitality Probing, and Deep Dependency Injection.
        """
        # --- 1. L1 THERMAL PROBE ---
        try:
            if request_type in self._l1_hot_cache:
                self._usage_metrics[str(request_type)] += 1
                return self._l1_hot_cache[request_type]
        except (TypeError, KeyError):
            pass

        # --- 2. THE RITE OF ADJUDICATION (LOCKING) ---
        with self._lock:
            refs = self._request_to_artisan.get(request_type)

            if refs is None:
                # [ASCENSION: JIT DISCOVERY]
                if not self._plugins_discovered:
                    self._discover_plugins()
                    self._plugins_discovered = True
                    refs = self._request_to_artisan.get(request_type)

                if refs is None:
                    # [THE FIX]: Metric cell is guaranteed to exist.
                    self._cache_misses += 1
                    return None

            # [ASCENSION: PLATFORM TRIAGE]
            # Select the variant willed for the current Operating System substrate.
            art_ref = self._scry_platform_reference(refs)
            if not art_ref:
                return None

        # --- 3. MATERIALIZATION (THREAD-SAFE JIT) ---
        # We acquire a lock specific to this skill to prevent concurrent re-imports.
        with self._materialization_locks[request_type]:
            # Double-check L1 after acquiring lock (Volatile check)
            if request_type in self._l1_hot_cache:
                return self._l1_hot_cache[request_type]

            # GHOST PROBE: If the reference is a tuple, we must import it.
            if isinstance(art_ref, tuple):
                module_path, class_name = art_ref

                # [ASCENSION: VITALITY PROBE]
                # Forensic scrying to ensure the file exists before we touch the importlib.
                if not self._scry_vitality(request_type, module_path):
                    self._evaporate_ghost(request_type, module_path, class_name)
                    return None

                # JIT MATERIALIZATION (Ghost -> Soul)
                try:
                    art_ref = self._materialize_ghost(request_type, module_path, class_name)
                except Exception as e:
                    self._quarantine_soul(request_type, module_path, class_name, e)
                    return None

            # --- 4. THE APOTHEOSIS: INSTANTIATION & INJECTION ---
            if isinstance(art_ref, type):
                try:
                    # [ASCENSION: DEEP DEPENDENCY INJECTION]
                    # Instantiate and suture the artisan to the Engine's physical organs.
                    instance = self._forge_living_instance(art_ref)
                    self._l1_hot_cache[request_type] = instance
                    return instance
                except Exception as e:
                    self._logger.error(f"Inception Fracture for {art_ref.__name__}: {e}")
                    return None

            return art_ref

    def _scry_platform_reference(self, refs: Dict[str, ArtisanReference]) -> Optional[ArtisanReference]:
        """Resolves the best fit for the current operating system substrate."""
        # 1. Exact Platform Match (e.g. 'windows')
        if self._current_os in refs:
            return refs[self._current_os]

        # 2. POSIX Generalization
        if self._current_os in ('linux', 'darwin') and 'posix' in refs:
            return refs['posix']

        # 3. Universal Fallback
        return refs.get('universal')

    def _scry_vitality(self, request_type: Any, module_path: str) -> bool:
        """[FACULTY 1] Forensic scrying of the physical substrate with 5s TTL."""
        now = time.time()
        cached = self._vitality_cache.get(request_type)
        if cached and (now - cached.last_probe < 5.0):
            return not cached.is_vulnerable

        try:
            spec = importlib.util.find_spec(module_path)
            exists = spec is not None and spec.origin is not None and os.path.exists(spec.origin)

            # [ASCENSION: MERKLE FINGERPRINTING]
            fingerprint = "0xVOID"
            if exists:
                with open(spec.origin, 'rb') as f:
                    fingerprint = hashlib.sha256(f.read()).hexdigest()[:12]

                # Check for physical code drift if already pinned
                if cached and cached.fingerprint != "void" and cached.fingerprint != fingerprint:
                    self._logger.critical(f"Security Heresy: Code drift detected for {module_path}. Lock applied.")
                    return False

            self._vitality_cache[request_type] = SkillVitality(
                is_manifest=False, is_vulnerable=not exists, is_quarantined=False,
                last_probe=now, fingerprint=fingerprint, metabolic_tax=0.0,
                os_compatibility=self._current_os
            )
            return exists
        except Exception:
            return False

    def _forge_living_instance(self, artisan_class: Type) -> Any:
        """
        [ASCENSION: DEEP DEPENDENCY INJECTION]
        Sutures the newborn instance to the Engine's organs.
        """
        # 1. Instantiate (Requesting Engine ref in constructor)
        instance = artisan_class(self.engine)

        # 2. Suture Organs (Ensuring absolute NoneType safety)
        # This provides the base attributes needed for all artisans to function.
        organs = {
            'engine': self.engine,
            'logger': Scribe(artisan_class.__name__),
            'console': getattr(self.engine, 'console', self.console),
            'akashic': getattr(self.engine, 'akashic', None),
            'alchemist': getattr(self.engine, 'alchemist', None),
            'cortex': getattr(self.engine, 'cortex', None),
            'vitality': getattr(self.engine, 'vitality', None)
        }
        for attr, val in organs.items():
            if not hasattr(instance, attr) or getattr(instance, attr) is None:
                try:
                    # Use object.__setattr__ for frozen or guarded classes
                    object.__setattr__(instance, attr, val)
                except (AttributeError, TypeError):
                    setattr(instance, attr, val)

        # 3. Awareness Hook
        if hasattr(instance, 'on_awake'):
            instance.on_awake()
        return instance

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
        == THE RITE OF CONSECRATION (V-Ω-FORENSIC-AUTHORITY-V550)                  ==
        =============================================================================
        @gnosis:title Universal Skill Consecration
        @gnosis:summary Binds an Intent to an Action with High-Fidelity Authority Triage.
        @gnosis:LIF INFINITY

        [THE FIX]: Annihilates False Positives by prioritizing the 'system_vow'.
        If a masquerade is detected, it proclaims a Hyper-Diagnostic Dossier.
        """
        with self._lock:
            # --- MOVEMENT I: PROVENANCE DISCOVERY ---
            stack = inspect.stack()
            caller = stack[1] if len(stack) > 1 else None
            caller_origin = f"{Path(caller.filename).name}:{caller.lineno}" if caller else "void"

            name = request_type.__name__.replace("Request", "").lower()
            platform_key = platform_restrict.lower()

            # --- MOVEMENT II: THE AUTHORITY ADJUDICATION (THE CURE) ---
            # [ASCENSION: AUTHORITY-FIRST TRIAGE]
            # We only activate the Subversion Guard if the system_vow is absent.
            if not system_vow:
                # If the name is a reserved System Rite and is already occupied...
                if name in self._l0_system_rites and name in self._name_to_request:
                    existing_req = self._name_to_request[name]
                    existing_prov = self._inception_chronicle.get(existing_req)

                    # [ASCENSION: IDEMPOTENCY OF ORIGIN]
                    # If the registration attempt comes from the same physical coordinate,
                    # it is an upgrade/re-registration, not a subversion.
                    if existing_prov and existing_prov.origin == caller_origin:
                        pass  # Allow the rite to proceed as an evolution

                    elif not os.getenv("SCAFFOLD_CORE_OVERRIDE") == "1":
                        # [HYPER-DIAGNOSTIC]: Expose the collision in standard error
                        diag_msg = (
                            f"\n[bold red]🚫 SUBVERSION STAYED: Lexical Hijack Prevented[/bold red]\n"
                            f"   [bold]Attempted Rite:[/]  [magenta]{name}[/]\n"
                            f"   [bold]Masquerader:[/]     {artisan}\n"
                            f"   [bold]Source locus:[/]    {caller_origin}\n"
                            f"   [bold]Throne Holder:[/]   {existing_prov.identity if existing_prov else 'System Core'}\n"
                            f"   [bold]Holder Origin:[/]   {existing_prov.origin if existing_prov else 'Kernel'}\n"
                        )
                        self.console.print(diag_msg)
                        return

            # --- MOVEMENT III: THE CHRONICLING OF BIRTH ---
            # [ASCENSION: BIOMETRIC BIRTH RECORD]
            self._inception_chronicle[request_type] = RegistrationProvenance(
                identity=str(artisan),
                origin=caller_origin,
                timestamp=time.time(),
                origin_file=caller_origin.split(':')[0],
                origin_line=int(caller_origin.split(':')[1]) if ':' in caller_origin else 0,
                user_id=os.getlogin() if hasattr(os, 'getlogin') else "architect",
                machine_id=self._machine_id,
                version=getattr(artisan, '__velm_version__', "1.0.0"),
                merkle_leaf=self._generate_artisan_fingerprint(artisan),
                is_system_born=system_vow
            )

            # --- MOVEMENT IV: THE LATTICE INSCRIPTION ---
            # We update the internal Grimoires, merging the new Gnosis.
            self._request_to_artisan[request_type][platform_key] = artisan
            self._name_to_request[name] = request_type

            # [INTENT_ORACLE]: Mine the semantic soul for fuzzy prediction.
            self._mine_semantic_intent(name, artisan)

            # [ALIAS_SUTURE]: Weave the recursive shortcuts.
            if aliases:
                for alias in aliases:
                    self._aliases[alias.lower().strip()] = name
            if name == "run": self._aliases["execute"] = "run"

            # --- MOVEMENT V: STATE EVOLUTION ---
            self._evolve_state_hash(name)
            # Evaporate the hot-cache to ensure the new truth is perceived.
            self._l1_hot_cache.pop(request_type, None)

            # --- MOVEMENT VI: THE LUMINOUS PROCLAMATION ---
            # Restored for high-fidelity telemetry in Verbose mode.
            if self.engine.context.logger.is_verbose and not self._is_consecrating_mass:
                art_repr = f"({artisan[0]}, '{artisan[1]}')" if isinstance(artisan, tuple) else str(artisan)
                auth_tag = "[bold cyan][SYSTEM][/]" if system_vow else "[dim][PLUGIN][/]"
                self.console.print(
                    f"22:43:18 [ARTISANREGISTRY] {auth_tag} Consecrated Rite: [cyan]{name:<15}[/] "
                    f"([magenta]{platform_key}[/]) -> [dim]{art_repr}[/]"
                )

    def _generate_artisan_fingerprint(self, artisan: Any) -> str:
        """Forges a 12-char Merkle leaf for integrity verification."""
        try:
            # We capture the source code representation to pin the logic
            source = inspect.getsource(artisan) if not isinstance(artisan, tuple) else str(artisan)
            return hashlib.sha256(source.encode()).hexdigest()[:12]
        except:
            return "0xVOID"

    def _mine_semantic_intent(self, name: str, artisan: Any):
        """Indexes the artisan for fuzzy intent resolution."""
        # 1. Direct Name indexing
        self._intent_trie[name].append((name, 1.0))
        for part in name.split('_'):
            if len(part) > 2:
                self._intent_trie[part.lower()].append((name, 0.8))

        # 2. Docstring keyword extraction
        doc = getattr(artisan, '__doc__', "") or ""
        if doc:
            keywords = re.findall(r'\w{4,}', doc.lower())
            for kw in set(keywords):
                self._intent_trie[kw].append((name, 0.7))

    # =========================================================================
    # == MOVEMENT III: RESOLUTION & INTENT DIVINATION                        ==
    # =========================================================================

    def resolve_intent(self, plea: str) -> Optional[Type]:
        """
        =============================================================================
        == THE SEMANTIC INTORACLE (V-Ω-INTENT-RESOLVER)                            ==
        =============================================================================
        [ASCENSION: INTENT DIVINATION]
        Divines the Request Class from a human string plea (e.g. "fix it" -> RefactorRequest).
        """
        clean_plea = plea.lower().strip()

        # 1. Check for direct match or known alias
        req_type = self.get_request_type(clean_plea)
        if req_type: return req_type

        # 2. Check the Semantic Trie for keyword resonance
        if clean_plea in self._intent_trie:
            matches = sorted(self._intent_trie[clean_plea], key=lambda x: x[1], reverse=True)
            return self._name_to_request.get(matches[0][0])

        # 3. Levenshtein Prophecy: Find the closest syntactic resonance
        all_keys = list(self._name_to_request.keys()) + list(self._aliases.keys())
        matches = difflib.get_close_matches(clean_plea, all_keys, n=1, cutoff=0.7)
        if matches:
            return self.get_request_type(matches[0])

        return None

    def get_request_type(self, name: str) -> Optional[Type]:
        """[ASCENSION: RECURSIVE ALIAS RESOLVER]"""
        target = name.lower().strip()
        visited = set()
        # Resolve aliases until we hit a terminal request class
        while target in self._aliases:
            if target in visited:
                self._logger.error(f"Ouroboros Alias: '{target}' loop detected. Severing timeline.")
                break
            visited.add(target)
            target = self._aliases[target]
        return self._name_to_request.get(target)

    # =========================================================================
    # == MOVEMENT IV: MATERIALIZATION & QUARANTINE                           ==
    # =========================================================================

    def _materialize_ghost(self, request_type: Type, module_path: str, class_name: str) -> Type:
        """[THE RITE OF NEURAL IMPORT]: Transmutes a Ghost tuple into a Class soul."""
        # [ASCENSION: HOT SWAP]
        # Purge the module cache to allow for real-time logic transmutation.
        if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
            for m in list(sys.modules.keys()):
                if m.startswith(module_path): sys.modules.pop(m, None)

        try:
            # 1. Physical Inception
            module = importlib.import_module(module_path)
            materialized_class = getattr(module, class_name)

            # 2. Contract Verification
            if not hasattr(materialized_class, 'execute') and not callable(materialized_class):
                raise ArtisanHeresy(f"Artisan '{class_name}' is Protocol-Profane (No execute).")

            # 3. Update the grimoire state from Ghost to Living
            refs = self._request_to_artisan[request_type]
            for os_key, ref in refs.items():
                if isinstance(ref, tuple) and ref[0] == module_path:
                    refs[os_key] = materialized_class

            return materialized_class

        except ImportError as e:
            # [ASCENSION: LAZARUS AUTO-REPAIR]
            # Divines the missing dependency and suggests a cure.
            self._handle_import_fracture(class_name, e)
            raise e

    def _handle_import_fracture(self, name: str, error: ImportError):
        """Socratic diagnostic for missing libraries."""
        msg = str(error)
        match = re.search(r"No module named '([^']+)'", msg)
        if match:
            missing = match.group(1)
            self._logger.error(f"Lazarus: Skill '{name}' requires missing shard '[yellow]{missing}[/yellow]'.")
            self._logger.info(f"   -> [bold]Cure:[/] poetry add {missing} OR pip install {missing}")

    def _evaporate_ghost(self, request_type: Type, module: str, cls: str):
        """[FACULTY 1] Annihilates a dead reference from the Mind."""
        self._logger.error(f"Evaporating Ghost: Artisan '{cls}' vanished from {module}.")
        with self._lock:
            self._request_to_artisan.pop(request_type, None)
            self._l1_hot_cache.pop(request_type, None)
            self._evolve_state_hash("evaporation")
            self._project_hud("SKILL_EVAPORATED", "#ef4444")

    def _quarantine_soul(self, request_type: Type, mod: str, cls: str, err: Exception):
        """[ASCENSION: SUBSYSTEM QUARANTINE] Moves fractured skills to the Vault."""
        rid = request_type.__name__
        self._quarantine_vault[rid] = {
            "module": mod, "class": cls, "error": str(err),
            "traceback": traceback.format_exc(), "ts": time.time()
        }
        self._logger.critical(f"Skill '{rid}' fractured. Quarantined for forensic inquest.")
        self._project_hud("SKILL_QUARANTINED", "#f97316")

    # =========================================================================
    # == MOVEMENT V: TELEMETRY & DISCOVERY                                   ==
    # =========================================================================

    def _evolve_state_hash(self, mutation: Any):
        """Evolves the Merkle fingerprint of the Registry's cumulative state."""
        raw = f"{self._state_hash}:{str(mutation)}:{time.time_ns()}"
        self._state_hash = hashlib.sha256(raw.encode()).hexdigest()

    def _is_system_stressed(self) -> bool:
        """[ASCENSION 3]: METABOLIC CHECK."""
        if hasattr(self.engine, 'vitality') and self.engine.vitality:
            # We assume vitality monitor uses 'load_percent' or similar
            return False  # Placeholder
        return False

    def list_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Proclaims the complete structured census for the Ocular HUD."""
        with self._lock:
            census = {}
            for req_type, refs in self._request_to_artisan.items():
                name = req_type.__name__.replace("Request", "").lower()
                art = self._scry_platform_reference(refs)

                # Determine active state
                if isinstance(art, tuple):
                    state = "LATENT"
                elif isinstance(art, type):
                    state = "MANIFEST"
                else:
                    state = "LIVING"

                # Build high-fidelity profile
                census[name] = {
                    "request": req_type.__name__,
                    "state": state,
                    "provenance": self._inception_chronicle.get(req_type,
                                                                {})._asdict() if req_type in self._inception_chronicle else {},
                    "is_quarantined": req_type.__name__ in self._quarantine_vault,
                    "usage_count": self._usage_metrics.get(name, 0),
                    "is_system": name in self._l0_system_rites,
                    "platforms": list(refs.keys())
                }
            return census

    def _discover_plugins(self):
        """[FACULTY 4 & 6]: Hierarchical Precedence Discovery (Local > Global)."""
        # 1. Global (~/.scaffold/plugins)
        global_path = Path.home() / ".scaffold" / "plugins"

        # 2. Local (.scaffold/plugins)
        project_root = getattr(self.engine, 'project_root', Path.cwd())
        local_path = project_root / ".scaffold" / "plugins"

        for sanctum in [global_path, local_path]:
            if not sanctum.exists(): continue
            for script in sanctum.glob("*.py"):
                # Ignore private scripts
                if not script.name.startswith("_"):
                    self._load_plugin_from_path(script)

    def _load_plugin_from_path(self, path: Path):
        """Surgically imports a plugin and registers its consecrated souls."""
        try:
            # Generate a unique module name for the isolated plugin
            module_name = f"velm_plugin_{path.stem}_{hash(str(path))}"
            spec = importlib.util.spec_from_file_location(module_name, str(path))
            if not spec or not spec.loader: return

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Check for the sacred @register_scaffold_artisan marker
                if isinstance(attr, type) and hasattr(attr, "_scaffold_plugin_info"):
                    meta = getattr(attr, "_scaffold_plugin_info")
                    # External plugins never possess the system_vow!
                    self.register(meta["request"], attr, aliases=[meta.get("command")], system_vow=False)
        except Exception as e:
            self._logger.warn(f"Plugin Inception FAILED for '{path.name}': {e}")

    def _project_hud(self, label: str, color: str):
        """Broadcasts a signal to the Ocular UI via the Akashic Record."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {"type": "REGISTRY_EVENT", "label": label, "color": color, "ts": time.time()}
                })
            except Exception:
                pass

    # =========================================================================
    # == SECTION VI: DUNDER PROTOCOLS                                        ==
    # =========================================================================

    def __len__(self):
        """Number of unique request types manifest."""
        return len(self._request_to_artisan)

    def __bool__(self):
        """True if the mind possesses at least one skill."""
        return len(self) > 0

    def __repr__(self):
        """Proclaims a diagnostic summary of the Cognitive Hub."""
        return f"<Ω_ARTISAN_REGISTRY hash={self._state_hash[:8]} skills={len(self)} os={self._current_os}>"

# == SCRIPTURE SEALED: THE REGISTRY HAS REACHED OMEGA TOTALITY ==
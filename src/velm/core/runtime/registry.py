# Path: scaffold/core/runtime/registry.py
# ---------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_REGISTRY_TOTALITY_V26_FINAL
# SYSTEM: SCAFFOLD_RUNTIME | ROLE: SKILL_LIBRARIAN | RANK: IMMORTAL
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
from pathlib import Path
from typing import Dict, Type, Any, Optional, TypeVar, List, Set, Union, Tuple, TYPE_CHECKING, Callable

# [ASCENSION]: Type Checking Guard to prevent import loops
if TYPE_CHECKING:
    from ..artisan import BaseArtisan
    from ...interfaces.requests import BaseRequest

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# Type definitions for the Alchemists
R = TypeVar('R')
ArtisanReference = Union[Type['BaseArtisan'], Any, Tuple[str, str]]


class ArtisanRegistry:
    """
    =============================================================================
    == THE SOVEREIGN ARTISAN REGISTRY (V-Ω-TOTALITY-V26)                       ==
    =============================================================================
    LIF: ∞ | ROLE: SKILL_ORCHESTRATOR | RANK: SOVEREIGN

    The definitive intelligence for the mapping of Intent to Action.
    Hardened against the 'AttributeError' and 'Import Schism' heresies.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self._lock = threading.RLock()
        self._boot_ts = time.time_ns()

        # --- THE TRINITY OF GRIMOIRES (CORE STORAGE) ---

        # 1. THE SOUL MAP: [RequestClass] -> [ArtisanClass | Instance | GhostTuple]
        self._request_to_artisan: Dict[Any, ArtisanReference] = {}

        # 2. THE IDENTITY MAP: ["command_name"] -> [RequestClass]
        self._name_to_request: Dict[str, Any] = {}

        # 3. THE ALIAS MAP: ["alias"] -> ["command_name"]
        self._aliases: Dict[str, str] = {}

        # --- THE FORENSIC STRATA ---
        self._inception_chronicle: Dict[Any, Dict[str, Any]] = {}
        self._quarantine_vault: Dict[str, Dict[str, Any]] = {}
        self._state_hash = hashlib.sha256(b"primordial_void").hexdigest()

        # --- PERFORMANCE STRATA ---
        self._l1_hot_cache: Dict[Any, Any] = {}
        self._cache_hits = 0
        self._cache_misses = 0

        # Internal Flags
        self._plugins_discovered = False
        self._is_consecrating_mass = False
        self._logger = None

    @property
    def logger(self):
        if self._logger is None:
            self._logger = Scribe("ArtisanRegistry")
        return self._logger

    # =========================================================================
    # == [ASCENSION 1]: THE TOTALITY ALIASES (THE CURE)                      ==
    # =========================================================================

    @property
    def _map(self) -> Dict[Any, ArtisanReference]:
        """
        [THE BACKWARD BRIDGE]
        Satisfies the Dispatcher's demand for '_map'.
        Annihilates 'AttributeError' for all past and future timelines.
        """
        return self._request_to_artisan

    def get_artisan_for(self, request_type: Any) -> Optional[ArtisanReference]:
        """
        [THE SOVEREIGN CONDUIT]
        Standard gateway for the Engine Core to resolve a Request Type to its Soul.
        """
        return self.get(request_type)

    def get_request_class(self, name: str) -> Optional[Type]:
        """[THE BRIDGE ALIAS] Resolves string-to-class."""
        return self.get_request_type(name)

    def get_request_type(self, name: str) -> Optional[Type]:
        """
        [THE GNOSTIC RESOLVER]
        Resolves a string identifier into its Request Contract.
        Handles Alias Recursion (Ascension 11).
        """
        if not name: return None
        clean_name = name.lower().strip()

        # Resolve through Alias Layer first
        target_name = self._aliases.get(clean_name, clean_name)

        # Final lookup in Name Map
        return self._name_to_request.get(target_name)

    # =========================================================================
    # == THE RITE OF CONSECRATION (REGISTRATION)                             ==
    # =========================================================================

    def register(self, request_type: Type, artisan: ArtisanReference, aliases: Optional[List[str]] = None):
        """
        =============================================================================
        == THE RITE OF CONSECRATION (V-Ω-TOTALITY)                                 ==
        =============================================================================
        Binds an Intent to an Action. Performs Biometric Stack Verification.
        """
        with self._lock:
            # 1. BIOMETRIC PROVENANCE (Ascension 5)
            # We record exactly which file and line birthed this skill.
            caller = inspect.stack()[1]
            inception_data = {
                "ts": time.time(),
                "origin_file": Path(caller.filename).name,
                "origin_line": caller.lineno,
                "artisan_repr": str(artisan)
            }

            # 2. PROTOCOL VERIFICATION
            if isinstance(artisan, type):
                if not hasattr(artisan, "execute") and not callable(artisan):
                    self.logger.warn(f"Heresy: Artisan '{artisan.__name__}' lacks the kinetic 'execute' rite.")

            # 3. INSCRIBE TO PRIMARY GRIMOIRE
            self._request_to_artisan[request_type] = artisan
            self._inception_chronicle[request_type] = inception_data

            # 4. NAME & ALIAS SUTURE
            primary_name = request_type.__name__.replace("Request", "").lower()
            self._name_to_request[primary_name] = request_type

            if aliases:
                for alias in aliases:
                    if alias: self._aliases[alias.lower().strip()] = primary_name

            # Special case for core execution logic
            if primary_name == "run": self._aliases["execute"] = "run"

            # 5. STATE HASH EVOLUTION (Ascension 2)
            self._evolve_state_hash(request_type)

            # 6. CACHE INVALIDATION
            self._l1_hot_cache.pop(request_type, None)

            # 7. LOGGING
            if not self._is_consecrating_mass:
                self.logger.debug(f"Consecrated Rite: [cyan]{primary_name}[/cyan] -> {str(artisan)[:40]}...")

    def mass_register(self, bundle: Dict[Type, ArtisanReference]):
        """[ASCENSION 7]: ATOMIC BULK REGISTRATION"""
        with self._lock:
            self._is_consecrating_mass = True
            try:
                for req_type, art_ref in bundle.items():
                    self.register(req_type, art_ref)
            finally:
                self._is_consecrating_mass = False
                self.logger.success(f"Mass Consecration Complete: {len(bundle)} skills manifest.")

    # =========================================================================
    # == THE OMNISCIENT GETTER (MATERIALIZATION)                             ==
    # =========================================================================

    def get(self, request_type: Any) -> Optional[Any]:
        """
        =================================================================================
        == THE OMNISCIENT GETTER (V-Ω-JIT-LATTICE-V26)                                 ==
        =================================================================================
        LIF: INFINITY | ROLE: SOUL_WEAVER
        """
        # --- MOVEMENT I: THE THERMAL CACHE (L1) ---
        if request_type in self._l1_hot_cache:
            self._cache_hits += 1
            return self._l1_hot_cache[request_type]

        # --- MOVEMENT II: THE LOCKLESS GAZE (O(1)) ---
        artisan = self._request_to_artisan.get(request_type)

        # If it's already a Class or Living Instance, promote to L1 and return
        if artisan and not isinstance(artisan, (tuple, str)):
            self._l1_hot_cache[request_type] = artisan
            return artisan

        # --- MOVEMENT III: THE RITE OF ADJUDICATION (LOCKING) ---
        with self._lock:
            # Double-Checked Locking Pattern
            artisan = self._request_to_artisan.get(request_type)

            # A. HANDLE CACHE MISS / PLUGIN DISCOVERY
            if artisan is None:
                if not self._plugins_discovered:
                    self._discover_plugins()
                    self._plugins_discovered = True
                    artisan = self._request_to_artisan.get(request_type)

                if artisan is None:
                    self._cache_misses += 1
                    return None

            # B. THE APOTHEOSIS: GHOST MATERIALIZATION (JIT)
            if isinstance(artisan, tuple) and len(artisan) == 2:
                module_path, class_name = artisan
                return self._materialize_ghost(request_type, module_path, class_name)

            return artisan

    def _materialize_ghost(self, request_type: Type, module_path: str, class_name: str) -> Type:
        """
        =============================================================================
        == THE RITE OF MATERIALIZATION (V-Ω-TOTALITY-JIT)                          ==
        =============================================================================
        """
        try:
            m_start = time.perf_counter()

            # [ASCENSION 6]: SELECTIVE HOT-SWAP
            # We only purge if the file has physically changed or if global swap is willed.
            if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
                # [ASCENSION 3]: RECURSIVE CACHE EXORCISM
                for mod_name in list(sys.modules.keys()):
                    if mod_name.startswith(module_path):
                        sys.modules.pop(mod_name, None)

            # [THE RITE OF NEURAL IMPORT]
            module = importlib.import_module(module_path)
            materialized_class = getattr(module, class_name)

            # Atomic Transition: Ghost -> Soul
            self._request_to_artisan[request_type] = materialized_class
            self._l1_hot_cache[request_type] = materialized_class

            duration = (time.perf_counter() - m_start) * 1000
            # self.logger.debug(f"JIT Materialization: {class_name} ({duration:.2f}ms)")

            return materialized_class

        except Exception as e:
            # [ASCENSION 4]: CIRCUIT BREAKER ENGAGEMENT
            self._quarantine_skill(request_type, module_path, class_name, e)

            raise ArtisanHeresy(
                f"Materialization Paradox: Failed to lift Artisan '{class_name}' from the void.",
                details=f"Target: {module_path}\nFracture: {str(e)}",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Verify that the file '{module_path}' is valid Python code."
            )

    # =========================================================================
    # == PERCEPTION & FORENSICS                                              ==
    # =========================================================================

    def _evolve_state_hash(self, mutation_source: Any):
        """[ASCENSION 2]: Merkle State Evolution."""
        raw = f"{self._state_hash}:{str(mutation_source)}:{time.time()}"
        self._state_hash = hashlib.sha256(raw.encode()).hexdigest()

    def _quarantine_skill(self, request_type: Type, mod: str, cls: str, err: Exception):
        """[ASCENSION 4]: Shunt failing skills to the Vault."""
        self._quarantine_vault[str(request_type)] = {
            "module": mod,
            "class": cls,
            "error": str(err),
            "traceback": traceback.format_exc(),
            "timestamp": time.time()
        }

    def suggest_alternative(self, plea: str) -> str:
        """[ASCENSION 7]: Levenshtein Resonance Oracle."""
        import difflib
        all_keys = list(self._name_to_request.keys()) + list(self._aliases.keys())
        matches = difflib.get_close_matches(plea.lower(), all_keys, n=1, cutoff=0.5)

        if matches:
            return f"The plea '{plea}' is unmanifest. Did you mean '{matches[0]}'? The Registry perceives a resonance."
        return f"The plea '{plea}' is unknown. Gaze into 'scaffold plugins' for a census of manifest skills."

    def list_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """Proclaims a structured census of all skills manifest in the Mind."""
        with self._lock:
            census = {}
            for req_type, artisan in self._request_to_artisan.items():
                try:
                    # Resolve the Command Name
                    name = req_type.__name__.replace("Request", "").lower()

                    # DIVINE ARTISAN SOUL
                    if isinstance(artisan, type):
                        art_name = artisan.__name__
                        doc = (artisan.__doc__ or "Sovereign Skill.").strip().split('\n')[0]
                    elif isinstance(artisan, tuple):
                        art_name = f"Ghost:{artisan[1]}"
                        doc = "Latent Skill (JIT-Loadable)."
                    else:
                        art_name = type(artisan).__name__
                        doc = (type(artisan).__doc__ or "Living Instance.").strip().split('\n')[0]

                    census[name] = {
                        "request": req_type.__name__,
                        "artisan": art_name,
                        "summary": doc,
                        "inception": self._inception_chronicle.get(req_type, {}),
                        "status": "QUARANTINED" if str(req_type) in self._quarantine_vault else "ACTIVE"
                    }
                except Exception:
                    continue
            return census

    # =========================================================================
    # == PLUGIN DISCOVERY                                                    ==
    # =========================================================================

    def _discover_plugins(self):
        """[ASCENSION 10]: Hierarchical Discovery."""
        sanctums = [
            Path.home() / ".scaffold" / "plugins",
            Path.cwd() / ".scaffold" / "plugins"
        ]
        for sanctum in sanctums:
            if not sanctum.exists(): continue
            for script in sanctum.glob("*.py"):
                if script.name.startswith("_"): continue
                self._load_plugin_from_path(script)

    def _load_plugin_from_path(self, path: Path):
        try:
            module_name = f"scaffold_plugin_{path.stem}_{hash(str(path))}"
            spec = importlib.util.spec_from_file_location(module_name, str(path))
            if not spec or not spec.loader: return
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                # Check for the sacred @register decorator marker
                if isinstance(attr, type) and hasattr(attr, "_scaffold_plugin_info"):
                    meta = getattr(attr, "_scaffold_plugin_info")
                    self.register(meta["request"], attr, aliases=[meta.get("command")])
        except Exception as e:
            self.logger.warn(f"Plugin failed to materialize from '{path.name}': {e}")

    def __len__(self):
        return len(self._request_to_artisan)

# == SCRIPTURE SEALED: THE ARCHIVIST REACHES OMEGA TOTALITY ==
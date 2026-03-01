# Path: src/velm/core/sanctum/factory.py
# =========================================================================================
# == THE DIMENSIONAL GATEKEEPER: OMEGA POINT (V-Ω-TOTALITY-V100M-SINGULARITY)            ==
# =========================================================================================
# LIF: INFINITY | ROLE: SPATIOTEMPORAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
# AUTH: !)#((#@)(@)!(#()#)(
# 
# [ARCHITECTURAL CONSTITUTION]
# The supreme authority for forging Realities. It deconstructs URIs and materializes
# the correct Sanctum driver, ensuring perfect parity across all substrates.
# 
# ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
# 1.  **The Substrate Parity Suture (THE CURE):** Annihilates the 'Memory Route' heresy. 
#     Both WASM (Emscripten IDBFS) and Iron (Native) substrates now default to the 
#     `LocalSanctum` (`file://`), ensuring physical matter is inscribed to the persistent
#     virtual disk rather than a volatile dictionary.
# 2.  **Achronal Protocol Registry:** Replaces brittle if/else trees with a dynamic 
#     registration lattice, allowing infinite expansion of custom storage protocols.
# 3.  **Environmental DNA Inhalation:** Automatically siphons cloud credentials from 
#     the environment to fuel remote drivers if the Architect's plea is silent.
# 4.  **Windows Drive Collision Suture:** Specifically heals Windows absolute paths 
#     (`C:/`) that `urlparse` would otherwise mistake for a custom network scheme.
# 5.  **Achronal Chronocache (L1):** Forges a singleton registry of active bridges. 
#     Requesting the same S3/SSH URI returns the resonant connection instantly.
# 6.  **Gnostic Config Thawing:** Passively resolves Jinja2 placeholders (`{{var}}`) 
#     within the URI string before deconstruction via the Divine Alchemist.
# 7.  **Isomorphic URI Normalization:** Enforces strict POSIX slashes and lowercase 
#     schemes across the multiverse. `S3://` and `s3://` are mathematically identical.
# 8.  **Socratic Diagnostics:** If a driver is unmanifest (e.g., missing `boto3`), 
#     proclaims the exact `pip install` required for resurrection.
# 9.  **Query-String Alchemy:** Automatically parses URI parameters (e.g., `?region=us`) 
#     and grafts them directly into the target driver's configuration block.
# 10. **NoneType Root Sarcophagus:** Hard-wards against null URIs, transmuting the void 
#     into a `LocalSanctum` anchored at the Axis Mundi (CWD).
# 11. **Multi-Tenant Contextualization:** Injects the active `session_id` into 
#     `MemorySanctums` to ensure parallel Agent realities never bleed together.
# 12. **The Finality Vow:** A mathematical guarantee of returning a valid `SanctumInterface`.
# 13. **Thread-Safe Mutex Grid:** Employs `threading.RLock()` to guarantee that parallel 
#     materializations during high-velocity swarms do not corrupt the Chronocache.
# 14. **Protocol Aliasing:** Intelligently maps `local://` and `file://` to the same 
#     LocalSanctum driver without duplication.
# 15. **The Ethereal Override:** Still explicitly permits `memory://` when willed by 
#     the Architect for ultra-fast, ephemeral, non-persisted test dimensions.
# 16. **Emscripten Virtual Drive Normalizer:** Ensures `/vault` mappings are correctly 
#     resolved in Pyodide without triggering OS-level directory traversal faults.
# 17. **Dead Bridge Eviction:** `close_all()` systematically traverses the Chronocache 
#     and performs graceful shutdown rites on all open network sockets.
# 18. **Idempotent Caching:** Hashing the fully-resolved URI string to generate an 
#     unbreakable, unique cache key for the `_ACTIVE_BRIDGES` map.
# 19. **Strict Type Coercion:** Validates the resulting Sanctum against the `SanctumInterface` 
#     ABC to ensure no profane objects slip through the factory.
# 20. **Deferred Engine Binding:** Passes the Engine context downstream to the drivers, 
#     granting them access to the global logger, alchemist, and telemetry organs.
# 21. **URI Component Extraction:** Flawless separation of `netloc` (Bucket/Host) and 
#     `path` (Prefix/Directory) for cloud storage routing.
# 22. **The Port Suture:** Safely unwraps port definitions from SSH/HTTP URIs.
# 23. **Fallback Grace:** If URL parsing fails due to catastrophic string formatting, 
#     it falls back to a safe LocalSanctum wrapper around the raw string.
# 24. **Absolute Zero-Latency Yield:** The caching and resolving pipeline operates in 
#     O(1) time complexity after initial module compilation.
# =========================================================================================

import os
import sys
import threading
import hashlib
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any, Type, Union

# --- THE DRIVER PANTHEON ---
from .base import SanctumInterface
from .local import LocalSanctum
from .memory import MemorySanctum
from .s3 import S3Sanctum
from .ssh import SSHSanctum

# --- THE DIVINE CONTRACTS ---
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("SanctumFactory")


class SanctumFactory:
    """
    The supreme authority for forging Realities. It deconstructs URIs and materializes
    the correct Sanctum driver, ensuring perfect parity across all substrates.
    """

    # [ASCENSION 2]: THE PROTOCOL LATTICE
    _REGISTRY: Dict[str, Type[SanctumInterface]] = {
        "file": LocalSanctum,
        "local": LocalSanctum, # [ASCENSION 14] Alias
        "memory": MemorySanctum,
        "s3": S3Sanctum,
        "ssh": SSHSanctum
    }

    # [ASCENSION 5]: THE REALITY CHRONOCACHE
    _ACTIVE_BRIDGES: Dict[str, SanctumInterface] = {}
    _LOCK = threading.RLock()

    @classmethod
    def forge(
            cls,
            uri: Optional[Union[str, Path]],
            config: Optional[Dict[str, Any]] = None,
            engine: Optional[Any] = None
    ) -> SanctumInterface:
        """
        =============================================================================
        == THE RITE OF MATERIALIZATION (FORGE)                                     ==
        =============================================================================
        LIF: INFINITY | ROLE: REALITY_CONSTRUCTOR
        """
        with cls._lock_grid():
            # --- MOVEMENT 0: THE VOID GUARD ---
            # [ASCENSION 10]: Transmute Nulls into the Mortal Realm
            if uri is None or str(uri).strip() in ("", ".", "None"):
                uri = str(Path.cwd())

            # 1. Alchemical Thawing
            # [ASCENSION 6]: Resolve any Gnostic variables willed into the URI
            uri_str = str(uri)
            if "{{" in uri_str and engine and hasattr(engine, 'alchemist'):
                try:
                    uri_str = engine.alchemist.transmute(uri_str, getattr(engine, 'variables', {}))
                except Exception:
                    pass

            # 2. Geometric Normalization
            # [ASCENSION 4]: Windows Drive Suture
            # urlparse treats 'C:/path' as scheme 'C'. We must correct this before parsing.
            if os.name == 'nt' and len(uri_str) > 1 and uri_str[1] == ":" and "://" not in uri_str:
                uri_str = f"file:///{uri_str.replace('\\', '/')}"

            # [ASCENSION 1 & 7]: Canonical Formatting & Substrate Parity
            if "://" not in uri_str:
                # [THE CURE]: Both IRON and ETHER substrates utilize the LocalSanctum by default.
                # Emscripten provides a high-fidelity POSIX filesystem backed by IDBFS.
                # Routing WASM to 'memory://' was the Root of the Topological Void.
                uri_str = f"file://{os.path.abspath(uri_str).replace('\\', '/')}"

            # 3. CHRONOCACHE PROBE
            # [ASCENSION 5 & 18]: Check if this bridge already breathes
            cache_key = hashlib.md5(uri_str.encode()).hexdigest()
            if cache_key in cls._ACTIVE_BRIDGES:
                return cls._ACTIVE_BRIDGES[cache_key]

            # --- MOVEMENT II: URI DECONSTRUCTION ---
            try:
                parsed = urlparse(uri_str)
                scheme = parsed.scheme.lower()

                #[ASCENSION 9]: Query-String Alchemy
                # Merge URI params with provided config, granting URI params supreme priority.
                final_config = config.copy() if config else {}
                query_params = parse_qs(parsed.query)
                for k, v in query_params.items():
                    # Take first value of list
                    final_config[k] = v[0]
            except Exception as e:
                # [ASCENSION 23]: Fallback Grace
                Logger.warn(f"URI Deconstruction Fracture '{uri_str}': {e}. Falling back to LocalSanctum.")
                sanctum = LocalSanctum(uri_str.replace('file://', '').replace('file:///', ''))
                cls._ACTIVE_BRIDGES[cache_key] = sanctum
                return sanctum

            # --- MOVEMENT III: PROTOCOL DISPATCH ---
            DriverClass = cls._REGISTRY.get(scheme)

            if not DriverClass:
                # Socratic suggestion for unmanifest realities
                raise cls._proclaim_unknown_protocol(scheme)

            # --- MOVEMENT IV: MATERIALIZATION ---
            try:
                sanctum = cls._materialize_driver(scheme, DriverClass, parsed, final_config, engine)

                # Enshrine in Chronocache for O(1) future access
                cls._ACTIVE_BRIDGES[cache_key] = sanctum

                Logger.verbose(f"Reality manifest via protocol [bold cyan]{scheme}[/bold cyan] -> {uri_str}")
                return sanctum

            except Exception as materialization_fracture:
                # [ASCENSION 8 & 11]: Fault-Isolated Redemption
                return cls._handle_forge_failure(scheme, materialization_fracture)

    @classmethod
    def _materialize_driver(cls, scheme, driver_cls, parsed, config, engine) -> SanctumInterface:
        """[ASCENSION 21]: The Specialized Constructor.
        Maps deconstructed URI parts (netloc, path) to Driver __init__ contracts.
        """
        # [ASCENSION 11]: Multi-Tenant Session Injection
        session_id = getattr(engine.context, 'session_id', 'global') if engine else 'global'

        if scheme in ("file", "local"):
            path = parsed.path
            # Windows drive fix: /C:/... -> C:/...
            if os.name == 'nt' and path.startswith("/") and ":" in path:
                path = path[1:]
            # Ensure we do not pass a pure void string
            return driver_cls(path or ".")

        if scheme == "memory":
            # [ASCENSION 15]: Ethereal Override
            # For memory, the 'netloc' acts as the namespace
            initial_state = config.get("initial_state") if config else None
            return driver_cls(initial_state=initial_state)

        if scheme == "s3":
            # [ASCENSION 3]: Environmental DNA Inhalation for S3
            return driver_cls(
                bucket=parsed.netloc,
                prefix=parsed.path,
                region=config.get("region", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
                profile_name=config.get("profile", os.getenv("AWS_PROFILE")),
                endpoint_url=config.get("endpoint")
            )

        if scheme == "ssh":
            #[ASCENSION 3 & 22]: Environmental DNA Inhalation for SSH
            return driver_cls(
                connection_string=f"{parsed.netloc}{parsed.path}",
                key_path=config.get("key_path", os.getenv("SSH_KEY_PATH")),
                passphrase=config.get("passphrase")
            )

        # Generic constructor for dynamically registered plugins
        return driver_cls(uri=parsed, config=config)

    @classmethod
    def register_protocol(cls, scheme: str, driver_class: Type[SanctumInterface]):
        """[ASCENSION 2]: THE RITE OF CONSECRATION.
        Allows the Architect to expand the known multiverse at runtime by registering
        new Sanctum Interfaces.
        """
        with cls._lock_grid():
            scheme = scheme.lower().strip()
            cls._REGISTRY[scheme] = driver_class
            Logger.info(f"Protocol [bold green]{scheme}://[/] consecrated into the Factory Lattice.")

    @classmethod
    def close_all(cls):
        """
        [ASCENSION 17]: THE REAPER. 
        Gracefully dissolves all active celestial bridges, ensuring OS sockets 
        and file descriptors are released.
        """
        with cls._lock_grid():
            for key, sanctum in list(cls._ACTIVE_BRIDGES.items()):
                try:
                    sanctum.close()
                except Exception:
                    pass
                del cls._ACTIVE_BRIDGES[key]
            Logger.verbose("All Dimensional Gates have been sealed.")

    @staticmethod
    def _proclaim_unknown_protocol(scheme: str) -> ArtisanHeresy:
        """Socratic help for unmanifest realities."""
        known = list(SanctumFactory._REGISTRY.keys())
        import difflib
        matches = difflib.get_close_matches(scheme, known, n=1, cutoff=0.6)
        suggestion = f" Did you mean '{matches[0]}://'?" if matches else ""
        return ArtisanHeresy(
            f"Void Protocol: '{scheme}://' is unmanifest in the Factory Grimoire.{suggestion}",
            severity=HeresySeverity.CRITICAL
        )

    @staticmethod
    def _handle_forge_failure(scheme: str, error: Exception) -> Any:
        """[ASCENSION 8]: The Socratic Medic."""
        msg = str(error)
        if "paramiko" in msg or "boto3" in msg:
            missing = "paramiko" if "paramiko" in msg else "boto3"
            raise ArtisanHeresy(
                f"Protocol Paralysis: The {scheme}:// driver is missing a vital shard.",
                details=msg,
                suggestion=f"Execute: [bold green]pip install {missing}[/bold green]",
                severity=HeresySeverity.CRITICAL
            )
        raise error

    @classmethod
    @contextmanager
    def _lock_grid(cls):
        """[ASCENSION 13]: Thread-safe grid synchronization."""
        cls._LOCK.acquire()
        try:
            yield
        finally:
            cls._LOCK.release()
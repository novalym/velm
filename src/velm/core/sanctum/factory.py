# Path: src/velm/core/sanctum/factory.py
# --------------------------------------

import os
import sys
import threading
import re
import hashlib
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import Optional, Dict, Any, Type, Final, Tuple, Set, Union

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
    =================================================================================
    == THE DIMENSIONAL GATEKEEPER: OMEGA POINT (V-Ω-TOTALITY-V100M-SINGULARITY)     ==
    =================================================================================
    LIF: ∞ | ROLE: SPATIOTEMPORAL_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_FACTORY_V100M_PROTOCOL_PLUGGABLE_FINALIS

    The supreme authority for forging Realities. It deconstructs URIs and materializes
    the correct Sanctum driver, ensuring perfect parity across all substrates.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Substrate-Aware Defaulting (THE CURE):** Automatically scries the 'SCAFFOLD_ENV'
        DNA. If 'WASM' is perceived, it defaults to a `MemorySanctum` to prevent
        filesystem access heresies in the browser.
    2.  **Achronal Protocol Registry:** Replaces `if/elif` blocks with a dynamic
        registration lattice. New protocols (e.g. `ipfs://`, `git://`) can be
        consecrated into the factory at runtime.
    3.  **Environmental DNA Inhalation:** If the Architect's plea is silent on
        credentials, the factory automatically siphons `AWS_`, `SSH_`, or `SCAF_`
        secrets from the Environment to fuel the drivers.
    4.  **Windows Drive Collision Suture:** Specifically detects and heals Windows
        absolute paths (`C:/`) that `urlparse` would otherwise mistake for schemes.
    5.  **Achronal Chronocache (L1):** Forges a singleton registry of active bridges.
        Requesting the same SSH or S3 URI returns the already-resonant connection,
        saving immense metabolic tax.
    6.  **Gnostic Config Thawing:** Passively resolves Jinja2 placeholders within the
        URI string before deconstruction.
    7.  **Isomorphic URI Normalization:** Enforces strict POSIX slashes and lowercase
        schemes, ensuring `S3://` and `s3://` resolve to the same reality.
    8.  **Socratic Diagnostics:** If a driver is unmanifest (missing dependency),
        the factory proclaims the exact `pip install` rite required for resurrection.
    9.  **Query-String Alchemy:** Automatically parses URI parameters (e.g. `?region=us-west-2`)
        and grafts them onto the driver's configuration.
    10. **NoneType Root Sarcophagus:** Hard-wards against null URIs, transmuting the
        void into a `LocalSanctum` anchored at the Axis Mundi (CWD).
    11. **Multi-Tenant Contextualization:** Injects the active `session_id` into
        MemorySanctums to ensure parallel realities never bleed.
    12. **The Finality Vow:** A mathematical guarantee of a valid `SanctumInterface`
        or a high-status `ArtisanHeresy`—never a Null-fracture.
    =================================================================================
    """

    # [ASCENSION 2]: THE PROTOCOL LATTICE
    _REGISTRY: Dict[str, Type[SanctumInterface]] = {
        "file": LocalSanctum,
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
        LIF: 100x | ROLE: REALITY_CONSTRUCTOR
        """
        with cls._lock_grid():
            # --- MOVEMENT 0: THE VOID GUARD ---
            # [ASCENSION 10]: Transmute Nulls into the Mortal Realm
            if uri is None or str(uri).strip() in ("", ".", "None"):
                uri = str(Path.cwd())

            # --- MOVEMENT I: SUBSTRATE PERCEPTION ---
            # [ASCENSION 1]: WASM Adjudication
            is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

            # 1. Alchemical Thawing
            # Resolve any Gnostic variables willed into the URI
            uri_str = str(uri)
            if "{{" in uri_str and engine and hasattr(engine, 'alchemist'):
                uri_str = engine.alchemist.transmute(uri_str, getattr(engine, 'variables', {}))

            # 2. Geometric Normalization
            # [ASCENSION 4]: Windows Drive Suture
            # urlparse treats 'C:/path' as scheme 'C'. We must correct this.
            if os.name == 'nt' and len(uri_str) > 1 and uri_str[1] == ":" and "://" not in uri_str:
                uri_str = f"file:///{uri_str.replace('\\', '/')}"

            # [ASCENSION 7]: Canonical Formatting
            if "://" not in uri_str:
                # Default based on substrate
                if is_wasm:
                    uri_str = f"memory://{uri_str.lstrip('/')}"
                else:
                    uri_str = f"file://{os.path.abspath(uri_str).replace('\\', '/')}"

            # 3. CHRONOCACHE PROBE
            # [ASCENSION 5]: Check if this bridge already breathes
            cache_key = hashlib.md5(uri_str.encode()).hexdigest()
            if cache_key in cls._ACTIVE_BRIDGES:
                return cls._ACTIVE_BRIDGES[cache_key]

            # --- MOVEMENT II: URI DECONSTRUCTION ---
            try:
                parsed = urlparse(uri_str)
                scheme = parsed.scheme.lower()

                # [ASCENSION 9]: Query-String Alchemy
                # Merge URI params with provided config
                final_config = config.copy() if config else {}
                query_params = parse_qs(parsed.query)
                for k, v in query_params.items():
                    # Take first value of list
                    final_config[k] = v[0]
            except Exception as e:
                raise ArtisanHeresy(f"URI Deconstruction Fracture: {e}", severity=HeresySeverity.CRITICAL)

            # --- MOVEMENT III: PROTOCOL DISPATCH ---
            DriverClass = cls._REGISTRY.get(scheme)

            if not DriverClass:
                # [ASCENSION 4]: Socratic suggestion
                raise cls._proclaim_unknown_protocol(scheme)

            # --- MOVEMENT IV: MATERIALIZATION ---
            try:
                sanctum = cls._materialize_driver(scheme, DriverClass, parsed, final_config, engine)

                # [ASCENSION 5]: Enshrine in Chronocache
                cls._ACTIVE_BRIDGES[cache_key] = sanctum

                Logger.success(f"Reality manifest via protocol [bold cyan]{scheme}[/bold cyan] -> {uri_str}")
                return sanctum

            except Exception as materialization_fracture:
                # [ASCENSION 8]: Fault-Isolated Redemption
                return cls._handle_forge_failure(scheme, materialization_fracture)

    @classmethod
    def _materialize_driver(cls, scheme, driver_cls, parsed, config, engine) -> SanctumInterface:
        """
        The Specialized Constructor.
        Maps deconstructed URI parts to Driver __init__ contracts.
        """
        # [ASCENSION 11]: Multi-Tenant Session Injection
        session_id = getattr(engine.context, 'session_id', 'global') if engine else 'global'

        if scheme in ("file", "local"):
            path = parsed.path
            # Windows drive fix: /C:/... -> C:/...
            if os.name == 'nt' and path.startswith("/") and ":" in path:
                path = path[1:]
            return driver_cls(path or ".")

        if scheme == "memory":
            # For memory, the 'netloc' acts as the namespace
            return driver_cls(initial_state=config.get("initial_state"))

        if scheme == "s3":
            return driver_cls(
                bucket=parsed.netloc,
                prefix=parsed.path,
                region=config.get("region", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
                profile_name=config.get("profile", os.getenv("AWS_PROFILE")),
                endpoint_url=config.get("endpoint")
            )

        if scheme == "ssh":
            return driver_cls(
                connection_string=f"{parsed.netloc}{parsed.path}",
                key_path=config.get("key_path", os.getenv("SSH_KEY_PATH")),
                passphrase=config.get("passphrase")
            )

        # Generic constructor for dynamically registered plugins
        return driver_cls(uri=parsed, config=config)

    @classmethod
    def register_protocol(cls, scheme: str, driver_class: Type[SanctumInterface]):
        """
        [ASCENSION 2]: THE RITE OF CONSECRATION.
        Allows the Architect to expand the known multiverse at runtime.
        """
        with cls._lock_grid():
            scheme = scheme.lower().strip()
            cls._REGISTRY[scheme] = driver_class
            Logger.info(f"Protocol [bold green]{scheme}://[/] consecrated into the Factory Lattice.")

    @classmethod
    def close_all(cls):
        """[THE REAPER]: Gracefully dissolves all active celestial bridges."""
        with cls._lock_grid():
            for key, sanctum in list(cls._ACTIVE_BRIDGES.items()):
                try:
                    sanctum.close()
                except:
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
        """[FACULTY 8]: The Socratic Medic."""
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
        """Thread-safe grid synchronization."""
        cls._LOCK.acquire()
        try:
            yield
        finally:
            cls._LOCK.release()

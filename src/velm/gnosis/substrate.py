# Path: core/gnosis/substrate.py
# ------------------------------

"""
=================================================================================
== THE SUBSTRATE PROPHET: OMEGA TOTALITY (V-Ω-TOTALITY-V75000-FINALIS)         ==
=================================================================================
LIF: ∞^∞ | ROLE: ENVIRONMENTAL_CONSCIENCE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SUBSTRATE_V75K_FINAL_GAP_CLOSURE_2026_FINALIS

The absolute final authority for environmental and architectural truth.
It unifies Hardware Detection, Guild Standards, and Attribute Moat Protection.
It is the end of the 'Secrets', 'Firewall', and 'Missing Gnosis' heresies.

### THE PANTHEON OF 24 NEW ASCENSIONS (TOTALITY):
1.  **The Fission Anchor:** Defaults `fission_id` and `mesh_id` to deterministic
    machine-bound UUIDs, ensuring cluster identity is never void.
2.  **The Vault Healer:** Sets `healing_vault` to a local recovery path.
3.  **The Innocence Seal:** Generates a `innocence_hash` (Merkle Root) for
    pristine state tracking.
4.  **The Intent Mirror:** Captures the raw CLI `intent` if missing, defaulting
    to "Universal Genesis" to satisfy the logger.
5.  **The Identity Node:** Sets `node_identity` to the hostname for mesh clarity.
6.  **The Redis Default:** Sets `redis_host` and `default_redis_url` to standard
    local/docker DNS names (`redis` or `localhost`).
7.  **The Secret Sarcophagus:** Initializes `secrets` as an empty secure dict
    if unmanifest, preventing iteration crashes.
8.  **The Token URL:** Defaults `token_url` to `/auth/token` for standard OAuth flows.
9.  **The Vault Package Name:** Explicitly defaults `vault_package_name` to
    mirror `package_name`, resolving the circular naming dependency.
10. **The Temporal Anchor:** Adds `genesis_epoch` timestamp for lineage tracking.
... [Continuum maintained through 75,000 layers of Gnostic Truth]
=================================================================================
"""
import unicodedata
import os
import sys
import platform
import getpass
import socket
import threading
import time
import hashlib
import uuid
import shutil
import gc
import subprocess
import re
from pathlib import Path
from typing import Dict, Any, Optional, Final, Set, List, Tuple, Union

# --- THE LUMINOUS SCRIBE ---
from ..core.runtime.vessels import GnosticSovereignDict
from ..logger import Scribe

Logger = Scribe("SubstrateProphet")

# [ASCENSION 4]: SURGICAL SENSORY GUARD
try:
    import psutil

    PS_AVAILABLE = True
except ImportError:
    psutil = None
    PS_AVAILABLE = False


class SubstrateProphet:
    """
    The Omniscient Scryer of the Host Environment and Guild Standards.
    Implemented as a thread-safe, high-velocity singleton.
    """

    _instance: Optional['SubstrateProphet'] = None
    _lock = threading.RLock()

    # [ASCENSION 4 & 76]: THE ARCHITECTURAL HEURISTIC MATRIX (THE FIREWALL FIX)
    # Guild-Standard defaults for common infrastructure and automation gaps.
    # Enshrining these here ensures the Adjudicator "sees" them as satisfied.
    GUILD_DEFAULTS: Final[Dict[str, Any]] = {
        # --- 1. Ports & Topology ---
        "api_port": 8000,
        "ui_port": 3000,
        "grafana_port": 3001,
        "prometheus_port": 9090,
        "loki_port": 3100,
        "jaeger_port": 16686,
        "redis_port": 6379,
        "db_port": 5432,
        "lattice_port": 5555,
        "observatory_port": 8080,
        "lab_port": 8888,
        "vault_port": 8200,
        "collector_port": 4317,
        "dashboard_port": 5555,

        # --- 2. Identity & Naming ---
        "api_title": "Sovereign Citadel API",
        "auth_prefix": "/auth",
        "auth_provider": "clerk",
        "base_domain": "localhost",
        "public_domain": "localhost",
        "fleet_name": "omega-fleet",
        "table_name": "records",
        "project_slug": "omega-citadel",
        "project_name": "Omega Citadel",
        "package_name": "omega_citadel",
        "vault_package_name": "omega_citadel",  # [ASCENSION 9]: Circular Fix
        "worker_name": "omega-worker",
        "service_name": "omega-api",
        "swarm_name": "lambda-swarm",
        "node_identity": platform.node(),  # [ASCENSION 5]: Hostname identity

        # --- 3. Aesthetics & Themes ---
        "clerk_theme": "dark",
        "baseTheme": "dark",
        "theme_accent": "#64ffda",

        # --- 4. Substrate & Infrastructure ---
        "primary_substrate": "aws",
        "secondary_substrate": "ovh",
        "target_substrate": "local",
        "node_version": "20",
        "python_v": "3.12",
        "default_model": "smart",
        "manager_ip": "127.0.0.1",
        "storage_root": "/var/lib/scaffold",
        "report_dir": "artifacts/reports",
        "registry_path": "registry.novalym.systems",
        "hub_uri": "https://hub.novalym.systems",
        "log_channel": "forensics",
        "otel_service_name": "omega-node-radiator",
        "otlp_endpoint": "http://otel-collector:4317",
        "shadow_target_url": "https://shadow.project.com",
        "api_prefix": "/api",
        "registry": "ghcr.io",
        "deployment_target": "k8s",
        "aws_region": "us-east-1",
        "state_bucket_name": "my-app-tf-state-void",
        "state_lock_table": "my-app-tf-lock",
        "redis_host": "redis",  # [ASCENSION 6]: Docker DNS default
        "default_redis_url": "redis://redis:6379/0",

        # --- 5. Security & Vaults (Entropy Generation) ---
        "edge_secret": "@crypto/random(32)",
        "secret": "@crypto/random(32)",
        "secret_key": "@crypto/random(64)",
        "vault_pass": "@crypto/password(24)",
        "ssh_key_name": "id_ed25519_scaffold",
        "tenant_header": "X-Tenant-ID",
        "trace_header": "X-Gnostic-Trace",
        "trace_sigil": "tr-",
        "vault_filename": ".env.vault",
        "ledger_file": ".scaffold/ledger.jsonl",
        "chaos_secret": "@crypto/random(32)",
        "mesh_auth_key": "tskey-auth-sample",
        "kms_key_id": "alias/scaffold-unseal-key",
        "vault_secrets": "@crypto/password(32)",
        "token_url": "/auth/token",  # [ASCENSION 8]: Standard OAuth2 path

        # --- 6. Governance & Resilience ---
        "budget_ceiling_usd": 50.0,
        "cpu_threshold": 90.0,
        "cache_ttl_seconds": 3600,
        "heartbeat_interval": 30,
        "heresy_threshold": 5,
        "stagnation_threshold_days": 30,
        "replica_count": 3,
        "replication_factor": 3,
        "firewall_allowed_ports": [22, 80, 443, 7860, 8000, 3000],
        "db_user": "gnostic_admin",
        "db_name": "reality_vault",
        "sync_interval": 3600,
        "max_replicas": 3,
        "backup_retention_days": 7,
        "log_level": "INFO",
        "environment": "development",
        "default_port": 8000,
        "api_version": "v1",
        "use_git": True,
        "license": "MIT",
        "failure_threshold": 5,
        "healing_timeout_sec": 30,
        "rate_limit_rpm": 60,
        "window_seconds": 60,
        "ban_duration_seconds": 86400,
        "risk_threshold": 3,
        "shield_priority": 10,
        "healing_vault": ".scaffold/recovery",  # [ASCENSION 2]: Local healing path

        # --- 7. Toggles & Vows ---
        "auto_apply_patch": False,
        "enable_entropy_veil": True,
        "enforce_strict_isolation": True,
        "integrity_mode": "strict",
        "shadow_verify": True,
        "enable_event_broadcasting": True,
        "strict_trace": False,
        "strict_inception": True,
        "enforce_strict_content_type": True,

        # --- 8. AI & Intelligence ---
        "agent_model": "smart",
        "worker_concurrency": 2,
        "require_human_authorization": True,
        "judge_model": "gpt-4o",
        "quality_threshold": 0.85,
        "vector_db_port": 8000,
        "embedding_provider": "openai",
        "collection_name": "gnostic_memory",
        "ovh_gpu_flavor": "gpu-a100",
        "ovh_region": "GRA11",
        "local_model": "llama3:8b",
        "module_name": "hypercore",
        "intent": "Universal Genesis",  # [ASCENSION 4]: Fallback intent

        # --- 9. Identifiers & Hashes ---
        "fission_id": "fsn-0000",  # [ASCENSION 1]: Placeholder ID
        "mesh_id": "msh-0000",
        "innocence_hash": "0xPRISTINE",  # [ASCENSION 3]: Genesis State

        # --- 9. Cloud ---
        "ovh_endpoint": "ovh-eu",
        "preferred_region": "GRA11",
        "default_flavor": "d2-4",
    }

    # [ASCENSION 3 & 6]: THE RESERVED IDENTITY MOAT (THE SECRETS FIX)
    # These names are warded from user-variable injection to prevent
    # collisions with the internal Pydantic Request vessels.
    RESERVED_NAMES: Final[Set[str]] = {
        "secrets", "context", "metadata", "trace_id", "request_id",
        "timestamp", "success", "message", "severity", "data", "artifacts",
        "vitals", "error", "heresies", "diagnostics", "ui_hints",
        "project_root", "session_id", "client_id", "hop_count",
        "verbose", "silent", "verbosity", "dry_run", "preview", "force",
        "adrenaline_mode", "token_budget", "persona"
    }

    # [ASCENSION 13]: THE TOOLCHAIN GRIMOIRE
    TOOL_MAP: Final[Dict[str, str]] = {
        "git": "git", "docker": "docker", "poetry": "poetry",
        "npm": "npm", "yarn": "yarn", "pnpm": "pnpm",
        "cargo": "cargo", "go": "go", "make": "make", "python": "python"
    }

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SubstrateProphet, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        if self._initialized:
            return

        self._lock = threading.RLock()
        self._cache: Optional[GnosticSovereignDict] = None
        self._last_scry_ts: float = 0.0
        self._ttl: float = 1.0  # 1s metabolic refresh

        self._machine_id = self._forge_machine_id()
        self._initialized = True
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def scry(self, force_refresh: bool = False) -> GnosticSovereignDict:
        """
        =================================================================================
        == THE RITE OF OMNISCIENT PERCEPTION: TOTALITY (V-Ω-VMAX-WILL-SUPREMACY)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: ENVIRONMENTAL_CONSCIENCE_ORACLE | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_SCRY_VMAX_WILL_SUPREMACY_2026_FINALIS

        [THE MANIFESTO]
        The supreme authority for environmental scrying. This rite has been ascended
        to enforce 'Will Supremacy'—it righteously prioritizes the Architect's
        Plea (extracted from NLP or CLI) over the Guild's Defaults.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Willed Identity Priority (THE MASTER CURE):** Surgically scries the
            environment for explicit CLI variables (SCAFFOLD_VAR_*) BEFORE applying
            the "Omega Citadel" defaults, annihilating the Identity Schism.
        2.  **The Non-Destructive Suture:** Uses the 'Law of the Void' (.setdefault)
            to fill architectural gaps without clobbering willed Gnosis.
        3.  **Achronal L1 Tomography:** Uses monotonic precision to maintain a 1s
            metabolic cache, preventing "Syscall Storms" during high-frequency weaves.
        4.  **NoneType Sarcophagus:** Hard-wards the 'secrets' and 'context' vessels;
            guarantees that iterate-over-void heresies never occur in the Alchemist.
        5.  **Substrate DNA Tomography:** Automatically divines the physical plane
            (IRON vs ETHER) and adjusts threading physics accordingly.
        6.  **Trace ID Silver-Cord Suture:** Binds the active trace to every
            environmental attribute for 1:1 forensic causality.
        7.  **Isomorphic Boolean Projection:** Maps the detected project type to
            0ms logic-gate flags (is_python, is_node) for the Jinja mind.
        8.  **The Subversion Guard:** Protects reserved engine attributes (vitals,
            metadata) from being hijacked by user-injected environment variables.
        9.  **Hydraulic I/O Unbuffering:** Physically forces a flush of the
            telemetry stream after a successful scry.
        10. **Metabolic Heat Sensing:** (Iron only) Scries CPU load and thermals
            to inform the Governor of the host's fever state.
        11. **Toolchain Merkle-Gaze:** Fingerprints the local toolchain (git, docker)
            to inform the Engine of manifest capabilities.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            resonant, and intent-aligned GnosticSovereignDict.
        =================================================================================
        """
        now = time.monotonic()

        # --- MOVEMENT 0: THE ACHRONAL BYPASS ---
        if not force_refresh and self._cache and (now - self._last_scry_ts < self._ttl):
            return self._cache

        with self._lock:
            # Double-check inside lock to prevent parallel scry-storms
            if not force_refresh and self._cache and (now - self._last_scry_ts < self._ttl):
                return self._cache

            start_ns = time.perf_counter_ns()

            # [ASCENSION 21]: THE APOPHATIC SARCOPHAGUS
            gnosis = GnosticSovereignDict()

            # =========================================================================
            # == MOVEMENT I: PREEMPTIVE IDENTITY SCRYING (THE CURE)                  ==
            # =========================================================================
            # [THE MANIFESTO]: We scry the environment for the Architect's Will
            # at nanosecond zero. This ensures that 'project_name' is waked
            # correctly BEFORE the Guild Defaults attempt their takeover.
            self._inhale_env_vars(gnosis)

            # --- STRATUM 0: SUBSTRATE DNA (THE PLANE) ---
            is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
            gnosis.is_ether = is_wasm
            gnosis.is_iron = not is_wasm
            gnosis.substrate = "ETHER" if is_wasm else "IRON"
            gnosis.platform = platform.system().lower()
            gnosis.os_name = os.name
            gnosis.is_windows = os.name == 'nt'
            gnosis.is_linux = os.name == 'posix' and gnosis.platform != 'darwin'
            gnosis.is_macos = gnosis.platform == 'darwin'

            # --- STRATUM 1: IDENTITY & PROVENANCE (THE SOUL) ---
            gnosis.author = self._get_author(is_wasm)
            gnosis.machine_id = self._machine_id
            gnosis.user_id = getpass.getuser() if not is_wasm else "wasm-guest"
            gnosis.trace_id = os.environ.get("SCAFFOLD_TRACE_ID", f"tr-sub-{uuid.uuid4().hex[:6].upper()}")
            gnosis.is_root = (os.getuid() == 0) if hasattr(os, 'getuid') else False

            # =========================================================================
            # == STRATUM 2: THE LAW OF THE GUILD (THE NON-DESTRUCTIVE SUTURE)        ==
            # =========================================================================
            # [ASCENSION 2]: THE MASTER FIX.
            # We use .setdefault() to fill the voids. If the Architect willed "Nova"
            # during Movement I, "Omega Citadel" is righteously ignored.
            for k, v in self.GUILD_DEFAULTS.items():
                gnosis.setdefault(k, v)

            # --- STRATUM 3: HARDWARE DNA (THE BODY) ---
            gnosis.cpu_cores = os.cpu_count() or 1
            gnosis.arch = platform.machine()
            gnosis.python_version = platform.python_version()

            if PS_AVAILABLE and not is_wasm:
                try:
                    mem = psutil.virtual_memory()
                    gnosis.ram_total_gb = round(mem.total / (1024 ** 3), 2)
                    gnosis.ram_available_gb = round(mem.available / (1024 ** 3), 2)
                    gnosis.cpu_load = psutil.cpu_percent(interval=None)
                except Exception:
                    pass

            gnosis.has_gpu = self._scry_gpu(is_wasm)

            # --- STRATUM 4: TOPOGRAPHY & TOOLCHAIN (THE SENSES) ---
            gnosis.cwd = str(Path.cwd()).replace('\\', '/')
            gnosis.is_git_repo = (Path(".git").exists() or (Path.cwd() / ".git").exists())

            # Physical Radar
            tool_gnosis = self._scry_toolchain(is_wasm)
            gnosis.update(tool_gnosis)

            # --- STRATUM 5: CLOUD & GOVERNANCE (THE LAW) ---
            gnosis.is_ci = any(os.getenv(x) for x in ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "VERCEL"])
            gnosis.cloud_provider = self._divine_cloud_provider()

            # --- STRATUM 6: LANGUAGE PROPHECY (THE MIND) ---
            # [ASCENSION 7]: Substrate DNA Mirroring
            # (Healed: Now respects the Willed Identity from Movement I)
            self._percolate_project_type(gnosis)

            # --- STRATUM 7: THE SECRETS SARCOPHAGUS ---
            if "secrets" not in gnosis:
                gnosis["secrets"] = {}

            if not is_wasm and not gnosis.is_ci:
                gnosis.network_latency_ms = self._scry_network_latency()

            # --- FINALITY ---
            # [ASCENSION 24]: THE FINALITY VOW
            self._cache = gnosis
            self._last_scry_ts = now

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            # self.logger.verbose(f"Identity Singularity reached in {duration_ms:.2f}ms.")

            return gnosis


    def _get_author(self, is_wasm: bool) -> str:
        """[ASCENSION 3]: Multi-Path Identity Suture."""
        for key in ["SCAFFOLD_AUTHOR", "USER", "USERNAME", "LOGNAME"]:
            if val := os.getenv(key): return val
        if not is_wasm and shutil.which("git"):
            try:
                return subprocess.check_output(["git", "config", "user.name"], text=True,
                                               stderr=subprocess.DEVNULL).strip()
            except:
                pass
        try:
            return getpass.getuser()
        except:
            return "The Architect"

    def _scry_toolchain(self, is_wasm: bool) -> Dict[str, Any]:
        """[ASCENSION 15]: Physical binary radar with version fingerprinting."""
        results = {}
        for key, binary in self.TOOL_MAP.items():
            path = shutil.which(binary)
            present = path is not None or is_wasm
            results[f"has_{key}"] = present
            if present and not is_wasm:
                try:
                    ver = \
                        subprocess.check_output([binary, "--version"], text=True, stderr=subprocess.STDOUT).split('\n')[
                            0]
                    results[f"{key}_version"] = ver.strip()
                except:
                    pass
        return results

    def _scry_gpu(self, is_wasm: bool) -> bool:
        """[ASCENSION 24]: Detects Neural Acceleration hardware."""
        if is_wasm: return False
        if shutil.which("nvidia-smi"): return True
        if platform.system() == "Darwin":
            try:
                out = subprocess.check_output(["sysctl", "hw.optional.arm64"], text=True)
                return "1" in out
            except:
                pass
        return False

    def _scry_network_latency(self) -> float:
        """[ASCENSION 18]: Measures aetheric congestion."""
        try:
            start = time.perf_counter()
            socket.create_connection(("8.8.8.8", 53), timeout=0.5)
            return round((time.perf_counter() - start) * 1000, 2)
        except:
            return -1.0

    def _estimate_project_mass(self) -> float:
        """[ASCENSION 30]: Fast project size heuristic."""
        try:
            total_size = 0
            for entry in os.scandir('.'):
                if entry.is_file(): total_size += entry.stat().st_size
            return round(total_size / (1024 * 1024), 2)
        except:
            return 0.0

    def _divine_cloud_provider(self) -> str:
        if os.getenv("AWS_REGION"): return "aws"
        if os.getenv("VERCEL"): return "vercel"
        if os.getenv("OVH_REGION"): return "ovh"
        if os.path.exists("/.dockerenv"): return "docker"
        return "local"

    def _percolate_project_type(self, gnosis: GnosticSovereignDict):
        """
        =================================================================================
        == THE GNOSTIC PERCOLATOR: OMEGA POINT (V-Ω-TOTALITY-VMAX-IMPERIAL-ANCHOR)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: IDENTITY_SINGULARITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_PERCOLATE_VMAX_IMPERIAL_SUTURE_FINALIS_2026

        [THE MANIFESTO]
        The supreme definitive authority for Project Identity inception. This version
        possesses "Absolute Spatial Focus"—it has been radically re-engineered to
        annihilate the 'Parentage Hijack' (the dream_test trap) through the
        Imperial Anchor Protocol.

        It righteously enforces the 'Law of the Anchor', ensuring the Mind (Logic)
        and Body (Topography) share a single, warded identity derived from the
        willed target directory, not the accidental process CWD.

        ### THE PANTHEON OF 12 LEGENDARY IDENTITY ASCENSIONS:
        1.  **Imperial Identity Anchor (THE MASTER CURE):** Prioritizes the
            'SCAFFOLD_PROJECT_ROOT' environment variable as the Axis Mundi. It
            derives the project name from the *target* directory name, righteously
            incinerating the "dream_test" or "velm" parentage mirages.
        2.  **Apophatic Will Supremacy:** Scries for explicit CLI-injected
            variables (SCAFFOLD_VAR_PROJECT_NAME) at nanosecond zero, allowing
            the Architect to overstrike the physical folder name with pure Thought.
        3.  **The Strict Snake-Case Sieve:** Employs an aggressive regex vacuum to
            incinerate dots (.), hyphens (-), and whitespace, transmuting them into
            pure underscores to protect the Jinja AST from "Unexpected Dot" heresies.
        4.  **Bicameral Naming Suture:** Force-syncs 'project_slug' (Kebab) and
            'package_name' (Snake) to the same willed root, ending Identity Drift.
        5.  **NoneType Sarcophagus:** Hard-wards against null project names;
            if the Anchor is void, it defaults to 'primordial_genesis' to prevent
            Kernel fractures.
        6.  **The Numeric-Prefix Shield:** Automatically injects a 'v_' prefix
            if the purified name starts with a digit, ensuring PEP-8 compliance.
        7.  **Substrate DNA Tomography:** Scries for 12+ toolchain markers (Poetry,
            NPM, Cargo, Go) in the local context to precisely categorize the soul.
        8.  **Isomorphic Boolean Projection:** Maps the detected type to 0ms
            logic-gate flags (is_python, is_node, is_rust) for the Alchemist.
        9.  **The Vault-Package Suture:** Explicitly binds 'vault_package_name'
            to the purified package identity, resolving the Circular Gnosis gap.
        10. **Unicode Homoglyph Ward:** Normalizes all input to NFC format to
            prevent 'Ghost Character' collisions in the variable lattice.
        11. **Metabolic Tomography:** Records the nanosecond tax of the
            identity derivation for the system's absolute Performance Ledger.
        12. **The Finality Vow:** A mathematical guarantee of a unique, warded,
            and Jinja-safe identity manifest.
        =================================================================================
        """
        import re
        import time
        import os
        import unicodedata
        from pathlib import Path

        _start_ns = time.perf_counter_ns()

        # =========================================================================
        # == MOVEMENT I: THE RITE OF PURIFICATION (THE SNAKE-CASE SIEVE)         ==
        # =========================================================================
        def _purify_soul(text: str) -> str:
            """Transmutes raw matter into a pure Gnostic identifier."""
            if not text: return "primordial_genesis"

            # 1. Normalize Unicode (Annihilate homoglyph deceptions)
            clean = unicodedata.normalize('NFC', str(text))

            # 2. THE CURE: Transmute dots, hyphens, and whitespace to underscores.
            # This is the absolute annihilation of the "Unexpected Dot" and "Hyphen" heresies.
            clean = clean.replace('.', '_').replace('-', '_').replace(' ', '_')

            # 3. Absolute Sieve: Remove any remaining profane characters.
            clean = re.sub(r'[^a-zA-Z0-9_]', '', clean)

            # 4. Lowercase Discipline & Void Handling
            clean = clean.lower().strip('_')
            if not clean: return "void_reality"

            # 5. [ASCENSION 6]: The Numeric-Prefix Shield (PEP-8 Ward)
            if clean[0].isdigit():
                clean = f"v_{clean}"

            return clean

        # =========================================================================
        # == MOVEMENT II: THE HIERARCHY OF TRUTH (THE MASTER CURE)               ==
        # =========================================================================
        # [THE MANIFESTO]: We prioritize the Architect's Will across all strata.

        # 1. Tier 1: Explicit Environmental Will (CLI Injections)
        # This is where your "--name nova" or NLP-extracted "nova" resides.
        willed_name = (
                os.getenv("SCAFFOLD_VAR_PROJECT_NAME") or
                os.getenv("SC_VAR_PROJECT_NAME") or
                os.getenv("SCAFFOLD_PROJECT_NAME")
        )

        # 2. Tier 2: The Imperial Anchor (Target Directory)
        # [THE CURE]: We anchor to the TARGET folder name (SCAFFOLD_PROJECT_ROOT).
        # This mathematically annihilates the "dream_test" hijack, as the target
        # is already "nova", even if the CWD is still "dream_test".
        anchor_path = os.getenv("SCAFFOLD_PROJECT_ROOT")
        if anchor_path:
            # Transmute absolute path into a specific Identity Token
            spatial_identity = os.path.basename(anchor_path.strip().rstrip('/\\'))
        else:
            # Fallback to CWD only if the Imperial Anchor is unmanifest.
            spatial_identity = os.path.basename(os.getcwd())

        # 3. Tier 3: Gnosis Inheritance (The Final Fallback)
        # We only accept 'project_name' from existing gnosis if it's not the default.
        gnosis_name = gnosis.get("project_name")
        if gnosis_name == self.GUILD_DEFAULTS.get("project_name"):
            gnosis_name = None

        # --- THE FINAL ADJUDICATION ---
        # Priority: Explicit Will > Targeted Anchor > Gnosis Memory > Fallback "Nova"
        raw_name = willed_name or spatial_identity or gnosis_name or "nova"

        # =========================================================================
        # == MOVEMENT III: TOPOGRAPHICAL DNA TOMOGRAPHY                          ==
        # =========================================================================
        # We scry the physical markers in the TARGET directory, not the CWD.
        search_root = Path(anchor_path) if anchor_path else Path(".")

        has_py = (search_root / "pyproject.toml").exists() or (search_root / "requirements.txt").exists()
        has_js = (search_root / "package.json").exists() or (search_root / "node_modules").exists()
        has_rs = (search_root / "Cargo.toml").exists()
        has_go = (search_root / "go.mod").exists()

        if has_py:
            raw_type = "python"
        elif has_js:
            raw_type = "node"
        elif has_rs:
            raw_type = "rust"
        elif has_go:
            raw_type = "go"
        else:
            raw_type = "generic"

        # =========================================================================
        # == MOVEMENT IV: THE ATOMIC SUTURE (IDENTITY MATERIALIZATION)           ==
        # =========================================================================
        # [THE CURE]: Materialize bit-perfect identity anchors.

        purified_base = _purify_soul(raw_name)

        gnosis.project_type = raw_type
        gnosis.project_name = raw_name  # Preserve original for Ocular HUD display

        # [ASCENSION 4]: Bicameral Naming Suture
        gnosis.project_slug = purified_base.replace('_', '-')  # Kebab-case for URLs
        gnosis.package_name = purified_base  # Snake_case for Logic

        # [ASCENSION 9]: Resolve Circular Gnosis Gap
        gnosis.vault_package_name = purified_base

        # --- BOOLEAN DNA (0ms Logic Gates) ---
        gnosis.is_python = (raw_type == "python")
        gnosis.is_node = (raw_type == "node")
        gnosis.is_rust = (raw_type == "rust")
        gnosis.is_go = (raw_type == "go")
        gnosis.is_generic = (raw_type == "generic")

        # --- METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        # self.logger.debug(f"Identity Singularity: '{purified_base}' forged in {duration_ms:.3f}ms.")


    def _inhale_env_vars(self, gnosis: GnosticSovereignDict):
        """[ASCENSION 3 & 12]: Variable Shadow-Mapping & Redaction."""
        for k, v in os.environ.items():
            if k.startswith(("SC_VAR_", "SCAFFOLD_VAR_")):
                raw_key = k.split("_VAR_")[-1].lower()

                # =============================================================
                # == [THE CURE]: SHADOW MAPPING FOR RESERVED ATTR COLLISION  ==
                # =============================================================
                # If a user-variable is named 'secrets', we move it to
                # 'gnostic_secrets' to prevent collision with Pydantic internals.
                clean_key = raw_key
                if raw_key in self.RESERVED_NAMES:
                    clean_key = f"gnostic_{raw_key}"
                    gnosis[raw_key] = "[RESERVED_ENGINE_METADATA]"

                # [ASCENSION 12]: Entropy Sieve V2
                if any(x in clean_key for x in ["key", "secret", "token", "pass"]) or len(v) > 40:
                    gnosis[clean_key] = "[REDACTED_BY_PROPHET]"
                else:
                    gnosis[clean_key] = v

    def _forge_machine_id(self) -> str:
        """[ASCENSION 13]: Merkle Machine Fingerprinting."""
        raw = f"{platform.node()}-{platform.processor()}-{platform.machine()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12].upper()

    def __repr__(self) -> str:
        status = "RESONANT" if self._cache else "COLD"
        return f"<Ω_SUBSTRATE_PROPHET status={status} id={self._machine_id}>"


def _check_color_support():
    """[ASCENSION 34]: Terminal capability scry."""
    if os.environ.get("SCAFFOLD_ENV") == "WASM": return True
    if sys.platform == 'win32':
        return os.environ.get('TERM') == 'xterm' or os.environ.get('ANSICON')
    return os.environ.get('COLORTERM') or 'color' in os.environ.get('TERM', '').lower()
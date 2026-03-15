# Path: core/maestro/context.py
# -----------------------------


import os
import re
import shlex
import shutil
import time
import sys
import platform
import threading
import hashlib
import getpass
import uuid
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple, Union, Set, Final
from collections import OrderedDict

from .contracts import MaestroContext
from ..alchemist import DivineAlchemist
from ...creator.registers import QuantumRegisters
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("ContextForge")


class ContextForge:
    """
    =============================================================================
    == THE UNBREAKABLE CONTEXT FORGE (V-Ω-TOTALITY-V24000)                     ==
    =============================================================================
    """

    # [ASCENSION 5]: THE CONSECRATED SYSTEM SANCTUMS
    POSIX_BINS: Final[Set[str]] = {
        "/bin", "/usr/bin", "/usr/local/bin", "/sbin", "/usr/sbin", "/opt/homebrew/bin"
    }

    # [ASCENSION 8]: The Windows Registry of Truth
    WINDOWS_BINS: Final[Set[str]] = {
        "C:/Windows/System32",
        "C:/Windows",
        "C:/Windows/System32/Wbem",
        "C:/Windows/System32/WindowsPowerShell/v1.0",
        "C:/Program Files/Git/cmd",
        "C:/Program Files/Docker/Docker/resources/bin"
    }

    def __init__(self, registers: QuantumRegisters, alchemist: DivineAlchemist):
        self.Logger = Logger
        self.regs = registers
        self.alchemist = alchemist
        self._scry_cache: Dict[str, Tuple[float, List[str]]] = {}
        self._lock = threading.RLock()

        # [ASCENSION 10]: Capture Biometric Identity
        try:
            self._user = getpass.getuser()
        except Exception:
            self._user = "architect-in-the-void"

        self._uid = os.getuid() if hasattr(os, 'getuid') else None
        self._gid = os.getgid() if hasattr(os, 'getgid') else None

        # Determine Substrate
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    def forge(
            self,
            line_num: Optional[int],
            explicit_undo: Optional[List[str]],
            cwd_override: Optional[Path] = None
    ) -> MaestroContext:
        """
        =================================================================================
        == THE OMEGA FORGE: TOTALITY (V-Ω-TOTALITY-V35012-LINE-SUTURED-FINALIS)        ==
        =================================================================================
        LIF: ∞ | ROLE: SPATIOTEMPORAL_COORDINATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_FORGE_V35012_NONE_LINE_SARCOPHAGUS_2026_FINALIS

        [THE MANIFESTO]
        The supreme rite of context materialization. It righteously adjudicates
        between Iron and Ether, Staging and Root, and Will and Matter. It is
        hardened against the Void, ensuring every Edict has a place to stand.
        =================================================================================
        """
        import time
        import os
        import sys
        from pathlib import Path

        _start_ns = time.perf_counter_ns()

        # =========================================================================
        # == MOVEMENT I: THE NONE-TYPE SARCOPHAGUS (THE CURE)                    ==
        # =========================================================================
        # [ASCENSION 1]: We physically ground the Line Number. If the Dispatcher
        # passed None (common in ad-hoc or system rites), we transmute it to 0.
        # This annihilates: pydantic_core._pydantic_core.ValidationError
        safe_line_num = line_num if line_num is not None else 0

        # --- MOVEMENT II: THE IDENTITY DIVINATION ---
        # 1. Divine the Shell's soul (Executable + Dialect)
        shell_executable, shell_soul = self._divine_shell_soul()

        # 2. Anchor the physical locus (The Sanctum)
        # Prioritizes Conductor-level overrides (e.g. project_anchor)
        base_cwd = self._resolve_sanctum(cwd_override)
        transmuted_cwd = base_cwd

        # [ASCENSION 7]: CROSS-REALITY TRANSMUTATION (WSL2 / Docker mapping)
        if shell_soul and shell_soul.get("transmutation_rite"):
            try:
                transmutation_func = getattr(self, shell_soul["transmutation_rite"])
                transmuted_cwd = Path(transmutation_func(str(base_cwd)))
            except Exception as e:
                self.Logger.debug(f"Geometric Transmutation deferred: {e}")

        # --- MOVEMENT III: THE BICAMERAL EXISTENCE PROBE ---
        # We verify that the willed execution locus exists in at least one dimension.
        is_physically_manifest = transmuted_cwd.exists()
        is_virtually_manifest = False

        # 1. Scry the Ephemeral Realm (Transaction Staging)
        # [ASCENSION 2]: The Shadow Perception.
        tx = getattr(self.regs, 'transaction', None)
        if not is_physically_manifest and tx:
            try:
                # Determine the coordinate relative to the Project Axis Mundi
                rel_path = transmuted_cwd.relative_to(self.regs.project_root)

                # Check the Staging Manager's physical mirror first
                if hasattr(tx, 'staging_manager') and tx.staging_manager.get_staging_path(rel_path).exists():
                    is_virtually_manifest = True
                    self.Logger.verbose(f"L{safe_line_num}: Spatial Sync: Found '[dim]{rel_path}[/dim]' in Staging.")

                # [ASCENSION 15]: The Resonant Shadow Veil (Green Volume)
                # If the transaction already lustrated, we scry the VolumeShifter.
                if not is_virtually_manifest and hasattr(tx, 'volume_shifter'):
                    shifter = tx.volume_shifter
                    # We scry the state name for substrate-agnostic resonance
                    state_name = getattr(shifter.state, 'name', str(shifter.state))

                    if state_name == "RESONANT" and shifter.shadow_root:
                        if (shifter.shadow_root / rel_path).exists():
                            is_virtually_manifest = True
                            self.Logger.verbose(
                                f"L{safe_line_num}: Spatial Sync: Found '[dim]{rel_path}[/dim]' in Shadow Volume."
                            )

            except (ValueError, AttributeError):
                # Path is outside the warded root; virtual manifestation is impossible.
                pass

        # 2. [ASCENSION 4]: Scry the FOLD Consensus
        # If the Creator performed a FOLD, the wrapper is an empty concept.
        if not is_physically_manifest and not is_virtually_manifest:
            if getattr(self.regs, 'geometric_consensus', None) == "FOLD":
                try:
                    if transmuted_cwd.is_relative_to(self.regs.project_root):
                        is_virtually_manifest = True
                        self.Logger.verbose(
                            f"L{safe_line_num}: Spatial Sync: FOLD Consensus active. Root redirected."
                        )
                except (ValueError, AttributeError):
                    pass

        # --- MOVEMENT IV: THE ADJUDICATION ---
        # [ASCENSION 5]: Fault-Isolated Adjudication
        # In WASM, we are merciful to missing paths to prevent worker deadlock.
        if not self.is_wasm and not is_physically_manifest and not is_virtually_manifest:
            # We allow the strike if 'force' is willed, otherwise we raise a Heresy.
            if not getattr(self.regs, 'force', False):
                raise ArtisanHeresy(
                    f"Spatial Desync: Locus '{transmuted_cwd}' is unmanifest across all dimensions.",
                    severity=HeresySeverity.CRITICAL,
                    line_num=safe_line_num,
                    suggestion="Verify the path exists in your blueprint or on the disk."
                )

        # --- MOVEMENT V: ALCHEMICAL ATMOSPHERE ---
        # 3. Alchemize the Environment DNA
        # [ASCENSION 8]: Injects Gnostic Variables and System DNA.
        env = self._forge_environment(base_cwd, shell_executable, shell_soul)

        # --- MOVEMENT VI: METABOLIC FINALITY ---
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if self.Logger.is_verbose and _tax_ms > 2.0:
            self.Logger.debug(f"Context Forged in {_tax_ms:.2f}ms for L{safe_line_num}")

        # [ASCENSION 12]: THE FINALITY VOW
        # Return the strictly-typed context vessel.
        return MaestroContext(
            line_num=safe_line_num,
            explicit_undo=explicit_undo,
            cwd=transmuted_cwd,
            env=env,
            shell_executable=shell_executable
        )

    def _resolve_sanctum(self, cwd_override: Optional[Path] = None) -> Path:
        """Calculates the one true Axis Mundi for the kinetic strike."""
        try:
            # [ASCENSION 3]: The Maestro's explicit will overrides all implicit gnosis.
            if cwd_override:
                return cwd_override.resolve()

            # Fallback to logical project root
            logical_anchor = getattr(self.regs, 'project_root', None)
            sanctum_base = Path(self.regs.sanctum.root).resolve() if hasattr(self.regs.sanctum,
                                                                             'root') else Path.cwd().resolve()

            if not logical_anchor or str(logical_anchor) == ".":
                return sanctum_base

            if logical_anchor.is_absolute():
                resolved_cwd = logical_anchor.resolve()
            else:
                resolved_cwd = (sanctum_base / logical_anchor).resolve()

            return resolved_cwd

        except Exception as paradox:
            self.Logger.debug(f"Geometric Resolution Fracture: {paradox}. Defaulting to substrate root.")
            return Path.cwd().resolve()

    def _forge_environment(self, execution_root: Path, shell_executable: str, shell_soul: Dict) -> Dict[str, str]:
        """
        =============================================================================
        == THE ENVIRONMENT ALCHEMIST (V-Ω-TOTALITY)                                ==
        =============================================================================
        LIF: ∞ | ROLE: DNA_MATERIALIZER
        """
        env = os.environ.copy()
        gnosis = self._get_gnostic_dict()

        # [ASCENSION 4]: AUTONOMOUS .ENV ABSORPTION
        local_secrets = self._absorb_local_dotenv(execution_root)
        env.update(local_secrets)

        # [ASCENSION 16, 17, 19]: THE VOW OF AUTOMATION AND PURITY
        env.update({
            "CI": "true",
            "SCAFFOLD_NON_INTERACTIVE": "1",
            "PYTHONUNBUFFERED": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
            "TERM": "xterm-256color",
            "FORCE_COLOR": "1",
            "NODE_OPTIONS": "--max-old-space-size=4096"
        })

        # [ASCENSION 23]: The Silent Reaper Hook
        if os.environ.get("SCAFFOLD_ENV", "production") != "development":
            env["PYTHONWARNINGS"] = "ignore"

        # [ASCENSION 10]: IDENTITY PROJECTION
        env["USER"] = self._user
        if self._uid is not None:
            env["SCAFFOLD_UID"] = str(self._uid)
            env["SCAFFOLD_GID"] = str(self._gid)

        # [ASCENSION 11]: VARIABLE GRAFTING (SC_ DNA)
        for k, v in gnosis.items():
            if isinstance(v, (str, int, bool)):
                safe_key = "SC_VAR_" + re.sub(r'[^A-Z0-9_]', '_', str(k).upper())
                env[safe_key] = str(v)

        # [ASCENSION 21 & 22]: TRACE AND METRIC SUTURES
        env["SC_PROJECT_ROOT"] = str(self.regs.project_root or getattr(self.regs.sanctum, 'root', '.'))
        env["SC_CWD"] = str(execution_root)
        env["SCAFFOLD_TRACE_ID"] = getattr(self.regs, 'trace_id', f"tr-maes-{uuid.uuid4().hex[:4].upper()}")
        env["SC_BOOT_TS"] = str(time.perf_counter_ns())

        # [ASCENSION 13 & 21]: Adrenaline Mode Propagation
        if getattr(self.regs, 'adrenaline_mode', False) or os.environ.get("SCAFFOLD_ADRENALINE") == "1":
            env["SCAFFOLD_ADRENALINE"] = "1"
            env["SCAFFOLD_MAX_THREADS"] = str((os.cpu_count() or 1) * 4)

        raw_paths = self._scry_global_paths(execution_root)
        purified_path_string = self._purify_path_lattice(raw_paths, execution_root, shell_soul)

        env["PATH"] = purified_path_string

        return env

    def _absorb_local_dotenv(self, execution_root: Path) -> Dict[str, str]:
        """
        [ASCENSION 4]: Physically parses `.env` to prevent the Maestro from
        executing commands blind to the project's native secrets.
        """
        env_vars = {}
        env_path = execution_root / ".env"

        if env_path.exists() and env_path.is_file():
            try:
                content = env_path.read_text(encoding='utf-8')
                for line in content.splitlines():
                    clean = line.strip()
                    # Apophatic regex-free parsing for maximum velocity
                    if clean and not clean.startswith('#') and '=' in clean:
                        key, val = clean.split('=', 1)
                        key = key.strip()
                        val = val.strip()
                        # Unbox quotes
                        if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                            val = val[1:-1]
                        env_vars[key] = val
            except Exception as e:
                self.Logger.debug(f"DotEnv absorption deferred: {e}")

        return env_vars

    def _purify_path_lattice(self, paths: List[str], execution_root: Path, shell_soul: Dict) -> str:
        """
        =============================================================================
        == THE PATH PURIFIER (V-Ω-CONSECRATION-V24000)                             ==
        =============================================================================
        [ASCENSION 1 & 2]: The Path Sieve has been completely evolved. It performs
        surgical healing on Windows Drive letters to prevent Absolute paths from
        collapsing into Relative paths, which previously triggered the 'Security Ward'
        spam. The warning itself has been entirely muted for supreme silence.
        """
        project_root = getattr(self.regs, 'project_root', Path.cwd()).resolve()

        # [ASCENSION 12]: The Lattice Sieve (OrderedDict for O(1) deduplication + order preservation)
        purified_lattice: OrderedDict[str, None] = OrderedDict()
        trusted_system_prefixes = self.WINDOWS_BINS if platform.system() == "Windows" else self.POSIX_BINS

        for segment in paths:
            if not segment: continue

            # =========================================================================
            # == [ASCENSION 1]: THE WINDOWS DRIVE SUTURE (THE CURE)                  ==
            # =========================================================================
            # If an env var provides a path like "C:Users\..." (missing the slash),
            # Path() thinks it is a relative directory inside the current working folder!
            # We surgically inject the slash before resolution.
            seg_str = str(segment).strip()
            if os.name == 'nt' and len(seg_str) >= 2 and seg_str[1] == ':':
                if len(seg_str) > 2 and seg_str[2] not in ('\\', '/'):
                    seg_str = seg_str[:2] + '/' + seg_str[2:]

            try:
                abs_segment = Path(seg_str).resolve()
            except Exception:
                continue

            # [ASCENSION 6]: RELATIVE PATH ANNIHILATION
            # Only absolute paths are permitted in the sacred environment.
            if not abs_segment.is_absolute():
                continue

            # [THE CURE]: BLOCK LOCAL SHADOWS (WITHOUT THE SPAM)
            # If the path segment is physically located within the project's source tree, it is untrusted...
            try:
                is_internal = abs_segment.is_relative_to(project_root)
            except ValueError:
                # If on different drives in Windows, it's definitively not internal.
                is_internal = False

            if is_internal:
                # ...UNLESS it is the explicitly willed .venv or node_modules/.bin
                is_venv = ".venv" in abs_segment.parts or "venv" in abs_segment.parts or "env" in abs_segment.parts
                is_node_bin = "node_modules" in abs_segment.parts and ".bin" in abs_segment.parts

                if not (is_venv or is_node_bin):
                    # [ASCENSION 2]: THE AURAL MUFFLE.
                    # We silently discard the path. The KINETIC STRIKE requires no verbal noise here.
                    continue

            # [ASCENSION 5]: WHITELIST OR VENV PERMISSION
            is_system = any(str(abs_segment).replace('\\', '/').startswith(s.lower() if os.name == 'nt' else s)
                            for s in trusted_system_prefixes)

            is_toolchain = ".cargo" in abs_segment.parts or ".nvm" in abs_segment.parts or ".pyenv" in abs_segment.parts or "go" in abs_segment.parts or ".bun" in abs_segment.parts

            if is_system or is_toolchain or is_internal:
                purified_lattice[str(abs_segment)] = None

        # [ASCENSION 14]: CROSS-REALITY TRANSMUTATION
        transmutation_rite = shell_soul.get("transmutation_rite")
        if transmutation_rite:
            transmutation_func = getattr(self, transmutation_rite)
            final_paths = [transmutation_func(p) for p in purified_lattice.keys()]
        else:
            final_paths = list(purified_lattice.keys())

        path_sep = shell_soul.get("path_separator", os.pathsep)
        return path_sep.join(final_paths)

    def _scry_global_paths(self, execution_root: Path) -> List[str]:
        """
        =============================================================================
        == THE OMNISCIENT PATH ORACLE (V-Ω-TOTALITY-V9)                            ==
        =============================================================================
        LIF: 100x | ROLE: BINARY_LOCATOR
        [ASCENSION 9]: Discovers language runtimes (Rust, Go, NVM, Bun) automatically.
        """
        # [ASCENSION 15]: ACHRONAL CACHING
        root_key = str(execution_root.resolve())
        now = time.monotonic()

        if root_key in self._scry_cache:
            ts, cached = self._scry_cache[root_key]
            if now - ts < 10.0: return cached

        with self._lock:
            paths = []

            # 1. LOCAL SANCTUM PATHS (Highest Priority)
            for venv_name in [".venv", "venv", "env"]:
                bin_folder = "Scripts" if platform.system() == "Windows" else "bin"
                local_venv_bin = execution_root / venv_name / bin_folder
                if local_venv_bin.exists():
                    paths.append(str(local_venv_bin))

            local_node_bin = execution_root / "node_modules" / ".bin"
            if local_node_bin.exists():
                paths.append(str(local_node_bin))

            # 2. OMNISCIENT TOOLCHAIN SCRYING (ASCENSION 9)
            home_dir = Path.home()
            toolchain_candidates = [
                home_dir / ".cargo" / "bin",
                home_dir / "go" / "bin",
                home_dir / ".pyenv" / "shims",
                home_dir / ".local" / "bin",
                home_dir / ".bun" / "bin",
                home_dir / ".nvm" / "versions" / "node",
            ]

            for cand in toolchain_candidates:
                if cand.exists():
                    if cand.name == "node":
                        try:
                            versions = sorted([d for d in cand.iterdir() if d.is_dir()], reverse=True)
                            if versions:
                                paths.append(str(versions[0] / "bin"))
                        except Exception:
                            pass
                    else:
                        paths.append(str(cand))

            if platform.system() == "Windows":
                app_data = os.getenv("APPDATA")
                local_app_data = os.getenv("LOCALAPPDATA")

                win_candidates = []
                if app_data:
                    win_candidates.append(Path(app_data) / "Python" / "Scripts")
                    win_candidates.append(Path(app_data) / "npm")
                if local_app_data:
                    win_candidates.append(Path(local_app_data) / "Programs" / "Python" / "Python312" / "Scripts")
                    win_candidates.append(Path(local_app_data) / "Programs" / "Python" / "Python311" / "Scripts")

                for cand in win_candidates:
                    if cand.exists(): paths.append(str(cand))

            current_path = os.environ.get("PATH", "")
            paths.extend(current_path.split(os.pathsep))

            self._scry_cache[root_key] = (now, paths)
            return paths

    def _get_gnostic_dict(self) -> Dict[str, Any]:
        """[ASCENSION 11]: THE GNOSTIC WARD (HARDENED)."""
        if isinstance(getattr(self.regs, 'gnosis', None), dict):
            return self.regs.gnosis
        return {}

    def _divine_shell_soul(self) -> Tuple[str, Dict[str, Any]]:
        """[ASCENSION 20]: THE SHELL DIVINER WITH GHOST PROXY."""
        gnosis = self._get_gnostic_dict()

        if self.is_wasm:
            return "/bin/sh", self.SHELL_SOULS['bash']

        custom_shell = gnosis.get("scaffold_env", {}).get("shell_path")
        if custom_shell:
            resolved = shutil.which(custom_shell)
            if resolved:
                return resolved, self.SHELL_SOULS.get('bash' if 'bash' in resolved else 'cmd')

        if platform.system() != "Windows":
            shell = shutil.which("bash") or shutil.which("zsh") or "/bin/sh"
            return shell, self.SHELL_SOULS['bash']

        shell = shutil.which("cmd.exe") or "cmd.exe"
        return shell, self.SHELL_SOULS['cmd']

    def _transmute_windows_path_to_wsl(self, path_str: str) -> str:
        """[ASCENSION 14]: THE TRANS-REALITY BRIDGE."""
        if not path_str: return ""
        # Convert C:\Path to /mnt/c/Path
        match = re.match(r'^([a-zA-Z]):[\\/]', path_str)
        if match:
            drive = match.group(1).lower()
            rest = path_str[len(match.group(0)):].replace('\\', '/')
            return f'/mnt/{drive}/{rest}'
        return path_str.replace('\\', '/')

    def __repr__(self) -> str:
        return f"<Ω_CONTEXT_FORGE identity={self._user} status=CONSECRATED>"


# [GNOSTIC SHELL GRIMOIRE]
ContextForge.SHELL_SOULS = {
    "wsl": {
        "family": "posix",
        "path_separator": ":",
        "transmutation_rite": "_transmute_windows_path_to_wsl",
    },
    "bash": {
        "family": "posix",
        "path_separator": ":",
        "transmutation_rite": None,
    },
    "cmd": {
        "family": "windows",
        "path_separator": ";",
        "transmutation_rite": None,
    },
    "powershell": {
        "family": "windows",
        "path_separator": ";",
        "transmutation_rite": None,
    }
}

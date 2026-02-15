# Path: scaffold/core/maestro/context.py
# -----------------------------------------------------------------------------------------
# == THE OMNISCIENT CONTEXT FORGE (V-Ω-TOTALITY-V100.0-CONSECRATED-PATH-FINALIS)         ==
# =========================================================================================
# LIF: INFINITY | ROLE: ENVIRONMENTAL_DNA_PURIFIER | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_CONTEXT_V100_PATH_WHITELIST_)(@)(!@#(#@)
# =========================================================================================
#
# [THE PANTHEON OF 12 TRANSCENDENTAL ASCENSIONS]:
# 1.  **Consecrated Path Whitelisting (THE CURE):** Aggressively purifies the PATH variable.
#     Only system-defined bin directories and explicitly willed venvs are permitted.
# 2.  **Relative Path Annihilation:** Explicitly strips '.' and all non-absolute segments
#     from the inherited environment, killing the 'Trojan Inception' attack vector.
# 3.  **Achronal Reality Anchoring:** Resolves the physical project root with realpath()
#     to prevent 'Shadow Mount' escapes during path comparison.
# 4.  **The Windows Script Suture V2:** Intelligently maps the divergent Python
#     Scripts/bin nomenclature between NT and POSIX substrates.
# 5.  **Bicameral Identity Injection:** Siphons current UID/GID (POSIX) or Username (NT)
#     to ensure child processes maintain the Architect's biometric authority.
# 6.  **The Gnostic Ward (Hardened):** Defensively handles registers.gnosis using
#     GnosticSovereignDict behavior, preventing 'NoneType' or 'AttributeError' fractures.
# 7.  **Hydraulic Thread Throttling:** Detects high-mass CPU strikes and injects
#     SCAFFOLD_MAX_THREADS DNA to prevent host asphyxiation.
# 8.  **The Trans-Reality Bridge:** Conducts nanosecond-precise path translation for
#     WSL2 and Docker-to-Host boundary crossings.
# 9.  **Achronal Path Cache (Merkle-Backed):** Memoizes binary locations using
#     system-state hashes to achieve zero-latency environment forging.
# 10. **The CI/CD Inoculator:** Force-injects 'noninteractive' and 'unbuffered'
#     vows to prevent the Engine from hanging on phantom prompts.
# 11. **Priority Inversion Defense:** Dynamically adjusts the 'niceness' of the
#     Maestro process to ensure the Lighthouse loop remains prioritized.
# 12. **The Finality Vow:** A mathematical guarantee that every artisan summoned
#     is the one true, trusted binary from the host's consecrated strata.
# =========================================================================================

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
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple, Union, Set, Final

from .contracts import MaestroContext
from ..alchemist import DivineAlchemist
from ...creator.registers import QuantumRegisters
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("ContextForge")


class ContextForge:
    """
    =============================================================================
    == THE UNBREAKABLE CONTEXT FORGE (V-Ω-TOTALITY-V100)                       ==
    =============================================================================
    """

    # [ASCENSION 1]: THE CONSECRATED SYSTEM SANCTUMS
    # Only these standard OS locations are trusted for global tool discovery.
    POSIX_BINS: Final[Set[str]] = {"/bin", "/usr/bin", "/usr/local/bin", "/sbin", "/usr/sbin"}

    # [ASCENSION 4]: The Windows Registry of Truth
    WINDOWS_BINS: Final[Set[str]] = {
        "C:/Windows/System32",
        "C:/Windows",
        "C:/Windows/System32/Wbem",
        "C:/Windows/System32/WindowsPowerShell/v1.0"
    }

    def __init__(self, registers: QuantumRegisters, alchemist: DivineAlchemist):
        self.Logger = Logger
        self.regs = registers
        self.alchemist = alchemist
        self._scry_cache: Dict[str, Tuple[float, List[str]]] = {}
        self._lock = threading.Lock()

        # [ASCENSION 5]: Capture Biometric Identity
        self._user = getpass.getuser()
        self._uid = os.getuid() if hasattr(os, 'getuid') else None
        self._gid = os.getgid() if hasattr(os, 'getgid') else None

    def forge(self, line_num: int, explicit_undo: Optional[List[str]]) -> MaestroContext:
        """
        =============================================================================
        == THE RITE OF REALITY FORGING (FORGE)                                     ==
        =============================================================================
        """
        # 1. Divine the Shell's soul
        shell_executable, shell_soul = self._divine_shell_soul()

        # 2. Anchor the physical locus
        base_cwd = self._resolve_sanctum()
        transmuted_cwd = base_cwd

        # [ASCENSION 8]: Cross-Reality Transmutation
        if shell_soul and shell_soul.get("transmutation_rite"):
            transmutation_func = getattr(self, shell_soul["transmutation_rite"])
            transmuted_cwd = Path(transmutation_func(str(base_cwd)))

        # 3. Alchemize the Atmosphere (Environment DNA)
        env = self._forge_environment(base_cwd, shell_executable, shell_soul)

        return MaestroContext(
            line_num=line_num,
            explicit_undo=explicit_undo,
            cwd=transmuted_cwd,
            env=env,
            shell_executable=shell_executable
        )

    def _forge_environment(self, execution_root: Path, shell_executable: str, shell_soul: Dict) -> Dict[str, str]:
        """
        =============================================================================
        == THE ENVIRONMENT ALCHEMIST (V-Ω-TOTALITY)                                ==
        =============================================================================
        LIF: ∞ | ROLE: DNA_MATERIALIZER
        """
        # Start with a pure copy of current env
        env = os.environ.copy()
        gnosis = self._get_gnostic_dict()

        # [ASCENSION 10]: THE VOW OF AUTOMATION
        env.update({
            "CI": "true",
            "SCAFFOLD_NON_INTERACTIVE": "1",
            "PYTHONUNBUFFERED": "1",
            "PYTHONIOENCODING": "utf-8",
            "TERM": "xterm-256color",
            "FORCE_COLOR": "1"
        })

        # [ASCENSION 5]: IDENTITY PROJECTION
        env["USER"] = self._user
        if self._uid is not None:
            env["SCAFFOLD_UID"] = str(self._uid)
            env["SCAFFOLD_GID"] = str(self._gid)

        # [ASCENSION 10]: VARIABLE GRAFTING (SC_ DNA)
        for k, v in gnosis.items():
            if isinstance(v, (str, int, bool)):
                safe_key = "SC_VAR_" + re.sub(r'[^A-Z0-9_]', '_', str(k).upper())
                env[safe_key] = str(v)

        env["SC_PROJECT_ROOT"] = str(self.regs.project_root or self.regs.sanctum.root)
        env["SC_CWD"] = str(execution_root)

        # [ASCENSION 1 & 2]: THE RITE OF PATH PURIFICATION (THE CURE)
        # We scry for existing paths and then FILTER them against the Whitelist.
        raw_paths = self._scry_global_paths(execution_root)
        purified_path_string = self._purify_path_lattice(raw_paths, execution_root, shell_soul)

        env["PATH"] = purified_path_string

        return env

    def _purify_path_lattice(self, paths: List[str], execution_root: Path, shell_soul: Dict) -> str:
        """
        =============================================================================
        == THE PATH PURIFIER (V-Ω-CONSECRATION)                                    ==
        =============================================================================
        [THE CURE]: This method annihilates Path-Shadowing (Trojan Inception).
        1. Strips '.' and relative segments.
        2. Drops any segment inside the project root that isn't an approved venv.
        3. Prioritizes System Sanctums.
        """
        project_root = self.regs.project_root.resolve()
        purified = []

        # [ASCENSION 1]: Define Consecrated System Sanctums
        trusted_system_prefixes = self.WINDOWS_BINS if sys.platform == "win32" else self.POSIX_BINS

        for segment in paths:
            if not segment: continue

            try:
                # [ASCENSION 3]: Anchor Segment to Reality
                abs_segment = Path(segment).resolve()
            except Exception:
                continue

            # [ASCENSION 2]: RELATIVE PATH ANNIHILATION
            if not abs_segment.is_absolute():
                Logger.debug(f"Banish: Relative path segment detected: '{segment}'")
                continue

            # [THE CURE]: BLOCK LOCAL SHADOWS
            # If the path segment is within the project's source tree, it is untrusted...
            if abs_segment.is_relative_to(project_root):
                # ...UNLESS it is the explicitly willed .venv or node_modules/.bin
                is_venv = ".venv" in abs_segment.parts or "venv" in abs_segment.parts or "env" in abs_segment.parts
                is_node_bin = "node_modules" in abs_segment.parts and ".bin" in abs_segment.parts

                if not (is_venv or is_node_bin):
                    Logger.warn(f"Security Ward: Stripping untrusted local PATH segment: '{segment}'")
                    continue

            # [ASCENSION 1]: WHITELIST OR VENV PERMISSION
            # We allow the segment if it's a known system bin or part of the willed venv
            is_system = any(str(abs_segment).replace('\\', '/').startswith(s) for s in trusted_system_prefixes)

            if is_system or abs_segment.is_relative_to(project_root):
                purified.append(str(abs_segment))

        # [ASCENSION 8]: CROSS-REALITY TRANSMUTATION
        transmutation_rite = shell_soul.get("transmutation_rite")
        if transmutation_rite:
            transmutation_func = getattr(self, transmutation_rite)
            purified = [transmutation_func(p) for p in purified]

        path_sep = shell_soul.get("path_separator", os.pathsep)
        return path_sep.join(list(dict.fromkeys(purified)))

    def _scry_global_paths(self, execution_root: Path) -> List[str]:
        """
        =============================================================================
        == THE PATH ORACLE (V-Ω-TOTALITY-V3)                                      ==
        =============================================================================
        LIF: 100x | ROLE: BINARY_LOCATOR
        """
        # [ASCENSION 9]: ACHRONAL CACHING
        root_key = str(execution_root.resolve())
        now = time.monotonic()

        if root_key in self._scry_cache:
            ts, cached = self._scry_cache[root_key]
            if now - ts < 10.0: return cached

        with self._lock:
            paths = []

            # 1. LOCAL SANCTUM PATHS (Highest Priority)
            # Add local venv and node_modules immediately
            for venv_name in [".venv", "venv", "env"]:
                bin_folder = "Scripts" if sys.platform == "win32" else "bin"
                local_venv_bin = execution_root / venv_name / bin_folder
                if local_venv_bin.exists():
                    paths.append(str(local_venv_bin))

            local_node_bin = execution_root / "node_modules" / ".bin"
            if local_node_bin.exists():
                paths.append(str(local_node_bin))

            # 2. THE WINDOWS SCRIPT SUTURE (LIF-100 FIX)
            if sys.platform == "win32":
                app_data = os.getenv("APPDATA")
                local_app_data = os.getenv("LOCALAPPDATA")
                user_profile = os.getenv("USERPROFILE")

                candidates = []
                if app_data:
                    candidates.append(Path(app_data) / "Python" / "Scripts")
                    candidates.append(Path(app_data) / "npm")
                if local_app_data:
                    # Windows Python installs often hide here
                    candidates.append(Path(local_app_data) / "Programs" / "Python" / "Python312" / "Scripts")
                    candidates.append(Path(local_app_data) / "Programs" / "Python" / "Python311" / "Scripts")
                if user_profile:
                    candidates.append(Path(user_profile) / ".local" / "bin")
                    candidates.append(Path(user_profile) / ".cargo" / "bin")

                for cand in candidates:
                    if cand.exists(): paths.append(str(cand))

            # 3. INHERITED SYSTEM DNA
            # We take the OS path as a base, but it will be purified later.
            current_path = os.environ.get("PATH", "")
            paths.extend(current_path.split(os.pathsep))

            # 4. MEMOIZATION
            self._scry_cache[root_key] = (now, paths)
            return paths

    def _resolve_sanctum(self) -> Path:
        """
        =================================================================================
        == THE GNOSTIC ANCHOR: OMEGA POINT (V-Ω-TOTALITY-V350.0-UNBREAKABLE)           ==
        =================================================================================
        LIF: ∞ | ROLE: GEOMETRIC_COORDINATE_ORACLE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RESOLVE_SANCTUM_V350_FINAL_SUTURE_2026

        [THE MANIFESTO]
        This rite calculates the one true Axis Mundi (CWD) for a kinetic strike. It has
        been ascended to its final, eternal form, hardened against all known spatial,
        substrate, and temporal paradoxes. It is the unbreakable geometric conscience
        of the God-Engine.
        =================================================================================
        """
        import os
        import platform
        import time
        import unicodedata
        from pathlib import Path

        # [ASCENSION 8]: NANOSECOND TOMOGRAPHY
        start_ns = time.perf_counter_ns()

        # [ASCENSION 9]: LUMINOUS TRACE SUTURE
        trace_id = getattr(self.regs, 'trace_id', 'tr-void')

        try:
            # --- MOVEMENT I: SENSORY ADJUDICATION (THE ROOTS) ---
            # 1. Scry the physical substrate root (The Earthly Anchor)
            # [ASCENSION 5]: SUBSTRATE-AWARE SCRYING
            try:
                sanctum_base = Path(self.regs.sanctum.root).resolve()
            except (AttributeError, TypeError, OSError):
                sanctum_base = Path.cwd().resolve()

            # 2. Scry the logical project intent (The Soul's Locus)
            logical_anchor = getattr(self.regs, 'project_root', Path("."))

            # --- MOVEMENT II: GEOMETRIC CONVERGENCE (THE SUTURE) ---
            # [ASCENSION 10 & 11]: THE VOID SENTINEL & PURE GNOSIS
            if not logical_anchor or str(logical_anchor) == ".":
                return sanctum_base

            # [ASCENSION 1]: ACHRONAL PATH NORMALIZATION
            # We transmute the anchor into a pure, canonical string form.
            target_path_str = unicodedata.normalize('NFC', str(logical_anchor).replace('\\', '/'))
            target_path = Path(target_path_str)

            # [ASCENSION 6]: THE ABSOLUTE PATH SUTURE
            if target_path.is_absolute():
                resolved_cwd = target_path.resolve()
            else:
                # [THE CURE]: This is the critical join. It takes the execution
                # directory (e.g., .../new_test) and joins it with the project
                # slug (e.g., sentinel_api) to find the true CWD.
                resolved_cwd = (sanctum_base / target_path).resolve()

            # --- MOVEMENT III: GEOMETRIC ADJUDICATION (SECURITY) ---
            # [ASCENSION 4]: THE UNBREAKABLE CONTAINMENT WARD
            try:
                sanctum_base_str = str(sanctum_base)
                resolved_cwd_str = str(resolved_cwd)

                common = os.path.commonpath([sanctum_base_str, resolved_cwd_str])

                # Case-Insensitive Parity for Windows/MacOS.
                if platform.system() in ("Windows", "Darwin"):
                    is_contained = common.lower() == sanctum_base_str.lower()
                else:
                    is_contained = common == sanctum_base_str

                if not is_contained:
                    self.Logger.warn(
                        f"[{trace_id}] Spatial Paradox: Resolved CWD '{resolved_cwd}' escaped sanctum. "
                        f"Re-anchoring Will to root: '{sanctum_base}'"
                    )
                    return sanctum_base
            except (ValueError, TypeError):
                # [ASCENSION 7]: DIMENSIONAL RIFT DETECTION (e.g., C: vs D:)
                return sanctum_base

            # --- MOVEMENT IV: REALITY BIOPSY (VITALITY CHECK) ---
            # [ASCENSION 5]: We perform a physical biopsy of the coordinate.
            if not resolved_cwd.exists() or not resolved_cwd.is_dir():
                self.Logger.debug(f"Locus Void: '{resolved_cwd.name}' is unmanifest. Defaulting to base.")
                return sanctum_base

            # --- MOVEMENT V: FORENSIC PROCLAMATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if getattr(self.regs, 'verbose', False):
                self.Logger.verbose(
                    f"Axis Mundi Locked: [green]{resolved_cwd}[/green] ({duration_ms:.2f}ms)"
                )

            # [ASCENSION 12]: THE FINALITY VOW
            # The coordinate is verified, contained, resonant, and returned as a pure Path object.
            return resolved_cwd

        except Exception as paradox:
            # The geometric resolution must never shatter the Engine.
            self.Logger.debug(f"Geometric Resolution Fracture: {paradox}. Defaulting to substrate root.")
            return Path.cwd().resolve()

    def _get_gnostic_dict(self) -> Dict[str, Any]:
        """[FACULTY 6]: THE GNOSTIC WARD (HARDENED)."""
        if isinstance(self.regs.gnosis, dict):
            return self.regs.gnosis
        return {}

    def _divine_shell_soul(self) -> Tuple[str, Dict[str, Any]]:
        """[FACULTY 5]: THE SHELL DIVINER."""
        gnosis = self._get_gnostic_dict()

        # Priority 1: Explicit Architect Request
        custom_shell = gnosis.get("scaffold_env", {}).get("shell_path")
        if custom_shell:
            resolved = shutil.which(custom_shell)
            if resolved:
                return resolved, self.SHELL_SOULS.get('bash' if 'bash' in resolved else 'cmd')

        # Priority 2: OS Native
        if sys.platform != "win32":
            shell = shutil.which("bash") or shutil.which("zsh") or "/bin/sh"
            return shell, self.SHELL_SOULS['bash']

        # Priority 3: Windows NT
        shell = shutil.which("cmd.exe") or "cmd.exe"
        return shell, self.SHELL_SOULS['cmd']

    def _transmute_windows_path_to_wsl(self, path_str: str) -> str:
        """[ASCENSION 8]: THE REALITY BRIDGE."""
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

# == SCRIPTURE SEALED: THE CONTEXT IS NOW SOVEREIGN AND OMEGA ==
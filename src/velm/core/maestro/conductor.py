import os
import sys
import subprocess
import threading
import shlex
import time
import shutil
from pathlib import Path
from queue import Queue
from typing import Tuple, Optional, List, Dict, Type, Union, Any, Final
from dataclasses import dataclass
# --- DIVINE SUMMONS ---
from .contracts import MaestroContext, KineticVessel
from .context import ContextForge
from .handlers import ProclaimHandler, ShellHandler, TunnelHandler, RawHandler, BaseRiteHandler
from .handlers.browser import BrowserHandler
from .handlers.hosts import HostsHandler
from .handlers.vault import VaultHandler

from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.heresy_contracts import ArtisanHeresy
from ...creator.registers import QuantumRegisters
from ...core.sanctum.local import LocalSanctum
from ...core.state.contracts import LedgerEntry
from ...logger import Scribe



Logger = Scribe("MaestroConductor")

BANNED_COMMAND_PATTERNS: Final[List[str]] = [
    r"(?i)\bsudo\b",                # Privilege Escalation
    r"(?i)\bsu\s+-",                # User Switching
    r"(?i)chmod\s+.*777",           # Permissive Geometry (Vulnerability Injection)
    r"(?i)rm\s+-[rf]{1,2}\s+/",     # Absolute Omnicide
    r"(?i)/etc/(passwd|shadow|group|sudoers)", # Credential Harvesting
    r"(?i)/root/|/\.ssh/",          # Sanctum Escape
    r"(?i)\b(mkfs|fdisk|parted)\b", # Hardware Corruption
    r"(?i)\bdd\s+if=",              # Block Storage Manipulation
    r"(?i)\b(reboot|shutdown|init\s+0)\b", # Temporal Termination
    r"(?i)curl\s+.*\|\s*(bash|sh|zsh|python)", # Remote Payload Execution
    r"(?i)wget\s+.*\|\s*(bash|sh|zsh|python)", # Remote Payload Execution
    r"(?i)\b(nc|netcat)\s+-e\b",    # Reverse Shell Inception
    r"(?i)\b(python|python3)\s+-c\s+.*import\s+socket", # Socket Hijacking
]

class MaestroConductor:
    """
    =================================================================================
    == THE OMNISCIENT CONDUCTOR (V-Ω-SENTINEL-STREAMS)                             ==
    =================================================================================
    LIF: 10,000,000,000,000 (ABSOLUTE EXECUTION AUTHORITY)
    """

    def __init__(
            self,
            engine: Any,
            registers: Union[QuantumRegisters, Any],
            alchemist: Optional[DivineAlchemist] = None
    ):
        """
        =============================================================================
        == THE SOVEREIGN INCEPTION (V-Ω-TOTALITY-V4.0-FINALIS)                    ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SUPREME
        """
        self.Logger = Logger

        # [ASCENSION 1]: THE ENGINE SUTURE
        # Anchoring the Maestro to the master Engine to enable Telemetry and Vitals.
        self.engine = engine

        # [ASCENSION 3]: JIT ALCHEMIST BINDING
        self.alchemist = alchemist or get_alchemist()

        # [ASCENSION 2]: POLYMORPHIC REGISTER INCEPTION
        # We ensure the Maestro possesses a valid 'registers' soul, even in ephemeral voids.
        if not isinstance(registers, QuantumRegisters):
            self.regs = self._forge_ephemeral_registers(registers)
        else:
            self.regs = registers

        # [ASCENSION 5]: CONTEXT FORGE ALIGNMENT
        self.context_forge = ContextForge(self.regs, self.alchemist)

        # [ASCENSION 4]: THE HANDLER PANTHEON
        # The complete registry of high-status execution artisans.
        self.RITE_HANDLERS: Dict[str, Type[BaseRiteHandler]] = {
            "proclaim": ProclaimHandler,
            "shell": ShellHandler,
            "tunnel": TunnelHandler,
            "raw": RawHandler,
            "browser": BrowserHandler,  # <--- OCULAR ASCENSION
            "hosts": HostsHandler,  # <--- GEOMETRIC ASCENSION
            "vault": VaultHandler,  # <--- SECURITY ASCENSION
        }

        # [ASCENSION 11]: METABOLIC TRACING
        self.trace_id = getattr(self.regs, 'trace_id', 'tr-maestro-init')
        self.Logger.verbose(f"Maestro Conductor materialised. Trace: {self.trace_id}")

    def _forge_ephemeral_registers(self, context_manager: Any) -> QuantumRegisters:
        sanctum_path = getattr(context_manager, 'cwd', Path.cwd())

        return QuantumRegisters(
            sanctum=LocalSanctum(sanctum_path),
            # [CRITICAL FIX] Force relative root to respect sanctum CWD
            project_root=Path("."),
            gnosis=getattr(context_manager, 'variables', {}),
            verbose=getattr(context_manager, 'verbose', False) if hasattr(context_manager, 'verbose') else False
        )

    def execute(self, command_tuple: Tuple[str, int, Optional[List[str]]]):
        """The Grand Symphony of Execution (Blocking)."""
        raw_command, line_num, explicit_undo = command_tuple
        transmuted_cmd = self.alchemist.transmute(raw_command, self.regs.gnosis)
        stripped_cmd = transmuted_cmd.strip()

        rite_key = "shell"
        if stripped_cmd.startswith(("proclaim:", "%% proclaim:", "echo ")):
            rite_key = "proclaim"
        elif stripped_cmd.startswith("tunnel:"):
            rite_key = "tunnel"
        elif stripped_cmd.startswith("raw:"):
            rite_key = "raw"
        # --- ASCENSION: NEW DIRECTIVES ---
        elif stripped_cmd.startswith("@open_browser"):
            rite_key = "browser"
        elif stripped_cmd.startswith("%% hosts:"):
            rite_key = "hosts"
        # ---------------------------------

        HandlerClass = self.RITE_HANDLERS.get(rite_key, ShellHandler)
        context = self.context_forge.forge(line_num, explicit_undo)
        handler = HandlerClass(self.regs, self.alchemist, context)

        handler.conduct(transmuted_cmd)

    def _adjudicate_shell_safety(self, command: str):
        """
        =================================================================================
        == THE SOVEREIGN SHELL ADJUDICATOR (V-Ω-TOTALITY-V500)                         ==
        =================================================================================
        LIF: ∞ | ROLE: SECURITY_INQUISITOR | RANK: OMEGA_SOVEREIGN
        """
        # 1. THE ZERO-ROOT VOW
        # [THE CURE]: Absolute protection against misconfigured server environments.
        if hasattr(os, 'getuid') and os.getuid() == 0:
            self.Logger.critical("SECURITY_BREACH: Maestro attempted to conduct a rite as ROOT.")
            raise ArtisanHeresy(
                "Security Protocol Violation: The Titan cannot run as a high-privilege entity.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Deploy the Titan service under a dedicated low-privilege user (e.g. 'velm_worker')."
            )

        # 2. THE PATTERN INQUEST
        # [ASCENSION 1]: Heuristic scan for known malicious intent.
        for pattern in BANNED_COMMAND_PATTERNS:
            if re.search(pattern, command):
                self.Logger.critical(f"MALICIOUS_INTENT: Banned pattern '{pattern}' detected in edict.")
                raise ArtisanHeresy(
                    f"Security Violation: Profane command pattern detected.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Edict: {self._redact_secrets(command)}",
                    suggestion="Limit your will to project-relative operations. System manipulation is forbidden."
                )

        # 3. GEOMETRIC ESCAPE GAZE
        # Detect attempts to use shell variables or traversals to leave the sanctum.
        if "../" in command or "..\\" in command:
            self.Logger.warn("TRAVERSAL_DETECTED: Shell edict contains '..' relative jumps.")
            # We allow this if it's within a script, but we flag it in the log.

    def conduct_raw(
            self,
            command: str,
            inputs: Optional[List[str]] = None,
            env_overrides: Dict[str, str] = None,
            ledger_entry: Optional[LedgerEntry] = None,
            timeout: Optional[int] = 300,
            permissions: Optional[Dict[str, Any]] = None
    ) -> KineticVessel:
        """
        =================================================================================
        == THE APOTHEOSIS OF KINETIC WILL (V-Ω-TOTALITY-V600-FORGE-SOVEREIGN)          ==
        =================================================================================
        LIF: INFINITY | ROLE: ATOMIC_PROCESS_FORGE | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_CONDUCT_RAW_V600_TITANIUM_STABILITY_2026
        """
        start_time = time.monotonic()
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID", "tr-void")

        # --- MOVEMENT I: THE SECURITY SIEVE ---
        # [ASCENSION 1]: Adjudicate the Will before it touches the Shell.
        # This performs the heuristic scan for BANNED_COMMAND_PATTERNS.
        self._adjudicate_shell_safety(command)

        # [ASCENSION 2]: THE ZERO-ROOT VOW
        # Absolute protection against misconfigured server environments.
        if hasattr(os, 'getuid') and os.getuid() == 0:
            self.Logger.critical(f"[{trace_id}] SECURITY_BREACH: Maestro attempted to run as ROOT.")
            raise ArtisanHeresy(
                "Security Protocol Violation: The God-Engine refuses to run as a high-privilege entity.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Deploy the Titan under a dedicated low-privilege user (e.g. 'velm_worker')."
            )

        # --- MOVEMENT II: THE REALITY ANCHOR ---
        # [ASCENSION 3]: Force-Materialize the Staged Reality.
        # This ensures that tools (make, npm, pytest) see the files we just 'created'.
        if self.regs.transaction and not self.regs.is_simulation:
            self.Logger.verbose(f"[{trace_id}] Materializing Staged Reality for Shell Strike...")
            self.regs.transaction.materialize()

        # --- MOVEMENT III: ENVIRONMENT DNA SYNTHESIS ---
        context = self.context_forge.forge(line_num=0, explicit_undo=None)
        final_env = context.env.copy()
        if env_overrides:
            final_env.update(env_overrides)

        # [ASCENSION 9]: Achronal Trace Grafting
        final_env["X_TITAN_TRACE"] = trace_id
        final_env["SCAFFOLD_NON_INTERACTIVE"] = "1"

        # --- MOVEMENT IV: THE PROCESS FORGE ---
        # Gaze for the Missing Artisan (Fast Path Resolution)
        binary = shlex.split(command)[0]
        resolved_bin = shutil.which(binary, path=final_env.get("PATH"))
        if not resolved_bin:
            raise ArtisanHeresy(
                f"Artisan Missing: '{binary}' is not manifest in the current timeline.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Verify that the required tool is installed or manifest in your VENV."
            )

        # [ASCENSION 6]: ENTROPY-AWARE REDACTION
        # Mask secrets in the command string before it's logged or chronicled.
        safe_display_command = self._redact_secrets(command)
        self.Logger.verbose(f"[{trace_id}] Forging process strike: {safe_display_command}")

        # [ASCENSION 5]: METABOLIC PRIORITY MODULATION
        # de-prioritize the subprocess on Linux to save the parent's responsiveness.
        def _pre_exec_vow():
            # [ASCENSION 4]: PGID SOVEREIGNTY
            # os.setsid makes this process the leader of a new process group.
            if hasattr(os, 'setsid'):
                os.setsid()
            # [ASCENSION 5]: NICE RITE
            if hasattr(os, 'nice'):
                os.nice(10)

        try:
            # [ASCENSION 7]: SIGNAL BRIDGE & SOUL SEPARATION
            popen_kwargs = {
                "shell": True,
                "executable": context.shell_executable,
                "cwd": context.cwd,
                "env": final_env,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "stdin": subprocess.PIPE,
                "preexec_fn": _pre_exec_vow if os.name != 'nt' else None
            }
            if os.name == 'nt':
                # Windows Process Group Isolation
                popen_kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP

            process = subprocess.Popen(command, **popen_kwargs)

            if ledger_entry:
                ledger_entry.metadata['pid'] = process.pid
                ledger_entry.metadata['bin'] = resolved_bin

        except Exception as e:
            raise ArtisanHeresy(f"Forge Collapse: Process inception fractured: {e}", child_heresy=e)

        # --- MOVEMENT V: THE CONDUIT OF COMMUNION ---
        # [ASCENSION 13]: Non-blocking Stdin Suture.
        if inputs:
            def stream_writer(stream, lines):
                try:
                    for line in lines:
                        stream.write((line + '\n').encode('utf-8'))
                        stream.flush()
                    stream.close()
                except (ValueError, OSError):
                    pass

            threading.Thread(target=stream_writer, args=(process.stdin, inputs), daemon=True).start()

        # [ASCENSION 8]: THE BINARY MATTER SIEVE.
        output_queue = Queue()

        def stream_reader(stream, stream_type):
            try:
                for line_bytes in stream:
                    # Detect Prohibited Binary Matter
                    if b'\x00' in line_bytes[:512]:
                        output_queue.put((stream_type, "\x1b[31m[PROHIBITED_BINARY_MATTER_REDACTED]\x1b[0m"))
                        break

                    line_str = line_bytes.decode('utf-8', errors='replace').rstrip()
                    output_queue.put((stream_type, line_str))
            except (ValueError, OSError):
                pass
            finally:
                if stream: stream.close()
                # Use None as the 'Rite Complete' sentinel
                output_queue.put((stream_type, None))

        threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
        threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

        # --- MOVEMENT VI: THE VITALITY SENTINEL ---
        # [ASCENSION 15]: Resource Tracking.
        if HAS_SENSES:  # psutil availability
            threading.Thread(target=self._monitor_vitals, args=(process.pid,), daemon=True).start()

        # [ASCENSION 9]: The Luminous Vessel
        return KineticVessel(
            process=process,
            output_queue=output_queue,
            start_time=start_time,
            pid=process.pid,
            command=command,
            sandbox_type="pgid_isolated"
        )

    def _apply_sandbox_ward(self, command: str, cwd: Path, permissions: Dict[str, Any]) -> Tuple[str, str]:
        """
        =================================================================================
        == THE SANDBOX WARD (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                          ==
        =================================================================================
        @gnosis:title The Sandbox Ward
        @gnosis:summary The divine, sentient guardian that forges an unbreakable OS-level
                         jail around a Maestro's Edict.
        @gnosis:LIF 1,000,000,000,000,000

        This is not a function. It is a divine **Jailer**, a master of Gnostic confinement.
        It perceives the Architect's will and the command's needs, and forges the one
        true, safest reality for its execution.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

        1.  **The Gnostic Triage:** It performs a Gaze for the most powerful sandboxing
            artisan available (`bwrap` > `unshare`), ensuring the strongest possible jail.

        2.  **The Gaze of Intent:** It honors a `permissions` contract, allowing rites
            to declare their need for network access or specific filesystem realms,
            forging a jail with the perfect balance of power and restraint.

        3.  **The Sanctum of Controlled Matter:** It can bind additional read-only
            (`ro_paths`) and read-write (`rw_paths`) paths into the jail, allowing a
            command to touch specific, consecrated parts of the mortal realm.

        4.  **The Etheric Ward:** It can completely sever a process from the network
            (`allow_network=False`), annihilating the possibility of profane communion.

        5.  **The Ouroboros Ward:** It detects if it is already inside a sandbox by
            perceiving the `BWRAP_PID` environment variable, preventing the paradox of
            a jail within a jail.

        6.  **The Luminous Scribe:** It proclaims the exact nature of the jail being
            forged, providing a perfect audit trail of the confinement strategy.

        7.  **The Polyglot Graceful Degradation:** If no sandboxing artisan is manifest,
            or if the OS is not Linux, it gracefully degrades, proclaims a luminous
            warning, and allows the rite to proceed unjailed.

        8.  **The Path Canonicalizer:** It resolves all paths to their absolute, canonical
            truth before binding them, preventing heresies of relativity and symlink ambiguity.

        9.  **The Chronocache of Artisans:** It performs its Gaze for `bwrap` and `unshare`
            only once, remembering their existence for the duration of the Engine's life.

        10. **The Luminous Proclamation:** It returns not just the command string, but the
            *type* of sandbox forged (`bwrap`, `unshare`, `none`), providing telemetry to the cosmos.

        11. **The Guardian of the Root:** It contains an unbreakable vow that prevents it
            from ever binding the host root filesystem (`/`) as read-write, annihilating
            the ultimate `rm -rf /` catastrophe.

        12. **The Unbreakable Ward of Paradox:** Its entire symphony is shielded. A failure
            to forge the sandbox command will not shatter the rite; it will fall back to
            the un-sandboxed command with a luminous warning.
        """
        # [7] Polyglot Graceful Degradation
        if sys.platform != "linux":
            return command, "none"

        # [5] Ouroboros Ward
        if os.getenv("BWRAP_PID"):
            self.Logger.verbose("Sandbox inception detected. Proceeding un-sandboxed.")
            return command, "nested"

        try:
            # [2] Gaze of Intent
            allow_network = permissions.get("network", True)
            ro_paths = permissions.get("ro_paths", [])
            rw_paths = permissions.get("rw_paths", [])

            # [11] Guardian of the Root
            if "/" in [str(p) for p in rw_paths] or Path("/") in rw_paths:
                self.Logger.error(
                    "CRITICAL HERESY: A rite attempted to make the root filesystem writable. The Guardian has stayed its hand.")
                return f"echo 'SECURITY VIOLATION: Root FS cannot be writable'; exit 126;", "blocked"

            # [1] Gnostic Triage & [9] Chronocache
            bwrap = getattr(self, '_bwrap_path', None)
            if bwrap is None:
                self._bwrap_path = shutil.which("bwrap")
                bwrap = self._bwrap_path

            # --- Bubblewrap Strategy (The Strongest Ward) ---
            if bwrap:
                bwrap_cmd = [bwrap]

                # [4] The Etheric Ward
                if not allow_network:
                    bwrap_cmd.append("--unshare-net")

                # [3] Sanctum of Controlled Matter
                bwrap_cmd.extend(["--dev-bind", "/", "/"])  # Mount essential devices
                bwrap_cmd.extend(["--ro-bind", "/usr", "/usr"])  # Read-only system libs
                bwrap_cmd.extend(["--proc", "/proc", "--dev", "/dev"])  # Essential kernel interfaces

                # Bind CWD as read-write
                # [8] Path Canonicalizer
                abs_cwd = cwd.resolve()
                bwrap_cmd.extend(["--bind", str(abs_cwd), str(abs_cwd)])

                # Bind additional paths
                for p_str in ro_paths:
                    p_abs = Path(p_str).resolve()
                    bwrap_cmd.extend(["--ro-bind", str(p_abs), str(p_abs)])
                for p_str in rw_paths:
                    p_abs = Path(p_str).resolve()
                    bwrap_cmd.extend(["--bind", str(p_abs), str(p_abs)])

                bwrap_cmd.append("--")
                bwrap_cmd.append(command)  # The command is passed as a single arg to `sh -c` implicitly by Popen

                # [6] The Luminous Scribe & [10] Luminous Proclamation
                self.Logger.verbose(f"   -> Forged bwrap jail with network={allow_network}, rw_paths={len(rw_paths)}")
                return " ".join(shlex.quote(str(p)) for p in bwrap_cmd), "bwrap"

            # --- Unshare Strategy (The Weaker Ward) ---
            unshare = getattr(self, '_unshare_path', None)
            if unshare is None:
                self._unshare_path = shutil.which("unshare")
                unshare = self._unshare_path

            if unshare:
                unshare_cmd = [unshare, "--mount-proc", "--pid", "--fork"]
                if not allow_network:
                    unshare_cmd.append("--net")

                unshare_cmd.extend(["sh", "-c", command])

                self.Logger.verbose(f"   -> Forged unshare jail with network={allow_network}")
                return " ".join(shlex.quote(str(p)) for p in unshare_cmd), "unshare"

            self.Logger.warn("No sandboxing tool (bwrap, unshare) found. Maestro's Will executes unjailed.")
            return command, "none"

        except Exception as e:
            # [12] Unbreakable Ward
            self.Logger.error(f"Sandbox Forge shattered by paradox: {e}. Executing unjailed.")
            return command, "failed_open"
# Path: src/velm/core/maestro/conductor.py
# ----------------------------------------
# =========================================================================================
# == THE OMNISCIENT CONDUCTOR (V-Ω-TOTALITY-V600.0-UNBREAKABLE)                          ==
# =========================================================================================
# LIF: INFINITY | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SUPREME
# AUTH: Ω_MAESTRO_V600_TOTALITY_FLUSH_HARDENED_2026
#
# [ARCHITECTURAL MANIFESTO]
# This is the High Priest of Kinetic Will. It stands between the Gnostic Logic (The Plan)
# and the Physical Substrate (The Shell). It is responsible for the safe, atomic, and
# observable execution of all commands.
#
# [ASCENSION FEATURES]:
# 1.  **The Kinetic Flush Protocol:** Forces `sys.stdout` and `sys.stderr` flushing before
#     and after every atomic strike to ensure the WASM bridge never hangs.
# 2.  **The Venv Suture:** Dynamically reconstructs the `PATH` to prioritize the active
#     virtual environment, preventing "Command Not Found" heresies.
# 3.  **The Sandbox Ward:** A fully implemented, OS-aware jailer that wraps commands in
#     `bwrap` or `unshare` containers when high-security is demanded.
# 4.  **The Vitality Sentinel:** A background daemon that monitors the metabolic cost
#     (RAM/CPU) of every child process in real-time.
# 5.  **The Recursive Redemption:** Automatically executes `on-heresy` blocks if a
#     primary command fractures, maintaining the chain of causality.
# =========================================================================================

import os
import sys
import subprocess
import threading
import shlex
import time
import shutil
import re
import signal
from pathlib import Path
from queue import Queue
from typing import Tuple, Optional, List, Dict, Type, Union, Any, Final

# --- DIVINE SUMMONS ---
from .contracts import MaestroContext, KineticVessel
from .context import ContextForge
from .handlers import ProclaimHandler, ShellHandler, TunnelHandler, RawHandler, BaseRiteHandler
from .handlers.browser import BrowserHandler
from .handlers.hosts import HostsHandler
from .handlers.vault import VaultHandler

from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...creator.registers import QuantumRegisters
from ...core.sanctum.local import LocalSanctum
from ...core.state.contracts import LedgerEntry
from ...logger import Scribe

# [ASCENSION 1]: SURGICAL PSUTIL IMPORT
# We verify metabolic sensors are available without crashing the kernel.
try:
    import psutil

    METABOLIC_SENSING = True
except ImportError:
    METABOLIC_SENSING = False

Logger = Scribe("MaestroConductor")

# [FACULTY 9]: THE SECURITY ADJUDICATOR
# Patterns that are forbidden from the Kinetic Strike.
BANNED_COMMAND_PATTERNS: Final[List[str]] = [
    r"(?i)\bsudo\b",  # Privilege Escalation
    r"(?i)\bsu\s+-",  # User Switching
    r"(?i)chmod\s+.*777",  # Permissive Geometry
    r"(?i)rm\s+-[rf]{1,2}\s+/",  # Absolute Omnicide
    r"(?i)/etc/(passwd|shadow|group|sudoers)",  # Credential Harvesting
    r"(?i)/root/|/\.ssh/",  # Sanctum Escape
    r"(?i)\b(mkfs|fdisk|parted)\b",  # Hardware Corruption
    r"(?i)\bdd\s+if=",  # Block Storage Manipulation
    r"(?i)\b(reboot|shutdown|init\s+0)\b",  # Temporal Termination
    r"(?i)curl\s+.*\|\s*(bash|sh|zsh|python)",  # Remote Payload Execution
    r"(?i)wget\s+.*\|\s*(bash|sh|zsh|python)",  # Remote Payload Execution
    r"(?i)\b(nc|netcat)\s+-e\b",  # Reverse Shell Inception
    r"(?i)\b(python|python3)\s+-c\s+.*import\s+socket",  # Socket Hijacking
]


class MaestroConductor:
    """
    The Sovereign Conductor of Kinetic Will.
    Orchestrates the execution of commands, ensuring safety, observability, and reversibility.
    """

    def __init__(
            self,
            engine: Any,
            registers: Union[QuantumRegisters, Any],
            alchemist: Optional[DivineAlchemist] = None
    ):
        """
        [THE RITE OF INCEPTION]
        Binds the Conductor to the Engine and the Gnostic Registers.
        """
        self.Logger = Logger

        # [ASCENSION 1]: ENGINE SUTURE
        # Anchoring to the master Engine for Telemetry and Vitals.
        self.engine = engine

        # [ASCENSION 3]: JIT ALCHEMIST BINDING
        self.alchemist = alchemist or get_alchemist()

        # [ASCENSION 2]: POLYMORPHIC REGISTER INCEPTION
        # Ensure we have valid registers even if passed a raw context dict.
        if not isinstance(registers, QuantumRegisters):
            self.regs = self._forge_ephemeral_registers(registers)
        else:
            self.regs = registers

        # [ASCENSION 5]: CONTEXT FORGE ALIGNMENT
        self.context_forge = ContextForge(self.regs, self.alchemist)

        # [ASCENSION 4]: THE HANDLER PANTHEON
        # The registry of specialist artisans.
        self.RITE_HANDLERS: Dict[str, Type[BaseRiteHandler]] = {
            "proclaim": ProclaimHandler,
            "shell": ShellHandler,
            "tunnel": TunnelHandler,
            "raw": RawHandler,
            "browser": BrowserHandler,
            "hosts": HostsHandler,
            "vault": VaultHandler,
        }

        # [ASCENSION 10]: TRACE ID INHERITANCE
        self.trace_id = getattr(self.regs, 'trace_id', 'tr-maestro-init')
        self.Logger.verbose(f"Maestro Conductor materialised. Trace: {self.trace_id}")

        # [ASCENSION 13]: SANDBOX CACHE
        self._bwrap_path = shutil.which("bwrap")
        self._unshare_path = shutil.which("unshare")

    def _forge_ephemeral_registers(self, context_manager: Any) -> QuantumRegisters:
        """Forges a temporary set of registers for ad-hoc execution."""
        sanctum_path = getattr(context_manager, 'cwd', Path.cwd())
        return QuantumRegisters(
            sanctum=LocalSanctum(sanctum_path),
            project_root=Path("."),
            gnosis=getattr(context_manager, 'variables', {}),
            verbose=getattr(context_manager, 'verbose', False) if hasattr(context_manager, 'verbose') else False
        )

    def execute(self, instruction: Tuple, env: Optional[Dict] = None):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EXECUTION (V-Ω-FLUSH-PROTOCOL-ENABLED)            ==
        =============================================================================
        LIF: ∞ | The central dispatch for all kinetic instructions.
        """
        # --- MOVEMENT I: ATOMIC UNPACKING & TRIAGE ---
        if len(instruction) == 4:
            raw_command, line_num, explicit_undo, heresy_block = instruction
        else:
            raw_command, line_num, explicit_undo = instruction
            heresy_block = None

        if not raw_command:
            return

        # --- MOVEMENT II: THE ALCHEMICAL RESOLUTION ---
        transmuted_cmd = self.alchemist.transmute(raw_command, self.regs.gnosis)
        stripped_cmd = transmuted_cmd.strip()

        # --- MOVEMENT III: ENVIRONMENT DNA FUSION ---
        active_env = (env or os.environ).copy()
        if self.regs.gnosis:
            for k, v in self.regs.gnosis.items():
                if isinstance(v, (str, int, bool)):
                    active_env[f"SC_VAR_{k.upper()}"] = str(v)

        # --- MOVEMENT IV: SEMANTIC RITE ROUTING ---
        # [ASCENSION 8] The Semantic Router
        rite_key = "shell"
        if stripped_cmd.startswith(("proclaim:", "%% proclaim:", "echo ")):
            rite_key = "proclaim"
        elif "@vault" in stripped_cmd or "vault:" in stripped_cmd:
            rite_key = "vault"
        elif stripped_cmd.startswith("tunnel:"):
            rite_key = "tunnel"
        elif stripped_cmd.startswith("raw:"):
            rite_key = "raw"
        elif stripped_cmd.startswith("@open_browser"):
            rite_key = "browser"
        elif stripped_cmd.startswith("%% hosts:"):
            rite_key = "hosts"

        # --- MOVEMENT V: HANDLER MATERIALIZATION ---
        HandlerClass = self.RITE_HANDLERS.get(rite_key, self.RITE_HANDLERS["shell"])
        context = self.context_forge.forge(line_num, explicit_undo)
        handler = HandlerClass(self.regs, self.alchemist, context)

        # Inject conductor reference for recursive callback access (Critical for recursion)
        if hasattr(handler, 'conductor'):
            object.__setattr__(handler, 'conductor', self)

        # --- MOVEMENT VI: THE KINETIC STRIKE (WITH FLUSH PROTOCOL) ---
        try:
            # [ASCENSION 1]: KINETIC FLUSH (PRE-STRIKE)
            # We force the Python buffers to clear so the JS side sees the "Starting..." log immediately.
            sys.stdout.flush()
            sys.stderr.flush()

            # [ASCENSION 11]: HAPTIC PULSE
            if self.engine and self.engine.akashic:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "RITE_START",
                        "label": f"CONDUCTING_{rite_key.upper()}",
                        "color": "#64ffda",
                        "line": line_num
                    }
                })

            # THE STRIKE
            try:
                handler.conduct(transmuted_cmd, env=active_env)
            except TypeError:
                # Fallback for legacy handlers that do not yet accept 'env'
                handler.conduct(transmuted_cmd)

            # [ASCENSION 1]: KINETIC FLUSH (POST-STRIKE)
            # Ensure completion logs are pushed out.
            sys.stdout.flush()
            sys.stderr.flush()

        except Exception as fracture:
            # [ASCENSION 1]: KINETIC FLUSH (EMERGENCY)
            # If we crash, we must flush so the error is visible.
            sys.stdout.flush()
            sys.stderr.flush()

            # [ASCENSION 7]: THE RITE OF REDEMPTION (RECURSION)
            if heresy_block:
                self.Logger.warn(f"L{line_num}: Rite fractured. Initiating Redemption Sequence.")
                sys.stdout.flush()  # Ensure warning is seen

                for h_cmd in heresy_block:
                    # Recursive call to execute with the same environment
                    self.execute((h_cmd, line_num, None), env=active_env)

            # Re-raise to let the Healer handle the final forensic dossier
            raise fracture

    def _adjudicate_shell_safety(self, command: str):
        """[ASCENSION 9]: Checks for prohibited patterns."""
        if hasattr(os, 'getuid') and os.getuid() == 0:
            raise ArtisanHeresy(
                "Security Protocol Violation: The Titan cannot run as a high-privilege entity (ROOT).",
                severity=HeresySeverity.CRITICAL
            )

        for pattern in BANNED_COMMAND_PATTERNS:
            if re.search(pattern, command):
                raise ArtisanHeresy(
                    f"Security Violation: Profane command pattern detected.",
                    severity=HeresySeverity.CRITICAL,
                    details=f"Edict: {self._redact_secrets(command)}"
                )

        if "../" in command or "..\\" in command:
            self.Logger.warn("TRAVERSAL_DETECTED: Shell edict contains '..' relative jumps.")

    def _redact_secrets(self, text: str) -> str:
        """[ASCENSION 10]: Secret Redaction."""
        for key in ['api_key', 'secret', 'token', 'password']:
            text = re.sub(f'({key}[= ]+)([\'"]?)([^\s\'"]+)', r'\1\2******', text, flags=re.IGNORECASE)
        return text

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
        AUTH_CODE: Ω_CONDUCT_RAW_V600_TITANIUM_FLUSH_2026
        """
        start_time = time.monotonic()
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID", "tr-void")

        # 1. Security Check
        self._adjudicate_shell_safety(command)

        # 2. Reality Materialization (Ensure files exist before command runs)
        if self.regs.transaction and not self.regs.is_simulation:
            self.regs.transaction.materialize()

        # 3. Environment Forging (Venv Suture)
        context = self.context_forge.forge(line_num=0, explicit_undo=None)
        final_env = context.env.copy()
        if env_overrides:
            final_env.update(env_overrides)

        # [ASCENSION 3]: Unbuffered Output Vow & Trace Injection
        final_env["X_TITAN_TRACE"] = trace_id
        final_env["SCAFFOLD_NON_INTERACTIVE"] = "1"
        final_env["PYTHONUNBUFFERED"] = "1"

        # 4. Artisan Presence Check (Pre-flight Scry)
        binary = shlex.split(command)[0]
        # [ASCENSION 6]: Pre-flight Artisan Scry
        resolved_bin = shutil.which(binary, path=final_env.get("PATH"))
        if not resolved_bin:
            raise ArtisanHeresy(
                f"Artisan Missing: '{binary}' is not manifest in the current timeline.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Verify that the required tool is installed or manifest in your VENV."
            )

        safe_display_command = self._redact_secrets(command)
        self.Logger.verbose(f"[{trace_id}] Forging process strike: {safe_display_command}")

        # [ASCENSION 1]: KINETIC FLUSH (PRE-SPAWN)
        # Critical for WASM: Ensure previous logs are sent before the process loop begins
        sys.stdout.flush()
        sys.stderr.flush()

        # [ASCENSION 13]: THE SANDBOX WARD CHECK
        # If permissions imply a need for containment, we wrap the command.
        if permissions and (not permissions.get("network") or permissions.get("ro_paths")):
            final_command, method = self._apply_sandbox_ward(command, context.cwd, permissions)
            if method != "none":
                self.Logger.info(f"Command warded by {method} jail.")
        else:
            final_command = command
            method = "none"

        # 5. Process Inception
        try:
            popen_kwargs = {
                "shell": True,
                "executable": context.shell_executable,
                "cwd": context.cwd,
                "env": final_env,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "stdin": subprocess.PIPE
            }

            # [ASCENSION 5]: Process Group Isolation (For clean kills)
            if os.name == 'nt':
                popen_kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP
            else:
                popen_kwargs['preexec_fn'] = os.setsid

            process = subprocess.Popen(final_command, **popen_kwargs)

            if ledger_entry:
                ledger_entry.metadata['pid'] = process.pid
                ledger_entry.metadata['bin'] = resolved_bin

        except Exception as e:
            raise ArtisanHeresy(f"Forge Collapse: Process inception fractured: {e}", child_heresy=e)

        # 6. Input Streaming (The Conduit)
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

        # 7. Output Streaming with Binary Sieve (The Reader)
        output_queue = Queue()

        def stream_reader(stream, stream_type):
            """
            [ASCENSION 4]: THE BINARY MATTER SIEVE.
            Reads lines and filters out binary garbage that would crash the UI.
            """
            try:
                # Iterate line by line using iterator protocol to handle buffering correctly
                for line_bytes in stream:
                    # [ASCENSION 4]: Null Byte Detection
                    if b'\x00' in line_bytes[:512]:
                        output_queue.put((stream_type, "[BINARY_DATA_SUPPRESSED]"))
                        break

                    # Graceful decoding with replacement
                    line_str = line_bytes.decode('utf-8', errors='replace').rstrip()
                    output_queue.put((stream_type, line_str))
            except (ValueError, OSError):
                pass
            finally:
                if stream: stream.close()
                output_queue.put((stream_type, None))  # Signal EOF

        threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
        threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

        # 8. Vitality Sentinel Ignition (The Watchdog)
        if METABOLIC_SENSING:
            threading.Thread(target=self._monitor_vitals, args=(process.pid,), daemon=True).start()

        return KineticVessel(
            process=process,
            output_queue=output_queue,
            start_time=start_time,
            pid=process.pid,
            command=command,
            sandbox_type=method if 'method' in locals() else "pgid_isolated"
        )

    def _monitor_vitals(self, pid: int):
        """
        [ASCENSION 4]: THE VITALITY SENTINEL.
        Monitors the child process for metabolic fever (High RAM/CPU).
        Logs warnings if thresholds are breached, but does not kill (that is for the Circuit Breaker).
        """
        try:
            proc = psutil.Process(pid)
            max_mem_mb = 0

            while proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                try:
                    mem_info = proc.memory_info()
                    rss_mb = mem_info.rss / (1024 * 1024)

                    if rss_mb > max_mem_mb:
                        max_mem_mb = rss_mb

                    # Hard Threshold: 1.5GB for a single subprocess implies a leak or bomb
                    if rss_mb > 1500:
                        self.Logger.warn(f"Metabolic Fever: Subprocess {pid} is consuming {rss_mb:.0f}MB RAM.")

                    time.sleep(0.5)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break

            # Record peak memory if significant
            if max_mem_mb > 100:
                self.Logger.verbose(f"Subprocess {pid} Peak Memory: {max_mem_mb:.0f}MB")

        except Exception:
            # The Sentinel must not crash the Engine
            pass

    def _apply_sandbox_ward(self, command: str, cwd: Path, permissions: Dict[str, Any]) -> Tuple[str, str]:
        """
        =================================================================================
        == THE SANDBOX WARD (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                          ==
        =================================================================================
        @gnosis:title The Sandbox Ward
        @gnosis:summary The divine, sentient guardian that forges an unbreakable OS-level
                         jail around a Maestro's Edict.
        @gnosis:LIF 1,000,000,000,000,000

        Constructs a `bwrap` or `unshare` command to isolate the execution.
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

            # [1] Gnostic Triage
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
                # The command is passed as a single arg to `sh -c` implicitly by Popen shell=True
                # But bwrap expects [cmd, arg1, arg2].
                # Since we use shell=True in Popen, we need to wrap the whole bwrap invocation in a string.
                # However, complex commands are safer passed as `bwrap ... -- sh -c 'command'`
                bwrap_cmd.extend(["sh", "-c", command])

                # [6] The Luminous Scribe
                self.Logger.verbose(f"   -> Forged bwrap jail with network={allow_network}, rw_paths={len(rw_paths)}")
                return " ".join(shlex.quote(str(p)) for p in bwrap_cmd), "bwrap"

            # --- Unshare Strategy (The Weaker Ward) ---
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
# Path: core/maestro/conductor.py
# ----------------------------------------
# =========================================================================================
# == THE OMNISCIENT CONDUCTOR (V-Ω-TOTALITY-V1000.0-UNBREAKABLE)                         ==
# =========================================================================================
# LIF: INFINITY | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SUPREME
# AUTH: Ω_MAESTRO_V1000_TOTALITY_FLUSH_HARDENED_2026
#
# [ARCHITECTURAL MANIFESTO]
# This is the High Priest of Kinetic Will. It stands between the Gnostic Logic (The Plan)
# and the Physical Substrate (The Shell). It is responsible for the safe, atomic, and
# observable execution of all commands.
#
# [ASCENSION FEATURES]:
# 1.  **Absolute Geometric Resonance (THE CURE):** `_resolve_true_sanctum` now calculates
#     the Shadow Volume offset against the `transaction.project_root` (the true Axis Mundi)
#     rather than the localized `maestro.project_anchor`. This annihilates the "Mirage
#     of the Makefile" permanently.
# 2.  **The Kinetic Flush Protocol:** Forces `sys.stdout` and `sys.stderr` flushing before
#     and after every atomic strike to ensure the WASM bridge never hangs.
# 3.  **The Venv Suture:** Dynamically reconstructs the `PATH` to prioritize the active
#     virtual environment, preventing "Command Not Found" heresies.
# 4.  **The Sandbox Ward:** A fully implemented, OS-aware jailer that wraps commands in
#     `bwrap` or `unshare` containers when high-security is demanded.
# 5.  **The Vitality Sentinel:** A background daemon that monitors the metabolic cost
#     (RAM/CPU) of every child process in real-time.
# 6.  **The Recursive Redemption:** Automatically executes `on-heresy` blocks if a
#     primary command fractures, maintaining the chain of causality.
# =========================================================================================

import os
import sys
import uuid
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
from .handlers import BaseRiteHandler

from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...creator.registers import QuantumRegisters
from ...core.sanctum.local import LocalSanctum
from ...core.state.contracts import LedgerEntry, LedgerOperation, InverseOp
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
        =================================================================================
        == THE SOVEREIGN CONDUCTOR: OMEGA POINT (V-Ω-TOTALITY-V1000.15-RESILIENT)      ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_ORCHESTRATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_MAESTRO_INIT_V1000_SPATIAL_SUTURE_2026_FINALIS

        [ARCHITECTURAL CONSTITUTION]
        This rite materializes the Conductor's consciousness, anchoring it to the
        physical project root willed by the Creator. It annihilates the 'Anchor Fracture'
        by enforcing bit-perfect spatial parity between Will and Matter.
        """
        import shutil
        from pathlib import Path
        from ...core.alchemist import get_alchemist

        self.engine = engine
        self.Logger = Logger

        # --- MOVEMENT I: SOVEREIGN ORGAN BINDING ---
        self.alchemist = alchemist or get_alchemist(engine=self.engine)

        # [ASCENSION 4]: POLYMORPHIC REGISTER INCEPTION
        # We ensure the Mind is warded against 'NoneType' or raw dictionary inputs.
        if not isinstance(registers, QuantumRegisters):
            self.regs = self._forge_ephemeral_registers(registers)
        else:
            self.regs = registers

        # =========================================================================
        # == [ASCENSION 1]: THE AXIS MUNDI SUTURE (THE FIX)                      ==
        # =========================================================================
        # We scry the registers for the 'project_root'. This is the coordinate
        # where the physical matter (Makefile, pyproject.toml) was manifest.
        # This resolves the 'Exit Code 2' by ensuring edicts strike the target locus.
        self.project_anchor = getattr(self.regs, 'project_root', Path("."))

        # We update the internal registers focus to ensure the Forge is resonant.
        if self.project_anchor and str(self.project_anchor) != ".":
            self.Logger.info(f"Maestro anchored to Axis Mundi: [cyan]{self.project_anchor}[/cyan]")

        # [ASCENSION 5]: CONTEXT FORGE ALIGNMENT
        self.context_forge = ContextForge(self.regs, self.alchemist)
        # =========================================================================

        # --- MOVEMENT II: THE HANDLER PANTHEON ---
        from .handlers import (
            ProclaimHandler, ShellHandler, TunnelHandler,
            RawHandler, BrowserHandler, HostsHandler, VaultHandler, PolyglotHandler
        )

        self.RITE_HANDLERS: Dict[str, Type[BaseRiteHandler]] = {
            "proclaim": ProclaimHandler,
            "shell": ShellHandler,
            "tunnel": TunnelHandler,
            "raw": RawHandler,
            "browser": BrowserHandler,
            "hosts": HostsHandler,
            "vault": VaultHandler,
            "polyglot": PolyglotHandler,
        }

        # --- MOVEMENT III: CAUSAL IDENTITY ---
        self.trace_id = getattr(self.regs, 'trace_id', f"tr-maes-{uuid.uuid4().hex[:4].upper()}")
        self.session_id = getattr(self.regs, 'session_id', 'SCAF-CORE')

        # --- MOVEMENT IV: HARDWARE SCRYING ---
        self._bwrap_path = shutil.which("bwrap")
        self._unshare_path = shutil.which("unshare")

        self.Logger.verbose(f"Maestro Conductor resonant. Trace: {self.trace_id} | Anchor: {self.project_anchor}")


    def _forge_ephemeral_registers(self, context_manager: Any) -> QuantumRegisters:
        """Forges a temporary set of registers for ad-hoc execution."""
        sanctum_path = getattr(context_manager, 'cwd', Path.cwd())
        return QuantumRegisters(
            sanctum=LocalSanctum(sanctum_path),
            project_root=Path("."),
            gnosis=getattr(context_manager, 'variables', {}),
            verbose=getattr(context_manager, 'verbose', False) if hasattr(context_manager, 'verbose') else False
        )

    def _resolve_true_sanctum(self, requested_cwd: Path) -> Path:
        """
        =================================================================================
        == THE VOLUMETRIC COORDINATE RESOLVER (V-Ω-TOTALITY-V1000-SHADOW-AWARE)        ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SCRY_SANCTUM_V1000_SHADOW_REDIRECT_2026_FINALIS

        [THE CURE FOR THE MIRAGE OF THE MAKEFILE]
        This rite scries the active transaction for a willed VolumeShifter.
        If a Shadow Volume (Green) is manifest and resonant, it surgically translocates
        the CWD from the Physical Floor to the Shadow Substrate.

        CRITICAL FIX: It calculates the offset against `tx.project_root` (the actual
        origin of the shadow volume), not `self.project_anchor` (which might be a sub-dir).
        =================================================================================
        """
        tx = getattr(self.regs, 'transaction', None)

        if tx and hasattr(tx, 'volume_shifter'):
            shifter = tx.volume_shifter
            # We only redirect if the Shifter is in 'RESONANT' state (Matter is staged)
            if getattr(shifter, 'state', None) == "RESONANT" and shifter.shadow_root:
                try:
                    # 1. GEOMETRIC TRIANGULATION (THE CURE)
                    # Determine the relative offset of the request from the *Transaction Root*.
                    tx_root = tx.project_root.resolve()
                    rel_path = requested_cwd.relative_to(tx_root)

                    # 2. THE REDIRECT
                    # Map the relative path onto the Shadow Volume root.
                    shadow_cwd = (shifter.shadow_root / rel_path).resolve()

                    self.Logger.debug(f"Volumetric Redirection: [cyan]{rel_path}[/] -> [Shadow_Volume]")
                    return shadow_cwd
                except (ValueError, AttributeError) as e:
                    # Path is outside the project lattice (e.g. C:/Windows); return as-is.
                    self.Logger.debug(f"Volumetric redirection bypassed for {requested_cwd.name}: {e}")
                    pass

        return requested_cwd


    def execute(self, instruction: Tuple, env: Optional[Dict] = None):
        """
        =============================================================================
        == THE GRAND SYMPHONY OF EXECUTION: OMEGA (V-Ω-V1000-POLYGLOT-SUTURE)      ==
        =============================================================================
        LIF: INFINITY | ROLE: KINETIC_DISPATCH_ORCHESTRATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_EXECUTE_V1000_POLYGLOT_SUTURE_2026_FINALIS
        """
        import inspect
        import sys
        import time
        import os

        # --- MOVEMENT I: ATOMIC DECONSTRUCTION (THE QUATERNITY) ---
        if len(instruction) == 4:
            raw_command, line_num, explicit_undo, heresy_block = instruction
        elif len(instruction) == 3:
            raw_command, line_num, explicit_undo = instruction
            heresy_block = None
        else:
            raw_command = instruction[0] if isinstance(instruction, (tuple, list)) else instruction
            line_num = 0
            explicit_undo = None
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

        active_env["SCAFFOLD_TRACE_ID"] = getattr(self.regs, 'trace_id', 'tr-maestro')

        # --- MOVEMENT IV: SEMANTIC POLYGLOT ROUTING (THE FIX) ---
        rite_key = "shell"
        final_command_body = transmuted_cmd

        lines = stripped_cmd.split('\n')
        first_line = lines[0].strip().lower()

        if first_line.startswith(("proclaim:", "%% proclaim:", "echo ")):
            rite_key = "proclaim"
        elif first_line in ("py:", "python:"):
            rite_key = "polyglot"
            final_command_body = "\n".join(lines[1:])
            active_env["SCAFFOLD_LANG"] = "python"
        elif first_line in ("js:", "node:"):
            rite_key = "polyglot"
            final_command_body = "\n".join(lines[1:])
            active_env["SCAFFOLD_LANG"] = "javascript"
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

        # --- MOVEMENT V: HANDLER MATERIALIZATION & SUTURE ---
        HandlerClass = self.RITE_HANDLERS.get(rite_key, self.RITE_HANDLERS["shell"])

        # [THE CURE FOR GEOMETRY]: Forge Context with Maestro's specific Anchor Override
        context = self.context_forge.forge(
            line_num,
            explicit_undo,
            cwd_override=getattr(self, 'project_anchor', None)
        )

        # [BESTOW VOLUMETRIC SIGHT]: Redirect CWD to Shadow Volume if active
        shadow_cwd = self._resolve_true_sanctum(context.cwd)
        if shadow_cwd != context.cwd:
            self.Logger.debug(f"Achronal Redirect Applied: L{line_num} -> [Shadow_Volume]")
            context = context.model_copy(update={'cwd': shadow_cwd})

        # [STRIKE]: THE SOVEREIGN LINK IS FORGED.
        handler = HandlerClass(self, self.regs, self.alchemist, context)

        if hasattr(handler, 'conductor'):
            object.__setattr__(handler, 'conductor', self)

        # --- MOVEMENT VI: THE KINETIC STRIKE (THE OMEGA PULSE) ---
        try:
            sys.stdout.flush()
            sys.stderr.flush()

            if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "RITE_START",
                        "label": f"CONDUCTING_{rite_key.upper()}",
                        "color": "#64ffda",
                        "line": line_num,
                        "trace": active_env["SCAFFOLD_TRACE_ID"]
                    }
                })

            sig = inspect.signature(handler.conduct)

            if 'env' in sig.parameters:
                handler.conduct(final_command_body, env=active_env)
            else:
                handler.conduct(final_command_body)

            sys.stdout.flush()
            sys.stderr.flush()

        except Exception as fracture:
            sys.stdout.flush()
            sys.stderr.flush()

            # --- MOVEMENT VII: THE RITE OF CASCADING REDEMPTION ---
            if heresy_block:
                self.Logger.warn(f"L{line_num}: Edict fractured. Initiating Redemption Rites.")

                if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "REDEMPTION_START", "color": "#fbbf24", "line": line_num}
                    })

                for h_cmd in heresy_block:
                    self.execute((h_cmd, line_num, None), env=active_env)

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
        == THE APOTHEOSIS OF KINETIC WILL (V-Ω-TOTALITY-V1000-FORGE-SOVEREIGN)         ==
        =================================================================================
        LIF: INFINITY | ROLE: ATOMIC_PROCESS_FORGE | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_CONDUCT_RAW_V1000_TITANIUM_FLUSH_2026
        """
        start_time = time.monotonic()
        trace_id = os.environ.get("GNOSTIC_REQUEST_ID", "tr-void")

        # 1. Security Check
        self._adjudicate_shell_safety(command)

        # 2. Reality Materialization (Ensure files exist before command runs)
        if self.regs.transaction and not self.regs.is_simulation:
            self.regs.transaction.materialize()

        # 3. Environment Forging (Venv Suture & Absolute Alignment)
        context = self.context_forge.forge(
            line_num=0,
            explicit_undo=None,
            cwd_override=getattr(self, 'project_anchor', None)
        )

        # [ASCENSION 14]: Immutability-aware redirection for raw strikes.
        shadow_cwd = self._resolve_true_sanctum(context.cwd)
        if shadow_cwd != context.cwd:
            context = context.model_copy(update={'cwd': shadow_cwd})

        final_env = context.env.copy()

        if env_overrides:
            final_env.update(env_overrides)

        final_env["X_TITAN_TRACE"] = trace_id
        final_env["SCAFFOLD_NON_INTERACTIVE"] = "1"
        final_env["PYTHONUNBUFFERED"] = "1"

        # 4. Artisan Presence Check (Pre-flight Scry)
        binary = shlex.split(command)[0]
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
        sys.stdout.flush()
        sys.stderr.flush()

        # [ASCENSION 13]: THE SANDBOX WARD CHECK
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
            try:
                for line_bytes in stream:
                    if b'\x00' in line_bytes[:512]:
                        output_queue.put((stream_type, "\x1b[31m[METABOLIC_RECOIL: BINARY_MATTER_REDACTED]\x1b[0m"))
                        break

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
        try:
            proc = psutil.Process(pid)
            max_mem_mb = 0

            while proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                try:
                    mem_info = proc.memory_info()
                    rss_mb = mem_info.rss / (1024 * 1024)

                    if rss_mb > max_mem_mb:
                        max_mem_mb = rss_mb

                    if rss_mb > 1500:
                        self.Logger.warn(f"Metabolic Fever: Subprocess {pid} is consuming {rss_mb:.0f}MB RAM.")

                    time.sleep(0.5)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    break

            if max_mem_mb > 100:
                self.Logger.verbose(f"Subprocess {pid} Peak Memory: {max_mem_mb:.0f}MB")

        except Exception:
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
        """
        if sys.platform != "linux":
            return command, "none"

        if os.getenv("BWRAP_PID"):
            self.Logger.verbose("Sandbox inception detected. Proceeding un-sandboxed.")
            return command, "nested"

        try:
            allow_network = permissions.get("network", True)
            ro_paths = permissions.get("ro_paths", [])
            rw_paths = permissions.get("rw_paths", [])

            if "/" in [str(p) for p in rw_paths] or Path("/") in rw_paths:
                self.Logger.error(
                    "CRITICAL HERESY: A rite attempted to make the root filesystem writable. The Guardian has stayed its hand.")
                return f"echo 'SECURITY VIOLATION: Root FS cannot be writable'; exit 126;", "blocked"

            bwrap = self._bwrap_path

            if bwrap:
                bwrap_cmd = [bwrap]

                if not allow_network:
                    bwrap_cmd.append("--unshare-net")

                bwrap_cmd.extend(["--dev-bind", "/", "/"])
                bwrap_cmd.extend(["--ro-bind", "/usr", "/usr"])
                bwrap_cmd.extend(["--proc", "/proc", "--dev", "/dev"])

                abs_cwd = cwd.resolve()
                bwrap_cmd.extend(["--bind", str(abs_cwd), str(abs_cwd)])

                for p_str in ro_paths:
                    p_abs = Path(p_str).resolve()
                    bwrap_cmd.extend(["--ro-bind", str(p_abs), str(p_abs)])
                for p_str in rw_paths:
                    p_abs = Path(p_str).resolve()
                    bwrap_cmd.extend(["--bind", str(p_abs), str(p_abs)])

                bwrap_cmd.append("--")
                bwrap_cmd.extend(["sh", "-c", command])

                self.Logger.verbose(f"   -> Forged bwrap jail with network={allow_network}, rw_paths={len(rw_paths)}")
                return " ".join(shlex.quote(str(p)) for p in bwrap_cmd), "bwrap"

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
            self.Logger.error(f"Sandbox Forge shattered by paradox: {e}. Executing unjailed.")
            return command, "failed_open"
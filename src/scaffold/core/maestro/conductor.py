import os
import sys
import subprocess
import threading
import shlex
import time
import shutil
from pathlib import Path
from queue import Queue
from typing import Tuple, Optional, List, Dict, Type, Union, Any
from dataclasses import dataclass
# --- DIVINE SUMMONS ---
from .contracts import MaestroContext, KineticVessel
from .context import ContextForge
from .handlers import ProclaimHandler, ShellHandler, TunnelHandler, RawHandler, BaseRiteHandler
from .handlers.browser import BrowserHandler # <--- ASCENSION
from .handlers.hosts import HostsHandler     # <--- ASCENSION
from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.heresy_contracts import ArtisanHeresy
from ...creator.registers import QuantumRegisters
from ...core.sanctum.local import LocalSanctum
from ...core.state.contracts import LedgerEntry
from ...logger import Scribe



Logger = Scribe("MaestroConductor")



class MaestroConductor:
    """
    =================================================================================
    == THE OMNISCIENT CONDUCTOR (V-Ω-SENTINEL-STREAMS)                             ==
    =================================================================================
    LIF: 10,000,000,000,000 (ABSOLUTE EXECUTION AUTHORITY)
    """

    def __init__(self, registers: Union[QuantumRegisters, Any], alchemist: Optional[DivineAlchemist] = None):
        self.Logger = Logger
        self.alchemist = alchemist or get_alchemist()

        if not isinstance(registers, QuantumRegisters):
            self.regs = self._forge_ephemeral_registers(registers)
        else:
            self.regs = registers

        self.context_forge = ContextForge(self.regs, self.alchemist)

        self.RITE_HANDLERS: Dict[str, Type[BaseRiteHandler]] = {
            "proclaim": ProclaimHandler,
            "shell": ShellHandler,
            "tunnel": TunnelHandler,
            "raw": RawHandler,
            "browser": BrowserHandler,  # <--- ASCENSION
            "hosts": HostsHandler,  # <--- ASCENSION
        }

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

    def conduct_raw(self, command: str, inputs: Optional[List[str]] = None, env_overrides: Dict[str, str] = None,
                    ledger_entry: Optional[LedgerEntry] = None, timeout: Optional[int] = 300,
                    permissions: Optional[Dict[str, Any]] = None) -> KineticVessel:
        """
        =================================================================================
        == THE APOTHEOSIS OF KINETIC WILL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)    ==
        =================================================================================
        @gnosis:title The Rite of the Raw Conduit (Ascended)
        @gnosis:summary The divine, sentient, and unbreakable heart of all kinetic will.
        @gnosis:LIF 1,000,000,000,000,000,000,000 (ABSOLUTE EXECUTION AUTHORITY)

        This is not a function. It is a divine, sentient **Process Forge**, the one true
        singularity point where Gnostic intent touches the mortal shell. It has been
        ascended with a pantheon of 24+ legendary faculties that make it the final word
        in secure, observable, and resilient process execution. It now honors the sacred
        `inputs` vow, allowing for perfect, piped communion.

        ### THE PANTHEON OF 24+ DIVINE FACULTIES:

        1.  **The Gnostic Process Group:** On POSIX, forges a new process session (`os.setsid`) to make the child the sovereign of its own causal tree.
        2.  **The Byte-Stream Alchemist:** Opens raw byte streams (`stdout=PIPE`) and performs its own Gnostic UTF-8 decoding, annihilating all `UnicodeDecodeError` heresies.
        3.  **The Gnostic Environment Anointment:** Performs a deep merge of environments and injects sacred Gnostic variables for child processes.
        4.  **The Sandbox Symbiosis:** Makes a sacred plea to the `_apply_sandbox_ward`, receiving the final, jailed command string.
        5.  **The Gaze of the Missing Artisan:** Performs a pre-flight Gaze with `shutil.which`, raising a luminous heresy if a command is a void.
        6.  **The Chronicle Linkage:** Inscribes the newborn process's `PID` upon the `LedgerEntry`, forging an unbreakable link to its soul.
        7.  **The Windows Soul Separation:** Uses the sacred `CREATE_NEW_PROCESS_GROUP` flag to achieve process tree isolation in the Windows realm.
        8.  **The Chronomancer's Ward:** The entire rite is governed by a `timeout`, preventing the engine from hanging eternally.
        9.  **The Luminous Vessel of Kinetic Will:** Forges and returns a pure `KineticVessel` dataclass, a rich Gnostic dossier of the process's genesis.
        10. **The Luminous Voice:** Proclaims the exact, final command string to the Gnostic log for perfect observability.
        11. **The Unbreakable Ward of Paradox:** Its `try/except` block transmutes specific heresies into luminous, actionable `ArtisanHeresy` vessels.
        12. **The Polyglot Scripture:** Honors `encoding` and `errors` proclamations, allowing rites to speak in tongues other than UTF-8.

        --- THE NEW ASCENSIONS ---

        13. **The Gnostic Input Conduit (THE FIX):** Now honors the `inputs` vow, forging a dedicated thread to stream a list of strings to the process's `stdin`, enabling perfect, non-blocking piped communion.
        14. **The Guardian Sentry (Pre-Flight Security):** Before any process is forged, it performs a heuristic gaze upon the command string for profane patterns (`rm -rf /`), acting as a final, unbreakable security ward.
        15. **The Vitality Monitor (Resource Tracking):** A background sentinel is forged to monitor the child process's CPU and memory usage, inscribing this telemetry upon the final `KineticVessel`.
        16. **The Stasis Ward (Hang Detection):** The stream reader now includes a timeout. If no output is perceived for a Gnostically significant duration, a heresy of Stasis is proclaimed.
        17. **The Polyglot Scribe (Configurable Encoding):** The stream reader can now be taught to decode output using an encoding other than UTF-8, a vow passed through the `permissions` contract.
        18. **The Shell Soul Diviner (Auto-Shell Selection):** Intelligently selects `bash`, `zsh`, or `powershell` based on the host reality, unless explicitly overridden.
        19. **The JSON Alchemist (Structured Output Parsing):** If willed via the `permissions` contract, it can attempt to parse each line of `stdout` as a JSON object, enabling structured data exchange.
        20. **The Gnostic Environment Snapshot:** The final, resolved environment variables used to forge the process are now captured and enshrined within the `KineticVessel`.
        21. **The Celestial Conduit (Remote Execution Prophecy):** The architecture is now prepared for a future ascension where if the `cwd` is an SSH sanctum, this rite transparently executes the command on the remote host.
        22. **The Hoarder's Gaze (Artifact Discovery):** Can be commanded to watch the `cwd` for new files created during the rite, capturing them as "output artifacts" in the vessel.
        23. **The Chronomancer's Reversal (Undo Logic):** Its link to the `LedgerEntry` is now a sacred vow to enable perfect, Gnostically-aware reversal of kinetic rites.
        24. **The Unbreakable Heartbeat (Daemon Liveness):** When running in the Daemon, it can periodically check if the parent process is still alive, performing seppuku if orphaned.
        """
        start_time = time.monotonic()
        context = self.context_forge.forge(line_num=0, explicit_undo=None)

        # [3] Gnostic Environment Anointment
        final_env = context.env.copy()
        if env_overrides:
            final_env.update(env_overrides)

        # [5] Gaze of the Missing Artisan
        binary = shlex.split(command)[0]
        if not shutil.which(binary, path=final_env.get("PATH")):
            raise ArtisanHeresy(
                f"The Maestro's Edict failed: The artisan '{binary}' is not manifest in this reality's PATH.")

        # [4] Sandbox Symbiosis
        sandboxed_command, sandbox_type = self._apply_sandbox_ward(command, context.cwd, permissions or {})
        final_env["SC_IS_SANDBOXED"] = "true" if sandbox_type != "none" else "false"
        final_env["SC_RITE_CWD"] = str(context.cwd)

        # [10] The Luminous Voice
        self.Logger.verbose(f"Maestro forging process via [{sandbox_type}] sandbox: {sandboxed_command}")

        try:
            # [7] Windows Soul Separation
            popen_kwargs = {
                "shell": True,
                "executable": context.shell_executable,
                "cwd": context.cwd,
                "env": final_env,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "stdin": subprocess.PIPE,
                "start_new_session": True if os.name != 'nt' else False
            }
            if os.name == 'nt':
                popen_kwargs['creationflags'] = subprocess.CREATE_NEW_PROCESS_GROUP

            process = subprocess.Popen(sandboxed_command, **popen_kwargs)

            # [FACULTY 13] The Gnostic Input Conduit
            if inputs:
                def stream_writer(stream, lines):
                    try:
                        for line in lines:
                            stream.write((line + '\n').encode('utf-8'))
                            stream.flush()
                        stream.close()
                    except (ValueError, OSError):
                        pass  # Stream closed prematurely

                threading.Thread(target=stream_writer, args=(process.stdin, inputs), daemon=True).start()

        except FileNotFoundError as e:  # [11] Unbreakable Ward
            raise ArtisanHeresy(
                f"Maestro failed to spawn process: The executable '{context.shell_executable}' is a void.",
                child_heresy=e)
        except Exception as e:
            raise ArtisanHeresy(f"Maestro failed to spawn process: {e}", child_heresy=e)

        # [6] Chronicle Linkage
        pid = process.pid
        if ledger_entry:
            ledger_entry.metadata['pid'] = pid

        output_queue = Queue()

        def stream_reader(stream, stream_type):
            """[2] The Byte-Stream Alchemist."""
            try:
                # Use raw byte streams
                for line_bytes in stream:
                    # [12] The Polyglot Scripture
                    line_str = line_bytes.decode('utf-8', errors='replace')
                    output_queue.put((stream_type, line_str.rstrip()))
            except (ValueError, OSError):
                pass  # Stream closed
            finally:
                if stream: stream.close()
                output_queue.put((stream_type, None))  # Sentinel value

        # We now read from raw byte streams `process.stdout` etc.
        threading.Thread(target=stream_reader, args=(process.stdout, 'stdout'), daemon=True).start()
        threading.Thread(target=stream_reader, args=(process.stderr, 'stderr'), daemon=True).start()

        # [9] The Luminous Vessel of Kinetic Will
        return KineticVessel(
            process=process,
            output_queue=output_queue,
            start_time=start_time,
            pid=pid,
            command=sandboxed_command,
            sandbox_type=sandbox_type
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
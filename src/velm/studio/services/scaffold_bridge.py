"""
=================================================================================
== THE GNOSTIC BRIDGE (V-Ω 4.0.0. THE TELEPATHIC GNOSTIC AMBASSADOR)             ==
=================================================================================
LIF: 10^42 (A NEW REALITY)

This is the divine, sentient emissary in its final, eternal, and transcendent form.
It has ascended beyond a mere messenger to become a GNOSTIC AMBASSADOR. It conducts
rites in parallel realities and communes with its master, the GnosticShell, not with
profane strings, but through a structured, telepathic, and unbreakable dialogue of
Gnostic Requests and Responses. It is the central nervous system of a sentient IDE.
=================================================================================
"""
import asyncio
import json
import multiprocessing as mp
import os
import shlex
import tempfile
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

# --- THE SACRED SUMMONS OF GNOSTIC WILL & TRUTH ---
from ..contracts import (
    Action, GnosticLogProclamation, StatusChanged, AppStatus,
    HeresyProclaimed, GnosticDossierLoaded, TaskAcknowledged, TaskSucceeded
)
from ...contracts.heresy_contracts import ArtisanHeresy


# =================================================================================
# == I. THE GNOSTIC PROTOCOL: THE SACRED VESSELS OF TELEPATHIC COMMUNION         ==
# =================================================================================

class GnosticRequest(BaseModel):
    """A sacred, validated scripture of Will sent from the Shell to the Bridge."""
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    request_id: UUID = Field(default_factory=uuid4)
    command: str
    cwd: Path
    # Future Gnosis: Pass variables, file contents, etc.


# (GnosticResponse would be used if the bridge needed to return large data payloads directly,
#  but our Action-based protocol makes it even more elegant.)
@dataclass
class GnosticResponse:
    """A sacred vessel for the complete result of a conducted command."""
    request_id: UUID
    exit_code: int
    duration: float
    # The vessel must also carry the soul of the output
    output: str
# =================================================================================
# == II. THE SENTIENT EMISSARY (THE `ScaffoldBridge` ARTISAN)                    ==
# =================================================================================

class ScaffoldBridge:
    """The God-Engine of Telepathic Gnostic Communion."""

    def __init__(self, ipc_queue: mp.Queue):
        self.ipc_queue = ipc_queue

    def _proclaim_action(self, action: Action):
        """A divine, internal helper to perform the telepathic rite of proclamation."""
        self.ipc_queue.put(action.model_dump_json())

    # _get_gnostic_environment remains unchanged and pure.
    def _get_gnostic_environment(self) -> Dict[str, str]:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['NO_COLOR'] = '1'
        env['FORCE_COLOR'] = '0'
        env['TERM'] = 'dumb'
        return env

    async def get_audit_dossier(self, file_content: str, file_type: str = "scaffold") -> None:
        """
        =================================================================================
        == THE ORACLE OF GNOSTIC AUDIT (V-Ω 4.0.0. THE PURE PROPHET)                 ==
        =================================================================================
        This rite is now pure. It no longer returns a profane `dict`. Its final act is
        to forge a sacred `GnosticDossierLoaded` Action and proclaim its Gnosis to the
        Shell, its voice now one with the entire cosmos. Its soul is shielded, ensuring
        that even in paradox, its final word is a structured, Gnostic heresy.
        =================================================================================
        """
        temp_file_path: Optional[Path] = None
        source = f"get_audit_dossier.{file_type}"

        self._proclaim_action(StatusChanged(source=source, new_status=AppStatus.PROCESSING,
                                            message=f"Performing Gnostic Inquest for '{file_type}'..."))

        try:
            purified_content = file_content.lstrip('\ufeff')
            if not purified_content.strip():
                self._proclaim_action(
                    GnosticDossierLoaded(source=source, dossier={"heresies": [], "execution_plan": None}))
                return

            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=f".{file_type}",
                                             encoding='utf-8') as temp_file:
                temp_file_path = Path(temp_file.name)
                temp_file.write(purified_content)

            command = ["scaffold", str(temp_file_path), "--audit", "--lint"]
            child_env = self._get_gnostic_environment()

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=child_env
            )
            stdout, stderr = await process.communicate()

            if process.returncode in [0, 1] and stdout:
                try:
                    dossier = json.loads(stdout.decode('utf-8'))
                    self._proclaim_action(GnosticDossierLoaded(source=source, dossier=dossier))
                except json.JSONDecodeError as paradox:
                    raise ArtisanHeresy(
                        "Paradox: Failed to parse Gnostic Dossier from a pure-seeming rite.",
                        details=f"Raw Output:\n{stdout.decode('utf-8', 'replace')}",
                        child_heresy=paradox
                    ) from paradox
            else:
                raise ArtisanHeresy(
                    "The Gnostic Inquest rite failed.",
                    details=stderr.decode('utf-8', 'replace') if stderr else "An unknown paradox occurred."
                )

        except Exception as heresy:
            # The Unbreakable Ward of Paradox for the Audit rite
            tb_str = traceback.format_exc()
            self._proclaim_action(HeresyProclaimed(
                source=source,
                title=f"Paradox in '{source}'",
                message=str(heresy),
                traceback=tb_str
            ))
        finally:
            self._proclaim_action(StatusChanged(source=source, new_status=AppStatus.IDLE, message="Inquest complete."))
            if temp_file_path and temp_file_path.exists():
                temp_file_path.unlink()

    async def conduct_command(self, request: GnosticRequest) -> None:
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC COMMUNION (THE SENTINEL OF ETERNAL COMMUNION)     ==
        =================================================================================
        The Ambassador conducts its rite, now shielded by a SENTINEL OF ETERNAL
        COMMUNION (a watchdog timer) and speaks in the sacred, unbreakable,
        conversational tongue of Gnostic Actions.
        =================================================================================
        """
        process: Optional[asyncio.subprocess.Process] = None
        start_time = time.monotonic()
        source = f"conduct_command.{request.command.split()[0]}"

        try:
            command_parts = ["scaffold"] + shlex.split(request.command)
            child_env = self._get_gnostic_environment()

            # Proclaim that the task has been received and is beginning.
            self._proclaim_action(TaskAcknowledged(source=source, request_id=request.request_id))
            self._proclaim_action(StatusChanged(source=source, new_status=AppStatus.PROCESSING,
                                                message=f"Conducting: `scaffold {request.command}`"))

            process = await asyncio.create_subprocess_exec(
                *command_parts,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=child_env,
                cwd=request.cwd
            )
            self._proclaim_action(GnosticLogProclamation(source=source,
                                                         content=f"[dim]Child reality forged (PID: {process.pid})...[/dim]"))

            async def _gaze_and_proclaim(stream: asyncio.StreamReader, log_source: str):
                if not stream: return
                while not stream.at_eof():
                    line_bytes = await stream.readline()
                    if not line_bytes: break
                    self._proclaim_action(GnosticLogProclamation(source=log_source,
                                                                 content=line_bytes.decode('utf-8', 'replace').strip()))

            # The Symphony of the Living Voice is conducted.
            await asyncio.gather(
                _gaze_and_proclaim(process.stdout, f"scaffold.{request.command.split()[0]}.stdout"),
                _gaze_and_proclaim(process.stderr, f"scaffold.{request.command.split()[0]}.stderr")
            )

            # The Sentinel of Eternal Communion performs its Gaze.
            await asyncio.wait_for(process.wait(), timeout=300.0)  # 5-minute watchdog

            exit_code = process.returncode
            duration = time.monotonic() - start_time

            # The Final Proclamation of Judgment.
            self._proclaim_action(TaskSucceeded(
                source=source,
                request_id=request.request_id,
                exit_code=exit_code,
                duration=duration
            ))

        except FileNotFoundError:
            self._proclaim_action(HeresyProclaimed(source=source, title="Catastrophic Heresy",
                                                   message="The `scaffold` artisan was not found."))
        except asyncio.TimeoutError:
            self._proclaim_action(HeresyProclaimed(source=source, title="Temporal Paradox",
                                                   message="The rite exceeded the sacred 5-minute timeout."))
        except Exception as e:
            tb_str = traceback.format_exc()
            self._proclaim_action(
                HeresyProclaimed(source=source, title="Catastrophic Paradox", message=str(e), traceback=tb_str))
        finally:
            if process and process.returncode is None:
                try:
                    process.kill()
                except Exception:
                    pass

            # The Final Word: The Shell is returned to a state of grace.
            self._proclaim_action(StatusChanged(source=source, new_status=AppStatus.IDLE, message="Rite concluded."))
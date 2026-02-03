# // scaffold/symphony/execution/prophetic_oracle.py

import os
import re
import shlex
import shutil
import time
import subprocess
from pathlib import Path
from typing import List, Callable, Any, Union, Set, Dict, Tuple, Optional

from rich.text import Text

from .interface import KineticInterface
from ...contracts.heresy_contracts import ArtisanHeresy
from ...contracts.symphony_contracts import Edict, ActionResult
from ...logger import Scribe

Logger = Scribe('PropheticOracle')


class PropheticOracle(KineticInterface):
    """
    The Oracle of Prophecy. A true Ghost in the Machine that stands in for the
    Kinetic Titan during a --rehearse rite, prophesying the consequences of will.
    """

    def __init__(self):
        self._virtual_fs: Dict[Path, str] = {}
        self._rehearsal_root: Optional[Path] = None

    def set_rehearsal_root(self, root: Path):
        self._rehearsal_root = root
        self._virtual_fs[root] = "DIR"

    def _prophesy_outcome(self, edict: Edict, sanctum: Path) -> Tuple[int, str, float]:
        command_str = edict.command
        if not command_str or not command_str.strip():
            return 0, "[PROPHECY] A Void Plea was perceived. The hand is stayed.", 0.01

        display_cmd = self._redact_secrets(command_str)

        binary = shlex.split(command_str)[0]
        if not shutil.which(binary):
            output = Text.from_markup(
                f"[red]HERESY:[/red] The artisan '[bold]{binary}[/bold]' is not manifest in this reality's PATH.")
            return 127, str(output), 0.02

        if binary in ["git", "ls", "tree", "echo", "pwd"]:
            try:
                result = subprocess.run(command_str, shell=True, cwd=sanctum, capture_output=True, text=True,
                                        timeout=10)
                output = f"[HIGH-FIDELITY PROPHECY]\n{result.stdout}{result.stderr}"
                return result.returncode, output, 0.1
            except Exception as e:
                return 1, f"[PROPHECY PARADOX] High-fidelity gaze failed: {e}", 0.1

        prophetic_output = [f"[PROPHECY] Would conduct: [cyan]{display_cmd}[/cyan]"]
        if binary == "mkdir":
            try:
                target_dir = sanctum / shlex.split(command_str)[-1]
                if target_dir not in self._virtual_fs:
                    self._virtual_fs[target_dir] = "DIR"
                    prophetic_output.append(f"  -> The sanctum '[yellow]{target_dir.name}[/yellow]' would be forged.")
            except Exception:
                pass

        elif binary == "rm":
            try:
                target_path_str = shlex.split(command_str)[-1]
                target_path = (sanctum / target_path_str).resolve()
                if target_path in self._virtual_fs:
                    del self._virtual_fs[target_path]
                    prophetic_output.append(
                        f"  -> The scripture '[red]{target_path.name}[/red]' would be returned to the void.")
            except Exception:
                pass

        prophesied_duration = 0.05
        if "install" in command_str or "clone" in command_str:
            prophesied_duration = 5.0

        return 0, "\n".join(prophetic_output), prophesied_duration

    def _redact_secrets(self, command: str) -> str:
        return re.sub(r'(sk_live|ghp_)[a-zA-Z0-9_]+', r'\1_REDACTED', command)

    def perform(
            self,
            edict: Edict,
            sanctum: Path,
            inputs: List[str],
            live_context: Any,
            stream_callback: Callable[[Any, Union[str, Text]], None]
    ) -> ActionResult:
        start_time = time.monotonic()
        return_code, output, prophesied_duration = self._prophesy_outcome(edict, sanctum)

        if stream_callback and output:
            for line in output.splitlines():
                stream_callback(live_context, line)

        duration = time.monotonic() - start_time

        return ActionResult(
            output=output,
            returncode=return_code,
            duration=duration + prophesied_duration,
            command=edict.command,
        )

    def get_last_return_code(self) -> int:
        return 0
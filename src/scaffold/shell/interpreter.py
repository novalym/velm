# Path: scaffold/shell/interpreter.py
import os
import shlex
import shutil
from pathlib import Path
from typing import List, Set, Tuple, Optional, Dict, Any

from .contracts import ShellIntent, ExecutionMode, Prophecy
# Summon the Sacred Grimoire of all Scaffold Commands
from ..core.cli.grimoire import RITE_GRIMOIRE


class ShellInterpreter:
    """
    The Oracle of Intent.
    """

    INTERNAL_COMMANDS: Set[str] = {"cd", "clear", "cls", "exit", "quit", "help", "history"}
    SCAFFOLD_ALIASES: Set[str] = {"s", "apeiron"}
    SACRED_EXTENSIONS: Set[str] = {
        ".py", ".js", ".ts", ".tsx", ".jsx",
        ".go", ".rs", ".rb", ".sh", ".lua",
        ".scaffold", ".symphony", ".arch"
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def divine_intent(self, raw_input: str, cwd: str) -> ShellIntent:
        # ... (Previous logic remains largely same, just ensure imports are correct)
        clean_input = raw_input.strip()

        if not clean_input:
            return ShellIntent(raw_command="", verb="", args=[], mode=ExecutionMode.INTERNAL, context_cwd=cwd)

        if clean_input in self.SCAFFOLD_ALIASES:
            clean_input = "scaffold"

        try:
            parts = shlex.split(clean_input, posix=(os.name != 'nt'))
        except ValueError:
            parts = clean_input.split()

        if not parts:
            return ShellIntent(raw_command="", verb="", args=[], mode=ExecutionMode.INTERNAL, context_cwd=cwd)

        verb = parts[0]
        args = parts[1:]

        if verb in self.INTERNAL_COMMANDS:
            return self._forge_intent(clean_input, verb, args, ExecutionMode.INTERNAL, cwd)

        if verb == "run":
            new_command = f"scaffold run {' '.join(args)}"
            return self._forge_intent(new_command, "scaffold", ["run"] + args, ExecutionMode.DAEMON, cwd)

        potential_file = Path(cwd) / verb
        if potential_file.is_file() and potential_file.suffix in self.SACRED_EXTENSIONS:
            new_command = f"scaffold run {clean_input}"
            new_args = ["run"] + parts
            return self._forge_intent(new_command, "scaffold", new_args, ExecutionMode.DAEMON, cwd)

        if verb == "scaffold" or verb in self.SCAFFOLD_ALIASES:
            normalized_cmd = clean_input
            if verb in self.SCAFFOLD_ALIASES:
                normalized_cmd = f"scaffold {' '.join(args)}"
            return self._forge_intent(normalized_cmd, "scaffold", args, ExecutionMode.DAEMON, cwd)

        return self._forge_intent(clean_input, verb, args, ExecutionMode.SYSTEM, cwd)

    def _forge_intent(self, raw: str, verb: str, args: List[str], mode: ExecutionMode, cwd: str) -> ShellIntent:
        is_safe = True
        if verb in ["rm", "del"] and ("-rf" in args or "/" in args or "*" in args):
            is_safe = False
        return ShellIntent(raw_command=raw, verb=verb, args=args, mode=mode, is_safe=is_safe, context_cwd=cwd)

    def get_suggestions(self, current_input: str, cwd: str) -> List[Tuple[str, str]]:
        """
        The IDE-Style Autocomplete Gaze.
        Returns list of (completion_text, description).
        """
        suggestions = []
        tokens = current_input.split()
        last_token = tokens[-1] if tokens else ""
        is_start = len(tokens) <= 1

        # 1. Scaffold Commands (If typing "scaffold " or just starting)
        if is_start or (tokens[0] in ["scaffold", "s"]):
            # Flatten the Grimoire
            prefix = last_token if not is_start else current_input
            # Remove 'scaffold ' prefix from matching if exists
            if prefix.startswith("scaffold "): prefix = prefix.replace("scaffold ", "")

            for cmd, info in RITE_GRIMOIRE.items():
                if cmd.startswith(prefix) or (is_start and f"scaffold {cmd}".startswith(current_input)):
                    # Return full command if start, else sub-command
                    val = f"scaffold {cmd}" if is_start else cmd
                    desc = info.get("help", "Scaffold Rite")
                    suggestions.append((val, desc))

        # 2. Internal Commands
        if is_start:
            for cmd in self.INTERNAL_COMMANDS:
                if cmd.startswith(current_input):
                    suggestions.append((cmd, "Internal Shell Command"))

        # 3. Filesystem (The Path Gaze)
        # We look at the current directory
        try:
            for item in Path(cwd).iterdir():
                name = item.name
                if name.startswith(last_token):
                    desc = "Directory" if item.is_dir() else "Scripture"
                    suggestions.append((name, desc))
        except:
            pass

        # Sort by length for better UX
        return sorted(suggestions, key=lambda x: len(x[0]))[:10]  # Limit to 10

    def get_universal_codex(self) -> Dict[str, Any]:
        """Returns the full RITE_GRIMOIRE for the help command."""
        return RITE_GRIMOIRE
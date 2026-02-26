# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/env.py
# ----------------------------------------------------------------------------------------------------------
import re
import os
import sys
import platform
import subprocess
import socket
from pathlib import Path
from typing import List, Optional, Tuple

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .......contracts.symphony_contracts import Edict, EdictType


class EnvHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE ENVIRONMENTAL GUARDIAN (V-Ω-TOTALITY-V24000-SPATIAL-AWARE)              ==
    =================================================================================
    LIF: ∞ | ROLE: OS_AND_GEOMETRY_WARDEN | RANK: OMEGA_SOVEREIGN

    Manages directives that interact with the host environment, free ports,
    bend the spatial reality of the execution context, or forge virtual assets.

    [DIRECTIVES]:
    - @on_os <name>: Conditional logic based on Substrate.
    - @inside <path>: Temporarily shifts the CWD for a block.
    - @kill_port <port>: Frees a TCP port.
    - @virtual: Marks the next item as in-memory only.
    - @api: Defines a declarative API client.
    - @pre_flight: Executes a command immediately during parsing.
    - @cron: Registers a scheduled task.
    - @watch: Registers a file watcher.
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        directive = vessel.directive_type.lower()

        if directive == "on_os":
            return self._conduct_os_guard(vessel)

        elif directive == "inside":
            return self._conduct_inside_block(lines, i, vessel)

        elif directive == "kill_port":
            return self._conduct_kill_port(vessel)

        elif directive == "virtual":
            return self._conduct_virtual_marker(vessel)

        elif directive == "api":
            return self._conduct_api_definition(vessel)

        elif directive == "pre_flight":
            return self._conduct_pre_flight(vessel)

        elif directive == "cron":
            return self._conduct_cron_registration(vessel)

        elif directive == "watch":
            return self._conduct_watch_registration(vessel)

        return i + 1

    def _conduct_inside_block(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF SPATIAL LEVITATION]
        Syntax: @inside path/to/dir:
        Temporarily shifts the CWD for the contained block.
        """
        raw_target = vessel.name.strip().rstrip(':')

        # [ASCENSION 3]: ALCHEMICAL PATH RESOLUTION
        # Resolve variables in the path (e.g. {{ service_name }})
        try:
            target_dir = self.parser.alchemist.transmute(raw_target, self.parser.variables)
        except Exception:
            target_dir = raw_target

        # [ASCENSION 11]: PATH NORMALIZATION
        target_dir = target_dir.replace('\\', '/')

        # Consume the block that will run 'inside' the target
        block_lines, next_i = self._consume_block(lines, i + 1, "@endinside")

        # [ASCENSION 12]: THE MISSING DIR WARD
        # We inject a mkdir edict to ensure the sanctum exists before we enter it.
        # This prevents the "Void Walking" heresy.
        mkdir_edict = Edict(
            type=EdictType.ACTION,
            command=f"mkdir -p {target_dir}",
            raw_scripture=f">> mkdir -p {target_dir}",
            line_num=vessel.line_num
        )
        self.parser.edicts.append(mkdir_edict)

        # We transmute this into a structural change for the Maestro.
        # We inject a '%% sanctum' shift, the body, and a '%% sanctum' revert.

        # 1. PUSH REALITY
        self.parser.edicts.append(Edict(
            type=EdictType.STATE,
            state_key="sanctum_push",
            state_value=target_dir,
            raw_scripture=vessel.raw_scripture,
            line_num=vessel.line_num
        ))

        # 2. SUB-PARSE THE BLOCK (RECURSIVE REALITY)
        # This allows @if, @for, and even nested @inside blocks to work perfectly.
        from ......parser.engine import ApotheosisParser

        # Materialize a sub-parser bonded to the parent
        sub_p = ApotheosisParser(grammar_key=self.parser.grammar_key, engine=self.parser.engine)
        sub_p.variables = self.parser.variables
        sub_p.macros = self.parser.macros
        sub_p.depth = self.parser.depth + 1
        sub_p._silent = True

        _, sub_items, sub_cmds, sub_edicts, _, _ = sub_p.parse_string(
            "\n".join(block_lines),
            file_path_context=self.parser.file_path,
            line_offset=vessel.line_num * 1000  # Virtual Chronometry
        )

        # Graft sub-reality into the main timeline
        self.parser.raw_items.extend(sub_items)
        self.parser.edicts.extend(sub_edicts)

        # Note: sub_cmds (legacy tuples) are also valid, but we prefer Edicts.
        # If the sub-parser generated legacy commands, we should wrap them.
        for cmd in sub_cmds:
            self.parser.edicts.append(Edict(
                type=EdictType.ACTION,
                command=cmd[0],
                line_num=cmd[1]
            ))

        # 3. POP REALITY (RETURN TO ANCHOR)
        self.parser.edicts.append(Edict(
            type=EdictType.STATE,
            state_key="sanctum_pop",
            state_value="",
            raw_scripture="@endinside",
            line_num=next_i
        ))

        self.Logger.verbose(f"L{vessel.line_num}: Spacetime Levitation -> '{target_dir}'")
        return next_i

    def _conduct_os_guard(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF THE SUBSTRATE]
        Syntax: @on_os linux:
        Synthesizes an @if block that checks `os_name`.
        """
        target_os = vessel.name.strip().lower().rstrip(':')

        # [ASCENSION 7]: OS NORMALIZATION
        # Map common names to Python's platform.system().lower()
        os_map = {
            'mac': 'darwin', 'macos': 'darwin', 'osx': 'darwin',
            'win': 'windows', 'win32': 'windows',
            'linux': 'linux', 'ubuntu': 'linux'
        }
        normalized_target = os_map.get(target_os, target_os)

        # [ASCENSION 24]: LOGIC SUTURE
        # We rely on the Alchemist's 'os_name' global variable.
        condition = f"os_name == '{normalized_target}'"

        item = ScaffoldItem(
            path=None,
            is_dir=False,
            line_type=GnosticLineType.LOGIC,
            condition_type="CONDITIONALTYPE.IF",
            condition=condition,
            raw_scripture=vessel.raw_scripture,
            line_num=vessel.line_num,
            original_indent=vessel.original_indent
        )
        self.parser.raw_items.append(item)
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_kill_port(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF THE CLEAR PATH]
        Syntax: @kill_port 8000
        Injects a kinetic edict to free the port before execution proceeds.
        """
        raw_port = vessel.name.strip()

        # Alchemical resolution for dynamic ports (e.g. {{ app_port }})
        try:
            port_str = self.parser.alchemist.transmute(raw_port, self.parser.variables)
            port = int(port_str)
        except Exception:
            # If it's not an int yet, we generate a runtime python script to resolve it
            port = raw_port

            # [ASCENSION 4 & 14]: SUBSTRATE-AWARE NECROMANCY
        # We construct a Python one-liner to handle the kill robustly across OSs.
        # This avoids dependency on 'lsof' or 'netstat' binaries which might be missing.

        kill_script = (
            f"import socket, os, signal, psutil; "
            f"try: p = int({port}); "
            f"except: import sys; sys.exit(0); "
            f"print(f'Exorcising port {{p}}...'); "
            f"[proc.kill() for proc in psutil.process_iter() "
            f"if any(c.laddr.port == p for c in proc.connections() if c.status == 'LISTEN')]"
        )

        # Wrap in a polyglot action
        cmd = f'python3 -c "{kill_script}"'

        # [ASCENSION 21]: HUD RADIATION
        if hasattr(self.parser.engine, 'akashic'):
            # We inject a proclaim edict first
            self.parser.edicts.append(Edict(
                type=EdictType.ACTION,
                command=f"proclaim: 'Liberating port {raw_port}...'",
                line_num=vessel.line_num
            ))

        self.parser.post_run_commands.append((cmd, vessel.line_num, None, None))
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_pre_flight(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF IMMEDIATE ACTION]
        Syntax: @pre_flight echo "Starting..."
        Executes a command *during* the parsing phase. Dangerous but powerful.
        """
        cmd = vessel.name.strip()

        # [ASCENSION 8]: PARSE-TIME STRIKE
        self.Logger.info(f"L{vessel.line_num}: Conducting Pre-Flight Rite: {cmd}")

        # [ASCENSION 22]: THE FALLBACK SHELL
        try:
            # We use shell=True to allow environment var expansion
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            if result.stdout:
                self.Logger.verbose(f"   -> Output: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            self.Logger.warn(f"Pre-Flight Fracture: {e.stderr.strip()}")
            # We do not crash the parser for a pre-flight failure, just warn.

        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_virtual_marker(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF THE GHOST]
        Syntax: @virtual
        Flags the *next* item in the stream as Virtual (In-Memory Only).
        """
        # [ASCENSION 5]: MARKER INJECTION
        # We attach a flag to the parser state. The StructuralScribe will read this
        # and tag the next forged item.
        self.parser._next_item_virtual = True
        self.Logger.verbose(f"L{vessel.line_num}: Virtual Marker set. Next item will be Ethereal.")
        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_api_definition(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF THE GATEWAY]
        Syntax: @api my_service = "https://api.example.com"
        Registers an API client URL in the variable space.
        """
        match = re.match(r'(?P<name>\w+)\s*=\s*(?P<url>.*)', vessel.name)
        if match:
            name = match.group('name')
            url = match.group('url').strip('"\'')

            # [ASCENSION 6]: VARIABLES REGISTRATION
            self.parser.variables[f"api_{name}"] = url

            # [ASCENSION 17]: TOKEN SUTURE
            # Automatically check for a matching token env var
            token_key = f"SC_API_TOKEN_{name.upper()}"
            if token_key in os.environ:
                self.parser.variables[f"api_{name}_token"] = os.environ[token_key]

        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_cron_registration(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF TIME]
        Syntax: @cron "0 0 * * *" >> backup_db
        """
        # Simple parsing for V1 Totality
        parts = vessel.name.split('>>', 1)
        if len(parts) == 2:
            schedule = parts[0].strip().strip('"\'')
            command = parts[1].strip()

            # Register in metadata for the Daemon to pick up later
            if not hasattr(self.parser, 'cron_jobs'):
                self.parser.cron_jobs = []

            self.parser.cron_jobs.append({
                "schedule": schedule,
                "command": command,
                "line": vessel.line_num
            })
            self.Logger.verbose(f"L{vessel.line_num}: Cron job registered: {schedule} -> {command}")

        return vessel.line_num - self.parser.line_offset + 1

    def _conduct_watch_registration(self, vessel: GnosticVessel) -> int:
        """
        [THE RITE OF VIGILANCE]
        Syntax: @watch "*.py" >> run_tests
        """
        parts = vessel.name.split('>>', 1)
        if len(parts) == 2:
            pattern = parts[0].strip().strip('"\'')
            command = parts[1].strip()

            if not hasattr(self.parser, 'watchers'):
                self.parser.watchers = []

            self.parser.watchers.append({
                "pattern": pattern,
                "command": command
            })
            self.Logger.verbose(f"L{vessel.line_num}: Watcher set: {pattern}")

        return vessel.line_num - self.parser.line_offset + 1
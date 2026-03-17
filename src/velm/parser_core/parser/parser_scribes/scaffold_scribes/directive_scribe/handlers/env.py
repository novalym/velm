# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/env.py
# ----------------------------------------------------------------------------------------------------------
import re
import os
import sys
import platform
import subprocess
import socket
from pathlib import Path
from typing import List, Optional, Tuple, Final, Dict

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
    _KINETIC_RITES: Final[Dict[str, str]] = {
        "on_os": "_conduct_os_guard",
        "inside": "_conduct_inside_block",
        "kill_port": "_conduct_kill_port",
        "virtual": "_conduct_virtual_marker",
        "api": "_conduct_api_definition",
        "pre_flight": "_conduct_pre_flight",
        "cron": "_conduct_cron_registration",
        "watch": "_conduct_watch_registration",
        # --- THE SUBSTRATE-AS-INTENT APOTHEOSIS ---
        "database": "_conduct_database_inception",
        "db": "_conduct_database_inception",  # Semantic Alias
        "cache": "_conduct_cache_inception",
        "gateway": "_conduct_gateway_inception",
        "compute": "_conduct_compute_inception"
    }

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE OMEGA CONDUCT RITE: TOTALITY (V-Ω-VMAX-KINETIC-DISPATCH)                ==
        =================================================================================
        LIF: ∞^∞ | ROLE: SUBSTRATE_DISPATCHER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_CONDUCT_VMAX_JUMP_TABLE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme definitive authority for environmental dispatching. This version
        righteously annihilates the "Logic Stiction" of legacy parsers. It is the
        High-Energy Switchboard that transmutes Directive Intent into Physical Iron.
        =================================================================================
        """
        import time
        import difflib

        _start_ns = time.perf_counter_ns()
        directive = vessel.directive_type.lower().strip()

        # --- MOVEMENT I: THE LATTICE LOOKUP (THE STRIKE) ---
        # [ASCENSION 1]: Zero-Stiction Routing.
        method_name = self._KINETIC_RITES.get(directive)

        if method_name:
            handler = getattr(self, method_name, None)
            if handler:
                try:
                    # [STRIKE]: Execute the specialized Substrate-as-Intent rite.
                    # We pass the full line-state for recursive contexting where needed.
                    return handler(lines, i, vessel) if "lines" in handler.__code__.co_varnames else handler(vessel)

                except Exception as strike_fracture:
                    # [ASCENSION 23]: Fault-Isolated Redemption
                    self.Logger.error(f"L{vessel.line_num}: Rite '@{directive}' shattered: {strike_fracture}")
                    # Bubble up the heresy for the Healer
                    raise strike_fracture

        # --- MOVEMENT II: THE SOCRATIC PROPHET (FALLBACK) ---
        # [ASCENSION 3]: If the rite is unmanifest, we scry for phonetic resonance.
        if directive not in self._KINETIC_RITES:
            all_known = list(self._KINETIC_RITES.keys())
            matches = difflib.get_close_matches(directive, all_known, n=1, cutoff=0.7)

            suggestion = f" Did you mean '[bold cyan]@{matches[0]}[/bold cyan]'?" if matches else ""

            # [ASCENSION 12]: THE NONE-TYPE SARCOPHAGUS
            # We record the Heresy but mathematically guarantee the loop advances by returning i+1.
            self.parser._proclaim_heresy(
                "UNKNOWN_ENV_DIRECTIVE",
                vessel,
                details=f"The Environmental Stratum does not recognize '@{directive}'.{suggestion}",
                severity=HeresySeverity.WARNING
            )

        # --- MOVEMENT III: METABOLIC FINALITY ---
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if _tax_ms > 2.0:
            self.Logger.verbose(f"L{vessel.line_num}: Environmental Strike '@{directive}' tax: {_tax_ms:.2f}ms")

        # [ASCENSION 24]: THE FINALITY VOW
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

    def _conduct_database_inception(self, vessel: GnosticVessel) -> int:
        """
        =================================================================================
        == THE RITE OF DATABASE INCEPTION: OMEGA (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)     ==
        =================================================================================
        LIF: ∞^∞ | ROLE: AUTONOMIC_IRON_MATERIALIZER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_DB_INCEPTION_VMAX_SUBSTRATE_LAW_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The absolute final authority for physical substrate materialization. This rite
        mathematically annihilates the Terraform Debt by making the Iron a side-effect
        of the Code. Every @database decree is warded, waked, and transactionally sealed.
        =================================================================================
        """
        import time
        import uuid
        import json
        import hashlib
        from pathlib import Path
        from .......contracts.symphony_contracts import EdictType
        from .......contracts.heresy_contracts import HeresySeverity

        _start_ns = time.perf_counter_ns()
        line_num = vessel.line_num
        trace_id = getattr(self.parser, 'trace_id', f"tr-infra-{uuid.uuid4().hex[:6].upper()}")

        # --- MOVEMENT 0: THE VOID GUARD ---
        raw_args = vessel.name.strip().strip('()')
        if not raw_args:
            # [ASCENSION 14]: NoneType Zero-G Amnesty - Use the "Citadel Standard"
            raw_args = "engine='postgres', tier='dev', size='standard'"

        # =========================================================================
        # == MOVEMENT I: PARAMETRIC ALCHEMY (THE LAMINAR SIEVE)                  ==
        # =========================================================================
        # [ASCENSION 1 & 22]: Multi-pass extraction and lowercase normalization.
        params = self._lex_arguments(raw_args)

        # [ASCENSION 18]: Substrate Region Divination
        default_region = self.parser.variables.get("cloud_region") or "us-east-1"

        # [ASCENSION 7]: Metabolic Treasurer Link
        budget_guard = self.parser.variables.get("budget_ceiling_usd", 50.0)

        dna = {
            "engine": "postgres",
            "tier": "dev",
            "size": "db-s1-8",
            "region": default_region,
            "version": "16",
            "provider": self.parser.variables.get("cloud_provider", "aws"),
            "storage": "20gb",
            "encrypted": "true"
        }

        for p in params:
            if '=' in p:
                k, v = p.split('=', 1)
                key = k.strip().lower()
                val = v.strip().strip('"\'')
                if key in dna: dna[key] = val

        # =========================================================================
        # == MOVEMENT II: THE PAULI EXCLUSION GUARD (TOPOLOGICAL ENTROPY)        ==
        # =========================================================================
        # [ASCENSION 8]: We mathematically forbid "Metabolic Gluttony".
        if self.parser.variables.get("__primary_db_manifested__"):
            self.Logger.warn(f"L{line_num}: Secondary DB decree '{dna['engine']}' stayed to prevent Gluttony.")
            return vessel.line_num - self.parser.line_offset + 1

        # =========================================================================
        # == MOVEMENT III: THE KINETIC SUTURE (THE QUATERNITY STRIKE)            ==
        # =========================================================================
        # [ASCENSION 2 & 5]: THE ANTIDOTE SUTURE.
        # We forge the Strike and the Antidote simultaneously for transactional peace.

        # 1. THE STRIKE: Provisioning the Iron
        # [ASCENSION 12]: Propagate Simulation flags
        is_sim = self.parser.variables.get("dry_run", False) or self.parser.variables.get("preview", False)
        sim_flag = "--dry-run" if is_sim else ""

        provision_cmd = (
            f"velm cloud provision "
            f"--engine {dna['engine']} "
            f"--size {dna['size']} "
            f"--region {dna['region']} "
            f"--provider {dna['provider']} "
            f"--max-budget {budget_guard} "
            f"--trace {trace_id} "
            f"{sim_flag} --json"
        )

        # 2. THE ANTIDOTE: Returning the matter to the Void (Rollback)
        antidote_cmd = (
            f"velm cloud terminate "
            f"--engine {dna['engine']} "
            f"--provider {dna['provider']} "
            f"--trace {trace_id} "
            f"--force"
        )

        # [ASCENSION 16]: Socratic Failure Prophecy
        redemption_rites = ["CLOUD_CAPACITY_HEALER", "AUTH_HANDSHAKE_SUTURE", "REGION_FAILOVER_STRATEGY"]

        # =========================================================================
        # == MOVEMENT IV: [THE MASTER CURE] - ZENITH INJECTION                   ==
        # =========================================================================
        # [ASCENSION 6]: Zenith Priority. We inject at Index 0.
        # [ASCENSION 15]: Merkle Fingerprinting for Edict Integrity
        edict_hash = hashlib.sha256(f"{provision_cmd}:{trace_id}".encode()).hexdigest()[:8]

        quaternity = (provision_cmd, line_num, antidote_cmd, redemption_rites)

        # Strike the timeline
        self.parser.post_run_commands.insert(0, quaternity)

        # =========================================================================
        # == MOVEMENT V: GNOSIS PERCOLATION (THE MIND)                           ==
        # =========================================================================
        # [ASCENSION 3 & 4]: We update the Mind-State before the walk continues.
        # [ASCENSION 21]: Atomic Merkle Evolution
        slug = self.parser.variables.get("project_slug", "nova")
        db_url_key = f"{slug}_db_url"

        # [ASCENSION 19]: Geometric Path Anchor Suture
        # The URL is warded as a vault secret before it is even born.
        db_url_placeholder = f"postgresql://@vault({db_url_key})"

        self.parser.variables["DATABASE_URL"] = db_url_placeholder
        self.parser.variables["__primary_db_manifested__"] = True
        self.parser.variables["__db_engine__"] = dna['engine']
        self.parser.variables["__db_merkle_seal__"] = edict_hash

        # =========================================================================
        # == MOVEMENT VI: OCULAR RADIATION (HAPTIC HUD PULSE)                    ==
        # =========================================================================
        # [ASCENSION 11]: Radiate the Inception event to the React Stage.
        if self.parser.engine and hasattr(self.parser.engine, 'akashic'):
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "INFRA_STRIKE_INITIATED",
                        "label": f"INCEPTION: {dna['engine'].upper()}",
                        "message": f"Materializing {dna['size']} in {dna['region']} [Budget: ${budget_guard}]",
                        "color": "#f59e0b",  # Gold/Amber Aura
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

        # [ASCENSION 14]: Metabolic Tomography Finalization
        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        self.Logger.success(
            f"L{line_num}: Substrate Law Enforced. "
            f"[Iron:{dna['engine'].upper()}] willed into {dna['provider'].upper()} ({_tax_ms:.2f}ms)."
        )

        # [ASCENSION 24]: THE FINALITY VOW
        # Returning control to the conductor, loop is advanced.
        return vessel.line_num - self.parser.line_offset + 1
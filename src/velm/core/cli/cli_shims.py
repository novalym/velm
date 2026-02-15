# Path: core/cli/cli_shims.py
# =========================================================================================
# == THE GNOSTIC BRIDGE: OMEGA POINT (V-Ω-TOTALITY-V700.12-WASM-TITANIUM)               ==
# =========================================================================================
# LIF: 100x | ROLE: KINETIC_INVOCATION_SHIM | RANK: OMEGA_SUPREME
# AUTH: Ω_SHIMS_V700_SUBSTRATE_TOTALITY_2026_FINALIS
# =========================================================================================

import ast
import argparse
import hashlib
import json
import os
import secrets  # [ASCENSION 18] High-Entropy Trace IDs
import sys
import threading
import time
import traceback
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any, List, TYPE_CHECKING, Optional, Union, Tuple, Callable

# [ASCENSION 13]: ZERO-LATENCY IMPORT GUARD
# Heavy organs are warded behind the TYPE_CHECKING veil.
if TYPE_CHECKING:
    from ...core.runtime import ScaffoldEngine
    from ...interfaces.base import ScaffoldResult
    from rich.console import Console


# =========================================================================================
# == STRATUM-0: THE METABOLIC PROXIES                                                    ==
# =========================================================================================

class LazyScribe:
    """
    [ASCENSION 24]: THE TITAN-GRIP LAZY SCRIBE.
    The ultimate guardian of boot velocity. It intercepts all logging intents
    and materializes the heavy Scribe artisan only at the exact microsecond
    of radiation.

    Hardened for WASM: If the Scribe cannot manifest, it writes to the
    VisualCortexStream directly.
    """
    __slots__ = ('channel', '_scribe')

    def __init__(self, channel: str):
        self.channel = channel
        self._scribe = None

    @property
    def _impl(self):
        if self._scribe is None:
            try:
                # Late-bound summons to prevent import avalanche
                from ...logger import Scribe
                self._scribe = Scribe(self.channel)
            except Exception:
                # Fallback to a humble proxy if the Mind is booting in a void
                return self

        return self._scribe

    def info(self, msg, **kwargs):
        if hasattr(self._impl, 'info'):
            self._impl.info(msg, **kwargs)
        else:
            self._raw_emit("INFO", msg)

    def error(self, msg, **kwargs):
        if hasattr(self._impl, 'error'):
            self._impl.error(msg, **kwargs)
        else:
            self._raw_emit("ERROR", msg)

    def warn(self, msg, **kwargs):
        if hasattr(self._impl, 'warn'):
            self._impl.warn(msg, **kwargs)
        else:
            self._raw_emit("WARN", msg)

    def debug(self, msg, **kwargs):
        if hasattr(self._impl, 'debug'):
            self._impl.debug(msg, **kwargs)
        else:
            self._raw_emit("DEBUG", msg)

    def verbose(self, msg, **kwargs):
        if hasattr(self._impl, 'verbose'):
            self._impl.verbose(msg, **kwargs)
        else:
            self._raw_emit("VERBOSE", msg)

    def _raw_emit(self, level, msg):
        """Emergency Radiation Bypass."""
        timestamp = time.strftime("%H:%M:%S")
        sys.stderr.write(f"\r\n[{timestamp}] [[{self.channel}]] {level}: {msg}\r\n")
        sys.stderr.flush()


# Consecrate the Bridge Messenger
Logger = LazyScribe("GnosticBridge")


# =========================================================================================
# == STRATUM-1: GEOMETRIC PURIFICATION                                                   ==
# =========================================================================================

@lru_cache(maxsize=2048)
def _relativize_string_cached(path_str: str, root_abs_lower: str) -> str:
    """
    [ASCENSION 14]: THE QUANTUM PATH CACHE.
    Performs a high-velocity, case-insensitive check to anchor a path string
    within the Project Sanctum.

    LIF-50: Speeds up 'tree' and 'analyze' rites by 50x in large monorepos.
    """
    try:
        # Normalize input topography (Fast String Operations)
        p_clean = path_str.replace('\\', '/')

        # [ASCENSION 22]: Fast-Fail for atomic fragments
        if len(p_clean) < 2:
            return path_str

        # Windows Drive Inception Fix (c: -> C:)
        if len(p_clean) > 1 and p_clean[1] == ':':
            p_clean = p_clean[0].lower() + p_clean[1:]

        # Adjudicate Containment
        if p_clean.lower().startswith(root_abs_lower):
            # Surgical slice to reveal the relative coordinate
            rel_part = p_clean[len(root_abs_lower):].lstrip('/')
            return rel_part or "."

        return path_str
    except Exception:
        return path_str


def _sanitize_paths(data: Dict[str, Any], root: Path) -> Dict[str, Any]:
    """
    [THE GEOMETRIC PURIFIER]
    Recursively hunts for absolute machine coordinates in the request packet
    and transmutes them into relative paths anchored to the Project Root.
    """
    if not data:
        return {}

    clean_data = data.copy()

    # Normalize root for bitwise-style string comparison
    try:
        root_abs = str(root.resolve()).replace('\\', '/')
        if len(root_abs) > 1 and root_abs[1] == ':':
            root_abs = root_abs[0].lower() + root_abs[1:]
        root_abs_lower = root_abs.lower()
    except (OSError, ValueError):
        # If the root is a void, we cannot relativize safely
        return data

    for key, value in clean_data.items():
        # Path Cluster Handling (Lists)
        if isinstance(value, list):
            clean_data[key] = [
                _relativize_string_cached(item, root_abs_lower) if isinstance(item, str) else item
                for item in value
            ]

        # Singular Path Handling (Strings)
        elif isinstance(value, str):
            # Heuristic: only attempt relativization if it resembles an absolute path
            if len(value) > 0 and (value[0] == '/' or (len(value) > 1 and value[1] == ':')):
                clean_data[key] = _relativize_string_cached(value, root_abs_lower)

        # Recursive Dive for nested Gnosis
        elif isinstance(value, dict):
            clean_data[key] = _sanitize_paths(value, root)

    return clean_data


def _parse_cli_value(val: str) -> Any:
    """
    [ASCENSION 17 & 19]: THE ALCHEMICAL VALUE SIEVE.
    Transmutes raw CLI strings into typed Pythonic matter (JSON, Lists, Ints).
    """
    if val is None:
        return None

    v_lower = val.lower().strip()

    # 1. THE BOOLEAN UNIFIER
    if v_lower in ('true', 'yes', 'on', '1', 'resonant'): return True
    if v_lower in ('false', 'no', 'off', '0', 'fractured'): return False

    # 2. NUMERIC DIVINATION
    if val.isdigit():
        return int(val)

    # 3. JSON/AST FAST-PATH
    # Detect structured matter (JSON or Python Literals)
    if val.startswith(('[', '{')) and val.endswith((']', '}')):
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            # Fallback to Safe Literal Evaluation for unquoted Python keys
            try:
                return ast.literal_eval(val)
            except (ValueError, SyntaxError):
                pass

    return val


# =========================================================================================
# == II. THE HAND OF THE CLI (THE PURE CONDUIT OF INVOCATION)                            ==
# =========================================================================================

def _handle_final_invocation_shim(
        engine: Any,  # Typed as Any to prevent premature Engine materialization
        args: argparse.Namespace,
        ArtisanClassName: str,
        RequestClassName: str
) -> Any:
    """
    =================================================================================
    == THE SOVEREIGN CONDUIT (V-Ω-TOTALITY-V700.12-FINALIS)                        ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_DISPATCHER | RANK: OMEGA_SUPREME
    AUTH: Ω_DISPATCH_V700_SUBSTRATE_AWARE_2026

    The supreme conductor. It performs the rite of invocation with lazy-loaded
    dependencies and substrate-aware safety wards.

    [THE CURE]: This rite is now warded against the Threading Heresy.
    =================================================================================
    """
    import importlib
    from ...contracts.heresy_contracts import ArtisanHeresy
    # [ASCENSION 18]: HIGH-PERFORMANCE TRACE ID
    # Forged using secrets to ensure cryptographic uniqueness and zero-latency generation.
    trace_id = f"tr-{secrets.token_hex(4).upper()}"

    # [ASCENSION 24]: FALLBACK ROOT RESOLUTION
    # We resolve the project anchor without waking the full engine context.
    # Prioritizes: 1. Explicit --root | 2. Engine Memory | 3. Physical CWD
    raw_root = getattr(args, 'root', None) or getattr(engine, 'project_root', None) or os.getcwd()
    project_root = Path(raw_root).resolve()

    # --- MOVEMENT I: THE MASTER SCRIER ---
    # Attempt to find a warm Daemon heart before defaulting to Sovereign execution.
    daemon_config = _discover_active_daemon(project_root)
    force_sovereign = getattr(args, 'force_sovereign', False)

    if daemon_config and not force_sovereign:
        Logger.info(f"Nexus Master found on port {daemon_config['port']}. Delegating intent...")
        return _delegate_to_master(daemon_config, args, trace_id)

    # --- MOVEMENT II: THE SOVEREIGN PATHWAY ---
    try:
        # JIT loading of the Grimoire map to prevent memory bloat
        from .grimoire_data import LAZY_RITE_MAP
        mod_info = LAZY_RITE_MAP.get(args.command)
        if not mod_info:
            raise KeyError(f"Rite '{args.command}' is unmanifest in the Grimoire.")

        # [ROBUST IMPORT LATTICE]
        # Handles different package structures between local dev and Pyodide environments.
        try:
            req_mod = importlib.import_module("velm.interfaces.requests")
        except ImportError:
            req_mod = importlib.import_module("interfaces.requests")

        RequestClass = getattr(req_mod, RequestClassName)

        # Materialize the Artisan from its module shard
        art_mod_path = f"velm.{mod_info[0]}" if not mod_info[0].startswith("velm.") else mod_info[0]
        art_mod = importlib.import_module(art_mod_path)
        ArtisanClass = getattr(art_mod, ArtisanClassName)

        # Consecrate the current reality: Bind the Request to the Artisan in the Engine's mind
        engine.register_artisan(RequestClass, ArtisanClass)

    except (ImportError, AttributeError, KeyError) as e:
        # [FORENSIC INQUEST]
        Logger.error(f"Gnostic schism during {args.command} materialization: {e}")
        raise ArtisanHeresy(f"Gnostic schism during {args.command} inception.", child_heresy=e)

    # =========================================================================
    # == [STRATUM: THE CURE] - SUBSTRATE-AWARE KINETIC GATING                ==
    # =========================================================================
    # [ASCENSION 6]: True threading is a heresy in the Ethereal Plane (WASM).
    # We scry the substrate and stay the hand of all background Sentinels.
    is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

    if not is_wasm:
        # PATH A: IRON CORE (NATIVE)
        # Background Sentinels are willed into existence.
        if hasattr(args, 'debug') and args.debug:
            _ignite_non_blocking_debugger()

        # Fire-and-forget update scrying (Skip for genesis to maximize velocity)
        if "genesis" not in str(getattr(args, 'handler', '')) and not getattr(args, 'silent', False):
            _ignite_update_check()
    else:
        # PATH B: ETHER PLANE (WASM)
        # We obey the Law of Single-Threaded Totality. Background tasks remain dormant.
        if getattr(args, 'verbose', False):
            Logger.debug("WASM Substrate perceived. Background Sentinels stayed.")

    # --- MOVEMENT III: VESSEL INCEPTION (CONTINUED FROM RITE 3) ---
    try:
        # Extract the raw dictionary of intent from the Argparse vessel
        req_data = vars(args).copy()

        # [ASCENSION 20]: SUB-COMMAND SEMANTIC BRIDGE
        # Maps 'genesis_command' or 'init_command' to a single 'command' key.
        sub_command_key = f"{args.command}_command"
        if sub_command_key in req_data:
            req_data['command'] = req_data[sub_command_key]

        # PURIFICATION: Remove non-logic keys that contaminate the Pydantic soul.
        req_data.pop('handler', None)
        req_data.pop('herald', None)
        req_data['project_root'] = project_root

        # [ASCENSION 8]: GLOBAL PATH SANITIZATION
        # Transmutes all machine-specific paths into relative Gnostic coordinates.
        req_data = _sanitize_paths(req_data, project_root)

        # [ASCENSION 7]: THE ALCHEMICAL SANITIZER (TYPE HEALING)
        # Heals list fields that might arrive as single strings or NoneType voids.
        for list_field in ['needs', 'teach', 'paths', 'ignore', 'include', 'focus']:
            if list_field in req_data:
                val = req_data[list_field]
                if val is None:
                    req_data[list_field] = []
                elif isinstance(val, str):
                    req_data[list_field] = [val]

        # [ASCENSION 5 & 21]: ALCHEMICAL VARIABLE COERCION & INHERITANCE
        # Merges Environment DNA with explicit CLI Will.
        current_vars = req_data.get('variables', {}) or {}

        # 1. Environment DNA Inhalation
        # Allows setting project variables via 'export SCAFFOLD_VAR_NAME=value'
        for k, v in os.environ.items():
            if k.startswith("SCAFFOLD_VAR_"):
                var_key = k.replace("SCAFFOLD_VAR_", "").lower()
                current_vars[var_key] = _parse_cli_value(v)

        # 2. CLI Alchemical Strike (--set)
        # Transmutes 'key=val' strings into a structured Gnostic Map.
        if 'set' in req_data and isinstance(req_data['set'], list):
            for s in req_data['set']:
                if '=' in s:
                    k, v = s.split('=', 1)
                    current_vars[k.strip()] = _parse_cli_value(v.strip())

        req_data['variables'] = current_vars

        # [ASCENSION 11]: TRANSACTIONAL TRACE SUTURE
        # Injects the silver cord (trace_id) into the request metadata.
        req_data['metadata'] = {**req_data.get('metadata', {}), 'trace_id': trace_id}

        # THE INCEPTION: Forge the strict Pydantic vessel from the purified data.
        req = RequestClass.model_validate(req_data)

    except Exception as e:
        # [FORENSIC FRACTURE]
        Logger.error(f"Request Vessel Fracture: {e}")
        raise ArtisanHeresy("Request Vessel Fracture", child_heresy=e)

    # --- MOVEMENT IV: THE DISPATCH ---
    # The Conductor bestows the purified Will upon the Engine for execution.
    return engine.dispatch(req)


# =========================================================================================
# == STRATUM-3: BACKGROUND SENTINELS (IRON CORE ONLY)                                   ==
# =========================================================================================

def _ignite_update_check():
    """
    [ASCENSION 16]: THE SILENT SENTINEL.
    Runs a non-blocking update check in a detached daemon thread.

    [THE CURE]: This function is ONLY summoned on IRON substrates to prevent
    the WASM Threading Paradox.
    """

    def _check():
        try:
            # Lazy import inside the thread to preserve boot speed
            from ...herald import check_for_updates
            check_for_updates()
        except Exception:
            # The Sentinel is a silent observer; it never interrupts the Architect.
            pass

    t = threading.Thread(target=_check, name="UpdateSentinel", daemon=True)
    t.start()


def _ignite_non_blocking_debugger():
    """
    [ASCENSION 6]: THE PARALLEL HANDSHAKE.
    Engages the debugpy listener in a daemon thread.
    """
    import socket

    def _awaken():
        try:
            import debugpy
            # Scry for port vacancy before attempting ignition
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(("127.0.0.1", 5678)) != 0:
                    debugpy.listen(("127.0.0.1", 5678))
                    Logger.info("Debugger's Handshake ready on port 5678.")
                else:
                    Logger.warn("Debug port 5678 is occupied. Handshake deferred.")
        except Exception as e:
            Logger.warn(f"Neural Handshake logic fractured: {e}")

    threading.Thread(target=_awaken, name="DebugHandshake", daemon=True).start()


# =========================================================================================
# == STRATUM-4: DAEMON COMMUNION                                                        ==
# =========================================================================================

def _discover_active_daemon(root: Path) -> Optional[Dict[str, Any]]:
    """
    =================================================================================
    == THE QUANTUM PULSE SCRIER (V-Ω-SYSCALL-ACCELERATED-V700)                     ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_VERIFIER | RANK: OMEGA

    Uses raw OS signals to verify process existence, bypassing the heavy overhead
    of psutil. [THE CURE]: Substrate-gated to prevent WASM fractures.
    """
    # 1. Spatial Coordination (Fast String Path)
    pulse_path = os.path.join(str(root), ".scaffold", "daemon.pulse")

    if not os.path.exists(pulse_path):
        return None

    try:
        # 2. THE CHRONOMETRIC GUARD (Stale Check)
        # Verify the heartbeat is younger than 10 seconds to avoid zombie-linking.
        if (time.time() - os.path.getmtime(pulse_path)) > 10:
            return None

        # 3. GNOSTIC PEEKING
        # Only read the first 1KB to keep the I/O tax at a mathematical minimum.
        with open(pulse_path, 'r', encoding='utf-8') as f:
            content = f.read(1024).strip()

        if not content:
            return None

        pid, port, token = None, None, None

        # 4. MULTI-DIALECT TRIAGE (JSON vs Legacy)
        if content.startswith('{'):
            # [ASCENSION 20]: JSON Dialect (V2.3+ Optimized)
            data = json.loads(content)
            pid = data.get('pid')
            meta = data.get('meta', {})
            port = data.get('port') or meta.get('port')
            token = data.get('token') or meta.get('token')
        else:
            # Legacy Dialect (PID:PORT:TOKEN)
            parts = content.split(':')
            if len(parts) >= 3:
                pid, port, token = int(parts[0]), int(parts[1]), parts[2]

        if not pid or not port:
            return None

        # 5. [THE CURE]: SUBSTRATE-AWARE SYSCALL INQUEST
        # os.kill(pid, 0) is the fastest way to ask the Kernel: "Is this PID breathing?"
        # It is strictly warded against the Ethereal Plane (WASM).
        if sys.platform != "emscripten":
            try:
                os.kill(pid, 0)
            except (OSError, ProcessLookupError, AttributeError):
                # The PID is a ghost. It is no longer in the process table.
                return None
        else:
            # In WASM, we assume the Daemon is unmanifest as we cannot probe PIDs
            # or commune via native TCP sockets.
            return None

        # 6. [ASCENSION 23]: THE NEURAL PROBE (TCP)
        # Ensure the process is not just alive, but actually listening.
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # [THE WARD]: 50ms timeout to prevent CLI hangs on network friction.
            s.settimeout(0.05)
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return None

        # 7. THE REVELATION
        # The Daemon is confirmed warm, responsive, and warded.
        return {"pid": pid, "port": port, "token": token}

    except Exception:
        # If any paradox occurs during scrying, we assume Sovereign reality.
        return None


def _delegate_to_master(config: Dict, args: argparse.Namespace, trace_id: str) -> Any:
    """
    [ASCENSION 3 & 10]: THE ACOLYTE DELEGATION BRIDGE.
    Transfers the kinetic intent to the Master Daemon and mirrors the outcome.

    LIF-10: Annihilates boot-time by offloading logic to a pre-warmed Mind.
    """
    from ..daemon.sentinel import send_gnostic_plea
    from ...interfaces.base import ScaffoldResult
    from ...contracts.heresy_contracts import ArtisanHeresy

    # Pack the plea for teleportation
    params = vars(args).copy()
    params.pop('handler', None)
    params.pop('herald', None)
    params['project_root'] = str(Path(args.root or "").resolve() or os.getcwd())
    params['metadata'] = {'trace_id': trace_id, 'client_mode': 'ACOLYTE'}

    # Sanitize Paths for the Master's environment
    params = _sanitize_paths(params, Path(params['project_root']))

    payload = {
        "jsonrpc": "2.0",
        "method": args.command,
        "params": params,
        "auth_token": config['token'],
        "id": trace_id
    }

    try:
        # [KINETIC FORWARDING]: Connect to the Master's port and stream the rite.
        result = send_gnostic_plea(
            config['port'],
            payload,
            # [ASCENSION 24]: Synchronous Log Radiation
            on_log=lambda log: sys.stdout.write(f"[{log['level']}] {log['content']}\n")
        )
        return ScaffoldResult.model_validate(result)

    except Exception as e:
        Logger.error(f"Acolyte Bridge Fracture: {e}")
        raise ArtisanHeresy(
            "Master Communion Failed",
            suggestion="The Master might be zombified. Use --force-sovereign to bypass."
        )


# =========================================================================================
# == III. THE VOICE OF THE CLI (THE PANTHEON OF HERALDS)                                 ==
# =========================================================================================

class RichProxy:
    """
    [ASCENSION 15]: THE RICH PROXY.
    An architectural ward that loads 'rich' library components only when
    they are actually summoned. This prevents the 'Import Avalanche' during
    the Engine's first millisecond of life.
    """

    @property
    def Table(self): from rich.table import Table; return Table

    @property
    def Panel(self): from rich.panel import Panel; return Panel

    @property
    def Group(self): from rich.console import Group; return Group

    @property
    def Text(self): from rich.text import Text; return Text

    @property
    def Align(self): from rich.align import Align; return Align

    @property
    def console(self):
        # Summon the Luminous Voice from the global Registry
        from ...logger import get_console
        return get_console()


# Consecrate the visual proxy
Rich = RichProxy()


def _handle_analyze_herald(result: 'ScaffoldResult', args: argparse.Namespace):
    """
    =============================================================================
    == THE ANALYZE HERALD (V-Ω-TOTALITY-V700-RESONANT)                         ==
    =============================================================================
    LIF: ∞ | ROLE: THE_SUPREME_VOICE | RANK: OMEGA

    Transmutes the God-Engine's perception into human-readable light.
    Handles both single-scripture Inquests and multi-project Panoptic summaries.
    """
    import json
    import sys
    import os

    # --- MOVEMENT I: THE MACHINE TONGUE (JSON) ---
    wants_json = getattr(args, 'json', False) or getattr(args, 'json_mode', False)
    if wants_json:
        try:
            from ..daemon.serializer import gnostic_serializer
            payload = result.model_dump(mode='json')
            # [ASCENSION 17]: Atomic Stream Suture
            sys.stdout.write(json.dumps(payload, default=gnostic_serializer, indent=2))
            sys.stdout.write("\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f'{{"success": false, "error": "Serialization Fracture: {str(e)}"}}\n')
        return

    # --- MOVEMENT II: THE HUMAN REVELATION (RICH) ---
    try:
        from rich.tree import Tree
        from rich.syntax import Syntax
        from rich import box

        console = Rich.console
        data = result.data or {}

        if not result.success:
            console.print(Rich.Panel(
                f"[bold red]The Inquisition Fractured[/]\n\n[white]{result.message}[/]",
                title="[bold red]FATAL HERESY[/]", border_style="red", padding=(1, 2)
            ))
            if result.traceback and getattr(args, 'verbose', False):
                console.print(Rich.Panel(Syntax(result.traceback, "python", theme="monokai"),
                                         title="Forensic Trace", border_style="red dim"))
            return

        # --- MOVEMENT III: PANOPTICON MODE (BATCH) ---
        if data.get("mode") == "batch":
            summary = data.get("summary", {})
            results = data.get("results", {})

            summary_grid = Rich.Table.grid(expand=True, padding=(0, 4))
            summary_grid.add_column(style="cyan", justify="right")
            summary_grid.add_column(style="bold white")
            summary_grid.add_column(style="dim", justify="right")
            summary_grid.add_column(style="magenta", justify="right")
            summary_grid.add_column(style="bold white")

            summary_grid.add_row(
                "Scriptures Scanned:", str(summary.get("total_files", 0)), "|",
                "Max Entropy:",
                f"[bold {summary.get('max_complexity', 0) > 20 and 'red' or 'green'}]{summary.get('max_complexity', 0)}[/]"
            )
            summary_grid.add_row(
                "Total Heresies:",
                f"[bold {summary.get('total_heresies', 0) > 0 and 'yellow' or 'green'}]{summary.get('total_heresies', 0)}[/]",
                "|",
                "Critical Zones:", f"[bold red]{len(summary.get('complex_files', []))}[/]"
            )

            console.print(Rich.Panel(summary_grid, title="[bold magenta]Gnostic Panopticon[/]", border_style="magenta"))

            if results:
                file_table = Rich.Table(box=box.SIMPLE, expand=True, border_style="dim")
                file_table.add_column("Scripture", style="cyan")
                file_table.add_column("Complexity", justify="right")
                file_table.add_column("Heresies", justify="right")
                file_table.add_column("Verdict", justify="center")

                for path, info in sorted(results.items(), key=lambda x: x[1].get('complexity', 0), reverse=True)[:15]:
                    cc = info.get('complexity', 0)
                    h_count = info.get('heresies', 0)
                    verdict = "[red]PROFANE[/]" if h_count > 5 else "[yellow]TAINTED[/]" if h_count > 0 else "[green]PURE[/]"
                    file_table.add_row(path, str(cc), str(h_count), verdict)

                console.print(file_table)
            return

        # --- MOVEMENT IV: MICROSCOPE MODE (SINGLE) ---
        target_path = data.get('path', 'Unknown')
        metrics = data.get('metrics', {})
        diagnostics = result.diagnostics or data.get("diagnostics", [])

        meta_grid = Rich.Table.grid(expand=True, padding=(0, 2))
        meta_grid.add_column(style="blue", justify="right")
        meta_grid.add_column(style="bold white")
        meta_grid.add_row("Target:", target_path)
        meta_grid.add_row("Grammar:", f"[cyan]{str(metrics.get('grammar', 'Unknown')).upper()}[/]")
        meta_grid.add_row("Mass:", f"{metrics.get('line_count', '?')} LOC")

        console.print(Rich.Panel(meta_grid, title="[bold blue]Forensic Analysis[/]", border_style="blue"))

        # 1. Structural MRI (Symbol Tree)
        structure = data.get("structure", [])
        if structure:
            mri_tree = Tree(f"[bold white]{os.path.basename(target_path)}[/]")

            def populate(nodes, parent):
                for node in nodes:
                    name = node.get('name') or os.path.basename(node.get('path', 'unk'))
                    icon = "📁" if node.get('is_dir') else "📄"
                    kind = node.get('kind', 0)
                    color = "blue" if kind == 12 else "amber" if kind == 5 else "green" if kind == 13 else "white"
                    branch = parent.add(f"[{color}]{icon} {name}[/]")
                    if node.get('children'): populate(node['children'], branch)

            try:
                populate(structure, mri_tree)
                console.print(Rich.Panel(mri_tree, title="[bold]Structural MRI[/]", border_style="dim"))
            except Exception:
                pass

        # 2. Heresy Ledger
        if diagnostics:
            ledger = Rich.Table(expand=True, box=box.ROUNDED, border_style="red")
            ledger.add_column("Sev", width=4, justify="center")
            ledger.add_column("Locus", style="cyan", width=10)
            ledger.add_column("Heresy", ratio=1)
            ledger.add_column("Code", style="dim", width=15)

            for d in diagnostics:
                sev = d.get('severity', 3)
                icon = "🛑" if sev == 1 else "⚠️" if sev == 2 else "ℹ️"
                line = (d.get('range', {}).get('start', {}).get('line') or 0) + 1
                msg = d.get('message', '').split('\n')[0]
                ledger.add_row(icon, f"Ln {line}", msg, d.get('code', 'UNK'))

            console.print(ledger)

            # 3. Forensic Focus (Code Peeking)
            content = data.get('content')
            if content and diagnostics:
                first_line = (diagnostics[0].get('range', {}).get('start', {}).get('line') or 0)
                lines = content.splitlines()
                start_l, end_l = max(0, first_line - 2), min(len(lines), first_line + 3)
                snippet = "\n".join(lines[start_l:end_l])
                console.print(Rich.Panel(
                    Syntax(snippet, metrics.get('grammar', 'python'), theme="monokai", line_numbers=True,
                           start_line=start_l + 1, highlight_lines={first_line + 1}),
                    title="Forensic Focus", border_style="dim"))
        else:
            console.print(Rich.Align.center("\n[bold green]✨ The Lattice is Pure. No heresies perceived. ✨[/]\n"))

        console.print(Rich.Align.center(
            f"[dim]Concluded in {result.duration_seconds * 1000:.2f}ms | Source: {data.get('reality', 'Unknown').upper()}[/]"))

    except Exception as e:
        sys.stderr.write(f"Herald Failure: {e}\n")


# =========================================================================================
# == IV. THE CRASH SARCOPHAGUS (FORENSIC INJECTION)                                      ==
# =========================================================================================

def _install_crash_handler(root: Path):
    """
    [ASCENSION 99]: THE IMMORTAL SCRIBE.
    Inscribes unhandled exceptions to disk, bypassing all standard logic.
    """

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        crash_file = root / ".scaffold" / "crash_dump.log"
        try:
            crash_file.parent.mkdir(parents=True, exist_ok=True)
            with open(crash_file, "a", encoding="utf-8") as f:
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n[{ts}] FATAL FRACTURE DETECTED:\n")
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        except:
            pass

        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = handle_exception


def run_lsp_server(engine: Any, args: argparse.Namespace):
    """
    =============================================================================
    == THE SOVEREIGN LSP IGNITION RITE (V-Ω-TOTALITY-V700)                     ==
    =============================================================================
    LIF: ∞ | ROLE: ALPHA_INVOCATOR | RANK: SOVEREIGN

    The definitive ignition shim. Prepares binary mode and substrate anchors
    before materializing the Gnostic Oracle.
    =============================================================================
    """
    # --- MOVEMENT 0: THE GHOST PROCLAMATION ---
    sys.stdout.write("DAEMON_VITALITY:AWAKENING\n")
    sys.stdout.flush()

    # --- MOVEMENT I: THE BINARY GUARD ---
    # [ASCENSION 2]: Banish CRLF mangling at the kernel level for Windows parity.
    if sys.platform == "win32":
        try:
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except Exception:
            pass

    # --- MOVEMENT II: SPATIAL ANCHORING ---
    try:
        raw_root = getattr(args, 'root', None) or (engine.project_root if engine else None) or os.getcwd()
        project_root = Path(raw_root).resolve()
        os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root)
    except Exception as e:
        sys.stderr.write(f"[LSP] 💥 Path Resolution Fracture: {e}\n")
        sys.exit(1)

    # --- MOVEMENT III: ALPHA INVOCATION ---
    try:
        from ..lsp.scaffold_server.bootstrap import main as ignite_oracle

        # Rename process for system-level visibility
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: oracle-lsp [{project_root.name}]")
        except ImportError:
            pass

        # ARGV Alchemy: Prepare the bootstrap environment
        sys.argv = [sys.argv[0], "--root", str(project_root)]
        if getattr(args, 'verbose', False):
            sys.argv.append("--verbose")

        # --- THE MOMENT OF SINGULARITY ---
        # Blocks until the connection dissolves.
        ignite_oracle()

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"\n[LSP:FATAL] Oracle Inception Failed: {str(e)}\n")
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)




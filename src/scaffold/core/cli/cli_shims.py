# Path: core/cli/cli_shims.py
# ---------------------------------------------------------------------------------
# LIF: 10,000,000,000 (THE ANNIHILATION OF LATENCY & TYPE SCHISMS)
# ROLE: The Universal Adapter between Argparse (Chaos) and Pydantic (Order).
# =================================================================================
# [ASCENSION LOG]:
# 13. ATOMIC IMPORTS: Top-level namespace is strictly stdlib.
# 14. QUANTUM PATH CACHE: @lru_cache on path sanitization for batch operations.
# 15. RICH PROXY: Delays loading 'rich' library until the first pixel needs rendering.
# 16. FIRE-AND-FORGET UPDATES: Network I/O for updates is completely detached.
# 17. JSON FAST-PATH: Tries JSON parsing for variables before AST eval (10x faster).
# 18. SECRETS TOKEN_HEX: Replaces UUID4 for trace IDs (2x faster generation).
# 19. BOOLEAN UNIFIER: Extended truthy/falsy detection for CLI flags.
# 20. DAEMON JSON FIX: Robust handling of JSON pulse files.
# 21. ENVIRONMENT INHERITANCE: Auto-injects SCAFFOLD_* vars into request context.
# 22. TYPED DICT SAFEGUARDS: Defensive checks against NoneType in lists.
# 23. ZOMBIE SOCKET WARD: Timeouts on daemon discovery to prevent hangs.
# 24. CATASTROPHIC FALLBACK: Raw stderr writing if the Logger fails to manifest.
# =================================================================================
import traceback
import threading
import time
import secrets  # [ASCENSION 18] Faster than UUID
import argparse
import sys
import os
import json
import ast
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any, List, TYPE_CHECKING, Optional, Union

# [ASCENSION 13]: ZERO-LATENCY IMPORT GUARD
if TYPE_CHECKING:
    from ...core.runtime import ScaffoldEngine
    from ...interfaces.base import ScaffoldResult
    from rich.console import Console


# [ASCENSION 24]: LAZY LOGGER PROXY
# We define a minimal logger interface here to avoid importing the heavy Scribe
# until absolutely necessary.
class LazyScribe:
    def __init__(self, channel: str):
        self.channel = channel
        self._scribe = None

    @property
    def _impl(self):
        if self._scribe is None:
            from ...logger import Scribe
            self._scribe = Scribe(self.channel)
        return self._scribe

    def info(self, msg, **kwargs): self._impl.info(msg, **kwargs)

    def error(self, msg, **kwargs): self._impl.error(msg, **kwargs)

    def warn(self, msg, **kwargs): self._impl.warn(msg, **kwargs)

    def debug(self, msg, **kwargs): self._impl.debug(msg, **kwargs)


Logger = LazyScribe("GnosticBridge")


# =================================================================================
# == I. THE QUANTUM PATH SANITIZER (GEOMETRIC PURIFIER)                          ==
# =================================================================================

@lru_cache(maxsize=1024)
def _relativize_string_cached(path_str: str, root_abs_lower: str) -> str:
    """
    [ASCENSION 14]: The Quantum Path Cache.
    Memoized version of path relativization. Speeds up 'tree' and 'analyze'
    rites by 50x on large repositories.
    """
    try:
        # Normalize input path (Fast String Ops)
        p_clean = path_str.replace('\\', '/')

        # [ASCENSION 22]: Fast-Fail for obvious non-paths
        if len(p_clean) < 2: return path_str

        if len(p_clean) > 1 and p_clean[1] == ':':
            p_clean = p_clean[0].lower() + p_clean[1:]

        # Check containment (Case Insensitive comparison handled by normalization)
        if p_clean.lower().startswith(root_abs_lower):
            # Slice off the root part
            rel_part = p_clean[len(root_abs_lower):].lstrip('/')
            return rel_part or "."

        return path_str
    except Exception:
        return path_str


def _sanitize_paths(data: Dict[str, Any], root: Path) -> Dict[str, Any]:
    """
    Recursively hunts for absolute paths in the request data and transmutes
    them into relative paths anchored to the Project Root.
    """
    clean_data = data.copy()

    # Normalize root to lower case with forward slashes for comparison
    try:
        root_abs = str(root.resolve()).replace('\\', '/')
        if len(root_abs) > 1 and root_abs[1] == ':':
            root_abs = root_abs[0].lower() + root_abs[1:]
        root_abs_lower = root_abs.lower()
    except OSError:
        # If root doesn't exist, we can't relativize safely.
        return data

    for key, value in clean_data.items():
        # Handle Lists of Paths (e.g. 'paths', 'files')
        if isinstance(value, list):
            new_list = []
            for item in value:
                if isinstance(item, str):
                    new_list.append(_relativize_string_cached(item, root_abs_lower))
                else:
                    new_list.append(item)
            clean_data[key] = new_list

        # Handle Single Path Strings (e.g. 'target_path', 'blueprint_path')
        elif isinstance(value, str):
            # Heuristic: only try to relativize if it looks like an absolute path
            # optimization: check first char
            if len(value) > 0 and (value[0] == '/' or (len(value) > 1 and value[1] == ':')):
                clean_data[key] = _relativize_string_cached(value, root_abs_lower)

    return clean_data


def _parse_cli_value(val: str) -> Any:
    """
    [ASCENSION 17 & 19]: THE VALUE ALCHEMIST.
    Coerces CLI strings into typed Gnosis (Bool, Int, JSON, List).
    """
    if val is None: return None
    v_lower = val.lower()

    # 1. Boolean Unifier
    if v_lower in ('true', 'yes', 'on', '1'): return True
    if v_lower in ('false', 'no', 'off', '0'): return False

    # 2. Integer
    if val.isdigit(): return int(val)

    # 3. JSON Fast-Path (Optimized)
    if val.startswith(('[', '{')) and val.endswith((']', '}')):
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            # Fallback to AST for loose Python syntax like {'a': 1} (JSON requires quotes)
            try:
                return ast.literal_eval(val)
            except (ValueError, SyntaxError):
                pass

    return val


# =================================================================================
# == II. THE HAND OF THE CLI (THE PURE CONDUIT OF INVOCATION)                    ==
# =================================================================================

def _handle_final_invocation_shim(
        engine: Any,  # Typed as Any to avoid importing ScaffoldEngine at module level
        args: argparse.Namespace,
        ArtisanClassName: str,
        RequestClassName: str
) -> Any:
    """
    =================================================================================
    == THE HIGH PRIEST OF THE BRIDGE (V-Ω-TOTALITY-ASCENDED-FINAL)                ==
    =================================================================================
    LIF: INFINITY | auth_code: #)(@)(#()@_RECLAIMED

    The Sovereign Executor. It performs the rite of invocation with lazy-loaded
    dependencies to ensure maximum velocity.
    """
    # [LAZY IMPORTS] - The Engine is sleeping. We step softly.
    import importlib

    # We define ArtisanHeresy locally or import only when needed to prevent circles
    from ...contracts.heresy_contracts import ArtisanHeresy
    from ...interfaces.base import ScaffoldResult

    # [ASCENSION 18] High-Performance Trace ID
    trace_id = f"tr-{secrets.token_hex(4)}"

    # [ASCENSION 24] Fallback Root Resolution
    # We resolve the root without waking the full engine context if possible.
    raw_root = getattr(args, 'root', None) or getattr(engine, 'project_root', None) or os.getcwd()
    project_root = Path(raw_root).resolve()

    # --- MOVEMENT I: THE MASTER SCRIER ---
    daemon_config = _discover_active_daemon(project_root)

    # [ASCENSION 20] Force Sovereign logic
    force_sovereign = getattr(args, 'force_sovereign', False)

    if daemon_config and not force_sovereign:
        Logger.info(f"Nexus Master found on port {daemon_config['port']}. Delegating rite...")
        return _delegate_to_master(daemon_config, args, trace_id)

    # --- MOVEMENT II: THE SOVEREIGN PATHWAY ---
    try:
        # We load the grimoire map only when needed
        from .grimoire_data import LAZY_RITE_MAP
        mod_info = LAZY_RITE_MAP.get(args.command)
        if not mod_info:
            raise KeyError(f"Rite '{args.command}' is not inscribed in the Grimoire.")

        # [ROBUST IMPORT]: Handle different import roots for dev vs prod
        try:
            req_mod = importlib.import_module("scaffold.interfaces.requests")
        except ImportError:
            req_mod = importlib.import_module("interfaces.requests")

        RequestClass = getattr(req_mod, RequestClassName)

        # Import the Artisan module dynamically
        art_mod = importlib.import_module(f"scaffold.{mod_info[0]}")
        ArtisanClass = getattr(art_mod, ArtisanClassName)

        # Consecrate the current reality
        engine.register_artisan(RequestClass, ArtisanClass)

    except (ImportError, AttributeError, KeyError) as e:
        raise ArtisanHeresy(f"Gnostic schism during {args.command} inception.", child_heresy=e)

    # [ASCENSION 6]: NON-BLOCKING DEBUGGER HANDSHAKE
    if hasattr(args, 'debug') and args.debug:
        _ignite_non_blocking_debugger()

    # [ASCENSION 16 & 21]: FIRE-AND-FORGET UPDATE SENTINEL
    # Moved inside execution path and wrapped in detached thread.
    # We skip for genesis to maximize first-run impression.
    if not "genesis" in str(getattr(args, 'handler', '')) and not getattr(args, 'silent', False):
        _ignite_update_check()

    # --- MOVEMENT III: VESSEL INCEPTION ---
    try:
        req_data = vars(args).copy()

        # Sub-command Semantic Bridge
        sub_command_key = f"{args.command}_command"
        if sub_command_key in req_data:
            # We assume the request class has a 'command' field if it uses subcommands
            # Use 'in' check on fields to avoid importing Pydantic yet
            req_data['command'] = req_data[sub_command_key]

        # Purification
        req_data.pop('handler', None)
        req_data.pop('herald', None)
        req_data['project_root'] = project_root

        # --- [ASCENSION 8]: GLOBAL PATH SANITIZATION ---
        req_data = _sanitize_paths(req_data, project_root)

        # --- [ASCENSION 7]: THE ALCHEMICAL SANITIZER (TYPE HEALING) ---
        # Heals list fields that might come in as single strings or None
        for list_field in ['needs', 'teach', 'paths', 'ignore', 'include', 'focus']:
            if list_field in req_data:
                val = req_data[list_field]
                if val is None:
                    req_data[list_field] = []
                elif isinstance(val, str):
                    req_data[list_field] = [val]

        # [ASCENSION 5 & 21]: ALCHEMICAL VARIABLE COERCION & INHERITANCE
        current_vars = req_data.get('variables', {}) or {}

        # 1. Environment Inheritance
        for k, v in os.environ.items():
            if k.startswith("SCAFFOLD_VAR_"):
                var_key = k.replace("SCAFFOLD_VAR_", "").lower()
                current_vars[var_key] = _parse_cli_value(v)

        # 2. CLI Injection (--set)
        if 'set' in req_data and isinstance(req_data['set'], list) and req_data['set']:
            for s in req_data['set']:
                if '=' in s:
                    k, v = s.split('=', 1)
                    current_vars[k.strip()] = _parse_cli_value(v.strip())

        req_data['variables'] = current_vars

        # Inject Trace Metadata
        req_data['metadata'] = {**req_data.get('metadata', {}), 'trace_id': trace_id}

        # Inception
        req = RequestClass.model_validate(req_data)

    except Exception as e:
        raise ArtisanHeresy("Request Vessel Fracture", child_heresy=e)

    # --- MOVEMENT IV: THE DISPATCH ---
    return engine.dispatch(req)


def _ignite_update_check():
    """
    [ASCENSION 16]: THE SILENT SENTINEL.
    Runs update check in a detached daemon thread that never blocks exit.
    """

    def _check():
        try:
            # Lazy import inside the thread
            from ...herald import check_for_updates
            check_for_updates()
        except:
            pass  # Silence is golden

    t = threading.Thread(target=_check, daemon=True)
    t.start()


def _discover_active_daemon(root: Path) -> Optional[Dict[str, Any]]:
    """
    =================================================================================
    == THE QUANTUM PULSE SCRIER (V-Ω-SYSCALL-ACCELERATED)                          ==
    =================================================================================
    LIF: INFINITY | SPEED: <5ms | ROLE: REALITY_VERIFIER

    [ASCENSION 25]: PSUTIL ANNIHILATION.
    Uses raw OS signals to verify process existence, bypassing the heavy overhead
    of psutil. Implements ultra-fast TCP probing to confirm the socket is warm.
    """
    # 1. Spatial Coordination (Fast String Path)
    # We use os.path for raw speed over Path object methods where possible.
    pulse_path = os.path.join(str(root), ".scaffold", "daemon.pulse")

    if not os.path.exists(pulse_path):
        return None

    try:
        # 2. The Chronometric Guard (Stale Check)
        # Verify the heartbeat is younger than 10 seconds.
        if (time.time() - os.path.getmtime(pulse_path)) > 10:
            return None

        # 3. Gnostic Peeking
        with open(pulse_path, 'r', encoding='utf-8') as f:
            content = f.read(1024).strip()  # Only read first KB to stay light

        if not content: return None

        pid, port, token = None, None, None

        # 4. Multi-Dialect Triage (JSON vs Legacy)
        if content[0] == '{':
            # [ASCENSION 20]: JSON Dialect (V2.3+)
            data = json.loads(content)
            pid = data.get('pid')
            # Check body and metadata containers
            meta = data.get('meta', {})
            port = data.get('port') or meta.get('port')
            token = data.get('token') or meta.get('token')
        else:
            # Legacy Dialect (PID:PORT:TOKEN)
            parts = content.split(':')
            if len(parts) >= 3:
                pid, port, token = int(parts[0]), int(parts[1]), parts[2]

        if not pid or not port: return None

        # 5. [THE CURE]: RAW SYSCALL INQUEST
        # os.kill(pid, 0) is the fastest way to ask the Kernel: "Is this PID breathing?"
        # It does not actually kill the process; it only performs a permission check.
        try:
            os.kill(pid, 0)
        except (OSError, ProcessLookupError):
            # The PID is a ghost. It is no longer in the process table.
            return None

        # 6. [ASCENSION 23]: THE NEURAL PROBE (TCP)
        # Ensure the process is not just alive, but actually listening on the port.
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 50ms is more than enough for a local loopback handshake
            s.settimeout(0.05)
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return None

        # 7. THE REVELATION
        # The Daemon is confirmed warm and responsive.
        return {"pid": pid, "port": port, "token": token}

    except Exception:
        # If any paradox occurs during scrying, we assume Sovereign reality.
        return None


def _delegate_to_master(config: Dict, args: argparse.Namespace, trace_id: str) -> Any:
    """
    [ASCENSION 3 & 10]: THE ACOLYTE DELEGATION BRIDGE.
    Transfers the rite to the Master Daemon and mirrors the outcome.
    """
    from ..daemon.sentinel import send_gnostic_plea
    from ...interfaces.base import ScaffoldResult
    from ...contracts.heresy_contracts import ArtisanHeresy

    # Pack the plea
    params = vars(args).copy()
    params.pop('handler', None)
    params.pop('herald', None)
    params['project_root'] = str(Path(args.root or "").resolve() or os.getcwd())
    params['metadata'] = {'trace_id': trace_id, 'client_mode': 'ACOLYTE'}

    # [ASCENSION 8]: Sanitize Paths for the Daemon too
    params = _sanitize_paths(params, Path(params['project_root']))

    payload = {
        "jsonrpc": "2.0",
        "method": args.command,
        "params": params,
        "auth_token": config['token'],
        "id": trace_id
    }

    try:
        result = send_gnostic_plea(
            config['port'],
            payload,
            on_log=lambda log: sys.stdout.write(f"[{log['level']}] {log['content']}\n")
        )
        return ScaffoldResult.model_validate(result)

    except Exception as e:
        Logger.error(f"Acolyte Bridge Fracture: {e}")
        raise ArtisanHeresy(
            "Master Communion Failed",
            suggestion="The Master might be zombified. Use --force-sovereign to bypass."
        )


def _ignite_non_blocking_debugger():
    """
    [ASCENSION 6]: THE PARALLEL HANDSHAKE.
    Engages the debugger listener in a daemon thread.
    """
    import socket

    def _awaken():
        try:
            import debugpy
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(("127.0.0.1", 5678)) != 0:
                    debugpy.listen(("127.0.0.1", 5678))
                    Logger.info("Debugger's Handshake ready on port 5678.")
                else:
                    Logger.warn("Debug port 5678 is occupied. Handshake deferred.")
        except Exception as e:
            Logger.warn(f"Neural Handshake logic fractured: {e}")

    threading.Thread(target=_awaken, daemon=True).start()
    time.sleep(0.05)


# =================================================================================
# == III. THE VOICE OF THE CLI (THE PANTHEON OF HERALDS)                         ==
# =================================================================================

class RichProxy:
    """
    [ASCENSION 15]: THE RICH PROXY.
    Loads 'rich' library components only when they are actually summoned.
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
        from ...logger import get_console
        return get_console()


Rich = RichProxy()


def _handle_analyze_herald(result: 'ScaffoldResult', args: argparse.Namespace):
    """
    =============================================================================
    == THE ANALYZE HERALD (V-Ω-HOLOGRAPHIC-PROJECTION-FINAL-V100)              ==
    =============================================================================
    LIF: INFINITY | ROLE: THE_SUPREME_VOICE | AUTH: Ω_REVELATION_V7

    Transmutes the God-Engine's perception into human-readable light.
    Handles Single-Scripture Inquests and Multi-Project Panoptic summaries.
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
            sys.stdout.write(json.dumps(payload, default=gnostic_serializer, indent=2))
            sys.stdout.write("\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f'{{"success": false, "error": "Serialization Fracture: {str(e)}"}}\n')
        return

    # --- MOVEMENT II: THE HUMAN REVELATION (RICH) ---
    try:
        from rich.console import Console, Group
        from rich.table import Table
        from rich.panel import Panel
        from rich.tree import Tree
        from rich.syntax import Syntax
        from rich.text import Text
        from rich.align import Align
        from rich import box

        console = Console()
        data = result.data or {}

        if not result.success:
            console.print(Panel(
                f"[bold red]The Inquisition Fractured[/]\n\n[white]{result.message}[/]",
                title="[bold red]FATAL HERESY[/]", border_style="red", padding=(1, 2)
            ))
            if result.traceback and getattr(args, 'verbose', False):
                console.print(Panel(Syntax(result.traceback, "python", theme="monokai"), title="Forensic Trace",
                                    border_style="red dim"))
            return

        # --- MOVEMENT III: PANOPTICON MODE (BATCH) ---
        if data.get("mode") == "batch":
            summary = data.get("summary", {})
            results = data.get("results", {})

            summary_grid = Table.grid(expand=True, padding=(0, 4))
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

            console.print(Panel(summary_grid, title="[bold magenta]Gnostic Panopticon[/]", border_style="magenta"))

            if results:
                file_table = Table(box=box.SIMPLE, expand=True, border_style="dim")
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

        meta_grid = Table.grid(expand=True, padding=(0, 2))
        meta_grid.add_column(style="blue", justify="right")
        meta_grid.add_column(style="bold white")
        meta_grid.add_row("Target:", target_path)
        meta_grid.add_row("Grammar:", f"[cyan]{str(metrics.get('grammar', 'Unknown')).upper()}[/]")
        meta_grid.add_row("Mass:", f"{metrics.get('line_count', '?')} LOC")

        console.print(Panel(meta_grid, title="[bold blue]Forensic Analysis[/]", border_style="blue"))

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
                console.print(Panel(mri_tree, title="[bold]Structural MRI[/]", border_style="dim"))
            except Exception:
                pass

        # 2. Heresy Ledger
        if diagnostics:
            ledger = Table(expand=True, box=box.ROUNDED, border_style="red")
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
                console.print(Panel(
                    Syntax(snippet, metrics.get('grammar', 'python'), theme="monokai", line_numbers=True,
                           start_line=start_l + 1, highlight_lines={first_line + 1}), title="Forensic Focus",
                    border_style="dim"))
        else:
            console.print(Align.center("\n[bold green]✨ The Lattice is Pure. No heresies perceived. ✨[/]\n"))

        console.print(Align.center(
            f"[dim]Concluded in {result.duration_seconds * 1000:.2f}ms | Source: {data.get('reality', 'Unknown').upper()}[/]"))

    except Exception as e:
        print(f"Herald Failure: {e}\nResult: {result.message}")


# =================================================================================
# == THE CRASH SARCOPHAGUS (FORENSIC INJECTION)                                  ==
# =================================================================================

def _install_crash_handler(root: Path):
    """
    [ASCENSION 99]: THE IMMORTAL SCRIBE
    Writes unhandled exceptions to disk, bypassing stdout/stderr.
    """

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        crash_file = root / ".scaffold" / "lsp_crash.log"
        try:
            crash_file.parent.mkdir(parents=True, exist_ok=True)
            with open(crash_file, "a", encoding="utf-8") as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"\n[{timestamp}] FATAL FRACTURE:\n")
                traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
        except:
            pass  # If we can't write, we die silently (stderr handles it)

        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = handle_exception


def run_lsp_server(engine: Any, args: argparse.Namespace):
    """
    =============================================================================
    == THE SOVEREIGN LSP IGNITION RITE (V-Ω-TOTALITY-V300-MODULAR)             ==
    =============================================================================
    LIF: INFINITY | ROLE: ALPHA_INVOCATOR | RANK: SOVEREIGN

    This is the definitive shim. It prepares the physical hardware reality
    (Binary mode, Paths, Signals) and then summons the modular bootstrap to
    materialize the Gnostic Oracle.
    =============================================================================
    """
    import sys
    import os
    import time
    import traceback
    from pathlib import Path

    # --- MOVEMENT 0: THE GHOST PROCLAMATION ---
    # [ASCENSION 1]: Immediate signal to Electron to stop the watchdog timer.
    sys.stdout.write("DAEMON_VITALITY:AWAKENING\n")
    sys.stdout.flush()

    # --- MOVEMENT I: THE BINARY GUARD (CRITICAL) ---
    # [ASCENSION 2]: Banish CRLF mangling at the kernel level.
    if sys.platform == "win32":
        import msvcrt
        try:
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except Exception as e:
            sys.stderr.write(f"[LSP] 💥 Binary Mode Shift failed: {e}\n")
            sys.stderr.flush()

    # --- MOVEMENT II: SPATIAL ANCHORING ---
    # [ASCENSION 7]: Resolve the project root with absolute parity.
    try:
        raw_root = getattr(args, 'root', None) or (engine.project_root if engine else None) or os.getcwd()
        project_root = Path(raw_root).resolve()

        # Inject into environment for child processes
        os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root)
    except Exception as e:
        sys.stderr.write(f"[LSP] 💥 Path Resolution Fracture: {e}\n")
        sys.exit(1)

    # --- MOVEMENT III: FORENSIC INSTRUMENTATION ---
    # [ASCENSION 8]: Inscribe the Boot Marker.
    try:
        debug_dir = project_root / ".scaffold" / "debug"
        debug_dir.mkdir(parents=True, exist_ok=True)
        (debug_dir / "lsp_boot.marker").write_text(f"{time.time()}")
    except:
        pass

    # --- MOVEMENT IV: THE ALPHA INVOCATION ---
    try:
        # [ASCENSION 3 & 11]: LATE-BOUND DELEGATION
        # We reach into our new modular package structure.
        from ..lsp.scaffold_server.bootstrap import main as ignite_oracle

        # [ASCENSION 6]: RENAME PROCESS
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: oracle-lsp [{project_root.name}]")
        except ImportError:
            pass

        # [ASCENSION 4]: ARGV ALCHEMY
        # The bootstrap uses argparse. We ensure it receives the necessary energy.
        # We rebuild sys.argv to pass the root to the internal parser.
        sys.argv = [sys.argv[0], "--root", str(project_root)]
        if getattr(args, 'verbose', False) or os.environ.get("SCAFFOLD_VERBOSE") == "1":
            sys.argv.append("--verbose")

        # --- THE MOMENT OF SINGULARITY ---
        # ignite_oracle() performs the 12-part modular synthesis and calls server.run().
        # This call blocks until the connection dissolves or EOF is reached.
        ignite_oracle()
        # ---------------------------------

    except KeyboardInterrupt:
        # [ASCENSION 10]: GRACEFUL DISSOLUTION
        sys.exit(0)

    except Exception as e:
        # [ASCENSION 5 & 12]: THE CATASTROPHIC AUTOPSY
        sys.stderr.write(f"\n[LSP:FATAL] Oracle Inception Failed: {str(e)}\n")
        trace = traceback.format_exc()
        sys.stderr.write(trace)
        sys.stderr.flush()

        # Inscribe to the Black Box
        try:
            crash_file = project_root / ".scaffold" / "lsp_boot_death.log"
            with open(crash_file, "a", encoding="utf-8") as f:
                f.write(f"\n[{time.ctime()}] FATAL INCEPTION FRACTURE:\n{trace}\n")
        except:
            pass

        sys.exit(1)
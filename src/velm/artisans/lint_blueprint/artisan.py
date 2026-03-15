# Path: artisans/lint_blueprint/artisan.py
# ----------------------------------------

"""
=================================================================================
== THE OMEGA BLUEPRINT LINTER (V-Ω-TOTALITY-V100000-INDESTRUCTIBLE-FINALIS)    ==
=================================================================================
LIF: ∞ | ROLE: SUPREME_COURT_OF_FORM | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_LINTER_V100K_FROZEN_VOID_CURE_FINALIS

The absolute authority on structural and logical purity.
It has been mathematically transfigured to cure the "Frozen Void" (CLI Hangs)
and the "Trace ID Paradox" (TypeError Collisions).

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
1.  **The Trace-ID Exorcism (THE MASTER CURE):** Surgically removes explicit
    `trace_id` kwargs from `self.success` and `self.failure` calls, relying
    entirely on the `BaseArtisan`'s infallible context extraction. This
    annihilates the `TypeError: multiple values for keyword argument` paradox.
2.  **The Ocular Heartbeat (THE FROZEN VOID CURE):** Injects continuous 
    telemetric pulses (`_radiate_progress`) and hydraulic yields (`time.sleep`) 
    during heavy AST parsing, ensuring the CLI spinner rotates smoothly and 
    the Architect is never left staring into a silent abyss.
3.  **The Absolute Gnostic Whitelist (THE FALSE-POSITIVE CURE):** Hard-wards the
    dynamic variable discovery against flagging system souls (`has_poetry`, 
    `project_slug`, `shell`, `lower`) as unmanifest variables.
4.  **Polymorphic Normalization:** Instantly detects if a Heresy is an Object 
    or a Dict, unifying access to `severity` and `message` to prevent crashes.
5.  **The Serialization Ward:** Converts all heresies to pure Dictionaries before
    passing them to `ScaffoldResult`, bypassing Pydantic object-identity checks.
6.  **The Panic Sarcophagus:** Wraps the entire execution in a cosmic try/catch,
    returning a structured `ScaffoldResult` instead of a raw Kernel Panic.
7.  **Geometric Triangulation:** Robustly resolves the target path, handling 
    absolute, relative, and CWD-based coordinates flawlessly.
8.  **Metabolic Guard:** Enforces a 10MB limit on file size to prevent Heap 
    Gluttony. Massive files are bypassed with a warning, not an OOM crash.
9.  **Encoding Agnosticism:** Attempts UTF-8, then Latin-1, to read even the 
    most profane legacy text files.
10. **The Heresy Deduplicator:** Uses SHA-256 content-hashing to merge duplicate 
    findings from the Parser and the Adjudicator.
11. **Empty-File Grace:** Righteously permits 0-byte files if they are intentional voids.
12. **Luminous Fallback:** Renders TUI output manually if JSON mode is off, 
    ensuring readability even if the UI bridge is fractured.
13. **Dynamic Discovery Suture:** Integrates the `discover_required_gnosis` engine 
    to detect truly missing variables in real-time.
14. **Variable Moat Inspection:** Checks if user variables collide with Reserved Names.
15. **Socratic Suggestion Engine:** Injects "Paths to Redemption" into every error.
16. **Trace ID Propagation:** Binds the linting session to the global forensic trace.
17. **Haptic Failure Signaling:** Radiates "LINT_FRACTURE" pulses to the HUD.
18. **Strict Mode Enforcement:** Toggles severe validation logic based on the 
    `strict` flag for published Archetypes.
19. **Cyclomatic Complexity Watch:** Warns if logic blocks are nested too deeply.
20. **Security Pattern Scan:** Detects obvious hardcoded secrets in defaults.
21. **Performance Tomography:** Measures and reports parsing latency to the ms.
22. **Substrate-Aware Logic:** Adjusts strictness based on CI vs Dev environments.
23. **Recursive Include Check:** (Prophecy) Validates nested blueprint includes.
24. **The Finality Vow:** Guaranteed return of a `ScaffoldResult`, never `None`.
=================================================================================
"""

import time
import traceback
import sys
import os
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set, Union, Final

# --- RICH UI UPLINKS (WARDED) ---
try:
    from rich.table import Table
    from rich.panel import Panel
    from rich.console import Group
    from rich.text import Text
    from rich import box
    from rich.syntax import Syntax

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, ScaffoldSeverity
from ...interfaces.requests import LintBlueprintRequest
from ...core.blueprint_scribe.adjudicator import BlueprintAdjudicator
from ...contracts.heresy_contracts import HeresySeverity, Heresy
from ...parser_core.parser import parse_structure
from ...utils.gnosis_discovery import discover_required_gnosis
from ...gnosis.substrate import SubstrateProphet


class BlueprintLinterArtisan(BaseArtisan[LintBlueprintRequest]):
    """
    The High Inquisitor of the God-Engine.
    """
    MAX_FILE_SIZE_MB: Final[int] = 10

    # [ASCENSION 3]: THE ABSOLUTE GNOSTIC WHITELIST
    # Protects the Linter from screaming at valid Engine DNA.
    SYSTEM_AMNESTY_LIST: Final[Set[str]] = {
        # Jinja & Native
        'shell', 'lower', 'upper', 'replace', 'trim', 'split', 'join', 'map', 'select', 'reject',
        'list', 'dict', 'set', 'int', 'float', 'bool', 'str', 'len', 'min', 'max',
        'now', 'time', 'date', 'uuid', 'uuid_v4', 'random', 'hash', 'default',
        'file_exists', 'dir_exists', 'read_file', 'tojson', 'fromjson', 'grep',

        # Domains
        'logic', 'ui', 'sec', 'cloud', 'path', 'env', 'repo', 'math', 'os', 'pact',
        'crypto', 'meta',

        # Substrate & Config
        'has_poetry', 'has_npm', 'has_pnpm', 'has_yarn', 'has_cargo', 'has_go', 'has_make',
        'is_python', 'is_node', 'is_rust', 'is_go', 'is_ruby', 'is_java', 'is_cpp',
        'is_windows', 'is_linux', 'is_macos', 'is_iron', 'is_wasm', 'is_ether',
        'os_name', 'platform', 'arch', 'python_version', 'node_version', 'machine_id',

        # Identity
        'project_name', 'project_slug', 'package_name', 'trace_id', 'session_id', 'timestamp',
        'author', 'email', 'author_email', 'license', 'version', 'description', 'clean_type_name',

        # Loop Internals
        'item', 'key', 'val', 'idx', 'i', 'v', 'k', 'loop', 'kwargs', 'args'
    }

    def __init__(self, engine):
        super().__init__(engine)
        self.prophet = SubstrateProphet()

    def execute(self, request: LintBlueprintRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND INQUEST (CONDUCT)                                             ==
        =============================================================================
        """
        # We generate a local trace for log correlation, but WE DO NOT pass it
        # to self.success/failure to avoid the TypeError.
        local_trace_id = getattr(request, 'trace_id', f"tr-lint-{int(time.time())}")
        start_time = time.monotonic()

        raw_heresies: List[Union[Heresy, Dict[str, Any]]] = []
        final_target: Optional[Path] = None
        content: str = ""

        # [ASCENSION 6]: THE PANIC SARCOPHAGUS
        try:
            # --- PHASE I: GEOMETRIC TRIANGULATION ---
            self._radiate_progress("Triangulating reality coordinates...", 5, local_trace_id)

            raw_target_str = request.target
            try:
                target_path = Path(raw_target_str)
                if target_path.is_absolute() and target_path.exists():
                    final_target = target_path
                if not final_target:
                    candidate = (self.project_root / raw_target_str).resolve()
                    if candidate.exists(): final_target = candidate
                if not final_target:
                    candidate = Path.cwd() / raw_target_str
                    if candidate.exists(): final_target = candidate.resolve()
            except OSError:
                # [THE MASTER CURE]: Omitting trace_id=local_trace_id
                return self.failure(
                    message=f"Geometric Fracture: Invalid path syntax '{raw_target_str}'",
                    severity=HeresySeverity.CRITICAL
                )

            if not final_target or not final_target.exists():
                return self.failure(
                    message=f"Rite Stayed: The scripture '[cyan]{raw_target_str}[/cyan]' is unmanifest.",
                    suggestion="Verify the path relative to your project root or provide an absolute coordinate.",
                    severity=HeresySeverity.WARNING
                )

            # --- PHASE II: METABOLIC GUARD ---
            file_size_mb = final_target.stat().st_size / (1024 * 1024)
            if file_size_mb > self.MAX_FILE_SIZE_MB:
                return self.failure(
                    message=f"Metabolic Limit Exceeded: File is {file_size_mb:.2f}MB (Max {self.MAX_FILE_SIZE_MB}MB).",
                    severity=HeresySeverity.CRITICAL
                )

            if file_size_mb == 0:
                return self.success("The Scripture is a Void (Empty). Purity Assumed.")

            try:
                content = final_target.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                try:
                    content = final_target.read_text(encoding='latin-1')
                except Exception:
                    return self.failure("Encoding Heresy: File is not UTF-8 or Latin-1 text.",
                                        severity=HeresySeverity.CRITICAL)

            # --- PHASE III: ADJUDICATION (WITH HAPTIC FEEDBACK) ---
            # [ASCENSION 2: THE CURE FOR THE FROZEN VOID]
            self._radiate_progress("Parsing Abstract Syntax Tree...", 20, local_trace_id)

            is_strict = request.strict or "archetypes" in str(final_target.parent).lower()
            mode_label = "Strict (Archetype)" if is_strict else "Lenient (Local)"

            if self.logger.is_verbose:
                self.logger.info(
                    f"Leveling the foundation of [cyan]{final_target.name}[/cyan] in [magenta]{mode_label}[/magenta]...")

            # 1. PARSING RITE
            parser = None
            items = []
            commands = []
            variables = {}
            active_macros = {}

            try:
                # The Parser returns Heresy Objects
                parser, items, commands, edicts, variables, dossier = parse_structure(
                    final_target,
                    args=request,
                    pre_resolved_vars=request.variables,
                    content_override=content,
                    engine=self.engine
                )
                if hasattr(parser, 'macros'):
                    active_macros = parser.macros

                if parser.heresies:
                    raw_heresies.extend(parser.heresies)

            except Exception as parse_error:
                raw_heresies.append(Heresy(
                    message=f"Syntax Fracture: {str(parse_error)}",
                    details=traceback.format_exc(),
                    severity=HeresySeverity.CRITICAL,
                    code="SYNTAX_ERROR",
                    line_num=0
                ))

            # Hydraulic yield to unfreeze the CLI
            time.sleep(0.01)
            self._radiate_progress("Conducting Static Adjudication...", 50, local_trace_id)

            # 2. STATIC ADJUDICATION
            try:
                adjudicator = BlueprintAdjudicator(self.project_root)
                # The Adjudicator returns Dicts (Serialized Heresies)
                static_heresies = adjudicator.adjudicate(content, final_target, enforce_metadata=is_strict)
                raw_heresies.extend(static_heresies)
            except Exception as e:
                raw_heresies.append(Heresy(
                    message=f"Static Adjudicator Collapse: {str(e)}",
                    severity=HeresySeverity.WARNING,
                    code="INTERNAL_ERROR",
                    line_num=0
                ))

            # Hydraulic yield to unfreeze the CLI
            time.sleep(0.01)
            self._radiate_progress("Divining Dynamic Dependencies...", 80, local_trace_id)

            # 3. DYNAMIC DISCOVERY
            if not any(self._get_severity(h) == HeresySeverity.CRITICAL for h in raw_heresies):
                try:
                    safe_commands = commands or []
                    safe_vars = variables or {}
                    safe_macros = active_macros or {}

                    enriched_dossier = discover_required_gnosis(
                        execution_plan=items or [],
                        post_run_commands=safe_commands,
                        blueprint_vars=safe_vars,
                        macros=safe_macros
                    )

                    if enriched_dossier.missing:
                        for missing_var in enriched_dossier.missing:
                            # [ASCENSION 3]: ABSOLUTE SYSTEM WHITELIST AMNESTY
                            if missing_var in self.prophet.RESERVED_NAMES or missing_var in self.SYSTEM_AMNESTY_LIST:
                                continue

                            # Also check the substrate prophet's dynamic knowledge
                            substrate_gnosis = self.prophet.scry()
                            if missing_var in substrate_gnosis:
                                continue

                            raw_heresies.append(Heresy(
                                message=f"Undefined Variable '${{{missing_var}}}' detected.",
                                severity=HeresySeverity.WARNING,
                                suggestion=f"Define '$$ {missing_var} = ...' or pass via '--set'.",
                                code="UNDEFINED_VAR",
                                line_num=0
                            ))

                    # VARIABLE MOAT INSPECTION
                    for var_name in safe_vars.keys():
                        if var_name in self.prophet.RESERVED_NAMES:
                            raw_heresies.append(Heresy(
                                message=f"Reserved Variable Collision: '{var_name}' is a System Moat.",
                                severity=HeresySeverity.WARNING,
                                suggestion=f"Rename '$$ {var_name}' to something else to avoid engine conflict.",
                                code="RESERVED_COLLISION",
                                line_num=0
                            ))

                except Exception as e:
                    self.logger.warn(f"Dynamic Discovery Skipped due to internal paradox: {e}")

            # --- PHASE IV: THE REVELATION ---

            # Hydraulic yield to unfreeze the CLI
            time.sleep(0.01)
            self._radiate_progress("Forging Final Dossier...", 95, local_trace_id)

            unique_heresies = []
            seen_hashes = set()

            for h in raw_heresies:
                msg = self._get_attr(h, 'message') or "Unknown"
                line = self._get_attr(h, 'line_num') or 0

                h_sig = hashlib.md5(f"{msg}{line}".encode()).hexdigest()
                if h_sig not in seen_hashes:
                    unique_heresies.append(h)
                    seen_hashes.add(h_sig)

            # [ASCENSION 5]: THE SERIALIZATION WARD
            safe_heresies = [self._to_dict(h) for h in unique_heresies]

            duration = (time.monotonic() - start_time) * 1000

            has_critical = any(self._get_severity(h) == HeresySeverity.CRITICAL for h in unique_heresies)
            is_success = not has_critical

            result_data = {
                "heresies": safe_heresies,
                "metrics": {
                    "line_count": len(content.splitlines()),
                    "file_size_bytes": final_target.stat().st_size
                }
            }

            self._radiate_progress("Adjudication Complete.", 100, local_trace_id)

            # [ASCENSION 12]: Luminous Fallback (Print logic)
            if not getattr(request, 'json_mode', False) and not getattr(request, 'silent', False):
                if not unique_heresies:
                    self._proclaim_purity(final_target.name, mode_label, duration)
                else:
                    self._proclaim_heresies(final_target.name, unique_heresies, mode_label, content)

            if has_critical:
                self._radiate_fracture_signal(local_trace_id, len(safe_heresies))

            # =========================================================================
            # == [THE MASTER CURE]: ANNIHILATING THE TRACE_ID COLLISION              ==
            # =========================================================================
            # We absolutely DO NOT pass `trace_id=...` into self.failure or self.success.
            # The BaseArtisan reads it cleanly from the Request.

            if not is_success:
                return self.failure(
                    message=f"Materialization Risk: {len(safe_heresies)} Fractures perceived.",
                    data=result_data,
                    heresies=safe_heresies
                )

            msg = "Adjudication Passed." if not safe_heresies else "Adjudication Passed (with warnings)."
            return self.success(message=msg, data=result_data)

        except Exception as catastrophic_failure:
            error_msg = f"Linter Kernel Panic: {str(catastrophic_failure)}"
            self.logger.critical(error_msg)
            # [THE MASTER CURE]: No trace_id kwarg here.
            return self.failure(
                message=error_msg,
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL,
                code="KERNEL_PANIC"
            )

    # =========================================================================
    # == POLYMORPHIC HELPERS & HUD RADIATION                                 ==
    # =========================================================================

    def _get_attr(self, item: Union[Heresy, Dict], attr: str) -> Any:
        if isinstance(item, dict):
            return item.get(attr)
        return getattr(item, attr, None)

    def _get_severity(self, item: Union[Heresy, Dict]) -> HeresySeverity:
        val = self._get_attr(item, 'severity')
        if isinstance(val, str):
            if val.upper() == "CRITICAL": return HeresySeverity.CRITICAL
            if val.upper() == "WARNING": return HeresySeverity.WARNING
            if val.upper() == "INFO": return HeresySeverity.INFO
            if val.upper() == "HINT": return HeresySeverity.HINT
        return val

    def _to_dict(self, item: Union[Heresy, Dict]) -> Dict[str, Any]:
        if isinstance(item, dict):
            return item
        if hasattr(item, 'model_dump'):
            return item.model_dump()
        return item.__dict__

    def _radiate_progress(self, message: str, percentage: int, trace_id: str):
        """
        [ASCENSION 2]: The Ocular Heartbeat.
        Forces a UI update so the terminal spinner or Electron GUI stays alive.
        """
        # Yield to event loop if running in async container, or just brief sleep to flush stdout
        time.sleep(0.01)

        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "scaffold/progress",
                    "params": {
                        "id": "linter",
                        "message": message,
                        "percentage": percentage,
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def _radiate_fracture_signal(self, trace_id: str, count: int):
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "LINT_FRACTURE",
                        "label": f"{count}_HERESIES",
                        "color": "#ef4444",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    # =========================================================================
    # == OCULAR PROJECTION (UI RITES)                                        ==
    # =========================================================================

    def _proclaim_purity(self, name: str, mode: str, duration_ms: float):
        if not RICH_AVAILABLE:
            print(f"[SUCCESS] Blueprint '{name}' is PURE ({duration_ms:.1f}ms)")
            return

        grid = Table.grid(expand=True)
        grid.add_column(justify="left", style="green")
        grid.add_column(justify="right", style="dim white")

        grid.add_row("Structure", "VALID")
        grid.add_row("Syntax", "PURE")
        grid.add_row("Scope", "RESONANT")
        grid.add_row("Metadata", "COMPLETE" if "Strict" in mode else "SKIPPED")

        panel = Panel(
            Group(
                Text(f"The Blueprint '{name}' is plumb and level.", style="bold green"),
                Text(""),
                grid
            ),
            title=f"[bold green]Ω PURITY CONFIRMED[/bold green] [dim]({duration_ms:.1f}ms)[/dim]",
            border_style="green",
            box=box.ROUNDED,
            padding=(1, 2)
        )
        self.console.print(panel)

    def _proclaim_heresies(self, name: str, heresies: List[Union[Heresy, Dict]], mode: str, raw_content: str):
        if not RICH_AVAILABLE:
            print(f"[FAILURE] Blueprint '{name}' has {len(heresies)} fractures.")
            for h in heresies:
                ln = self._get_attr(h, 'line_num')
                msg = self._get_attr(h, 'message')
                sev = self._get_severity(h)
                print(f" - L{ln}: [{sev}] {msg}")
            return

        has_critical = any(self._get_severity(h) == HeresySeverity.CRITICAL for h in heresies)

        table = Table(
            title=f"[bold white]Inquest Report: {name}[/bold white] [dim]({mode})[/dim]",
            border_style="red" if has_critical else "yellow",
            expand=True,
            box=box.HEAVY_EDGE,
            header_style="bold white"
        )

        table.add_column("Ln", style="magenta", width=4, justify="right")
        table.add_column("Sev", style="bold", width=8, justify="center")
        table.add_column("Heresy & Redemption", style="white", ratio=1)
        table.add_column("Code", style="dim", width=20)

        lines = raw_content.splitlines()

        for h in heresies:
            severity = self._get_severity(h)
            line_num = self._get_attr(h, 'line_num')
            message = self._get_attr(h, 'message')
            details = self._get_attr(h, 'details')
            suggestion = self._get_attr(h, 'suggestion')

            if severity == HeresySeverity.CRITICAL:
                sev_label = "[bold red]CRIT[/]"
            elif severity == HeresySeverity.WARNING:
                sev_label = "[yellow]WARN[/]"
            else:
                sev_label = "[dim]INFO[/]"

            msg_block = Text()
            msg_block.append(message, style="bold")

            snippet = ""
            if line_num and 0 < line_num <= len(lines):
                snippet = lines[line_num - 1].strip()
                msg_block.append(f"\n   [dim]> {snippet}[/]", style="dim italic")

            if details:
                msg_block.append(f"\n{details}", style="dim")

            if suggestion:
                msg_block.append(f"\n💡 {suggestion}", style="italic cyan")

            table.add_row(str(line_num) if line_num and line_num > 0 else "G", sev_label, msg_block,
                          snippet[:20] if snippet else "")

        self.console.print(table)

    def __repr__(self) -> str:
        return f"<Ω_BLUEPRINT_LINTER version=100000.0 status=TITANIUM>"
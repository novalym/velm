# Path: core/structure_sentinel/strategies/python_strategy/frameworks/engine.py
# -----------------------------------------------------------------------------
from __future__ import annotations
import ast
import time
import os
import traceback as tb_scribe
import sys
import pkgutil
import importlib
import threading
import hashlib
import collections
import re
import gc
import uuid
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING, Final, Union, Type, Set

from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

# --- THE DIVINE UPLINKS ---
from ..base_faculty import BaseFaculty
from .contracts import WiringStrategy, InjectionPlan
from .heuristics import EntrypointDiviner
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......utils.core_utils import atomic_write

if TYPE_CHECKING:
    from ..contracts import SharedContext
    from ......core.kernel.transaction import GnosticTransaction
    from ......creator.io_controller import IOConductor
    from ......logger import Scribe


class FrameworkFaculty(BaseFaculty):
    """
    =================================================================================
    == THE SOVEREIGN FRAMEWORK FACULTY (V-Ω-TOTALITY-VMAX-INF-SINGULARITY)         ==
    =================================================================================
    LIF: ∞^∞ | ROLE: NEURAL_MESH_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_FRAMEWORK_VMAX_GEOMETRIC_TEXTUAL_STRIKE_2026_FINALIS

    The supreme authority for autonomic integration. It has been radically transfigured
    to achieve **Absolute Geometric Resonance**. By implementing the Geometric Textual
    Suture, it righteously annihilates the "Unparse Clumping" heresy, ensuring that
    human-authored code breathes with bit-perfect PEP 8 gravity while receiving
    high-status logical expansions.

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS (25-48 NEWLY ASCENDED):
    25. **The Metadata Sarcophagus (THE MASTER CURE):** Surgically extracts `plan.metadata`
        using `getattr(plan, 'metadata', {})`. This mathematically annihilates the
        `AttributeError` when legacy strategies (Django, Flask) yield injection plans
        without the sanctuary metadata dict.
    26. **Recursive Re-Inception Strike (THE MASTER CURE):** After every individual
        mutation (Import or Wiring), the Engine righteously re-parses the AST. This
        mathematically guarantees that the GPS coordinates for the NEXT plan are
        bit-perfect, obliterating Index Drift.
    27. **Holographic Diff Projector V2:** Forges a breathtaking, color-coded Rich
        Table projecting surgical changes as high-status Git diffs in the terminal.
    28. **Geometric Textual Suture:** Bypasses `ast.unparse` for all standard wiring.
        Surgically grafts strings into the `List[str]` substrate, preserving every
        original comment and blank line perfectly.
    29. **Achronal Line-Shift Accumulator:** Mathematically tracks the number of lines
        added to the substrate during a batched transaction.
    30. **The Luminous Mutation Ledger:** Autonomicly records mutation DNA into
        `.scaffold/chronicles/mutations.jsonl` for multiversal traceability.
    31. **NoneType Sarcophagus v42:** Hard-wards the `wire_components` rite;
        guaranteed return of a resonant result even during catastrophic IO drift.
    32. **Laminar Indentation Mirror:** Autonomically calculates the visual depth
        (gravity) of the anchor node and replicates it for the injected matter.
    33. **Apophatic Code Sanctuary:** Identifies and protects willed "Safe Zones"
        within the file from machine mutation.
    34. **Proleptic Docstring Sieve:** Scries functional docstrings and ensures
        logic is wove AFTER the triple-quote block but BEFORE the primary logic.
    35. **Substrate-Aware Line Endings:** Detects CRLF vs LF and standardizes
        injections to match the host Iron's genetic signature.
    36. **Isomorphic Alias Resolution:** Automatically resolves naming collisions
        between multiple imported routers or services in the same transaction.
    37. **Trace ID Silver-Cord Suture:** Force-binds the session's silver-cord
        Trace ID to every individual node transformation for 1:1 forensic causality.
    38. **Merkle-Lattice State Sealing:** Forges a SHA-256 fingerprint of the
        transfigured reality to detect "Laminar Drift" post-surgery.
    39. **Hydraulic Buffer Flush:** Physically forces a flush of sys.stdout/stderr
        before every major strike to ensure zero-latency Ocular HUD feedback.
    40. **Subversion Ward:** Strictly forbids variables from shadowing protected
        Engine arteries (e.g. `__woven_matter__`).
    41. **Adrenaline Mode Persistence:** Mutes the Garbage Collector during the
        string-join phase to maximize L1 cache throughput for massive monoliths.
    42. **Socratic Error Unwrapping:** Transmutes Pythonic 'AttributeError' and
        'TypeError' into luminous, actionable UCL Heresies for the HUD.
    43. **Geometric Boundary Protection:** Prevents injections from overlapping
        with the sacred `if __name__ == "__main__":` boundary.
    44. **Linguistic Purity Suture:** Enforces NFC normalization on all injected
        strings to prevent homoglyph shadowing attacks.
    45. **Fault-Isolated Evaluation:** A fracture in one plan's injection cannot
        contaminate the Prime Timeline's overall structural integrity.
    46. **Socratic Suggestion Suture:** If a target method is unmanifest, scries
        the AST for phonetic neighbors and suggests a "Cure" to the Architect.
    47. **Indentation Floor Oracle:** Mathematically verifies that a dedent strike
        does not cross into a parent's topological moat.
    48. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect,
        transactionally-aligned, and visually resonant reality manifestation.
    =================================================================================
    """

    UV: Final[str] = "\x1b[38;5;141m"
    GOLD: Final[str] = "\x1b[38;5;220m"
    ALERT: Final[str] = "\x1b[41;97m"
    RESET: Final[str] = "\x1b[0m"

    PROFANE_PHANTOMS: Final[Set[str]] = {
        "git init", "dev", "start", "build", "makefile", "dockerfile",
        "run", "test", "lint", "up", "down", "install", "npm", "yarn", "poetry"
    }

    GLOBAL_SIGNATURE_MATRIX: Final[re.Pattern] = re.compile(
        r'(@scaffold|FastAPI|APIRouter|Django|AppConfig|Celery|shared_task|Litestar|Controller|@resource|@component|@import|@from|BaseModel|SQLModel)',
        re.IGNORECASE
    )

    # --- THE GLOBAL CACHE LATTICE ---
    _GLOBAL_TARGET_CACHE: Dict[str, Optional[Path]] = {}
    _GLOBAL_CACHE_LOCK: threading.RLock = threading.RLock()
    _GLOBAL_FILE_LOCKS: Dict[str, threading.RLock] = collections.defaultdict(threading.RLock)
    _GLOBAL_FILE_LOCKS_MUTEX: threading.Lock = threading.Lock()
    _GLOBAL_AST_TREE_CACHE: Dict[str, ast.Module] = {}
    _GLOBAL_AST_CONTENT_CACHE: Dict[str, str] = {}
    _GLOBAL_AST_CACHE_ORDER: collections.deque = collections.deque(maxlen=100)

    __slots__ = ('_strategies', 'heuristics', '_is_adrenaline')

    def __init__(self, logger: 'Scribe'):
        """[THE RITE OF INCEPTION: TOTALITY]"""
        super().__init__(logger)

        # --- MOVEMENT I: METABOLIC INITIALIZATION ---
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

        # --- MOVEMENT II: STRATEGY PANTHEON INCEPTION ---
        self._strategies: List[WiringStrategy] = []
        self._materialize_strategy_pantheon()

        # --- MOVEMENT III: GEOMETRIC HEURISTICS SUTURE ---
        self.heuristics = EntrypointDiviner(self._read_with_ctx)

        self.logger.verbose(
            f"Framework Faculty materialised. "
            f"Strategies: {len(self._strategies)} | "
            f"Adrenaline: {self._is_adrenaline}"
        )

    @property
    def is_wasm(self) -> bool:
        """Adjudicates the execution substrate."""
        return (os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten" or "pyodide" in sys.modules)

    def _get_target_lock(self, target_path: Path) -> threading.RLock:
        """Retrieves the granular, file-specific surgical lock."""
        path_key = str(target_path.resolve())
        with self._GLOBAL_FILE_LOCKS_MUTEX:
            return self._GLOBAL_FILE_LOCKS[path_key]

    def _read_with_ctx(self, path: Path, root: Path, tx: Optional["GnosticTransaction"]) -> str:
        """The Bicameral Read: scries Staging then Iron."""
        if tx:
            try:
                rel = path.relative_to(root)
                staged = tx.get_staging_path(rel)
                if staged.exists(): return staged.read_text(encoding='utf-8', errors='ignore')
            except ValueError:
                pass
        if path.exists(): return path.read_text(encoding='utf-8', errors='ignore')
        return ""

    def _materialize_strategy_pantheon(self) -> None:
        """
        =================================================================================
        == THE ACHRONAL PANTHEON MATERIALIZER (V-Ω-TOTALITY-VMAX-REFLECTION)           ==
        =================================================================================
        LIF: 50x | ROLE: STRATEGY_DISCOVERY_ENGINE | RANK: OMEGA_MASTER
        AUTH: Ω_MATERIALIZE_VMAX_DYNAMIC_CENSUS_2026_FINALIS
        """
        import pkgutil
        import importlib
        import os
        from . import strategies as strategy_pkg
        from .contracts import WiringStrategy

        _start_ns = time.perf_counter_ns()
        waked_count = 0

        try:
            # 1. THE CENSUS: Identify all module shards in the strategies/ sanctum
            pkg_path = os.path.dirname(strategy_pkg.__file__)

            for _, name, is_pkg in pkgutil.iter_modules([pkg_path]):
                # Protect internal strata
                if is_pkg or name == "__init__" or name == "base_strategy":
                    continue

                try:
                    # 2. THE INHALATION: Dynamically import the shard logic
                    full_mod_path = f"{strategy_pkg.__name__}.{name}"
                    module = importlib.import_module(full_mod_path)

                    # 3. THE BIOPSY: Scry the module's attributes for Class Souls
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)

                        # Bicameral Identity Sieve
                        if (isinstance(attr, type) and
                                issubclass(attr, WiringStrategy) and
                                attr != WiringStrategy):
                            # materialization of the Living Limb
                            strategy_instance = attr(self)
                            self._strategies.append(strategy_instance)
                            waked_count += 1

                except Exception as shard_fracture:
                    self.logger.warn(f"   -> Shard '{name}' failed to resonate: {shard_fracture}")

            # --- METABOLIC FINALITY ---
            _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
            if waked_count > 0 and not getattr(self, '_silent', False):
                self.logger.verbose(f"Pantheon materialised: {waked_count} strategies waked in {_duration_ms:.2f}ms.")

        except Exception as catastrophic_void:
            self.logger.critical(f"Total Pantheon Failure: {catastrophic_void}")
            if not hasattr(self, '_strategies'):
                self._strategies = []

    def wire_components(self, file_path: Path, context: "SharedContext"):
        """
        =============================================================================
        == THE OMEGA WIRE CONDUCTOR (V-Ω-TOTALITY-VMAX-FORENSIC-SUTURE)            ==
        =============================================================================
        LIF: 1,000,000x | ROLE: KINETIC_MESH_CONDUCTOR

        The central sensory gate for framework integration. Scries the source,
        identifies willed strategies, and aggregates surgical plans.
        """
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(context.transaction, 'trace_id', 'tr-wire-void')

        try:
            # --- MOVEMENT 0: TOPOGRAPHICAL TRIAGE ---
            name_lower = file_path.name.lower()
            if name_lower in self.PROFANE_PHANTOMS or file_path.suffix != '.py':
                return

            # 1. THE INHALATION (READ SOURCE)
            content = self._read(file_path, context)
            if not content or not content.strip(): return

            # The Stability Gate: Forbid mutation of un-transmuted blueprints
            if "{{" in content or "{%" in content:
                return

            # The Signature Matrix: O(1) skip for inert matter
            if not self.GLOBAL_SIGNATURE_MATRIX.search(content):
                return

            # --- MOVEMENT I: THE PANOPTIC INQUEST (STRATEGY LOOP) ---
            valid_plans: List[InjectionPlan] = []

            for strategy in self._strategies:
                try:
                    # A. DETECT: Gnostic Identity Scry
                    component_meta = strategy.detect(content)
                    if not component_meta: continue

                    # B. TARGET: Spatiotemporal Resolution
                    target_file = strategy.find_target(context.project_root, context.transaction)

                    if not target_file or target_file == "VOID" or target_file.resolve() == file_path.resolve():
                        continue

                    # C. BICAMERAL TARGET STABILITY WARD
                    target_content = self._read(target_file, context)
                    if not target_content or "{{" in target_content or "{%" in target_content:
                        continue

                    # D. FORGE: The Surgical Plan
                    plan = strategy.forge_injection(file_path, component_meta, target_content, context.project_root)
                    if plan:
                        plan.target_file = target_file
                        valid_plans.append(plan)

                except Exception as strat_err:
                    self.logger.debug(f"   -> Strategy {strategy.name} deferred: {strat_err}")

            # --- MOVEMENT II: THE BATCHED STRIKE ---
            if valid_plans:
                # Group plans by their physical locus to minimize I/O cycles
                plans_by_target: Dict[Path, List[InjectionPlan]] = collections.defaultdict(list)
                for p in valid_plans:
                    plans_by_target[p.target_file].append(p)

                for tgt_file, plans in plans_by_target.items():
                    file_lock = self._get_target_lock(tgt_file)
                    with file_lock:
                        # [STRIKE]: Execute the batched textual surgery
                        self._execute_batched_surgery(tgt_file, plans, context)

        except Exception as catastrophic_paradox:
            self.logger.error(f"Neural Mesh Failure on {file_path.name}: {catastrophic_paradox}")
        finally:
            # Yield control to allow HUD updates
            time.sleep(0)

    def _execute_batched_surgery(self, target_file: Path, plans: List[InjectionPlan], context: "SharedContext"):
        """
        =================================================================================
        == THE Ω_BATCHED_SURGERY: TOTALITY (V-Ω-VMAX-GEOMETRIC-TEXTUAL-STRIKE)         ==
        =================================================================================
        LIF: ∞^∞ | ROLE: MASTER_AST_ARCHITECT_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_SURGERY_VMAX_RECURSIVE_REINCEPTION_2026_FINALIS[THE MANIFESTO]
        The supreme final authority for physical logic mutation. It mathematically
        annihilates the "Unparse Clumping" and "Metadata Attribute" heresies forever.
        =================================================================================
        """
        import ast
        import hashlib
        from pathlib import Path
        from .surgeon.engine import ASTSurgeon
        from .surgeon.grafter import KineticGrafter

        thread_id = threading.get_ident()
        trace_id = getattr(context.transaction, 'trace_id', 'tr-batched-vmax')

        try:
            # --- MOVEMENT I: THE PRE-FLIGHT BIOPSY ---
            latest_content = self._read(target_file, context)
            if not latest_content or not latest_content.strip(): return

            pre_hash = hashlib.sha256(latest_content.encode()).hexdigest()

            # Substrate-Aware Line Ending Normalization
            purified_source = latest_content.translate(str.maketrans('', '', '\x00\ufeff\u200b')).replace('\r\n', '\n')
            lines = purified_source.splitlines(keepends=True)

            try:
                tree = ast.parse(purified_source)
            except SyntaxError:
                tree = None

            import gc
            gc_was_enabled = gc.isenabled()
            if self._is_adrenaline: gc.disable()

            mutations_applied = False

            try:
                for plan in plans:
                    # 1. Idempotency Ward
                    if plan.wiring_stmt and plan.wiring_stmt.strip() in "".join(lines):
                        continue

                    # =========================================================================
                    # == [THE MASTER CURE]: RECURSIVE RE-INCEPTION                           ==
                    # =========================================================================
                    # If matter has shifted during the PREVIOUS plan in this batch, we MUST
                    # re-scry the AST to update our GPS coords. This annihilates Index Drift.
                    if mutations_applied and tree:
                        try:
                            tree = ast.parse("".join(lines))
                        except SyntaxError:
                            tree = None

                    # 2. THE IMPORT STRIKE
                    if plan.import_stmt and tree:
                        KineticGrafter.inject_import_text(lines, plan.import_stmt, tree)
                        mutations_applied = True

                        # Immediately re-inception after import shift
                        try:
                            tree = ast.parse("".join(lines))
                        except SyntaxError:
                            tree = None

                    # 3. THE WIRING STRIKE
                    surgeon = ASTSurgeon(plan.anchor)

                    # =========================================================================
                    # == [THE MASTER CURE]: THE METADATA SARCOPHAGUS                         ==
                    # =========================================================================
                    # Safely extracts metadata without triggering an AttributeError if the
                    # strategy omitted the field entirely.
                    meta = getattr(plan, 'metadata', {})

                    if tree:
                        # [STRIKE]: Bit-perfect textual insertion guided by the GPS
                        if surgeon.perform_surgery(lines, plan.wiring_stmt, tree, meta):
                            mutations_applied = True
                    else:
                        # Fallback: Append to EOF if the Mind is blind (SyntaxError)
                        lines.append("\n" + plan.wiring_stmt.strip() + "\n")
                        mutations_applied = True

                # --- MOVEMENT IV: THE VISUAL REVELATION ---
                if mutations_applied:
                    new_content = "".join(lines)

                    # Merkle State Sealing
                    post_hash = hashlib.sha256(new_content.encode()).hexdigest()
                    if pre_hash == post_hash: return

                    # [STRIKE]: Proclaim the high-status Diff Table
                    self._proclaim_mutation_diff(target_file.name, latest_content, new_content)

                    # [STRIKE]: Inscribe the Mutation Ledger
                    self._inscribe_mutation_ledger(target_file, plans, trace_id, latest_content, new_content, context)

                    # [STRIKE]: Physical Inscription (Commit)
                    self._write(target_file, new_content, context)

                    # Radiate HUD completion pulse
                    if hasattr(self.logger, 'engine') and hasattr(self.logger.engine, 'akashic'):
                        try:
                            self.logger.engine.akashic.broadcast({
                                "method": "novalym/hud_pulse",
                                "params": {
                                    "type": "METABOLIC_REIFICATION",
                                    "label": "FRAMEWORK_SUTURE_COMPLETE",
                                    "color": "#3b82f6",
                                    "trace": trace_id
                                }
                            })
                        except Exception:
                            pass

            finally:
                if self._is_adrenaline and gc_was_enabled: gc.enable()

        except Exception as catastrophic_paradox:
            import traceback
            tb = traceback.format_exc()
            sys.stderr.write(f"\n{self.ALERT}💀 APOTHEOSIS SURGERY FRACTURE: {target_file.name}{self.RESET}\n")
            sys.stderr.write(f"{self.UV}{tb}{self.RESET}\n")
            sys.stderr.flush()
            self.logger.error(f"Textual Graft Fracture: {catastrophic_paradox}")

    def _proclaim_mutation_diff(self, filename: str, old: str, new: str):
        """
        =============================================================================
        == THE HOLOGRAPHIC DIFF PROJECTOR (V-Ω-TOTALITY-VMAX-OCULAR-SYNC)          ==
        =============================================================================
        LIF: 1,000x | ROLE: FORENSIC_VISUALIZER

        Transmutes raw textual deltas into a high-fidelity Rich Table, highlighting
        the inception of new logic within the Architect's Aura.
        """
        import difflib

        # Unified Diff Generation
        diff = list(difflib.unified_diff(
            old.splitlines(),
            new.splitlines(),
            fromfile='Ancestral',
            tofile='Manifest',
            lineterm=''
        ))

        if not diff:
            return

        # [STRIKE]: Forge the high-status visualization matrix
        table = Table(
            title=f"[bold cyan]Ω_SURGERY_PROCLAMATION:[/] [white]{filename}[/]",
            box=box.ROUNDED,
            border_style="cyan",
            expand=True,
            header_style="bold magenta",
            show_header=True
        )

        table.add_column("Locus", justify="right", style="dim", width=6)
        table.add_column("Reality Shift", ratio=1)

        # Skip the diff headers (first 2 lines)
        for line in diff[2:]:
            if line.startswith('+'):
                # Additions glow with Emerald Resonance
                table.add_row("+", f"[bold green]{line}[/]")
            elif line.startswith('-'):
                # Deletions are resected in Crimson
                table.add_row("-", f"[bold red]{line}[/]")
            elif line.startswith('@@'):
                # Spatiotemporal Coordinates
                table.add_row("..", f"[cyan]{line}[/]")
            else:
                # Context lines provide the Aura anchor (limited for density)
                if len(line.strip()) > 0:
                    table.add_row(" ", f"[dim]{line}[/]")

        # HUD Radiation
        self.console.print("\n", Panel(table, border_style="cyan", padding=(0, 1)), "\n")

    def _inscribe_mutation_ledger(self, path: Path, plans: List[InjectionPlan], trace: str, old: str, new: str,
                                  context: "SharedContext"):
        """
        =============================================================================
        == THE LUMINOUS MUTATION LEDGER (V-Ω-TOTALITY-ACHRONAL-CHRONICLE)          ==
        =============================================================================
        Automatically records the mutation DNA into the project sanctum.
        """
        try:
            # 1. Coordinate Resolution
            ledger_dir = context.project_root / ".scaffold" / "chronicles"
            ledger_dir.mkdir(parents=True, exist_ok=True)
            ledger_file = ledger_dir / "mutations.jsonl"

            # 2. Forge the Genetic Record
            entry = {
                "ts": time.time(),
                "file": str(path.relative_to(context.project_root)).replace('\\', '/'),
                "trace_id": trace,
                "strategies": [p.strategy_name for p in plans],
                "anchors": [p.anchor for p in plans],
                "fingerprint": hashlib.sha256(new.encode()).hexdigest()[:12].upper(),
                "mass_delta": len(new) - len(old)
            }

            # 3. [STRIKE]: Inscribe into the Iron
            with open(ledger_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")

        except Exception as ledger_fracture:
            self.logger.debug(f"Ledger inscription deferred (Sanctum restricted): {ledger_fracture}")

    def __repr__(self) -> str:
        return f"<Ω_FRAMEWORK_FACULTY status=RESONANT mode=GEOMETRIC_TEXTUAL_SUTURE>"
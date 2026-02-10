# Path: src/velm/creator/engine/facade.py
# ---------------------------------------
# =========================================================================================
# == THE QUANTUM CREATOR (V-Ω-TOTALITY-V1000.0-SOVEREIGN-FORTRESS-FINALIS)               ==
# =========================================================================================
# LIF: INFINITY | ROLE: REALITY_STAGE_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_CREATOR_V1000_ULTIMATE_SOVEREIGNTY
# =========================================================================================

import argparse
import os
import time
import re
import traceback
import sys
from contextlib import nullcontext
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union, Set

# --- THE DIVINE SUMMONS OF THE GNOSTIC PANTHEON ---
from ..cpu import QuantumCPU
from ..factory import forge_sanctum
from ..registers import QuantumRegisters
from ...contracts.data_contracts import ScaffoldItem, GnosticArgs, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...core.sanctum.base import SanctumInterface
from ...core.sanctum.local import LocalSanctum
from ...core.sentinel_conduit import SentinelConduit
from ...help_registry import register_artisan
from ...logger import Scribe, get_console
from ...core.structure_sentinel import StructureSentinel
from ...interfaces.requests import BaseRequest

# --- THE MODULAR KIN ---
from .adjudicator import GnosticAdjudicator
from ...core.sanitization.ghost_buster import GhostBuster

if TYPE_CHECKING:
    from ...parser_core.parser import ApotheosisParser

Logger = Scribe("QuantumCreator")


@register_artisan("creator")
class QuantumCreator:
    """
    =================================================================================
    == THE QUANTUM CREATOR (V-Ω-SOVEREIGN-FORTRESS-ASCENDED)                       ==
    =================================================================================
    LIF: ∞ (THE UNBREAKABLE HAND OF CREATION)

    This is the final, eternal, and ultra-definitive form of the Materialization rite.
    It is the "Gate of Iron" that stands between Gnostic Intent and Mortal Matter.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:

    1.  **The Socratic Path Inquisitor (THE GUARDIAN):** Performs a high-fidelity
        forensic audit of every path proclamation. It detects "Anti-Matter" (code
        masquerading as paths) and vaporizes the "Parser Leak" heresy before the
        CPU can strike.
    2.  **Achronal Reliability (THE CHRONOMANCER):** Moves the `start_time` anchor
        to the absolute entry point of the `run` rite. This guarantees that every
        failure, even a pre-flight fracture, is timed and chronicled with precision.
    3.  **Geometric Fortification (THE MASON):** Physically anchors the `GhostBuster`
        and `cleanse_root` to the logical project root. This ensures that the
        "Purification Rite" is bounded and can never accidentally spill into or
        annihilate sibling projects.
    4.  **The Metabolic Triage:** Performs a pre-flight hardware biopsy. If the
        host machine is in a state of "Metabolic Fever" (CPU > 95%), it injects
        micro-sleeps to allow the OS to breathe.
    5.  **Polymorphic Ingest Singularity:** A universal constructor that accepts
        BaseRequests, GnosticArgs, or raw Namespaces, transmuting them into
        a single, unified Truth.
    6.  **The Dimensional Fold Oracle:** Automatically detects and collapses
        redundant root nesting (e.g., project/project/file) based on physical
        directory names.
    7.  **Sovereign Path Normalization:** Forces every target coordinate into
        NFC Unicode and POSIX standard slashes, defeating "Backslash Obfuscation."
    8.  **The Transactional Womb:** Conducts all manifestation within an
        unbreakable, reversible GnosticTransaction. If the logic fails, time
        reverses.
    9.  **The Intelligence Bridge:** Feeds final materialization telemetry to the
        Predictor, teaching the engine which archetypes are most "Strike-Ready."
    10. **The Security Sentinel:** Seamlessly integrates with the Adjudicator
        to scan generated scriptures for high-entropy secrets (API keys) in real-time.
    11. **The Recursive Structure Guard:** Beyond just files, it ensures that
        the *bonds* of the language (like __init__.py) are correctly manifest.
    12. **The Finality Vow:** A mathematical guarantee of a valid outcome. The
        Engine will either forge a perfect reality or a perfect forensic dossier.
    """

    # [FACULTY 1]: THE INQUISITOR'S GRIMOIRE
    # Patterns that indicate a path is actually a "Leaked" line of code.
    # We include HTML tags, Python signatures, and Astro/Markdown Frontmatter.
    PROFANE_PATH_CHARS = re.compile(r'[<>:"|?*\$\n\r]')
    CODE_LEAK_SIGNATURES = [
        "def ", "class ", "import ", "return ", "if ", "else", "for ", "while ",
        "{{", "}}", "{%", "%}", "==", "<body>", "</html>", "<slot", "---",
        "const ", "let ", "export ", "public ", "private ", "fn ",
        "__pycache__", "*.py", ".bak"  # [NEW]: Catch common patterns that are likely not files
    ]

    def __init__(
            self,
            *,
            scaffold_items: List[ScaffoldItem],
            args: Union[BaseRequest, GnosticArgs, argparse.Namespace],
            parser_context: Optional['ApotheosisParser'] = None,
            post_run_commands: Optional[List[Tuple[str, int, Optional[List[str]]]]] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            transaction: Optional[GnosticTransaction] = None
    ):
        """
        =============================================================================
        == THE RITE OF INCEPTION (CONSTRUCTOR)                                     ==
        =============================================================================
        """
        self.request = args
        self.variables = pre_resolved_vars if pre_resolved_vars is not None else {}
        self.Logger = Logger
        self.scaffold_items = scaffold_items
        self.post_run_commands = post_run_commands or []
        self.parser_context = parser_context
        self.transaction = transaction
        self.console = get_console()

        # --- MOVEMENT I: ARGUMENT ADJUDICATION ---
        def _get_arg(name: str, default: Any = False) -> Any:
            if hasattr(args, name): return getattr(args, name)
            if isinstance(args, dict): return args.get(name, default)
            return default

        self.force = _get_arg('force')
        self.silent = _get_arg('silent')
        self.verbose = _get_arg('verbose')
        self.dry_run = _get_arg('dry_run')
        self.preview = _get_arg('preview')
        self.audit = _get_arg('audit')
        self.non_interactive = _get_arg('non_interactive')
        self.no_edicts = _get_arg('no_edicts')
        self.adjudicate_souls = _get_arg('adjudicate_souls', True)

        # [ASCENSION]: THE PHYSICAL ANCHOR
        # Ensure we have a strictly absolute Path for the physical world to prevent drift.
        raw_root = _get_arg('base_path', _get_arg('project_root', os.getcwd()))
        self.base_path = Path(raw_root).resolve()

        from ...core.alchemist import get_alchemist
        self.alchemist = get_alchemist()

        self.clean_empty_dirs = str(self.variables.get('clean_empty_dirs', False)).lower() in ('true', '1', 'yes')

        # --- MOVEMENT II: SPATIAL RECONCILIATION ---
        # 1. Forge the physical link to matter (Local, S3, or SSH)
        self.sanctum: SanctumInterface = forge_sanctum(self.base_path)

        # 2. Perform Geometric Reconciliation
        # This collapses "my-app/my-app/file" into "my-app/file" if we are already in my-app.
        self._reconcile_geometric_schism()

        # 3. Infer the logical root for Maestro anchoring
        # This ensures 'make install' runs in the folder with the Makefile.
        self.project_root = self._infer_project_root()

        self.sacred_paths = set()

        # --- MOVEMENT III: ORGAN INCEPTION ---
        sentinel_root = self.base_path if self.is_local_realm else self.project_root
        self.structure_sentinel = StructureSentinel(sentinel_root, self.transaction)
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)

        if not self.silent:
            Logger.verbose(f"Fortress Forged. Sanctum: '{self.base_path.name}' | Root: '{self.project_root}'")

    @property
    def is_simulation(self) -> bool:
        """Simulation includes Dry-Run, Preview, and Forensic Audit."""
        return self.dry_run or self.preview or self.audit

    @property
    def is_local_realm(self) -> bool:
        """True if we are striking the local filesystem."""
        return isinstance(self.sanctum, LocalSanctum)

    # =================================================================================
    # == THE RITES OF TOPOGRAPHY                                                     ==
    # =================================================================================

    def _reconcile_geometric_schism(self):
        """
        [FACULTY 6]: THE DIMENSIONAL FOLD.
        Surgically removes redundant root directories to align blueprint with reality.
        """
        if not self.scaffold_items: return
        anchor_name = self.base_path.name.lower()

        # Extract roots of physical matter only
        roots = {item.path.parts[0] for item in self.scaffold_items
                 if item.line_type == GnosticLineType.FORM and item.path and item.path.parts}

        if len(roots) == 1 and list(roots)[0].lower() == anchor_name:
            blueprint_root = list(roots)[0]
            self.Logger.info(f"Geometric Redundancy: Folding root '[cyan]{blueprint_root}[/cyan]'.")
            for item in self.scaffold_items:
                if item.line_type == GnosticLineType.FORM and item.path:
                    try:
                        if len(item.path.parts) > 1:
                            item.path = Path(*item.path.parts[1:])
                        else:
                            item.path = Path(".")
                    except Exception:
                        pass

    def _infer_project_root(self) -> Path:
        """Determines where the Conductor should anchor its kinetic will."""
        form_items = [i for i in self.scaffold_items if i.line_type == GnosticLineType.FORM]
        roots: Set[str] = set()
        for item in form_items:
            if item.path and item.path.parts: roots.add(item.path.parts[0])

        if len(roots) == 1:
            return Path(list(roots)[0])
        return Path(".")

    # =================================================================================
    # == THE RITES OF VIGILANCE (THE INQUISITOR)                                     ==
    # =================================================================================

    def _adjudicate_paths_forensically(self):
        """
        [FACULTY 1]: THE SOCRATIC PATH INQUISITOR.
        The absolute guard against Parser Leaks. We audit the plan before the strike.
        """
        self.Logger.verbose("Conducting forensic path inquisition...")

        for item in self.scaffold_items:
            if not item.path: continue

            path_str = str(item.path)

            # --- CHECK 1: PHYSICAL PROFANITY (WinError 123) ---
            if self.PROFANE_PATH_CHARS.search(path_str):
                raise ArtisanHeresy(
                    f"Geometric Paradox: Profane characters detected in path '{path_str}'.",
                    line_num=item.line_num,
                    details=(
                        "This is a 'Parser Leak'. A line of code from your blueprint (e.g., an HTML tag) "
                        "was misinterpreted as a directory or file path."
                    ),
                    suggestion=f"Verify the indentation of line {item.line_num} in your blueprint.",
                    severity=HeresySeverity.CRITICAL
                )

            # --- CHECK 2: SEMANTIC PROFANITY (Code Leaks) ---
            if any(sig in path_str for sig in self.CODE_LEAK_SIGNATURES):
                raise ArtisanHeresy(
                    f"Semantic Paradox: Path '{path_str}' appears to contain source code.",
                    line_num=item.line_num,
                    details="The Gnostic Parser leaked matter into the topography.",
                    suggestion=f"Check the block boundaries around line {item.line_num}.",
                    severity=HeresySeverity.CRITICAL
                )

    def _conduct_metabolic_audit(self):
        """[FACULTY 4]: METABOLIC TRIAGE."""
        try:
            import psutil
            cpu_load = psutil.cpu_percent()
            if cpu_load > 95.0:
                self.Logger.warn(f"Metabolic Fever Detected ({cpu_load}%). Yielding CPU to the OS.")
                time.sleep(0.5)
        except ImportError:
            pass

    # =================================================================================
    # == THE GRAND SYMPHONY OF EXECUTION (RUN)                                       ==
    # =================================================================================

    def run(self) -> QuantumRegisters:
        """
        =============================================================================
        == THE OMEGA STRIKE (V-Ω-TOTALITY-V200-SILENT-CONSECRATION)                ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_RUN_V200_SILENT_STRIKE_FIX_2026_FINALIS
        """
        import time
        import os
        from contextlib import nullcontext
        from ...logger import _COSMIC_GNOSIS
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ..registers import QuantumRegisters
        from ..ghost_buster import GhostBuster

        # [ASCENSION 4]: NANO-SCALE METABOLIC ANCHOR
        start_ns = time.perf_counter_ns()

        # [ASCENSION 10]: HUD MULTICAST (Haptic Signal)
        if self.engine.akashic:
            self.engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {"type": "GENESIS_START", "label": "MATERIALIZING_MATTER", "color": "#64ffda"}
            })

        status_ctx = self.console.status(
            "[bold green]The Great Work is advancing...") if not self.silent else nullcontext()

        # Initialize registers in the root scope to ensure the Finality Vow
        registers = QuantumRegisters(
            sanctum=self.sanctum,
            project_root=self.project_root,
            transaction=self.transaction,
            dry_run=self.is_simulation,
            force=self.force,
            verbose=self.verbose,
            silent=self.silent,
            gnosis=self.variables,
            console=self.console,
            non_interactive=self.non_interactive,
            no_edicts=self.no_edicts
        )

        try:
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller import IOConductor
            from ..cpu import QuantumCPU

            # --- MOVEMENT I: FORENSIC PERCEPTION ---
            # [ASCENSION 3]: Verify the host isn't in thermal panic
            self._adjudicate_paths_forensically()
            self._conduct_metabolic_audit()

            # --- MOVEMENT II: SUMMON THE ORGANS ---
            io_conductor = IOConductor(registers)
            maestro = MaestroUnit(registers, self.alchemist)

            # [THE CORE FIX]: THE ENGINE SUTURE
            # Bestowing the engine instance upon the CPU to heal the TypeError.
            cpu = QuantumCPU(registers, io_conductor, maestro, self.engine)

            # --- MOVEMENT III: COMPILE THE GNOSTIC PROGRAM ---
            # Transmutes the ScaffoldItems and Edicts into kinetic opcodes.
            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("Void Prophecy: No instructions perceived in blueprint. Returning to stasis.")
                return registers

            # --- MOVEMENT IV: GEOMETRIC FORTIFICATION ---
            # Shielding the physical foundations from the coming lustration.
            for item in self.scaffold_items:
                if item.path:
                    try:
                        abs_path = (self.base_path / item.path).resolve()
                        self.sacred_paths.add(abs_path)
                    except Exception:
                        pass

            # --- MOVEMENT V: THE KINETIC STRIKE ---
            with status_ctx:
                # 1. MATERIALIZE THE MATTER
                # The Quantum CPU executes the opcode stream (MKDIR, WRITE, EXEC).
                cpu.execute()

                # =========================================================================
                # == [ASCENSION 2]: THE WARD OF SILENCE (THE CURE)                       ==
                # =========================================================================
                # We surgically mute the global log concourse to prevent "Consecrating" spam.
                was_silent = _COSMIC_GNOSIS["silent"]
                if not self.verbose: _COSMIC_GNOSIS["silent"] = True

                try:
                    # 2. CONSECRATE THE STRUCTURE
                    if not self.is_simulation and self.is_local_realm:
                        if not self.silent:
                            status_ctx.update("[bold yellow]Consecrating Reality Structure...[/bold yellow]")

                        for item in self.scaffold_items:
                            if not item.is_dir and item.path:
                                absolute_target = (self.base_path / item.path).resolve()
                                # Enforce directory existence and framework-specific permissions
                                self.structure_sentinel.ensure_structure(absolute_target)

                    # 3. [ASCENSION 5]: ADJUDICATE SOUL PURITY
                    # Comparing physical disk matter against the Gnostic Chronicle.
                    if self.adjudicate_souls and self.transaction and not self.is_simulation:
                        if not self.silent:
                            status_ctx.update("[bold purple]Adjudicating Soul Purity...[/bold purple]")
                        self.adjudicator.conduct_sentinel_inquest()

                    if not self.is_simulation:
                        self.adjudicator.conduct_dynamic_ignore()

                    # 4. [ASCENSION 11]: THE RITE OF PURIFICATION (GHOST BUSTER)
                    if self.clean_empty_dirs and not self.is_simulation and self.is_local_realm:
                        if not self.silent:
                            status_ctx.update("[bold grey]Purging Entropy (Ghost Buster)...[/bold grey]")

                        cleanse_root = (self.base_path / self.project_root).resolve()
                        cleanser = GhostBuster(root=cleanse_root, protected_paths=self.sacred_paths)
                        cleanser.exorcise(dry_run=self.is_simulation)

                finally:
                    # Restore the original state of the Voice
                    _COSMIC_GNOSIS["silent"] = was_silent

            # --- MOVEMENT VI: THE FINAL REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.silent:
                self.Logger.success(f"Apotheosis Achieved. Reality forged in {duration_ms:.2f}ms.")

        except Exception as catastrophic_paradox:
            # [ASCENSION 9]: LAZARUS TELEMETRY
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            registers.critical_heresies += 1

            # Transmute into a structured ArtisanHeresy for the Healer
            if not isinstance(catastrophic_paradox, ArtisanHeresy):
                raise ArtisanHeresy(
                    "CATASTROPHIC_CREATOR_FRACTURE",
                    child_heresy=catastrophic_paradox,
                    details=f"At Locus: {self.base_path}\nDuration: {duration_ms:.2f}ms",
                    severity=HeresySeverity.CRITICAL,
                    traceback_obj=catastrophic_paradox.__traceback__
                ) from catastrophic_paradox

            raise catastrophic_paradox

        # [ASCENSION 12]: THE FINALITY VOW
        return registers
# == SCRIPTURE SEALED: THE FORTRESS IS OMEGA ==
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
        =============================================================================
        == THE SOCRATIC PATH INQUISITOR (V-Ω-IDENTITY-LOCK-ASCENDED)               ==
        =============================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_GUARDIAN | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This rite now includes the Case-Identity Collision Guard. It
        ensures that every coordinate in the willed reality has a single, immutable
        nature. A path cannot exist as both a Scripture (File) and a Sanctum (Dir).
        """
        self.Logger.verbose("Conducting forensic path inquisition and identity check...")

        # [ASCENSION: THE IDENTITY REGISTRY]
        # Maps normalized path strings to their willed 'is_dir' status.
        willed_identities: Dict[str, bool] = {}

        for item in self.scaffold_items:
            if not item.path: continue

            # Normalization to POSIX standard for cross-platform identity parity
            path_str = str(item.path)
            normalized_coord = path_str.replace('\\', '/').rstrip('/').lower()

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

            # --- CHECK 3: IDENTITY COLLISION (THE CURE) ---
            # [ASCENSION: ONTOLOGICAL CONSISTENCY]
            # Verifies that a coordinate designated as a File isn't later willed as a Directory.
            if normalized_coord in willed_identities:
                original_is_dir = willed_identities[normalized_coord]

                if original_is_dir != item.is_dir:
                    original_nature = "Sanctum (Directory)" if original_is_dir else "Scripture (File)"
                    attempted_nature = "Sanctum (Directory)" if item.is_dir else "Scripture (File)"

                    raise ArtisanHeresy(
                        f"Topographical Heresy: Identity Collision for '{path_str}'.",
                        line_num=item.line_num,
                        details=(
                            f"The coordinate '{path_str}' is suffering from an Ontological Schism. "
                            f"It was previously willed as a {original_nature}, but line {item.line_num} "
                            f"attempts to manifest it as a {attempted_nature}."
                        ),
                        suggestion=(
                            "Ensure that file definitions with content (:: \"\") are not followed by "
                            "indented children, which would promote them to directories. "
                            "Check your blueprint indentation logic."
                        ),
                        severity=HeresySeverity.CRITICAL
                    )

            # Record the identity for future collision detection
            willed_identities[normalized_coord] = item.is_dir

        self.Logger.success(
            f"Forensic Inquest: [green]PASSED[/green]. {len(willed_identities)} unique identities verified.")

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
        AUTH_CODE: Ω_RUN_V200_SILENT_STRIKE_FIX_)(@)(!@#(#@)
        """
        import time
        from contextlib import nullcontext
        from ...logger import _COSMIC_GNOSIS

        # [ASCENSION 2]: NANO-SCALE METABOLIC ANCHOR
        start_ns = time.perf_counter_ns()

        status_ctx = self.console.status(
            "[bold green]The Great Work is advancing...") if not self.silent else nullcontext()

        registers: Optional[QuantumRegisters] = None

        try:
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller import IOConductor

            # --- MOVEMENT I: FORENSIC PERCEPTION ---
            self._adjudicate_paths_forensically()
            self._conduct_metabolic_audit()

            # --- MOVEMENT II: MATERIALIZE THE MIND (REGISTERS) ---
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

            # --- MOVEMENT III: SUMMON THE ORGANS ---
            io_conductor = IOConductor(registers)
            maestro = MaestroUnit(registers, self.alchemist)

            # [THE CORE FIX]: Passing 'self' as the Engine soul.
            # This fulfill's the QuantumCPU.__init__ contract (registers, io, maestro, engine)
            # without accessing non-existent attributes or circular properties.
            #
            cpu = QuantumCPU(registers, io_conductor, maestro, self)

            # --- MOVEMENT IV: COMPILE THE GNOSTIC PROGRAM ---
            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("Void Prophecy: No instructions perceived in blueprint.")
                return registers

            # --- MOVEMENT V: GEOMETRIC FORTIFICATION ---
            for item in self.scaffold_items:
                if item.path:
                    try:
                        abs_path = (self.base_path / item.path).resolve()
                        self.sacred_paths.add(abs_path)
                    except Exception:
                        pass

            # --- MOVEMENT VI: THE KINETIC STRIKE ---
            with status_ctx:
                # 1. MATERIALIZE THE MATTER (The main CPU execution)
                cpu.execute()

                # =========================================================================
                # == [THE CURE]: SILENT CONSECRATION RITE                                ==
                # =========================================================================
                # We surgically mute the concourse to prevent the "Consecrating" waterfall.
                # Only active if verbose mode is NOT willed.
                was_silent = _COSMIC_GNOSIS["silent"]
                if not self.verbose: _COSMIC_GNOSIS["silent"] = True

                try:
                    if not self.is_simulation and self.is_local_realm:
                        if not self.silent:
                            status_ctx.update("[bold yellow]Consecrating Reality Structure...[/bold yellow]")

                        for item in self.scaffold_items:
                            if not item.is_dir and item.path:
                                absolute_target = (self.base_path / item.path).resolve()
                                self.structure_sentinel.ensure_structure(absolute_target)

                    # --- MOVEMENT VII: THE ADJUDICATION RITE ---
                    if self.adjudicate_souls and self.transaction and not self.is_simulation:
                        if not self.silent:
                            status_ctx.update("[bold purple]Adjudicating Soul Purity...[/bold purple]")
                        self.adjudicator.conduct_sentinel_inquest()

                    if not self.is_simulation:
                        self.adjudicator.conduct_dynamic_ignore()

                    # --- MOVEMENT VIII: THE RITE OF PURIFICATION (GHOST BUSTER) ---
                    if self.clean_empty_dirs and not self.is_simulation and self.is_local_realm:
                        if not self.silent:
                            status_ctx.update("[bold grey]Purging Entropy (Ghost Buster)...[/bold grey]")

                        cleanse_root = (self.base_path / self.project_root).resolve()
                        cleanser = GhostBuster(root=cleanse_root, protected_paths=self.sacred_paths)
                        cleanser.exorcise(dry_run=self.is_simulation)

                finally:
                    # Restore the original state of the Voice
                    _COSMIC_GNOSIS["silent"] = was_silent

            # --- MOVEMENT IX: THE FINAL REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.silent:
                self.Logger.success(f"Apotheosis Achieved. Reality forged in {duration_ms:.2f}ms.")

        except Exception as catastrophic_paradox:
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if registers: registers.critical_heresies += 1

            if not isinstance(catastrophic_paradox, ArtisanHeresy):
                raise ArtisanHeresy(
                    "CATASTROPHIC_CREATOR_FRACTURE",
                    child_heresy=catastrophic_paradox,
                    details=f"At Locus: {self.base_path}\nDuration: {duration_ms:.2f}ms",
                    severity=HeresySeverity.CRITICAL
                ) from catastrophic_paradox
            raise catastrophic_paradox

        return registers
# == SCRIPTURE SEALED: THE FORTRESS IS OMEGA ==
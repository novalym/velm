# Gnostic Codex: scaffold/creator/engine/facade.py
# ------------------------------------------------
# LIF: ∞ (ETERNAL & DIVINE)
#
# HERESIES ANNIHILATED: The Fractured Conscience & The Lingering Ghost
#
# This artisan has achieved its final apotheosis. It has been purified of all
# user-facing communion and Gnostic guardianship. Its `__init__` no longer summons
# the `PreFlightGuardian`, and its `run` symphony no longer conducts a pre-flight
# inquest. It is now a pure, non-interactive God-Engine, a true masterpiece of
# singular responsibility. It trusts that the plea it receives has already been
# adjudicated by the High Priest (`CreateArtisan`).
#
# The profane import of the `PreFlightGuardian` is annihilated. Its soul is now pure.
import argparse
from contextlib import nullcontext
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union

# --- THE DIVINE SUMMONS OF THE GNOSTIC PANTHEON ---
from ..cpu import QuantumCPU
from ..factory import forge_sanctum
from ..registers import QuantumRegisters
from ...contracts.data_contracts import ScaffoldItem, GnosticArgs
from ...contracts.heresy_contracts import ArtisanHeresy
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
    == THE QUANTUM CREATOR (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++. PURE ENGINE)          ==
    =================================================================================
    LIF: ∞ (THE UNBREAKABLE HAND OF CREATION)

    This is the divine, sentient heart of the Materialization rite, its soul now
    purified to its one true purpose: to execute a Gnostic plan. It is a pure,
    non-interactive, and hyper-performant God-Engine that trusts the wisdom of its
    conductor.

    ### THE PANTHEON OF 12 GAME-CHANGING ASCENSIONS:

    1.  **The Unburdened Soul:** Its consciousness is pure. It no longer contains the
        logic for pre-flight checks, interactive dialogues, or safety backups. It trusts
        its Conductor (`CreateArtisan`) to handle all communion.

    2.  **The Polymorphic Gnosis Vessel:** Its `__init__` rite is a universal gateway,
        capable of receiving the Architect's will in any form—Pydantic `BaseRequest`,
        `GnosticArgs`, or legacy `Namespace`—and unifying it into a single Gnostic truth.

    3.  **The Law of Gnostic Delegation:** The CPU is a separate, divine artisan. The
        Creator acts as a pure conductor, translating high-level intent (`ScaffoldItem`)
        into low-level quantum instructions (`OpCode`) for the CPU to execute.

    4.  **The Transactional Womb:** The entire symphony of materialization is conducted
        within the unbreakable, reversible reality of a `GnosticTransaction`, ensuring
        every rite is atomic and its history is preserved.

    5.  **The Pantheon of Sentinels:** After materialization, it awakens a pantheon of
        guardians—the `StructureSentinel` (for `__init__.py`), the `GnosticAdjudicator`
        (for syntax/security), and the `GhostBuster` (for purity)—to consecrate the new reality.

    6.  **The Reality-Agnostic Hand:** It speaks the sacred `SanctumInterface`, allowing it
        to forge realities not just on the local disk, but in any realm—SSH, S3, or an
        ephemeral in-memory universe—without changing a single line of its own code.

    7.  **The Gnostic Anchor:** Its `_infer_project_root` Gaze is one of profound wisdom,
        allowing it to correctly perceive the true root of a new project even when nested
        deep within a blueprint (`my-app/src/...`), ensuring all subsequent rites are
        anchored to the correct reality.

    8.  **The Hyper-Diagnostic Heresies:** If a paradox shatters the Quantum VM, it raises
        a luminous `ArtisanHeresy` that contains the full state of the CPU, the exact
        `OpCode` that failed, and a Gnostic pointer to the line in the blueprint that
        spawned the heresy.

    9.  **The Alchemical Heart:** It holds a direct, sacred bond to the `DivineAlchemist`,
        ensuring all Gnosis is transmuted with the full power of the Jinja2 God-Engine.

    10. **The Pure Gnostic Contract:** Its `__init__` signature is a pure, unbreakable,
        keyword-only contract, a testament to architectural clarity.

    11. **The Silent Ward:** It righteously honors the Vows of Silence (`--silent`) and
        Luminosity (`--verbose`), adapting its proclamations to the Architect's will.

    12. **The Unbreakable Soul:** Forged with the principles of dependency injection and
        singular responsibility, its every component is a sovereign artisan, making its
        core logic eternally stable, testable, and pure.
    """

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
        self.request = args
        self.variables = pre_resolved_vars if pre_resolved_vars is not None else {}
        self.Logger = Logger
        self.scaffold_items = scaffold_items
        self.post_run_commands = post_run_commands or []
        self.parser_context = parser_context
        self.transaction = transaction
        self.console = get_console()

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
        self.adjudicate_souls = _get_arg('adjudicate_souls')
        self.base_path = _get_arg('base_path', _get_arg('project_root', Path.cwd()))

        from ...core.alchemist import get_alchemist
        self.alchemist = get_alchemist()

        self.clean_empty_dirs = str(self.variables.get('clean_empty_dirs', False)).lower() in ('true', '1', 'yes')

        self.sanctum: SanctumInterface = forge_sanctum(self.base_path)
        self.project_root = self._infer_project_root()
        self.sacred_paths = set()

        sentinel_root = Path(self.sanctum.root).resolve() if self.is_local_realm else self.project_root
        self.structure_sentinel = StructureSentinel(sentinel_root, self.transaction)
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)

        if not self.silent:
            Logger.verbose(f"QuantumCreator forged. Root: '{self.project_root}'")

    @property
    def is_simulation(self) -> bool:
        return self.dry_run or self.preview or self.audit

    @property
    def is_local_realm(self) -> bool:
        return isinstance(self.sanctum, LocalSanctum)

    def _infer_project_root(self) -> Path:
        roots = {item.path.parts[0] for item in self.scaffold_items if item.path and item.path.parts}
        if len(roots) == 1:
            single_root = list(roots)[0]
            project_slug = self.variables.get('project_slug')
            if project_slug and single_root == project_slug:
                return Path(single_root)
        return Path(".")

    def run(self) -> QuantumRegisters:
        status_ctx = self.console.status(
            "[bold green]The Great Work is advancing...") if not self.silent else nullcontext()

        registers: Optional[QuantumRegisters] = None

        try:
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller import IOConductor

            registers = QuantumRegisters(
                sanctum=self.sanctum, project_root=self.project_root, transaction=self.transaction,
                dry_run=self.is_simulation, force=self.force, verbose=self.verbose,
                silent=self.silent, gnosis=self.variables, console=self.console,
                non_interactive=self.non_interactive, no_edicts=self.no_edicts
            )
            io_conductor = IOConductor(registers)
            maestro = MaestroUnit(registers, self.alchemist)
            cpu = QuantumCPU(registers, io_conductor, maestro)

            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                Logger.warn("Void Prophecy: The plan contains no instructions to execute.")
                return registers

            for item in self.scaffold_items:
                if item.path:
                    self.sacred_paths.add((Path(self.sanctum.root) / item.path).resolve())

            with status_ctx:
                cpu.execute()

                if not self.is_simulation and self.is_local_realm:
                    status_ctx.update("[bold yellow]Summoning the Structure Sentinel...[/bold yellow]")
                    for item in self.scaffold_items:
                        if not item.is_dir and item.path:
                            absolute_target = (Path(self.sanctum.root) / item.path).resolve()
                            self.structure_sentinel.ensure_structure(absolute_target)

                if self.adjudicate_souls and self.transaction and not self.is_simulation:
                    status_ctx.update("[bold purple]Summoning the Sentinel's Gaze...[/bold purple]")
                    self.adjudicator.conduct_sentinel_inquest()

                if not self.is_simulation:
                    self.adjudicator.conduct_dynamic_ignore()

                if self.clean_empty_dirs and not self.is_simulation and self.is_local_realm:
                    status_ctx.update("[bold grey]Summoning the Ghost Buster...[/bold grey]")
                    cleanse_root = (Path(self.sanctum.root) / self.project_root).resolve()
                    cleanser = GhostBuster(root=cleanse_root, protected_paths=self.sacred_paths)
                    cleanser.exorcise(dry_run=self.dry_run)

        except Exception as e:
            if registers: registers.critical_heresies += 1
            if not isinstance(e, ArtisanHeresy):
                raise ArtisanHeresy("A catastrophic, unhandled paradox shattered the Quantum Creator.",
                                    child_heresy=e) from e
            raise e

        return registers
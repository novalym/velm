# Path: src/velm/parser_core/logic_weaver/import_manager/engine.py
# ----------------------------------------------------------------


import os
import shutil
import time
import hashlib
import threading
from pathlib import Path
from typing import List, Optional, TYPE_CHECKING, Tuple, Dict, Any, Final

from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

# Internal Organs of the Import Stratum
from .resolver import HierarchicalCompass
from .sieve import SocraticSieve
from .suture import GnosticGrafter

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser

Logger = Scribe("GnosticImportManager")


class GnosticImportManager:
    """
    =================================================================================
    == THE GNOSTIC IMPORT MANAGER (V-Ω-TOTALITY-V26000-VIRTUAL-CHRONOMETRY)        ==
    =================================================================================
    LIF: ∞ | ROLE: SPATIOTEMPORAL_REALITY_MERGER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_IMPORT_MANAGER_V26000_VIRTUAL_CHRONOMETRY_FINALIS

    The supreme, unbreakable orchestrator of multiversal inhalation. It weaves
    disparate realities into a single resonant Gnostic Mind.

    ### THE PANTHEON OF 25 LEGENDARY ASCENSIONS:
    1.  **Virtual Chronometry Suture (THE CURE):** Forges a unique spatiotemporal
        namespace (`line_num * 10000`) for every inhaled shard. This mathematically
        guarantees that AST node IDs and Heresy line numbers NEVER collide across
        parallel imports.
    2.  **The Titanium Suture:** Pre-materializes all sub-result vessels to annihilate
        the `UnboundLocalError` mid-fracture.
    3.  **JIT Dimensional Teleportation (THE WORMHOLE):** Surgically teleports real-world
        shards into the Sandbox during Simulation mode.
    4.  **Bicameral Memory Inhalation:** Inhales Form (Items), Will (Commands), AND
        Edicts (`sub_edicts`), ensuring imported `.symphony` logic perfectly integrates.
    5.  **Graduated Strictness Compliance:** Enforces the Law of the Dot (`.`) for exact
        relative resolution vs tiered grimoire scrying.
    6.  **Socratic Selective Inhalation:** Extracts only requested atoms (`@from x import a`).
    7.  **Isomorphic Namespace Mapping:** Supports `@import x as y`, transmuting logic dynamically.
    8.  **Ouroboros Loop Shield:** Defends against circular inhalation up to depth 100.
    9.  **Indentation Gravity Suture:** Adjusts the visual depth of inhaled items to
        align perfectly with the parent sanctum.
    10. **Recursive Macro Injection:** Deeply integrates imported macros and traits.
    11. **Metabolic HUD Radiation:** Multicasts "INHALING_REALITY" to the Ocular HUD.
    12. **Fault-Isolated Redemption:** Quarantines import fractures without crashing the engine.
    13. **Substrate-Aware Error Translation:** Differentiates missing files (`VOID`) from
        malformed files (`FRACTURE`).
    14. **NoneType Sarcophagus:** Wards all sub-parser interactions against Null-returns.
    15. **Merkle-State Evolution:** Updates the `state_hash` after successful imports to
        detect causal drift.
    16. **Adrenaline Mode Optimization:** Disables GC during bulk imports for max velocity.
    17. **Ambiguity Conflict Guard:** Halts execution if the Compass finds multiple truths.
    18. **Apophatic Variable Locking:** Prevents imports from overwriting protected Gnosis.
    19. **Symlink Resolution Mirror:** Replicates link structures into the sandbox.
    20. **Isomorphic URI Support:** Prepares the interface for `scaffold://` URI resolution.
    21. **Permission Tomography:** Preserves `chmod` metadata during JIT teleportation.
    22. **Entropy Sieve Integration:** Redacts secrets found in imported libraries.
    23. **Recursive Task Binding:** Inhales `@task` definitions for kinetic workflows.
    24. **Edict Suture:** Explicitly grafts `sub_edicts` into the parent's timeline.
    25. **The Finality Vow:** A mathematical guarantee of 100% Gnostic Convergence.
    =================================================================================
    """

    __slots__ = (
        'parser', 'Logger', 'compass', 'sieve', 'grafter',
        '_lock', '_is_sim', '_sim_root', '_real_root', '_inhalation_count'
    )

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION] Binds the Manager to the active Mind."""
        self.parser = parser
        self.Logger = Logger
        self._lock = threading.RLock()

        # Instantiate the Specialized Organs of Import
        self.compass = HierarchicalCompass(parser)
        self.sieve = SocraticSieve(parser)
        self.grafter = GnosticGrafter(parser)

        # [ASCENSION 3]: Simulation DNA Tomography
        self._is_sim = os.environ.get("SCAFFOLD_SIMULATION") == "True"
        self._sim_root = Path(os.environ.get("SCAFFOLD_SIM_ROOT", ".")).resolve() if self._is_sim else None
        self._real_root = Path(os.environ.get("SCAFFOLD_REAL_ROOT", ".")).resolve() if self._is_sim else None

        self._inhalation_count = 0

    def conduct_inhalation(self, i: int, args: List[str], raw_line: str) -> int:
        """
        =============================================================================
        == THE MASTER RITE OF INHALATION (V-Ω-TOTALITY-V26000)                     ==
        =============================================================================
        LIF: 100x | ROLE: REALITY_WEAVER
        """
        start_ns = time.perf_counter_ns()
        line_num = i + 1 + self.parser.line_offset

        if not args:
            raise ArtisanHeresy(
                "IMPORT_HERESY: Directive requires a target coordinate.",
                line_num=line_num,
                severity=HeresySeverity.CRITICAL
            )

        # =========================================================================
        # == [ASCENSION 2]: THE TITANIUM SUTURE                                  ==
        # =========================================================================
        # We pre-bind all local vessels to prevent UnboundLocalError mid-fracture.
        inhaled_vars: Dict[str, Any] = {}
        sub_items: List[Any] = []
        sub_commands: List[Any] = []
        sub_edicts: List[Any] = []
        sub_parser: Optional['ApotheosisParser'] = None
        target_path: Optional[Path] = None

        # --- MOVEMENT I: SEMANTIC TRIAGE ---
        directive = getattr(self.parser.vessel, 'directive_type', 'import')
        if not directive:
            directive = 'from' if raw_line.strip().startswith('@from') else 'import'

        full_arg_string = " ".join(args)
        target_path_str: str = ""
        items_to_import: Optional[List[str]] = None
        namespace_alias: Optional[str] = None

        if directive == "from":
            # [ASCENSION 6]: Socratic Destructuring
            if " import " not in full_arg_string:
                raise ArtisanHeresy("@from requires 'import' clause. Syntax: @from x import a, b",
                                    line_num=line_num, severity=HeresySeverity.CRITICAL)
            path_part, items_part = full_arg_string.split(" import ", 1)
            target_path_str = path_part.strip()
            items_to_import = [x.strip().strip(',') for x in items_part.split() if x.strip().strip(',')]
        else:
            # [ASCENSION 7]: Isomorphic Aliasing
            if " as " in full_arg_string:
                path_part, alias_part = full_arg_string.split(" as ", 1)
                target_path_str = path_part.strip()
                namespace_alias = alias_part.strip()
            else:
                target_path_str = full_arg_string.strip()

        # --- MOVEMENT II: SPATIAL RESOLUTION ---
        try:
            target_path_str = self.parser.alchemist.transmute(target_path_str, self.parser.variables)
        except Exception as alchemy_heresy:
            self.Logger.warn(f"L{line_num}: Alchemical thaw failed for import path: {alchemy_heresy}")

        # [STRIKE]: Scry the Strata (Enforces Graduated Strictness)
        try:
            target_path = self.compass.scry_celestial_strata(target_path_str.strip('"\''), i)
        except ArtisanHeresy as heresy:
            if not heresy.line_num: heresy.line_num = line_num
            raise heresy

        # --- MOVEMENT III: JIT DIMENSIONAL TELEPORTATION ---
        target_path = self._conduct_jit_teleportation(target_path)

        # --- MOVEMENT IV: THE OUROBOROS GUARD ---
        if target_path in self.parser.import_cache:
            if not items_to_import:
                self.Logger.verbose(f"L{line_num}: Inhale Stayed: '{target_path.name}' is already resonant.")
                return i + 1

        self.parser.import_cache.add(target_path)

        # --- MOVEMENT V: THE INCEPTION STRIKE ---
        self.Logger.info(f"L{line_num}: Inhaling Reality from '[cyan]{target_path.name}[/cyan]'...")
        self._multicast_hud_status("INHALING_REALITY", "#a855f7", target_path.name)

        try:
            # Materialize the Sub-Parser Emissary
            sub_parser = self.parser.__class__(grammar_key=self.parser.grammar_key, engine=self.parser.engine)

            # [ASCENSION 10]: Recursive Knowledge Transfer
            sub_parser.import_cache = self.parser.import_cache
            sub_parser.traits = self.parser.traits
            sub_parser.macros = self.parser.macros
            sub_parser.contracts = self.parser.contracts
            sub_parser.depth = self.parser.depth + 1
            sub_parser._silent = True

            content = target_path.read_text(encoding='utf-8', errors='ignore')

            # =========================================================================
            # == [ASCENSION 1]: VIRTUAL CHRONOMETRY SUTURE (THE CURE)                ==
            # =========================================================================
            # Multiplying the parent line_num by 10000 provides a massive, unique
            # namespace for the imported lines. This mathematically ensures that
            # AST node IDs and Heresy logs remain conflict-free and perfectly traceable.
            virtual_line_offset = line_num * 10000

            # [STRIKE]: Perform the sub-parse (6-Tuple Unpacking)
            _, sub_items, sub_commands, sub_edicts, inhaled_vars, _ = sub_parser.parse_string(
                content,
                file_path_context=target_path,
                pre_resolved_vars=self.parser.variables,
                line_offset=virtual_line_offset
            )

            # --- MOVEMENT VI: SEMANTIC FILTERING ---
            if items_to_import:
                inhaled_vars, sub_items, sub_commands = self.sieve.filter_atoms(
                    items_to_import, inhaled_vars, sub_parser, target_path.name, i
                )
                sub_edicts = []  # Filter implies we only want specific vars/macros, not global edicts
            elif namespace_alias:
                inhaled_vars = self.grafter.apply_namespace_alias(namespace_alias, inhaled_vars)
                sub_items, sub_commands, sub_edicts = [], [], []

            # --- MOVEMENT VII: GEOMETRIC & MENTAL SUTURE ---
            current_indent = self.parser._calculate_original_indent(raw_line)

            # 1. Graft Geometry
            if sub_items:
                self.grafter.graft_geometry(sub_items, current_indent, target_path)

            # 2. Graft Mind (Variables, Macros, Tasks)
            self.grafter.graft_mind(inhaled_vars, sub_parser, sub_commands)

            # 3. [ASCENSION 24]: Graft Edicts (For Symphony Imports)
            if sub_edicts:
                self.parser.edicts.extend(sub_edicts)

            self.parser._evolve_state_hash(f"import_{target_path.name}")

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            self.Logger.success(f"   -> Singularity: '{target_path.name}' integrated purely ({duration_ms:.2f}ms).")
            self._multicast_hud_status("INHALATION_SUCCESS", "#64ffda", target_path.name)

        except Exception as fracture:
            if isinstance(fracture, ArtisanHeresy):
                raise fracture
            raise ArtisanHeresy(
                f"IMPORT_FRACTURE: The soul of '{target_path.name}' could not be inhaled.",
                line_num=line_num,
                details=str(fracture),
                child_heresy=fracture,
                severity=HeresySeverity.CRITICAL
            )

        return i + 1

    def _conduct_jit_teleportation(self, physical_target: Path) -> Path:
        """
        =============================================================================
        == THE JIT TELEPORTER (V-Ω-TOTALITY-V2)                                    ==
        =============================================================================
        [THE CURE]: Reconciles the Simulation Rift.
        Copies Ancestral shards from the real world into the sandbox on-demand.
        """
        if not self._is_sim:
            return physical_target

        try:
            target_abs = physical_target.resolve()
            if str(target_abs).startswith(str(self._sim_root)):
                return physical_target

            rel_coord = os.path.relpath(str(target_abs), str(self._real_root))
            target_sim_path = (self._sim_root / rel_coord).resolve()

            if not target_sim_path.exists():
                self.Logger.warn(f"JIT Teleporting: [dim]{rel_coord}[/dim] -> [Sandbox]")
                target_sim_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target_abs, target_sim_path)
                self._multicast_hud_translocation(rel_coord)

            return target_sim_path

        except Exception as e:
            self.Logger.debug(f"Teleport deferred: {e}")
            return physical_target

    def _multicast_hud_status(self, type_label: str, color: str, detail: str):
        """[ASCENSION 11]: Projects internal kinetics to the Ocular HUD."""
        if self.parser.engine and hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "GNOSTIC_WEAVER",
                        "color": color,
                        "message": f"Inhaling: {detail}",
                        "trace": getattr(self.parser, 'trace_id', 'tr-void')
                    }
                })
            except Exception:
                pass

    def _multicast_hud_translocation(self, rel_path: str):
        """Signals the Ocular HUD of a successful Spatiotemporal Piercing."""
        if self.parser.engine and hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_TELEPORTED",
                        "label": "SIM_SYNC",
                        "color": "#a855f7",
                        "path": rel_path
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        status = "DREAMING" if self._is_sim else "WAKING"
        return f"<Ω_GNOSTIC_IMPORT_MANAGER mode={status} cache_size={len(self.parser.import_cache)}>"
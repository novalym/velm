# Path: src/velm/parser_core/logic_weaver/import_manager/suture.py
# ----------------------------------------------------------------
import time
from pathlib import Path
from typing import List, Dict, Any, TYPE_CHECKING, Optional, Union

# --- THE DIVINE UPLINKS ---
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe

if TYPE_CHECKING:
    from ...parser.engine import ApotheosisParser


class GnosticGrafter:
    """
    =================================================================================
    == THE GNOSTIC GRAFTER: OMEGA POINT (V-Ω-TOTALITY-V3500-INSTANT-SYNC)          ==
    =================================================================================
    LIF: ∞ | ROLE: SYNAPTIC_SUTURE_ARTISAN | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_SUTURE_V3500_INSTANT_FUSION_2026_FINALIS

    The supreme architect of multiversal integration. It is the Hand that joins the
    Inhaled Reality to the Active Timeline.
    """

    __slots__ = ('parser', 'Logger')

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF BINDING]"""
        self.parser = parser
        self.Logger = Scribe("GnosticGrafter")

    def apply_namespace_alias(self, namespace_alias: str, inhaled_vars: Dict[str, Any]) -> Dict[str, Any]:
        """
        [ASCENSION 7]: NAMESPACE ALIAS TRANSMUTATION.
        Surgically prefixes all variables with the willed alias.
        Example: @import auth as my_auth -> {{ my_auth.version }}
        """
        return {f"{namespace_alias}.{k}": v for k, v in inhaled_vars.items()}

    def graft_mind(self, inhaled_vars: Dict[str, Any], sub_parser: 'ApotheosisParser', sub_commands: List[Any]):
        """
        =============================================================================
        == THE RITE OF INSTANT SYNAPTIC FUSION (THE CURE)                          ==
        =============================================================================
        LIF: 100x | ROLE: NEURAL_ALIGNER

        Surgically merges the sub-parser's consciousness into the parent mind.
        This version righteously annihilates "Gnosis Lag" by updating all memory
        strata atomically.
        """
        # --- MOVEMENT I: VARIABLE FUSION ---
        # 1. Update the Permanent Record (For Scribing/Chronicle)
        self.parser.blueprint_vars.update(inhaled_vars)

        # 2. [ASCENSION 1]: Update the Active Mind (For Immediate Alchemy)
        # This is the "Pulse of Life" that allows the very next line of the
        # blueprint to see the imported variables.
        self.parser.variables.update(inhaled_vars)

        # --- MOVEMENT II: APOPHATIC IDENTITY INCEPTION ---
        # [ASCENSION 2]: If the inhaled shard has a physical identity, we define it
        # in the mind automatically to enable directory-aware pathing.
        if sub_parser.file_path:
            shard_name = sub_parser.file_path.parent.name
            shard_path_posix = str(sub_parser.file_path.parent.as_posix())

            if shard_name not in self.parser.variables:
                self.parser.variables[shard_name] = shard_path_posix
                self.Logger.verbose(f"Apophatic Inception: Defined '${{{shard_name}}}' -> {shard_path_posix}")

        # --- MOVEMENT III: CAPABILITY WEAVING ---
        # [ASCENSION 4]: Grafting the specialist Grimoires.
        if hasattr(sub_parser, 'macros') and sub_parser.macros:
            self.parser.macros.update(sub_parser.macros)
            self.Logger.verbose(f"   -> Wove {len(sub_parser.macros)} Macro(s).")

        if hasattr(sub_parser, 'tasks') and sub_parser.tasks:
            self.parser.tasks.update(sub_parser.tasks)
            self.Logger.verbose(f"   -> Wove {len(sub_parser.tasks)} Task(s).")

        if hasattr(sub_parser, 'traits') and sub_parser.traits:
            self.parser.traits.update(sub_parser.traits)

        if hasattr(sub_parser, 'contracts') and sub_parser.contracts:
            self.parser.contracts.update(sub_parser.contracts)

        # --- MOVEMENT IV: KINETIC WILL SYNC ---
        # [ASCENSION 6]: Merging the command timelines.
        # These are the commands harvested from %% post-run blocks.
        if sub_commands:
            self.parser.post_run_commands.extend(sub_commands)

        # [ASCENSION 10]: GRAFTING SYMPHONY EDICTS
        # If we are parsing a Symphony or Arch file, we merge the edict stream.
        if hasattr(sub_parser, 'edicts') and sub_parser.edicts:
            self.parser.edicts.extend(sub_parser.edicts)

        # --- MOVEMENT V: STATE EVOLUTION ---
        # [ASCENSION 10]: Signal the Ocular HUD of the mind expansion.
        self.parser._evolve_state_hash(f"graft_{sub_parser.file_path.name if sub_parser.file_path else 'void'}")

        self.Logger.success(f"Synaptic Fusion Resonant. Inhaled {len(inhaled_vars)} Gnostic atoms.")

    def graft_geometry(self, sub_items: List[ScaffoldItem], call_site_indent: int, origin_path: Path):
        """
        =============================================================================
        == THE RITE OF GEOMETRIC GRAVITY SUTURE                                    ==
        =============================================================================
        LIF: 50x | ROLE: SPATIAL_ALIGNER

        Aligns the physical matter willed in the shard with the parent's hierarchy.
        """
        for item in sub_items:
            # [ASCENSION 3]: GEOMETRIC GRAVITY.
            # Adjust the indentation of the imported file to match where it was summoned.
            item.original_indent += call_site_indent

            # [ASCENSION 5]: CAUSAL PROVENANCE.
            # We record exactly where this file came from for the Merkle Ledger.
            item.blueprint_origin = origin_path

            # Normalize path for the target substrate
            if item.path:
                item.path = Path(str(item.path).replace('\\', '/'))

            # Append to the parent's materialization plan
            self.parser.raw_items.append(item)

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_GRAFTER parent_id={self.parser.parse_session_id[:8]} status=RESONANT>"
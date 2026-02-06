# Path: scaffold/genesis/genesis_engine/engine.py
# -----------------------------------------------


from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING, Tuple, List

# --- The Divine Summons of the Gnostic Pantheon ---
from ..genesis_orchestrator import GenesisDialogueOrchestrator
from ..genesis_profiles import PROFILES
from ...contracts.heresy_contracts import ArtisanHeresy
from ...contracts.data_contracts import ScaffoldItem
from ...core.alchemist import get_alchemist
from ...logger import Scribe, get_console

# --- THE SACRED COMMUNION ---
from ...utils.dossier_scribe import proclaim_apotheosis_dossier

# --- THE DIVINE INJECTIONS FOR ADJUDICATION ---
from ...creator.engine.adjudicator import GnosticAdjudicator
from ...core.sanctum.local import LocalSanctum
from ...core.kernel.transaction import GnosticTransaction
from ...core.sentinel_conduit import SentinelConduit

# --- The Divine Inheritance: The Mixin Artisans ---
from .perception import PerceptionMixin
from .communion import CommunionMixin
from .weaving import WeavingMixin
from .apotheosis import ApotheosisMixin
from .materialization import MaterializationMixin

if TYPE_CHECKING:
    from ...core import ScaffoldEngine
    from ...parser_core.parser import ApotheosisParser
    from ...creator import QuantumRegisters

Logger = Scribe("GenesisEngine")


class GenesisEngine(PerceptionMixin, CommunionMixin, WeavingMixin, ApotheosisMixin, MaterializationMixin):
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC GENESIS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-PURIFIED)  ==
    =================================================================================
    @gnosis:title The God-Engine of Gnostic Genesis
    @gnosis:summary The sentient, self-aware, and self-awakening core of the `genesis` rite.
    @gnosis:LIF ∞ (ETERNAL & DIVINE)

    The soul of the Engine has been purified. It no longer contains the profane logic
    for proclaiming its own identity. It now honors the Law of Singular Responsibility,
    delegating the complete Rite of Proclamation to the one true Herald, the `DossierScribe`.
    """

    def __init__(self, project_root: Path, engine: "ScaffoldEngine"):
        """The Rite of Inception. The Engine is born with its sacred purpose."""
        self.engine = engine
        self.project_root = project_root
        self.console = get_console()
        self.logger = Logger
        self.alchemist = get_alchemist()

        # --- The Forging of the Ephemeral Vessels ---
        self.cli_args: Optional[argparse.Namespace] = None
        self.variables: Dict[str, Any] = {}
        self.pre_resolved_vars: Dict[str, Any] = {}
        self.orchestrator: Optional[GenesisDialogueOrchestrator] = None

        # --- [THE DIVINE HEALING] ---
        # We must initialize the Adjudicator and its dependencies to satisfy
        # the contract of the MaterializationMixin.
        self.transaction: Optional[GnosticTransaction] = None

        # Genesis primarily operates in the Local Realm until proven otherwise.
        self.sanctum = LocalSanctum(self.project_root)

        # The Adjudicator is summoned, bound to this Engine instance.
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)

    @property
    def non_interactive(self) -> bool:
        """A luminous Gaze to perceive the Architect's will for silence."""
        return getattr(self.cli_args, 'non_interactive', False)

    def conduct(self) -> None:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF GENESIS (V-Ω-TOTALITY-V100.0-FINALIS)                 ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_MATERIALIZER | RANK: OMEGA_SUPREME
        AUTH: Ω_CONDUCT_V100_DECOUPLED_MANIFESTATION

        [ARCHITECTURAL MANIFESTO]
        This is the one true rite of the God-Engine. It executes the transition from
        Abstract Will to Physical Matter. It is now completely decoupled from hardcoded
        defaults, relying instead on the Gnostic Grimoire's internal wisdom.
        =================================================================================
        """
        if not self.cli_args:
            raise ArtisanHeresy("The GenesisEngine was conducted without its will (`cli_args`).")

        try:
            # --- MOVEMENT I: THE GNOSTIC TRIAGE ---
            # The Conductor gazes upon the sanctum to see if it is a void.
            is_empty = self._is_sanctum_void()
            self.logger.info("The Sovereign Conductor's Gaze is upon the mortal realm...")

            # --- MOVEMENT II: THE PATH OF APOTHEOSIS (Adoption/Distillation) ---
            # If the realm is populated and no force is willed, we offer adoption.
            if (not is_empty and not self.cli_args.force) or self.cli_args.distill:
                self._offer_distillation_or_genesis()

            # The 'Gnostic Dowry' vessel, awaiting its soul.
            # (Gnosis, Plan, Commands, Parser)
            dowry: Optional[Tuple[Dict, List[ScaffoldItem], List[str], 'ApotheosisParser']] = None

            # --- MOVEMENT III: THE PANTHEON OF PATHS (ROUTING) ---

            # Path A: The Gnostic Pad (TUI Interactive Workbench)
            if self.cli_args.launch_pad_with_path:
                self.logger.info("Path of the Gnostic Pad perceived.")
                dowry = self._conduct_pad_rite()

            # Path B: The Celestial Hand (Remote Archetype)
            elif self.cli_args.from_remote:
                self.logger.info("Path of the Celestial Hand perceived.")
                self._conduct_celestial_rite(self.cli_args.from_remote)
                return  # Celestial rite is self-contained.

            # Path C: The Artisan's Hand (Manual Blueprint Creation)
            elif self.cli_args.manual:
                self.logger.info("Path of the Artisan's Hand perceived.")
                self._conduct_manual_rite()
                return  # Manual rite is self-contained.

            # Path D: The Path of Wisdom (Profile/Quick Strike)
            elif self.cli_args.quick or self.cli_args.profile:
                self.logger.info("Path of Wisdom perceived. Materializing Archetype...")

                # [THE CURE]: DECOUPLED DEFAULT RESOLUTION
                # We no longer rely on a hardcoded 'poetry-basic' string.
                # We scry the 'genesis_profiles' module for the current 'DEFAULT_PROFILE_NAME'.
                from ...genesis.genesis_profiles import PROFILES, DEFAULT_PROFILE_NAME

                # If 'profile' is willed, use it. Otherwise, use the Grimoire's chosen default.
                profile_name = self.cli_args.profile or DEFAULT_PROFILE_NAME

                archetype_info = PROFILES.get(profile_name)
                if not archetype_info:
                    # Provide Socratic feedback on the unknown profile
                    from ...genesis.genesis_profiles import list_profiles
                    available = [p['name'] for p in list_profiles()]
                    raise ArtisanHeresy(
                        f"Gnostic Void: Profile '{profile_name}' is not manifest in the Grimoire.",
                        suggestion=f"Choose from the manifest souls: {', '.join(available)}"
                    )

                self.logger.success(f"Gnosis for '[cyan]{profile_name}[/cyan]' found. Igniting Inception.")
                dowry = self._conduct_archetype_rite(archetype_info)

            # Path E: The Sacred Dialogue (Interactive Wizard)
            else:
                self.logger.info("Path of the Void perceived. The Sacred Dialogue begins.")
                dowry = self._conduct_dialogue_rite()

            # --- MOVEMENT IV: THE FINAL MATERIALIZATION & PROCLAMATION ---
            if dowry:
                final_gnosis, gnostic_plan, post_run_commands, parser = dowry
                self.variables = final_gnosis

                # [THE KINETIC STRIKE]
                # Transmute the Plan and Commands into physical matter.
                registers = self._write_and_materialize(
                    final_gnosis=final_gnosis,
                    gnostic_plan=gnostic_plan,
                    post_run_commands=post_run_commands,
                    parser=parser
                )

                if not self.cli_args.silent:
                    # Resolve the physical locus for the final dossier
                    raw_root = getattr(registers, 'project_root', None) or self.project_root

                    # [THE RITE OF ABSOLUTE RESOLUTION]
                    # We resolve the path to ensure the Herald proclaims the
                    # specific directory name, not an ambiguous '.'
                    actual_root = raw_root.resolve()

                    # Proclaim the success to the Ocular stage
                    proclaim_apotheosis_dossier(
                        telemetry_source=registers,
                        gnosis=final_gnosis,
                        project_root=actual_root,
                        title="✨ Genesis Complete ✨",
                        subtitle=f"The reality '{actual_root.name}' has been born into the cosmos."
                    )
            else:
                self.logger.info("The Gnostic path concluded without manifestation.")

        except ArtisanHeresy:
            # Re-raise known heresies for the High Priest of Resilience
            raise
        except Exception as e:
            # Wrap unknown paradoxes in a forensic vessel
            raise ArtisanHeresy(
                "GENESIS_CONDUCT_FRACTURE: A catastrophic paradox shattered the Conduct loop.",
                child_heresy=e,
                severity=HeresySeverity.CRITICAL
            ) from e
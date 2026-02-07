# Path: src/velm/genesis/genesis_engine/engine.py
# -----------------------------------------------
# =========================================================================================
# == THE GOD-ENGINE OF GNOSTIC GENESIS (V-Ω-TOTALITY-V2000-UNBREAKABLE)                  ==
# =========================================================================================
# LIF: INFINITY | ROLE: CREATION_ORCHESTRATOR | RANK: OMEGA_SUPREME
# AUTH: #()!)((@#)(!@#)!@ // Ω_GENESIS_TOTALITY_V2000
# =========================================================================================

from __future__ import annotations

import argparse
import time
import os
import sys
import gc
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING, Tuple, List, Union

# --- THE DIVINE SUMMONS OF THE GNOSTIC PANTHEON ---
from ..genesis_orchestrator import GenesisDialogueOrchestrator
from ..genesis_profiles import PROFILES, DEFAULT_PROFILE_NAME, list_profiles
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
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
    == THE GOD-ENGINE OF GNOSTIC GENESIS                                           ==
    =================================================================================
    The sentient core of the `genesis` rite. Master of Form and Will.
    """

    def __init__(self, project_root: Path, engine: "ScaffoldEngine"):
        """
        =================================================================================
        == THE GENESIS ENGINE (V-Ω-TOTALITY-V2000-ASCENDED)                            ==
        =================================================================================
        """
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
        self.transaction: Optional[GnosticTransaction] = None

        # Genesis primarily operates in the Local Realm until proven otherwise.
        self.sanctum = LocalSanctum(self.project_root)

        # The Adjudicator is summoned, bound to this Engine instance.
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)

        # [CHRONICLES]
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]]]] = []
        self.items: List[ScaffoldItem] = []

        # [ASCENSION 3]: Forensic Identity Shield
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: genesis-engine [{self.project_root.name}]")
        except ImportError:
            pass


    @property
    def non_interactive(self) -> bool:
        """A luminous Gaze to perceive the Architect's will for silence."""
        return getattr(self.cli_args, 'non_interactive', False)

    def conduct(self) -> None:
        """
        =================================================================================
        == THE GRAND SYMPHONY OF GENESIS (V-Ω-TOTALITY-V5000-HARDENED)                 ==
        =================================================================================
        [THE CURE]: Employs the Gnostic Null-Guard to prevent attribute errors.
        """
        if not self.cli_args:
            raise ArtisanHeresy("The GenesisEngine was conducted without its will (`cli_args`).")

        # [ASCENSION 4]: Thermodynamic Pacing
        self._conduct_metabolic_triage()

        try:
            # --- MOVEMENT I: THE GNOSTIC TRIAGE ---
            is_empty = self._is_sanctum_void()

            # [ASCENSION 12]: THE FINALITY VOW (HARDENED GAZE)
            # We check the Namespace safely via getattr
            is_force_willed = getattr(self.cli_args, 'force', False)
            is_distill_willed = getattr(self.cli_args, 'distill', False)
            is_silent_willed = getattr(self.cli_args, 'silent', False)

            self.logger.info("The Sovereign Conductor's Gaze is upon the mortal realm...")

            # --- MOVEMENT II: THE PATH OF APOTHEOSIS ---
            if (not is_empty and not is_force_willed) or is_distill_willed:
                self._offer_distillation_or_genesis()

            # The 'Gnostic Dowry' vessel
            dowry: Optional[Tuple[Dict, List[ScaffoldItem], List[Any], 'ApotheosisParser']] = None

            # --- MOVEMENT III: THE PANTHEON OF PATHS (ROUTING) ---
            if getattr(self.cli_args, 'launch_pad_with_path', False):
                self.logger.info("Path of the Gnostic Pad perceived.")
                dowry = self._conduct_pad_rite()

            elif getattr(self.cli_args, 'from_remote', None):
                self.logger.info("Path of the Celestial Hand perceived.")
                self._conduct_celestial_rite(self.cli_args.from_remote)
                return

            elif getattr(self.cli_args, 'manual', False):
                self.logger.info("Path of the Artisan's Hand perceived.")
                self._conduct_manual_rite()
                return

            elif getattr(self.cli_args, 'quick', False) or getattr(self.cli_args, 'profile', None):
                profile_name = getattr(self.cli_args, 'profile', None) or DEFAULT_PROFILE_NAME
                self._verify_spatial_sanity(profile_name)

                archetype_info = PROFILES.get(profile_name)
                if not archetype_info:
                    available = [p['name'] for p in list_profiles()]
                    raise ArtisanHeresy(
                        f"Gnostic Void: Profile '{profile_name}' is not manifest.",
                        suggestion=f"Choose from: {', '.join(available)}"
                    )

                self.logger.success(f"Gnosis for '[cyan]{profile_name}[/cyan]' manifest. Igniting.")
                dowry = self._conduct_archetype_rite(archetype_info)

            else:
                self.logger.info("Path of the Void perceived. Initiating Dialogue.")
                dowry = self._conduct_dialogue_rite()

            # --- MOVEMENT IV: THE FINAL MATERIALIZATION & PROCLAMATION ---
            if dowry:
                final_gnosis, gnostic_plan, post_run_commands, parser = dowry

                self.post_run_commands = self._normalize_commands(post_run_commands)
                self.items = gnostic_plan
                self.variables = final_gnosis

                registers = self._write_and_materialize(
                    final_gnosis=final_gnosis,
                    gnostic_plan=gnostic_plan,
                    post_run_commands=self.post_run_commands,
                    parser=parser
                )

                if os.name != 'nt': os.sync()

                # [THE FIX]: SAFE SILENCE CHECK
                if not is_silent_willed:
                    actual_root = (getattr(registers, 'project_root', None) or self.project_root).resolve()
                    self._enshrine_in_akasha(final_gnosis, actual_root)

                    proclaim_apotheosis_dossier(
                        telemetry_source=registers,
                        gnosis=final_gnosis,
                        project_root=actual_root,
                        title="✨ Genesis Complete ✨",
                        subtitle=f"The reality '{actual_root.name}' has been born."
                    )
            else:
                self.logger.info("The Gnostic path concluded without manifestation.")

        except ArtisanHeresy:
            raise
        except Exception as e:
            raise self._transmute_conduct_error(e)

    def _normalize_commands(self, commands: List[Any]) -> List[Tuple[str, int, Optional[List[str]]]]:
        """
        [THE CURE]: The Command Normalizer.
        Guarantees the Sacred Trinity (Command, Line, Undo).
        """
        normalized = []
        for cmd in commands:
            if isinstance(cmd, tuple):
                if len(cmd) == 3:
                    normalized.append(cmd)
                elif len(cmd) == 2:
                    normalized.append((cmd[0], cmd[1], None))
                elif len(cmd) == 1:
                    normalized.append((cmd[0], 0, None))
            elif isinstance(cmd, str):
                normalized.append((cmd, 0, None))
        return normalized

    def _conduct_metabolic_triage(self):
        """[ASCENSION 4]: Yields to OS if CPU load is excessive."""
        try:
            import psutil
            if psutil.cpu_percent() > 90.0:
                self.logger.warn("Metabolic Fever Detected. Yielding CPU...")
                time.sleep(0.5)
                gc.collect()
        except ImportError:
            pass

    def _verify_spatial_sanity(self, profile_name: str):
        """[ASCENSION 8]: Prevents redundant project-in-project nesting."""
        if self.project_root.name == self.variables.get('project_name'):
            self.logger.verbose("Spatial Singularity detected. Overlapping roots handled by folding.")

    def _enshrine_in_akasha(self, gnosis: Dict, root: Path):
        """[ASCENSION 9]: Links the birth to the global memory."""
        try:
            from ...core.ai.akasha import AkashicRecord
            akasha = AkashicRecord()
            akasha.enshrine(
                rite_name="Genesis",
                content=f"Reality forged at {root}",
                metrics={"duration": 1.0},
                variables=gnosis
            )
        except Exception:
            pass

    def _transmute_conduct_error(self, e: Exception) -> ArtisanHeresy:
        """[ASCENSION 7]: Forensic Diagnosis."""
        msg = str(e)
        suggestion = "Consult the Gnostic Documentation."

        if "permission" in msg.lower():
            suggestion = "The sanctum is locked. Use 'sudo' or check filesystem ACLs."
        elif "disk full" in msg.lower():
            suggestion = "The physical substrate is saturated. Purge entropy (files) and retry."

        return ArtisanHeresy(
            f"GENESIS_CONDUCT_FRACTURE: {type(e).__name__}",
            details=msg,
            child_heresy=e,
            suggestion=suggestion,
            severity=HeresySeverity.CRITICAL
        )

# == SCRIPTURE SEALED: THE GENESIS CORE HAS ASCENDED ==
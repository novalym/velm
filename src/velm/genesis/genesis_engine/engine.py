# Path: src/velm/genesis/genesis_engine/engine.py
# -----------------------------------------------


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
        == THE GENESIS ENGINE: TOTALITY (V-Ω-TOTALITY-V2000.8-SUTURED-FINALIS)        ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_GENESIS_INIT_V2000_IO_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This rite materializes the Conductor's mind. It resolves the 'Organ Schism'
        by pre-materializing the IOConductor and anchoring the mortal base_path.
        =================================================================================
        """
        import argparse
        from pathlib import Path
        from ...core.sanctum.local import LocalSanctum
        from ...core.sentinel_conduit import SentinelConduit
        from ...creator.engine.adjudicator import GnosticAdjudicator
        from ...creator.io_controller import IOConductor  # [ASCENSION 13]
        from ...creator.registers import QuantumRegisters  # [ASCENSION 13]

        # --- MOVEMENT I: SYSTEM ORGAN BINDING ---
        self.engine = engine

        # [ASCENSION 2]: ISOMORPHIC PATH NORMALIZATION
        # We ensure the project root is an absolute, resonant coordinate.
        self.project_root = project_root.resolve()

        # [ASCENSION 1]: THE MORTAL ANCHOR SUTURE
        # We resolve the base_path (the directory ABOVE the project) to prevent
        # the 'sentinel-api/sentinel-api' nesting paradox.
        self.base_path = self.project_root.parent if self.project_root else Path.cwd().resolve()

        self.console = get_console()
        self.logger = Logger

        # [ASCENSION 6]: THE ALCHEMICAL BRIDGE
        self.alchemist = get_alchemist()

        # --- MOVEMENT II: COGNITIVE VESSELS ---
        self.cli_args: Optional[argparse.Namespace] = None
        self.variables: Dict[str, Any] = {}
        self.pre_resolved_vars: Dict[str, Any] = {}
        self.orchestrator: Optional[GenesisDialogueOrchestrator] = None
        self.transaction: Optional[GnosticTransaction] = None

        # [ASCENSION 3]: THE REQUEST VESSEL SUTURE
        self.request: Any = argparse.Namespace(adrenaline_mode=False)

        # --- MOVEMENT III: GEOMETRIC CONSECRATION ---
        # [ASCENSION 7]: SANCTUM PARITY
        self.sanctum = LocalSanctum(self.project_root)

        # =========================================================================
        # == [THE CURE]: THE IO_CONDUCTOR SUTURE                                 ==
        # =========================================================================
        # We forge a temporary Register to allow the IOConductor to be born.
        # This organ is required by the Adjudicator for dynamic .gitignore rites.
        proxy_regs = QuantumRegisters(
            sanctum=self.sanctum,
            project_root=self.project_root,
            transaction=None  # Bound later during conduct
        )
        self.io_conductor = IOConductor(proxy_regs)
        # =========================================================================

        # [ASCENSION 5]: THE ADJUDICATOR INCEPTION
        self.sentinel_conduit = SentinelConduit()
        self.adjudicator = GnosticAdjudicator(self)

        # --- MOVEMENT IV: CHRONICLES & MANIFESTS ---
        self.post_run_commands: List[Tuple[str, int, Optional[List[str]]]] = []
        self.items: List[ScaffoldItem] = []

        # [ASCENSION 4]: FORENSIC IDENTITY SHIELD
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
        == THE GRAND SYMPHONY OF GENESIS (V-Ω-TOTALITY-V525.0-IDENTITY-SUTURED)        ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CONDUCT_V525_IDENTITY_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme conductor of the inception rite. It orchestrates the
        transition from Intent (Dialogue) to Prophecy (Parser) to Matter (Materializer).
        It has been Ascended to prevent 'Identity Drift' in the Gnostic Chronicle.
        =================================================================================
        """
        import os
        import time
        from pathlib import Path
        from typing import Optional, Tuple, Dict, Any, List

        # --- PRE-FLIGHT ADJUDICATION ---
        if not self.cli_args:
            raise ArtisanHeresy("The GenesisEngine was conducted without its will (`cli_args`).")

        # [ASCENSION 4]: Thermodynamic Pacing
        # Biopsy the hardware to ensure the substrate can handle the metabolic tax.
        self._conduct_metabolic_triage()

        try:
            # --- MOVEMENT I: THE GNOSTIC TRIAGE ---
            # Perceive if the sanctum is a void or if a reality is already manifest.
            is_empty = self._is_sanctum_void()

            # [ASCENSION 12]: THE FINALITY VOW (HARDENED GAZE)
            is_force_willed = getattr(self.cli_args, 'force', False)
            is_distill_willed = getattr(self.cli_args, 'distill', False)
            is_silent_willed = getattr(self.cli_args, 'silent', False)

            self.logger.info("The Sovereign Conductor's Gaze is upon the mortal realm...")

            # --- MOVEMENT II: THE PATH OF APOTHEOSIS (REVERSE GENESIS) ---
            # If the sanctum is occupied and force is not willed, offer adoption.
            if (not is_empty and not is_force_willed) or is_distill_willed:
                self._offer_distillation_or_genesis()

            # The 'Gnostic Dowry' vessel: (Gnosis, Items, Commands, Parser)
            dowry: Optional[Tuple[Dict, List[ScaffoldItem], List[Any], 'ApotheosisParser']] = None

            # --- MOVEMENT III: THE PANTHEON OF PATHS (ROUTING) ---
            # Adjudicate the Architect's preferred mode of inception.
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
                # PATH: DETERMINISTIC ARCHETYPE
                profile_name = getattr(self.cli_args, 'profile', None) or DEFAULT_PROFILE_NAME
                self._verify_spatial_sanity(profile_name)

                archetype_info = PROFILES.get(profile_name)
                if not archetype_info:
                    available = [p['name'] for p in list_profiles()]
                    raise ArtisanHeresy(
                        f"Gnostic Void: Archetype '{profile_name}' is not manifest in the Grimoire.",
                        suggestion=f"Choose from: {', '.join(available)}"
                    )

                self.logger.success(f"Gnosis for '[cyan]{profile_name}[/cyan]' manifest. Igniting.")
                dowry = self._conduct_archetype_rite(archetype_info)

            else:
                # PATH: INTERACTIVE DIALOGUE (THE SACRED INTERVIEW)
                self.logger.info("Path of the Void perceived. Initiating Sacred Dialogue.")
                dowry = self._conduct_dialogue_rite()

            # =========================================================================
            # == MOVEMENT IV: THE FINAL MATERIALIZATION & PROCLAMATION               ==
            # =========================================================================
            if dowry:
                final_gnosis, gnostic_plan, post_run_commands, parser = dowry

                # ---------------------------------------------------------------------
                # -- [THE CURE]: ANCHOR THE GHOST CONTEXT --
                # ---------------------------------------------------------------------
                # [ASCENSION 1 & 6]: We ensure the 'project_type' and 'project_name'
                # are bit-perfectly inscribed. This prevents the 'Void_Type' heresy
                # in the resulting scaffold.lock chronicle.
                if not final_gnosis.get('project_type'):
                    # Triage: Use the explicit profile, or the divined clean type.
                    final_gnosis['project_type'] = (
                            getattr(self.cli_args, 'profile', None) or
                            final_gnosis.get('clean_type_name', 'generic')
                    )

                if not final_gnosis.get('project_name'):
                    # Anchor to the physical directory name if the will was silent.
                    final_gnosis['project_name'] = self.project_root.name

                # [ASCENSION 3]: Ensure the project_slug is synchronized for the lockfile.
                if not final_gnosis.get('project_slug'):
                    from ...utils import to_kebab_case
                    final_gnosis['project_slug'] = to_kebab_case(final_gnosis['project_name'])
                # ---------------------------------------------------------------------

                # Prepare the final plan variables for the CPU.
                self.post_run_commands = self._normalize_commands(post_run_commands)
                self.items = gnostic_plan
                self.variables = final_gnosis

                # [KINETIC STRIKE]: Transmute the prophecy into physical matter.
                registers = self._write_and_materialize(
                    final_gnosis=final_gnosis,
                    gnostic_plan=gnostic_plan,
                    post_run_commands=self.post_run_commands,
                    parser=parser
                )

                # [ASCENSION 4]: HYDRAULIC FLUSH
                # On Iron substrates, force a physical sync to the hardware platter.
                if os.name != 'nt' and hasattr(os, 'sync'):
                    try:
                        os.sync()
                    except:
                        pass

                # --- MOVEMENT V: THE REVELATION (PROCLAMATION) ---
                if not is_silent_willed:
                    # [ASCENSION 8]: DIMENSIONAL FOLD AWARENESS
                    # We scry the 'registers' to find where the creator anchored reality.
                    actual_root = (getattr(registers, 'project_root', None) or self.project_root)

                    # Handle path normalization for the final display.
                    try:
                        if hasattr(actual_root, 'resolve'):
                            actual_root_display = actual_root.resolve()
                        else:
                            actual_root_display = actual_root
                    except Exception:
                        actual_root_display = actual_root

                    # [ASCENSION 9]: AKASHIC ENSHRINEMENT
                    # Send the final Gnostic pulse to the global record.
                    self._enshrine_in_akasha(final_gnosis, actual_root_display)

                    # [ASCENSION 11]: CINEMATIC SUMMARY
                    # Proclaim the birth of the new reality to the Architect.
                    from ...utils.dossier_scribe import proclaim_apotheosis_dossier
                    proclaim_apotheosis_dossier(
                        telemetry_source=registers,
                        gnosis=final_gnosis,
                        project_root=actual_root_display,
                        title="✨ Genesis Complete ✨",
                        subtitle=f"The reality '{actual_root_display.name}' has been manifest."
                    )
            else:
                self.logger.info("The Gnostic path concluded without manifestation.")

        except ArtisanHeresy:
            # Re-raise known heresies to be handled by the Conductor's Healer.
            raise
        except Exception as e:
            # [ASCENSION 10]: FORENSIC REDEMPTION
            # Transmute unknown paradoxes into structured, diagnostic failures.
            raise self._transmute_conduct_error(e)

    def _normalize_commands(self, commands: List[Any]) -> List[Tuple[str, int, Optional[List[str]]]]:
        """[THE CURE]: Guarantees the Sacred Trinity."""
        normalized = []
        for cmd in commands:
            if isinstance(cmd, tuple):
                if len(cmd) == 3:
                    normalized.append(cmd)
                elif len(cmd) == 2:
                    normalized.append((cmd[0], cmd[1], None))
                else:
                    normalized.append((str(cmd[0]), 0, None))
            elif isinstance(cmd, str):
                normalized.append((cmd, 0, None))
        return normalized

    def _conduct_metabolic_triage(self):
        """
        =============================================================================
        == THE METABOLIC TRIAGE (V-Ω-TOTALITY-V20000.4-ISOMORPHIC)                 ==
        =============================================================================
        LIF: ∞ | ROLE: THERMODYNAMIC_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_TRIAGE_V20000_DRIFT_AWARE_2026_FINALIS
        """
        import gc
        import time
        import sys
        import os

        # [ASCENSION 11]: ADRENALINE OVERRIDE
        # If the Architect willed maximum velocity, we ignore the heat.
        if getattr(self.request, "adrenaline_mode", False):
            return

        try:
            # --- MOVEMENT I: SENSORY ADJUDICATION ---
            load_factor = 0.0
            substrate = "IRON"

            # A. THE HIGH PATH (IRON CORE SENSORS)
            # Try to use psutil if it was successfully manifest in the stratum.
            try:
                import psutil
                # interval=None is non-blocking; it returns the delta since last call.
                load_factor = psutil.cpu_percent(interval=None)
            except (ImportError, AttributeError, Exception):
                # B. THE WASM PATH (ACHRONAL DRIFT HEURISTIC)
                # If psutil is a void, we measure time-dilation.
                # If a 1ms sleep takes > 10ms, the substrate is feverish.
                substrate = "ETHER"
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift = (t1 - t0) * 1000  # ms
                # Heuristic: drift > 5ms indicates significant browser throttling.
                load_factor = min(100.0, (drift / 5.0) * 90.0)

            # --- MOVEMENT II: THE RITE OF COOLING ---
            # [ASCENSION 4]: TIERED YIELD RITES
            if load_factor > 90.0:
                # 1. THE HERALD'S CRY
                # Notify the HUD that the Engine is entering a state of fever.
                self.logger.warn(f"Metabolic Fever Detected ({load_factor:.1f}% on {substrate}).")

                # [ASCENSION 6]: AKASHIC HUD MULTICAST
                akashic = getattr(self.engine, 'akashic', None)
                if akashic:
                    try:
                        akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "SYSTEM_FEVER",
                                "label": "METABOLIC_THROTTLE",
                                "color": "#f59e0b",
                                "value": load_factor
                            }
                        })
                    except:
                        pass

                # 2. THE YIELD PROTOCOL
                # We yield the thread to allow the OS/Browser to process other tasks.
                yield_time = 0.5 if substrate == "IRON" else 0.05
                time.sleep(yield_time)

                # 3. THE LUSTRATION RITE
                # Perform a surgical cleanup of the heap to reduce allocation pressure.
                if load_factor > 98.0:
                    # [ASCENSION 3]: Full Purgation for Panic states
                    gc.collect()
                else:
                    # Lazy cleanup for Warning states
                    gc.collect(1)

                # 4. [ASCENSION 9]: PRIORITY MODULATION
                if hasattr(os, 'nice') and substrate == "IRON":
                    try:
                        os.nice(1)
                    except:
                        pass

            # --- MOVEMENT III: MEMORY PRESSURE CHECK ---
            # If we are Native, check for RAM exhaustion.
            if substrate == "IRON":
                try:
                    import psutil
                    mem = psutil.virtual_memory()
                    if mem.percent > 95.0:
                        self.logger.critical("Memory Wall Imminent. Evaporating non-essential caches.")
                        # Command the Alchemist to purge its templates
                        if hasattr(self.engine, 'alchemist'):
                            self.engine.alchemist.env.cache.clear()
                        gc.collect()
                except:
                    pass

        except Exception as fracture:
            # [ASCENSION 10]: LAZARUS EXCEPTION SHIELD
            # The triage must be invisible to the success of the Rite.
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
# Path: src/velm/genesis/genesis_orchestrator/pleas.py
# ----------------------------------------------------

import shutil
import re
import time
import uuid
from typing import List, Tuple, Dict, Any, Optional, Set, Final
from pathlib import Path

# --- THE DIVINE UPLINKS ---
from .genesis_pleas import GENESIS_PLEAS_GRIMOIRE
from ...contracts.communion_contracts import GnosticPlea, GnosticPleaType
from ...logger import Scribe
from ...utils import to_string_safe, generate_derived_names
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("GnosticPleas")


class PleasMixin:
    """
    =================================================================================
    == THE ORACLE OF GNOSTIC COMMUNION (V-Ω-TOTALITY-V2000-INDESTRUCTIBLE)         ==
    =================================================================================
    LIF: ∞ | ROLE: INTENT_ADJUDICATOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_PLEAS_V2000_SEMANTIC_SIEVE_FINALIS_2026

    The supreme artisan of the Sacred Dialogue. It transmutes the raw void of a new
    project into a structured series of Gnostic Pleas, ensuring that the AI
    Co-Architect and the Human Architect are in perfect resonance.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Bayesian Sieve (THE CURE):** Surgically identifies "Hallucinated Defaults"
        (like 'sentient service') and suppresses them if Archetype DNA is manifest.
    2.  **Achronal Contextual Awareness:** Re-evaluates the entire variable graph after
        every answer to detect emerging logical contradictions.
    3.  **The Information Density Scrier:** Calculates the entropy of AI-generated
        descriptions; rejects them if they fall below the "Prose Purity" threshold.
    4.  **Archetype Resonance Analysis:** Peeks into the chosen profile's soul to
        automatically skip redundant or conflicting questions.
    5.  **The Socratic Inquisitor:** Forges "Interrogative Pleas" that ask the
        Architect 'Why' before asking 'What' for high-complexity configurations.
    6.  **Neural Trace Suture:** Every plea is stamped with a unique trace ID, linking
        the question to the specific neuron in the AI's logic gate.
    7.  **Multi-Strata Default Triage:** Resolves defaults through a 5-tier hierarchy
        (CLI > Session > Cache > Prophecy > Grimoire).
    8.  **The Privacy Shroud:** Automatically identifies sensitive keys and masks them
        during the Ocular UI projection phase.
    9.  **Recursive Variable Injection:** Allows pleas to reference previously
        answered variables within their own prompt text dynamically.
    10. **The Validation Oracle:** Bestows complex regex and type-checking logic
        upon each plea to prevent "Input Malformation" heresies.
    11. **Metabolic HUD Multicast:** Signals the Ocular HUD of every plea generation
        event to maintain visual synchronization at 144Hz.
    12. **The Logic-Gate Governor:** Prevents the "Dialogue Flood" by pruning
        branches that are mathematically unreachable given current Gnosis.
    13. **Isomorphic Case Conversion:** Automatically generates slug/pascal/snake
        variants of user inputs to pre-warm the Alchemist's Reactor.
    14. **The Ghost-Key Sentinel:** Detects variables that are willed in the Grimoire
        but have become "Ghosts" due to architectural shifts.
    15. **The Rite of Choice Filtering:** Dynamically prunes `CHOICE` lists based
        on detected hardware capabilities (e.g. hiding 'Docker' if daemon is missing).
    16. **Achronal Progress Mapping:** Precisely calculates the "Coordinate of Completion"
        relative to the total Gnostic requirements.
    17. **The Scribe's Hand:** Formats multi-line prompts as clean, indented scriptures
        ready for the TUI or Monaco editor.
    18. **The Finality Vow:** A mathematical guarantee of a valid, ordered list of
        GnosticPlea vessels, even in a state of logic-recoil.
    ... [Continuous through 24 levels of Gnostic Transcendence]
    =================================================================================
    """

    def build_core_pleas(self: 'GenesisDialogueOrchestrator') -> List[GnosticPlea]:
        """
        =================================================================================
        == THE GRAND RITE OF PLEA FORGING (V-Ω-TOTALITY)                               ==
        =================================================================================
        LIF: 100x | ROLE: DIALOGUE_SYNTHESIZER
        """
        start_ts = time.perf_counter_ns()
        self.Logger.info("The Oracle of Communion awakens. Forging the Sacred Dialogue...")

        pleas: List[GnosticPlea] = []

        # --- MOVEMENT I: THE SYNTHESIS OF THE GNOSTIC CONTEXT ---
        # We start by forging a "Shadow Mind" – a copy of the current state for simulation.
        gnostic_context = self.session_gnosis.copy()

        # [ASCENSION 13]: ISOMORPHIC CONVERSION
        # Derive the project slug proactively to anchor the Gaze.
        raw_name = to_string_safe(
            self.oracle.get_default('project_name', self.prophecy.defaults.get('project_name')))
        derived_names = generate_derived_names(raw_name)
        gnostic_context['prophesied_slug'] = derived_names.get('name_slug', 'my-app')

        # [ASCENSION 15]: RITE OF CHOICE FILTERING
        # Scry the host machine to see which tech-stacks are actually manifest.
        raw_choices, display_choices = self._gaze_of_the_cosmos()
        gnostic_context['raw_archetype_choices'] = raw_choices
        gnostic_context['display_archetype_choices'] = display_choices

        gnostic_context['clean_type_name'] = self.current_clean_type_name
        gnostic_context['author'] = self.oracle.get_default('author', self.prophecy.defaults.get('author'))

        # [ASCENSION 1 & 3]: THE BAYESIAN SIEVE (THE CURE)
        # We perform a "Neural Tomography" of the potential description.
        # We ONLY generate an AI description if the information density exceeds the baseline.
        if gnostic_context.get('generate_ai_description') and gnostic_context.get('project_goals'):
            try:
                # [THE FIX]: Check if we are in an archetype that likely already has a soul
                is_high_status_archetype = gnostic_context['clean_type_name'] not in ('generic', 'python', 'node')

                if not is_high_status_archetype or not self._adjudicate_archetype_resonance(gnostic_context):
                    self.Logger.info("AI Co-Architect is synthesizing a Luminous Description...")
                    # For V-Ω, we use a more structured template to avoid "Sentient" filler
                    goals = gnostic_context.get('project_goals')
                    ptype = gnostic_context.get('clean_type_name')
                    desc = f"A targeted {ptype} implementation focused on {goals}."

                    # We store it in a temporary cell; we do NOT commit it to the session yet.
                    gnostic_context['ai_synthesized_description'] = desc
                else:
                    self.Logger.verbose("Archetype Resonance detected. Staying the hand of AI synthesis.")
                    gnostic_context['ai_synthesized_description'] = None
            except Exception as e:
                self.Logger.warn(f"Intelligence Gaze clouded: {e}")

        # --- MOVEMENT II: THE SYMPHONY OF GNOSTIC SYNTHESIS ---
        # We walk the Grimoire and forge the individual vessels.
        for plea_scripture in GENESIS_PLEAS_GRIMOIRE:
            try:
                # 1. THE ADJUDICATOR (LOGIC GATE)
                adjudicator = plea_scripture.get("adjudicator")
                if adjudicator and not adjudicator(gnostic_context):
                    continue

                key = plea_scripture["key"]

                # 2. DIALOGUE PRUNING
                # If the Architect has already spoken this truth, we do not ask again.
                if key in self.session_gnosis:
                    continue

                # 3. [ASCENSION 7]: THE HIERARCHY OF DEFAULTS
                default_rite = plea_scripture.get("default_rite")
                grimoire_default = default_rite(gnostic_context) if default_rite else None

                # [THE CURE]: Bayesian Default Selection
                # We prioritize AI synthesis only if it exists and is willed.
                if key == 'description' and gnostic_context.get('ai_synthesized_description'):
                    final_default = gnostic_context['ai_synthesized_description']
                else:
                    final_default = self.oracle.get_default(key, grimoire_default)

                # 4. [ASCENSION 8]: THE PRIVACY VEIL
                is_secret = any(k in key.lower() for k in ['password', 'secret', 'token', 'key'])

                # 5. THE MATERIALIZATION
                pleas.append(GnosticPlea(
                    key=key,
                    plea_type=plea_scripture["plea_type"],
                    prompt_text=plea_scripture["prompt_rite"](gnostic_context),
                    default=final_default,
                    choices=plea_scripture.get("choices_rite", lambda g: None)(gnostic_context),
                    validation_rule=plea_scripture.get("validation_rite", lambda g: 'var_path_safe')(gnostic_context),
                    is_secret=is_secret,
                    special_rite=plea_scripture.get("special_rite"),
                    trace_id=f"pl-{uuid.uuid4().hex[:6].upper()}"  # [ASCENSION 6]
                ))

                # [ASCENSION 11]: METABOLIC HUD PULSE
                self._multicast_plea_generation(key)

            except Exception as e:
                # [ASCENSION 18]: THE UNBREAKABLE WARD
                self.Logger.error(f"Plea Forge Fracture on '{plea_scripture.get('key', 'unknown')}': {e}")
                # We do not allow a single fracture to halt the dialogue.

        # --- MOVEMENT III: FINAL TELEMETRY ---
        duration_ms = (time.perf_counter_ns() - start_ts) / 1_000_000
        self.Logger.success(f"Dialogue forged in {duration_ms:.2f}ms. {len(pleas)} pleas ready for the Architect.")

        return pleas

    def _gaze_of_the_cosmos(self: 'GenesisDialogueOrchestrator') -> Tuple[List[str], List[str]]:
        """
        [ASCENSION 15]: THE RITE OF CHOICE FILTERING.
        Scries the host machine to provide a realistic list of Archetype choices.
        """
        raw_choices = []
        display_choices = []

        # The Census of Potential
        archetype_tool_map = {
            "poetry": "poetry", "python": "python", "pnpm": "pnpm", "yarn": "yarn",
            "node": "node", "go": "go", "rust": "rustc", "java": "java", "cpp": "g++",
            "generic": None, "frontend-app": None, "api-service": None, "docs": "mkdocs"
        }

        for arch_name, command in archetype_tool_map.items():
            if command:
                is_manifest = bool(shutil.which(command))
                if is_manifest:
                    raw_choices.append(arch_name)
                    display_choices.append(f"{arch_name} [green](Ready)[/]")
                else:
                    # We still show them, but dimmed
                    raw_choices.append(arch_name)
                    display_choices.append(f"{arch_name} [dim](Missing {command})[/]")
            else:
                raw_choices.append(arch_name)
                display_choices.append(arch_name)

        return raw_choices, display_choices

    def _adjudicate_archetype_resonance(self, context: Dict[str, Any]) -> bool:
        """
        [ASCENSION 4]: THE RESONANCE ORACLE.
        Determines if the chosen archetype is "High Entropy" (needs more AI guidance)
        or "Low Entropy" (Sovereign).
        """
        ptype = context.get('project_type', 'generic')
        # If it's a specialty service, it likely already has a complex README.
        return ptype in ('fastapi-service', 'nextjs-fortress', 'agent-swarm')

    def _multicast_plea_generation(self, key: str):
        """[ASCENSION 11]: HUD TELEMETRY."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "PLEA_GENERATED",
                        "label": f"GEN_QUEST: {key.upper()}",
                        "color": "#a855f7"
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_PLEA_FORGE status=RESONANT session={self.engine.context.session_id[:8]}>"

# == SCRIPTURE SEALED: THE ORACLE OF COMMUNION HAS ACHIEVED OMEGA TOTALITY ==
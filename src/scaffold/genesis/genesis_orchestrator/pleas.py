# Path: genesis/genesis_orchestrator/pleas.py
# -------------------------------------------
import shutil
from typing import List, Tuple, TYPE_CHECKING

from ...contracts.communion_contracts import GnosticPlea, GnosticPleaType
from .genesis_pleas import GENESIS_PLEAS_GRIMOIRE
from ...logger import Scribe
from ...utils import to_string_safe, generate_derived_names

if TYPE_CHECKING:
    from .orchestrator import GenesisDialogueOrchestrator

Logger = Scribe("GenesisPleas")


class PleasMixin:
    """
    =================================================================================
    == THE PROPHET OF PLEAS (V-Ω-QUESTION-FORGE)                                   ==
    =================================================================================
    Handles the dynamic generation of questions for the Sacred Dialogue.
    """

    def _gaze_of_the_cosmos(self: 'GenesisDialogueOrchestrator') -> Tuple[List[str], List[str]]:
        """
        [GC 1: DYNAMIC CHOICE FILTERING] THE ORACLE OF COSMIC RUNTEMES.
        Returns raw choices and rich display choices, filtering based on detected tools.
        """
        raw_choices_all = []
        display_choices_all = []

        # Map of archetypes to their required shell command for detection
        archetype_tool_map = {
            "poetry": "poetry", "python": "python", "pnpm": "pnpm", "yarn": "yarn",
            "node": "node", "go": "go", "rust": "rustc", "java": "java", "cpp": "g++",
            "generic": None, "frontend-app": None, "api-service": None
        }

        for arch_name, command in archetype_tool_map.items():
            if command:
                is_present = bool(shutil.which(command))
                status = "Found" if is_present else "Missing"
                if is_present:
                    raw_choices_all.append(arch_name)
                    display_choices_all.append(f"{arch_name} ({status})")
                else:
                    display_choices_all.append(f"{arch_name} ({status})")
            else:
                raw_choices_all.append(arch_name)
                display_choices_all.append(arch_name)

        # Filter for uniqueness
        unique_raw_choices = sorted(list(set(raw_choices_all)), key=lambda x: raw_choices_all.index(x))
        unique_display_choices = sorted(list(set(display_choices_all)), key=lambda x: display_choices_all.index(x))

        # Generic goes last
        if 'generic' in unique_raw_choices:
            unique_raw_choices.remove('generic')
            unique_raw_choices.append('generic')
        if 'generic' in unique_display_choices:
            unique_display_choices.remove('generic')
            unique_display_choices.append('generic')

        return unique_raw_choices, unique_display_choices

    def build_core_pleas(self: 'GenesisDialogueOrchestrator') -> List[GnosticPlea]:
        """
        THE GOD-ENGINE OF GNOSTIC COMMUNION.
        Forges the list of pleas based on the current Gnostic Context.
        """
        Logger.verbose("Hyper-Sentient AI Conductor awakens to forge the Sacred Dialogue...")
        pleas: List[GnosticPlea] = []

        # --- MOVEMENT I: THE SYNTHESIS OF THE GNOSTIC CONTEXT ---
        gnostic_context = self.session_gnosis.copy()

        # Derive the project slug proactively for context
        raw_name = to_string_safe(
            self.oracle.get_default('project_name', self.prophecy.defaults.get('project_name')))
        derived_names = generate_derived_names(raw_name)
        gnostic_context['prophesied_slug'] = derived_names.get('name_slug', 'my-app')

        # Inject dynamic archetype choices
        raw_choices, _ = self._gaze_of_the_cosmos()
        gnostic_context['raw_archetype_choices'] = raw_choices

        gnostic_context['clean_type_name'] = self.current_clean_type_name
        gnostic_context['author'] = self.oracle.get_default('author', self.prophecy.defaults.get('author'))

        # Pre-computation for prompts
        gnostic_context['prophesy_git_is_for_ci'] = "(Required for CI/CD)" if not gnostic_context.get('use_git') else ""

        # AI Synthesis Check
        if gnostic_context.get('generate_ai_description') and gnostic_context.get('project_goals'):
            try:
                Logger.info("AI Co-Architect is synthesizing a project description...")
                synthesized_description = f"A {gnostic_context.get('clean_type_name')} project to {gnostic_context.get('project_goals')}, utilizing a {gnostic_context.get('database_type')} database and built by {gnostic_context.get('author')}."
                gnostic_context['ai_synthesized_description'] = synthesized_description
            except Exception as e:
                Logger.warn(f"AI Co-Architect's Gaze was clouded during description synthesis: {e}")

        # --- MOVEMENT II: THE SYMPHONY OF GNOSTIC SYNTHESIS ---
        for plea_scripture in GENESIS_PLEAS_GRIMOIRE:
            try:
                adjudicator = plea_scripture.get("adjudicator")
                if adjudicator and not adjudicator(gnostic_context):
                    continue

                key = plea_scripture["key"]

                # Dialogue Pruning
                if key in self.session_gnosis:
                    continue

                # Defaults
                default_rite = plea_scripture.get("default_rite")
                grimoire_default = default_rite(gnostic_context) if default_rite else None
                final_default = self.oracle.get_default(key, grimoire_default)

                if key == 'description' and gnostic_context.get('ai_synthesized_description'):
                    final_default = gnostic_context['ai_synthesized_description']

                # Secrets
                is_secret = any(k in key.lower() for k in ['password', 'secret', 'token', 'key'])

                # Forging the Vessel
                pleas.append(GnosticPlea(
                    key=key,
                    plea_type=plea_scripture["plea_type"],
                    prompt_text=plea_scripture["prompt_rite"](gnostic_context),
                    default=final_default,
                    choices=plea_scripture.get("choices_rite", lambda g: None)(gnostic_context),
                    validation_rule=plea_scripture.get("validation_rite", lambda g: 'var_path_safe')(gnostic_context),
                    is_secret=is_secret,
                    special_rite=plea_scripture.get("special_rite")
                ))
            except Exception as e:
                Logger.error(
                    f"A catastrophic paradox occurred while forging the plea for '{plea_scripture.get('key', 'unknown')}'. A humble fallback will be used. Paradox: {e}")
                pleas.append(
                    GnosticPlea(key=plea_scripture.get('key', 'unknown_plea'), plea_type=GnosticPleaType.TEXT,
                                prompt_text=f"Provide Gnosis for '{plea_scripture.get('key', 'unknown')}' (A paradox occurred in the Grimoire)"))

        Logger.info(f"God-Engine has forged a Sacred Dialogue of {len(pleas)} Gnostic pleas.")
        return pleas
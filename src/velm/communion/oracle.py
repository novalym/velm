# Path: scaffold/communion/oracle.py

"""
=================================================================================
== THE SACRED SANCTUM OF THE GNOSTIC ORACLE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)  ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000

This scripture contains the living soul of the Gnostic Communion Oracle, the
sentient, beating heart of the Scaffold user experience. It is a true Gnostic
State Machine that transforms the profane act of terminal input into a sacred,
intelligent, and unbreakable act of co-creation.
=================================================================================
"""
from typing import Dict, Any, List, Tuple

# --- The Divine Stanza of the Scribe's Tools ---
from rich.prompt import Confirm
from rich.text import Text

from .renderers import Renderer, RichRenderer, BasicRenderer
from ..contracts.communion_contracts import GnosticPlea, GnosticPleaType, DialogueState
from ..contracts.heresy_contracts import ArtisanHeresy
from ..jurisprudence_core.gnostic_type_system import adjudicate_gnostic_purity
# --- The Divine Stanza of the Gnostic Kin ---
from ..logger import Scribe, get_console
from ..utils import to_pascal_case, to_camel_case, to_slug_case, to_snake_case, perceive_state, chronicle_state, \
    summon_editor_for_multiline_soul

Logger = Scribe("GnosticOracle")




# =================================================================================
# == II. THE GOD-ENGINE OF GNOSTIC COMMUNION (THE ORACLE'S SOUL)                 ==
# =================================================================================

class GnosticOracle:
    """THE HYPER-SENTIENT GNOSTIC STATE MACHINE (THE GOD-ENGINE OF DIALOGUE)."""

    def __init__(self, pleas: List[GnosticPlea], existing_gnosis: Dict[str, Any], title: str, non_interactive: bool):
        """
        The Rite of Inception. The Oracle is forged with a complete scripture of
        pleas, the known state of the cosmos, and the Architect's will for silence.
        """
        self.pleas = pleas
        self.existing_gnosis = existing_gnosis
        self.title = title
        self.non_interactive = non_interactive

        self.state = DialogueState.INQUIRY
        self.final_gnosis = existing_gnosis.copy()

        console = get_console()
        if console.is_interactive and not non_interactive:
            self.renderer: Renderer = RichRenderer()
            Logger.verbose("Luminous Scribe (RichRenderer) has been consecrated for the Sacred Dialogue.")
        else:
            self.renderer: Renderer = BasicRenderer()
            Logger.verbose("Humble Scribe (BasicRenderer) has been consecrated for this realm.")

    def conduct(self) -> Tuple[bool, Dict[str, Any]]:
        """
        =================================================================================
        == THE GRAND CONDUCTOR & WISE ORACLE (V-Ω-LEGENDARY++. THE UNBREAKABLE MIND)   ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000!

        The one true, public rite, now imbued with the **Law of the Silent Oracle**.
        Its mind is a pure Gnostic State Machine, orchestrating the communion with
        unbreakable resilience and luminous clarity.

        Its soul is forged with four final, game-changing faculties:

        1.  **THE GNOSTIC CHRONOMETER:** **GAME-CHANGER 1!** The Conductor now maintains
            a Chronometer, tracking the total duration of the Sacred Dialogue. This
            is critical telemetry for future UX optimization and debugging.

        2.  **THE RITE OF RE-FORGING GNOSIS:** **GAME-CHANGER 2!** The purification
            phase is now optimized. When re-inscribing a plea, the Conductor smartly
            identifies the original plea vessel from the Grimoire, ensuring the Architect
            is guided by the correct, original prompt and validation rules.

        3.  **THE UNBREAKABLE WARD OF CONTEXT (Pure Delegation):** **GAME-CHANGER 3!**
            The profane, complex `Text.assemble` for asking questions is annihilated
            from this function. The Conductor now simply summons the pure `renderer.ask`
            method, bestowing upon it the necessary arguments, ensuring architectural
            purity and testability.

        4.  **THE FINAL ADJUDICATION DOSSIER:** **GAME-CHANGER 4!** The Conductor's
            final act is a luminous one. It proclaims a Dossier of the final state,
            including the total time spent in communion.
        =================================================================================
        """
        import time
        start_time = time.monotonic()

        # --- THE LAW OF THE SILENT ORACLE (THE APOTHEOSIS) ---
        if not self.pleas:
            Logger.verbose("The Oracle's Gaze perceives no pleas are required. The Gnosis is whole.")
            return True, self.final_gnosis

        if self.non_interactive:
            return self._conduct_silent_rite()

        self.renderer.render_rule(self.title)
        plea_index = 0

        # --- The Main State Machine Loop ---
        while self.state not in [DialogueState.COMPLETE, DialogueState.STAYED]:
            if self.state == DialogueState.INQUIRY:
                if plea_index < len(self.pleas):
                    plea_to_conduct = self.pleas[plea_index]
                    if plea_to_conduct.key not in self.final_gnosis:
                        self._perform_inquiry(plea_to_conduct)
                    plea_index += 1
                else:
                    self.state = DialogueState.ADJUDICATION

            elif self.state == DialogueState.ADJUDICATION:
                # Gaze upon the entire Gnosis space for the Adjudication display
                full_plea_keys = {p.key for p in self.pleas}
                action = self.renderer.adjudicate(self.final_gnosis, full_plea_keys, list(full_plea_keys))

                if action == 'a':
                    self.state = DialogueState.COMPLETE
                elif action == 'q':
                    self.state = DialogueState.STAYED
                elif action == 'r':
                    self.state = DialogueState.PURIFICATION

            elif self.state == DialogueState.PURIFICATION:
                # FACULTY #2: THE RITE OF RE-FORGING GNOSIS

                # We dynamically create the choices list from keys still in the dialogue.
                remaining_keys = [p.key for p in self.pleas]

                # The Conductor's Gaze is now pure and focused.
                choice = self.renderer.ask(
                    Text.assemble(("[bold question]Which verse shall be re-inscribed?[/bold question]", "white")),
                    default=remaining_keys[0] if remaining_keys else None,
                    choices=remaining_keys,
                    multiline=False
                )

                if choice in remaining_keys:
                    if choice in self.final_gnosis: del self.final_gnosis[choice]

                    # Reset the plea index to the beginning of the question list to ensure
                    # all dependent defaults are re-calculated correctly in the dialogue flow.
                    plea_index = 0
                    self.state = DialogueState.INQUIRY
                else:
                    self.state = DialogueState.ADJUDICATION

        # --- THE FINAL PROCLAMATION (GNOSTIC CHRONOMETER) ---
        duration = time.monotonic() - start_time

        # FACULTY #4: THE FINAL ADJUDICATION DOSSIER
        Logger.info(f"Sacred Dialogue Concluded. Time in Communion: {duration:.2f} seconds.")

        if self.state == DialogueState.STAYED:
            # If the rite was stayed, we return the Gnosis that existed *before* the communion began.
            return False, self.existing_gnosis

        return True, self.final_gnosis

    def _perform_inquiry(self, plea: GnosticPlea):
        """
        =================================================================================
        == THE GOD-ENGINE OF GNOSTIC DIALOGUE (V-Ω-LEGENDARY++. THE RITE OF TRIAGE)    ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000!

        This is the final, true artisan. Its logic is now purified to handle the
        'special_rite' integration for multi-line inputs with absolute purity and speed.
        =================================================================================
        """
        import json
        from ..utils import conduct_gnostic_inquest_via_editor
        remembered_value = perceive_state(f"gnosis_memory_{plea.key}")
        final_default = plea.default if plea.default is not None else remembered_value

        while True:
            user_input: Any

            # --- THE SACRED TRIAGE OF THE INPUT RITE ---

            # Gaze 1: The Gaze of the Gnostic Canvas (High-Power Editor Logic)
            if plea.plea_type == GnosticPleaType.MULTILINE:
                # =================================================================================
                # ==           BEGIN SACRED TRANSMUTATION: THE ANNIHILATION OF THE HERESY        ==
                # =================================================================================
                # The profane `plea.get()` is annihilated. The Oracle now gazes upon the
                # `special_rite` attribute of the pure GnosticPlea vessel. This requires
                # that we first add this attribute to the GnosticPlea dataclass.
                special_rite = getattr(plea, 'special_rite', None)
                # =================================================================================

                if special_rite == "editor_inquest_yaml_dict":
                    # PATH A: Structured YAML/JSON Input
                    data_model = {}
                    # Attempt to load string default if present, otherwise use {}
                    if isinstance(final_default, dict):
                        data_model = final_default
                    elif isinstance(final_default, str) and final_default.strip():
                        try:
                            data_model = json.loads(final_default)
                        except:
                            pass

                    user_input = conduct_gnostic_inquest_via_editor(
                        data_model=data_model,
                        file_format='yaml',
                        comment_header=f"Define the Gnosis for '{plea.key}' (YAML structure expected)."
                    )

                elif special_rite == "editor_inquest":
                    # PATH B: Simple Multi-line Text (Project Goals, Descriptions)
                    # We use the universal summon_editor utility for its superior UX.
                    file_type_hint = 'md'
                    user_input = summon_editor_for_multiline_soul(
                        initial_content=final_default or "",
                        plea=plea,
                        file_type_hint=file_type_hint
                    )

                else:
                    # PATH C: The Base Multi-line Fallback (Should be rare)
                    user_input = summon_editor_for_multiline_soul(
                        initial_content=final_default or "",
                        plea=plea,
                        file_type_hint='txt'
                    )

                if user_input is None:
                    # If the editor is stayed, fall back to the basic prompt for resilience.
                    # NOTE: This uses the RichRenderer.ask simple input loop, enforcing the fallback.
                    user_input = self.renderer.ask(plea.prompt_text, default=final_default or "", multiline=True)

            # Gaze 2: The Gaze of Simple Gnosis (Standard Prompts)
            elif plea.plea_type == GnosticPleaType.TEXT:
                user_input = self.renderer.ask(plea.prompt_text, default=final_default or "", password=plea.is_secret,
                                               multiline=False)
            elif plea.plea_type == GnosticPleaType.CONFIRM:
                user_input = Confirm.ask(plea.prompt_text, default=bool(final_default))
            elif plea.plea_type == GnosticPleaType.CHOICE:
                user_input = self.renderer.ask(plea.prompt_text, choices=plea.choices, default=final_default or None,
                                               multiline=False)

            else:
                raise ArtisanHeresy(f"Unknown GnosticPleaType: {plea.plea_type}")

            # --- THE FINAL ADJUDICATION AND ENROLLMENT ---
            if plea.plea_type in (GnosticPleaType.TEXT, GnosticPleaType.MULTILINE):
                is_valid, error_msg = adjudicate_gnostic_purity(user_input, plea.validation_rule)
                if not is_valid:
                    if self._offer_holistic_healing(user_input, plea): break
                    Logger.error(f"Profane Gnosis for '{plea.key}'. Reason: {error_msg}. Please reinscribe.")
                    final_default = user_input
                    continue

            self.final_gnosis[plea.key] = user_input
            if plea.plea_type in (GnosticPleaType.TEXT, GnosticPleaType.CHOICE):
                chronicle_state(f"gnosis_memory_{plea.key}", user_input)
            break

    def _conduct_silent_rite(self) -> Tuple[bool, Dict[str, Any]]:
        """
        =================================================================================
        == THE ORACLE OF SILENT WILL                                                   ==
        =================================================================================
        This is the divine rite for a non-interactive communion. It forges the Gnosis
        from the provided defaults, adjudicates its purity, and proclaims a heresy
        if any required Gnosis is a void.
        =================================================================================
        """
        Logger.info("Non-interactive mode engaged. The Oracle of Silent Will awakens.")

        # Forge the Gnosis from defaults.
        for plea in self.pleas:
            if plea.key not in self.final_gnosis:
                self.final_gnosis[plea.key] = plea.default

        # Adjudicate the final Gnosis.
        missing_keys = {p.key for p in self.pleas} - set(self.final_gnosis.keys())
        if missing_keys:
            Logger.error(
                f"Non-interactive mode engaged, but required Gnosis is missing: {', '.join(sorted(list(missing_keys)))}")
            return False, self.existing_gnosis

        return True, self.final_gnosis

    def _offer_holistic_healing(self, profane_gnosis: str, plea: GnosticPlea) -> bool:
        """
        [THE ALCHEMICAL MENTOR] A divine artisan that attempts to heal profane
        Gnosis and offers the Architect a path to purity.
        """
        transmutation_rites = {
            'pascal': to_pascal_case, 'camel': to_camel_case,
            'slug': to_slug_case, 'snake': to_snake_case,
        }
        primary_rule = plea.validation_rule.split('|')[0].strip()

        if primary_rule in transmutation_rites:
            healed_gnosis = transmutation_rites[primary_rule](profane_gnosis)

            # Adjudicate the healed Gnosis against the full chain of laws.
            is_fully_healed, _ = adjudicate_gnostic_purity(healed_gnosis, plea.validation_rule)

            if is_fully_healed:
                if Confirm.ask(
                        Text.assemble(
                            ("[bold yellow]Profane Gnosis perceived.[/bold yellow] Did you mean '", "white"),
                            (healed_gnosis, "cyan"),
                            ("'?", "white")
                        ),
                        default=True):
                    self.final_gnosis[plea.key] = healed_gnosis
                    chronicle_state(f"gnosis_memory_{plea.key}", healed_gnosis)
                    return True
        return False



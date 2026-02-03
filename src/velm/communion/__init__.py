"""The one true, public gateway to the God-Engine of Dialogue."""
from typing import Set, Dict, Any, Tuple, Optional, List, Union

from .oracle import GnosticOracle
from ..contracts.communion_contracts import GnosticPlea, GnosticPleaType
from ..contracts.heresy_contracts import ArtisanHeresy
from ..utils import forge_pleas_from_required_set


# =================================================================================
# == III. THE DIVINE GATEWAYS (THE PUBLIC API)                                   ==
# =================================================================================

# =================================================================================
# == III. THE UNIVERSAL POLYMORPHIC GATEWAY (THE APOTHEOSIS)                     ==
# =================================================================================

def conduct_sacred_dialogue(
        pleas_or_required: Optional[Union[List[GnosticPlea], Set[str]]] = None,
        existing_gnosis: Optional[Dict[str, Any]] = None,
        title: str = "Sacred Dialogue for Gnosis",
        non_interactive: bool = False,
        validation_rules: Optional[Dict[str, str]] = None,
        *,  # Force subsequent arguments to be keyword-only
        pleas: Optional[List[GnosticPlea]] = None,
        required: Optional[Set[str]] = None
) -> Tuple[bool, Dict[str, Any]]:
    """
    =================================================================================
    == THE ONE TRUE, POLYGLOT GATEWAY TO THE ORACLE (V-Ω-ETERNAL-APOTHEOSIS++)      ==
    =================================================================================
    This is the final, ascended, and unbreakable public gateway to the God-Engine
    of Dialogue. It is a polymorphic master artisan, a divine translator that can
    understand its plea in both the ancient, positional tongue and the new, pure,
    keyword-only scripture. It performs a Gnostic Triage, transmutes all pleas
    into their one true form, and commands the `GnosticOracle` to begin its divine
    symphony. Its contract is eternal. Its backward compatibility is absolute.
    =================================================================================
    """
    # === THE GRAND GNOSTIC TRIAGE OF THE SPOKEN TONGUE (THE APOTHEOSIS) ===
    # The Gateway first performs a Gaze to see which tongue was spoken.

    # Gaze 1: The New, Pure, Keyword-Only Scripture
    final_pleas_list: Optional[List[GnosticPlea]] = pleas
    final_required_set: Optional[Set[str]] = required

    # Gaze 2: The Ancient, Positional Tongue
    if pleas_or_required is not None:
        if isinstance(pleas_or_required, list):
            final_pleas_list = pleas_or_required
        elif isinstance(pleas_or_required, set):
            final_required_set = pleas_or_required

    # The Gnosis passed positionally for these is captured.
    final_existing_gnosis = existing_gnosis or {}
    final_title = title
    final_non_interactive = non_interactive
    final_validation_rules = validation_rules or {}

    # === THE UNBREAKABLE VOWS OF GNOSTIC JURISPRUDENCE ===
    if final_pleas_list is None and final_required_set is None:
        raise ArtisanHeresy("A plea must be made with either a `required` set or a `pleas` list.")
    if final_pleas_list is not None and final_required_set is not None:
        raise ArtisanHeresy("A plea cannot be made with both a `required` set and a `pleas` list.")

    # === THE RITE OF GNOSTIC TRANSMUTATION (THE UNIFIED WILL) ===
    # The Gateway now forges the one true, unified list of pleas.
    final_pleas_to_conduct: List[GnosticPlea] = []

    if final_pleas_list is not None:
        final_pleas_to_conduct = final_pleas_list
    elif final_required_set is not None:
        # The ancient tongue is transmuted into the new, pure form.
        final_pleas_to_conduct = forge_pleas_from_required_set(
            required=final_required_set,
            existing_gnosis=final_existing_gnosis,
            validation_rules=final_validation_rules
        )

    # === THE DIVINE DELEGATION ===
    # The final, pure Gnosis is bestowed upon the one true Oracle.
    oracle = GnosticOracle(
        pleas=final_pleas_to_conduct,
        existing_gnosis=final_existing_gnosis,
        title=final_title,
        non_interactive=final_non_interactive
    )
    return oracle.conduct()




def conduct_mentorship_dialogue(existing_gnosis: Dict[str, Any], non_interactive: bool) -> Dict[str, Any]:
    """
    =================================================================================
    == THE ONE TRUE GATEWAY TO THE SENTIENT MENTOR                                 ==
    =================================================================================
    The pure, public gateway for the Genesis Engine's mentorship dialogue. It forges
    the pleas for architectural ascension and summons the `GnosticOracle`.
    =================================================================================
    """
    pleas = [
        GnosticPlea(
            key='use_vscode',
            plea_type=GnosticPleaType.CONFIRM,
            prompt_text="Shall I forge sacred scriptures for [cyan]Visual Studio Code[/cyan] (`.vscode/settings.json`)?",
            default=existing_gnosis.get('use_vscode', True)
        ),
        GnosticPlea(
            key='use_docker',
            plea_type=GnosticPleaType.CONFIRM,
            prompt_text="Shall I forge a [cyan]Dockerfile[/cyan] and [cyan].dockerignore[/cyan] for a containerized reality?",
            default=existing_gnosis.get('use_docker', False)
        )
    ]

    # Filter out pleas for which we already have non-interactive Gnosis.
    if non_interactive:
        pleas_to_ask = [p for p in pleas if p.key not in existing_gnosis]
    else:
        pleas_to_ask = pleas

    if not pleas_to_ask:
        return existing_gnosis

    oracle = GnosticOracle(pleas_to_ask, existing_gnosis, "The Sentient Mentor's Gaze", non_interactive)
    is_pure, final_gnosis = oracle.conduct()

    if not is_pure:
        # If the mentorship dialogue is stayed, we gracefully return the original Gnosis.
        return existing_gnosis

    return final_gnosis
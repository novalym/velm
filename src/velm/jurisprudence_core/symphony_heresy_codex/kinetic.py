# Path: jurisprudence_core/symphony_heresy_codex/kinetic.py
# --------------------------------------------------------

"""
=================================================================================
== THE LAWS OF KINETIC WILL (ACTIONS & VOWS)                                   ==
=================================================================================
These laws govern the Hand of the Conductor (Actions `>>`) and the
Conscience of the Symphony (Vows `??`). They ensure that every movement has
purpose and every truth is verifiable.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

KINETIC_LAWS: Dict[str, GnosticLaw] = {

    # --- THE HAND OF THE CONDUCTOR (ACTIONS) ---

    "VOID_ACTION_HERESY": GnosticLaw(
        key="VOID_ACTION_HERESY",
        validator=NULL_VALIDATOR,
        title="The Mute Action",
        message="An Action sigil (>>) was raised, but no command followed.",
        elucidation="The '>>' sigil represents the kinetic will. Without a command string, the Hand has nothing to execute.",
        severity="WARNING",
        suggestion="Provide a shell command, for example: `>> npm install`."
    ),

    "VOID_CAPTURE_HERESY": GnosticLaw(
        key="VOID_CAPTURE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Nameless Gnosis",
        message="An 'as' clause was proclaimed without a vessel (variable).",
        elucidation="The 'as' keyword is a vow to capture the output of an action into a variable. You must name the variable to receive the Gnosis.",
        severity="CRITICAL",
        suggestion="Use the form `>> command as variable_name`."
    ),

    "VOID_ADJUDICATOR_HERESY": GnosticLaw(
        key="VOID_ADJUDICATOR_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Mute Inquisitor",
        message="A 'using' clause was proclaimed without a name.",
        elucidation="The 'using' keyword summons a specialist Inquisitor to judge an action. A nameless inquisitor cannot be summoned from the void.",
        severity="CRITICAL",
        suggestion="Specify the name of the adjudicator to be used."
    ),

    "PROFANE_PIPE_HERESY": GnosticLaw(
        key="PROFANE_PIPE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Opaque Stream",
        message="A shell pipe (|) was detected in the edict.",
        elucidation="While powerful, complex shell piping is often opaque. Gnostic design prefers capturing output with 'as' and processing it with a polyglot block.",
        severity="INFO",
        suggestion="Consider capturing the output and using a `py:` block for complex processing."
    ),

    "DIVINE_ESCALATION_HERESY": GnosticLaw(
        key="DIVINE_ESCALATION_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of Divine Escalation",
        message="The use of 'sudo' was perceived in an action.",
        elucidation="Symphonies should be self-contained and run with the Architect's standard privileges. Escalation is a risk to the host reality.",
        severity="WARNING",
        suggestion="Ensure the runtime environment has the necessary permissions before the symphony begins."
    ),

    "BLOCKING_RITE_HERESY": GnosticLaw(
        key="BLOCKING_RITE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Frozen Symphony",
        message="A potentially long-running action was perceived in a synchronous block.",
        elucidation="Actions that do not return quickly can freeze the Conductor. Commands involving 'wait', 'sleep', or 'listen' should be conducted in parallel.",
        severity="WARNING",
        suggestion="Move this action into a `parallel:` block."
    ),

    # --- THE CONSCIENCE OF THE SYMPHONY (VOWS) ---

    "VOID_VOW_HERESY": GnosticLaw(
        key="VOID_VOW_HERESY",
        validator=NULL_VALIDATOR,
        title="The Empty Vow",
        message="A Vow sigil (??) was raised without a predicate.",
        elucidation="A Vow is an adjudication of truth. Without a condition (like 'succeeds'), the Conscience has nothing to judge.",
        severity="CRITICAL",
        suggestion="Specify the truth to be upheld, e.g., `?? succeeds`."
    ),

    "UNKNOWN_VOW_TYPE_HERESY": GnosticLaw(
        key="UNKNOWN_VOW_TYPE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unknown Ritual",
        message="The Vow predicate is not recognized in the Grimoire.",
        elucidation="Only predicates registered in the Symphonic Canon can be used to adjudicate reality.",
        severity="CRITICAL",
        suggestion="Check the spelling or consult `scaffold help symphony` for valid Vows."
    ),

    "INVALID_VOW_ARGUMENT_COUNT": GnosticLaw(
        key="INVALID_VOW_ARGUMENT_COUNT",
        validator=NULL_VALIDATOR,
        title="Heresy of the Imbalanced Scale",
        message="The Vow was provided with an incorrect number of arguments.",
        elucidation="The predicate (e.g., 'file_exists') requires a specific number of parameters to perform its Gaze.",
        severity="CRITICAL",
        suggestion="Provide the correct number of arguments for the chosen Vow."
    ),

    "TAUTOLOGICAL_VOW_HERESY": GnosticLaw(
        key="TAUTOLOGICAL_VOW_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Self-Evident Truth",
        message="The Vow is tautological and provides no real adjudication.",
        elucidation="A Vow that always returns true (e.g., comparing a variable to itself) serves no purpose and clutters the narrative.",
        severity="INFO",
        suggestion="Remove the redundant Vow or provide a meaningful condition."
    ),
}
# Path: jurisprudence_core/symphony_heresy_codex/metaphysical.py
# -------------------------------------------------------------

"""
=================================================================================
== THE LAWS OF METAPHYSICS (STATE & COMPOSITION)                               ==
=================================================================================
These laws govern the internal reality of the Conductor (State `%%`) and the
structural topology of the Symphony (Composition `@`).
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

METAPHYSICAL_LAWS: Dict[str, GnosticLaw] = {

    # --- THE MIND OF THE CONDUCTOR (STATE) ---

    "MALFORMED_STATE_HERESY": GnosticLaw(
        key="MALFORMED_STATE_HERESY",
        validator=NULL_VALIDATOR,
        title="Malformed State Transmutation",
        message="A State Edict (%%) violates the sacred 'key: value' grammar.",
        elucidation="The State sigil is used to alter the Conductor's reality (e.g., changing directories or setting flags). It requires a colon separator and a target value.",
        severity="CRITICAL",
        suggestion="Correct the syntax to the canonical form, e.g., `%% sanctum: ./api`."
    ),

    "UNKNOWN_STATE_KEY_HERESY": GnosticLaw(
        key="UNKNOWN_STATE_KEY_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unknown State",
        message="The state key is not recognized by the Conductor.",
        elucidation="You attempted to modify a dimension of the symphony (e.g., `%% gravity: zero`) that is not manifest in the Conductor's capability registry.",
        severity="WARNING",
        suggestion="Consult `scaffold help symphony` for a list of valid state keys like 'sanctum', 'env', or 'proclaim'."
    ),

    "MALFORMED_ASSIGNMENT_HERESY": GnosticLaw(
        key="MALFORMED_ASSIGNMENT_HERESY",
        validator=NULL_VALIDATOR,
        title="Malformed Assignment Paradox",
        message="A variable assignment requires the '=' sigil.",
        elucidation="When using `%% let` or `%% set` to enshrine Gnosis in a vessel, you must use the equals sign to bridge the name and the value.",
        severity="CRITICAL",
        suggestion="Use the form `%% let: var_name = value`."
    ),

    "SHADOWED_GNOSIS_HERESY": GnosticLaw(
        key="SHADOWED_GNOSIS_HERESY",
        validator=NULL_VALIDATOR,
        title="The Eclipse of Gnosis",
        message="A variable was redefined, shadowing its previous soul.",
        elucidation="Redefining an active variable (e.g., setting 'project_name' twice) can lead to 'Contextual Drift' where edicts rely on an unexpected version of the truth.",
        severity="INFO",
        suggestion="Use a unique name if the original value must be preserved, or ensure redefinition is intentional."
    ),

    "HERESY_OF_STALE_GNOSIS": GnosticLaw(
        key="HERESY_OF_STALE_GNOSIS",
        validator=NULL_VALIDATOR,
        title="The Heresy of Stale Gnosis",
        message="A variable was captured too early in the timeline.",
        elucidation="Attempting to use a variable that is updated inside a loop or parallel block before the update is committed results in a 'Temporal Schism'.",
        severity="WARNING",
        suggestion="Ensure variable capture (as) and usage are correctly sequenced in the narrative."
    ),

    # --- THE ARCHITECTURE OF WILL (COMPOSITION) ---

    "UNKNOWN_DIRECTIVE_HERESY": GnosticLaw(
        key="UNKNOWN_DIRECTIVE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unknown Directive",
        message="The Gnostic Directive (@) is not in the Canon.",
        elucidation="Only directives authorized by the Master Architect (e.g., @if, @for, @macro, @import) can be used to structure the symphony.",
        severity="CRITICAL",
        suggestion="Check the spelling of the directive or consult the Oracle via `scaffold help`."
    ),

    "UNCLOSED_BLOCK_HERESY": GnosticLaw(
        key="UNCLOSED_BLOCK_HERESY",
        validator=NULL_VALIDATOR,
        title="The Unsealed Chamber Paradox",
        message="A Gnostic block was opened but never returned to the void.",
        elucidation="Every structural chamber (@if, @for, @try, @task, @macro) must be explicitly sealed with an `@end` directive. An unsealed block leaks logic into the rest of the scripture.",
        severity="CRITICAL",
        suggestion="Add the missing `@end` (or specific `@endif`, `@endfor`) to seal the logic block."
    ),

    "ORPHANED_END_HERESY": GnosticLaw(
        key="ORPHANED_END_HERESY",
        validator=NULL_VALIDATOR,
        title="The Phantom Seal",
        message="A closing directive was perceived without an opening.",
        elucidation="The Conductor found an `@end` directive but has no record of a block being opened. This is a structural impossibility.",
        severity="CRITICAL",
        suggestion="Remove the stray closure or ensure the block was correctly opened."
    ),

    "VACUOUS_BRANCH_HERESY": GnosticLaw(
        key="VACUOUS_BRANCH_HERESY",
        validator=NULL_VALIDATOR,
        title="The Branch of Nothingness",
        message="A conditional or loop block contains no edicts.",
        elucidation="Opening a logical branch requires a Will to be conducted inside it. An empty block is a 'Hollow Thought' that serves no purpose.",
        severity="WARNING",
        suggestion="Add an Action (>>) or State change (%%) to the block, or remove the structure."
    ),

    "ELSE_CONDITION_HERESY": GnosticLaw(
        key="ELSE_CONDITION_HERESY",
        validator=NULL_VALIDATOR,
        title="The Over-Specified Fallback",
        message="An @else block was proclaimed with a condition.",
        elucidation="The `@else` rite is the final, unconditional path. It represents 'all other cases'. Adding a condition to it creates a logical contradiction.",
        severity="CRITICAL",
        suggestion="Use `@elif` for specific conditional paths, or remove the condition from `@else`."
    ),

    "IMPORT_NOT_FOUND_HERESY": GnosticLaw(
        key="IMPORT_NOT_FOUND_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Celestial Void",
        message="The target of the @import could not be manifest.",
        elucidation="The Conductor attempted to weave in another symphony, but the file path provided is a void in the mortal filesystem.",
        severity="CRITICAL",
        suggestion="Check the file path in the `@import` directive and ensure the file exists."
    ),

    "SELF_IMPORT_HERESY": GnosticLaw(
        key="SELF_IMPORT_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Ouroboros",
        message="A scripture attempts to import its own soul.",
        elucidation="Infinite recursion occurs when a symphony imports itself, creating a loop that would devour the Conductor's memory.",
        severity="CRITICAL",
        suggestion="Remove the self-referencing `@import` directive."
    ),

    "MACRO_REDEFINITION_HERESY": GnosticLaw(
        key="MACRO_REDEFINITION_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Double Truth",
        message="A @macro was proclaimed that already exists in the Grimoire.",
        elucidation="A macro name must be a unique identifier of a specific rite. Redefining it creates ambiguity in the Conductor's memory.",
        severity="CRITICAL",
        suggestion="Choose a unique name for the new macro or remove the duplicate definition."
    ),
}
# Path: jurisprudence_core/heresy_codex/architectural.py
# ------------------------------------------------------

"""
=================================================================================
== THE LAWS OF STRUCTURE (ARCHITECTURAL & LOGICAL HERESIES)                    ==
=================================================================================
These laws govern the logical coherence of the Blueprint. They detect cycles,
orphaned variables, and impossible geometries.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

ARCHITECTURAL_LAWS: Dict[str, GnosticLaw] = {

    "ARCHITECTURAL_HERESY_DIR_WITH_SOUL": GnosticLaw(
        key="ARCHITECTURAL_HERESY_DIR_WITH_SOUL",
        validator=NULL_VALIDATOR,
        title="Animate Sanctum Paradox",
        message="Architectural Heresy: A Directory Cannot Possess a Soul.",
        elucidation="In the Scaffold cosmos, directories (Sanctums) are containers for Form. Only files (Scriptures) may possess Content (::) or Seeds (<<).",
        severity="CRITICAL",
        suggestion="Remove the content/seed sigil from the directory path or transmute the path into a file."
    ),

    "VOID_SOUL_HERESY_SEED": GnosticLaw(
        key="VOID_SOUL_HERESY_SEED",
        validator=NULL_VALIDATOR,
        title="Heresy of the Void Soul",
        message="The scripture's soul was promised from a non-existent seed.",
        elucidation="An external seed (<<) was referenced, but the source file does not exist in the Template Forge or project root.",
        severity="CRITICAL",
        suggestion="Verify that the path following the `<<` sigil points to a living file."
    ),

    "FORMLESS_SOUL_HERESY": GnosticLaw(
        key="FORMLESS_SOUL_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Formless Soul",
        message="Gnosis was proclaimed, but it is not bound to a Form.",
        elucidation="Content (::) or Seeds (<<) were detected on a line that does not proclaim a valid file path.",
        severity="CRITICAL",
        suggestion="Ensure the line begins with a valid relative path before the sigil."
    ),

    "UNDEFINED_VARIABLE_REFERENCE_HERESY": GnosticLaw(
        key="UNDEFINED_VARIABLE_REFERENCE_HERESY",
        validator=NULL_VALIDATOR,
        title="Gnostic Paradox: The Unseen Soul",
        message="A variable is used, but its soul has not been defined.",
        elucidation="The Alchemist cannot transmute a placeholder if the underlying Gnosis is missing from the context.",
        severity="CRITICAL",
        suggestion="Define the variable using `$$ name = value` or provide it via the `--set` flag."
    ),

    "UNDEFINED_GNOSIS_HERESY": GnosticLaw(
        key="UNDEFINED_GNOSIS_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Undefined Gnosis",
        message="The scripture references a variable defined in a different reality.",
        elucidation="A variable is used that is not present in the current blueprint's scope, potentially due to a missing `@include`.",
        severity="WARNING",
        suggestion="Ensure all required blueprints are included or define the variable locally."
    ),

    "ARCHITECTURAL_HERESY_DUPLICATE": GnosticLaw(
        key="ARCHITECTURAL_HERESY_DUPLICATE",
        validator=NULL_VALIDATOR,
        title="Heresy of the Doppleganger",
        message="Architectural Heresy: Duplicate Path Definition.",
        elucidation="A single path has been willed into existence multiple times within the same blueprint. Reality allows only one origin for each Form.",
        severity="CRITICAL",
        suggestion="Consolidate the definitions or use different paths."
    ),

    "CIRCULAR_DEPENDENCY_HERESY": GnosticLaw(
        key="CIRCULAR_DEPENDENCY_HERESY",
        validator=NULL_VALIDATOR,
        title="Gnostic Paradox: Ouroboros",
        message="Circular variable dependency detected.",
        elucidation="Variable A depends on Variable B, which in turn depends on Variable A. This creates an infinite loop in the Alchemist's mind.",
        severity="CRITICAL",
        suggestion="Break the cycle by removing the reciprocal reference."
    ),

    "REALITY_PARADOX_HERESY": GnosticLaw(
        key="REALITY_PARADOX_HERESY",
        validator=NULL_VALIDATOR,
        title="Reality Paradox",
        message="The Blueprint contradicts the existing Form.",
        elucidation="The blueprint commands a path to be a file, but the filesystem currently holds a directory at that location (or vice versa).",
        severity="CRITICAL",
        suggestion="Annihilate the existing path or update the blueprint to match the current reality."
    ),

    "VOID_PATH_HERESY": GnosticLaw(
        key="VOID_PATH_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Void Path",
        message="The scripture must resolve to a valid name.",
        elucidation="A path variable (e.g., `src/{{ name }}.py`) resolved to an empty string, creating a formless path.",
        severity="CRITICAL",
        suggestion="Ensure the variables used in path names are not empty."
    ),
}
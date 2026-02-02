# Path: jurisprudence_core/heresy_codex/meta.py
# ---------------------------------------------

"""
=================================================================================
== THE FRACTURE OF THE GOD-ENGINE (META-HERESIES)                              ==
=================================================================================
These are not faults of the Architect's code, but paradoxes within the
Scaffold Engine itself. They represent internal crashes, corruption, or
logical impossibilities caught by the Resilience layer.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

META_HERESY_LAWS: Dict[str, GnosticLaw] = {

    "META_HERESY_INQUISITOR_FRACTURED": GnosticLaw(
        key="META_HERESY_INQUISITOR_FRACTURED",
        validator=NULL_VALIDATOR,
        title="The Inquisitor Shattered",
        message="A catastrophic unhandled exception occurred within the analysis core.",
        elucidation="This is not a heresy of the code being analyzed, but a paradox within the God-Engine itself. The Scribe's hand has been stayed by a bug.",
        severity="CRITICAL",
        suggestion="Examine the Daemon logs and report the traceback to the Architects."
    ),

    "META_HERESY_VARIABLE_SCRIBE_FRACTURED": GnosticLaw(
        key="META_HERESY_VARIABLE_SCRIBE_FRACTURED",
        validator=NULL_VALIDATOR,
        title="Oracle of Gnosis Fractured",
        message="The internal system for tracking variable state has failed.",
        elucidation="The engine has lost its ability to resolve the Gnostic context, likely due to memory corruption or a recursive depth limit.",
        severity="CRITICAL",
        suggestion="Restart the Gnostic Daemon to reset the Cortex memory."
    ),

    "META_HERESY_STRUCTURAL_SCRIBE_FRACTURED": GnosticLaw(
        key="META_HERESY_STRUCTURAL_SCRIBE_FRACTURED",
        validator=NULL_VALIDATOR,
        title="The Builder's Hand Crumbled",
        message="The Structural Scribe encountered a paradox while parsing file definitions.",
        elucidation="The logic that converts indented lines into filesystem objects has failed. The blueprint cannot be materialized.",
        severity="CRITICAL",
        suggestion="Check for mixed indentation or invisible characters in the blueprint."
    ),

    "META_HERESY_POSTRUN_SCRIBE_FRACTURED": GnosticLaw(
        key="META_HERESY_POSTRUN_SCRIBE_FRACTURED",
        validator=NULL_VALIDATOR,
        title="The Conductor's Baton Snapped",
        message="The Oracle of Orchestration failed to parse the Maestro's Will.",
        elucidation="The logic handling `%% post-run` commands encountered an unrecoverable state.",
        severity="CRITICAL",
        suggestion="Verify the syntax of the post-run block."
    ),
}
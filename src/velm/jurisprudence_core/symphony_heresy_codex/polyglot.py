# Path: jurisprudence_core/symphony_heresy_codex/polyglot.py
# -----------------------------------------------------------

"""
=================================================================================
== THE LAWS OF TONGUES (POLYGLOT HERESIES)                                     ==
=================================================================================
These laws govern the embedding of foreign code (`py:`, `js:`, `sh:`) within the
Symphony. They enforce safety, performance, and type integrity across boundaries.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

POLYGLOT_LAWS: Dict[str, GnosticLaw] = {

    "UNKNOWN_LANGUAGE_HERESY": GnosticLaw(
        key="UNKNOWN_LANGUAGE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unknown Tongue",
        message="The polyglot rite uses a grammar unrecognized by the cosmos.",
        elucidation="The Conductor only knows how to bridge specific realities (e.g., `py:`, `js:`, `ts:`, `rs:`). Speaking an unknown tongue leaves the Will un-executable.",
        severity="CRITICAL",
        suggestion="Check the language prefix spelling or install the required polyglot artisan."
    ),

    "EMPTY_SCRIPT_BLOCK_HERESY": GnosticLaw(
        key="EMPTY_SCRIPT_BLOCK_HERESY",
        validator=NULL_VALIDATOR,
        title="The Hollow Scripture",
        message="A polyglot block was proclaimed but contains no code.",
        elucidation="Opening a foreign realm without providing instructions is a void of intent that clutters the architectural narrative.",
        severity="WARNING",
        suggestion="Add the code to be executed or remove the polyglot block header."
    ),

    "MUTE_ARTISAN_HERESY": GnosticLaw(
        key="MUTE_ARTISAN_HERESY",
        validator=NULL_VALIDATOR,
        title="The Mute Artisan",
        message="The polyglot block produces no output and captures no Gnosis.",
        elucidation="Polyglot blocks are intended for data processing or complex logic. A block that does not log to the Scribe or return a value via 'as' is potentially a logic error.",
        severity="INFO",
        suggestion="Ensure the script performs a meaningful action or captures its result."
    ),

    "UNSERIALIZABLE_RETURN_GNOSIS_HERESY": GnosticLaw(
        key="UNSERIALIZABLE_RETURN_GNOSIS_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Mute Oracle",
        message="The polyglot rite returned Gnosis that cannot be serialized.",
        elucidation="To return Gnosis to the Symphony Conductor, the foreign script must provide data that can be transmuted into JSON. Complex memory objects or circular references shatter this bridge.",
        severity="CRITICAL",
        suggestion="Ensure the polyglot block returns a simple dictionary, list, string, or number."
    ),

    "POLYGLOT_TYPE_SCHISM_HERESY": GnosticLaw(
        key="POLYGLOT_TYPE_SCHISM_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Type Schism",
        message="Gnostic data was misinterpreted during the polyglot bridge crossing.",
        elucidation="This occurs when a Symphony variable (e.g., a boolean) is treated as a different type (e.g., a string) inside the foreign block, leading to logical paradoxes.",
        severity="WARNING",
        suggestion="Explicitly cast or validate variable types at the start of the polyglot block."
    ),

    "GNOSTIC_ISOLATION_BREACH_HERESY": GnosticLaw(
        key="GNOSTIC_ISOLATION_BREACH_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Broken Seal",
        message="A polyglot block has unmanaged side-effects in the host reality.",
        elucidation="The script modified files or environment variables outside of the Gnostic Transaction. This prevents the 'undo' artisan from being able to reverse the rite.",
        severity="WARNING",
        suggestion="Use the provided Gnostic APIs (like `scaffold.write`) inside your script to ensure side-effects are chronicled."
    ),

    "REPEATED_RUNTIME_IGNITION_HERESY": GnosticLaw(
        key="REPEATED_RUNTIME_IGNITION_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of Repeated Ignition",
        message="A slow-starting runtime was summoned inside a dense loop.",
        elucidation="Invoking a runtime (like `rs:` or `go:`) inside a high-frequency loop causes massive latency as the engine must re-ignite the foreign mind for every iteration.",
        severity="WARNING", # Demoted from PERFORMANCE for V1 compatibility
        suggestion="Consolidate the logic into a single polyglot block that handles the iteration internally."
    ),

    "TRIVIAL_POLYGLOT_RITE_HERESY": GnosticLaw(
        key="TRIVIAL_POLYGLOT_RITE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Usurped Tongue",
        message="A polyglot block was used for a simple shell command.",
        elucidation="Using `py: print('hello')` instead of `>> echo hello` adds unnecessary overhead. Use the simplest tongue that satisfies the intent.",
        severity="INFO",
        suggestion="Replace the polyglot block with a standard Action Edict (>>)."
    ),
}
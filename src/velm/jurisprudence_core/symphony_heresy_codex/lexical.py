# Path: jurisprudence_core/symphony_heresy_codex/lexical.py
# ---------------------------------------------------------

"""
=================================================================================
== THE LAWS OF SYMPHONIC FORM (LEXICAL HERESIES)                               ==
=================================================================================
These laws govern the syntactic purity of the Symphony. They detect malformed
sigils, broken indentation, and ambiguous structures.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

LEXICAL_LAWS: Dict[str, GnosticLaw] = {

    "UNKNOWN_SIGIL_HERESY": GnosticLaw(
        key="UNKNOWN_SIGIL_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unknown Tongue",
        message="An unrecognized sigil was perceived at the dawn of the line.",
        elucidation="Every line in a .symphony scripture must begin with a sacred sigil (>>, ??, %%, @, #) or a polyglot tag. A bare line is a void of intent.",
        severity="CRITICAL",
        suggestion="Verify that the line begins with a valid Symphonic sigil or comment marker."
    ),

    "LEXICAL_HERESY": GnosticLaw(
        key="LEXICAL_HERESY",
        validator=NULL_VALIDATOR,
        title="Shattered Lexical Vessel",
        message="A syntax error shatters the scripture's form.",
        elucidation="This typically indicates unclosed quotation marks or a malformed character escape sequence that prevents the Lexer from perceiving the soul of the edict.",
        severity="CRITICAL",
        suggestion="Check for mismatched quotes (' or \") and ensure all backslashes are valid."
    ),

    "MALFORMED_EXPLICIT_SOUL_HERESY": GnosticLaw(
        key="MALFORMED_EXPLICIT_SOUL_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Ambiguous Soul",
        message="Indentation and explicit content sigils (::) are in conflict.",
        elucidation="A line cannot possess both an indented block and an inline content sigil. You must choose one path for the scripture's soul.",
        severity="CRITICAL",
        suggestion="Remove the indentation or the '::' sigil to restore structural harmony."
    ),

    "MIXED_INDENTATION_HERESY": GnosticLaw(
        key="MIXED_INDENTATION_HERESY",
        validator=NULL_VALIDATOR,
        title="The War of Invisible Glyphs",
        message="Mixed tabs and spaces detected in the hierarchy.",
        elucidation="The Conductor demands a single, consistent character for indentation. Mixing them creates a fractured reality where logic blocks may be misinterpreted.",
        severity="WARNING",
        suggestion="Convert all indentation to spaces (the Gnostic standard)."
    ),
}
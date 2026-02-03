# Path: jurisprudence_core/heresy_codex/lexical.py
# ------------------------------------------------

"""
=================================================================================
== THE LAWS OF FORM (LEXICAL & PARSER HERESIES)                                ==
=================================================================================
These laws govern the syntactic purity of the Blueprint. They detect malformed
atoms, broken strings, and unrecognizable sigils.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

LEXICAL_LAWS: Dict[str, GnosticLaw] = {

    "LEXICAL_HERESY_DECONSTRUCTION": GnosticLaw(
        key="LEXICAL_HERESY_DECONSTRUCTION",
        validator=NULL_VALIDATOR,
        title="Gnostic Deconstruction Paradox",
        message="The Scribe could not deconstruct the line into Gnostic atoms.",
        elucidation="The line of scripture contains a syntax so profane that the tokenizer's mind shattered. This usually indicates malformed sigils or unclosed strings.",
        severity="CRITICAL",
        suggestion="Verify the syntax of the current line against the Gnostic Canon."
    ),

    "MALFORMED_DIRECTIVE_HERESY": GnosticLaw(
        key="MALFORMED_DIRECTIVE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Formless Directive",
        message="A directive sigil (@) was proclaimed without a valid will.",
        elucidation="Directives must follow a strict grammar (e.g., `@if {{ condition }}`). A bare or misspelled directive is a void of intent.",
        severity="CRITICAL",
        suggestion="Check the spelling of the directive and ensure its parameters are provided."
    ),

    "CONDITIONAL_WILL_HERESY": GnosticLaw(
        key="CONDITIONAL_WILL_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Fractured Will",
        message="The narrative of conditional logic has been shattered.",
        elucidation="An `@elif` or `@else` was perceived without a preceding `@if`, or an `@endif` was found in a void.",
        severity="CRITICAL",
        suggestion="Ensure every conditional block begins with an `@if` and ends with a single `@endif`."
    ),

    "MALFORMED_VARIABLE_HERESY": GnosticLaw(
        key="MALFORMED_VARIABLE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Formless Variable",
        message="A variable proclamation violates the sacred grammar.",
        elucidation="Variable definitions must follow the law: `$$ name = value`. Any other form is a stylistic heresy.",
        severity="CRITICAL",
        suggestion="Ensure variable names are alphanumeric and use the standard assignment operator (=)."
    ),

    "PROFANE_WILL_HERESY": GnosticLaw(
        key="PROFANE_WILL_HERESY",
        validator=NULL_VALIDATOR,
        title="Profane Will Heresy",
        message="The permission scripture is impure.",
        elucidation="The permission sigil (%%) demands a pure, 3-digit octal form (e.g., 755 or 644) or a named alias (executable, secret).",
        severity="WARNING",
        suggestion="Correct the permission to a valid 3-digit octal value or named permission."
    ),

    "PROFANE_PATH_HERESY": GnosticLaw(
        key="PROFANE_PATH_HERESY",
        validator=NULL_VALIDATOR,
        title="Profane Path Heresy",
        message="A path contains characters forbidden in the mortal realms.",
        elucidation="The path contains characters like `<`, `>`, or `|` which cause paradoxes in Windows or Unix filesystems.",
        severity="WARNING",
        suggestion="Rename the file/directory using only alphanumeric characters, dots, and hyphens."
    ),

    "UNSEEN_HERESY_PATH": GnosticLaw(
        key="UNSEEN_HERESY_PATH",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unseen Phantom",
        message="A path is corrupted by non-printable phantoms.",
        elucidation="Invisible control characters (0-31) were detected in the path string. This usually happens during a profane copy-paste.",
        severity="CRITICAL",
        suggestion="Re-type the path manually to purge the invisible phantoms."
    ),

    "STYLISTIC_HERESY_PATH": GnosticLaw(
        key="STYLISTIC_HERESY_PATH",
        validator=NULL_VALIDATOR,
        title="Ambiguous Path Whitespace",
        message="Stylistic Heresy: A path contains leading or trailing voids.",
        elucidation="Paths should not contain spaces around slashes or at the ends of lines, as this leads to inconsistent materialization.",
        severity="WARNING",
        suggestion="Trim the whitespace from the path definition."
    ),

    # [THE DEFINITIVE HEALING] Adding the exact code matching our Healer
    "WHITESPACE_IN_FILENAME_HERESY": GnosticLaw(
        key="WHITESPACE_IN_FILENAME_HERESY",
        validator=NULL_VALIDATOR,
        title="Gnostic Paradox: Whitespace In Filename Heresy",
        message="A filename contains internal whitespace.",
        elucidation="Filenames with spaces are a heresy in the terminal realm, requiring profane escaping. Use snake_case or kebab-case.",
        severity="WARNING",
        suggestion="Use the Quick Fix to transmute spaces to underscores."
    ),

    "PROFANE_ESCAPE_HERESY": GnosticLaw(
        key="PROFANE_ESCAPE_HERESY",
        validator=NULL_VALIDATOR,
        title="Profane Escape Paradox",
        message="An unrecognized escape sequence was perceived.",
        elucidation="The scripture contains a backslash followed by a character not recognized in the Alchemical Law.",
        severity="WARNING",
        suggestion="Verify your backslashes and use valid escape sequences (\\n, \\t, etc.)."
    ),
}
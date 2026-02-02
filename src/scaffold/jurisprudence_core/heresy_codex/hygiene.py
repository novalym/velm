# Path: jurisprudence_core/heresy_codex/hygiene.py
# ------------------------------------------------

"""
=================================================================================
== THE GUARDIAN OF HYGIENE (IDIOMATIC & QUALITY HERESIES)                      ==
=================================================================================
These laws govern the elegance and correctness of the code generated or managed
by Scaffold. They enforce best practices in the target languages (Python, JS, etc.).
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

HYGIENE_LAWS: Dict[str, GnosticLaw] = {

    "MUTABLE_DEFAULT_HERESY": GnosticLaw(
        key="MUTABLE_DEFAULT_HERESY",
        validator=NULL_VALIDATOR,
        title="The Silent Killer of State",
        message="A mutable object (list/dict) is used as a default argument.",
        elucidation="In Python, default arguments are evaluated once. A mutable default will persist changes across all summons of the function, poisoning the state.",
        severity="CRITICAL",
        suggestion="Use `None` as the default and initialize the object inside the function body."
    ),

    "DANGEROUS_EVAL_HERESY": GnosticLaw(
        key="DANGEROUS_EVAL_HERESY",
        validator=NULL_VALIDATOR,
        title="The Gateway to the Abyss",
        message="The use of `eval()` or `exec()` was detected.",
        elucidation="Summoning the evaluator on arbitrary strings allows profane external wills to execute code within your sanctum. This is the highest security transgression.",
        severity="CRITICAL",
        suggestion="Use `ast.literal_eval` for data or refactor to avoid dynamic execution."
    ),

    "MIXED_INDENTATION_HERESY": GnosticLaw(
        key="MIXED_INDENTATION_HERESY",
        validator=NULL_VALIDATOR,
        title="The War of Invisible Glyphs",
        message="Mixed tabs and spaces detected in the scripture.",
        elucidation="Hierarchy must be expressed with a single, consistent character. Mixing them leads to a Fractured Reality where the Architect and the Machine see different structures.",
        severity="WARNING",
        suggestion="Convert all indentation to a single form (spaces are the Gnostic standard)."
    ),

    "SHADOWED_BUILTIN_HERESY": GnosticLaw(
        key="SHADOWED_BUILTIN_HERESY",
        validator=NULL_VALIDATOR,
        title="The Usurper of Names",
        message="A local variable name shadows a built-in function (e.g., 'list', 'id').",
        elucidation="By naming a variable after a built-in rite, you blind the scripture to the original function's soul within that scope.",
        severity="WARNING",
        suggestion="Choose a more descriptive, unique name for your variable."
    ),

    "WEAK_EQUALITY_HERESY": GnosticLaw(
        key="WEAK_EQUALITY_HERESY",
        validator=NULL_VALIDATOR,
        title="The Heresy of the Uncertain Match",
        message="Weak equality (==) used instead of strict equality (===).",
        elucidation="In the JavaScript realm, weak equality performs profane type coercion. Strict equality is the only way to ensure truth of both value and form.",
        severity="WARNING",
        suggestion="Use `===` to ensure a pure and certain comparison."
    ),

    "MISSING_RETURN_TYPE_HERESY": GnosticLaw(
        key="MISSING_RETURN_TYPE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Prophet's Unspoken Vow",
        message="A public function lacks a return type annotation.",
        elucidation="Clear architectural Gnosis requires that every rite proclaims what it will return to its caller. This enables better static analysis and documentation.",
        severity="INFO",
        suggestion="Add a return type hint (e.g., `-> List[str]`) to the function signature."
    ),

    "VAR_NAME_SNAKE": GnosticLaw(
        key="VAR_NAME_SNAKE",
        validator=NULL_VALIDATOR,
        title="Stylistic Heresy: Variable Name",
        message="Variable names should be snake_case or camelCase alphanumeric identifiers.",
        elucidation="Variables are the soul of the blueprint. Their names must be pure identifiers to be compatible with Jinja2.",
        severity="WARNING",
        suggestion="Rename the variable using only letters, numbers, and underscores (e.g., `project_name`)."
    ),
}
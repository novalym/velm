# Path: scaffold/jurisprudence_core/scaffold_grammar_codex.py
# -----------------------------------------------------------

"""
=================================================================================
== THE CODEX OF STRUCTURAL LAW (V-Ω-APOTHEOSIS. THE ETERNAL CONSTITUTION)      ==
=================================================================================
LIF: 10,000,000,000,000,000,000

This scripture is the eternal, immutable constitution of the Scaffold Language of
Form (.scaffold). It is the one true, centralized source of Gnosis for its
grammar, sigils, and sacred laws.
=================================================================================
"""
import re
from typing import List
from ..contracts.law_contracts import GnosticLaw

# =============================================================================
# == I. THE SACRED SIGILS (THE ATOMS OF FORM)                                ==
# =============================================================================
SCAFFOLD_SIGILS = {
    "DIR_SUFFIX": "/",
    "INLINE_CONTENT": "::",
    "EXTERNAL_SEED": "<<",
    "PERMISSIONS": "%%",
    "VARIABLE_DEF": "$$",
    "COMMENT": "#",
    "JINJA_START": "{%",
    "JINJA_VAR": "{{",
    "SYMLINK": "->",  # [NEW]
    "TRAIT_DEF": "%% trait",  # [NEW]
    "TRAIT_USE": "%% use"  # [NEW]
}

# =============================================================================
# == II. THE REGEX GRIMOIRE (THE UNBREAKABLE GAZES)                          ==
# =============================================================================
SCAFFOLD_PATTERNS = {
    "VARIABLE_DEFINITION": re.compile(
        r"""^\s*(?:\$\$|let|def|const)\s*
        (?P<name>[\w.-]+)           # The sacred name
        \s*(?::\s*(?P<type>[^=]+))? # Optional type hint
        \s*=\s*
        (?P<value>.*)               # The soul
        $""", re.VERBOSE
    ),
    "BARE_ASSIGNMENT": re.compile(
        r"^\s*(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*(?::\s*(?P<type>[^=]+))?\s*=\s*(?P<value>.*)$"
    ),
    "MAESTRO_BLOCK": re.compile(r"^\s*%%\s*(?P<rite>post-run|pre-run|on-undo|on-heresy|weave)\b"),
    "POST_RUN_BLOCK": re.compile(r"^\s*%%\s*post-run\b"),

    # [NEW] Trait Patterns
    "TRAIT_DEF": re.compile(r"^\s*%%\s*trait\s+(?P<name>\w+)\s*=\s*(?P<path>.*)$"),
    "TRAIT_USE": re.compile(r"^\s*%%\s*use\s+(?P<name>\w+)(?:\s+(?P<args>.*))?$"),

    "WEAVE_EDICT": re.compile(r"^\s*(?:%%\s*)?weave\b"),

    # [NEW] Symlink Pattern
    "SYMLINK": re.compile(r"^(?P<source>.*?)\s*->\s*(?P<target>.*)$"),

    "INLINE_CONTENT": re.compile(r"^(?P<path>.*?)\s*::\s*(?P<content>.*)$"),
    "EXTERNAL_SEED": re.compile(r"^(?P<path>.*?)\s*<<\s*(?P<source>.*)$"),

    # [NEW] Updated Permissions Regex to allow named permissions
    "PERMISSIONS": re.compile(r"^(?P<main_body>.*?)\s*%%\s*(?P<mode>[0-7]{3}|executable|readonly|secret)\s*$"),

    "DIRECTORY": re.compile(r"^(?P<path>.+?)/\s*(?:#.*)?$"),
    "DIRECTIVE": re.compile(r"^\s*@(?P<name>\w+)"),
    "COMMENT": re.compile(r"^\s*#.*$"),

    # [NEW] Hash Anchor Pattern
    "HASH_ANCHOR": re.compile(r"@hash\((?P<algo>\w+):(?P<digest>[a-fA-F0-9]+)\)")
}

# =============================================================================
# == III. THE LAWS OF THE ALCHEMIST (VARIABLES & FILTERS)                    ==
# =============================================================================
ALLOWED_VAR_TYPES = {
    "str", "string", "int", "integer", "bool", "boolean", "float", "number",
    "list", "array", "dict", "object", "path", "secret", "any"
}

SAFE_JINJA_FILTERS = {
    "pascal", "camel", "snake", "kebab", "slug", "screaming_snake", "dot", "path",
    "sentence", "title",
    "upper", "lower", "default", "replace", "join", "split", "int", "float", "string", "sort", "unique",
    "to_json", "to_yaml", "native",
    "basename", "dirname", "stem",
    "shell_escape",
    "base64"  # [NEW] Added for Binary Embedder
}

ALLOWED_DIRECTIVES = {
    "if", "elif", "else", "endif",
    "include", "def", "let",
    "error", "warn", "print", "contract"
}

# =============================================================================
# == IV. THE SCAFFOLD GRAMMAR CODEX (ASCENDED)                               ==
# =============================================================================
SCAFFOLD_GRAMMAR_CODEX: List[GnosticLaw] = [
    GnosticLaw(
        key="VAR_NAME_SNAKE",
        validator=lambda name: not re.fullmatch(r"^[a-zA-Z_][\w]*$", name),
        title="Stylistic Heresy: Variable Name",
        message="Variable names should be snake_case or camelCase alphanumeric identifiers.",
        elucidation="Variables are the soul of the blueprint. Their names must be pure identifiers to be compatible with Jinja2.",
        severity="WARNING",
        suggestion="Rename the variable using only letters, numbers, and underscores (e.g., `project_name`)."
    ),
    GnosticLaw(
        key="INVALID_PERMISSION",
        validator=lambda perm: not re.fullmatch(r"^(?:[0-7]{3}|executable|readonly|secret)$", str(perm)),
        title="Permission Heresy",
        message="Permissions must be a 3-digit octal string or a named permission (executable, readonly, secret).",
        elucidation="The mortal realm's filesystem requires exact octal rites to set file modes.",
        severity="CRITICAL",
        suggestion="Use '755', 'executable', 'readonly', or 'secret'."
    ),
    GnosticLaw(
        key="UNKNOWN_DIRECTIVE",
        validator=lambda d: d not in ALLOWED_DIRECTIVES,
        title="Unknown Directive",
        message="The directive is not in the Sacred Grimoire.",
        severity="CRITICAL",
        suggestion=f"Valid directives are: {', '.join(ALLOWED_DIRECTIVES)}"
    )
]
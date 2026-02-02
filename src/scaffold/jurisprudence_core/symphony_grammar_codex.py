"""
=================================================================================
== THE CODEX OF SYMPHONIC LAW (V-Ω-EXECUTABLE-ULTIMA-COMPLETE)                 ==
=================================================================================
LIF: 10,000,000,000
AUTH_CODE: #)(@)(#()@

This scripture defines the valid grammar, allowed parameters, security wards,
and adjudication contracts for the Symphony language. It is the one true
source of truth for the Gnostic Oracle's self-awareness.
=================================================================================
"""
import re
from typing import Dict, List, Any, Tuple
from ..contracts.law_contracts import GnosticLaw

# --- I. THE POLYGLOT GRIMOIRE ---
# [ASCENSION]: Every language now possesses a description for the Oracle's Gaze.
POLYGLOT_LANGUAGES = {
    "py": {
        "name": "Python",
        "safe": True,
        "description": "Execute a block of pure Python code within the Gnostic environment."
    },
    "js": {
        "name": "Node.js",
        "safe": True,
        "description": "Execute a block of JavaScript code using the Node.js runtime."
    },
    "ts": {
        "name": "TypeScript",
        "safe": True,
        "description": "Execute a block of TypeScript code, auto-transpiled by the God-Engine."
    },
    "sh": {
        "name": "Bash/Shell",
        "safe": False,
        "description": "Execute a raw shell script. Warning: This rite touches the mortal realm directly."
    },
    "go": {
        "name": "Go",
        "safe": True,
        "description": "Compile and execute a block of Go code in a hermetic sandbox."
    },
    "rs": {
        "name": "Rust",
        "safe": True,
        "description": "Compile and execute a block of Rust code using the internal Cargo forge."
    },
    "rb": {
        "name": "Ruby",
        "safe": True,
        "description": "Execute a block of Ruby code within the system's Gem environment."
    },
    "lua": {
        "name": "Lua",
        "safe": True,
        "description": "Execute a block of Lua code, often used for hyper-fast internal logic."
    },
}

# [THE DEFINITIVE FIX]: Every parameter now possesses a mandatory description.
POLYGLOT_PARAMETERS = {
    "timeout": {
        "type": int,
        "default": 60,
        "validator": lambda x: x > 0,
        "description": "The maximum duration in seconds before the rite is forcibly returned to the void."
    },
    "filesystem": {
        "type": str,
        "allowed": ["read-write", "read-only", "temp-only", "void"],
        "default": "read-write",
        "description": "The degree of access granted to the physical filesystem within the sandbox."
    },
    "network": {
        "type": bool,
        "default": True,
        "description": "Permits or forbids the foreign soul from communicating with the celestial aether (network)."
    },
    "isolation": {
        "type": str,
        "allowed": ["process", "container", "vm"],
        "default": "process",
        "description": "The level of Gnostic jailing used to contain the foreign execution."
    },
    "workers": {
        "type": int,
        "default": 1,
        "validator": lambda x: 1 <= x <= 32,
        "description": "The number of parallel instances to summon for this specific block."
    }
}

# [ASCENSION]: Metadata is now structured to prevent future KeyError paradoxes.
POLYGLOT_METADATA = {
    "requirements": {
        "description": "A comma-separated list of external packages required for the rite."
    },
    "packages": {
        "description": "An alias for 'requirements'. Lists the necessary library souls."
    },
    "import": {
        "description": "A path to a local file whose Gnosis should be injected into the script context."
    },
    "return": {
        "description": "A format hint for the Scribe to interpret the stdout (e.g., 'json', 'text')."
    },
    "env": {
        "description": "A mapping of environment variables to be anointed upon the child process."
    },
}

# --- IV. THE PANTHEON OF VOWS (??) ---
VOW_SIGNATURES = {
    "exists": (1, 1, "Asserts that a specific path is manifest in the mortal realm."),
    "not_exists": (1, 1, "Asserts that a specific path is currently a void."),
    "file_exists": (1, 1, "Asserts that a scripture (file) is manifest."),
    "dir_exists": (1, 1, "Asserts that a sanctum (directory) is manifest."),
    "succeeds": (0, 0, "Asserts that the previously conducted rite returned Exit Code 0."),
    "fails": (0, 0, "Asserts that the previously conducted rite returned a non-zero Exit Code."),
    "stdout_contains": (1, 1, "Asserts that the output of the previous rite contains a specific substring."),
    "is_json": (0, 0, "Asserts that the output of the previous rite is a valid JSON scripture."),
    "json_path_exists": (1, 1, "Asserts that a specific JSONPath resolves within the previous output."),
    "json_equals": (2, 2, "Asserts equality between a JSONPath result and a expected value."),
    "http_status": (2, 2, "Asserts that a celestial URL returns a specific HTTP status code."),
    "wait_for": (2, 2, "Pauses the symphony's timeline until a specific condition is met."),
    "confirm": (1, 1, "Pauses for user intercession; requires the Architect's manual vow."),
    "port_available": (1, 1, "Asserts that a specific TCP port is free for binding.")
}

# --- V. THE DIVINE CODEX OF DIRECTIVES ---
DIRECTIVE_SIGNATURES = {
    "if": (1, 99, "Begins a conditional logic gate."),
    "elif": (1, 99, "Defines a secondary path in a logic gate."),
    "else": (0, 0, "Defines the fallback path in a logic gate."),
    "end": (0, 0, "The universal sigil for closing a logical block."),
    "for": (3, 99, "Begins a rite of iteration (loop)."),
    "try": (0, 0, "Begins an unbreakable resilience block."),
    "catch": (0, 0, "Defines the handler for a paradox within a resilience block."),
    "finally": (0, 0, "Defines the final, mandatory rite of a resilience block."),
    "task": (1, 1, "Consecrates an indented block as a named, reusable task."),
    "macro": (1, 99, "Consecrates an indented block as a Gnostic macro with parameters."),
    "call": (1, 99, "Invokes a previously defined macro."),
    "import": (1, 1, "Summons the soul of an external Symphony library."),
    "conduct": (1, 99, "Executes an external Symphony scripture as a sub-process."),
}

# --- VI. THE GRAMMAR OF WILL (REGEX) ---
SYMPHONY_PATTERNS = {
    "BLOCK_HEADER": re.compile(r"^([a-z]{2,10})(?:\((.*)\))?:$"),
    "ACTION": re.compile(r"^>>\s*(.*)"),
    "VOW": re.compile(r"^\?\?\s*(.*)"),
    "STATE": re.compile(r"^%%\s*(.*)"),
    "DIRECTIVE": re.compile(r"^@(\w+)(?:\s+(.*))?"),
    "VARIABLE_USAGE": re.compile(r"\{\{\s*([\w\.]+)\s*\}\}"),
    "COMMENT": re.compile(r"^#.*"),
    "RETRY_SUFFIX": re.compile(r"\s+retry\((.*?)\)$"),
    "ASK_ACTION": re.compile(r"^@ask\s+(?:\"|')(.*?)(?:\"|')\s*->\s*\$([\w_]+)$"),
    "SERVICE_ACTION": re.compile(r"^@service\s+(start|stop|restart)\s+(?:\"|')(.*?)(?:\"|')(?:\s+as\s+([\w_]+))?$"),
    "VAULT_VALUE": re.compile(r"@vault\((?:\"|')(.*?)(?:\"|')\)")
}

# --- VII. THE GNOSTIC LAWS OF THE SYMPHONY ---
SYMPHONY_GRAMMAR_CODEX: List[GnosticLaw] = [
    GnosticLaw(
        key="UNKNOWN_VOW",
        validator=lambda v: v not in VOW_SIGNATURES,
        title="Heresy of the Unknown Vow",
        message="The Vow is not in the Pantheon.",
        severity="CRITICAL",
        suggestion=f"Consult the Grimoire for valid vows: {', '.join(VOW_SIGNATURES.keys())}"
    ),
    GnosticLaw(
        key="UNKNOWN_LANGUAGE",
        validator=lambda l: l not in POLYGLOT_LANGUAGES,
        title="Tongue of Babel",
        message="The Polyglot block speaks an unknown tongue.",
        severity="CRITICAL",
        suggestion=f"Valid tongues in this reality: {', '.join(POLYGLOT_LANGUAGES.keys())}"
    )
]
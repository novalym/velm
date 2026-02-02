# Path: core/lsp/scaffold_features/hover/grimoire_data.py
# -------------------------------------------------------

"""
=================================================================================
== THE LUMINOUS GRIMOIRE (V-Ω-TOTALITY-V24-ASCENDED)                           ==
=================================================================================
LIF: INFINITY | ROLE: LOCAL_KNOWLEDGE_BASE | RANK: ANCESTRAL
AUTHORITY: IBQ-GENESISENGINE-PRIME

The primary source of zero-latency Gnosis for the Ocular UI.
This scripture serves as the fundamental lexicon of Form and Will.
=================================================================================
"""

from typing import Dict, Any

# =============================================================================
# == SECTION I: THE SIGILS OF FORM (SCAFFOLD)                                ==
# =============================================================================

STATIC_GRIMOIRE: Dict[str, Dict[str, Any]] = {
    "$$": {
        "title": "Gnostic Variable",
        "law": "Form / Memory",
        "body": (
            "Inscribes a unit of data into the project's memory.\n\n"
            "**Syntax:** `$$ name: type = value`\n\n"
            "**LIF:** 10x (Scale architecture via variables).\n\n"
            "💡 **Mentor:** Use `snake_case` for all variable identifiers. "
            "Variables defined with `$$` are globally accessible and immutable "
            "during the materialization phase."
        ),
        "example": "$$ project_port: int = 8080"
    },
    "::": {
        "title": "Inline Content Inscription",
        "law": "Matter / Genesis",
        "body": (
            "Binds a textual soul directly to a physical path.\n\n"
            "**Syntax:** `path/to/scripture :: \"content\"`\n\n"
            "**LIF:** 1x (Direct creation).\n\n"
            "⚠️ **Ward:** Use triple quotes (`\"\"\"`) for multi-line scriptures to "
            "preserve the sacred geometry of indentation."
        ),
        "example": "main.py :: \"print('Hello World')\""
    },
    "<<": {
        "title": "Celestial Seeding",
        "law": "Matter / Replication",
        "body": (
            "Clones the soul of a template or existing file into a new destination.\n\n"
            "**Syntax:** `path/to/target << path/to/source`\n\n"
            "**LIF:** 50x (Massive pattern reuse).\n\n"
            "💡 **Mentor:** The source path is subject to alchemical transmutation. "
            "Variables inside the source will be resolved using the current context."
        ),
        "example": "src/config.json << ./.scaffold/templates/base.json"
    },
    "->": {
        "title": "Symbolic Link (Neural Link)",
        "law": "Matter / Topology",
        "body": (
            "Forges a persistent link between two points in the filesystem's spacetime.\n\n"
            "**Syntax:** `link_path -> target_path`\n\n"
            "**LIF:** 5x (Structural flexibility).\n\n"
            "⚠️ **Ward:** Ensure the target path exists. Cross-volume links on "
            "Windows (Junctions) require Elevated Will (Admin permissions)."
        ),
        "example": "current -> releases/v1.0.4"
    },
    "@if": {
        "title": "Logic Gate (Condition)",
        "law": "Logic / Branching",
        "body": (
            "Branches reality based on Gnostic truth.\n\n"
            "**Syntax:** `@if {{ condition }} ... @endif`\n\n"
            "**LIF:** 100x (Adaptive architecture).\n\n"
            "💡 **Mentor:** Always provide an `@else` branch to handle the void "
            "if the condition is not met."
        ),
        "example": "@if {{ use_auth }}\n  src/auth.py :: ...\n@endif"
    },
    "@include": {
        "title": "Gnostic Composition",
        "law": "Logic / Modularization",
        "body": (
            "Weaves the soul of an external blueprint into the current scripture.\n\n"
            "**Syntax:** `@include \"path/to/fragment.scaffold\"`\n\n"
            "**LIF:** 20x (Decompose monoliths).\n\n"
            "💡 **Mentor:** Fragments should be stored in the `.scaffold/fragments` sanctum "
            "for guild-wide accessibility."
        ),
        "example": "@include \"shared/database_config.scaffold\""
    },

    # =============================================================================
    # == SECTION II: THE SIGILS OF WILL (SYMPHONY)                               ==
    # =============================================================================
    "%%": {
        "title": "Maestro's Mark",
        "law": "Will / Automation",
        "body": (
            "Declares a block of **Kinetic Will** (Maestro Edicts).\n\n"
            "**Usage:** `%% post-run`, `%% pre-run`, `%% on-undo`.\n\n"
            "**LIF:** 10x (Lifecycle management).\n\n"
            "⚠️ **Ward:** Commands within `%%` blocks run in the host shell. "
            "Always follow risky actions with a Vow (`??`)."
        ),
        "example": "%% post-run\n  >> npm install"
    },
    "%% post-run": {
        "title": "Post-Materialization Rite",
        "law": "Will / Persistence",
        "body": (
            "Commands that execute *after* the physical files have been manifest.\n\n"
            "**LIF:** 5x (Automated setup).\n\n"
            "💡 **Mentor:** Ideal for triggering compilers, installing dependencies, "
            "or initializing Git repositories."
        )
    },
    ">>": {
        "title": "Kinetic Action (Shell)",
        "law": "Will / Impact",
        "body": (
            "Dispatches a raw command to the mortal realm's shell.\n\n"
            "**Syntax:** `>> shell_command`\n\n"
            "**LIF:** 1x (Standard execution).\n\n"
            "💀 **Critical:** Sanitize all variables passed to `>>` using the "
            "`| shell_escape` filter to prevent injection heresies."
        ),
        "example": ">> docker-compose up -d"
    },
    "??": {
        "title": "Gnostic Vow (Assertion)",
        "law": "Will / Adjudication",
        "body": (
            "A mandatory adjudication of reality. If the Vow returns `False`, "
            "the Symphony halts immediately with a Heresy.\n\n"
            "**Syntax:** `?? succeeds`, `?? file_exists: path`\n\n"
            "**LIF:** 50x (Resilience).\n\n"
            "💡 **Mentor:** Turning 'Blind Faith' scripts into 'Resilient Workflows' "
            "starts with placing a Vow after every Action (`>>`)."
        ),
        "example": "?? succeeds\n?? port_open: 8080"
    },
    "!!": {
        "title": "Intercession (Breakpoint)",
        "law": "Will / Observation",
        "body": (
            "Suspends the flow of time within the Symphony.\n\n"
            "**LIF:** 1x (Debugging).\n\n"
            "💡 **Mentor:** Opens an interactive altar allowing the Architect to "
            "inspect variables or manually conduct edicts before resuming."
        )
    },

    # =============================================================================
    # == SECTION III: THE ALCHEMIST'S TOOLS (FUNCTIONS & FILTERS)                ==
    # =============================================================================
    "now": {
        "title": "Temporal Gaze",
        "law": "Alchemy / Time",
        "body": (
            "Returns the current timestamp.\n\n"
            "**Signature:** `now(format: str = '%Y-%m-%d') -> str`\n\n"
            "**Usage:** `{{ now() }}`"
        )
    },
    "secret": {
        "title": "Forge of Chaos",
        "law": "Alchemy / Entropy",
        "body": (
            "Generates a cryptographically secure random string.\n\n"
            "**Signature:** `secret(length: int, type: str = 'hex') -> str`\n\n"
            "**Usage:** `$$ api_key = {{ secret(32) }}`"
        )
    },
    "snake": {
        "title": "Snake-Case Transmutation",
        "law": "Alchemy / Form",
        "body": (
            "Converts a string to `snake_case`.\n\n"
            "**Input:** `MyVariableName` -> **Output:** `my_variable_name`"
        )
    },
    "pascal": {
        "title": "Pascal-Case Transmutation",
        "law": "Alchemy / Form",
        "body": (
            "Converts a string to `PascalCase`.\n\n"
            "**Input:** `my_variable` -> **Output:** `MyVariable`"
        )
    },
    "shell_escape": {
        "title": "Shell Ward",
        "law": "Alchemy / Security",
        "body": (
            "Sanitizes a string for safe usage in shell commands.\n\n"
            "**Mandate:** MUST be used for any variable injected into a `>>` action."
        )
    }
}

# =============================================================================
# == SECTION IV: KINETIC WARNINGS (THE MENTOR'S ALERTS)                      ==
# =============================================================================

KINETIC_WARNINGS: Dict[str, str] = {
    "rm -rf": "Absolute Annihilation: This command returns its target to the true void. Ensure the path is warded.",
    "sudo": "Privilege Escalation: This may fail in non-interactive CI environments without a pre-configured tty.",
    "chmod 777": "Permissive Access Heresy: Use 755 (Exec) or 644 (Read) for a secure sanctum.",
    "curl | sh": "Blind Execution: Do not pipe remote scriptures directly into your shell without first auditing the source.",
    ":latest": "Stability Warning: Usage of the `:latest` tag in Docker prevents reproducible materializations. Pin a version.",
    "0.0.0.0": "Exposure Warning: Binding to the universal gate makes this service visible to the entire mesh network.",
}

# =============================================================================
# == SECTION V: GNOSTIC PRAGMAS (# @HEADERS)                                 ==
# =============================================================================

PRAGMA_GRIMOIRE: Dict[str, Dict[str, str]] = {
    "@description": {
        "title": "Reality Context",
        "body": "Provides the AI Co-Pilot with a high-level summary of this scripture's purpose."
    },
    "@require-os": {
        "title": "OS Constraint",
        "body": "Halts materialization if the host machine does not match the required OS (e.g., `linux`, `windows`)."
    },
    "@require-scaffold": {
        "title": "Version Constraint",
        "body": "Enforces a specific version of the God-Engine to prevent protocol drift."
    },
    "@gnosis:grade": {
        "title": "Knowledge Tier",
        "body": "Defines the required Architect Grade to modify this file (Initiate, Adept, Master)."
    }
}
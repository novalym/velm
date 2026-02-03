# Path: jurisprudence_core/heresy_codex/supply_chain.py
# -----------------------------------------------------

"""
=================================================================================
== THE KEEPER OF BONDS (SUPPLY CHAIN & DEPENDENCY HERESIES)                    ==
=================================================================================
These laws govern the relationships between the project and the external cosmos.
They enforce version pinning, manifest integrity, and dependency purity.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

SUPPLY_LAWS: Dict[str, GnosticLaw] = {

    "PHANTOM_DEPENDENCY_HERESY": GnosticLaw(
        key="PHANTOM_DEPENDENCY_HERESY",
        validator=NULL_VALIDATOR,
        title="The Heresy of the Unbound Soul",
        message="A scripture imports a soul not declared in the manifest.",
        elucidation="The code relies on an external library that is not listed in `pyproject.toml` or `package.json`. This leads to the 'Works on my Machine' heresy when materialized in other realities.",
        severity="CRITICAL",
        suggestion="Add the missing dependency to your project's manifest."
    ),

    "UNPINNED_PIP_HERESY": GnosticLaw(
        key="UNPINNED_PIP_HERESY",
        validator=NULL_VALIDATOR,
        title="The Chaos of the Floating Version",
        message="A dependency is declared without a version pin.",
        elucidation="Allowing dependencies to float freely makes the materialization of reality non-deterministic. What works today may shatter tomorrow when a library's soul changes.",
        severity="WARNING",
        suggestion="Pin the dependency to a specific version (e.g., `requests == 2.31.0`)."
    ),

    "UNUSED_GNOSIS_HERESY": GnosticLaw(
        key="UNUSED_GNOSIS_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Silent Soul",
        message="A Gnostic variable is defined but never used.",
        elucidation="Definitions that serve no purpose clutter the Architect's mind and the Alchemist's context. Every variable should contribute to the final reality.",
        severity="INFO",
        suggestion="Remove the unused variable or implement its use in the scripture."
    ),

    "REQUIREMENTS_TXT_INSTEAD_OF_POETRY_HERESY": GnosticLaw(
        key="REQUIREMENTS_TXT_INSTEAD_OF_POETRY_HERESY",
        validator=NULL_VALIDATOR,
        title="Redundant Dependency Manifest",
        message="A `requirements.txt` was perceived alongside a Poetry-based `pyproject.toml`.",
        elucidation="The `poetry` artisan manages dependencies holistically. Maintaining a separate `requirements.txt` creates a dual source of truth and leads to drift.",
        severity="WARNING",
        suggestion="Remove `requirements.txt` and rely on `poetry.lock`."
    ),

    "MISSING_GO_MOD_HERESY": GnosticLaw(
        key="MISSING_GO_MOD_HERESY",
        validator=NULL_VALIDATOR,
        title="The Formless Golem",
        message="A Go reality was perceived without a `go.mod` scripture.",
        elucidation="The `go.mod` file is the heart of a modern Go project, defining its module path and dependencies.",
        severity="CRITICAL",
        suggestion="Run `go mod init <module-name>`."
    ),

    "MISSING_CARGO_TOML_HERESY": GnosticLaw(
        key="MISSING_CARGO_TOML_HERESY",
        validator=NULL_VALIDATOR,
        title="The Unmanifested Crate",
        message="A Rust reality was perceived without a `Cargo.toml`.",
        elucidation="This scripture is the heart, soul, and mind of a Rust crate. Without it, the compiler cannot function.",
        severity="CRITICAL",
        suggestion="Create a `Cargo.toml` manifest."
    ),

    "MISSING_PACKAGE_JSON_HERESY": GnosticLaw(
        key="MISSING_PACKAGE_JSON_HERESY",
        validator=NULL_VALIDATOR,
        title="The Void Node",
        message="A JavaScript/TypeScript reality was perceived without a `package.json`.",
        elucidation="This scripture is the central soul of the Node.js cosmos, defining dependencies and scripts.",
        severity="CRITICAL",
        suggestion="Run `npm init -y` or create a `package.json`."
    ),

    "MIXED_PACKAGE_MANAGERS_HERESY": GnosticLaw(
        key="MIXED_PACKAGE_MANAGERS_HERESY",
        validator=NULL_VALIDATOR,
        title="Schism of the Managers",
        message="Multiple lockfiles (npm, yarn, pnpm) were perceived.",
        elucidation="This indicates a Gnostic Schism in dependency management. A project should serve only one master (package manager).",
        severity="WARNING",
        suggestion="Delete the extraneous lockfiles and stick to one manager."
    ),
}
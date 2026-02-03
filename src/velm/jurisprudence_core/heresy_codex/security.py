# Path: jurisprudence_core/heresy_codex/security.py
# -------------------------------------------------

"""
=================================================================================
== THE CITADEL OF TRUST (SECURITY HERESIES)                                    ==
=================================================================================
These laws govern the safety of the Sanctum. They detect path traversal,
secret leakage, and injection attacks.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

SECURITY_LAWS: Dict[str, GnosticLaw] = {

    "GUARDIAN_WARD_HERESY": GnosticLaw(
        key="GUARDIAN_WARD_HERESY",
        validator=NULL_VALIDATOR,
        title="Guardian's Intercession",
        message="The Gnostic Sentry has blocked a command to protect the Host Reality.",
        elucidation="A shell command or file operation attempted to escape the consecrated project sanctum or used forbidden patterns like `sudo` or redirection into system paths.",
        severity="CRITICAL",
        suggestion="Refactor the command to operate strictly within the project root or use `--force` to override (not recommended)."
    ),

    "DANGEROUS_PATH_TRAVERSAL_HERESY": GnosticLaw(
        key="DANGEROUS_PATH_TRAVERSAL_HERESY",
        validator=NULL_VALIDATOR,
        title="Path Traversal Paradox",
        message="A path attempts to escape the sanctum via '../'.",
        elucidation="Architectural law forbids any scripture from gazing upon or modifying the reality outside of its own project root. This protects the Architect's machine from accidental or malicious sprawl.",
        severity="CRITICAL",
        suggestion="Keep all paths relative and anchored within the project structure."
    ),

    "HARDCODED_SECRET_HERESY": GnosticLaw(
        key="HARDCODED_SECRET_HERESY",
        validator=NULL_VALIDATOR,
        title="The Open Vein: Hardcoded Secret Detected",
        message="A raw secret (key, password, token) was perceived in the scripture.",
        elucidation="Storing secrets in plaintext is a grave transgression. They must be abstracted and injected via Environment Gnosis (${...}) or summoned via the Vault (@vault).",
        severity="CRITICAL",
        suggestion="Abstract this value into an environment variable or a secure secret store."
    ),

    "SQL_INJECTION_HERESY": GnosticLaw(
        key="SQL_INJECTION_HERESY",
        validator=NULL_VALIDATOR,
        title="The Poisoned Query",
        message="Potential SQL injection vulnerability detected.",
        elucidation="The Gaze perceived raw string interpolation within a database query. This allows profane data to alter the intent of the command.",
        severity="CRITICAL",
        suggestion="Use parameterized queries or an ORM to shield the database."
    ),

    "TIMING_ATTACK_HERESY": GnosticLaw(
        key="TIMING_ATTACK_HERESY",
        validator=NULL_VALIDATOR,
        title="The Leaking Clock",
        message="Insecure secret comparison detected (Timing Attack).",
        elucidation="Comparing secrets using standard equality (==) takes variable time, allowing an attacker to divine the secret's soul by measuring response times.",
        severity="WARNING",
        suggestion="Use a constant-time comparison rite like `secrets.compare_digest`."
    ),

    # [ASCENSION] The Hardcoded Secret in Content
    # This was previously in the architectural grimoire, but belongs here.
    "HARDCODED_SECRET_IN_CONTENT_HERESY": GnosticLaw(
        key="HARDCODED_SECRET_IN_CONTENT_HERESY",
        validator=NULL_VALIDATOR,
        title="Secret in Soul",
        message="The scripture's content appears to contain a hardcoded secret.",
        elucidation="Static analysis detected a high-entropy string or keyword resembling a secret within the file content.",
        severity="CRITICAL",
        suggestion="Move the secret to .env and use variable injection."
    ),
}
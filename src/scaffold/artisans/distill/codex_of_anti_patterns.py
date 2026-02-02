# Path: artisans/distill/codex_of_anti_patterns.py
# ------------------------------------------------

"""
=================================================================================
== THE SACRED GRIMOIRE OF ARCHITECTURAL LAW                                    ==
=================================================================================
This scripture contains the declarative laws of good architecture. The
ArchitecturalInquisitor will adjudicate the dependency graph against these laws
during the distillation rite.

Each law is a tuple: (HERESY_KEY, FORBIDDEN_BOND_REGEX)

- HERESY_KEY: A unique identifier for the violation.
- FORBIDDEN_BOND_REGEX: A regex where group 1 is the sinner (importer) and
  group 2 is the sin (imported). The pattern matches against the full,
  project-relative POSIX path of the files.
=================================================================================
"""

# The laws are defined as tuples: (KEY, REGEX_PATTERN)
# The regex must have two capturing groups: (source_pattern) -> (target_pattern)
ARCHITECTURAL_GRIMOIRE = [
    (
        "LAYER_VIOLATION_CONTROLLER_TO_VIEW",
        r"(controllers/.+)\s*->\s*(views/.+)",
        "A Controller must not import directly from a View. It should receive data via a Service."
    ),
    (
        "LAYER_VIOLATION_MODEL_TO_API",
        r"(models/.+)\s*->\s*(api/.+|routes/.+|controllers/.+)",
        "A Model must not import from an API layer. Data should flow inwards (API -> Service -> Model)."
    ),
    (
        "LAYER_VIOLATION_SERVICE_TO_CONTROLLER",
        r"(services/.+)\s*->\s*(api/.+|routes/.+|controllers/.+)",
        "A Service must not import from the Controller/API layer. This creates a circular dependency."
    ),
    (
        "DOMAIN_LEAK_AUTH_TO_BILLING",
        r"(domain/auth/.+)\s*->\s*(domain/billing/.+)",
        "The Auth domain must not have a direct dependency on the Billing domain."
    ),
    (
        "DOMAIN_LEAK_BILLING_TO_AUTH",
        r"(domain/billing/.+)\s*->\s*(domain/auth/.+)",
        "The Billing domain must not have a direct dependency on the Auth domain. Use a shared kernel."
    ),
    (
        "TEST_LEAK_SRC_IMPORTS_TEST",
        r"^(?!tests/)(.+)\s*->\s*(tests/.+)",
        "Production code must never import from the test suite."
    ),
]
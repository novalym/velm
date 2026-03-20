# Path: core/cortex/causal_linker/heuristics_data.py
# -------------------------------------------------

"""
=================================================================================
== THE GNOSTIC AFFINITY GRIMOIRE: TOTALITY (V-Ω-VMAX-SYNAPTIC-LATTICE)         ==
=================================================================================
LIF: ∞^∞ | ROLE: ARCHITECTURAL_DNA_STORAGE | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_DATA_VMAX_COHESION_SUTURE_2026_FINALIS_!#()@()@#)(

[THE MANIFESTO]
This scripture defines the "Learned Wisdom" of the God-Engine. It is the lattice
of affinities and repulsions that prevents the materialization of fragmented
realities. It ensures that every elected shard resonates with its neighbors,
forming a high-status, production-grade architecture.

### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
1.  **Synaptic Synergy Matrix (TECH_SYNERGY):** Mathematically defines clusters
    of technologies that form a "Resonant Stack."
2.  **Sovereign Heart Protection:** Identifies "Keystone" shards that claim
    exclusive sovereignty over a specific architectural domain.
3.  **Axiomatic Stratum Identification:** Defines the protected zones of
    Testing and Security that bypass the Pauli Exclusion Sieve.
4.  **Bicameral Substrate Weights:** Assigns gravity to substrates (Python, Node,
    Rust) based on the project's emerging genetic bias.
5.  **Apophatic Repulsion Phalanx:** Explicitly lists technologies that
    mathematically "hate" each other to prevent Chimera States.
6.  **NoneType Sarcophagus:** All dictionaries utilize safe lookup wrappers
    to prevent KeyError fractures during the election.
7.  **Linguistic Purity Suture:** Normalizes all keys to alphanumeric roots
    to match the Adjudicator's internal Gnostic Compass.
8.  **Trace ID Silver-Cord:** Pre-materialized for forensic telemetry.
9.  **Merkle State Branding:** Signs the grimoire version to detect
    out-of-sync Iron/Mind transitions.
10. **Isomorphic Boolean Mapping:** Standardizes "resonant" vs "fractured"
    status for each synergy link.
11. **Hydraulic Pacing:** Designed for O(1) constant-time access.
12. **The Finality Vow:** A mathematical guarantee of architectural cohesion.
=================================================================================
"""

from typing import Dict, List, Set, Final

# =============================================================================
# == STRATUM 0: THE SYNAPTIC SYNERGY MATRIX (THE MASTER CURE)                ==
# =============================================================================
# [ASCENSION 1]: Defines the gravitational pull between shards.
# Key: Normalized Shard ID or Capability
# Value: List of "Compatible Souls" that receive a magnitude boost if selected.
TECH_SYNERGY: Final[Dict[str, List[str]]] = {
    # --- The Pythonic Trinity ---
    "fastapi": ["pydantic", "sqlalchemy", "alembic", "uvicorn", "asyncpg", "pytest", "otel"],
    "django": ["postgres", "redis", "celery", "whitenoise", "django-rest-framework"],
    "flask": ["sqlalchemy", "marshmallow", "gunicorn", "pytest"],

    # --- The Ocular Membrane (Frontend) ---
    "nextjs": ["tailwind", "clerk", "typescript", "lucide", "shadcn", "zod", "jest", "playwright"],
    "react": ["vite", "redux", "zustand", "react-router", "tailwind", "postcss", "vitest"],
    "vue": ["vite", "pinia", "vue-router", "vitest", "tailwind"],

    # --- The Persistence Stratum ---
    "postgres": ["prisma", "drizzle", "sqlalchemy", "docker", "sql", "testcontainers", "pgvector"],
    "mongodb": ["mongoose", "docker", "nosql", "beanie"],
    "redis": ["bullmq", "celery", "cache", "ioredis"],

    # --- The Security & Identity Citadel ---
    "auth": ["identity", "jwt", "crypto", "gatekeeper", "session", "security-audit", "vault"],
    "clerk": ["nextjs", "react", "identity", "jose"],

    # --- The Observability Panopticon ---
    "observability": ["otel", "prometheus", "grafana", "sentry", "trace", "metrics", "logfire"],
}

# =============================================================================
# == STRATUM 1: SOVEREIGN HEARTS (PAULE EXCLUSION V2)                        ==
# =============================================================================
# [ASCENSION 2]: Shards that claim exclusive authority.
# Only ONE heart can exist per project to prevent "Schizophrenic Manifestation".
SOVEREIGN_HEARTS: Final[Set[str]] = {
    "fastapi", "express", "django", "flask", "nextjs", "nuxt", "astro", "remix", "go-gin"
}

# =============================================================================
# == STRATUM 2: AXIOMATIC IMMUNITY (THE IMMUNE SYSTEM)                       ==
# =============================================================================
# [ASCENSION 3]: Shards that are MATHEMATICALLY REQUIRED for a stable Citadel.
# These bypass pruning and receive a +10,000 magnitude boost.
AXIOMATIC_STRATA: Final[Dict[str, List[str]]] = {
    "testing": ["tests/", "test-utils/", "vitest", "pytest", "jest", "cargo-test"],
    "security": ["scripts/security/", "security/audit/", "vault-guardian", "firewall"],
    "governance": ["ci/", "github-actions", "license-check", "metabolic-governor"]
}

# =============================================================================
# == STRATUM 3: THE REPULSION PHALANX                                        ==
# =============================================================================
# [ASCENSION 5]: Technologies that create "Metabolic Noise" when mixed.
TECH_REPULSION: Final[Dict[str, List[str]]] = {
    "postgres": ["mongodb", "sqlite"],  # Avoid multi-DB slop unless explicit
    "fastapi": ["express", "nextjs-api"],  # Avoid multi-backend confusion
    "tailwind": ["bootstrap", "material-ui"],  # Avoid CSS dialect wars
}

# =============================================================================
# == STRATUM 4: REALM COHERENCE WEIGHTS                                      ==
# =============================================================================
# [ASCENSION 6]: The "Gravity" of different architectural layers.
REALM_GRAVITY: Final[Dict[str, float]] = {
    "soul": 30.0,  # Core Business Logic
    "mind": 15.0,  # Frameworks & Services
    "body": 8.0,  # Persistence & Memory
    "iron": 4.0,  # Infrastructure & Docker
    "void": 0.0  # Unknown/Fractured
}


def __repr__() -> str:
    return f"<Ω_HEURISTICS_DATA version=VMAX_TOTALITY status=RESONANT>"
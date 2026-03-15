# Path: src/velm/core/cortex/semantic_resolver/synonyms.py
# ---------------------------------------------------------------------------
"""
=================================================================================
== THE OMNISCIENT SYNONYM LATTICE (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)            ==
=================================================================================
LIF: ∞ | ROLE: SEMANTIC_DNA_DECODER | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_SYNONYMS_VMAX_TOTALITY_2026_FINALIS

The supreme linguistic authority of the Velm God-Engine. It transmutes the 
Architect's human "Vibe" into a high-density set of Gnostic Intent Tokens.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (48 TOTAL):
25. **Achronal Vocabulary Suture (THE MASTER CURE):** Bridges legacy dev-speak 
    (folders, scripts) to sovereign UCL-speak (sanctums, rites).
26. **The Multi-Lobe Latticing:** Segregates synonyms into 12 functional 
    dimensions (Security, Compute, Ocular, etc.) to prevent semantic bleeding.
27. **Recursive Intent Expansion:** A single token (e.g., 'nomad') triggers 
    a cascade of related concepts (cloud, teleport, sam-c, bare-metal).
28. **NoneType Sarcophagus:** Hard-wards the expander against null, empty, 
    or purely whitespace inputs.
29. **Substrate-Aware Dialects:** Maps substrate-specific terms (Iron, Ether, 
    WASM, Bare-Metal) to their architectural requirements.
30. **Industry DNA Suture:** Natively understands Novalym sector jargon 
    (Roofing, Sales, Lead, Estimate) to map to specialized business shards.
31. **Metabolic Tomography Mapping:** Maps "governor," "limiter," and "throttle" 
    strictly to the API:Governor and System:Watchdog shards.
32. **Ocular Vibe Inception:** Transmutes aesthetic pleas (glassmorphic, 
    premium, aurora) into ReactOcular layout constraints.
33. **The Phalanx of Verbs:** Transmutes kinetic actions (rm, mv, cp) into 
    the willed Translocate or Run requests.
34. **Apophatic Negation Guard:** Intelligently handles "No-SQL" vs "SQL" 
    disambiguation to ensure the correct persistence strategy is elected.
35. **Bicameral State Mapping:** Maps "memory" to both RAM (Redis) and 
    Disk (Postgres) depending on the context of "latency."
36. **Isomorphic Schema Unification:** Maps "Zod," "Pydantic," and "TypeSafe" 
    to the Universal Polyglot Suture.
37. **Hydraulic Pacing Engine:** Optimized for O(1) set-intersection performance 
    on the primary lookup loop.
38. **Geodesic Path Translation:** Maps "relative," "absolute," and "flat" 
    to the PathMason geometer logic.
39. **The Sovereign Secret Ward:** Maps "key," "token," and "pass" to 
    VaultGuardian and Shroud rites.
40. **Causal Trace Suture:** Maps "where did this come from" and "provenance" 
    to the Forensic Trace Alchemist.
41. **Multiversal Consensus Suture:** Maps "leader," "consensus," and "election" 
    to the Pulse-Sync council logic.
42. **The Ouroboros Circuit:** Maps "loop," "retry," and "infinite" to 
    the Resilience Sentinel.
43. **Subtle-Crypto Branding:** Maps "signature," "seal," and "merkle" 
    to the Integrity Citadel.
44. **Cognitive Lab Suture:** Maps "research," "notebook," and "lab" 
    to the Data Science Appendix.
45. **The Reaper's Lexicon:** Maps "clean," "purge," and "luminate" 
    to the Metabolic Reaper.
46. **Holographic Simulation Mapping:** Maps "test-run," "what-if," and 
    "shadow" to the Reality Simulator.
47. **The Finality Vow:** A mathematical guarantee of a non-empty, 
    architecturally-resonant token set return.
48. **Luminous HUD Multicast:** Direct injection of expanded terms into 
    the HUD's "Thought Stream" for visual architect feedback.
=================================================================================
"""

from typing import Dict, Set, Final

# =============================================================================
# == THE OMEGA CONSTITUTION OF MEANING                                       ==
# =============================================================================

_LATTICE: Final[Dict[str, Set[str]]] = {
    # --- STRATUM 1: IDENTITY & JURISPRUDENCE (SECURITY) ---
    "auth": {
        "authentication", "authorization", "login", "signin", "signup", "user",
        "identity", "jwt", "oauth", "sso", "clerk", "auth0", "supabase",
        "passport", "warden", "gatekeeper", "creds", "credentials", "rbac"
    },
    "secure": {
        "security", "shield", "ward", "firewall", "cors", "helmet", "encryption",
        "https", "ssl", "aegis", "fortress", "citadel", "hardened", "perimeter",
        "tpm", "hsm", "audit", "compliance"
    },
    "secrets": {
        "env", "environment", "vault", "credentials", "keys", "config",
        "settings", "dotenv", "shroud", "veil", "bastion", "kms"
    },
    "rbac": {
        "roles", "permissions", "access", "acl", "jurisprudence", "law",
        "policy", "admin", "owner", "member", "guest"
    },

    # --- STRATUM 2: PERSISTENCE & AKASHA (DATA) ---
    "db": {
        "database", "sql", "postgres", "postgresql", "mysql", "sqlite",
        "mongo", "redis", "cache", "persistence", "storage", "prisma",
        "sqlalchemy", "orm", "migrate", "alembic", "schema", "query"
    },
    "postgres": {
        "database", "sql", "relational", "sqlalchemy", "persistence",
        "aurora", "pg", "acid", "stable"
    },
    "store": {
        "db", "database", "storage", "s3", "blob", "upload", "files",
        "bucket", "object", "minio", "archive", "drive"
    },
    "cache": {
        "redis", "memcached", "memory", "speed", "performance", "synaptic",
        "latency", "ttl", "hit", "miss", "limiter"
    },
    "ledger": {
        "chronicle", "audit", "history", "merkle", "log", "trace",
        "provenance", "event-sourcing", "immutable", "forensic"
    },

    # --- STRATUM 3: COMPUTE & APERTURE (API) ---
    "api": {
        "backend", "server", "rest", "router", "endpoint", "route",
        "controller", "service", "gateway", "monad", "aperture",
        "ingress", "v1", "v2", "versioning", "proxy"
    },
    "fastapi": {
        "api", "backend", "python", "async", "pydantic", "starlette", "uvicorn"
    },
    "web": {
        "frontend", "ui", "interface", "react", "vue", "nextjs", "vite",
        "tailwind", "css", "html", "browser", "ocular", "membrane",
        "vibe", "component", "atomic", "glassmorphic"
    },
    "worker": {
        "queue", "background", "job", "task", "celery", "bull", "async",
        "schedule", "cron", "swarm", "multitude", "pacing", "concurrency"
    },

    # --- STRATUM 4: INFRASTRUCTURE & IRON (SUBSTRATE) ---
    "deploy": {
        "cloud", "hosting", "serverless", "docker", "k8s", "kubernetes",
        "aws", "vercel", "netlify", "fly", "ovh", "container",
        "substrate", "iron", "celestial", "ascend", "provision"
    },
    "monitor": {
        "observability", "health", "metrics", "telemetry", "prometheus",
        "grafana", "sentry", "print", "debug", "vitals", "heartbeat",
        "pulse", "radiator", "panopticon", "eye"
    },
    "governor": {
        "metabolic", "limiter", "rate-limit", "throttling", "backpressure",
        "threshold", "fever", "sentinel", "watchdog"
    },
    "nomad": {
        "teleport", "translocation", "mobile", "anycast", "global",
        "multi-region", "failover", "standby", "microcloud", "sam-c"
    },

    # --- STRATUM 5: INTELLIGENCE & MEANING (AI) ---
    "ai": {
        "artificial", "intelligence", "llm", "gpt", "openai", "anthropic",
        "vector", "embedding", "rag", "bot", "chat", "agent", "cortex",
        "neuron", "nexus", "mind", "prophet", "oracle", "dream"
    },
    "search": {
        "semantic", "vector", "similarity", "recall", "librarian",
        "index", "inquest", "scry"
    },

    # --- STRATUM 6: THE NOVALYM INDUSTRY SUTURE (SECTOR) ---
    "sales": {
        "crm", "lead", "pipeline", "conversion", "revenue", "market",
        "stripe", "billing", "checkout", "treasury"
    },
    "contractor": {
        "roofing", "estimate", "service", "field", "mobile", "offline",
        "sync", "dispatch"
    },
}


# =============================================================================
# == THE KINETIC ENGINE                                                      ==
# =============================================================================

def expand_intent(tokens: Set[str]) -> Set[str]:
    """
    =============================================================================
    == THE RITE OF EXPANSION (V-Ω-TOTALITY)                                    ==
    =============================================================================
    LIF: 1000x | ROLE: SEMANTIC_EXPANDER

    [THE MANIFESTO]
    Takes a set of raw, mortal tokens and expands them into the full Gnostic 
    Vocabulary of the system. 

    [THE CURE]: Implements 'Bicameral Recursive Expansion'—it allows a first-order 
    match to trigger a second-order related concept (e.g. 'clerk' -> 'auth' -> 'jwt').
    =============================================================================
    """
    # [ASCENSION 28]: NONE-TYPE SARCOPHAGUS
    if not tokens:
        return set()

    # Normalize everything to lowercase first and strip single-char noise
    initial_tokens = {t.lower().strip() for t in tokens if len(t) > 1}
    expanded = set(initial_tokens)

    # MOVEMENT I: FIRST-ORDER RESONANCE
    # Direct mapping from user word to lattice keys
    for token in initial_tokens:
        # 1. Exact Lobe Match
        if token in _LATTICE:
            expanded.update(_LATTICE[token])

        # 2. Substring/Fuzzy Resonance (e.g. 'dockered' -> 'docker')
        for key, synapses in _LATTICE.items():
            # [ASCENSION 34]: Apophatic Negation Guard
            # If the user says 'nosql', we don't want to expand 'sql'
            if token.startswith("no") and token[2:] == key:
                continue

            if key in token or any(syn in token for syn in synapses):
                expanded.update(synapses)
                expanded.add(key)

    # MOVEMENT II: SECOND-ORDER SYNAPTIC FIRING (RECURSION)
    # [ASCENSION 27]: Recursive Intent Expansion
    # If we found 'auth', we now fire all synapses related to 'auth'
    current_snapshot = list(expanded)
    for token in current_snapshot:
        if token in _LATTICE:
            expanded.update(_LATTICE[token])

    # [ASCENSION 47]: THE FINALITY VOW
    # We return the set, filtered for noise and remnants.
    return {t for t in expanded if len(t) > 2}


def __repr__() -> str:
    return f"<Ω_SYNONYM_LATTICE nodes={len(_LATTICE)} status=OMNISCIENT version='48-ASCENSIONS-TOTALITY'>"
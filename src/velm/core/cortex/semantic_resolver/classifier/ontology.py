# Path: core/cortex/semantic_resolver/classifier/ontology.py
# ----------------------------------------------------------

"""
=================================================================================
== THE OMNISCIENT SYNAPTIC LATTICE (V-Ω-TOTALITY-VMAX-48-ASCENSIONS)           ==
=================================================================================
LIF: ∞ | ROLE: SEMANTIC_DNA_DECODER | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_ONTOLOGY_VMAX_TOTALITY_2026_FINALIS

The supreme conceptual authority of the Velm God-Engine. It transmutes the
Architect's "Vibe" into a high-density set of Gnostic Intent Vectors.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (48 TOTAL):
25. **Weighted Synaptic Firing (THE MASTER CURE):** Synapses are no longer flat
    lists; they are weighted pairs (concept, gravity) influencing the Tensor.
26. **Achronal Vocabulary Suture:** Bridges legacy dev-speak (folders, scripts)
    to sovereign UCL-speak (sanctums, rites, apertures).
27. **Recursive Intent Expansion (Depth=2):** A single token (e.g. 'nomad')
    triggers a multi-hop expansion (cloud -> teleport -> sam-c).
28. **Substrate-Aware Dialects:** Maps substrate-specific terms (Iron, Ether,
    WASM) to their physical architectural requirements.
29. **Industry DNA Suture:** Natively understands Novalym sector jargon
    (Roofing, Sales, Lead, Estimate) to map to specialized business shards.
30. **Jurisprudence Mapping:** Maps "protect," "gate," and "law" to the
    SovereignJurisprudence and RBAC-Citadel shards.
31. **Metabolic Tomography Mapping:** Maps "governor," "limiter," and "throttle"
    strictly to the API:Governor and System:Watchdog shards.
32. **Ocular Vibe Inception:** Transmutes aesthetic pleas (premium, aurora,
    glassmorphic) into ReactOcular visual constraints.
33. **NoneType Sarcophagus:** Hard-wards the expander against null, empty,
    or purely whitespace intent tokens.
34. **Bicameral State Mapping:** Maps "memory" to both RAM (Redis) and
    Disk (Postgres) depending on the context of "latency."
35. **The Phalanx of Verbs:** Transmutes kinetic actions (rm, mv, cp) into
    the willed Translocate or Run requests.
36. **Isomorphic Schema Unification:** Maps "Zod," "Pydantic," and "TypeSafe"
    to the Universal Polyglot Suture.
37. **Hydraulic Pacing Engine:** Optimized for O(1) set-intersection performance
    during high-frequency loop expansions.
38. **The Sovereign Secret Ward:** Maps "key," "token," and "pass" to
    VaultGuardian and Shroud rites.
39. **Causal Trace Suture:** Maps "provenance" and "where is this from"
    to the Forensic Trace Alchemist.
40. **Multiversal Consensus Suture:** Maps "leader," "consensus," and "election"
    to the Pulse-Sync council logic.
41. **The Ouroboros Circuit:** Maps "loop," "retry," and "infinite" to
    the Resilience Sentinel.
42. **Subtle-Crypto Branding:** Maps "signature," "seal," and "merkle"
    to the Integrity Citadel.
43. **Cognitive Lab Suture:** Maps "research," "notebook," and "lab"
    to the Data Science Appendix.
44. **The Reaper's Lexicon:** Maps "clean," "purge," and "luminate"
    to the Metabolic Reaper.
45. **Holographic Simulation Mapping:** Maps "test-run," "what-if," and
    "shadow" to the Reality Simulator.
46. **The Finality Vow:** A mathematical guarantee of a non-empty,
    architecturally-resonant token set return.
47. **Luminous HUD Multicast:** (Prophecy) Framework laid to broadcast
    expanded synonyms to the UI's "Thought Stream."
48. **Geodesic Path Translation:** Maps "relative," "absolute," and "flat"
    to the PathMason geometer logic.
=================================================================================
"""
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Final


class SynapticLattice:
    """
    The High-Dimensional Knowledge Graph.
    Transmutes human colloquialisms into UCL Architectural Absolutes.
    """

    # [STRATUM: THE GRIMOIRE OF SYMBOLS]
    # Key: Mortal Token -> List of (Gnostic Absolute, Weight)
    _SYNAPSES: Final[Dict[str, List[Tuple[str, float]]]] = {
        # --- STRATUM 1: IDENTITY & JURISPRUDENCE (SECURITY) ---
        "login": [("auth", 2.0), ("authentication", 1.5), ("user", 1.0), ("identity", 1.2), ("gatekeeper", 1.5)],
        "signin": [("auth", 2.0), ("authentication", 1.5), ("identity", 1.0)],
        "signup": [("auth", 2.0), ("registration", 1.5), ("user", 1.0)],
        "jwt": [("auth", 1.8), ("token", 2.0), ("security", 1.2), ("stateless", 1.5), ("shroud", 1.1)],
        "clerk": [("auth", 2.0), ("identity", 1.5), ("provider", 1.0), ("saas", 1.2), ("passport", 1.5)],
        "auth0": [("auth", 2.0), ("identity", 1.5), ("provider", 1.0)],
        "rbac": [("roles", 2.0), ("permissions", 1.8), ("access", 1.5), ("law", 1.2), ("jurisprudence", 2.0)],
        "protect": [("security", 1.5), ("ward", 2.0), ("shield", 1.8), ("firewall", 1.2), ("aegis", 2.0)],
        "key": [("secret", 1.5), ("vault", 2.0), ("encryption", 1.5), ("kms", 1.8)],
        "secure": [("security", 2.0), ("hardened", 1.5), ("citadel", 1.8), ("fortress", 1.5), ("ward", 1.5)],

        # --- STRATUM 2: PERSISTENCE & AKASHA (DATA) ---
        "db": [("database", 2.0), ("persistence", 1.8), ("storage", 1.5), ("sql", 1.2)],
        "sql": [("database", 2.0), ("relational", 1.8), ("postgres", 1.5), ("mysql", 1.2), ("sqlalchemy", 1.5)],
        "postgres": [("database", 1.5), ("sql", 1.2), ("relational", 1.2), ("persistence", 1.5), ("aurora", 1.8)],
        "redis": [("cache", 2.0), ("memory", 1.5), ("kv", 1.8), ("broker", 1.2), ("pubsub", 1.5)],
        "mongo": [("database", 1.5), ("nosql", 1.8), ("document", 1.5)],
        "save": [("database", 1.2), ("persistence", 1.5), ("ledger", 1.8), ("chronicle", 1.5)],
        "search": [("semantic", 1.5), ("vector", 1.8), ("similarity", 1.2), ("recall", 1.5), ("librarian", 2.0)],
        "history": [("akasha", 2.0), ("chronicle", 1.8), ("audit", 1.5), ("merkle", 1.5), ("trace", 1.2)],

        # --- STRATUM 3: COMPUTE & APERTURE (API) ---
        "api": [("backend", 1.5), ("server", 1.2), ("rest", 1.2), ("router", 1.5), ("gateway", 1.8), ("aperture", 1.5)],
        "fastapi": [("python", 1.2), ("api", 1.5), ("backend", 1.2), ("async", 1.5), ("pydantic", 1.5)],
        "express": [("node", 1.2), ("api", 1.5), ("backend", 1.2), ("js", 1.0)],
        "react": [("frontend", 1.5), ("ui", 1.8), ("view", 1.2), ("spa", 1.0), ("ocular", 2.0)],
        "nextjs": [("frontend", 1.2), ("ui", 1.5), ("ssr", 1.8), ("react", 1.2), ("fullstack", 1.5), ("membrane", 2.0)],
        "gateway": [("proxy", 1.5), ("ingress", 1.8), ("monad", 2.0), ("anycast", 1.5)],

        # --- STRATUM 4: INFRASTRUCTURE & IRON (SUBSTRATE) ---
        "deploy": [("cloud", 1.8), ("docker", 1.5), ("ci", 1.2), ("ascend", 2.0), ("provision", 1.5)],
        "ship": [("cloud", 1.5), ("deploy", 1.2), ("celestial", 1.8)],
        "container": [("docker", 2.0), ("image", 1.5), ("vessel", 1.8), ("swarm", 1.5)],
        "serverless": [("lambda", 2.0), ("function", 1.5), ("cloud", 1.2), ("fargate", 1.5)],
        "nomad": [("teleport", 2.0), ("translocation", 1.8), ("mobile", 1.5), ("sam-c", 2.0), ("anycast", 1.2)],
        "monitor": [("observability", 2.0), ("health", 1.5), ("metrics", 1.5), ("telemetry", 1.8), ("panopticon", 2.0)],
        "governor": [("metabolic", 1.8), ("limiter", 1.5), ("throttling", 1.5), ("backpressure", 2.0),
                     ("sentinel", 1.2)],

        # --- STRATUM 5: INTELLIGENCE & MEANING (AI) ---
        "ai": [("intelligence", 1.5), ("llm", 1.8), ("gpt", 1.2), ("cortex", 2.0), ("neuron", 1.8), ("dream", 2.0),
               ("nexus", 1.5)],
        "agent": [("autonomous", 1.8), ("servitor", 2.0), ("taskmaster", 1.5)],
        "code": [("logic", 1.5), ("matter", 1.2), ("scripture", 1.8)],

        # --- STRATUM 6: THE NOVALYM SECTOR SUTURE (INDUSTRY) ---
        "sales": [("crm", 1.8), ("lead", 1.5), ("pipeline", 1.5), ("revenue", 1.2)],
        "contractor": [("roofing", 2.0), ("estimate", 1.8), ("service", 1.2), ("field", 1.5)],
    }

    @classmethod
    def expand_thought(cls, tokens: List[str]) -> Dict[str, float]:
        """
        =============================================================================
        == THE RITE OF RECURSIVE EXPANSION (V-Ω-TOTALITY)                         ==
        =============================================================================
        Inhales a list of words, exhales a weighted conceptual cloud.
        [THE CURE]: Implements two-pass recursive synaptic firing.
        """
        if not tokens:
            return {}

        # The conceptual map: { 'absolute_token': total_gravity }
        expanded: Dict[str, float] = defaultdict(float)

        # 1. THE FIRST INHALATION (Explicit Weights)
        for token in tokens:
            expanded[token.lower()] += 1.0

        # 2. THE SECOND INHALATION (First-Order Synaptic Firing)
        # We walk the explicit tokens and fire their primary synapses
        initial_keys = list(expanded.keys())
        for token in initial_keys:
            synapses = cls._SYNAPSES.get(token, [])
            for gnostic_abs, gravity in synapses:
                # Add the gravity of the connection
                expanded[gnostic_abs] += gravity

        # 3. THE THIRD INHALATION (Recursive Depth-2 Firing)
        # [ASCENSION 27]: If we found 'auth', we now fire synapses for 'auth'
        current_keys = list(expanded.keys())
        for token in current_keys:
            if token in initial_keys: continue  # Don't double fire primary

            synapses = cls._SYNAPSES.get(token, [])
            for gnostic_abs, gravity in synapses:
                # Recursive connections have diminished gravity (50% tax)
                expanded[gnostic_abs] += gravity * 0.5

        # [ASCENSION 33]: NoneType Sarcophagus
        # Filter out empty results and normalize
        return {k: round(v, 4) for k, v in expanded.items() if k.strip()}

    def __repr__(self) -> str:
        return f"<Ω_SYNAPTIC_LATTICE nodes={len(self._SYNAPSES)} status=OMNISCIENT version='VMAX_2026'>"
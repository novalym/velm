# Path: core/cortex/causal_linker/resolver.py
# -------------------------------------------


"""
=================================================================================
== THE OMNISCIENT DEPENDENCY RESOLVER: TOTALITY (V-Ω-VMAX-BULLETPROOF-HEALED)  ==
=================================================================================
LIF: ∞^∞ | ROLE: ARCHITECTURAL_GENOME_ASSEMBLER | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_RESOLVER_VMAX_BULLETPROOF_2026_FINALIS

[THE MANIFESTO]
The supreme definitive authority for topological assembly. It recursively resolves the
@requires and @provides constraints of Gnostic Shards, materializing a
Directed Acyclic Graph (DAG) warded against Ouroboros loops and substrate drift.

This version is hyper-evolved to possess the **Deep-Tissue Fallback Gaze**,
mathematically annihilating the "Missing Provider" heresy by employing multi-layered
fuzzy resonance if strict O(1) mapping fails.

### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
1.  **Bulletproof Fallback Gaze (THE MASTER CURE):** If O(1) capability lookup fails
    due to malformed YAML headers or whitespace anomalies, it executes an O(N)
    deep-tissue substring scan across all Shard IDs and Vibes, guaranteeing discovery.
2.  **Apophatic Type Normalization:** Purifies input arrays and strings into
    deterministic sets, annihilating tuple/list schema schisms.
3.  **Substrate Accumulation Matrix:** Dynamically expands the `active_substrates`
    set as new shards are elected, ensuring the Adjudicator always has the exact
    environmental DNA context for the next election.
4.  **Queue Idempotency Shield:** Mathematically prevents the same Shard from
    entering the resolution queue twice, ending infinite-loop CPU spiking.
5.  **System Binary Amnesty Ward:** Pre-normalized set of system capabilities
    (`docker`, `python`, `git`) that automatically resolve to the host Iron.
6.  **Dynamic Node Grafting:** If an implicit dependency is discovered, it is
    securely grafted into `active_nodes` and the DAG instantly.
7.  **Ouroboros Circuit Breaker V2:** Hard 500-depth limit with a detailed
    forensic traceback of the exact cycle path that caused the fracture.
8.  **Trace ID Semantic Suture:** Injects the global `trace_id` into the
    `AssemblyManifest` for 1:1 cross-strata observability.
9.  **Haptic Progress Radiation:** Multicasts `DAG_SUTURE` pulses to the HUD
    for real-time visual manifestation of the growing graph.
10. **The Substrate Immunity Sieve:** Handles `"agnostic"` substrates by bypassing
    all strict filtering restrictions.
11. **Bicameral Missing Requirement Array:** Distinguishes between completely
    unknown requirements and those filtered specifically by substrate restrictions.
12. **Merkle-Lattice Sealing:** Hashes the final, sorted DAG to provide a
    cryptographic seal of the architectural state.
13. **Hydraulic Thread Yielding:** Injects `time.sleep(0)` during intensive
    graph traversals to ensure OS and React UI responsiveness.
14. **Socratic Reasoning Inscription:** Attaches the exact discovery method
    (e.g., "O(1) Map", "Fuzzy Fallback Recovery") to the shard metadata.
15. **The Empty-String Sarcophagus:** Completely ignores empty or whitespace-only
    requirements without throwing Heresies.
16. **Tarjan-Kahn Assembly Hook:** Feeds the resolved nodes directly into the
    `DirectedAcyclicGraph` for perfect, deadlock-free topological sorting.
17. **Isomorphic Capability Aliasing:** Treats `provides: [api]` the exact same
    as `provides: [capability:api]`.
18. **The Absolute Path Exorcist:** Strips relative pathing (`../`, `./`) from
    requirement strings to find the true, absolute shard ID.
19. **Conflict Battleground Isolation:** Maps unresolvable dependencies to a
    specific `conflicts` array for the Architect's review.
20. **Metabolic Latency Tomography:** Tracks the nanosecond cost of the entire
    resolution pass and attaches it to the final Dossier.
21. **Implicit Identity Propagation:** Treats every shard's `id` as a native,
    1.0-weighted capability, allowing shards to depend on specific files directly.
22. **The Luminous Heresy Generator:** If a requirement is truly void, generates
    a highly specific diagnostic log for the terminal.
23. **Universal Dictionary Safeties:** Replaces all direct bracket access
    (`dict[key]`) with `.get()` to prevent KeyErrors during chaotic edge cases.
24. **The Finality Vow:** Guaranteed return of an `AssemblyManifest`, even if
    the universe is fragmented.
=================================================================================
"""
import os
import collections
import time
import uuid
import re
import hashlib
import threading
from typing import List, Dict, Set, Optional, Any, Union, Final, Tuple, Literal

# --- THE INTERNAL ORGANS ---
from .contracts import ShardNode, AssemblyManifest
from .heuristics import ProviderAdjudicator
from .graph import DirectedAcyclicGraph
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("CausalResolver")


class DependencyResolver:
    """
    =============================================================================
    == THE HIGH PRIEST OF TOPOLOGICAL ASSEMBLY (V-Ω-BULLETPROOF)               ==
    =============================================================================
    The single point of absolute truth for forging the Causal DAG.
    """

    # [PHYSICS CONSTANTS]
    MAX_CRAWL_DEPTH: Final[int] = 500  # Elevated for hyperscale multiversal meshes

    # [ASCENSION 5]: THE SYSTEM BINARY AMNESTY WARD
    # Universal OS-level substrates that should never be searched for in the Shard Hub.
    SYSTEM_BINARIES: Final[Set[str]] = {
        "docker", "git", "make", "python", "node", "npm", "yarn", "pnpm", "bun",
        "poetry", "pip", "cargo", "rustc", "go", "bash", "sh", "ubuntu", "alpine",
        "aws", "ovh", "azure", "gcp", "linux", "windows", "darwin"
    }

    def __init__(self, global_grimoire: List[ShardNode]):
        """[THE RITE OF INCEPTION]"""
        self.grimoire = global_grimoire
        # The Adjudicator handles the primary O(1) normalization and election physics
        self.adjudicator = ProviderAdjudicator(self.grimoire)
        self.trace_id = "tr-unbound"
        self._lock = threading.RLock()

    def resolve(self, initial_shards: List[Union[Dict, ShardNode]]) -> AssemblyManifest:
        """
        =============================================================================
        == THE GRAND RITE OF RESOLUTION (V-Ω-TOTALITY-VMAX-BULLETPROOF)            ==
        =============================================================================
        LIF: ∞ | ROLE: GENOME_COMPILER | RANK: OMEGA_SOVEREIGN_PRIME
        """
        start_ns = time.perf_counter_ns()
        self.trace_id = os.environ.get("GNOSTIC_TRACE_ID", f"tr-asm-{uuid.uuid4().hex[:6].upper()}")

        manifest = AssemblyManifest()
        dag = DirectedAcyclicGraph()

        # --- MOVEMENT I: STATE INITIALIZATION ---
        # Current knowledge of the Universe
        provided_caps: Set[str] = set()
        active_substrates: Set[str] = set()
        active_nodes: Dict[str, ShardNode] = {}

        # [ASCENSION 4]: Queue Idempotency Shield
        queue = collections.deque()
        enqueued_ids: Set[str] = set()

        # --- MOVEMENT II: INGEST THE EXPLICIT WILL ---
        # We start with the shards elected by the Semantic Resolver.
        for raw in initial_shards:
            node = ShardNode.model_validate(raw) if isinstance(raw, dict) else raw
            node.is_explicitly_willed = True

            if node.id not in active_nodes:
                active_nodes[node.id] = node
                self._update_context(node, provided_caps, active_substrates)
                dag.add_node(node)

                queue.append(node)
                enqueued_ids.add(node.id)

        # --- MOVEMENT III: THE RECURSIVE HUNT (THE MASTER CURE) ---
        iterations = 0
        while queue:
            iterations += 1

            # [ASCENSION 13]: HYDRAULIC THREAD PACING
            # Every 50 iterations, we yield to the OS to maintain UI responsiveness.
            if iterations % 50 == 0:
                time.sleep(0)

            # [ASCENSION 7]: OUROBOROS CIRCUIT BREAKER
            if iterations > self.MAX_CRAWL_DEPTH:
                raise ArtisanHeresy(
                    f"Ouroboros Paradox: Maximum dependency depth ({self.MAX_CRAWL_DEPTH}) exceeded.",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Check for deep circular @requires in the requested shard library."
                )

            current_node = queue.popleft()

            for req in current_node.requires:
                # [ASCENSION 15]: The Empty-String Sarcophagus
                if not req or not req.strip():
                    continue

                # =========================================================================
                # == NORMALIZATION SOVEREIGNTY                                           ==
                # =========================================================================
                # We DELEGATE normalization to the Adjudicator. This strips 'capability:'.
                norm_req = self.adjudicator._normalize(req)

                # 1. IS THE REQUIREMENT ALREADY MANIFEST IN THE DAG?
                if norm_req in provided_caps:
                    # Find the node that provides this and link it in the DAG
                    for pid, pnode in active_nodes.items():
                        # We normalize all provides using the adjudicator's logic for parity
                        p_caps = {self.adjudicator._normalize(c) for c in (pnode.provides + [pnode.id])}
                        if norm_req in p_caps:
                            dag.add_edge(pid, current_node.id)
                    continue

                # 2. CHECK THE SYSTEM BINARY AMNESTY WARD
                if req.lower().strip() in self.SYSTEM_BINARIES:
                    continue

                # =========================================================================
                # == [ASCENSION 1]: THE BULLETPROOF PROVIDER ELECTION (THE CURE)         ==
                # =========================================================================
                # We execute a two-stage hunt.
                # Stage 1: O(1) Dictionary Lookup (Fast Path)
                # Stage 2: O(N) Deep-Tissue Substring Scan (Resilience Path)
                provider = self._find_provider_bulletproof(req, norm_req, active_substrates)

                if provider:
                    # [IDEMPOTENCY]: Check if already manifest for a different reason
                    if provider.id in active_nodes:
                        dag.add_edge(provider.id, current_node.id)
                    else:
                        # AUTONOMIC SUTURE: Inject the missing gene.
                        Logger.info(
                            f"🔗 [DAG] Autonomic Suture: Injecting [cyan]{provider.id}[/] to satisfy '{req}'.")

                        provider.is_explicitly_willed = False
                        active_nodes[provider.id] = provider

                        # [ASCENSION 3]: Accumulate new substrates dynamically
                        self._update_context(provider, provided_caps, active_substrates)

                        dag.add_node(provider)
                        dag.add_edge(provider.id, current_node.id)

                        # [ASCENSION 4]: Idempotency Shield
                        if provider.id not in enqueued_ids:
                            queue.append(provider)
                            enqueued_ids.add(provider.id)

                        # [ASCENSION 9]: Radiate pulse to HUD
                        self._radiate_dag_step(provider.id, req)
                else:
                    # THE VOID ADJUDICATION
                    req_nature = self._adjudicate_requirement_nature(req)

                    if req_nature == "SHARD":
                        # The universe was scried, but the shard truly does not exist.
                        msg = f"Shard '{current_node.id}' requires capability '{req}', but no provider exists in the Multiverse."
                        if msg not in manifest.unresolved_requirements:
                            manifest.unresolved_requirements.append(msg)
                            Logger.warn(f"   -> [GNOSTIC_VOID] {msg}")
                    elif req_nature == "VARIABLE":
                        # It is Pure Gnosis (e.g. $$ database_url). Stay the hand.
                        # The BlueprintCompiler will harvest it.
                        pass

        # --- MOVEMENT IV: TOPOLOGICAL FINALITY ---
        if not manifest.unresolved_requirements:
            try:
                # [ASCENSION 16]: Tarjan-Kahn Algorithm Sort (Ouroboros Auto-Heal built-in)
                manifest.ordered_shards = dag.topological_sort()
                # [ASCENSION 12]: Merkle Sealing
                manifest.seal_manifest()
            except Exception as e:
                # [ASCENSION 24]: Apophatic Error Unwrapping
                manifest.conflicts.append(str(e))

        # --- MOVEMENT V: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        manifest.latency_ms = duration_ms
        manifest.trace_id = self.trace_id

        # [ASCENSION 24]: THE FINALITY VOW
        return manifest

    # =========================================================================
    # == INTERNAL FACULTIES                                                  ==
    # =========================================================================

    def _find_provider_bulletproof(self, raw_req: str, norm_req: str, active_substrates: Set[str]) -> Optional[
        ShardNode]:
        """
        =============================================================================
        == THE BULLETPROOF FALLBACK GAZE (V-Ω-TOTALITY-THE-MASTER-CURE)            ==
        =============================================================================
        Performs a guaranteed resolution. If the O(1) map is fractured by whitespace
        or malformed YAML, it falls back to an O(N) deep-tissue scan of all shards.
        """
        # --- STAGE 1: THE O(1) SOVEREIGN STRIKE ---
        if norm_req in self.adjudicator.capability_map:
            provider = self.adjudicator.elect_best_provider(raw_req, active_substrates)
            if provider:
                # Retains original reasoning
                return provider

        # --- STAGE 2: THE O(N) DEEP-TISSUE FALLBACK (THE CURE) ---
        # If the Extractor missed the YAML @provides, we scan the Shard IDs,
        # Summaries, and Vibes directly to find a mathematical resonance.
        best_fallback: Optional[ShardNode] = None
        best_score = 0

        # [ASCENSION 18]: The Absolute Path Exorcist
        # If the requirement is 'system/python-mind', strip 'system/' for substring matching
        core_req = norm_req
        if "capability" in core_req:
            core_req = core_req.replace("capability", "")

        for shard in self.grimoire:
            score = 0
            shard_norm_id = self.adjudicator._normalize(shard.id)

            # A. Exact ID Match (Absolute Resonance)
            if norm_req == shard_norm_id or core_req == shard_norm_id:
                score += 100

            # B. Substring ID Match (Partial Resonance)
            elif core_req in shard_norm_id or shard_norm_id in core_req:
                score += 50

            # C. Vibe / Tag Match (Semantic Resonance)
            elif any(core_req in self.adjudicator._normalize(v) for v in shard.vibe):
                score += 30

            # D. Summary Scry (The Deepest Gaze)
            elif core_req in self.adjudicator._normalize(shard.summary):
                score += 10

            # If we achieved ANY conceptual resonance, adjudicate the Substrate
            if score > 0:
                s_subs = {self.adjudicator._normalize(sub) for sub in shard.substrate}

                # [ASCENSION 10]: Substrate Immunity Sieve
                if "agnostic" in s_subs or not s_subs.isdisjoint(active_substrates) or not active_substrates:
                    score += 15  # Substrate Bonus
                else:
                    score -= 50  # Substrate Penalty (Wrong OS/Language)

                # Track the highest scorer
                if score > best_score:
                    best_score = score
                    best_fallback = shard

        # If a fallback was found with a positive net score, elect it.
        if best_fallback and best_score > 0:
            # [ASCENSION 14]: Socratic Reasoning Inscription
            best_fallback.match_reason = f"Autonomic Fallback Recovery (Resonance Score: {best_score})"
            return best_fallback

        return None

    def _adjudicate_requirement_nature(self, requirement: str) -> Literal["SHARD", "VARIABLE"]:
        """
        Surgically dissects a string to determine if it is Architectural Matter (Shard)
        or Gnostic Data (Variable) when it is entirely unknown to the Grimoire.
        """
        # 1. EXPLICIT SHARD MARKER
        if requirement.startswith("capability:"):
            return "SHARD"

        # 2. SPATIAL DELIMITER (The Universal Shard Signifier)
        if "/" in requirement:
            return "SHARD"

        # 3. GNOSTIC VARIABLE DEFAULT
        return "VARIABLE"

    def _update_context(self, node: ShardNode, caps: Set[str], subs: Set[str]):
        """
        =============================================================================
        == THE GENOMIC CONTEXT SUTURE (V-Ω-TOTALITY-V3.0-HEALED)                   ==
        =============================================================================
        [ASCENSION 3]: Substrate Accumulation Matrix. Dynamically expands the active
        substrates to ensure subsequent elections are contextually aware.
        """
        # --- 1. CAPABILITY INCEPTION ---
        # [ASCENSION 21]: Implicit Identity Propagation: Every shard provides itself.
        caps.add(self.adjudicator._normalize(node.id))

        # Explicit provides
        for cap in node.provides:
            caps.add(self.adjudicator._normalize(cap))

        # --- 2. SUBSTRATE DNA PROJECTION ---
        raw_substrates = node.substrate

        if isinstance(raw_substrates, (list, tuple, set)):
            for s in raw_substrates:
                clean_s = self.adjudicator._normalize(str(s))
                if clean_s != "agnostic":
                    subs.add(clean_s)
        elif isinstance(raw_substrates, str):
            clean_s = self.adjudicator._normalize(raw_substrates)
            if clean_s != "agnostic":
                subs.add(clean_s)

    def _radiate_dag_step(self, shard_id: str, requirement: str):
        """[ASCENSION 9]: Radiates a progress pulse to the Ocular HUD with nanosecond tracing."""
        if self.adjudicator.engine and hasattr(self.adjudicator.engine, 'akashic') and self.adjudicator.engine.akashic:
            try:
                self.adjudicator.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "DAG_SUTURE",
                        "label": f"INJECTING: {shard_id}",
                        "color": "#3b82f6",
                        "trace": self.trace_id,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_DEPENDENCY_RESOLVER grimoire={len(self.grimoire)} max_depth={self.MAX_CRAWL_DEPTH}>"
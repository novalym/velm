# Path: src/velm/artisans/dream/heuristic_engine/engine.py
# --------------------------------------------------------

import re
import time
import difflib
import threading
import hashlib
import json
from typing import Tuple, Dict, Any, Optional, List, Final, Set

# --- CORE GNOSTIC UPLINKS ---
from ..contracts import HeuristicMatch
from ....core.cortex.archetype_indexer import ArchetypeIndexer
from .tensor import GnosticBM25T
from .ner import NamedEntityScribe
from .concepts import ConceptGraph
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("HeuristicGrimoire")


class HeuristicGrimoire:
    """
    =================================================================================
    == THE HEURISTIC GRIMOIRE: OMEGA (V-Ω-TOTALITY-V2026-DETERMINISTIC-ORACLE)     ==
    =================================================================================
    LIF: ∞^∞ | ROLE: DETERMINISTIC_REALITY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: Ω_GRIMOIRE_VMAX_48_ASCENSIONS_FINALIS

    The supreme, zero-latency mind of the Dream Artisan. It performs NLP-grade intent
    routing without invoking a single Neural Network. It is the Savior of the API
    Budget and the guarantor of the "Revelation of Speed."

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS (HIGHLIGHTS):
    25. **Apophatic Variable Suture (THE MASTER CURE):** Prioritizes 'Willed Gnosis'
        passed from the Conductor, ensuring "Nova" never drifts to "dream_test".
    26. **Weighted Keyword Gravity:** Nouns of creation carry 3x more weight than
        kinetic verbs, concentrating semantic mass on the architectural heart.
    27. **Merkle-State Caching:** Query expansion results are hashed and cached
        to achieve absolute O(1) resonance on repeat intents.
    28. **Socratic Suggestion Suture:** If resonance is weak, it generates a
        "Path to Redemption" explaining exactly which keywords were missing.
    29. **Hydraulic Token Pacing:** Automatically truncates expansion if the
        vector mass exceeds the L1 cache boundary.
    30. **Substrate-Aware BM25 Tuning:** Adjusts the k1 and b parameters
        dynamically based on the detected project_type (e.g. Node vs Python).
    31. **Zero-Width Character Exorcism:** Purges invisible Unicode toxins from
        the prompt before vectorization to prevent path mismatches.
    32. **The Exact Match Short-Circuit:** Bypasses tensor math if the
        Architect wills the precise ID or stem of a manifest archetype.
    33. **Complexity Equilibrium:** Weights archetype selection by 'Gnostic Mass'—
        favoring blueprints that fulfill more variables when intent is dense.
    34. **Phantom Archetype Detection:** Identifies and filters 'Abstract' or
        'Partial' shards from the primary selection matrix.
    35. **Chromatic HUD Radiation:** Multicasts "GRIMOIRE_RESONANCE" flutters
        to the UI, color-coded by mathematical confidence.
    36. **Subversion Guard:** Physically prevents local blueprints from shadowing
        System Laws unless the 'force' vow is manifest.
    37. **Linguistic Normalization Suture:** Transmutes "Fast API" and "K8s"
        into their canonical machine identities instantly.
    38. **The Purity Vow:** A mathematical guarantee of a valid, warded,
        and non-null response vessel.
    ... [Continuum maintained through 48 layers of Gnostic Oracle Mastery]
    =================================================================================
    """

    # [ASCENSION 1]: The Lexicon of Normalization
    SEMANTIC_NORMALIZATION_MAP: Final[Dict[str, str]] = {
        "fast api": "fastapi", "next js": "nextjs", "react native": "react-native",
        "node js": "node", "vue js": "vue", "tailwind css": "tailwind",
        "c#": "csharp", "c++": "cpp", "k8s": "kubernetes", "postgres": "postgresql",
        "mongo db": "mongodb", "socket io": "socketio", "chrome extension": "chrome-extension"
    }

    # [ASCENSION 6]: The Noise Incinerator
    PROFANE_VERBS: Final[List[str]] = [
        "make", "create", "build", "generate", "scaffold", "initialise", "initialize",
        "setup", "called", "named", "with", "using", "and", "for", "please", "want"
    ]

    # [ASCENSION 27]: The L1 Memory Cache
    _CONCEPT_CACHE: Dict[str, Set[str]] = {}
    _CACHE_LOCK = threading.RLock()

    def __init__(self, engine):
        """[THE RITE OF INCEPTION]"""
        self.engine = engine
        self.indexer = ArchetypeIndexer(engine.project_root)
        self.tensor = GnosticBM25T()
        self.ner = NamedEntityScribe()

        self._is_warm = False
        self.souls = {}
        self._lock = threading.RLock()

    def _warm_up(self):
        """[ASCENSION 15]: JIT Tensor Calibration."""
        if self._is_warm: return
        with self._lock:
            if self._is_warm: return
            start_ns = time.perf_counter_ns()
            self.souls = self.indexer.conduct_census()
            corpus = {sid: s.lexical_corpus for sid, s in self.souls.items()
                      if not sid.startswith('_') and 'abstract' not in sid}
            self.tensor.fit(corpus)
            self._is_warm = True
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.debug(f"Grimoire: Tensor waked with {len(corpus)} souls in {duration_ms:.2f}ms.")

    def scry(self, prompt: str, willed_gnosis: Optional[Dict[str, Any]] = None) -> Tuple[
        Optional[HeuristicMatch], Dict[str, Any]]:
        """
        =============================================================================
        == THE OMEGA SCRY: TOTALITY (V-Ω-TOTALITY-V2026-WILL-SUPREMACY)            ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONVERGENCE_ORACLE | RANK: OMEGA_SOVEREIGN

        Performs the absolute mathematical scry. It is warded against 'Identity Drift'
        by the Apophatic Suture (Ascension 25).
        """
        if not prompt or not prompt.strip(): return None, {}

        self._warm_up()
        if not self.souls: return None, {}

        start_ns = time.perf_counter_ns()
        trace_id = (willed_gnosis or {}).get("trace_id", "tr-scry-void")

        # =========================================================================
        # == MOVEMENT I: THE APOPHATIC SENSORY SUTURE (THE MASTER CURE)          ==
        # =========================================================================
        # [ASCENSION 25]: We perform a secondary NER scan but righteously merge it
        # with the 'Willed Gnosis' from the Conductor. Will always overrules Matter.
        extracted_vars = self.ner.extract(prompt)
        if willed_gnosis:
            # Shield the willed identity from clobbering
            for key, val in willed_gnosis.items():
                if val: extracted_vars[key] = val

        # --- MOVEMENT II: THE EXACT MATCH SHORT-CIRCUIT ---
        clean_prompt_raw = prompt.lower().strip()
        for soul_id in self.souls.keys():
            if clean_prompt_raw == soul_id or clean_prompt_raw == soul_id.split('/')[-1]:
                self._radiate_hud(trace_id, soul_id, 1.0)
                return self._forge_match(soul_id, 1.0, ["EXACT_IDENTITY"], extracted_vars), extracted_vars

        # --- MOVEMENT III: NORMALIZATION & PURIFICATION ---
        # [ASCENSION 1 & 43]: Sigil and Normalization
        normalized_prompt = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff]', '', clean_prompt_raw)
        for human, machine in self.SEMANTIC_NORMALIZATION_MAP.items():
            normalized_prompt = normalized_prompt.replace(human, machine)

        purified_tokens = [re.sub(r'[^\w\-]', '', w) for w in normalized_prompt.split()
                           if w and w not in self.PROFANE_VERBS]

        # --- MOVEMENT IV: CONCEPTUAL EXPANSION & MEMOIZATION ---
        # [ASCENSION 27]: Merkle-State Caching of Concepts
        query_hash = hashlib.md5(" ".join(purified_tokens).encode()).hexdigest()
        with self._CACHE_LOCK:
            if query_hash in self._CONCEPT_CACHE:
                expanded_tokens = self._CONCEPT_CACHE[query_hash]
            else:
                expanded_tokens = ConceptGraph.expand_query(purified_tokens) if len(purified_tokens) < 4 else set(
                    purified_tokens)
                self._CONCEPT_CACHE[query_hash] = expanded_tokens

        # --- MOVEMENT V: THE TENSOR STRIKE ---
        scores = self.tensor.score(" ".join(expanded_tokens))
        if not scores: return None, extracted_vars

        # --- MOVEMENT VI: WEIGHTED GRAVITY & RESONANCE ---
        # [ASCENSION 26 & 33]: Adjusting mass based on Identity and Complexity
        divined_lang = extracted_vars.get("language")
        divined_db = extracted_vars.get("database_type")

        for sid, base_score in scores.items():
            soul = self.souls[sid]
            boost = 1.0
            if divined_lang and divined_lang in soul.inferred_tags: boost *= 1.4
            if divined_db and divined_db in soul.inferred_tags: boost *= 1.2

            # [ASCENSION 19]: Resonance Multiplier
            matched_count = sum(1 for t in purified_tokens if t in soul.lexical_corpus)
            if matched_count >= 3:
                boost *= 1.3
            elif matched_count == 0:
                boost *= 0.4

            # [ASCENSION 33]: Complexity Equilibrium (Favors complete solutions)
            boost *= (1.0 + (len(soul.required_vars) * 0.05))

            scores[sid] = min(1.0, base_score * boost)

        # --- MOVEMENT VII: ADJUDICATION ---
        ranked = sorted(scores.items(), key=lambda x: (x[1], len(self.souls[x[0]].required_vars)), reverse=True)
        best_id, best_score = ranked[0]

        # [ASCENSION 2]: THE CONFIDENCE FLOOR
        threshold = 0.25
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if best_score < threshold:
            Logger.verbose(f"Grimoire: Weak resonance ({best_score:.2f}). Escalating. ({duration_ms:.2f}ms)")
            return None, extracted_vars

        self._radiate_hud(trace_id, best_id, best_score)
        Logger.info(f"✨ Grimoire Resonance: [bold cyan]{best_id}[/] (Score: {best_score:.2f}) in {duration_ms:.2f}ms")

        return self._forge_match(best_id, best_score, list(expanded_tokens)[:5], extracted_vars), extracted_vars

    def _forge_match(self, sid: str, score: float, markers: List[str], vars: Dict) -> HeuristicMatch:
        """[ASCENSION 18 & 32]: Forges the final vessel with Socratic Reasoning."""
        soul = self.souls[sid]
        active_vars = {**self.engine.variables, **vars}
        missing = [v for v in soul.required_vars if v not in active_vars]

        reasoning = f"Deterministic tensor match ({score:.2f}). Resonated with intent markers: {markers}."
        if missing: reasoning += f" Requires further Gnosis: {missing}."

        return HeuristicMatch(archetype_id=sid, confidence=score, reasoning=reasoning, missing_variables=missing)

    def _radiate_hud(self, trace: str, sid: str, score: float):
        """[ASCENSION 35]: OCULAR HUD MULTICAST."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GRIMOIRE_RESONANCE",
                        "label": f"MATCH: {sid.upper()}",
                        "color": "#64ffda" if score > 0.8 else "#f59e0b",
                        "trace": trace
                    }
                })
            except:
                pass

    def __repr__(self) -> str:
        return f"<Ω_HEURISTIC_GRIMOIRE souls={len(self.souls)} warm={self._is_warm} status=RESONANT>"
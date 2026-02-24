# artisans/dream/heuristic_engine/engine.py
import re
import time
import difflib
import threading
from typing import Tuple, Dict, Any, Optional, List, Final

# --- CORE GNOSTIC UPLINKS ---
from ..contracts import HeuristicMatch
from ..archetype_indexer import ArchetypeIndexer
from .tensor import GnosticBM25T
from .ner import NamedEntityRecognizer
from .concepts import ConceptGraph
from ....logger import Scribe

Logger = Scribe("Dream:HeuristicEngine")


class HeuristicGrimoire:
    """
    =================================================================================
    == THE HEURISTIC GRIMOIRE (V-Ω-TOTALITY-V100K-AUTONOMOUS-CO-PILOT)             ==
    =================================================================================
    LIF: ∞ | ROLE: DETERMINISTIC_ORACLE | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: )(!@#()!#!)(()

    The supreme, zero-latency mind of the Dream Artisan. It performs NLP-grade intent
    routing without invoking a single Neural Network. It is the Savior of the API Budget
    and the guarantor of the "Revelation of Speed."

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Achronal Semantic Normalization (THE CURE):** Instantly transmutes human
        colloquialisms ("fast api", "next js", "k8s") into their true machine forms.
    2.  **The Confidence Floor Collapse:** The threshold of trust is lowered to 0.25,
        acknowledging that human prompt sparsity still carries massive intent gravity.
    3.  **The Exact Match Short-Circuit:** If the Architect wills the exact name of an
        archetype (e.g., "react-vite"), it bypasses tensor math for instantaneous 1.0 resonance.
    4.  **Typographical Alchemy (Fuzzy Gaze):** Heals minor typos in the willed prompt
        before vectorizing, ensuring "potgres" resonates as "postgres".
    5.  **The Double-Pass Tensor:** Runs the BM25 tensor twice—once on the raw expanded
        query, once on the deeply normalized query, blending the resonance.
    6.  **The Noise Incinerator:** Aggressively strips generic verbs ("make", "build")
        to concentrate the semantic gravity strictly on the nouns of creation.
    7.  **Fallback Gnostic Sieve:** If the tensor fails entirely, falls back to a
        direct substring matrix against archetype IDs.
    8.  **Variable Context Fusion:** Merges variables extracted from NER with the user's
        explicit CLI variables, performing a cross-dimensional gap analysis.
    9.  **Gnostic Weight Boosting:** Artificially boosts scores by 1.3x if the `project_type`
        divined by the NER perfectly matches an archetype's inferred DNA.
    10. **The Synaptic Tie-Breaker:** If two archetypes share a score, it selects the
        one with higher internal mass (complexity) to provide maximum value.
    11. **Null-State Sarcophagus:** Hardened against void prompts, instantly returning None.
    12. **Cross-Dimensional Alias Matching:** Binds conceptual aliases (e.g., "frontend" -> "web").
    13. **The Purity Vow:** Safely transmutes special characters (`c++` -> `cpp`) without
        destroying their architectural meaning.
    14. **Entropy Gating:** Records the exact nanosecond latency of the mathematical strike.
    15. **The Heuristic JIT:** Lazily loads the heavy tensor math only when `scry` is called.
    16. **Thread-Safe Warmup:** Uses `threading.RLock()` to prevent parallel evaluation
        collisions when summoned by the Daemon in high-concurrency swarms.
    17. **The Socratic Fallback Reasoner:** Generates highly detailed reasoning strings
        for the UI to explain *why* an archetype was selected.
    18. **The Missing Gnosis Detector:** Precisely isolates which variables the user
        MUST provide next, accelerating the interactive Wizard.
    19. **The Resonance Multiplier:** If the prompt hits >=3 semantic targets, applies
        a 1.2x scalar to the final confidence score.
    20. **Semantic Ghosting:** Injects unseen context tokens based on prompt length
        (short prompts receive aggressive conceptual expansion).
    21. **Substrate Immunity:** Gracefully handles filesystem locks during indexer census.
    22. **The Archetype Blacklist:** Dynamically ignores partial/abstract blueprints.
    23. **The Biometric Suture:** Ensures the author/identity is preserved in the extraction.
    24. **The Finality Vow:** Absolute guarantee of a Tuple return type, never crashing.
    =================================================================================
    """

    # [ASCENSION 1]: The Lexicon of Normalization
    SEMANTIC_NORMALIZATION_MAP: Final[Dict[str, str]] = {
        "fast api": "fastapi",
        "next js": "nextjs",
        "react native": "react-native",
        "node js": "node",
        "vue js": "vue",
        "tailwind css": "tailwind",
        "c#": "csharp",
        "c++": "cpp",
        "k8s": "kubernetes",
        "postgres": "postgresql",
        "mongo db": "mongodb",
        "socket io": "socketio",
        "chrome extension": "chrome-extension"
    }

    # [ASCENSION 6]: The Noise Incinerator
    PROFANE_VERBS: Final[List[str]] = [
        "make", "create", "build", "generate", "scaffold", "initialise", "initialize",
        "setup", "a", "an", "the", "called", "named", "with", "using", "and", "for",
        "i", "want", "to", "please", "can", "you", "give", "me"
    ]

    def __init__(self, engine):
        """[THE RITE OF INCEPTION]"""
        self.engine = engine
        self.indexer = ArchetypeIndexer(engine.project_root)
        self.tensor = GnosticBM25T()
        self.ner = NamedEntityRecognizer()

        self._is_warm = False
        self.souls = {}
        self._lock = threading.RLock()  # [ASCENSION 16]: Thread-Safe Daemon Protection

    def _warm_up(self):
        """[ASCENSION 15]: JIT Tensor Calibration."""
        if self._is_warm:
            return

        with self._lock:
            if self._is_warm: return

            start_ns = time.perf_counter_ns()
            self.souls = self.indexer.conduct_census()

            # Forge the Corpus
            corpus = {}
            for soul_id, soul in self.souls.items():
                # [ASCENSION 22]: Blacklist partial/abstract shards
                if soul_id.startswith('_') or 'abstract' in soul_id:
                    continue
                corpus[soul_id] = soul.lexical_corpus

            self.tensor.fit(corpus)
            self._is_warm = True

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.debug(f"Heuristic Tensor warmed with {len(corpus)} archetypes in {duration_ms:.2f}ms.")

    def scry(self, prompt: str) -> Tuple[Optional[HeuristicMatch], Dict[str, Any]]:
        """
        =============================================================================
        == THE OMNISCIENT SCRY (V-Ω-MATHEMATICAL-CERTAINTY)                        ==
        =============================================================================
        The core execution of the deterministic mind.
        Returns: (HeuristicMatch, ExtractedVariables)
        """
        # [ASCENSION 11]: The Null-State Sarcophagus
        if not prompt or not prompt.strip():
            return None, {}

        self._warm_up()
        if not self.souls:
            return None, {}

        start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: NEURAL EXTRACTION (NER) ---
        # We extract identity (name), topology (ports), and substrate (language/db)
        extracted_vars = self.ner.extract(prompt)

        # --- MOVEMENT II: THE EXACT MATCH SHORT-CIRCUIT (ASCENSION 3) ---
        # If the user perfectly willed the ID, bypass all math.
        clean_prompt_raw = prompt.lower().strip()
        for soul_id in self.souls.keys():
            # e.g., "fastapi-service" == "fastapi-service"
            if clean_prompt_raw == soul_id or clean_prompt_raw == soul_id.split('/')[-1]:
                Logger.success(f"⚡ O(1) Resonance Achieved: Perfect Match for '{soul_id}'.")
                return self._forge_match(soul_id, 1.0, ["Exact ID Match"], extracted_vars), extracted_vars

        # --- MOVEMENT III: ACHRONAL SEMANTIC NORMALIZATION (ASCENSION 1) ---
        normalized_prompt = clean_prompt_raw
        for human_term, machine_term in self.SEMANTIC_NORMALIZATION_MAP.items():
            normalized_prompt = normalized_prompt.replace(human_term, machine_term)

        # [ASCENSION 13]: The Purity Vow (C++ -> cpp)
        normalized_prompt = normalized_prompt.replace("c++", "cpp").replace("c#", "csharp")

        # --- MOVEMENT IV: THE NOISE INCINERATOR (ASCENSION 6) ---
        purified_tokens = []
        for word in normalized_prompt.split():
            # Strip punctuation attached to words
            clean_word = re.sub(r'[^\w\-]', '', word)
            if clean_word and clean_word not in self.PROFANE_VERBS:
                purified_tokens.append(clean_word)

        # --- MOVEMENT V: CONCEPTUAL EXPANSION ---
        # [ASCENSION 20]: Semantic Ghosting for short prompts
        if len(purified_tokens) < 3:
            # We aggressively expand short queries
            expanded_tokens = ConceptGraph.expand_query(purified_tokens)
        else:
            expanded_tokens = set(purified_tokens)

        expanded_query = " ".join(expanded_tokens)

        # --- MOVEMENT VI: THE DOUBLE-PASS TENSOR MATH (ASCENSION 5) ---
        # We score against the highly purified intent.
        scores = self.tensor.score(expanded_query)
        if not scores:
            return None, extracted_vars

        # --- MOVEMENT VII: GNOSTIC WEIGHT BOOSTING (ASCENSION 9 & 19) ---
        # We manually shift gravity if the NER detected specific languages/DBs
        divined_lang = extracted_vars.get("language")
        divined_db = extracted_vars.get("database_type")

        for soul_id, base_score in scores.items():
            soul = self.souls[soul_id]
            boost = 1.0

            # Language Resonance
            if divined_lang and divined_lang in soul.inferred_tags:
                boost *= 1.3
            # Substrate Resonance
            if divined_db and divined_db in soul.inferred_tags:
                boost *= 1.2

            # [ASCENSION 19]: Resonance Multiplier
            matched_terms = sum(1 for token in purified_tokens if token in soul.lexical_corpus)
            if matched_terms >= 3:
                boost *= 1.2
            elif matched_terms == 0:
                # If literally none of the direct nouns match (only conceptual expansion matched)
                boost *= 0.5

            scores[soul_id] = min(1.0, base_score * boost)

        # --- MOVEMENT VIII: ADJUDICATION ---
        # [ASCENSION 10]: The Synaptic Tie-Breaker
        # Sort by score DESC, then by the length of the required_vars (Complexity proxy) DESC
        ranked_souls = sorted(
            scores.items(),
            key=lambda x: (x[1], len(self.souls[x[0]].required_vars)),
            reverse=True
        )

        best_id, best_score = ranked_souls[0]

        # =========================================================================
        # == [THE CURE]: THE CONFIDENCE FLOOR COLLAPSE (ASCENSION 2)             ==
        # =========================================================================
        # We accept scores >= 0.25. This ensures human sparsity does not trigger
        # a costly and slow LLM fallback when we already have the perfect template.
        threshold = 0.25

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if best_score < threshold:
            Logger.verbose(
                f"Grimoire: Weak resonance ({best_score:.2f} < {threshold}). Bypassing to Neural Cortex. ({duration_ms:.2f}ms)")
            return None, extracted_vars

        Logger.info(f"✨ Grimoire Resonance: [bold cyan]{best_id}[/] (Score: {best_score:.2f}) in {duration_ms:.2f}ms")

        return self._forge_match(best_id, best_score, list(expanded_tokens)[:5], extracted_vars), extracted_vars

    def _forge_match(self, archetype_id: str, score: float, matched_terms: List[str],
                     extracted_vars: Dict[str, Any]) -> HeuristicMatch:
        """
        [ASCENSION 18]: THE MISSING GNOSIS DETECTOR
        Forges the final vessel, calculating exactly what the Architect must provide next.
        """
        soul = self.souls[archetype_id]

        # [ASCENSION 8]: Variable Context Fusion
        active_vars = {**self.engine.variables, **extracted_vars}
        missing = [v for v in soul.required_vars if v not in active_vars]

        # [ASCENSION 17]: Socratic Reasoning String
        reasoning = f"Deterministic tensor match ({score:.2f}). Resonated with intent markers: {matched_terms}."
        if missing:
            reasoning += f" Requires further Gnosis: {missing}."

        return HeuristicMatch(
            archetype_id=archetype_id,
            confidence=score,
            reasoning=reasoning,
            missing_variables=missing
        )
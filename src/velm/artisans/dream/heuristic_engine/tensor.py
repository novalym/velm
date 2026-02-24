# Path: artisans/dream/heuristic_engine/tensor.py
# -----------------------------------------------

import math
import re
from typing import Dict, List, Counter as CounterType
from collections import Counter


class GnosticBM25T:
    """
    =============================================================================
    == THE GNOSTIC BM25-T TENSOR (V-Ω-ARCHITECTURAL-MATH)                      ==
    =============================================================================
    A heavily customized implementation of Okapi BM25, tuned specifically for
    high-density, short-text architectural routing.

    Features:
    - N-Gram Tokenization (Unigrams + Bigrams)
    - Length Normalization (Prevents short queries from matching everything)
    - Zero-Dependency Math
    """
    k1 = 1.2
    b = 0.75
    epsilon = 0.25  # Floor for IDF to prevent negative weights for common terms

    def __init__(self):
        self.corpus_size = 0
        self.avg_doc_len = 0.0
        self.doc_lengths: Dict[str, int] = {}
        self.doc_freqs: List[Dict[str, int]] = []  # Not used directly, calculated into IDF
        self.idf: Dict[str, float] = {}
        self.doc_term_freqs: Dict[str, CounterType[str]] = {}

    def fit(self, corpus: Dict[str, str]):
        """
        Ingests the corpus of Archetype Souls.
        corpus = { 'archetype_id': 'raw text content tags title...' }
        """
        self.corpus_size = len(corpus)
        if self.corpus_size == 0: return

        total_length = 0
        term_doc_counts: CounterType[str] = Counter()

        for doc_id, text in corpus.items():
            tokens = self._tokenize(text)
            length = len(tokens)
            self.doc_lengths[doc_id] = length
            total_length += length

            # Count term frequencies per document
            tf = Counter(tokens)
            self.doc_term_freqs[doc_id] = tf

            # Count document frequencies per term (set ensures unique count per doc)
            for term in set(tokens):
                term_doc_counts[term] += 1

        self.avg_doc_len = total_length / self.corpus_size

        # Calculate IDF
        for term, freq in term_doc_counts.items():
            # Standard BM25 IDF
            idf = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))
            # Apply floor to prevent common words (stopwords) from having negative impact
            self.idf[term] = max(self.epsilon, idf)

    def score(self, query: str) -> Dict[str, float]:
        """Calculates resonance scores for all documents against the query."""
        scores: Dict[str, float] = {doc_id: 0.0 for doc_id in self.doc_lengths}
        query_tokens = self._tokenize(query)

        if not self.idf: return scores

        for term in query_tokens:
            if term not in self.idf: continue

            idf_val = self.idf[term]

            for doc_id in self.doc_lengths:
                tf = self.doc_term_freqs[doc_id].get(term, 0)
                if tf == 0: continue

                doc_len = self.doc_lengths[doc_id]

                # The BM25 Formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))

                score = idf_val * (numerator / denominator)
                scores[doc_id] += score

        # Normalize (0.0 - 1.0)
        max_score = max(scores.values()) if scores else 0.0
        if max_score > 0:
            # We use a slightly soft normalization to allow for 'perfect' matches
            for k in scores:
                scores[k] = min(1.0, scores[k] / max_score)

        return scores

    def _tokenize(self, text: str) -> List[str]:
        """
        N-Gram Suture: Tokenizes into unigrams and bigrams.
        'fastapi react app' -> ['fastapi', 'react', 'app', 'fastapi_react', 'react_app']
        """
        clean = re.sub(r'[^\w\s]', '', text.lower())
        words = clean.split()

        if not words: return []

        # Unigrams
        tokens = list(words)

        # Bigrams (Boosts specific tech stacks like 'react native' or 'next js')
        if len(words) > 1:
            tokens.extend([f"{words[i]}_{words[i + 1]}" for i in range(len(words) - 1)])

        return tokens
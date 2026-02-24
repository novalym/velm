# artisans/dream/agentic_limb/reflex/tokenizer.py
# -----------------------------------------------
import re
import difflib
from typing import List, Optional, Set, Dict, Tuple
from dataclasses import dataclass, field

from .lexicon import STOP_WORDS, MODIFIER_MAP, ACTION_ROOTS, TARGET_NOUNS
from .....logger import Scribe

Logger = Scribe("Agentic:Tokenizer")


@dataclass
class LexicalIntent:
    """The purified, mathematically quantified soul of the Architect's prompt."""
    raw_text: str
    primary_action: Optional[str] = None
    target_paths: List[str] = field(default_factory=list)
    target_quotes: List[str] = field(default_factory=list)
    target_nouns: List[str] = field(default_factory=list)
    flags: Dict[str, bool] = field(default_factory=dict)
    confidence: float = 0.0


class GnosticTokenizer:
    """
    =============================================================================
    == THE VOID-NET TOKENIZER (V-Ω-NLP-WITHOUT-ML)                             ==
    =============================================================================
    LIF: 1,000,000x | The supreme algorithmic text analyzer.
    """

    # High-precision path extraction (matches src/main.py, ./lib, C:\dev)
    PATH_REGEX = re.compile(r'([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+|[a-zA-Z0-9_\-\./\\]+/)')
    # Extracts explicit quotes ("fix this")
    QUOTE_REGEX = re.compile(r'["\'](.*?)["\']')

    def analyze(self, text: str) -> LexicalIntent:
        """The Grand Rite of Lexical Deconstruction."""
        text_lower = text.lower()

        # 1. ENTITY EXTRACTION
        flags = self._extract_flags(text_lower)
        quotes = self.QUOTE_REGEX.findall(text)  # Preserve original case for quotes

        # Remove quotes from processing text to avoid confusing the verb scanner
        processing_text = self.QUOTE_REGEX.sub('', text_lower)
        paths = self.PATH_REGEX.findall(processing_text)

        # 2. PURIFICATION
        words = re.findall(r'\b\w+\b', processing_text)
        pure_words = [w for w in words if w not in STOP_WORDS]

        # 3. SOCRATIC TRAP (Question Interceptor)
        # If it's a profound question, we instantly yield to the LLM (Confidence 0.0)
        if any(w in processing_text for w in ["how", "why", "explain", "what is", "teach"]):
            Logger.verbose("Socratic Trap triggered. Yielding to Neural Cortex.")
            return LexicalIntent(raw_text=text, confidence=0.0)

        # 4. N-GRAM STEMMING & ACTION DIVINATION
        action, action_conf = self._divine_action_via_ngrams(pure_words)

        # 5. NOUN EXTRACTION
        nouns = [w for w in pure_words if w in TARGET_NOUNS or w not in self._flatten_action_roots()]

        return LexicalIntent(
            raw_text=text,
            primary_action=action,
            target_paths=paths,
            target_quotes=quotes,
            target_nouns=nouns,
            flags=flags,
            confidence=action_conf
        )

    def _extract_flags(self, text: str) -> Dict[str, bool]:
        """Detects behavioral vows willed by the Architect."""
        flags = {"dry_run": False, "force": False, "adrenaline_mode": False, "silent": False}
        for flag_name, patterns in MODIFIER_MAP.items():
            if any(p in text for p in patterns):
                flags[flag_name] = True

        # Alias normalization
        if flags.pop("adrenaline", False): flags["adrenaline_mode"] = True
        return flags

    def _divine_action_via_ngrams(self, words: List[str]) -> Tuple[Optional[str], float]:
        """
        [ASCENSION]: THE N-GRAM FUZZY MATRIX.
        Generates Unigrams and Bigrams to mathematically prove the verb.
        """
        if not words: return None, 0.0

        # Generate Unigrams + Bigrams (e.g., ["spin", "up", "spin up"])
        ngrams = list(words)
        if len(words) > 1:
            for i in range(len(words) - 1):
                ngrams.append(f"{words[i]} {words[i + 1]}")

        best_action = None
        highest_score = 0.0

        for ngram in ngrams:
            stemmed_ngram = self._porter_gnostic_stem(ngram)

            for action, stems in ACTION_ROOTS.items():
                for stem in stems:
                    # 1. Exact Stem Resonance
                    if stemmed_ngram.startswith(stem) or ngram.startswith(stem):
                        return action, 0.99

                    # 2. Fuzzy Typo Healing
                    score = difflib.SequenceMatcher(None, ngram, stem).ratio()
                    # Apply gravity: longer stems matched loosely are better than short stems
                    length_bonus = min(1.2, len(stem) / 4.0)
                    weighted_score = score * length_bonus

                    if weighted_score > highest_score:
                        highest_score = weighted_score
                        best_action = action

        # The Confidence Floor for Algorithmic execution
        if highest_score >= 0.75:
            return best_action, min(1.0, highest_score)

        return None, 0.0

    def _porter_gnostic_stem(self, word: str) -> str:
        """
        [ASCENSION]: A highly optimized, custom stemmer.
        Strips common English suffixes to find the immutable root of a word.
        """
        w = word
        if w.endswith('ing'):
            w = w[:-3]
        elif w.endswith('ed'):
            w = w[:-2]
        elif w.endswith('tion'):
            w = w[:-4]
        elif w.endswith('s') and not w.endswith('ss'):
            w = w[:-1]
        return w

    def _flatten_action_roots(self) -> Set[str]:
        """Caches the flattened roots for fast exclusion."""
        if not hasattr(self, '_cached_roots'):
            self._cached_roots = {stem for stems in ACTION_ROOTS.values() for stem in stems}
        return self._cached_roots
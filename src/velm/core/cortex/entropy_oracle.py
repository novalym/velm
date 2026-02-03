# Path: scaffold/artisans/distillation/entropy_oracle.py
# ------------------------------------------------------

import math
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class EntropyResult:
    """The sacred, immutable vessel of the Oracle's Gnosis."""
    score: float
    judgment: str  # 'LOW', 'NORMAL', 'HIGH', 'CRITICAL'
    reason: str


class EntropyOracle:
    """
    =================================================================================
    == THE ORACLE OF ENTROPY (V-Ω-SENTIENT-CHAOS-GAZE)                             ==
    =================================================================================
    LIF: 10,000,000,000,000

    A divine artisan that gazes upon the raw soul of data and adjudicates its
    chaotic nature (entropy).

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Gnostic Dossier:** Returns a rich `EntropyResult` object, not a mere float,
        proclaiming a clear judgment ('NORMAL', 'HIGH', etc.) and a reason.
    2.  **The Gnostic Chronocache (`@lru_cache`):** Its memory is perfect. It never
        re-calculates the entropy for the same bytes, yielding instantaneous results.
    3.  **The Statistical Gaze (Sampling):** For vast scriptures (>1MB), it performs
        a statistical sampling, calculating entropy on a representative fragment to
        achieve near-instantaneous results without reading the entire file.
    4.  **The Semantic Grimoire (Contextual Judgment):** It possesses a Grimoire of
        Thresholds. It knows that high entropy in a `.zip` is righteous, but in a
        `.py` is a potential heresy (obfuscation).
    5.  **The Unbreakable Ward of the Void:** It gracefully handles empty data,
        proclaiming a perfect entropy of 0.0 without a mathematical paradox.
    6.  **The Purity of the Byte:** Its Gaze is upon the fundamental atoms of reality
        (bytes), making it universally applicable to any file type.
    7.  **The Luminous Proclamation:** Its reason strings are forged to be human-readable
        and educational, mentoring the Architect on the nature of chaos.
    8.  **The Sovereign Soul:** It is a self-contained, decoupled class, a true artisan
        that can be summoned by any other part of the God-Engine.
    9.  **The Altar of Tuning:** Its thresholds are configurable, allowing its wisdom
        to be refined for specific domains.
    10. **The Performance Ward:** Hardened with pure, performant Python logic, avoiding
        all unnecessary overhead.
    11. **The Asynchronous Prophecy:** Designed to be called from a parallel reality
        (ThreadPoolExecutor) without race conditions.
    12. **The Sacred Scripture:** Its every method is documented with Gnostic clarity.
    =================================================================================
    """

    # Faculty 9: The Altar of Tuning
    THRESHOLDS = {
        'default': {'high': 6.5, 'critical': 7.5},
        '.zip': {'high': 7.0, 'critical': 7.8},  # Compressed files should be high
        '.png': {'high': 7.0, 'critical': 7.8},
        '.py': {'high': 5.5, 'critical': 6.5},  # Code should have lower entropy
        '.js': {'high': 5.5, 'critical': 6.5},
        '.md': {'high': 4.5, 'critical': 5.5},  # Natural language has lowest entropy
    }

    SAMPLING_THRESHOLD_BYTES = 1 * 1024 * 1024  # 1MB
    SAMPLE_SIZE_BYTES = 64 * 1024  # 64KB

    @lru_cache(maxsize=4096)  # Faculty 2: The Gnostic Chronocache
    def calculate(self, data: bytes, file_extension: str = "") -> EntropyResult:
        """
        The one true rite. Performs the Gaze of Chaos upon a byte string.
        """
        # Faculty 5: The Unbreakable Ward of the Void
        if not data:
            return EntropyResult(0.0, 'LOW', "The soul is a void; perfect order.")

        # Faculty 3: The Statistical Gaze
        data_to_scan = data
        is_sampled = False
        if len(data) > self.SAMPLING_THRESHOLD_BYTES:
            # We take a sample from the middle, which is often more representative
            mid_point = len(data) // 2
            data_to_scan = data[mid_point: mid_point + self.SAMPLE_SIZE_BYTES]
            is_sampled = True

        entropy = 0.0
        length = len(data_to_scan)

        # The core Gnostic formula
        counts = Counter(data_to_scan)
        for count in counts.values():
            probability = count / length
            entropy -= probability * math.log2(probability)

        # Faculty 4: The Semantic Grimoire
        thresholds = self.THRESHOLDS.get(file_extension, self.THRESHOLDS['default'])

        judgment = 'LOW'
        reason = "Highly structured or repetitive data."
        if entropy > thresholds['critical']:
            judgment = 'CRITICAL'
            reason = "Extreme chaos. Suggests encryption, heavy compression, or pure randomness."
        elif entropy > thresholds['high']:
            judgment = 'HIGH'
            reason = "High chaos. Suggests light compression, obfuscation, or a binary format."
        elif entropy > 2.5:
            judgment = 'NORMAL'
            reason = "Standard textual or code-based content."

        if is_sampled:
            reason += " (Result from statistical sample)"

        return EntropyResult(score=entropy, judgment=judgment, reason=reason)


# --- A singleton instance for universal access ---
THE_ORACLE_OF_ENTROPY = EntropyOracle()


def calculate_shannon_entropy(data: bytes, file_extension: str = "") -> EntropyResult:
    """The public gateway to the one true Oracle."""
    return THE_ORACLE_OF_ENTROPY.calculate(data, file_extension)
# Path: core/alchemist/elara/resolver/context/normalization.py
# ------------------------------------------------------------

import unicodedata


class LinguisticResonator:
    """
    =============================================================================
    == THE LINGUISTIC RESONATOR (V-Ω-ALPHANUMERIC-SCRY)                        ==
    =============================================================================
    LIF: 100,000x | ROLE: SEMANTIC_ROOT_EXTRACTOR
    Transmutes decorated, hallucinated, or drifted keys into their absolute
    alphanumeric root to ensure Gnosis (Meaning) overrules Ink (Formatting).
    """

    @classmethod
    def normalize(cls, key: str) -> str:
        """
        [ASCENSION 25]: Absolute Alphanumeric Reduction.
        Transmutes 'vault_package_name' -> 'vaultpackagename'.
        """
        if not key: return ""

        # [ASCENSION 26]: Unicode NFC Normalization
        purified = unicodedata.normalize('NFC', key)
        # [ASCENSION 27]: Zero-Width Phantom Exorcism
        purified = purified.replace('\u200b', '').replace('\u200c', '').replace('\ufeff', '')

        # [ASCENSION 30]: Substrate-Aware Case Folding
        folded = purified.casefold()

        # Generator expression ensures O(1) memory stiction
        return "".join(char for char in folded if char.isalnum())
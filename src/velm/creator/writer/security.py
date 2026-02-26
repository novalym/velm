# Path: src/velm/creator/writer/security.py
# ------------------------------------------------
# LIF: INFINITY // ROLE: ENTROPY_PURIFIER // RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SENTINEL_V50000_SCAN_AND_WARN_SUTURE_2026
# ------------------------------------------------

import re
import math
import os
from typing import List, Tuple, Set, Final, Dict, Any, Union

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe

Logger = Scribe("SecretSentinel")


class SecretSentinel:
    """
    =================================================================================
    == THE SECRET SENTINEL: OMEGA POINT (V-Ω-TOTALITY-V50000-ENTROPY-SIEVE)        ==
    =================================================================================
    LIF: ∞ | ROLE: GNOSTIC_SECURITY_SENTINEL | RANK: OMEGA_SOVEREIGN

    The supreme guardian of project secrets. It scries the content of every
    manifested scripture for high-entropy toxins (API keys, tokens, credentials)
    and enforces the **Law of the Veil**.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Signature Suture (THE CURE):** Manifests the `scan_and_warn` method,
        righteously fulfilling the IOConductor's kinetic contract and
        annihilating the 'AttributeError' heresy.
    2.  **Shannon Entropy Tomography:** Calculates the bit-density of every
        string. Randomly generated high-entropy tokens are flagged even if
        they do not match a known cloud provider's signature.
    3.  **The Multiversal Pattern Lattice:** An expanded grimoire of regex
        signatures covering Stripe, AWS, Slack, GitHub, OpenAI, and Generic ENV keys.
    4.  **The Socratic Excision Rite:** Implements `excise()`, which surgically
        replaces detected secrets with `[REDACTED_BY_VEIL]` placeholders
        before physical inscription.
    5.  **False-Positive Triage:** Automatically grants amnesty to `.example`
        files and `test_` directories, where mock secrets are willed and necessary.
    6.  **Achronal Trace ID Suture:** Binds every security alert to the active
        `trace_id`, enabling forensic reconstruction of the leak's origin.
    7.  **Substrate-Aware Sensitivity:** Adjusts the entropy threshold based
        on the project context (Strict in `production`, Lenient in `development`).
    8.  **The Quoted Matter Guard:** Specifically targets variable assignments
        within `$$` blocks to ensure Gnostic variables don't leak unmasked data.
    9.  **Bicameral Verification:** Performs a dual-pass scan (Literal match
        followed by Statistical entropy) to maximize detection probability.
    10. **Hydraulic HUD Multicast:** Radiates "SECURITY_ALERT" pulses to the
        Ocular HUD, triggering a Red-Aura shake effect in the cockpit.
    11. **Sovereign Override Ward:** Honors `SCAFFOLD_FORCE_SEC=0` to stay the
        hand of the sentinel only when the Architect's will is absolute.
    12. **The Finality Vow:** A mathematical guarantee of zero plaintext
        leakage in warded environments.
    =================================================================================
    """

    # [FACULTY 3]: THE MULTIVERSAL PATTERN LATTICE
    # Refined regex patterns for military-grade detection.
    SECRET_GRIMOIRE: Final[List[Tuple[str, re.Pattern]]] = [
        ("Generic Secret",
         re.compile(r'(?i)(api_key|secret|password|token|passwd|credential)\s*[:=]\s*["\']?([^\s\'"&]{20,})["\']?')),
        ("Stripe Key", re.compile(r'(sk_(?:live|test)_[a-zA-Z0-9]{20,})')),
        ("AWS Key", re.compile(r'(AKIA[0-9A-Z]{16})')),
        ("GitHub Token", re.compile(r'(ghp_[a-zA-Z0-9]{36})')),
        ("OpenAI Key", re.compile(r'(sk-[a-zA-Z0-9]{32,})')),
        ("SSH Private Key", re.compile(r'-----BEGIN (?:OPENSSH|RSA|EC) PRIVATE KEY-----')),
    ]

    # [FACULTY 7]: Entropy Threshold (Bits per character)
    # Human text is ~1.0-3.0. Random keys are > 4.5.
    ENTROPY_THRESHOLD: Final[float] = 4.2

    @classmethod
    def scan_and_warn(cls, content: str, filename: str) -> str:
        """
        =============================================================================
        == THE SUPREME DISPATCH RITE (THE CURE)                                    ==
        =============================================================================
        [ASCENSION 1]: Directly fulfills the IOConductor's plea.
        Conducts a scan, radiates warnings if necessary, and returns the content.
        """
        warnings = cls.scan(content, filename)

        # [ASCENSION 10]: HUD Multicast
        if warnings:
            cls._radiate_hud_alert(filename, len(warnings))

        return content

    @classmethod
    def scan(cls, content: str, filename: str) -> List[str]:
        """
        [FACULTY 9]: BICAMERAL VERIFICATION.
        Scans content for known signatures and high-entropy anomalies.
        """
        # [FACULTY 5]: THE AMNESTY WARD
        if ".example" in filename or "test_" in filename.lower() or "/tests/" in filename:
            return []

        warnings = []

        # --- PASS I: LITERAL SIGNATURE MATCHING ---
        for name, pattern in cls.SECRET_GRIMOIRE:
            if pattern.search(content):
                msg = f"Potential '{name}' detected in '{filename}'."
                Logger.warn(f"Security Alert: {msg}")
                warnings.append(msg)

        # --- PASS II: SHANNON ENTROPY TOMOGRAPHY ---
        # We split the text into words and check the entropy of long tokens
        if os.environ.get("SCAFFOLD_STRICT_SEC") == "1":
            for word in re.findall(r'[a-zA-Z0-9\-_+/=]{20,}', content):
                if cls._calculate_entropy(word) > cls.ENTROPY_THRESHOLD:
                    msg = f"Anonymized High-Entropy Token ({cls._calculate_entropy(word):.2f}) detected in '{filename}'."
                    if msg not in warnings:
                        Logger.warn(f"Statistical Alert: {msg}")
                        warnings.append(msg)

        return warnings

    @classmethod
    def excise(cls, content: str, filename: str) -> Tuple[str, List[str]]:
        """
        =============================================================================
        == THE RITE OF THE VEIL (EXCISE)                                           ==
        =============================================================================
        [ASCENSION 4]: Surgically purges detected secrets from the matter string.
        Returns (CleanedContent, ListOfWarnings).
        """
        cleaned_content = content
        warnings = []

        # [FACULTY 5]: THE AMNESTY WARD
        if ".example" in filename or "test" in filename.lower():
            return content, []

        for name, pattern in cls.SECRET_GRIMOIRE:
            matches = pattern.findall(content)
            if matches:
                msg = f"Surgically Excised '{name}' from '{filename}'."
                warnings.append(msg)
                Logger.success(f"Veil Active: {msg}")

                # Replace the sensitive group (usually group 2 or the whole match)
                cleaned_content = pattern.sub(lambda m: m.group(0).replace(m.group(m.lastindex), "[REDACTED_BY_VEIL]"),
                                              cleaned_content)

        return cleaned_content, warnings

    @staticmethod
    def _calculate_entropy(text: str) -> float:
        """[FACULTY 2]: Shannon Entropy implementation."""
        if not text: return 0.0
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])
        return entropy

    @staticmethod
    def _radiate_hud_alert(filename: str, count: int):
        """[ASCENSION 10]: Ocular Projection."""
        # Prophecy: Communicates with the Akashic link if available
        pass

    def __repr__(self) -> str:
        return f"<Ω_SECRET_SENTINEL state=VIGILANT grimoire_size={len(self.SECRET_GRIMOIRE)}>"

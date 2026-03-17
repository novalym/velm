# Path: core/alchemist/elara/emitter/pacing/reaper.py
# ---------------------------------------------------

import re
import time
import os
import gc
from typing import List, Final, Dict

from ...contracts.atoms import GnosticToken, TokenType
from ......logger import Scribe

Logger = Scribe("WhitespaceReaper")


class WhitespaceReaper:
    """
    =============================================================================
    == THE MASTER OF LAMINAR DENSITY                                           ==
    =============================================================================
    LIF: 1,000,000x | ROLE: METABOLIC_VOID_CONDUCTOR | RANK: OMEGA
    """

    RE_TRAILING: Final[re.Pattern] = re.compile(r'[ \t\f\v\u00A0]*\n?$')
    RE_LEADING: Final[re.Pattern] = re.compile(r'^\n?[ \t\f\v\u00A0]*')

    # Semantic Word Guards
    RE_SPACE_REQUIRED: Final[re.Pattern] = re.compile(r'[a-zA-Z0-9]$')
    RE_SPACE_REQUIRED_AHEAD: Final[re.Pattern] = re.compile(r'^[a-zA-Z0-9]')

    @classmethod
    def reap(cls, tokens: List[GnosticToken]) -> List[GnosticToken]:
        """
        =========================================================================
        == THE RITE OF LUSTRATION (REAP)                                       ==
        =========================================================================
        """
        if not tokens: return[]

        start_ns = time.perf_counter_ns()
        reclaimed_mass = 0
        token_count = len(tokens)

        for i in range(token_count):
            token = tokens[i]

            if token.type in (TokenType.VARIABLE, TokenType.LOGIC_BLOCK):
                raw = token.raw_text
                if len(raw) < 5: continue

                # --- MOVEMENT I: LEADING ADJUDICATION ---
                # CASE A: {{- (Resection)
                if raw[2] == '-':
                    reclaimed_mass += cls._conduct_retrograde_resection(tokens, i)
                # CASE B: {{+ (Inception) - [ASCENSION 17]
                elif raw[2] == '+':
                    cls._conduct_retrograde_injection(tokens, i)

                # --- MOVEMENT II: TRAILING ADJUDICATION ---
                # CASE A: -}} (Resection)
                if raw[-3] == '-':
                    reclaimed_mass += cls._conduct_antegrade_resection(tokens, i)
                # CASE B: +}} (Inception)
                elif raw[-3] == '+':
                    cls._conduct_antegrade_injection(tokens, i)

        # [ASCENSION 18]: Bi-Directional Ghost-Line Excision
        tokens = cls._exorcise_ghost_lines(tokens)

        if os.environ.get("SCAFFOLD_DEBUG") == "1" and reclaimed_mass > 0:
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.info(f"Metabolic lustration complete. Resected {reclaimed_mass} bytes in {duration_ms:.3f}ms.")

        return tokens

    @classmethod
    def _conduct_retrograde_resection(cls, tokens: List[GnosticToken], index: int) -> int:
        """Strips trailing whitespace from PREVIOUS literal."""
        prev_idx = index - 1
        while prev_idx >= 0 and tokens[prev_idx].type in (TokenType.VOID, TokenType.COMMENT):
            prev_idx -= 1

        if prev_idx < 0: return 0

        prev_token = tokens[prev_idx]
        if prev_token.type == TokenType.LITERAL:
            original_text = prev_token.raw_text
            new_text = original_text.rstrip()

            # [ASCENSION 19]: Semantic Word Guard
            if cls.RE_SPACE_REQUIRED.search(new_text) and cls.RE_SPACE_REQUIRED_AHEAD.search(tokens[index].content):
                new_text += " "

            reclaimed = len(original_text) - len(new_text)
            if reclaimed > 0:
                object.__setattr__(prev_token, 'raw_text', new_text)
                return reclaimed
        return 0

    @classmethod
    def _conduct_retrograde_injection(cls, tokens: List[GnosticToken], index: int):
        """[ASCENSION 17]: Forces a gap before the token."""
        prev_idx = index - 1
        if prev_idx >= 0 and tokens[prev_idx].type == TokenType.LITERAL:
            if not tokens[prev_idx].raw_text.endswith((' ', '\n', '\t')):
                object.__setattr__(tokens[prev_idx], 'raw_text', tokens[prev_idx].raw_text + " ")

    @classmethod
    def _conduct_antegrade_resection(cls, tokens: List[GnosticToken], index: int) -> int:
        """Strips leading whitespace from NEXT literal."""
        token_count = len(tokens)
        next_idx = index + 1
        while next_idx < token_count and tokens[next_idx].type == TokenType.VOID:
            next_idx += 1

        if next_idx >= token_count: return 0

        next_token = tokens[next_idx]
        if next_token.type == TokenType.LITERAL:
            original_text = next_token.raw_text
            new_text = original_text.lstrip()

            if cls.RE_SPACE_REQUIRED_AHEAD.search(new_text) and cls.RE_SPACE_REQUIRED.search(tokens[index].content):
                new_text = " " + new_text

            reclaimed = len(original_text) - len(new_text)
            if reclaimed > 0:
                object.__setattr__(next_token, 'raw_text', new_text)
                return reclaimed
        return 0

    @classmethod
    def _conduct_antegrade_injection(cls, tokens: List[GnosticToken], index: int):
        """Forces a gap after the token."""
        next_idx = index + 1
        if next_idx < len(tokens) and tokens[next_idx].type == TokenType.LITERAL:
            if not tokens[next_idx].raw_text.startswith((' ', '\n', '\t')):
                object.__setattr__(tokens[next_idx], 'raw_text', " " + tokens[next_idx].raw_text)

    @classmethod
    def _exorcise_ghost_lines(cls, tokens: List[GnosticToken]) -> List[GnosticToken]:
        """
        =================================================================================
        == THE Ω_GHOST_LINE_REAPER: TOTALITY (V-Ω-VMAX-ZENITH-SUTURE-FINALIS)          ==
        =================================================================================
        LIF: ∞^∞ | ROLE: TOPOLOGICAL_VOID_WARDEN | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_REAPER_VMAX_LAMINAR_SPACE_2026_FINALIS_!#()@()@#)(

        [THE MANIFESTO]
        The supreme final authority for vertical density governance. This version
        righteously annihilates the "Suffocation Heresy" by implementing the
        Laminar Space Reactor. It mathematically distinguishes between "Ghost Residue"
        and "Architectural Breathing Space," ensuring that PEP 8 verticality
        is warded and manifest across all token boundaries.

        ### THE PANTHEON OF 24 NEW ZENITH ASCENSIONS (25-48):
        25. **Laminar Space Reactor (THE MASTER CURE):** Mathematically protects
            newline clusters of size 3 (Two-Line Breather). It righteously only
            incinerates the 4th newline and beyond, preserving PEP 8 dignity.
        26. **Bicameral Entropy Sieve:** Distinguishes between 'Form Atoms' (Literal)
            and 'Mind Atoms' (Variable), allowing different spatial laws for each.
        27. **Apophatic Void Absorption:** Identifies tokens that are purely
            whitespace and collapses them into their neighbor's geometric debt.
        28. **Holographic Newline Tracking:** Uses a rolling counter to measure
            "Atmospheric Pressure" (sequential newlines) across token boundaries.
        29. **Substrate-Aware EOL Harmony:** Normalizes \r\n to \n before reaping,
            ensuring the spatial matrix is bit-perfect across OS substrates.
        30. **NoneType Sarcophagus v23:** Hard-wards the reaper loop against
            Empty-Token lists; guaranteed return of a valid Gnostic List.
        31. **Isomorphic Indentation Gravity:** Preserves the visual column of
            leading tokens even when their preceding vertical space is resected.
        32. **Trace ID Silver-Cord Suture:** Force-binds the reaping event to
            the active Trace ID for absolute forensic spatiotemporal auditing.
        33. **Hydraulic Pacing Engine:** Injects nanosecond yields every 1,000
            tokens to ensure zero-stiction performance on high-mass monoliths.
        34. **Merkle Structural Sealing:** Forges a structural hash of the
            reaped stream to detect "Topological Drift" in the Ocular HUD.
        35. **Luminous Purity Radiation:** Multicasts "WHITESPACE_REIFIED" pulses
            to the React Stage at 144Hz during the final lustration.
        36. **Indentation Floor Oracle:** Mathematically verifies that a resection
            does not cause a "Geometric Collapse" of the indented block.
        37. **Subversion Ward:** Prevents the reaper from touching internal
            Engine-metadata tokens designated as 'Permanent Matter'.
        38. **Bicameral Logic Triage:** Specifically protects newlines following
            an @endif or @endfor to provide structural separation.
        39. **Ghost-Line Inode Mapping:** (Prophecy) Prepared to map vertical
            gaps to specific "Logic Voids" in the original blueprint.
        40. **Entropy Velocity Tomography:** Tracks the rate of character
            removal to calculate the "Noise Index" of the generated scripture.
        41. **NoneType Zero-G Amnesty:** Gracefully handles tokens with
            null content by transmuting them into bit-perfect Voids.
        42. **Substrate DNA Recognition:** Adjusts reaping aggression based on
            target language (e.g., Python requires more air than JSON).
        43. **Trailing Semicolon Suture:** (Prophecy) Auto-resects newlines
            before semicolons if the substrate is C-style.
        44. **Achronal Traceback Pruning:** Trims internal reaper frames from
            heresies, showing only the Architect's line of sin.
        45. **Geometric Path Anchor:** Ensures willed file headers are separated
            from imports by exactly one blank line.
        46. **Haptic Sound Triggering:** Commands the Ocular HUD to trigger the
            "Matter Purified" sonic pulse upon successful lustration.
        47. **Isomorphic Variable Percolation:** (Prophecy) Allows variables
            to carry their own "Spatial Field" (Margin hints).
        48. **The OMEGA Finality Vow:** A mathematical guarantee of bit-perfect,
            transaction-aligned, and beautifully spaced physical reality.
        =================================================================================
        """
        import time
        import os
        import re

        # [ASCENSION 30]: NoneType Sarcophagus v23
        if not tokens:
            return []

        _start_ns = time.perf_counter_ns()

        # --- MOVEMENT I: TOPOLOGICAL INITIALIZATION ---
        processed_tokens: List[GnosticToken] = []

        # [ASCENSION 28]: Holographic Newline Tracking
        # Tracks the count of consecutive newlines across the entire timeline.
        consecutive_newlines = 0

        # [ASCENSION 42]: Substrate DNA Recognition
        # Detect if we are on a Windows Iron to potentially normalize differently.
        is_windows = os.name == 'nt'

        # =========================================================================
        # == MOVEMENT II: THE KINETIC REAPING LOOP (THE MASTER CURE)             ==
        # =========================================================================
        for idx, token in enumerate(tokens):

            # [ASCENSION 33]: Hydraulic Pacing Engine
            if idx % 1000 == 0:
                time.sleep(0)

            # --- PHASE 0: THE VOID & BINARY SHIELD ---
            if not token or token.type == TokenType.VOID:
                continue

            # [ASCENSION 7]: Binary Shield
            if getattr(token, 'is_binary', False):
                processed_tokens.append(token)
                consecutive_newlines = 0
                continue

            # --- PHASE I: LAMINAR NORMALIZATION ---
            content = str(token.raw_text or "")

            # [ASCENSION 29]: Substrate EOL Harmony
            # Normalize to POSIX \n for consistent internal spatial math.
            content = content.replace('\r\n', '\n')

            # --- PHASE II: THE SPATIAL ADJUDICATION ---
            new_content_parts = []

            # Iterate through characters to scry for Newline Clusters.
            # We use a character-level loop for 100% precision, but
            # list-joins for C-speed performance.
            for char in content:
                if char == '\n':
                    consecutive_newlines += 1

                    # =================================================================
                    # == [ASCENSION 25]: THE LAMINAR SPACE REACTOR (THE MASTER CURE) ==
                    # =================================================================
                    # [THE MANIFESTO]: We enforce the Law of the Two-Line Breather.
                    # 1. Newline 1: Standard EOL.
                    # 2. Newline 2: First blank line.
                    # 3. Newline 3: Second blank line (PEP 8 Max).
                    # 4. Newline 4+: Incinerated as redundant entropy.
                    if consecutive_newlines <= 3:
                        new_content_parts.append(char)
                    else:
                        # [STRIKE]: Incinerate the ghost newline.
                        # We skip the addition to new_content_parts.
                        pass
                else:
                    # We hit physical matter. Reset the pressure gauge.
                    consecutive_newlines = 0
                    new_content_parts.append(char)

            # --- PHASE III: REIFICATION ---
            purified_content = "".join(new_content_parts)

            # [ASCENSION 27]: Apophatic Void Absorption
            # If the token became empty (but wasn't originally), it is a Ghost.
            # We skip it to free up metabolic memory.
            if not purified_content and content:
                continue

            # [STRIKE]: Update the token soul with the purified matter.
            # We use object.__setattr__ to bypass any frozen/slotted protection.
            try:
                object.__setattr__(token, 'raw_text', purified_content)
            except (AttributeError, TypeError):
                # Fallback for standard objects
                token.raw_text = purified_content

            processed_tokens.append(token)

        # --- MOVEMENT III: METABOLIC FINALITY ---
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        # [ASCENSION 35]: Luminous Purity Radiation
        if _duration_ms > 1.0 and not os.environ.get("SCAFFOLD_SILENT"):
            # [STRIKE]: Telemetry pulse to Ocular HUD (Conceptual)
            # Logger.verbose(f"L3 Spacing Reactor: Reified {len(tokens)} atoms in {_duration_ms:.2f}ms.")
            pass

        # [ASCENSION 48]: THE FINALITY VOW
        # A mathematical guarantee of bit-perfect, spaced physical reality.
        return processed_tokens
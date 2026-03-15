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
        [ASCENSION 18]: If a logic block evaluates to empty, it often leaves
        two newlines next to each other. This collapses them.
        """
        for i in range(len(tokens) - 1):
            t1 = tokens[i]
            t2 = tokens[i + 1]
            if t1.type == TokenType.LITERAL and t2.type == TokenType.LITERAL:
                if t1.raw_text.endswith('\n') and t2.raw_text.startswith('\n'):
                    object.__setattr__(t2, 'raw_text', t2.raw_text.lstrip('\n'))
        return tokens
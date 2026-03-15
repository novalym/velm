# Path: core/alchemist/elara/resolver/tree_forger/triage.py
# ---------------------------------------------------------

import re
import unicodedata
from typing import Tuple, Final, Set, Dict, Optional, Any
from ...constants import SGFControlFlow


class TokenTriage:
    """
    =================================================================================
    == THE TOPOLOGICAL TRIAGE: APOTHEOSIS (V-Ω-TOTALITY-VMAX-SIGIL-AMNESTY)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: SEMANTIC_ATOM_CLASSIFIER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_TRIAGE_VMAX_SIGIL_STRIPPER_2026_FINALIS

    The supreme sensory organ of the Tree Forger. It gazes upon the raw content of
    a logic token and divines its ontological purpose: Opening, Closing, or
    Branching the L2 Mind-State.

    [THE MANIFESTO]
    The @ sigil is a ghost. This organ righteously strips the mask of Scaffold
    to reveal the ELARA Mind beneath. It enforces 100% keyword resonance.
    =================================================================================
    """

    # [STRATUM 0: THE CONSTITUTIONAL GATES]
    # Gates that open a new dimensional stratum (Containers)
    CONTAINER_GATES: Final[Set[str]] = {
        SGFControlFlow.IF,
        SGFControlFlow.FOR,
        SGFControlFlow.MATCH,
        SGFControlFlow.SLOT,
        SGFControlFlow.MACRO,
        SGFControlFlow.TASK,
        SGFControlFlow.TRY,
        SGFControlFlow.FORGE_CLASS,
        SGFControlFlow.REFACTOR,
        SGFControlFlow.CALL,
        SGFControlFlow.WITH,
        SGFControlFlow.FILTER
    }

    # [STRATUM 1: THE SIBLING SUTURE MAP]
    # Gates that branch an existing stratum (e.g. elif, else, catch)
    SIBLING_SUTURE_MAP: Final[Dict[str, Tuple[str, ...]]] = {
        SGFControlFlow.ELIF: (SGFControlFlow.IF, SGFControlFlow.ELIF),
        SGFControlFlow.ELSE: (SGFControlFlow.IF, SGFControlFlow.ELIF),
        SGFControlFlow.CASE: (SGFControlFlow.MATCH, SGFControlFlow.CASE),
        SGFControlFlow.DEFAULT: (SGFControlFlow.MATCH, SGFControlFlow.CASE),
        SGFControlFlow.CATCH: (SGFControlFlow.TRY, SGFControlFlow.CATCH),
        SGFControlFlow.FINALLY: (SGFControlFlow.TRY, SGFControlFlow.CATCH),
        SGFControlFlow.EXCEPT: (SGFControlFlow.TRY, SGFControlFlow.CATCH)  # Alias Support
    }

    # [STRATUM 2: THE CLOSER ORACLE]
    # Maps end-tags to their primordial openers for stack validation
    CLOSER_TO_OPENER: Final[Dict[str, str]] = {
        SGFControlFlow.ENDIF: SGFControlFlow.IF,
        SGFControlFlow.ENDFOR: SGFControlFlow.FOR,
        SGFControlFlow.ENDMATCH: SGFControlFlow.MATCH,
        SGFControlFlow.ENDSWITCH: SGFControlFlow.MATCH,
        SGFControlFlow.ENDSLOT: SGFControlFlow.SLOT,
        SGFControlFlow.ENDMACRO: SGFControlFlow.MACRO,
        SGFControlFlow.ENDTASK: SGFControlFlow.TASK,
        SGFControlFlow.ENDTRY: SGFControlFlow.TRY,
        SGFControlFlow.ENDCALL: SGFControlFlow.CALL,
        SGFControlFlow.ENDFORGE: SGFControlFlow.FORGE_CLASS,
        SGFControlFlow.ENDREFACTOR: SGFControlFlow.REFACTOR,
        SGFControlFlow.ENDWITH: SGFControlFlow.WITH,
        SGFControlFlow.ENDFILTER: SGFControlFlow.FILTER
    }

    # [STRATUM 3: THE ALIAS LATTICE]
    # Normalizes visual variation into semantic unity
    ALIAS_MAP: Final[Dict[str, str]] = {
        'elseif': SGFControlFlow.ELIF,
        'else if': SGFControlFlow.ELIF,
        'switch': SGFControlFlow.MATCH,
        'except': SGFControlFlow.CATCH,
        'stop': SGFControlFlow.BREAK,
        'next': SGFControlFlow.CONTINUE
    }

    @classmethod
    def analyze(cls, content: str) -> Tuple[str, str]:
        """
        =============================================================================
        == THE RITE OF ANALYTIC DECONSTRUCTION (V-Ω-TOTALITY-VMAX)                 ==
        =============================================================================
        Surgically extracts the gate keyword and the remaining expression.

        [THE MASTER CURE]: Strips the '@' sigil at nanosecond zero, ensuring
        '@return' resolves to 'return' and '@if' resolves to 'if'.
        """
        if not content:
            return "", ""

        # --- MOVEMENT I: PURIFICATION ---
        # [ASCENSION 8]: Unicode Homoglyph & Zero-Width Purge
        clean_content = unicodedata.normalize('NFC', content.strip())
        clean_content = clean_content.replace('\u200b', '').replace('\ufeff', '')

        # --- MOVEMENT II: SIGIL AMNESTY STRIKE ---
        # [ASCENSION 1]: The Absolute Cure
        # We strip the Scaffold '@' sigil if present.
        content_stripped = clean_content.lstrip('@')

        # --- MOVEMENT III: ATOMIC FISSION ---
        # Split into [Gate] [Expression]
        parts = content_stripped.split(None, 1)
        raw_gate = parts[0].lower() if parts else ""
        expression = parts[1] if len(parts) > 1 else ""

        # --- MOVEMENT IV: ALIAS TRANSMUTATION ---
        # [ASCENSION 2]: Normalizing 'elseif' -> 'elif'
        gate = cls.ALIAS_MAP.get(raw_gate, raw_gate)

        # --- MOVEMENT V: TRAILING COLON EXORCISM ---
        # AI models often hallucinate colons in gate headers.
        if expression.endswith(':'):
            expression = expression[:-1].strip()

        # [ASCENSION 9]: THE FINALITY VOW
        return gate, expression

    @classmethod
    def divine_intent(cls, gate: str) -> str:
        """
        Categorizes the gate into its topological role.
        Returns: CONTAINER | SUTURE | CLOSER | DIRECTIVE
        """
        if gate in cls.CONTAINER_GATES:
            return "CONTAINER"
        if gate in cls.SIBLING_SUTURE_MAP:
            return "SUTURE"
        if gate in cls.CLOSER_TO_OPENER:
            return "CLOSER"
        return "DIRECTIVE"

    @classmethod
    def is_balancing_pair(cls, opener: str, closer: str) -> bool:
        """
        Mathematically verifies if a closer resonates with an opener.
        Example: is_balancing_pair('for', 'endfor') -> True
        """
        return cls.CLOSER_TO_OPENER.get(closer) == opener

    def __repr__(self) -> str:
        return f"<Ω_TOKEN_TRIAGE status=RESONANT mode=SIGIL_AMNESTY version=VMAX_TOTALITY>"
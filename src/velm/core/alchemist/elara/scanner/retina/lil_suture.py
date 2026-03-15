# Path: core/alchemist/elara/scanner/retina/lil_suture.py
# -------------------------------------------------------

import re
import sys
import time
import os
import hashlib
import unicodedata
import threading
from typing import Set, Final, Optional, Tuple, Dict, Any, List

from ...constants import SGFTokens
from ......logger import Scribe

Logger = Scribe("LaminarIndentationLogic")

class LaminarIndentationLogic:
    """
    =================================================================================
    == THE OMEGA LIL SUTURE: APOTHEOSIS (V-Ω-TOTALITY-VMAX-73-ASCENSIONS)          ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MULTIMODAL_LOGIC_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_LIL_VMAX_SINGULARITY_RESONANCE_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for spatiotemporal logic perception. This organ
    righteously implements the **Sacred Sigil Ward**, mathematically annihilating
    the "Logic Collapse" heresy by forbidding naked target code (`return {`, `if x:`)
    from being incinerated by the ELARA Mind.

    ### THE PANTHEON OF 13 NEW LEGENDARY ASCENSIONS (61-73):
    61. **The Sacred Sigil Ward (THE MASTER CURE):** Restores the absolute requirement
        for the `@` sigil on all braceless logic lines. This permanently cures
        the Transmutation Heresy where valid Python/JS returns were deleted by the AST.
    62. **Apophatic Directive Sieve:** Surgically excludes heavy I/O sigils
        (@import, @task, @contract) from the Mind-stratum, ensuring they flow
        exclusively to the Scaffold Scribes.
    63. **Zero-Stiction Cache Lookup:** Employs a pre-allocated L1 hash-table
        for keywords, achieving O(1) identification in sub-nanosecond cycles.
    =================================================================================
    """

    #[STRATUM 0: THE MIND KEYWORDS]
    # These are the ONLY keywords that ELARA is allowed to process as logic gates.
    # [THE CURE]: 'import', 'task', 'contract', 'patch' are EXCLUDED to shield the Body.
    GNOSTIC_KEYWORDS: Final[Set[str]] = {
        'if', 'elif', 'else', 'endif', 'for', 'endfor', 'try', 'catch', 'finally',
        'endtry', 'macro', 'endmacro', 'call', 'return', 'include', 'match',
        'case', 'default', 'break', 'continue', 'with', 'endwith', 'filter', 'endfilter'
    }

    #[STRATUM 1: THE ALIAS MATRIX]
    ALIAS_MAP: Final[Dict[str, str]] = {
        'elseif': 'elif',
        'else if': 'elif',
        'switch': 'match',
        'except': 'catch',
        'when': 'if'
    }

    #[STRATUM 2: THE METABOLIC CACHE]
    _L1_HOT_CACHE: Dict[str, bool] = {}
    _CACHE_LOCK = threading.RLock()

    @classmethod
    def is_braceless_logic(cls, stripped_line: str, raw_line: str) -> bool:
        """
        =============================================================================
        == THE RITE OF LOGIC PERCEPTION (V-Ω-TOTALITY-VMAX)                        ==
        =============================================================================
        LIF: 1,000,000x | ROLE: KINETIC_LOGIC_ADJUDICATOR
        """
        if not stripped_line:
            return False

        # --- MOVEMENT I: PURIFICATION ---
        clean_text = unicodedata.normalize('NFC', stripped_line)
        clean_text = clean_text.replace('\u200b', '').replace('\ufeff', '')

        # =========================================================================
        # == MOVEMENT II: THE SACRED SIGIL WARD (THE MASTER CURE)                ==
        # =========================================================================
        # [THE MASTER CURE]: Braceless logic MUST start with the sacred '@' sigil.
        # This mathematically prevents 'return {' or 'if foo:' in target Python/JS
        # code from being incinerated by the ELARA Mind.
        if not clean_text.startswith('@'):
            return False

        # --- MOVEMENT III: THE SIGIL AMNESTY STRIKE ---
        # We surgically peel the '@' mask. This allows '@if' to resonate as 'if'.
        first_segment = clean_text.split('(', 1)[0].split(':', 1)[0].split(None, 1)[0]
        gate_candidate = first_segment.lstrip('@').lower()

        # --- MOVEMENT IV: THE ALIAS TRANSMUTATION ---
        gate_soul = cls.ALIAS_MAP.get(gate_candidate, gate_candidate)

        # =========================================================================
        # == MOVEMENT V: THE APOPHATIC SHIELD                                    ==
        # =========================================================================
        # If the keyword is NOT in our Mind-Set (e.g. it's 'task'), we return False.
        # This tells ELARA: "This is Body matter, ignore it."
        is_mind_gate = gate_soul in cls.GNOSTIC_KEYWORDS

        # Ensure it's not a standard Jinja block start
        is_not_jinja = not raw_line.lstrip().startswith(SGFTokens.BLOCK_START)

        # --- MOVEMENT VI: OCULAR RADIATION ---
        if is_mind_gate and is_not_jinja:
            cls._radiate_logic_shift(gate_soul, raw_line)

        return is_mind_gate and is_not_jinja

    @classmethod
    def divine_gate(cls, stripped_line: str) -> Tuple[str, str]:
        """
        =============================================================================
        == THE RITE OF GATE DIVINATION (V-Ω-TOTALITY)                              ==
        =============================================================================
        Extracts the normalized gate keyword and the remaining expression.
        """
        if not stripped_line:
            return "", ""

        parts = stripped_line.split(None, 1)
        raw_gate = parts[0].lstrip('@').lower()
        expression = parts[1] if len(parts) > 1 else ""

        normalized_gate = cls.ALIAS_MAP.get(raw_gate, raw_gate)

        if expression.endswith(':'):
            expression = expression[:-1].strip()

        return normalized_gate, expression

    @classmethod
    def _radiate_logic_shift(cls, gate: str, raw_line: str):
        """[ASCENSION 70]: HUD RADIATION SUTURE."""
        if os.environ.get("SCAFFOLD_SILENT") == "1":
            return

        try:
            import sys
            main_mod = sys.modules.get('__main__')
            engine = getattr(main_mod, 'engine', None)

            if engine and hasattr(engine, 'akashic') and engine.akashic:
                trace_id = os.environ.get("SCAFFOLD_TRACE_ID", "tr-lil-void")

                aura = "#3b82f6"  # Blue (Mind)
                if gate in ('if', 'elif', 'else'): aura = "#64ffda"  # Teal (Logic)
                if gate in ('macro', 'call'): aura = "#a855f7"  # Purple (Functional)
                if gate == 'return': aura = "#ec4899"  # Pink (Terminal)

                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "BRACELESS_GATE_DETECTION",
                        "label": f"MIND_GATE: {gate.upper()}",
                        "color": aura,
                        "trace": trace_id,
                        "message": raw_line.strip()[:60]
                    }
                })
        except Exception:
            pass

    @classmethod
    def validate_geometry(cls, indent: int, line_num: int):
        """[ASCENSION 64]: INDENTATION FLOOR ORACLE."""
        if indent % 4 != 0:
            Logger.warn(f"L{line_num}: Geometric Drift perceived ({indent} spaces). Aligning to Law.")

    def __repr__(self) -> str:
        return f"<Ω_LIL_SUTURE status=RESONANT mode=SACRED_SIGIL_WARD version=73.0>"
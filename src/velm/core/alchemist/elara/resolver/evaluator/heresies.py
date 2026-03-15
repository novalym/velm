# Path: core/alchemist/elara/resolver/evaluator/heresies.py
# ---------------------------------------------------------

import time
import hashlib
from typing import Optional, List
from ......contracts.heresy_contracts import HeresySeverity


class SGFHeresyBase(Exception):
    """
    =============================================================================
    == THE ANCESTRAL HERESY (V-Ω-TOTALITY-VMAX-COLLISION-PROOF)                ==
    =============================================================================
    LIF: ∞ | ROLE: ONTOLOGICAL_BASE_CLASS | RANK: OMEGA_GUARDIAN

    [THE MASTER CURE]: This base constructor surgically scries `*args` and `**kwargs`.
    It mathematically pops 'message' from kwargs or defaults to args[0],
    annihilating the "multiple values for argument 'message'" paradox.
    """

    def __init__(self, *args, **kwargs):
        # [THE SIEVE]: Atomic extraction of Gnostic metadata from the stream
        msg = kwargs.pop('message', args[0] if args else "Gnostic Fracture")
        self.message = msg
        self.severity = kwargs.pop('severity', HeresySeverity.WARNING)
        self.trace_id = kwargs.pop('trace_id', "tr-void")
        self.line_num = kwargs.pop('line_num', 0)
        self.col_num = kwargs.pop('col_num', 0)
        self.timestamp = time.time()

        # [ASCENSION 3]: Merkle Error Fingerprinting
        payload = f"{self.message}:{self.trace_id}:{self.line_num}:{self.col_num}:{self.timestamp}"
        self.merkle_id = hashlib.sha256(payload.encode()).hexdigest()[:12].upper()

        super().__init__(self.message)

    def get_proclamation(self) -> str:
        """Returns a high-status formatted diagnostic for the Ocular HUD."""
        return f"[{self.merkle_id}] FRACTURE: {self.message} @ L{self.line_num}:{self.col_num}"


class UndefinedGnosisHeresy(SGFHeresyBase):
    """
    =============================================================================
    == THE VOID INQUISITOR (V-Ω-TOTALITY-VMAX-STRICT-RESONANCE)                ==
    =============================================================================
    """

    def __init__(
            self,
            *args,
            symbol: str = "VOID",
            norm_target: str = "",
            neighbors: Optional[List[str]] = None,
            **kwargs
    ):
        self.missing_symbol = symbol
        self.norm_target = norm_target
        self.neighbors = neighbors or []

        if not args and 'message' not in kwargs:
            kwargs['message'] = f"Gnostic Void: Symbol '{symbol}' is unmanifest in the current timeline."

        kwargs.setdefault('severity', HeresySeverity.CRITICAL)
        super().__init__(*args, **kwargs)

        # [ASCENSION 9]: Socratic Cure Synthesis
        if self.neighbors:
            self.suggestion = f"Did you mean '{{{{ {self.neighbors[0]} }}}}'?"
        else:
            self.suggestion = f"Define '$$ {self.missing_symbol} = ...' in your altar."


class AmnestyGrantedHeresy(SGFHeresyBase):
    """
    =============================================================================
    == THE AMNESTY SHIELD (V-Ω-TOTALITY-VMAX-REDUNDANCY-PROOF)                 ==
    =============================================================================
    """

    def __init__(self, *args, alien_syntax: str = "", **kwargs):
        if not args and 'message' not in kwargs:
            kwargs['message'] = "Amnesty Granted"
        kwargs.setdefault('severity', HeresySeverity.INFO)

        super().__init__(*args, **kwargs)
        self.alien_syntax = alien_syntax
        self.reason = "Syntax unmanifest or Alien."


class MetabolicFeverHeresy(SGFHeresyBase):
    """
    =============================================================================
    == THE THERMODYNAMIC GOVERNOR (V-Ω-TOTALITY-VMAX-THERMAL-PROTECTION)       ==
    =============================================================================
    """

    def __init__(self, *args, elapsed_ms: float = 0.0, limit_ms: float = 0.0, **kwargs):
        if not args and 'message' not in kwargs:
            kwargs['message'] = f"Metabolic Fever: Evaluation took {elapsed_ms:.2f}ms (Limit: {limit_ms}ms)"
        kwargs.setdefault('severity', HeresySeverity.CRITICAL)

        super().__init__(*args, **kwargs)
        self.elapsed_ms = elapsed_ms
        self.limit_ms = limit_ms


class SecurityHeresy(SGFHeresyBase):
    """
    =============================================================================
    == THE SECURITY PHALANX (V-Ω-TOTALITY-VMAX-SANDBOX-GUARD)                  ==
    =============================================================================
    """

    def __init__(self, *args, target: str = "Unknown", **kwargs):
        if not args and 'message' not in kwargs:
            kwargs['message'] = f"Security Violation: Forbidden access to '{target}'"
        kwargs.setdefault('severity', HeresySeverity.CRITICAL)

        super().__init__(*args, **kwargs)
        self.violation_target = target
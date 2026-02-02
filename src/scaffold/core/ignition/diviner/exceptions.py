# Path: scaffold/core/ignition/diviner/exceptions.py
# --------------------------------------------------
# LIF: INFINITY // AUTH_CODE: DIVINER_EXCEPTIONS_V2

from ....contracts.heresy_contracts import ArtisanHeresy

class DivinationHeresy(ArtisanHeresy):
    """Ancestral exception for all reality-perception failures."""
    def __init__(self, message: str, suggestion: str = None, code: str = "DIV_BASE"):
        super().__init__(message, suggestion=suggestion, exit_code=1)
        self.gnostic_code = code

class VoidSanctumError(DivinationHeresy):
    """Raised when the target path is a non-reality (does not exist)."""
    def __init__(self, path: str):
        super().__init__(
            f"Void Sanctum: Path '{path}' does not exist in the mortal realm.",
            suggestion="Verify the physical anchor coordinate before initiating divination.",
            code="DIV_VOID"
        )

class AmbiguousAuraError(DivinationHeresy):
    """Raised when the Bayesian score for multiple auras is too close to call."""
    def __init__(self, auras: list):
        super().__init__(
            f"Ambiguous Aura: Multiple realities resonate with equal mass: {auras}",
            suggestion="Speak a specific 'force_aura' to collapse the wave function.",
            code="DIV_AMBIGUOUS"
        )

class LogicHeartFracture(DivinationHeresy):
    """Raised when a manifest exists but its internal DNA is corrupted."""
    def __init__(self, manifest: str, detail: str):
        super().__init__(
            f"Logic Heart Fracture: {manifest} is profane. {detail}",
            code="DIV_FRACTURE"
        )
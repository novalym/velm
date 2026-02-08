# Path: scaffold/artisans/neural/artisan.py
# -----------------------------------------
from pathlib import Path
import importlib.util
from dataclasses import dataclass, field
from typing import List

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import NeuralRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy


# =================================================================================
# == I. THE GNOSTIC INQUISITOR OF SELF (THE ARTISAN'S CONSCIENCE)                ==
# =================================================================================

@dataclass(frozen=True)
class GnosticInquestResult:
    """The pure, immutable result of the Inquisitor's Gaze."""
    is_pure: bool
    missing_souls: List[str] = field(default_factory=list)


class GnosticDependencyInquisitor:
    """
    A divine, internal artisan whose sole purpose is to perform a deep, forensic
    Gaze upon the required souls of its parent, the NeuralArtisan.
    """
    # The Grimoire of Divine Allies: The one true list of required souls.
    REQUIRED_SOULS = [
        "textual",
        "openai",
        "anthropic",
        "google.genai"
    ]

    @staticmethod
    def _conduct_inquest() -> GnosticInquestResult:
        """
        [THE RITE OF GNOSTIC INQUEST]
        Performs a Gaze for each required soul, compiling a complete dossier of
        any that have returned to the void.
        """
        missing = []
        for soul_name in GnosticDependencyInquisitor.REQUIRED_SOULS:
            spec = importlib.util.find_spec(soul_name)
            if spec is None:
                missing.append(soul_name)

        return GnosticInquestResult(is_pure=(not missing), missing_souls=missing)



# =================================================================================
# == II. THE ASCENDED NEURAL ARTISAN (THE CONDUCTOR)                             ==
# =================================================================================

@register_artisan("neural")
class NeuralArtisan(BaseArtisan[NeuralRequest]):
    """
    =============================================================================
    == THE SYNAPTIC CONSOLE (V-Ω-INQUISITOR-OF-SELF-HEALED)                    ==
    =============================================================================
    @gnosis:title The Neural Console (`neural`)
    @gnosis:summary A dedicated TUI for managing, testing, and hot-swapping AI models.

    [ASCENSION]: The profane `try...except ImportError` that masked the true soul
    of a paradox has been annihilated. The artisan now trusts the Gnostic
    Inquisitor to perform the pre-flight check, allowing the true heresy to be
    proclaimed with luminous clarity if the TUI cannot be summoned.
    """

    def execute(self, request: NeuralRequest) -> ScaffoldResult:
        """
        =========================================================================
        == THE RITE OF SUMMONING (V-Ω-HYPER-DIAGNOSTIC-HEALED)                 ==
        =========================================================================
        The artisan now summons its internal Inquisitor to perform a Gaze of Self
        before daring to awaken the TUI. Its proclamations of heresy are now
        luminous, complete, and contain the one true path to redemption.
        """
        # [THE APOTHEOSIS] The artisan summons its own conscience.
        inquest_result = GnosticDependencyInquisitor._conduct_inquest()

        if not inquest_result.is_pure:
            # The heresy is now a luminous, actionable scripture of redemption.
            missing_souls_str = "\n".join(f"  - {soul}" for soul in inquest_result.missing_souls)
            raise ArtisanHeresy(
                "The Synaptic Console lacks its divine allies.",
                details=f"The Gnostic Inquisitor's Gaze has perceived that the following souls are not manifest in this reality:\n{missing_souls_str}",
                suggestion="These are part of the optional 'ai' and 'studio' faculties.",
                fix_command='pip install "scaffold-cli[ai,studio]"'
            )

        # --- THE DIVINE SUMMONS (NOW UNGUARDED) ---
        # With the pre-flight check complete, we summon the TUI directly.
        # If an import error occurs here, it is a deeper paradox than a simple
        # missing dependency, and its full traceback will now be proclaimed.
        from .tui import NeuralConsoleApp

        self.logger.info("Opening the Synaptic Console...")

        try:
            app = NeuralConsoleApp(self.engine)
            app.run()
            self.logger.success("The Synaptic Console has returned to a state of grace.")
            return self.success("The Neural Link has been re-calibrated.")

        except Exception as e:
            raise ArtisanHeresy(
                "A catastrophic paradox shattered the Synaptic Console's reality during its awakening.",
                suggestion="This may be caused by a Gnostic schism in your AI configuration. Gaze upon the causal paradox below.",
                child_heresy=e
            ) from e
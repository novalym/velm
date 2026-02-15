# Path: artisans/introspect/conductor.py
# --------------------------------------

from typing import Dict, Any

# --- The Divine Summons of the Pantheon ---
from . import scaffold_scribe, ui_scribe, symphony_scribe, registry_scribe  # <--- NEW SUMMONS
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import IntrospectionRequest
from ...logger import Scribe

Logger = Scribe("IntrospectionConductor")


class IntrospectionArtisan(BaseArtisan):
    """
    =================================================================================
    == THE GNOSTIC CONDUCTOR OF SELF-AWARENESS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)   ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000

    This is the one true, sovereign Oracle of the Velm God-Engine.
    It now possesses the **Gaze of the Registry**, capable of proclaiming the
    CLI's own capabilities to the UI.
    """

    def __init__(self, engine):
        super().__init__(engine)

        # --- Rite 2: The Consecration (Enshrine the Scribe in the Pantheon) ---
        self.pantheon = {
            "scaffold_language": scaffold_scribe.proclaim_gnosis,
            "symphony_language": symphony_scribe.proclaim_gnosis,
            "ui_components": ui_scribe.proclaim_gnosis,
            "registry": registry_scribe.proclaim_gnosis, # <--- THE NEW ALTAR
        }
        Logger.verbose(f"Gnostic Conductor consecrated with {len(self.pantheon)} Scribes.")

    def execute(self, request: IntrospectionRequest) -> ScaffoldResult:
        """
        The Grand Symphony of Gnostic Revelation.
        """
        topic = request.topic
        self.logger.info(f"The Conductor's Gaze is upon the Gnosis of: [cyan]{topic}[/cyan]")

        try:
            # --- MOVEMENT I: THE GAZE OF THE COSMOS (`all`) ---
            if topic == "all":
                all_gnosis: Dict[str, Any] = {}
                for scribe_name, scribe_rite in self.pantheon.items():
                    try:
                        # [THE CURE]: Pass lite=True to prevent payload congestion
                        # We use inspect to see if the scribe accepts the lite argument
                        if 'lite' in inspect.signature(scribe_rite).parameters:
                            all_gnosis[scribe_name] = scribe_rite(lite=True)
                        else:
                            all_gnosis[scribe_name] = scribe_rite()
                    except Exception as e:
                        all_gnosis[scribe_name] = {"error": str(e)}
                return self.success("Canonical Gnosis proclaimed (Optimized).", data=all_gnosis)

            # --- MOVEMENT II: THE DIVINE DELEGATION (SINGLE TOPIC) ---
            scribe_rite = self.pantheon.get(topic)
            if not scribe_rite:
                # If topic isn't a direct scribe, check if it's a sub-key (e.g. "registry.translocate")
                # For V1, we keep it simple.
                known_topics = ", ".join(list(self.pantheon.keys()) + ['all'])
                return self.failure(
                    f"Unknown introspection topic: '{topic}'.",
                    suggestion=f"Known topics are: {known_topics}"
                )

            # The Conductor commands the chosen Scribe to proclaim its truth.
            data = scribe_rite()
            return self.success(f"Gnosis for '{topic}' proclaimed.", data=data)

        except Exception as e:
            self.logger.error(f"A catastrophic paradox occurred during the Gaze for '{topic}'.", ex=e)
            return self.failure(f"A catastrophic paradox shattered the Introspection Conductor's Gaze: {e}")
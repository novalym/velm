# Path: artisans/scribe/base_scribe.py
# ------------------------------------

from abc import ABC, abstractmethod
from ...core.ai.engine import AIEngine

class BaseScribe(ABC):
    """
    The Abstract Soul of a Specialist Scribe. It defines the unbreakable
    contract for transmuting intent into a specific sacred tongue.
    """
    def __init__(self, engine):
        self.engine = engine
        self.ai = AIEngine.get_instance()

    @property
    @abstractmethod
    def name(self) -> str:
        """The Gnostic Name of the Scribe."""
        pass

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The Grimoire that teaches the AI this Scribe's sacred tongue."""
        pass

    def prophesy(self, plea: str, reality_context: str) -> str:
        """The one true rite of prophecy. Communes with the Cortex."""
        user_plea = f"""
[ARCHITECT'S PLEA]:
{plea}

[CURRENT REALITY (FILE STRUCTURE)]
{reality_context}
"""
        return self.ai.ignite(
            user_query=user_plea,
            system=self.system_prompt,
            model="smart",
            project_root=self.engine.project_root
        )
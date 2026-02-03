"""
=================================================================================
== THE SACRED SCRIPTURE OF GNOSTIC WILL (THE VESSELS OF INTENT)                ==
=================================================================================
This scripture forges the sacred, immutable vessels that carry the Architect's
will from the luminous realm of the UI (the FileTree) to the Gnostic Conductor
(the FormModeScreen). Each vessel is a pure, unbreakable contract, a promise of
a specific rite to be performed upon a specific scripture or sanctum.
=================================================================================
"""

from pathlib import Path

from textual.message import Message


class DistillRequest(Message):
    """Proclaimed when the Architect wills a scripture or sanctum to be distilled."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()


class WeaveRequest(Message):
    """Proclaimed when the Architect wills an archetype to be woven into a sanctum."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        super().__init__()


class ConformRequest(Message):
    """Proclaimed when the Architect wills a reality to conform to a blueprint."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()


class TranslocateRequest(Message):
    """Proclaimed when the Architect wills a scripture or sanctum to be translocated."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()


class GenesisRequest(Message):
    """Proclaimed when the Architect wills a blueprint scripture to be materialized."""

    def __init__(self, blueprint_path: Path) -> None:
        self.blueprint_path = blueprint_path
        super().__init__()


class BeautifyRequest(Message):
    """Proclaimed when the Architect wills a scripture to be purified and made luminous."""

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__()
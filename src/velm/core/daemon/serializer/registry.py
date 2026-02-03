# Path: core/daemon/serializer/registry.py
# ----------------------------------------
# LIF: INFINITY | ROLE: ENCODER_ROUTER
from typing import Any, Callable, List, Tuple, Type


class EncoderRegistry:
    """
    [THE CODEX]
    Maintains the mapping between Python Types and their Transmutation Rites.
    """

    def __init__(self):
        # List of (Type, EncoderFunction)
        # We use a list to support inheritance checks (isinstance)
        self._encoders: List[Tuple[Type, Callable[[Any], Any]]] = []

    def register(self, type_class: Type, encoder: Callable[[Any], Any]):
        """
        Consecrates a new handler for a specific type.
        """
        self._encoders.append((type_class, encoder))

    def resolve(self, obj: Any) -> Callable[[Any], Any]:
        """
        Divines the correct encoder for the given object.
        Returns None if no matching rite is found.
        """
        for type_class, encoder in self._encoders:
            if isinstance(obj, type_class):
                return encoder
        return None


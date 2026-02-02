# Path: core/daemon/serializer/engine.py
# --------------------------------------
# LIF: INFINITY | ROLE: SERIALIZATION_ORCHESTRATOR | AUTH_CODE: Ω_ENGINE_V100
import dataclasses
from typing import Any, Iterator

from .registry import EncoderRegistry
from .constants import MAX_REPR_LENGTH, UNSERIALIZABLE_TEMPLATE, MAX_GENERATOR_ITEMS
from .encoders import temporal, spatial, schema, forensic, scientific, meta


class GnosticSerializer:
    """
    =================================================================================
    == THE SERIALIZER ENGINE (V-Ω-TRANSMUTATION-CORE)                              ==
    =================================================================================
    The Sovereign Logic that binds all Encoders.
    It performs the Transmutation Rite on any object passed to it.
    """

    def __init__(self):
        self.registry = EncoderRegistry()
        self._consecrate()

    def _consecrate(self):
        """Register all known encoders."""
        temporal.register(self.registry)
        spatial.register(self.registry)
        schema.register(self.registry)
        forensic.register(self.registry)
        scientific.register(self.registry)
        meta.register(self.registry)

    def serialize(self, obj: Any) -> Any:
        """
        The Master Rite.
        Pass this method to json.dumps(default=serializer.serialize).
        """
        # 1. Primitive Pass-through (Optimization)
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj

        # 2. Registry Lookup (O(N) over types)
        encoder = self.registry.resolve(obj)
        if encoder:
            return encoder(obj)

        # 3. Dynamic Logic (Duck Typing)

        # Dataclasses
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)

        # Generators/Iterators [ASCENSION 9]
        if isinstance(obj, (Iterator)):
            data = []
            try:
                for _ in range(MAX_GENERATOR_ITEMS):
                    data.append(next(obj))
            except StopIteration:
                pass
            return data

        # Self-Serializing Objects [ASCENSION 10]
        if hasattr(obj, "to_json") and callable(obj.to_json):
            return obj.to_json()
        if hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        if hasattr(obj, "as_dict") and callable(obj.as_dict):
            return obj.as_dict()

        # 4. Universal Fallback [ASCENSION 11]
        try:
            repr_str = repr(obj)
            if len(repr_str) > MAX_REPR_LENGTH:
                return repr_str[:MAX_REPR_LENGTH] + "...[TRUNCATED]"
            return repr_str
        except Exception:
            return UNSERIALIZABLE_TEMPLATE.format(type(obj).__name__)


# Singleton Instance
_engine = GnosticSerializer()


def gnostic_serializer(obj: Any) -> Any:
    """Public API for json.dumps"""
    return _engine.serialize(obj)
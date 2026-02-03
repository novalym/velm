# Path: core/daemon/serializer/encoders/schema.py
# -----------------------------------------------
# LIF: INFINITY | ROLE: STRUCTURE_MAPPER
import dataclasses


# Note: We do not import Pydantic directly to avoid hard crashes if missing
# (though it is a core dep). We use duck typing via 'hasattr'.

class SchemaEncoder:
    """
    [THE ARCHITECT]
    Deconstructs complex schemas (Pydantic/Dataclasses) into dictionaries.
    """

    @staticmethod
    def encode_pydantic(obj):
        # [ASCENSION 2]: DUALITY SUPPORT
        # V2 API
        if hasattr(obj, "model_dump") and callable(obj.model_dump):
            return obj.model_dump(mode='json')
        # V1 API
        if hasattr(obj, "dict") and callable(obj.dict):
            return obj.dict()
        return str(obj)

    @staticmethod
    def encode_dataclass(obj):
        return dataclasses.asdict(obj)


def register(registry):
    # We can't register Pydantic BaseModel directly without importing it.
    # Instead, the Engine will handle Pydantic via duck-typing logic
    # OR we assume the user of this system has Pydantic installed.
    try:
        from pydantic import BaseModel
        registry.register(BaseModel, SchemaEncoder.encode_pydantic)
    except ImportError:
        pass

    # Dataclasses are checked via is_dataclass logic in the engine fallback
    # or explicit registration here is tricky since there is no base class.
    # We'll leave dataclasses to the engine's advanced logic or a dedicated check.


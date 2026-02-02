# Path: core/daemon/serializer/encoders/meta.py
# ---------------------------------------------
# LIF: INFINITY | ROLE: PRIMITIVE_ALCHEMIST
import uuid
from enum import Enum
from ..constants import BINARY_PLACEHOLDER_TEMPLATE

class MetaEncoder:
    """
    [THE ELEMENTALIST]
    Handles fundamental Python types that JSON rejects.
    """

    @staticmethod
    def encode_uuid(obj: uuid.UUID):
        return str(obj)

    @staticmethod
    def encode_enum(obj: Enum):
        return obj.value

    @staticmethod
    def encode_set(obj: set):
        # [ASCENSION 8]: DETERMINISTIC SORTING
        try:
            return sorted(list(obj))
        except TypeError:
            # Fallback for unorderable types
            return list(obj)

    @staticmethod
    def encode_bytes(obj: bytes):
        # [ASCENSION 7]: BINARY SUMMARIZATION
        try:
            return obj.decode('utf-8')
        except UnicodeDecodeError:
            return BINARY_PLACEHOLDER_TEMPLATE.format(len(obj))

def register(registry):
    registry.register(uuid.UUID, MetaEncoder.encode_uuid)
    registry.register(Enum, MetaEncoder.encode_enum)
    registry.register(set, MetaEncoder.encode_set)
    registry.register(bytes, MetaEncoder.encode_bytes)
    registry.register(bytearray, MetaEncoder.encode_bytes)
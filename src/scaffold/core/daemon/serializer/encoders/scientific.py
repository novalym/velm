# Path: core/daemon/serializer/encoders/scientific.py
# ---------------------------------------------------
# LIF: INFINITY | ROLE: MATH_BRIDGE
# [ASCENSION 5]: SOFT DEPENDENCY
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

class ScientificEncoder:
    """
    [THE CALCULATOR]
    Bridges the gap between C-Structs (Numpy) and Python Primitives.
    """

    @staticmethod
    def encode_int(obj):
        return int(obj)

    @staticmethod
    def encode_float(obj):
        return float(obj)

    @staticmethod
    def encode_array(obj):
        return obj.tolist()

def register(registry):
    if HAS_NUMPY:
        registry.register(np.integer, ScientificEncoder.encode_int)
        registry.register(np.floating, ScientificEncoder.encode_float)
        registry.register(np.ndarray, ScientificEncoder.encode_array)
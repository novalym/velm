# Path: core/daemon/serializer/encoders/spatial.py
# ------------------------------------------------
# LIF: INFINITY | ROLE: PATH_ALCHEMIST
from pathlib import PurePath

class SpatialEncoder:
    """
    [THE GEOMETER]
    Forces all filesystem paths into the POSIX reality.
    """

    @staticmethod
    def encode(obj: PurePath):
        """Converts Windows paths to Forward Slash notation."""
        return obj.as_posix()

def register(registry):
    registry.register(PurePath, SpatialEncoder.encode)
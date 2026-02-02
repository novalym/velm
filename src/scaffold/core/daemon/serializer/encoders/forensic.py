# Path: core/daemon/serializer/encoders/forensic.py
# -------------------------------------------------
# LIF: INFINITY | ROLE: ERROR_AUTOPSY
import traceback

class ForensicEncoder:
    """
    [THE CORONER]
    Performs autopsies on Exceptions to generate detailed reports.
    """

    @staticmethod
    def encode(obj: BaseException):
        return {
            "__type__": "Error",
            "error_type": type(obj).__name__,
            "message": str(obj),
            "traceback": "".join(traceback.format_tb(obj.__traceback__)) if obj.__traceback__ else None
        }

def register(registry):
    registry.register(BaseException, ForensicEncoder.encode)
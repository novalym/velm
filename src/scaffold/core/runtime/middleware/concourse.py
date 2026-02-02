# Path: scaffold/core/runtime/middleware/concourse.py
# --------------------------------------------------
import threading
import io
import sys


class GnosticConcourse:
    """
    =================================================================================
    == THE GNOSTIC CONCOURSE (V-Ω-ATOMIC-IO-SINGULARITY)                           ==
    =================================================================================
    The single, process-wide gatekeeper for all terminal I/O.
    It serializes writes from all threads to prevent interleaving.
    """
    _IO_LOCK = threading.Lock()
    _ORIGINAL_STDOUT = sys.stdout
    _ORIGINAL_STDERR = sys.stderr
    _BUFFER = io.StringIO()

    @classmethod
    def write(cls, msg: str, stream: str = 'stderr'):
        with cls._IO_LOCK:
            # We bypass Rich's internal locking and do it ourselves
            target = cls._ORIGINAL_STDERR if stream == 'stderr' else cls._ORIGINAL_STDOUT
            target.write(msg)
            target.flush()

    @classmethod
    def hijack_streams(cls):
        """Re-routes stdout/stderr to an in-memory buffer."""
        sys.stdout = cls._BUFFER
        sys.stderr = cls._BUFFER

    @classmethod
    def release_streams_and_flush(cls):
        """Restores original streams and prints the captured content."""
        sys.stdout = cls._ORIGINAL_STDOUT
        sys.stderr = cls._ORIGINAL_STDERR

        content = cls._BUFFER.getvalue()
        cls._BUFFER = io.StringIO()  # Reset

        if content:
            cls.write(content, 'stdout')  # Flush to original stdout


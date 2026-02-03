# Path: core/lsp/base/state.py
# ---------------------------
import threading
from enum import Enum
from typing import Optional

class ServerState(str, Enum):
    """
    =============================================================================
    == THE PHASES OF BEING (STOCHASTIC STATE MACHINE)                          ==
    =============================================================================
    """
    DORMANT = "DORMANT"           # Process manifest, mind cold
    AWAKENING = "AWAKENING"       # Handshake in progress
    ACTIVE = "ACTIVE"             # Neural lattice hot
    DRAINING = "DRAINING"         # Finishing active rites before dissolution
    SHUTDOWN = "SHUTDOWN"         # Mind dissolving
    VOID = "VOID"                 # Terminated

class RequestContext(threading.local):
    """
    =============================================================================
    == THE CAUSAL ANCHOR (THREAD-LOCAL GNOSIS)                                 ==
    =============================================================================
    Ensures that Trace IDs and metrics survive the jump between the async loop
    and the kinetic worker threads.
    """
    def __init__(self):
        self.trace_id: str = "0xVOID"
        self.start_time: float = 0.0
        self.active_uri: Optional[str] = None
        self.meta: dict = {}
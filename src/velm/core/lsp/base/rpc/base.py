# Path: core/lsp/rpc/base.py
# --------------------------

from pydantic import BaseModel, ConfigDict

class RpcModel(BaseModel):
    """
    [THE ROOT SPIRIT]
    Base configuration for all Gnostic RPC models.
    Enforces strict typing, aliasing, and immutability where needed.
    """
    model_config = ConfigDict(
        populate_by_name=True,      # Accept 'traceId', map to 'trace_id'
        arbitrary_types_allowed=True,
        validate_assignment=True,   # Runtime type checking on mutation
        extra='allow'               # Tolerance for future protocol extensions
    )
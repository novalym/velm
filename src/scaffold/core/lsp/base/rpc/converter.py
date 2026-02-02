# Path: core/lsp/rpc/converter.py
# -------------------------------

import json
from typing import Any, Union, List
from .messages import Request, Notification, Response, JsonRpcMessage


class MessageConverter:
    """
    [THE ALCHEMICAL TRANSMUTER]
    Converts raw Dict/List structures into Pydantic Models.
    Handles Batch requests recursively.
    """

    @staticmethod
    def from_dict(data: Any) -> JsonRpcMessage:
        """
        Takes raw matter (Dict or List) and performs the Rite of Inception.
        """
        # 1. BATCH REQUEST (List)
        if isinstance(data, list):
            if not data:
                raise ValueError("Empty batch")
            # Recursive transmutation for batch items
            return [MessageConverter.from_dict(item) for item in data]  # type: ignore

        if not isinstance(data, dict):
            raise ValueError("Payload must be Object or Array")

        # 2. RESPONSE (Has 'id' and either 'result' or 'error', but NO 'method')
        # [CRITICAL]: We must check for result/error keys explicitly
        if 'id' in data and ('result' in data or 'error' in data) and 'method' not in data:
            return Response.model_validate(data)

        # 3. REQUEST (Has 'id' and 'method')
        if 'id' in data and 'method' in data:
            return Request.model_validate(data)

        # 4. NOTIFICATION (Has 'method' but NO 'id')
        if 'method' in data and 'id' not in data:
            return Notification.model_validate(data)

        # 5. EXCEPTION: AMORPHOUS MATTER
        # If we reach here, the packet is profane.
        raise ValueError(
            f"Profane Packet: Keys {list(data.keys())} do not align with Gnostic Law."
        )



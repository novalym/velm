# Path: scaffold/artisans/services/twilio/simulation/physics.py
# -------------------------------------------------------------

import random
import time
from typing import Tuple, Optional


class CarrierPhysics:
    """
    [THE LAWS OF THE ETHER]
    Simulates Network Latency, Congestion, and Carrier Filtering.
    """

    # Trigger words that cause specific failures
    CHAOS_TRIGGERS = {
        "FAIL_30007": (30007, "Carrier Violation: Message Content Filtered"),
        "FAIL_30005": (30005, "Carrier Violation: Unknown Destination"),
        "FAIL_30003": (30003, "Unreachable Destination (Handset Off)"),
        "FAIL_21610": (21610, "The Blacklist: User has opted out (STOP)"),
        "FAIL_500": (500, "Twilio Internal Server Error (Simulation)"),
    }

    @classmethod
    def calculate_latency(cls, body_len: int, media_count: int) -> float:
        """
        Calculates realistic transmission delay.
        Base: 100ms.
        + 10ms per 100 chars.
        + 500ms per media attachment.
        + Random Jitter.
        """
        base = 0.1
        mass_drag = (body_len / 100) * 0.01
        media_drag = media_count * 0.5
        jitter = random.uniform(0.05, 0.2)

        return base + mass_drag + media_drag + jitter

    @classmethod
    def adjudicate_chaos(cls, body: str, to_number: str) -> Optional[Tuple[int, str]]:
        """
        Checks if the message triggers a simulated carrier failure.
        """
        # 1. Content Triggers
        if body:
            for trigger, (code, msg) in cls.CHAOS_TRIGGERS.items():
                if trigger in body:
                    return code, msg

        # 2. Number Triggers (Magic Numbers)
        # Ends in 0000 -> Delivery Failure
        if to_number.endswith("0000"):
            return 30008, "Unknown Delivery Failure"

        # Ends in 6666 -> Filtered
        if to_number.endswith("6666"):
            return 30007, "Content Filtered"

        return None
# Path: core/runtime/engine/execution/retry.py
# --------------------------------------------

import time
import random
from typing import Callable, TypeVar

T = TypeVar("T")


class ResiliencePolicy:
    """
    =============================================================================
    == THE PHOENIX POLICY (V-Ω-RETRY-LOGIC)                                    ==
    =============================================================================
    Strategies for overcoming transient entropy.
    """

    @staticmethod
    def exponential_backoff(
            func: Callable[[], T],
            max_retries: int = 3,
            base_delay: float = 0.5,
            max_delay: float = 5.0,
            exceptions: tuple = (Exception,)
    ) -> T:
        """
        Retries the function with exponential backoff + jitter.
        """
        attempt = 0
        while True:
            try:
                return func()
            except exceptions as e:
                attempt += 1
                if attempt > max_retries:
                    raise e

                # Calculate Delay: base * 2^attempt + jitter
                delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                jitter = random.uniform(0, 0.1 * delay)
                total_delay = delay + jitter

                time.sleep(total_delay)
# Path: scaffold/artisans/distillation/assembler/budget.py
# --------------------------------------------------------

from .....core.cortex.tokenomics import TokenEconomist

class TokenAccountant:
    """
    =============================================================================
    == THE TOKEN ACCOUNTANT (V-Ω-PRECISE-LEDGER)                               ==
    =============================================================================
    Manages the budget of the distillation.
    Ensures the AI Context Window is never breached.
    """

    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.current_tokens = 0
        self.economist = TokenEconomist()

    def can_afford(self, text: str) -> bool:
        """Checks if the text fits in the remaining budget."""
        cost = self.estimate(text)
        return (self.current_tokens + cost) <= self.max_tokens

    def charge(self, text: str) -> int:
        """Records the cost of the text."""
        cost = self.estimate(text)
        self.current_tokens += cost
        return cost

    def estimate(self, text: str) -> int:
        """Delegates to the Economist."""
        return self.economist.estimate_cost(text)

    @property
    def remaining(self) -> int:
        return max(0, self.max_tokens - self.current_tokens)
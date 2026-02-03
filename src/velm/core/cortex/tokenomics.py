# Path: scaffold/core/cortex/tokenomics
# --------------------------------------------------

# Try to import tiktoken, handle failure gracefully
try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False


class TokenEconomist:
    """
    The Guardian of the Budget.
    Estimates the cognitive cost of a scripture.
    """

    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self._encoder = None
        if TIKTOKEN_AVAILABLE:
            try:
                self._encoder = tiktoken.encoding_for_model(model)
            except:
                self._encoder = tiktoken.get_encoding("cl100k_base")

    def estimate_cost(self, text: str) -> int:
        """
        Calculates the token cost.
        If tiktoken is missing, uses a heuristic (4 chars ~= 1 token).
        """
        if not text:
            return 0

        if self._encoder:
            try:
                # Encode overhead is minimal, but we catch errors to be safe
                return len(self._encoder.encode(text))
            except Exception:
                pass

        # The Heuristic Fallback
        return len(text) // 4
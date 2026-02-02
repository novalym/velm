# Path: scaffold/symphony/conductor_core/handlers/state_handler/utils/time_parser.py
# ----------------------------------------------------------------------------------
class TimeParser:
    """
    =============================================================================
    == THE TIMEKEEPER (V-Ω-CHRONOMETRIC-PARSER)                                ==
    =============================================================================
    """
    @staticmethod
    def parse_seconds(duration_str: str) -> float:
        """Parses 100ms, 5s, 1m into float seconds."""
        s = duration_str.strip().lower()
        try:
            if s.endswith('ms'):
                return float(s[:-2]) / 1000
            elif s.endswith('s'):
                return float(s[:-1])
            elif s.endswith('m'):
                return float(s[:-1]) * 60
            elif s.endswith('h'):
                return float(s[:-1]) * 3600
            else:
                return float(s)
        except ValueError:
            raise ValueError(f"Invalid temporal duration: '{duration_str}'")
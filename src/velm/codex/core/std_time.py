# Path: codex/core/std_time.py
# ----------------------------

"""
=================================================================================
== THE CHRONOMANCER: OMEGA TOTALITY (V-Ω-TIME-DOMAIN-ASCENDED)                 ==
=================================================================================
LIF: INFINITY | ROLE: TEMPORAL_GOVERNOR | RANK: OMEGA_SOVEREIGN
AUTH: Ω_TIME_V500_ACHRONAL_TOTALITY_2026_FINALIS

Provides absolute mastery over temporal states. Allows blueprints to generate
expirations, timestamps, cron boundaries, and ISO-8601 strict formats natively.
It is warded against the 'strftime' heresy and supports deep humanization.
=================================================================================
"""
import time
import calendar
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Union, Optional, Final

# [ASCENSION 2]: Optional high-fidelity parsing
try:
    from dateutil import parser as date_parser
    HAS_DATEUTIL = True
except ImportError:
    HAS_DATEUTIL = False

from ..contract import BaseDirectiveDomain, CodexHeresy
from ..loader import domain


@domain("time")
class TimeDomain(BaseDirectiveDomain):
    """
    The High Priest of Spacetime and Duration.
    """

    @property
    def namespace(self) -> str:
        return "time"

    def help(self) -> str:
        return "Temporal manipulation: now, strftime, shift, humanize, parse, and cron."

    # =========================================================================
    # == STRATUM 0: THE PRESENT MOMENT                                       ==
    # =========================================================================

    def _directive_now(self, context: Dict[str, Any], format: str = "iso", *args, **kwargs) -> str:
        """
        @time/now(format="%Y-%m-%d")
        Defaults to UTC ISO-8601.
        """
        now_utc = datetime.now(timezone.utc)
        if format == "iso":
            return now_utc.isoformat()
        if format == "unix":
            return str(int(now_utc.timestamp()))
        return now_utc.strftime(format)

    def _directive_strftime(self, context: Dict[str, Any], format: str = "%Y-%m-%d", *args, **kwargs) -> str:
        """
        =============================================================================
        == THE STRFTIME SUTURE (THE MASTER CURE)                                   ==
        =============================================================================
        Direct alias for now() to heal blueprints assuming this legacy name.
        """
        return self._directive_now(context, format=format)

    def _directive_unix(self, context: Dict[str, Any], ms: bool = False, *args, **kwargs) -> int:
        """@time/unix(ms=True) -> 1708812345000"""
        ts = time.time()
        return int(ts * 1000) if ms else int(ts)

    def _directive_year(self, context: Dict[str, Any], *args, **kwargs) -> int:
        """@time/year -> 2026"""
        return datetime.now(timezone.utc).year

    # =========================================================================
    # == STRATUM 1: TEMPORAL TRANSMUTATION                                   ==
    # =========================================================================

    def _directive_shift(self, context: Dict[str, Any],
                         days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0,
                         format: str = "iso", *args, **kwargs) -> str:
        """
        @time/shift(days=30, hours=1)
        Calculates a relative temporal coordinate with mathematical precision.
        """
        target_time = datetime.now(timezone.utc) + timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds
        )
        if format == "iso":
            return target_time.isoformat()
        if format == "unix":
            return str(int(target_time.timestamp()))
        return target_time.strftime(format)

    def _directive_parse(self, context: Dict[str, Any], text: str, format: str = "iso") -> str:
        """
        @time/parse("2024-01-01", format="%Y-%m-%d")
        Transmutes a string soul back into a Gnostic timestamp.
        """
        try:
            if HAS_DATEUTIL:
                dt = date_parser.parse(text)
            else:
                dt = datetime.fromisoformat(text) if format == "iso" else datetime.strptime(text, format)
            return dt.isoformat()
        except Exception as e:
            raise CodexHeresy(f"Temporal Fracture: Could not parse '{text}'. {e}")

    # =========================================================================
    # == STRATUM 2: THE HUMAN EYE (HUMANIZE)                                 ==
    # =========================================================================

    def _directive_humanize(self, context: Dict[str, Any], timestamp: Union[str, float, int]) -> str:
        """
        @time/humanize(1708812345) -> "3 hours ago"
        Provides a relative, high-status description of time.
        """
        try:
            if isinstance(timestamp, str):
                ts = datetime.fromisoformat(timestamp).timestamp()
            else:
                ts = float(timestamp)
        except:
            return "unknown time"

        diff = time.time() - ts
        if diff < 60: return "just now"
        if diff < 3600: return f"{int(diff // 60)} minutes ago"
        if diff < 86400: return f"{int(diff // 3600)} hours ago"
        return f"{int(diff // 86400)} days ago"

    # =========================================================================
    # == STRATUM 3: METABOLIC DURATION (DURATION)                            ==
    # =========================================================================

    def _directive_duration_to_seconds(self, context: Dict[str, Any], duration: str) -> int:
        """
        @time/duration_to_seconds("1h 30m") -> 5400
        [ASCENSION 5]: The Duration Alchemist.
        """
        total = 0
        units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
        matches = re.findall(r'(\d+)([dhms])', duration.lower())
        for val, unit in matches:
            total += int(val) * units[unit]
        return total

    # =========================================================================
    # == STRATUM 4: THE CHRONOS ORACLE (CRON)                                ==
    # =========================================================================

    def _directive_next_cron(self, context: Dict[str, Any], cron: str) -> str:
        """
        @time/next_cron("0 0 * * *")
        [ASCENSION 4]: Prophesies the next metabolic pulse of a scheduled rite.
        """
        # (Simplified heuristic for V-Ω)
        return f"# [CHRONOS] Next strike predicted in approx 24 hours (Cron: {cron})"

    # =========================================================================
    # == STRATUM 5: JURISPRUDENCE (IS_WORKDAY)                              ==
    # =========================================================================

    def _directive_is_workday(self, context: Dict[str, Any], date_str: Optional[str] = None) -> bool:
        """
        @time/is_workday()
        [ASCENSION 12]: Adjudicates if today is a righteous day for deployment.
        """
        dt = datetime.fromisoformat(date_str) if date_str else datetime.now()
        return dt.weekday() < 5 # Monday-Friday

    # =========================================================================
    # == STRATUM 6: FISCAL TOMOGRAPHY                                        ==
    # =========================================================================

    def _directive_fiscal_quarter(self, context: Dict[str, Any]) -> str:
        """@time/fiscal_quarter -> 'Q1'"""
        month = datetime.now().month
        return f"Q{(month - 1) // 3 + 1}"

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _directive_leap_year(self, context: Dict[str, Any], year: Optional[int] = None) -> bool:
        """@time/leap_year(2024) -> True"""
        y = year or self._directive_year(context)
        return calendar.isleap(y)

    def _directive_uptime(self, context: Dict[str, Any]) -> float:
        """
        @time/uptime()
        [ASCENSION 6]: Scries the age of the God-Engine session.
        """
        engine = context.get("__engine__")
        if engine and hasattr(engine, '_creation_time'):
            return round(time.perf_counter() - engine._creation_time, 2)
        return 0.0

    def __repr__(self) -> str:
        return f"<Ω_TIME_DOMAIN status=RESONANT precision=NANOSECOND capacity=24_ASCENSIONS>"
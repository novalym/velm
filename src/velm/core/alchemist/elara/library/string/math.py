# Path: core/alchemist/elara/library/string/math.py
# -------------------------------------------------

import math
from typing import Any
from datetime import datetime, timedelta
from ..registry import register_rite


@register_rite("abs")
def abs_rite(value: Any) -> Any:
    try:
        return abs(value)
    except:
        return value


@register_rite("round")
def round_rite(value: Any, precision: int = 0, method: str = 'common') -> Any:
    """[ASCENSION 39]: Advanced Rounding Algorithms (ceil, floor, common)."""
    try:
        val = float(value)
        if method == 'ceil':
            factor = 10 ** precision
            return math.ceil(val * factor) / factor
        elif method == 'floor':
            factor = 10 ** precision
            return math.floor(val * factor) / factor
        return round(val, precision)
    except:
        return value


@register_rite("int")
def int_rite(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))  # Handles string floats gracefully
    except:
        return default


@register_rite("float")
def float_rite(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except:
        return default


@register_rite("min")
def min_rite(value: Any) -> Any:
    try:
        return min(value)
    except:
        return value


@register_rite("max")
def max_rite(value: Any) -> Any:
    try:
        return max(value)
    except:
        return value


@register_rite("sum")
def sum_rite(value: Any, attribute: str = None) -> Any:
    try:
        if attribute:
            return sum(
                float(x.get(attribute)) if isinstance(x, dict) else float(getattr(x, attribute, 0)) for x in value)
        return sum(float(x) for x in value)
    except:
        return 0


@register_rite("clamp")
def clamp_rite(value: Any, floor: Any, ceiling: Any) -> Any:
    """[ASCENSION 12]: The Clamp Governor."""
    try:
        val = float(value)
        return max(float(floor), min(val, float(ceiling)))
    except Exception:
        return value


@register_rite("mean")
@register_rite("avg")
def mean_rite(value: Any) -> float:
    """[ASCENSION 13]: Statistical Gaze."""
    try:
        ls = list(value)
        if not ls: return 0.0
        return sum(float(x) for x in ls) / len(ls)
    except Exception:
        return 0.0


@register_rite("to_base")
def to_base_rite(value: Any, base: int = 16) -> str:
    """[ASCENSION 14]: Base-N Transmuter."""
    try:
        val = int(value)
        if base == 16: return hex(val)
        if base == 2: return bin(val)
        if base == 8: return oct(val)
        return str(val)
    except Exception:
        return str(value)


@register_rite("date")
def date_rite(value: Any, format_str: str = "%Y-%m-%d") -> str:
    """[ASCENSION 40]: Isomorphic DateTime Transmuter."""
    if not value: return ""
    try:
        if str(value).lower() == "now":
            return datetime.now().strftime(format_str)

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value).strftime(format_str)

        if isinstance(value, datetime):
            return value.strftime(format_str)

        if isinstance(value, str):
            # Fallback parsing for standard ISO strings
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return dt.strftime(format_str)

    except Exception:
        pass
    return str(value)


@register_rite("filesizeformat")
def filesizeformat_rite(value: Any, binary: bool = False) -> str:
    """[ASCENSION 9]: File-Size Formatter."""
    try:
        bytes_val = float(value)
        base = 1024 if binary else 1000
        prefixes = ['KiB', 'MiB', 'GiB', 'TiB'] if binary else ['kB', 'MB', 'GB', 'TB']

        if bytes_val == 1:
            return "1 Byte"
        elif bytes_val < base:
            return f"{bytes_val:.0f} Bytes"
        else:
            for i, prefix in enumerate(prefixes):
                unit = base ** (i + 2)
                if bytes_val < unit:
                    return f"{bytes_val / (base ** (i + 1)):.1f} {prefix}"
        return f"{bytes_val / (base ** len(prefixes)):.1f} {prefixes[-1]}"
    except Exception:
        return "0 Bytes"


@register_rite("currency")
def currency_rite(value: Any, symbol: str = "$", decimal_places: int = 2) -> str:
    """[ASCENSION 41]: Fiscal Representation Forge."""
    try:
        val = float(value)
        return f"{symbol}{val:,.{decimal_places}f}"
    except Exception:
        return f"{symbol}0.00"


@register_rite("numberformat")
def numberformat_rite(value: Any, decimal_places: int = 0, grouping: str = ",") -> str:
    """[ASCENSION 42]: Comma-Separated Digit Aligner."""
    try:
        val = float(value)
        format_str = f"{{:{grouping}.{decimal_places}f}}"
        return format_str.format(val)
    except Exception:
        return str(value)


@register_rite("timedelta")
def timedelta_rite(value: Any, format_str: str = "auto") -> str:
    """[ASCENSION 43]: Chronological Delta Translator."""
    try:
        seconds = float(value)
        td = timedelta(seconds=seconds)
        if format_str == "auto":
            return str(td)
        # Custom time formatting logic could expand here
        return str(td)
    except Exception:
        return str(value)


@register_rite("percent")
def percent_rite(value: Any, decimal_places: int = 1) -> str:
    """[ASCENSION 44]: Probability-to-Percentage Transmuter."""
    try:
        return f"{float(value) * 100:.{decimal_places}f}%"
    except Exception:
        return "0%"


@register_rite("ceil")
def ceil_rite(value: Any) -> int:
    try:
        return math.ceil(float(value))
    except:
        return int(value) if str(value).isdigit() else 0


@register_rite("floor")
def floor_rite(value: Any) -> int:
    try:
        return math.floor(float(value))
    except:
        return int(value) if str(value).isdigit() else 0
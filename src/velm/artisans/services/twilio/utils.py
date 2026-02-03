# Path: scaffold/artisans/services/twilio/utils.py
# ------------------------------------------------

import re
import math
from typing import Optional, Tuple
from twilio.base.exceptions import TwilioRestException
from .constants import (
    ERROR_MAP, GSM_CHARSET, SEGMENT_SIZE_GSM,
    SEGMENT_SIZE_GSM_MULTI, SEGMENT_SIZE_UCS2, SEGMENT_SIZE_UCS2_MULTI
)


class TelephonicPhysics:
    """[THE CALCULATOR] Adjudicates message mass and encoding."""

    @staticmethod
    def calculate_segments(body: str) -> Tuple[int, str]:
        """
        Returns (num_segments, encoding_type).
        """
        if not body: return 0, "GSM7"

        is_gsm = all(c in GSM_CHARSET for c in body)
        encoding = "GSM7" if is_gsm else "UCS2"
        length = len(body)

        if is_gsm:
            if length <= SEGMENT_SIZE_GSM: return 1, encoding
            return math.ceil(length / SEGMENT_SIZE_GSM_MULTI), encoding
        else:
            if length <= SEGMENT_SIZE_UCS2: return 1, encoding
            return math.ceil(length / SEGMENT_SIZE_UCS2_MULTI), encoding


class TelephonicAlchemist:
    """[THE PURIFIER] Normalizes data."""

    @staticmethod
    def normalize_e164(number: str, default_country: str = "US") -> Optional[str]:
        if not number: return None
        clean = re.sub(r'(?<!^)\+|[^\d+]', '', str(number).strip())

        if clean.startswith('+'): return clean

        if default_country in ["US", "CA"]:
            if len(clean) == 10: return f"+1{clean}"
            if len(clean) == 11 and clean.startswith('1'): return f"+{clean}"

        return f"+{clean}"

    @staticmethod
    def transmute_error(e: TwilioRestException, context: str = "") -> str:
        heresy = ERROR_MAP.get(e.code, "UNKNOWN_CARRIER_FRACTURE")
        return f"{heresy} ({e.code}): {e.msg} [{context}]"
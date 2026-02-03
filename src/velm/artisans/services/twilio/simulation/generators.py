# Path: scaffold/artisans/services/twilio/simulation/generators.py
# ----------------------------------------------------------------

import uuid
import random
import time
from typing import Dict, Any


class PhantomGenerator:
    """
    [THE DREAM WEAVER]
    Forges high-fidelity hallucinations of Telephonic Data.
    """

    # Gnostic Map of Area Codes to States/Regions
    GEO_MAP = {
        "415": ("CA", "San Francisco"), "212": ("NY", "New York"),
        "512": ("TX", "Austin"), "206": ("TX", "Seattle"),
        "305": ("FL", "Miami"), "702": ("NV", "Las Vegas"),
        "617": ("MA", "Boston"), "312": ("IL", "Chicago"),
        "404": ("GA", "Atlanta"), "202": ("DC", "Washington")
    }

    @staticmethod
    def sid(prefix: str = "SM") -> str:
        """Generates a 34-char Twilio-style SID with entropy."""
        return f"{prefix}{uuid.uuid4().hex}"

    @staticmethod
    def phone_number(area_code: str = "555") -> str:
        """Generates a valid-looking E.164 number."""
        clean_area = "".join(filter(str.isdigit, area_code))
        if not clean_area: clean_area = "555"

        exchange = random.randint(200, 999)
        subscriber = random.randint(1000, 9999)
        return f"+1{clean_area}{exchange}{subscriber}"

    @staticmethod
    def price(base: str) -> str:
        """Adds micro-jitter to price for realism."""
        val = float(base)
        # 10% chance of variance (e.g. Carrier Surcharge)
        if random.random() > 0.9:
            val += 0.0025
        return f"{val:.4f}"

    @classmethod
    def node_metadata(cls, number: str) -> Dict[str, Any]:
        """Divines location data based on Area Code."""
        if len(number) < 4: return {}
        ac = number[2:5]
        state, city = cls.GEO_MAP.get(ac, ("UNK", "Unknown Region"))

        return {
            "phone_number": number,
            "friendly_name": f"({ac}) {number[5:8]}-{number[8:]}",
            "locality": city,
            "region": state,
            "iso_country": "US",
            "capabilities": {"voice": True, "SMS": True, "MMS": True},
            "beta": False
        }
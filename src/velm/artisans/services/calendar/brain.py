# Path: packages/novalym-logic/novalym_logic/artisans/products/calendar/brain.py
# -------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: SYMBOLIC_REASONER | RANK: SOVEREIGN
# =========================================================================================

import datetime
from typing import List, Dict, Any


class TemporalBrain:
    """[THE CHRONOMANCER] Transmutes raw API data into Human Gnosis."""

    def distill_options(self, raw_slots: List[Dict], buffer_mins: int) -> Dict[str, str]:
        """
        [ASCENSION 1 & 9]: ADRENALINE BUFFER & STOCHASTIC SELECTION.
        Filters for human-centric windows and returns A/B map.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        min_start = now + datetime.timedelta(minutes=buffer_mins)

        valid = []
        for slot in raw_slots:
            ts = datetime.datetime.fromisoformat(slot["start"].replace('Z', '+00:00'))
            # 1. Buffer Check
            if ts < min_start: continue
            # 2. Social Window (8am - 6pm local)
            if 8 <= ts.hour <= 18:
                valid.append(ts.isoformat())

        if len(valid) < 2: return {}

        return {
            "A": valid[0],
            "B": valid[1]
        }

    def humanize_slots(self, distilled: Dict[str, str], tz: str) -> List[Dict]:
        """[ASCENSION 4]: Transmutes ISO matter into 'Tomorrow at 2pm' style."""
        res = []
        for key, ts_str in distilled.items():
            dt = datetime.datetime.fromisoformat(ts_str)
            # Formatting logic (simplified for manifest)
            label = f"{dt.strftime('%A')} at {dt.strftime('%I:%M %p')}"
            res.append({"id": key, "human": label})
        return res
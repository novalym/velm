# // scaffold/artisans/translocate_core/resolvers/rust/surgeon.py
# ---------------------------------------------------------------

from typing import List
from .....logger import Scribe
from .contracts import RustHealingEdict

Logger = Scribe("RustSurgeon")


class RustSurgeon:
    def heal(self, content: str, plan: List[RustHealingEdict]) -> str:
        if not plan: return content
        data = bytearray(content, 'utf-8')
        sorted_plan = sorted(plan, key=lambda x: x.start_byte, reverse=True)

        for edict in sorted_plan:
            new_bytes = edict.new_path.encode('utf-8')
            data[edict.start_byte:edict.end_byte] = new_bytes
            Logger.verbose(f"   -> Rewrote: {edict.original_path} -> {edict.new_path}")

        return data.decode('utf-8')
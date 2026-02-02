# // scaffold/artisans/translocate_core/resolvers/cpp/surgeon.py
# --------------------------------------------------------------

from typing import List
from .....logger import Scribe
from .contracts import CppHealingEdict

Logger = Scribe("CppSurgeon")


class CppSurgeon:
    def heal(self, content: str, plan: List[CppHealingEdict]) -> str:
        if not plan: return content
        data = bytearray(content, 'utf-8')

        sorted_plan = sorted(plan, key=lambda x: x.start_byte, reverse=True)

        for edict in sorted_plan:
            # Edict new_path already includes quotes/brackets
            new_bytes = edict.new_path.encode('utf-8')
            data[edict.start_byte:edict.end_byte] = new_bytes
            Logger.verbose(f"   -> Rewrote: {edict.original_path} -> {edict.new_path}")

        return data.decode('utf-8')
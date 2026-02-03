# // scaffold/artisans/translocate_core/resolvers/java/surgeon.py
# ---------------------------------------------------------------

from typing import List
from .....logger import Scribe
from .contracts import JavaHealingEdict

Logger = Scribe("JavaSurgeon")


class JavaSurgeon:
    def heal(self, content: str, plan: List[JavaHealingEdict]) -> str:
        if not plan: return content
        data = bytearray(content, 'utf-8')

        # Reverse order to preserve offsets
        sorted_plan = sorted(plan, key=lambda x: x.start_byte, reverse=True)

        for edict in sorted_plan:
            new_bytes = edict.new_path.encode('utf-8')
            data[edict.start_byte:edict.end_byte] = new_bytes
            Logger.verbose(f"   -> Rewrote: {edict.original_path} -> {edict.new_path}")

        return data.decode('utf-8')
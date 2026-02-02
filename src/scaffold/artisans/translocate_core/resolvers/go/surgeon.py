# // scaffold/artisans/translocate_core/resolvers/go/surgeon.py
from typing import List
from .contracts import GoHealingEdict


class GoSurgeon:
    def heal(self, content: str, plan: List[GoHealingEdict]) -> str:
        if not plan: return content
        data = bytearray(content, "utf-8")

        # Reverse order to preserve offsets
        for edict in sorted(plan, key=lambda x: x.start_byte, reverse=True):
            # Go imports are double-quoted
            new_bytes = f'"{edict.new_path}"'.encode("utf-8")
            data[edict.start_byte:edict.end_byte] = new_bytes

        return data.decode("utf-8")
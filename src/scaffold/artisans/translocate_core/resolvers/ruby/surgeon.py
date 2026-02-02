# // scaffold/artisans/translocate_core/resolvers/ruby/surgeon.py
# ---------------------------------------------------------------

from typing import List
from .....logger import Scribe
from .contracts import RubyHealingEdict

Logger = Scribe("RubySurgeon")


class RubySurgeon:
    """
    Performs byte-level surgery on Ruby scriptures.
    """

    def heal(self, content: str, plan: List[RubyHealingEdict]) -> str:
        if not plan: return content

        # Work with bytes for precision
        data = bytearray(content, 'utf-8')

        # Reverse order to preserve offsets
        sorted_plan = sorted(plan, key=lambda x: x.start_byte, reverse=True)

        for edict in sorted_plan:
            new_bytes = edict.new.encode('utf-8')
            # We replace the content INSIDE the quotes
            data[edict.start_byte:edict.end_byte] = new_bytes

            Logger.verbose(f"   -> Spliced L{edict.line_num}: {edict.original} -> {edict.new}")

        return data.decode('utf-8')
# // scaffold/artisans/translocate_core/resolvers/javascript/surgeon.py
# ---------------------------------------------------------------------

from typing import List
from .....logger import Scribe
from .contracts import JSHealingEdict

Logger = Scribe("JSSurgeon")


class JSSurgeon:
    """
    Performs byte-level surgery on the source code.
    Using AST for JS is hard in Python; Byte Splicing via Tree-sitter ranges is precise.
    """

    def heal(self, content: str, plan: List[JSHealingEdict]) -> str:
        if not plan: return content

        # Work with bytes to ensure index accuracy
        data = bytearray(content, 'utf-8')

        # Apply edits in reverse order so offsets don't shift
        # Sort by start_byte descending
        sorted_plan = sorted(plan, key=lambda x: x.start_byte, reverse=True)

        for edict in sorted_plan:
            # Construct the replacement string (preserving quotes)
            # Tree-sitter node.text includes quotes.
            # Edict has original_specifier (inner) and quote_style

            # However, start_byte/end_byte from Inquisitor INCLUDES quotes for string nodes?
            # Let's check inquisitor. It captures @src (string). Yes, includes quotes.

            new_bytes = f"{edict.quote_style}{edict.new_specifier}{edict.quote_style}".encode('utf-8')

            # Splice
            data[edict.start_byte:edict.end_byte] = new_bytes

            Logger.verbose(f"   -> Spliced {edict.original_specifier} -> {edict.new_specifier}")

        return data.decode('utf-8')
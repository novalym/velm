# Path: parser_core/logic_weaver/state/alchemy.py
# -----------------------------------------------

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import GnosticContext


class TruthPurifier:
    """
    =============================================================================
    == THE TRUTH PURIFIER (V-Ω-TYPE-SOVEREIGN-ALCHEMIST)                       ==
    =============================================================================
    Scans the raw, untyped strings provided by the Architect and transmutes
    them into absolute Pythonic logic (Booleans, Integers).
    """

    __slots__ = ('ctx',)

    def __init__(self, ctx: 'GnosticContext'):
        self.ctx = ctx

    def purify(self):
        """
        [ASCENSION 4 & 5]: APOPHATIC TRUTH FILTERING.
        Transmutes string truths into logical bits in-place, armed against
        type-casting paradoxes.
        """
        for k, v in list(self.ctx._context.items()):
            if isinstance(v, str):
                lower_v = v.lower().strip()

                # Thaw Booleans
                if lower_v in ('true', 'yes', '1', 'on', 'resonant'):
                    self.ctx._context[k] = True
                elif lower_v in ('false', 'no', '0', 'off', 'fractured'):
                    self.ctx._context[k] = False

                # Thaw Numbers
                elif lower_v.isdigit():
                    try:
                        self.ctx._context[k] = int(lower_v)
                    except ValueError:
                        pass  # Retain as string if int coercion fractures
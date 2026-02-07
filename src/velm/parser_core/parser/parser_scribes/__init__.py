# Path: src/velm/parser_core/parser/parser_scribes/__init__.py
# ------------------------------------------------------------

"""
=================================================================================
== THE LIVING GRIMOIRE OF SCRIBES (V-Ω-ETERNAL-APOTHEOSIS)                     ==
=================================================================================
This sacred scripture is now the living, self-aware mind of the Scribe Pantheon.
It contains the SCRIBE_PANTHEON, the one true, declarative map that teaches the
ApotheosisParser which Scribes to summon for each Gnostic tongue.

To teach the parser a new grammar, one must only inscribe it here.
=================================================================================
"""
from ....contracts.data_contracts import GnosticLineType
from ....contracts.symphony_contracts import EdictType
from .base_scribe import FormScribe

# --- The Scribes of Form (.scaffold) ---
from .scaffold_scribes import (
    CommentScribe,
    ContractScribe,
    DirectiveScribe,
    JinjaScribe,
    MakefileScribe,
    PostRunScribe,
    StructuralScribe,
    VariableScribe,
    OnUndoScribe,
    OnHeresyScribe  # <--- THE NEW GUARDIAN OF REDEMPTION
)

# --- The Scribes of Will (.symphony) ---
from .symphony_scribes import (
    SymphonyAtomicScribe,
    SymphonyCommunionScribe,
    SymphonyDirectiveScribe,
    SymphonyLogicScribe,
    SymphonyParallelScribe,
    SymphonyPolyglotScribe
)

# =================================================================================
# == THE SACRED GRIMOIRE (THE DECLARATIVE MIND)                                  ==
# =================================================================================
SCRIBE_PANTHEON = {
    "scaffold": {
        # The Gaze is upon the LineType's Soul
        GnosticLineType.COMMENT: CommentScribe,
        GnosticLineType.VARIABLE: VariableScribe,
        GnosticLineType.LOGIC: DirectiveScribe,
        GnosticLineType.POST_RUN: PostRunScribe,
        GnosticLineType.FORM: StructuralScribe,
        GnosticLineType.CONTRACT_DEF: ContractScribe,
        GnosticLineType.JINJA_CONSTRUCT: JinjaScribe,
        GnosticLineType.TRAIT_DEF: StructuralScribe,
        GnosticLineType.TRAIT_USE: StructuralScribe,

        # The Laws of Reversal and Redemption
        GnosticLineType.ON_UNDO: OnUndoScribe,
        GnosticLineType.ON_HERESY: OnHeresyScribe,  # <--- MAPPED AND VIGILANT
    },
    "symphony": {
        # The Gaze is first upon the Edict's Soul (Highest Precedence)
        EdictType.ACTION: SymphonyAtomicScribe,
        EdictType.VOW: SymphonyAtomicScribe,
        EdictType.STATE: SymphonyAtomicScribe,
        EdictType.BREAKPOINT: SymphonyAtomicScribe,
        EdictType.CONDITIONAL: SymphonyLogicScribe,
        EdictType.LOOP: SymphonyDirectiveScribe,
        EdictType.RESILIENCE: SymphonyDirectiveScribe,
        EdictType.PARALLEL_RITE: SymphonyParallelScribe,
        EdictType.DIRECTIVE: SymphonyDirectiveScribe,
        EdictType.POLYGLOT_ACTION: SymphonyPolyglotScribe,

        # The Gaze falls back to the LineType's Soul for non-Edict Gnosis
        GnosticLineType.COMMENT: CommentScribe,
    }
}
# =================================================================================

__all__ = list(SCRIBE_PANTHEON.keys())  # Proclaim the known grammars
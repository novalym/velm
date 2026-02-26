# Path: src/velm/parser_core/parser/parser_scribes/__init__.py
# ------------------------------------------------------------

"""
=================================================================================
== THE LIVING GRIMOIRE OF SCRIBES (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)              ==
=================================================================================
@gnosis:title The Scribe Pantheon
@gnosis:summary The declarative map of all specialized perception artisans.
@gnosis:LIF INFINITY

This sacred scripture is the living, self-aware mind of the Scribe Pantheon.
It maps the `GnosticLineType` and `EdictType` to their respective Sovereign
Guardians, ensuring perfect delegation of parsing logic.
=================================================================================
"""
from ....contracts.data_contracts import GnosticLineType
from ....contracts.symphony_contracts import EdictType
from .base_scribe import FormScribe

# --- The Scribes of Form (.scaffold) ---
from .scaffold_scribes import (
    CommentScribe,
    ContractScribe,
    ScaffoldDirectiveScribe,
    JinjaScribe,
    MakefileScribe,
    PostRunScribe,
    StructuralScribe,
    VariableScribe,
    OnUndoScribe,
    OnHeresyScribe
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
        GnosticLineType.LOGIC: ScaffoldDirectiveScribe,
        GnosticLineType.FORM: StructuralScribe,
        GnosticLineType.CONTRACT_DEF: ContractScribe,
        GnosticLineType.JINJA_CONSTRUCT: JinjaScribe,
        GnosticLineType.TRAIT_DEF: StructuralScribe,
        GnosticLineType.TRAIT_USE: StructuralScribe,

        # [THE AST SUTURE]: The Trinity of Will
        # These scribes act as Structural Anchors, allowing the AST Weaver to build
        # the true hierarchy of execution.
        GnosticLineType.POST_RUN: PostRunScribe,
        GnosticLineType.ON_UNDO: OnUndoScribe,
        GnosticLineType.ON_HERESY: OnHeresyScribe,

        # [THE AST SUTURE]: The Atoms of Execution
        # VOW nodes (>> commands) are handled by the PostRunScribe as Leaf Nodes.
        GnosticLineType.VOW: PostRunScribe,
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
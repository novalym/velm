# Path: parser_core/logic_weaver/traversal/walker.py
# --------------------------------------------------

from pathlib import Path

from .context import SpacetimeContext
from .evaluator import LogicAdjudicator
from .mason import GeometricMason
from .reaper import KineticReaper
from ..contracts import LogicScope
from ....contracts.data_contracts import _GnosticNode, GnosticLineType
from ....logger import Scribe

Logger = Scribe("DimensionalWalker")


class DimensionalWalker:
    """
    =============================================================================
    == THE DIMENSIONAL WALKER (V-Ω-TOTALITY-V15000-UNBREAKABLE)                ==
    =============================================================================
    LIF: ∞ | ROLE: RECURSIVE_ORCHESTRATOR | RANK: OMEGA_SUPREME

    The orchestrator of the graph traversal. It visits every node, consults the
    LogicAdjudicator to manage the Scope, and delegates to the Mason and Reaper
    to harvest the manifest reality.
    """

    MAX_RECURSION_DEPTH = 100

    def __init__(self, ctx: SpacetimeContext):
        self.ctx = ctx
        self.adjudicator = LogicAdjudicator(ctx)
        self.mason = GeometricMason(ctx)
        self.reaper = KineticReaper(ctx)

    def walk(self, node: _GnosticNode, current_path: Path, ctx: SpacetimeContext, parent_visible: bool = True,
             depth: int = 0, breadcrumb: str = "ROOT"):
        """
        The Core Recursive Loop.
        """
        # [ASCENSION 22]: Cyclic Depth Guard
        if depth > self.MAX_RECURSION_DEPTH:
            Logger.error(f"Recursion Limit Exceeded at {breadcrumb}. The Tree is Ouroboric.")
            return

        # [ASCENSION 19]: Strict Order Preservation
        sorted_children = sorted(
            node.children,
            key=lambda c: c.item.line_num if c.item else 0
        )

        # Every level of the AST hierarchy requires its own LogicScope
        # to manage the state machine of sibling if/elif/else chains.
        scope = LogicScope(parent_visible=parent_visible)

        for child in sorted_children:
            child_name = child.name or "?"
            new_breadcrumb = f"{breadcrumb} > {child_name}"

            # --- CASE 1: FORM NODES WITHOUT EXPLICIT ITEMS (Implicit Dirs) ---
            if not child.item:
                if scope.parent_visible:
                    next_path = self.mason.forge_matter(child, current_path)
                    self.walk(child, next_path, ctx, parent_visible=True, depth=depth + 1, breadcrumb=new_breadcrumb)
                continue

            line_type = child.item.line_type

            # --- CASE 2: LOGIC & TEMPLATES ---
            if line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT):
                ctx.visibility_map[child.item.line_num] = scope.parent_visible

                # If the parent branch is dead, all children are dead.
                if not scope.parent_visible:
                    child.logic_result = False
                    self.walk(child, current_path, ctx, parent_visible=False, depth=depth + 1,
                              breadcrumb=new_breadcrumb)
                    continue

                # The Adjudicator determines if this specific block is resonant
                should_enter = self.adjudicator.evaluate_gate(child, scope)
                self.walk(child, current_path, ctx, parent_visible=should_enter, depth=depth + 1,
                          breadcrumb=new_breadcrumb)

            # --- CASE 3: CAUSAL BLOCKS (ON_HERESY / ON_UNDO / POST_RUN) ---
            elif line_type in (GnosticLineType.POST_RUN, GnosticLineType.ON_HERESY, GnosticLineType.ON_UNDO):
                ctx.visibility_map[child.item.line_num] = scope.parent_visible

                if scope.parent_visible:
                    # If it's a standard POST_RUN, we just walk into it naturally
                    if line_type == GnosticLineType.POST_RUN:
                        self.walk(child, current_path, ctx, parent_visible=True, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)

                    # [ASCENSION 1 & 5]: If it's a causal block, the Reaper handles it via Isolated Timelines
                    else:
                        self.reaper.attach_causal_block(child, line_type, self)

            # --- CASE 4: THE ATOM OF WILL (VOW) ---
            elif line_type == GnosticLineType.VOW:
                ctx.visibility_map[child.item.line_num] = scope.parent_visible
                if scope.parent_visible:
                    self.reaper.harvest_vow(child.item)

                    # VOWs can technically have children if they are legacy or structured oddly.
                    # We walk them just in case.
                    self.walk(child, current_path, ctx, parent_visible=True, depth=depth + 1, breadcrumb=new_breadcrumb)

            # --- CASE 5: THE ATOM OF MATTER (FORM) ---
            elif line_type == GnosticLineType.FORM:
                # Catch legacy POST_RUN items masquerading as FORM
                if hasattr(child.item, 'edict_type') and child.item.edict_type is not None:
                    if scope.parent_visible:
                        edict_soul = ctx.parser_edicts.get(child.item.line_num)
                        if edict_soul:
                            ctx.edicts.append(edict_soul)
                else:
                    if scope.parent_visible:
                        next_path = self.mason.forge_matter(child, current_path)
                        self.walk(child, next_path, ctx, parent_visible=True, depth=depth + 1,
                                  breadcrumb=new_breadcrumb)
                    else:
                        ctx.visibility_map[child.item.line_num] = False

            # --- CASE 6: METADATA & COMMENTS ---
            else:
                if child.item.line_num > 0:
                    ctx.visibility_map[child.item.line_num] = scope.parent_visible
# Path: parser_core/logic_weaver/traversal/reaper.py
# --------------------------------------------------

import json
from pathlib import Path
from typing import List, Optional, Any

from .context import SpacetimeContext
from ....contracts.data_contracts import _GnosticNode, ScaffoldItem, GnosticLineType
from ....logger import Scribe

Logger = Scribe("KineticReaper")


class KineticReaper:
    """
    =============================================================================
    == THE KINETIC REAPER (V-Ω-CAUSAL-SUTURE-ULTIMA)                           ==
    =============================================================================
    Harvests VOW nodes and legacy POST_RUN commands.
    It is the master of Reverse-Causality, capable of attaching ON_HERESY and
    ON_UNDO blocks to their rightful parent commands by spawning Isolated Timelines.
    """

    def __init__(self, ctx: SpacetimeContext):
        self.ctx = ctx

    def harvest_vow(self, item: ScaffoldItem):
        """
        [THE RITE OF HARVEST]
        Reconstructs the pure command and appends it to the global command buffer.
        """
        self.ctx.visibility_map[item.line_num] = True
        cmd = self._reconstruct_kinetic_will(item)

        # We append a fresh 4-tuple. Sibling ON_HERESY/ON_UNDO nodes
        # will update the Undo/Heresy slots in subsequent walk iterations.
        self.ctx.post_run_commands.append((cmd, item.line_num, None, None))
        # Logger.verbose(f"L{item.line_num}: Harvested Vow -> {cmd[:30]}...")

    def harvest_legacy_post_run(self, node: _GnosticNode):
        """Handles older serialized arrays of line numbers."""
        if not node.item or not node.item.content:
            return

        if node.item.content.startswith('[') and node.item.content.endswith(']'):
            try:
                command_line_numbers = json.loads(node.item.content)
                for line_num in command_line_numbers:
                    command_tuple = self.ctx.parser_post_run.get(line_num)
                    if command_tuple:
                        self.ctx.post_run_commands.append(command_tuple)
            except (json.JSONDecodeError, TypeError):
                pass

    def attach_causal_block(self, block_node: _GnosticNode, block_type: GnosticLineType, walker: Any):
        """
        =============================================================================
        == THE ISOLATED TIMELINE SUTURE (THE ABSOLUTE CURE)                        ==
        =============================================================================
        [ASCENSION 1 & 5]: Instead of parsing strings, we spawn an Isolated Timeline
        (a sub-context) and tell the Walker to process the subtree natively.
        This guarantees that @if logic inside rollbacks is flawlessly evaluated.
        """
        if not self.ctx.post_run_commands:
            Logger.warn(f"Orphaned {block_node.item.line_type.name} block at L{block_node.item.line_num} ignored.")
            return

        # 1. Spawn the Sub-Context
        isolated_ctx = self.ctx.spawn_isolated_timeline()

        # 2. Command the Walker to traverse the block natively
        # Note: We pass parent_visible=True because the block ITSELF is verified visible by the parent
        walker.walk(block_node, Path("."), isolated_ctx, parent_visible=True)

        # 3. Harvest the resulting pure commands
        # isolated_ctx.post_run_commands contains the 4-tuples. We just want the string commands.
        block_cmds = [cmd[0] for cmd in isolated_ctx.post_run_commands]

        if not block_cmds:
            return

        # 4. Attach to the LAST command emitted in the main timeline
        last_cmd = self.ctx.post_run_commands.pop()

        # The Quaternity: (Cmd, Line, Undo, Heresy)
        if block_type == GnosticLineType.ON_HERESY:
            new_cmd = (last_cmd[0], last_cmd[1], last_cmd[2], block_cmds)
        else:  # ON_UNDO
            new_cmd = (last_cmd[0], last_cmd[1], block_cmds, last_cmd[3])

        self.ctx.post_run_commands.append(new_cmd)
        # Logger.verbose(f"L{block_node.item.line_num}: Attached {len(block_cmds)} causal commands to L{last_cmd[1]}")

    def _reconstruct_kinetic_will(self, item: ScaffoldItem) -> str:
        """
        [ASCENSION 4]: THE KINETIC ALCHEMIST.
        Re-weaves the pure command string with its semantic modifiers,
        ensuring the Maestro receives the exact, original intent that was peeled
        by the PostRunScribe during the initial parsing phase.
        """
        cmd = item.content
        meta = item.semantic_selector or {}

        if not meta:
            return cmd

        # 1. Prefix Modifiers
        if meta.get("retry"):
            cmd = f"retry({meta['retry']}): {cmd}"
        if meta.get("allow_fail"):
            cmd = f"allow_fail: {cmd}"

        # 2. Postfix Modifiers
        if meta.get("capture_as"):
            cmd = f"{cmd} as {meta['capture_as']}"
        if meta.get("adjudicator_type"):
            cmd = f"{cmd} using {meta['adjudicator_type']}"
        if meta.get("timeout"):
            cmd = f"{cmd} timeout({meta['timeout']})"
        if meta.get("env_overrides"):
            env_str = ",".join([f"{k}={v}" for k, v in meta["env_overrides"].items()])
            cmd = f"{cmd} env({env_str})"

        return cmd
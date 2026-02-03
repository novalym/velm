# Path: scaffold/symphony/conductor_core/handlers/logic_handler.py
# ----------------------------------------------------------------
from .base import BaseHandler
from ....contracts.symphony_contracts import Edict
from ....contracts.heresy_contracts import ArtisanHeresy


class LogicHandler(BaseHandler):
    """
    =================================================================================
    == THE MIND OF FLOW (V-Ω-BRANCHING-LOGIC)                                      ==
    =================================================================================
    LIF: 10,000,000,000

    The Master of Control Flow.
    Handles `@if`, `@for`, `@filter`.
    """

    def execute_conditional(self, edict: Edict):
        """The Fork in the Road."""
        resolved_condition = self.alchemist.transmute(edict.command, self.context)

        # [ELEVATION 1] The Adjudicator's Gaze
        is_true = self.adjudicator.judge_condition(resolved_condition)

        self.logger.verbose(f"L{edict.line_num}: @if '{resolved_condition}' adjudicated as {is_true}")

        if is_true:
            # Callback to the Engine to execute the body
            self.engine._execute_block(edict.body)
        elif edict.else_body:
            self.engine._execute_block(edict.else_body)

    def execute_loop(self, edict: Edict):
        """The Rite of Eternal Return (@for)."""
        loop_var = edict.capture_as
        list_expr = edict.command

        # Transmute the list expression to get the iterable
        iterable = self.alchemist.transmute(f"{{{{ {list_expr} }}}}", self.context)

        # [ELEVATION 2] Robust Iterable Parsing
        if not isinstance(iterable, list):
            if isinstance(iterable, str):
                # Split comma-separated strings automatically
                iterable = [x.strip() for x in iterable.split(',') if x.strip()]
            else:
                raise ArtisanHeresy(f"Loop Heresy: '{list_expr}' did not resolve to a list.", line_num=edict.line_num)

        original_context_value = self.context.get(loop_var)

        # [ELEVATION 3] The Loop Context Injection
        for i, item in enumerate(iterable):
            self.context[loop_var] = item
            self.context['loop'] = {
                'index': i,
                'index0': i,
                'index1': i + 1,
                'first': i == 0,
                'last': i == len(iterable) - 1,
                'length': len(iterable)
            }
            self.engine._execute_block(edict.body)

        # Restore original context to prevent side-effects
        if original_context_value is None:
            self.context.pop(loop_var, None)
        else:
            self.context[loop_var] = original_context_value
        self.context.pop('loop', None)

    def execute_filter(self, edict: Edict):
        """The Alchemical Sieve (@filter)."""
        target_var = edict.capture_as
        condition_expr = edict.command

        raw_list = self.context.get(target_var)
        if not isinstance(raw_list, list):
            self.logger.warn(f"Filter Heresy: Target '{target_var}' is not a list. It cannot be sieved.")
            return

        filtered_list = []
        for item in raw_list:
            # Create a temporary context for the filter condition
            eval_context = self.context.copy()
            eval_context['item'] = item

            if self.adjudicator.judge_condition(condition_expr, eval_context):
                filtered_list.append(item)

        self.context[target_var] = filtered_list
        self.logger.info(f"Filtered '{target_var}': {len(raw_list)} -> {len(filtered_list)} items.")
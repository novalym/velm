# scaffold/studio/pads/distill_pad/widgets/config_pane.py

import asyncio
from typing import Union, Optional

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.timer import Timer
from textual.widgets import Static, Input, RadioSet, RadioButton, Label

from ..state import ConfigChanged, DistillConfig
from ....logger import Scribe


class ConfigPane(VerticalScroll):
    """The Altar of Will."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scribe = Scribe("ConfigPane")
        # [FIX] Type hint for Textual Timer
        self._config_change_timer: Optional[Timer] = None

    def compose(self) -> ComposeResult:
        with Static(classes="config-group") as vs:
            vs.border_title = "Token Budget"
            with RadioSet(id="budget-radioset"):
                yield RadioButton("Hawk (~50k)", id="budget-hawk")
                yield RadioButton("Sage (~150k)", id="budget-sage")
                yield RadioButton("Cosmos (~500k)", id="budget-cosmos")
                yield RadioButton("Infinite", id="budget-infinite")
                yield RadioButton("Custom", id="budget-custom")
            yield Input(placeholder="e.g., 200k, 1.2m", id="budget-custom-input", classes="-hidden")

        with Static(classes="config-group") as vs:
            vs.border_title = "Strategy"
            with RadioSet(id="strategy-radioset"):
                yield RadioButton("Balanced", id="strategy-balanced")
                yield RadioButton("Aggressive", id="strategy-aggressive")
                yield RadioButton("Structure", id="strategy-structure")
                yield RadioButton("Faithful", id="strategy-faithful")

        with Static(classes="config-group") as vs:
            vs.border_title = "Focus Keywords"
            yield Input(placeholder="e.g., api, route, auth", id="focus-input")

        with Static(classes="config-group") as vs:
            vs.border_title = "Temporal Gaze"
            yield Input(placeholder="e.g., HEAD~3, main", id="since-input")

        with Static(classes="config-group") as vs:
            vs.border_title = "Gaze Filters"
            yield Input(placeholder="Ignore (e.g., *.log)", id="ignore-input")
            yield Input(placeholder="Include (e.g., src/**/*.py)", id="include-input")

    def on_mount(self) -> None:
        self.query_one("#budget-sage").value = True
        self.query_one("#strategy-balanced").value = True
        # [FIX] Use set_timer for initial call
        self.set_timer(0.1, self._proclaim_will)

    @on(RadioSet.Changed, "#budget-radioset")
    def on_budget_preset_changed(self, event: RadioSet.Changed) -> None:
        custom_input = self.query_one("#budget-custom-input", Input)
        is_custom = (event.pressed.id == "budget-custom")
        if is_custom:
            custom_input.remove_class("-hidden")
            custom_input.focus()
        else:
            custom_input.add_class("-hidden")
        self._trigger_proclamation()

    @on(Input.Changed)
    @on(RadioSet.Changed, "#strategy-radioset")
    def handle_config_change(self, event) -> None:
        self._trigger_proclamation()

    def _trigger_proclamation(self) -> None:
        # [FIX] Use .stop() for Textual Timer
        if self._config_change_timer is not None:
            self._config_change_timer.stop()
        # [FIX] Use self.set_timer
        self._config_change_timer = self.set_timer(0.25, self._proclaim_will)

    def _proclaim_will(self) -> None:
        try:
            budget_radio = self.query_one("#budget-radioset", RadioSet)
            strategy_radio = self.query_one("#strategy-radioset", RadioSet)

            if not budget_radio.pressed_button or not strategy_radio.pressed_button:
                return

            budget_preset = budget_radio.pressed_button.id.split("-")[-1]
            strategy_val = strategy_radio.pressed_button.id.split("-")[-1]

            budget_value = self.query_one("#budget-custom-input",
                                          Input).value if budget_preset == "custom" else budget_preset

            config = DistillConfig(
                budget=budget_value,
                strategy=strategy_val,
                focus_keywords=[k.strip() for k in self.query_one("#focus-input", Input).value.split(',') if k.strip()],
                since=self.query_one("#since-input", Input).value or None,
                ignore_patterns=[p.strip() for p in self.query_one("#ignore-input", Input).value.split(',') if
                                 p.strip()],
                include_patterns=[p.strip() for p in self.query_one("#include-input", Input).value.split(',') if
                                  p.strip()],
            )
            self.post_message(ConfigChanged(config=config))
        except Exception as e:
            self.scribe.error(f"Proclamation paradox: {e}")
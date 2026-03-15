# scaffold/semantic_injection/directives/ui_knowledge/go_tui.py

from textwrap import dedent
from typing import List, Tuple

from .registry import ComponentRegistry

# We define the import path based on what you named the module in the .scaffold file
MODULE_PATH = "gnostic-tui"

@ComponentRegistry.register("tui-card")
def forge_tui_card(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Generates Go code that uses the 'gnostic-tui' library.
    Usage: main.go :: @ui/component(name="WelcomeCard", props="title:Hello, content:World")
    """
    # Parse props
    config = {k: v for k, v in props}
    title = config.get("title", "Card Title")
    content = config.get("content", "Card Content")
    width = config.get("width", "40")

    return dedent(f"""
        package main

        import (
            "fmt"
            "{MODULE_PATH}/ui/molecules"
        )

        func {name}() string {{
            // Uses the Molecule from your generated library
            return molecules.Card("{title}", "{content}", {width})
        }}
    """).strip()

@ComponentRegistry.register("tui-view")
def forge_tui_view(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Generates a full Bubble Tea View method utilizing the Atoms.
    """
    return dedent(f"""
        func (m model) View() string {{
            // The Layout Organism
            return lipgloss.JoinVertical(
                lipgloss.Left,
                atoms.NewButton("Start").View(),
                atoms.NewButton("Stop").View(),
            )
        }}
    """).strip()
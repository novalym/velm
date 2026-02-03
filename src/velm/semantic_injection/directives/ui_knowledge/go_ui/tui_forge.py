# scaffold/semantic_injection/directives/ui_knowledge/go_ui/tui_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry

# This assumes the user named their library 'gnostic-tui' in the previous step.
# Future elevation: Make this dynamic via scaffold settings.
LIB_IMPORT = "gnostic-tui/ui"

@ComponentRegistry.register("go-main")
def forge_go_main(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a `main.go` entry point wired up to the Gnostic TUI library.
    """
    return dedent(f"""
        package main

        import (
            "fmt"
            "os"
            tea "github.com/charmbracelet/bubbletea"
            "{LIB_IMPORT}/molecules"
            "{LIB_IMPORT}/atoms"
            "{LIB_IMPORT}/theme"
        )

        type model struct {{
            width, height int
        }}

        func (m model) Init() tea.Cmd {{ return nil }}

        func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {{
            switch msg := msg.(type) {{
            case tea.KeyMsg:
                if msg.String() == "q" {{ return m, tea.Quit }}
            case tea.WindowSizeMsg:
                m.width, m.height = msg.Width, msg.Height
            }}
            return m, nil
        }}

        func (m model) View() string {{
            card := molecules.Card("System Status", "All systems nominal.", 40)
            btn := atoms.NewButton("Reboot").View()
            return fmt.Sprintf("\\n%s\\n\\n%s\\n(Press 'q' to quit)", card, btn)
        }}

        func main() {{
            p := tea.NewProgram(model{{}}, tea.WithAltScreen())
            if _, err := p.Run(); err != nil {{
                fmt.Printf("Error: %v", err)
                os.Exit(1)
            }}
        }}
    """).strip()
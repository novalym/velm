package atoms

import (
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

// Button represents a clickable action
type Button struct {
    Label    string
    Active   bool
    OnPress  func()
}

func NewButton(label string) Button {
    return Button{Label: label}
}

func (b Button) View() string {
    style := lipgloss.NewStyle().
        Padding(0, 3).
        MarginRight(1).
        Foreground(theme.Text).
        Background(theme.Surface)

    if b.Active {
        style = style.
            Background(theme.Primary).
            Foreground(lipgloss.Color("#ffffff")).
            Bold(true)
    }

    return style.Render(b.Label)
}
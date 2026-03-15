package atoms

import (
    "github.com/charmbracelet/bubbles/spinner"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

// NewGnosticSpinner creates a styled spinner model
func NewGnosticSpinner() spinner.Model {
    s := spinner.New()
    s.Spinner = spinner.Dot
    s.Style = lipgloss.NewStyle().Foreground(theme.Secondary)
    return s
}
package atoms

import (
    "strings"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

func HLine(width int) string {
    return lipgloss.NewStyle().
        Foreground(theme.Border).
        Render(strings.Repeat("─", width))
}

func VLine(height int) string {
    return lipgloss.NewStyle().
        Foreground(theme.Border).
        Render(strings.Repeat("│\\n", height))
}
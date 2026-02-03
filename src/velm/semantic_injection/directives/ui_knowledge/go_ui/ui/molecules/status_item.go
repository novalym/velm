package molecules

import (
    "fmt"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/atoms"
    "gnostic-tui/ui/theme"
)

// StatusRow renders a "Key: Value [Badge]" row
func StatusRow(key string, value string, badge string, variant atoms.BadgeVariant) string {
    k := lipgloss.NewStyle().Foreground(theme.Subtext).Width(15).Render(key + ":")
    v := lipgloss.NewStyle().Foreground(theme.Text).Width(20).Render(value)
    b := atoms.Badge(badge, variant)

    return fmt.Sprintf("%s %s %s", k, v, b)
}
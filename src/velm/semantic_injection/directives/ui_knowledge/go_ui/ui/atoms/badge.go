package atoms

import (
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

type BadgeVariant int

const (
    BadgeInfo BadgeVariant = iota
    BadgeSuccess
    BadgeWarning
    BadgeDanger
)

func Badge(text string, variant BadgeVariant) string {
    base := lipgloss.NewStyle().
        Padding(0, 1).
        HasForeground(true).
        Bold(true).
        CornerRadius(3) // Rounded pills

    switch variant {
    case BadgeSuccess:
        return base.Background(theme.Accent).Foreground(lipgloss.Color("#000")).Render(text)
    case BadgeWarning:
        return base.Background(theme.Warning).Foreground(lipgloss.Color("#000")).Render(text)
    case BadgeDanger:
        return base.Background(theme.Danger).Foreground(lipgloss.Color("#fff")).Render(text)
    default:
        return base.Background(theme.Primary).Foreground(lipgloss.Color("#fff")).Render(text)
    }
}
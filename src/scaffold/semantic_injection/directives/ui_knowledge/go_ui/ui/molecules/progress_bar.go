package molecules

import (
    "github.com/charmbracelet/bubbles/progress"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

func NewProgressBar(width int) progress.Model {
    return progress.New(
        progress.WithDefaultGradient(),
        progress.WithWidth(width),
        progress.WithoutPercentage(),
    )
}

// RenderWithLabel adds a label above the bar
func RenderProgress(p progress.Model, label string) string {
    return lipgloss.JoinVertical(
        lipgloss.Left,
        lipgloss.NewStyle().Foreground(theme.Subtext).MarginBottom(1).Render(label),
        p.View(),
    )
}
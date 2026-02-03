package molecules

import (
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

// Card renders a titled container
func Card(title string, content string, width int) string {
    titleRender := theme.TitleStyle.Render(title)

    // Ensure content wraps or fits
    contentStyle := lipgloss.NewStyle().Width(width - 4) // Account for padding/border

    return theme.CardStyle.
        Width(width).
        Render(
            lipgloss.JoinVertical(
                lipgloss.Left,
                titleRender,
                contentStyle.Render(content),
            ),
        )
}
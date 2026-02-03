package molecules

import (
    "github.com/charmbracelet/bubbles/textinput"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

// NewSearchInput creates a styled text input for searching
func NewSearchInput() textinput.Model {
    ti := textinput.New()
    ti.Placeholder = "Search the cosmos..."
    ti.CharLimit = 156
    ti.Width = 40

    ti.Prompt = "🔍 "
    ti.PromptStyle = lipgloss.NewStyle().Foreground(theme.Primary)
    ti.TextStyle = lipgloss.NewStyle().Foreground(theme.Text)
    ti.PlaceholderStyle = lipgloss.NewStyle().Foreground(theme.Subtext)

    return ti
}
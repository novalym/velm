package theme

import "github.com/charmbracelet/lipgloss"

// The Palette of the Cosmos
var (
    Primary   = lipgloss.Color("#6366f1") // Indigo
    Secondary = lipgloss.Color("#ec4899") // Pink
    Accent    = lipgloss.Color("#10b981") // Emerald
    Warning   = lipgloss.Color("#f59e0b") // Amber
    Danger    = lipgloss.Color("#ef4444") // Red
    Text      = lipgloss.Color("#f8fafc") // Slate 50
    Subtext   = lipgloss.Color("#94a3b8") // Slate 400
    Surface   = lipgloss.Color("#1e293b") // Slate 800
    Border    = lipgloss.Color("#334155") // Slate 700
)

// The Styles of Form
var (
    BaseStyle = lipgloss.NewStyle().
        Foreground(Text)

    CardStyle = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(Border).
        Padding(1, 2).
        MarginBottom(1)

    TitleStyle = lipgloss.NewStyle().
        Foreground(Primary).
        Bold(true).
        MarginBottom(1)

    FocusedStyle = lipgloss.NewStyle().
        Border(lipgloss.RoundedBorder()).
        BorderForeground(Primary)
)
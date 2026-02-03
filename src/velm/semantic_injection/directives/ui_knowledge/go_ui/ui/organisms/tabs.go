package organisms

import (
    "strings"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

var (
    activeTabBorder = lipgloss.Border{
        Top:         "─",
        Bottom:      " ",
        Left:        "│",
        Right:       "│",
        TopLeft:     "╭",
        TopRight:    "╮",
        BottomLeft:  "┘",
        BottomRight: "└",
    }

    tabBorder = lipgloss.Border{
        Top:         "─",
        Bottom:      "─",
        Left:        "│",
        Right:       "│",
        TopLeft:     "╭",
        TopRight:    "╮",
        BottomLeft:  "┴",
        BottomRight: "┴",
    }

    inactiveTab = lipgloss.NewStyle().
        Border(tabBorder, true).
        BorderForeground(theme.Border).
        Padding(0, 1)

    activeTab = inactiveTab.Copy().
        Border(activeTabBorder, true).
        BorderForeground(theme.Primary).
        Foreground(theme.Primary)

    tabGap = lipgloss.NewStyle().
        Border(lipgloss.Border{Bottom: "─"}, false, false, true, false).
        BorderForeground(theme.Border).
        Width(2)
)

func RenderTabs(items []string, activeIndex int, width int) string {
    var renderedTabs []string

    for i, item := range items {
        if i == activeIndex {
            renderedTabs = append(renderedTabs, activeTab.Render(item))
        } else {
            renderedTabs = append(renderedTabs, inactiveTab.Render(item))
        }
    }

    row := lipgloss.JoinHorizontal(lipgloss.Top, renderedTabs...)

    // Fill remaining width with bottom border
    gapWidth := width - lipgloss.Width(row)
    if gapWidth > 0 {
        gap := lipgloss.NewStyle().
            Border(lipgloss.Border{Bottom: "─"}, false, false, true, false).
            BorderForeground(theme.Border).
            Width(gapWidth).
            Render("")
        row = lipgloss.JoinHorizontal(lipgloss.Top, row, gap)
    }

    return row
}
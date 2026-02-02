package organisms

import (
    "github.com/charmbracelet/bubbles/table"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

func NewDataTable() table.Model {
    columns := []table.Column{
        {Title: "ID", Width: 5},
        {Title: "Scripture", Width: 20},
        {Title: "Status", Width: 10},
        {Title: "Size", Width: 10},
    }

    rows := []table.Row{
        {"1", "genesis.py", "Active", "12KB"},
        {"2", "weaver.go", "Active", "45KB"},
        {"3", "void.rs", "Dormant", "0KB"},
        {"4", "prophet.ts", "Active", "18KB"},
    }

    t := table.New(
        table.WithColumns(columns),
        table.WithRows(rows),
        table.WithFocused(true),
        table.WithHeight(7),
    )

    s := table.DefaultStyles()
    s.Header = s.Header.
        BorderStyle(lipgloss.NormalBorder()).
        BorderForeground(theme.Border).
        BorderBottom(true).
        Bold(true)

    s.Selected = s.Selected.
        Foreground(lipgloss.Color("229")).
        Background(theme.Primary).
        Bold(false)

    t.SetStyles(s)
    return t
}
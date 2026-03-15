package main

import (
    "fmt"
    "os"
    "strings"

    tea "github.com/charmbracelet/bubbletea"
    "github.com/charmbracelet/lipgloss"

    "gnostic-tui/ui/theme"
    "gnostic-tui/ui/atoms"
    "gnostic-tui/ui/molecules"
    "gnostic-tui/ui/organisms"
    "github.com/charmbracelet/bubbles/spinner"
    "github.com/charmbracelet/bubbles/table"
)

type model struct {
    // State
    tabs        []string
    activeTab   int
    quitting    bool
    width       int
    height      int

    // Components
    spinner     spinner.Model
    dataTable   table.Model
    help        tea.Model // Using generic model interface for simplicity here
}

func initialModel() model {
    s := atoms.NewGnosticSpinner()
    t := organisms.NewDataTable()

    return model{
        tabs:      []string{"Overview", "Data", "System"},
        activeTab: 0,
        spinner:   s,
        dataTable: t,
    }
}

func (m model) Init() tea.Cmd {
    return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    var cmd tea.Cmd
    var cmds []tea.Cmd

    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "q", "ctrl+c":
            m.quitting = true
            return m, tea.Quit
        case "tab", "right":
            m.activeTab = (m.activeTab + 1) % len(m.tabs)
        case "shift+tab", "left":
            if m.activeTab > 0 {
                m.activeTab--
            } else {
                m.activeTab = len(m.tabs) - 1
            }
        }
    case tea.WindowSizeMsg:
        m.width = msg.Width
        m.height = msg.Height
    }

    // Update sub-components
    m.spinner, cmd = m.spinner.Update(msg)
    cmds = append(cmds, cmd)

    m.dataTable, cmd = m.dataTable.Update(msg)
    cmds = append(cmds, cmd)

    return m, tea.Batch(cmds...)
}

func (m model) View() string {
    if m.quitting {
        return "The Gnostic UI returns to the void.\\n"
    }

    // 1. Header / Tabs
    tabBar := organisms.RenderTabs(m.tabs, m.activeTab, m.width-4)

    var content string

    // 2. Content Area
    switch m.activeTab {
    case 0: // Overview
        welcome := theme.TitleStyle.Render("Welcome to the Citadel")

        // Row 1: Metrics
        metrics := lipgloss.JoinHorizontal(lipgloss.Top,
            molecules.Card("CPU Usage", molecules.StatusRow("Core 1", "45%", "Normal", atoms.BadgeSuccess), 30),
            lipgloss.NewStyle().Width(2).Render(""), // Gap
            molecules.Card("Memory", molecules.StatusRow("Heap", "1.2GB", "High", atoms.BadgeWarning), 30),
        )

        // Row 2: Spinner & Buttons
        controls := lipgloss.JoinHorizontal(lipgloss.Center, 
            lipgloss.NewStyle().MarginRight(2).Render(m.spinner.View() + " Processing..."),
            atoms.NewButton("Deploy").View(),
            atoms.NewButton("Reset").View(),
        )

        content = lipgloss.JoinVertical(lipgloss.Left, welcome, metrics, "\\n", controls)

    case 1: // Data
        content = lipgloss.JoinVertical(lipgloss.Left,
            theme.TitleStyle.Render("Scripture Registry"),
            m.dataTable.View(),
        )

    case 2: // System
        content = lipgloss.JoinVertical(lipgloss.Left,
            theme.TitleStyle.Render("System Status"),
            molecules.RenderProgress(molecules.NewProgressBar(40), "Initialization"),
            "\\n",
            molecules.Card("Alert", "System integrity at 99%. Gnostic field stable.", 50),
        )
    }

    // 3. Layout
    return lipgloss.JoinVertical(lipgloss.Left,
        tabBar,
        "\\n",
        lipgloss.NewStyle().Padding(1, 2).Render(content),
        "\\n",
        lipgloss.NewStyle().Foreground(theme.Subtext).Render("Press 'q' to quit • 'tab' to switch view"),
    )
}

func main() {
    p := tea.NewProgram(initialModel(), tea.WithAltScreen())
    if _, err := p.Run(); err != nil {
        fmt.Printf("Alas, there's been an error: %v", err)
        os.Exit(1)
    }
}
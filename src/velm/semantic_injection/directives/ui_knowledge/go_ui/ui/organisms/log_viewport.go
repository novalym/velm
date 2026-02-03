package organisms

import (
    "fmt"
    "github.com/charmbracelet/bubbles/viewport"
    "github.com/charmbracelet/lipgloss"
    "gnostic-tui/ui/theme"
)

func NewLogViewport(width, height int) viewport.Model {
    vp := viewport.New(width, height)
    vp.Style = lipgloss.NewStyle().
        Border(lipgloss.NormalBorder()).
        BorderForeground(theme.Border).
        Padding(0, 1)

    vp.SetContent("System initialized.\\nListening for Gnostic signals...\\n")
    return vp
}

func AppendLog(vp *viewport.Model, msg string) {
    oldContent := vp.View()
    // A simple simulation of log appending. 
    // In a real app, you'd maintain a buffer.
    newContent := fmt.Sprintf("%s\\n> %s", oldContent, msg)
    vp.SetContent(newContent)
    vp.GotoBottom()
}
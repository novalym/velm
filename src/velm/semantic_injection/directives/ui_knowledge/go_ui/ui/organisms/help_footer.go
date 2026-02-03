package organisms

import (
    "github.com/charmbracelet/bubbles/help"
    "github.com/charmbracelet/bubbles/key"
)

// KeyMap defines the available keybindings
type KeyMap struct {
    Up    key.Binding
    Down  key.Binding
    Enter key.Binding
    Quit  key.Binding
    Help  key.Binding
}

func (k KeyMap) ShortHelp() []key.Binding {
    return []key.Binding{k.Quit, k.Help}
}

func (k KeyMap) FullHelp() [][]key.Binding {
    return [][]key.Binding{
        {k.Up, k.Down, k.Enter},
        {k.Quit, k.Help},
    }
}

var Keys = KeyMap{
    Up:    key.NewBinding(key.WithKeys("up", "k"), key.WithHelp("↑/k", "up")),
    Down:  key.NewBinding(key.WithKeys("down", "j"), key.WithHelp("↓/j", "down")),
    Enter: key.NewBinding(key.WithKeys("enter"), key.WithHelp("enter", "select")),
    Quit:  key.NewBinding(key.WithKeys("q", "esc"), key.WithHelp("q", "quit")),
    Help:  key.NewBinding(key.WithKeys("?"), key.WithHelp("?", "toggle help")),
}

func NewHelp() help.Model {
    return help.New()
}
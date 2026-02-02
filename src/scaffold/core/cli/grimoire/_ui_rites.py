# scaffold/core/cli/grimoire/_ui_rites.py
"""Rites that govern the user interface and interaction with the Architect."""
from ..cli_utils import add_common_flags

RITES = {
    "pad": {
        "module_path": "artisans.pad",
        "artisan_class_name": "PadArtisan",
        "request_class_name": "PadRequest",
        "help": "Summons a lightweight, focused TUI 'Pad' for a specific task.",
        "flags": [add_common_flags],
        "args": [("pad_name", {"help": "The name of the Gnostic Pad to summon (e.g., 'distill', 'refactor')."})]
    },
    "studio": {
        "module_path": "artisans.studio",
        "artisan_class_name": "StudioArtisan",
        "request_class_name": "StudioRequest",
        "help": "Launches the full TUI Design Studio for interactive project management.",
        "flags": [add_common_flags],
        "args": [("path", {"nargs": "?", "default": ".", "help": "The initial directory to open in the studio."})],
    },
    "shell": {
        "module_path": "artisans.shell",
        "artisan_class_name": "ShellArtisan",
        "request_class_name": "ShellRequest",
        "help": "The Gateway to the Gnostic Cockpit. Summons the TUI environment.",
        "flags": [add_common_flags],
    },
    "gui": {
        "module_path": "artisans.gui",
        "artisan_class_name": "GuiArtisan",
        "request_class_name": "GuiRequest",
        "help": "The Omni-Bar. Dynamically generates a TUI for every registered artisan.",
        "flags": [add_common_flags],
    },
    "help": {
        "module_path": "artisans.help",
        "artisan_class_name": "HelpArtisan",
        "request_class_name": "HelpRequest",
        "help": "The Gnostic Oracle. Reveals the living codex of the Scaffold God-Engine.",
        "flags": [],
        "args": [("topic", {"nargs": "?", "help": "The specific Gnosis you seek."})],
    },
    "repl": {
        "module_path": "artisans.repl_artisan",
        "artisan_class_name": "ReplArtisan",
        "request_class_name": "ReplRequest",
        "help": "The Tower of Babel: A Gnostic Polyglot REPL.",
        "flags": [add_common_flags],
    },
    "telepathy": {
        "module_path": "artisans.telepathy",
        "artisan_class_name": "TelepathyArtisan",
        "request_class_name": "TelepathyRequest",
        "help": "The Telepathic Clipboard. Watches for code and offers to capture it.",
        "flags": [add_common_flags],
    },
}
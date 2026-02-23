# Path: core/cli/grimoire/_ui_bridge_rites.py
from ..cli_utils import add_common_flags

RITES = {
    "ui": {
        "module_path": "artisans.ui.artisan",
        "artisan_class_name": "UIArtisan",
        "request_class_name": "UIRequest",
        "help": "Awaken the Sovereign Local Workbench.",
        "description": (
            "The `ui` command materializes the Gnostic Workbench as a local desktop app "
            "running in your browser. It provides total sovereignty over your local "
            "filesystem while maintaining the high-status Next.js interface."
        ),
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--port', type=int, default=7860, help='The localhost port to bind.'),
            lambda p: p.add_argument('--no-browser', action='store_true', help='Suppress automatic browser opening.'),
        ]
    }
}
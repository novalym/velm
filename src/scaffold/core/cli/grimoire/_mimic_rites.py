# Path: core/cli/grimoire/_mimic_rites.py
# ---------------------------------------

from ..cli_utils import add_common_flags

RITES = {
    "mimic": {
        "module_path": "artisans.mimic.artisan",
        "artisan_class_name": "MimicArtisan",
        "request_class_name": "MimicRequest",
        "help": "The Simulacrum. Materialize an ephemeral API from a type definition.",
        "flags": [add_common_flags],
        "args": [
            ("source_path", {"help": "Path to the type definition (e.g., src/models/user.py)."}),
            ("--port", {"type": int, "default": 8000, "help": "Port to bind the simulation to."}),
            ("--framework", {"choices": ["fastapi", "express"], "default": "fastapi", "help": "The soul of the simulation."}),
            ("--no-watch", {"action": "store_false", "dest": "watch", "help": "Disable auto-regeneration on change."})
        ]
    }
}
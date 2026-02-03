# scaffold/core/cli/grimoire/_automation_rites.py
"""Rites for conducting workflows, orchestrating symphonies, and local vigilance."""
from ..cli_utils import add_common_flags, add_variable_flags, add_simulation_flags
import argparse

RITES = {
    "symphony": {
        "module_path": "artisans.symphony",
        "artisan_class_name": "SymphonyArtisan",
        "request_class_name": "SymphonyRequest",
        "help": "The Sovereign Conductor. Orchestrates complex executable workflows.",
        "flags": [add_common_flags, add_variable_flags, add_simulation_flags],
        "args": [
            ("symphony_command", {"choices": ["conduct", "debug"], "help": "The symphonic rite to perform."}),
            ("symphony_path", {"nargs": "?", "help": "Path to the .symphony scripture."})
        ],
    },
    "watch": {
        "module_path": "artisans.watchman",
        "artisan_class_name": "WatchmanArtisan",
        "request_class_name": "WatchmanRequest",
        "help": "The Watchman. Sentinel of local vigilance and auto-execution.",
        "flags": [add_common_flags],
        "args": [
            ("glob_pattern", {"help": "The profile name or glob pattern to watch."}),
            ("command_to_run", {"nargs": "?", "help": "The shell command to execute on change."})
        ],
    },
    "save": {
        "module_path": "artisans.save_artisan",
        "artisan_class_name": "SaveArtisan",
        "request_class_name": "SaveRequest",
        "help": "The Neural Scribe. Generates intent-driven commits and self-heals.",
        "flags": [add_common_flags],
        "args": [("intent", {"help": "The natural language intent for this save point."})],
    },
    "changelog": {
        "module_path": "artisans.changelog.artisan",
        "artisan_class_name": "ChangelogArtisan",
        "request_class_name": "ChangelogRequest",
        "help": "The Chronicle Scribe. Transmutes git history into a CHANGELOG.md.",
        "flags": [add_common_flags],
    },
    "ci-optimize": {
        "module_path": "artisans.ci_optimize",
        "artisan_class_name": "OptimizeCIArtisan",
        "request_class_name": "OptimizeCIRequest",
        "help": "The Self-Mutating CI. Analyzes telemetry to optimize workflow speeds.",
        "flags": [add_common_flags],
        "args": [("workflow_path", {"help": "Path to the CI workflow YAML to optimize."})],
    },
}
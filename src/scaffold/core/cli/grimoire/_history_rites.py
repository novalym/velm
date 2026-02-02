# scaffold/core/cli/grimoire/_history_rites.py
"""Rites governing the Gnostic Timeline and causality."""
from ..cli_utils import add_common_flags
import argparse

RITES = {
    "history": {
        "module_path": "artisans.history",
        "artisan_class_name": "HistoryArtisan",
        "request_class_name": "HistoryRequest",
        "help": "The Chronomancer. Gazes into the Gnostic Timeline of project changes.",
        "flags": [add_common_flags],
        "args": [
            ("command", {"nargs": "?", "choices": ["list", "inspect", "undo"], "help": "The temporal rite to perform."}),
            ("target_id", {"nargs": "?", "help": "The ID of the rite to inspect or undo to."}),
        ],
    },
    "undo": {
        "module_path": "artisans.undo",
        "artisan_class_name": "UndoArtisan",
        "request_class_name": "UndoRequest",
        "help": "Reverses the last rite, returning reality to its previous state.",
        "flags": [add_common_flags],
        "args": [("steps", {"nargs": "?", "type": int, "default": 1, "help": "Number of rites to reverse."})],
    },
    "blame": {
        "module_path": "artisans.blame",
        "artisan_class_name": "BlameArtisan",
        "request_class_name": "BlameRequest",
        "help": "The Forensic Omniscient. Reconstructs the causal reality of a scripture.",
        "flags": [add_common_flags],
        "args": [("target_path", {"help": "The path to the scripture whose provenance you seek."})],
    },
    "time-branch": {
        "module_path": "artisans.time_branch",
        "artisan_class_name": "TimeBranchArtisan",
        "request_class_name": "TimeBranchRequest",
        "help": "Creates a new Git branch from a past rite in the Gnostic Chronicle.",
        "flags": [add_common_flags],
        "args": [
            ("from_rite", {"help": "The Rite ID (or prefix) to branch from."}),
            ("new_branch_name", {"help": "The name of the new timeline (branch) to forge."}),
        ],
    },
    "time-machine": {
        "module_path": "artisans.time_machine",
        "artisan_class_name": "TimeMachineArtisan",
        "request_class_name": "TimeMachineRequest",
        "help": "The Gnostic gateway to the interactive timeline.",
        "flags": [add_common_flags],
    },
    "replay": {
        "module_path": "artisans.replay",
        "artisan_class_name": "ReplayArtisan",
        "request_class_name": "ReplayRequest",
        "help": "The Temporal Engine. Re-runs past rites from a Daemon traffic log.",
        "flags": [add_common_flags],
        "args": [("log_path", {"help": "Path to the daemon_traffic.jsonl log file."})],
    },
}
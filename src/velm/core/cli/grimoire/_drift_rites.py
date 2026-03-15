# Path: src/velm/core/cli/grimoire/_drift_rites.py
# -----------------------------------------------

from ..cli_utils import add_common_flags, add_variable_flags, add_simulation_flags

RITES = {
    "drift": {
        "module_path": "artisans.drift.artisan",
        "artisan_class_name": "DriftArtisan",
        "request_class_name": "DriftRequest",
        "help": "The State Governor. Reconciles Blueprint, Lockfile, and Reality.",
        "description": "The 'drift' rite is the ultimate authority for state management. "
                       "It performs a 3-way AST-aware reconciliation to find and heal schisms "
                       "between your blueprint and the physical disk.",
        "flags": [
            add_common_flags,
            add_variable_flags,
            add_simulation_flags,
            lambda p: p.add_argument('--strict', action='store_true', help='Fracture build if drift is found (CI mode).'),
            lambda p: p.add_argument('--auto-approve', action='store_true', help='Execute plan without confirmation.'),
            lambda p: p.add_argument('--out', dest='out_file', help='Export Execution Plan to JSON.')
        ],
        "args": [
            ("drift_command", {
                "nargs": "?",
                "default": "plan",
                "choices": ["check", "plan", "apply", "heal", "interactive"],
                "help": "The reconciliation verb."
            }),
            ("target_path", {
                "nargs": "?",
                "help": "Limit the gaze to a specific file or directory."
            })
        ]
    }
}
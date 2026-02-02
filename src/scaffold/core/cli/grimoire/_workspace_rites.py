# Path: scaffold/core/cli/grimoire/_workspace_rites.py
# ----------------------------------------------------

from ..cli_utils import add_common_flags, add_variable_flags

RITES = {
    "workspace": {
        "module_path": "artisans.workspace",
        "artisan_class_name": "WorkspaceArtisan",
        "request_class_name": "WorkspaceRequest",
        "help": "The God-Engine of the Gnostic Observatory. Manage the multi-project cosmos.",
        "flags": [add_common_flags, add_variable_flags],
        "subparsers": {
            "pad": {
                "help": "Summon the Gnostic Cockpit (TUI) for the workspace."
            },
            "genesis": {
                "help": "Forge a new multi-project cosmos from a .splane scripture.",
                "args": [("splane_path", {"help": "Path to the .splane definition."})]
            },
            "discover": {
                "help": "Scan the current directory for unmanaged git repositories."
            },
            "add": {
                "help": "Adopt a project into the workspace.",
                "args": [("path_to_add", {"help": "Path to the project root."})],
                # [THE FIX] We bestow the JSON flag upon this rite
                "flags": [lambda p: p.add_argument('--json', action='store_true', help='Output in JSON format for the Daemon.')]
            },
            "list": {
                "help": "Proclaim the roster of all managed projects.",
                "flags": [lambda p: p.add_argument('--json', action='store_true', help='Output in JSON format for the Daemon.')]
            },
            "graph": {
                "help": "Visualize the dependency graph of the entire workspace."
            },
            "health": {
                "help": "Conduct a panoptic health inquest on all projects."
            },
            "exec": {
                "help": "Execute a command across all projects (Topological Order).",
                "args": [
                    ("command_to_run", {"help": "The shell command to execute."}),
                    ("--tag", {"help": "Filter projects by tag."})
                ]
            },
            "sync": {
                "help": "Clone missing repositories defined in the workspace config."
            },
            "git": {
                "help": "Run a git command across all projects.",
                "args": [
                    ("git_command", {"help": "The git args (e.g. 'pull origin main')."}),
                    ("--tag", {"help": "Filter projects by tag."})
                ]
            }
        }
    }
}
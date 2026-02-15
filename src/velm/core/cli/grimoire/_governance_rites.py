# Path: src/velm/core/cli/grimoire/_governance_rites.py
# -----------------------------------------------------
# LIF: ∞ | ROLE: GOVERNANCE_INTERFACE_DEFINITION | RANK: OMEGA
# AUTH: Ω_RITES_GOVERNANCE_V1_FINALIS

"""
=================================================================================
== THE RITES OF GOVERNANCE (V-Ω-MULTIVERSE-ADMINISTRATION)                     ==
=================================================================================
These rites empower the Architect to create, destroy, and navigate between
parallel realities (Projects) within the Velm Cosmos.
"""

from ..cli_utils import add_common_flags
import argparse

RITES = {
    "project": {
        "module_path": "artisans.project.artisan",
        "artisan_class_name": "ProjectArtisan",
        "request_class_name": "ProjectRequest",
        "help": "The Reality Governor. Manage workspaces, contexts, and the multiverse registry.",
        "description": (
            "The `project` artisan is the Hypervisor of the Velm Engine. It manages the `projects.json` "
            "registry, allowing you to create isolated workspaces, switch active contexts, and manage "
            "lifecycle events for multiple distinct projects."
        ),
        "flags": [
            add_common_flags,

            # --- IDENTITY ---
            lambda p: p.add_argument('--id', help='The UUID of the target reality (for switch/delete/update).'),
            lambda p: p.add_argument('--name', help='The human-readable name for a new reality.'),
            lambda p: p.add_argument('--desc', dest='description', help='A brief summary of the reality\'s purpose.'),

            # --- GENESIS PARAMETERS ---
            lambda p: p.add_argument('--template',
                                     help='The Archetype DNA to seed the new reality with (e.g., "fastapi-service").'),
            lambda p: p.add_argument('--tags', nargs='*',
                                     help='Semantic labels for categorization (e.g., "backend", "production").'),

            # --- SOVEREIGNTY ---
            lambda p: p.add_argument('--owner', dest='owner_id',
                                     help='The identity of the creator (e.g., "GUEST" or a Clerk ID).'),
            lambda p: p.add_argument('--demo', dest='is_demo', action='store_true',
                                     help='Mark this reality as a read-only System Reference.'),

            # --- MUTATION ---
            lambda p: p.add_argument('--path', help='Physical path override for import operations.'),

            # --- FILTERING ---
            lambda p: p.add_argument('--filter-tags', nargs='*', help='Filter the list by tags.'),
            lambda p: p.add_argument('--filter-status', choices=['active', 'archived'],
                                     help='Filter the list by status.'),

            # --- OUTPUT ---
            lambda p: p.add_argument('--json', action='store_true',
                                     help='Proclaim the registry as machine-readable JSON.'),
        ],
        "args": [
            ("action", {
                "choices": ["list", "create", "delete", "switch", "update", "import", "archive", "restore"],
                "help": "The Governance Rite to perform."
            })
        ],
        "subparsers": {
            "list": {
                "help": "Proclaim the census of all known realities.",
                "description": "Lists all projects in the registry with their status, ID, and active state."
            },
            "create": {
                "help": "Forge a new reality from the void.",
                "description": "Creates a new workspace directory, registers it, and optionally seeds it with an archetype."
            },
            "switch": {
                "help": "Anchor the Engine to a specific reality.",
                "description": "Updates the `active_project_id` and symlinks the workspace root to the target project."
            },
            "delete": {
                "help": "Annihilate a reality.",
                "description": "Permanently removes a project and its files from the multiverse. Requires ID."
            },
            "import": {
                "help": "Adopt an existing directory as a managed reality.",
                "description": "Registers an existing folder in the `projects.json` without moving it."
            }
        }
    }
}
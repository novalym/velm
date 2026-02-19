# Path: src/velm/core/cli/grimoire/_cloud_rites.py
# ------------------------------------------------
# LIF: ∞ | ROLE: CLOUD_CLI_DEFINITION

from ..cli_utils import add_common_flags, add_variable_flags

RITES = {
    "cloud": {
        "module_path": "artisans.cloud.artisan",
        "artisan_class_name": "CloudArtisan",
        "request_class_name": "CloudRequest",
        "help": "The Celestial Manager. Provision and manage remote compute.",
        "description": (
            "The `cloud` artisan is the bridge to the Infrastructure Layer. "
            "It manages the lifecycle of VMs and Containers across multiple providers "
            "(AWS, Oracle, Docker) using a unified Gnostic Interface."
        ),
        "flags": [
            add_common_flags,
            add_variable_flags,
            # Global override for provider
            lambda p: p.add_argument('--provider', help='Override the cloud provider (aws, oracle, docker) for this rite.')
        ],
        "subparsers": {
            "provision": {
                "help": "Materialize a new VM from the void.",
                "description": "Spins up a new compute node based on the provided specifications.",
                "args": [
                    ("--name", {"help": "Human-readable identifier for the node."}),
                    ("--size", {"help": "Instance size (e.g., t3.micro, standard-2)."}),
                    ("--image", {"help": "OS Image ID or slug."}),
                    ("--region", {"help": "Target geographic region."})
                ]
            },
            "terminate": {
                "help": "Return a VM to the void.",
                "description": "Permanently destroys a compute node and releases its resources.",
                "args": [
                    ("instance_id", {"help": "The unique ID of the node to annihilate."})
                ]
            },
            "status": {
                "help": "Scry the health of a specific node.",
                "args": [
                    ("instance_id", {"help": "The unique ID of the node."})
                ]
            },
            "list": {
                "help": "Proclaim the census of all active infrastructure.",
                "description": "Lists all nodes currently managed by VELM across the active provider."
            }
        }
    }
}
# Path: src/velm/core/cli/grimoire/_cloud_rites.py
# ------------------------------------------------
from ..cli_utils import add_common_flags

RITES = {
    "cloud": {
        "module_path": "artisans.cloud.artisan",
        "artisan_class_name": "CloudArtisan",
        "request_class_name": "CloudRequest",
        "help": "The Celestial Manager. Provision and manage remote compute.",
        "flags": [add_common_flags],
        "subparsers": {
            "provision": {
                "help": "Materialize a new VM.",
                "args": [
                    ("--provider", {"choices": ["oracle", "aws", "hetzner"], "default": "oracle", "help": "Cloud Provider."}),
                    ("--name", {"help": "Name of the instance."})
                ]
            },
            "terminate": {
                "help": "Return a VM to the void.",
                "args": [("instance_id", {"help": "ID of the instance."})]
            },
            "status": {
                "help": "Scry the status of an instance.",
                "args": [("instance_id", {"help": "ID of the instance."})]
            }
        }
    }
}
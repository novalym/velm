# scaffold/core/cli/grimoire/_security_rites.py
"""Rites of security, compliance, and celestial projection."""
from ..cli_utils import add_common_flags, add_simulation_flags
import argparse

RITES = {
    "isolate": {
        "module_path": "artisans.isolate",
        "artisan_class_name": "IsolateArtisan",
        "request_class_name": "IsolateRequest",
        "help": "The Supply Chain Sentinel. Protects the sanctum from profane dependencies.",
        "flags": [add_common_flags],
        "args": [("command_to_run", {"nargs": "+", "help": "The command to run in an isolated ward."})],
    },
    "signature": {
        "module_path": "artisans.signature_artisan",
        "artisan_class_name": "SignatureArtisan",
        "request_class_name": "SignatureRequest",
        "help": "The Keeper of the Seals. Learns and verifies the Architect's fingerprint.",
        "flags": [add_common_flags],
        "args": [("signature_command", {"choices": ["learn", "verify", "list"], "help": "The identity rite to conduct."})],
    },
    "with": {
        "module_path": "artisans.with_secrets",
        "artisan_class_name": "WithSecretsArtisan",
        "request_class_name": "WithSecretsRequest",
        "help": "The Ephemeral Vault. Executes rites within a secure, secret context.",
        "flags": [add_common_flags],
        "args": [
            ("secrets", {"nargs": "+", "help": "List of secret references (e.g. op://vault/item)."}),
            ("--", {"dest": "command", "nargs": argparse.REMAINDER, "help": "The command to execute."})
        ],
    },
    "deploy": {
        "module_path": "artisans.deploy",
        "artisan_class_name": "DeployArtisan",
        "request_class_name": "DeployRequest",
        "help": "The Helm Chart Weaver. Transmutes local reality for Kubernetes.",
        "flags": [add_common_flags, add_simulation_flags],
    },
    "expose": {
        "module_path": "artisans.expose",
        "artisan_class_name": "ExposeArtisan",
        "request_class_name": "ExposeRequest",
        "help": "The Port Key. Opens a secure portal from localhost to the public aether.",
        "flags": [add_common_flags],
        "args": [("port", {"type": int, "help": "The local port to expose."})],
    },
    "prophesy": {
        "module_path": "artisans.prophesy",
        "artisan_class_name": "ProphesyArtisan",
        "request_class_name": "ProphesyRequest",
        "help": "The Oracle of Celestial Economy. Prophesies the cost of infrastructure.",
        "flags": [add_common_flags],
        "args": [("target_path", {"help": "Path to the IaC scripture to analyze."})],
    },
}
# Path: core/cli/grimoire/_publish_rites.py
# -----------------------------------------
# LIF: ∞ | ROLE: KINETIC_COMMAND_DEFINITION | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PUBLISH_RITES_V100_TOTALITY_2026_FINALIS

"""
=================================================================================
== THE RITES OF CELESTIAL ASCENSION (V-Ω-PUBLISH-COMMAND-ULTIMA)               ==
=================================================================================
These rites empower the Architect to consecrate a local directory as a
Gnostic Shard, making its soul and matter available to the SCAF-Hub registry.
=================================================================================
"""

from ..cli_utils import add_common_flags, add_variable_flags, add_simulation_flags
import argparse

RITES = {
    "publish": {
        "module_path": "artisans.publish.artisan",
        "artisan_class_name": "PublishArtisan",
        "request_class_name": "PublishRequest",
        "help": "The Rite of Celestial Ascension. Consecrate and share a Gnostic Shard with SCAF-Hub.",
        "description": (
            "===============================================================================\n"
            "== THE ALTAR OF DISTRIBUTION (V-Ω-TOTALITY-V100)                             ==\n"
            "===============================================================================\n"
            "The `publish` command transmutes a local directory into a content-addressable\n"
            "Celestial Shard. It calculates a Merkle-root identity, compresses the matter,\n"
            "mines semantic gnosis from index.scaffold, and striking the Hub registry.\n\n"
            "Use this to build the Standard Library and share architectural laws across\n"
            "the Multiverse."
        ),
        "flags": [
            add_common_flags,  # --verbose, --root, --trace_id
            add_variable_flags,  # --set var=val
            add_simulation_flags,  # --dry-run, --preview, --audit

            # [ASCENSION 1]: IDENTITY PHALANX
            lambda p: p.add_argument(
                '--namespace',
                required=True,
                help='The Gnostic namespace (e.g. "std.io", "hub.novalym.auth").'
            ),
            lambda p: p.add_argument(
                '--name',
                dest='shard_name',
                required=True,
                help='The unique name of the shard within the namespace.'
            ),

            # [ASCENSION 4]: THE PRIVATE WARD
            lambda p: p.add_argument(
                '--private',
                action='store_true',
                dest='is_private',
                help='Shroud the shard with organization-level encryption.'
            ),
            lambda p: p.add_argument(
                '--org-id',
                help='Associate this shard with a specific Organization ID.'
            ),

            # [ASCENSION 5]: SEMANTIC TAGGING
            lambda p: p.add_argument(
                '--tags',
                nargs='*',
                default=[],
                help='Gnostic keywords to bestown upon the shard for Vector Recall.'
            ),

            # [ASCENSION 11]: THE MERKLE AUDIT
            lambda p: p.add_argument(
                '--audit-only',
                action='store_true',
                dest='audit',
                help='Proclaim the Merkle-Lattice hash and mass without striking the Hub.'
            ),

            # [ASCENSION 12]: METABOLIC IMPACT
            lambda p: p.add_argument(
                '--lif',
                type=int,
                default=1,
                dest='lif_index',
                help='Willed Logarithmic Impact Factor for this shard.'
            )
        ],
        "args": [
            ("target_path", {
                "nargs": "?",
                "default": ".",
                "help": "The physical directory sanctum to ascend. Defaults to current root."
            })
        ],
    }
}

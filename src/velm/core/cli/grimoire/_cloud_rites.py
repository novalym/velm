# Path: src/velm/core/cli/grimoire/_cloud_rites.py
# ------------------------------------------------
# LIF: ∞ | ROLE: CELESTIAL_WILL_INTERFACE | RANK: OMEGA_SOVEREIGN
# AUTH_CODE: Ω_CLOUD_RITES_V100000_MANIFESTATION_FINALIS

from ..cli_utils import add_common_flags, add_variable_flags

RITES = {
    "cloud": {
        "module_path": "artisans.cloud.artisan",
        "artisan_class_name": "CloudArtisan",
        "request_class_name": "CloudRequest",
        "help": "The Multiversal Hypervisor. Provision, Teleport, and Govern Sovereign Iron.",
        "description": (
            "===============================================================================\n"
            "== THE ALTAR OF CELESTIAL WILL (V-Ω-TOTALITY-V100K)                          ==\n"
            "===============================================================================\n"
            "The `cloud` artisan is the bridge to the Infrastructure Layer. It manages the\n"
            "lifecycle of Sovereign Nodes across the Multiverse (OVH, AWS, Oracle, Docker).\n\n"
            "It transforms the Cloud from a 'Service' into a 'Substrate' governed by\n"
            "immutable Gnostic Law. Use this to Materialize, Translocate, and Reboot\n"
            "physical reality at the speed of thought."
        ),
        "flags": [
            add_common_flags,
            add_variable_flags,
            # [ASCENSION 1]: GLOBAL SUBSTRATE OVERRIDE
            # Allows 'velm cloud list --provider ovh' or 'velm cloud status ... --provider aws'
            lambda p: p.add_argument(
                '--provider',
                choices=['ovh', 'aws', 'azure', 'oracle', 'docker', 'auto'],
                default='auto',
                help='Override the target cloud substrate. Default: "auto" (Scry Env DNA).'
            ),
            # [ASCENSION 2]: FISCAL TREASURY WARD
            lambda p: p.add_argument(
                '--max-rate',
                type=float,
                dest='max_hourly_rate',
                default=0.0,
                help='Safety Floor: Abort provisioning if the estimated tax exceeds this hourly rate ($/hr).'
            ),
            # [ASCENSION 3]: ADRENALINE SIGNAL
            lambda p: p.add_argument(
                '--adrenaline',
                action='store_true',
                dest='is_adrenaline',
                help='Invoke Adrenaline Mode: High-metabolic execution priority for critical strikes.'
            )
        ],
        "subparsers": {
            # =========================================================================
            # == RITE I: PROVISION (MATERIALIZATION)                                 ==
            # =========================================================================
            "provision": {
                "help": "Materialize a new Sovereign Node from the void.",
                "description": "Spins up a new compute node based on the project's DNA or explicit Architect will.",
                "args": [
                    ("--name", {"help": "Human-readable label for the node. Default: Auto-generated from Project DNA."}),
                    ("--size", {"default": "default", "help": "Instance size slug (e.g. 'd2-4', 't3.micro'). Default: HardwareOracle prophecy."}),
                    ("--image", {"help": "OS Image ID or slug (e.g. 'ubuntu-22.04')."}),
                    ("--region", {"help": "Target geographic region (e.g. 'GRA11', 'us-east-1')."})
                ]
            },
            # =========================================================================
            # == RITE II: TELEPORT (TRANSLOCATION)                                   ==
            # =========================================================================
            "teleport": {
                "help": "Teleport a Project Vessel (.zip) to a remote Node.",
                "description": "The Rite of Translocation. Ships the virtual project matter across the bridge to the physical Iron.",
                "args": [
                    ("instance_id", {"help": "The unique ID of the target Sovereign Node."}),
                    ("artifact_path", {"help": "Path to the .zip vessel manifest to be teleported."}),
                    ("--dest", {
                        "dest": "remote_dest",
                        "default": "/tmp/vessel.zip",
                        "help": "The destination coordinate on the remote filesystem."
                    })
                ]
            },
            # =========================================================================
            # == RITE III: REBOOT (THE PHOENIX PROTOCOL)                             ==
            # =========================================================================
            "reboot": {
                "help": "Conduct the Phoenix Protocol: Soft-cycle a remote reality.",
                "description": "Restarts the remote instance without destroying the persistent matter shards (Disk).",
                "args": [
                    ("instance_id", {"help": "The ID of the node to cycle."})
                ]
            },
            # =========================================================================
            # == RITE IV: TERMINATE (THE RITE OF OBLIVION)                           ==
            # =========================================================================
            "terminate": {
                "help": "Return a Sovereign Node to the void.",
                "description": "Permanently destroys a compute node and releases its resources. IRREVERSIBLE.",
                "args": [
                    ("instance_id", {"help": "The unique ID of the node to annihilate."})
                ]
            },
            # =========================================================================
            # == RITE V: STATUS (THE SCRYING RITE)                                   ==
            # =========================================================================
            "status": {
                "help": "Scry the vitality and metadata of a specific node.",
                "description": "Peers into the substrate to retrieve state, IP, and metabolic health.",
                "args": [
                    ("instance_id", {"help": "The unique ID of the node to scry. Use 'auth_handshake_trigger' for auth-probes."})
                ]
            },
            # =========================================================================
            # == RITE VI: LIST (THE PANOPTIC CENSUS)                                 ==
            # =========================================================================
            "list": {
                "help": "Proclaim the census of all active Titan Nodes in the Fleet.",
                "description": "Lists all nodes currently managed by VELM. Reconciles with the cloud by default.",
                "args": [
                    ("--fast", {
                        "action": "store_true",
                        "dest": "no_sync",
                        "help": "Bypass the cloud sync and return the cached Gnostic Ledger (Fast Path)."
                    })
                ]
            },
            # =========================================================================
            # == RITE VII: RECONCILE (ACHRONAL ALIGNMENT)                            ==
            # =========================================================================
            "reconcile": {
                "help": "Force an Achronal Reconciliation of the local Ledger with the Cloud.",
                "description": "Finds Zombies (dead but tracked) and Orphans (alive but untracked) and heals the registry."
            },
            # =========================================================================
            # == RITE VIII: COST_CHECK (THE PROPHET OF THRIFT)                       ==
            # =========================================================================
            "cost_check": {
                "help": "Scry the Multiversal Market to find the highest-value substrate.",
                "description": "Analyzes the project mass and compares metabolic tax ($/hr) across all resonant providers."
            }
        }
    }
}

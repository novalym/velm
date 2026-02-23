# Path: core/cli/grimoire/_identity_rites.py
# ------------------------------------------

"""
Rites of Global Identity and Authentication.
These rites are Root-Agnostic and can be performed from the Lobby.
"""
from ..cli_utils import add_common_flags, add_variable_flags

RITES = {
    "identity": {
        "module_path": "artisans.identity.artisan",
        "artisan_class_name": "IdentityArtisan",
        "request_class_name": "IdentityRequest",
        "help": "The Keeper of Keys. Manage global authentication states.",
        "description": (
            "The `identity` artisan is the Sovereign Diplomat. It manages cryptographic "
            "handshakes with the Celestial Providers (OVH, AWS, Azure, Hetzner).\n\n"
            "It supports 3-legged OAuth (OVH), Service Principals (Azure), and "
            "IAM Access Keys (AWS). Use `whoami` to verify your current resonance."
        ),
        "flags": [
            add_common_flags,
            add_variable_flags,  # Allows --set key=value for ad-hoc injection

            # --- IDENTITY TARGETING ---
            lambda p: p.add_argument(
                '--provider',
                required=True,
                choices=['ovh', 'aws', 'azure', 'hetzner'],
                help="The target Celestial Body."
            ),
            lambda p: p.add_argument(
                '--region',
                help="The physical region endpoint (e.g., 'ovh-eu', 'us-east-1')."
            ),

            # --- OVH SPECIFIC ---
            lambda p: p.add_argument('--app-key', help="[OVH] Application Key."),
            lambda p: p.add_argument('--app-secret', help="[OVH] Application Secret."),
            lambda p: p.add_argument('--consumer-key', dest='consumer_key', help="[OVH] Pre-validated Consumer Key."),

            # --- AWS SPECIFIC ---
            lambda p: p.add_argument('--aws-key', dest='aws_access_key_id', help="[AWS] Access Key ID."),
            lambda p: p.add_argument('--aws-secret', dest='aws_secret_access_key', help="[AWS] Secret Access Key."),

            # --- AZURE SPECIFIC ---
            lambda p: p.add_argument('--client-id', dest='azure_client_id',
                                     help="[Azure] Service Principal Client ID."),
            lambda p: p.add_argument('--client-secret', dest='azure_client_secret',
                                     help="[Azure] Service Principal Secret."),
            lambda p: p.add_argument('--tenant-id', dest='azure_tenant_id', help="[Azure] Tenant (Directory) ID."),

            # --- HETZNER SPECIFIC ---
            lambda p: p.add_argument('--token', dest='hcloud_token', help="[Hetzner] API Token."),

            # --- BEHAVIOR ---
            lambda p: p.add_argument(
                '--no-persist',
                action='store_false',
                dest='persist_globally',
                help="Do not save the negotiated keys to the local .env vault."
            )
        ],
        "args": [
            ("action", {
                "choices": ["handshake", "verify", "whoami", "forget", "rotate"],
                "help": "The identity rite to perform."
            })
        ]
    }
}
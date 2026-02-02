# Path: core/cli/grimoire/_guild_rites.py
# ---------------------------------------

from ..cli_utils import add_common_flags

RITES = {
    "guild": {
        "module_path": "artisans.guild.artisan",
        "artisan_class_name": "GuildArtisan",
        "request_class_name": "GuildRequest",
        "help": "The Guild Nexus. Manage federated Gnosis and shared archetypes.",
        "flags": [add_common_flags],
        "subparsers": {
            "publish": {
                "help": "Bundle and publish an archetype to the Guild.",
                "args": [("target", {"help": "The name of the local archetype to publish."}),
                         ("--name", {"help": "Optional alias for the published artifact."})]
            },
            "join": {
                "help": "Subscribe to a remote Guild.",
                "args": [("target", {"help": "The URI of the Guild (Git URL, S3, etc.)."}),
                         ("--name", {"help": "Local alias for this subscription."})]
            },
            "update": {
                "help": "Refresh Gnosis from all subscribed Guilds."
            },
            "list": {
                "help": "Show active Guild subscriptions."
            }
        }
    }
}
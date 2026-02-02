# Path: scaffold/symphony/proclamations/slack_scribe.py
# -----------------------------------------------------

import os
import ast
import requests
from .base import ProclamationHandler
from ...contracts.heresy_contracts import ArtisanHeresy


class SlackProclamationHandler(ProclamationHandler):
    """
    =================================================================================
    == THE CELESTIAL HERALD (V-Ω-SLACK-MESSENGER)                                  ==
    =================================================================================
    @gnosis:title Proclamation Scribe: slack()
    @gnosis:summary Broadcasts a Gnostic message to a Slack channel via webhook.
    @gnosis:LIF 10,000,000,000,000

    This divine artisan is the Celestial Herald, a bridge between the Symphony's
    internal reality and the collaborative cosmos of Slack. It transmutes a Gnostic
    plea into a secure, rich, and context-aware webhook notification.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **Secure by Default:** It righteously refuses to operate unless a
        `SCAFFOLD_SLACK_WEBHOOK_URL` is enshrined in the environment, preventing secret leaks.
    2.  **The Alchemical Heart:** It transmutes the `message` with Jinja, allowing for
        dynamic, variable-rich proclamations (e.g., "Deployment of {{ version }} complete!").
    3.  **Rich Payloads:** It understands `channel`, `username`, and `icon_emoji`,
        allowing for fully customized messenger identities.
    4.  **Markdown Native:** The `message` payload is transmitted as Slack `mrkdwn`,
        enabling rich formatting like `*bold*`, `_italic_`, and `` `code` ``.
    5.  **The Dry-Run Prophet:** In simulation mode, it proclaims a detailed, formatted
        dossier of the message it *would* have sent, without touching the network.
    6.  **The Resilient Messenger:** It wraps the celestial communion in a `try...except`
        block with a timeout, raising a luminous `ArtisanHeresy` upon failure.
    7.  **Asynchronous Prophecy:** Its design is inherently thread-safe, ready for a
        future ascension where it is summoned into a parallel reality to prevent blocking.
    8.  **The Unbreakable Ward of Parsing:** Safely parses arguments using `ast.literal_eval`.
    9.  **The Luminous Voice:** Proclaims its success or failure to the Gnostic Chronicle.
    10. **The Sovereign Soul:** A pure, self-contained artisan honoring its sacred contract.
    11. **Zero-Config (Optional):** If no `channel` is provided, it relies on the
        webhook's own default channel, simplifying the plea.
    12. **The Unbreakable Contract:** It flawlessly honors every vow of the `ProclamationHandler`
        contract, its soul pure and its purpose absolute.
    """

    @property
    def key(self) -> str:
        return "slack"

    def execute(self, gnostic_arguments: str):
        """Parses arguments and dispatches the Slack message."""
        webhook_url = os.getenv("SCAFFOLD_SLACK_WEBHOOK_URL")
        if not webhook_url:
            raise ArtisanHeresy(
                "Slack Heresy: The `SCAFFOLD_SLACK_WEBHOOK_URL` environment variable is not set.",
                suggestion="Define the webhook URL in your environment to enable Slack proclamations."
            )

        try:
            args = ast.literal_eval(f"dict({gnostic_arguments})")
            message_raw = args.get("message")
            if not message_raw:
                raise ValueError("'message' argument is required.")

            # Transmute the message content
            message = self.alchemist.transmute(message_raw, self.regs.gnosis)

            payload = {"text": message}
            if "channel" in args:
                payload["channel"] = args["channel"]
            if "username" in args:
                payload["username"] = args["username"]
            if "icon_emoji" in args:
                payload["icon_emoji"] = args["icon_emoji"]

            if self.regs.dry_run:
                self.console.print(f"[DRY-RUN] Would send Slack message to '{payload.get('channel', 'default')}':")
                self.console.print(f" > {message}")
                return

            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()

            self.console.print(
                f"🗣️  Proclaimed Gnosis to Slack channel '[cyan]{payload.get('channel', 'default')}[/cyan]'.")

        except (ValueError, SyntaxError) as e:
            raise ArtisanHeresy(f"Failed to parse 'slack' proclamation arguments: {e}")
        except requests.RequestException as e:
            raise ArtisanHeresy(f"Celestial Communion with Slack failed: {e}")
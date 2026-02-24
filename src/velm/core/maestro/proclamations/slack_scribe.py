# Path: src/velm/core/maestro/proclamations/slack_scribe.py
# --------------------------------------------------------

import os
import requests
from .base import ProclamationScribe


class SlackScribe(ProclamationScribe):
    """Radiates truth to the Slack Multiverse."""

    def proclaim(self, payload: str, metadata: dict):
        webhook = os.getenv("SCAFFOLD_SLACK_WEBHOOK")
        if not webhook:
            self.logger.warn("Slack Webhook unmanifest. Proclamation restricted to Iron.")
            return

        clean_msg = self._purify(payload or metadata.get("msg", "Gnostic Pulse detected."))

        # [ASCENSION]: We weave the Slack Block-Kit soul
        data = {"text": f"✨ *Scaffold Proclamation*\n> {clean_msg}"}

        try:
            requests.post(webhook, json=data, timeout=5)
            self.logger.success("Proclamation radiated to the Slack void.")
        except Exception as e:
            self.logger.error(f"Celestial radiation fractured: {e}")
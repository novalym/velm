# scaffold/semantic_injection/directives/fetch_domain.py

"""
=================================================================================
== THE HAND OF THE VOID (V-Ω-FETCH-DOMAIN)                                     ==
=================================================================================
LIF: 100,000,000,000

This artisan implements the `@fetch` namespace. It gives the blueprint the power
to reach out to the internet and ingest content. This transforms a static
template into a dynamic aggregator.

Usage:
    .gitignore :: @fetch/gitignore(type="python")
    LICENSE :: @fetch/text(url="https://...")
=================================================================================
"""
from typing import Dict, Any

import requests

from ..contract import BaseDirectiveDomain, SemanticHeresy
from ..loader import domain


@domain("fetch")
class FetchDomain(BaseDirectiveDomain):
    """
    The Universal Client.
    """

    @property
    def namespace(self) -> str:
        return "fetch"

    def help(self) -> str:
        return "Fetches remote content from URLs or APIs (gitignore.io, raw text)."

    def _directive_text(self, context: Dict[str, Any], url: str = "", *args, **kwargs) -> str:
        """
        @fetch/text(url="https://example.com/raw.txt")
        Fetches raw text from a URL.
        """
        if not url:
            raise SemanticHeresy("The 'url' argument is required for @fetch/text.")

        try:
            # We set a strict timeout to prevent the engine from hanging on the void.
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except Exception as e:
            raise SemanticHeresy(f"Failed to fetch from the void: {url}. Reason: {e}")

    def _directive_gitignore(self, context: Dict[str, Any], type: str = "", *args, **kwargs) -> str:
        """
        @fetch/gitignore(type="python,windows,visualstudiocode")
        Communes with the gitignore.io API to fetch standard ignore lists.
        """
        if not type:
            raise SemanticHeresy("The 'type' argument is required (e.g., 'python,node').")

        api_url = f"https://www.toptal.com/developers/gitignore/api/{type}"
        try:
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                return response.text
            else:
                # Gitignore.io returns text even on error often, but let's be safe
                raise SemanticHeresy(f"Gitignore API rejected the plea for '{type}'.")
        except Exception as e:
            raise SemanticHeresy(f"Failed to commune with Gitignore Oracle. Reason: {e}")

    def _directive_github_raw(self, context: Dict[str, Any], user: str, repo: str, path: str, branch: str = "main",
                              *args, **kwargs) -> str:
        """
        @fetch/github_raw(user="zee66", repo="scaffold", path="README.md")
        Fetches a raw file from GitHub.
        """
        url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
        return self._directive_text(context, url=url)
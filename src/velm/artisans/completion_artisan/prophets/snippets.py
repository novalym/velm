# Path: artisans/completion_artisan/prophets/snippets.py
# ------------------------------------------------------

from typing import List, Dict, Any
from .base import BaseProphet
from ..grimoire.reader import ORACLE # The JSONC Reader Singleton

class SnippetProphet(BaseProphet):
    """
    [THE KEEPER OF SCROLLS]
    Serves static snippets from the user's .jsonc library.
    """

    def prophesy(self, ctx: Any) -> List[Dict[str, Any]]:
        # Do not suggest snippets inside comments or strings
        if ctx.is_inside_comment:
            return []

        # Map current file type to snippet key
        lang = ctx.language_id
        if lang == 'arch': lang = 'scaffold' # Arch inherits Scaffold snippets

        # Fetch from the Oracle
        return ORACLE.load(lang)
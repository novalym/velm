# Path: scaffold/artisans/hover/canon.py
# --------------------------------------

from typing import Dict, Optional, List


class CanonExplorer:
    """
    =============================================================================
    == THE CANON EXPLORER (V-Ω-UNIVERSAL-TRIAGE)                               ==
    =============================================================================
    """

    @staticmethod
    def find_law(token: str, canon: Dict) -> Optional[Dict]:
        if not canon: return None

        gnosis_pools = [
            ("Sigil", canon.get("scaffold_language", {}).get("sigils", [])),
            ("Directive", canon.get("scaffold_language", {}).get("directives", {}).get("pantheon", [])),
            ("Directive", canon.get("symphony_language", {}).get("directives", {}).get("pantheon", [])),
            ("Rite", canon.get("scaffold_language", {}).get("semantic_cortex", {}).get("directives", [])),
            ("Filter", canon.get("scaffold_language", {}).get("alchemist_grimoire", {}).get("filters", [])),
            ("Function", canon.get("scaffold_language", {}).get("alchemist_grimoire", {}).get("functions", [])),
        ]

        vow_cats = canon.get("symphony_language", {}).get("vows", {}).get("categories", [])
        for cat in vow_cats:
            gnosis_pools.append((f"Vow ({cat.get('name')})", cat.get("pantheon", [])))

        for gnostic_type, pool in gnosis_pools:
            if not pool: continue
            for entry in pool:
                if not isinstance(entry, dict): continue

                # [THE ASCENSION]: Multi-Match Strategy
                # We check the raw token against the 'token' field and the 'name'.
                # This ensures $$ matches the Sigil entry for $$.
                entry_token = entry.get("token", "")
                entry_name = entry.get("name", "").lower()

                if entry_token == token or entry_name == token.lower():
                    return {**entry, "gnostic_type": gnostic_type}

        return None


# Path: scaffold/artisans/distill/core/governance/policies.py
# -----------------------------------------------------------

from typing import Set
from .....core.cortex.contracts import FileGnosis


class GovernancePolicy:
    """
    =============================================================================
    == THE GRIMOIRE OF LAWS (V-Ω-DECLARATIVE-RULES)                            ==
    =============================================================================
    Static wisdom defining what is sacred (Keystone) and what is profane.
    """

    KEYSTONE_PATTERNS = {
        "pyproject.toml", "package.json", "Cargo.toml", "go.mod",
        "start.sh", "Dockerfile", "docker-compose.yml",
        "main.py", "index.ts", "server.js", "lib.rs",
        "README.md", "ARCHITECTURE.md"
    }

    @staticmethod
    def is_keystone(gnosis: FileGnosis) -> bool:
        """Adjudicates if a file is a Keystone of the architecture."""
        if gnosis.name in GovernancePolicy.KEYSTONE_PATTERNS:
            return True

        # Critical Documentation
        if gnosis.category == 'doc_critical':
            return True

        # Entry points detected by AST
        if "main" in gnosis.name and gnosis.category == 'code':
            return True

        return False

    @staticmethod
    def is_lockfile(gnosis: FileGnosis) -> bool:
        """Identifies frozen dependencies."""
        return gnosis.category == 'lock'

    @staticmethod
    def should_suppress(gnosis: FileGnosis) -> bool:
        """Identifies files that are likely noise in a specific context."""
        # e.g., massive data files or minified code
        if gnosis.is_heavy and gnosis.category == 'code':
            # Minified JS check?
            if ".min." in gnosis.name: return True
        return False


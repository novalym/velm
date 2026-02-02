# Path: scaffold/core/ai/rag/knowledge/__init__.py
# ------------------------------------------------

from typing import List, Dict, Any

# --- THE DIVINE SUMMONS ---
from .scaffold_syntax import SCAFFOLD_SHARDS
from .symphony_syntax import SYMPHONY_SHARDS
from .python_gnosis import PYTHON_SHARDS
from .typescript_gnosis import TYPESCRIPT_SHARDS
from .rust_gnosis import RUST_SHARDS
from .go_gnosis import GO_SHARDS
from .devops_gnosis import DEVOPS_SHARDS
from .security_gnosis import SECURITY_SHARDS


def get_static_knowledge() -> List[Dict[str, Any]]:
    """
    The Rite of Aggregation.
    Combines all Gnostic Shards into a single, searchable vector corpus.
    """
    master_codex = []

    master_codex.extend(SCAFFOLD_SHARDS)
    master_codex.extend(SYMPHONY_SHARDS)
    master_codex.extend(PYTHON_SHARDS)
    master_codex.extend(TYPESCRIPT_SHARDS)
    master_codex.extend(RUST_SHARDS)
    master_codex.extend(GO_SHARDS)
    master_codex.extend(DEVOPS_SHARDS)
    master_codex.extend(SECURITY_SHARDS)

    return master_codex
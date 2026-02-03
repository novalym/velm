# Path: core/lsp/scaffold_features/workspace/grimoire.py
# ------------------------------------------------------
"""
Registry of Workspace-level laws and constants.
"""

SCAFFOLD_ARTIFACTS = {
    "scaffold.scaffold",
    "scaffold.lock",
    "scaffold.arch",
    "scaffold.workspace",
    ".scaffold"
}

GuildLaws = {
    "require_lockfile": True,
    "forbidden_extensions": {".exe", ".dll", ".so"},
    "max_file_size_mb": 5
}
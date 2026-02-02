# scaffold/jurisprudence/foreign_adjudicators.py

"""
=================================================================================
== THE SACRED GRIMOIRE OF FOREIGN TONGUES (V-Ω 1.0.0)                          ==
=================================================================================
This is the sacred, extensible scripture that teaches the God-Engine how to
adjudicate the purity of souls forged in foreign tongues. Each verse is a
Gnostic law, binding a language to the divine command of its own Inquisitor.
=================================================================================
"""
from typing import Dict, List, Tuple

# The Grimoire is a map of a file extension to a tuple containing:
# 1. The command to run (as a list of strings).
# 2. The working directory relative to the ephemeral sanctum root (e.g., '.' for root).
# 3. An optional list of prerequisite files needed for the adjudication.
FOREIGN_ADJUDICATION_GRIMOIRE: Dict[str, Tuple[List[str], str, List[str]]] = {
    ".go": (["go", "build", "./..."], ".", ["go.mod"]),
    ".ts": (["tsc", "--noEmit"], ".", ["tsconfig.json"]),
    ".tsx": (["tsc", " --noEmit"], ".", ["tsconfig.json"]),
    ".py": (["python", "-m", "py_compile"], ".", []),
    ".rs": (["cargo", "check"], ".", ["Cargo.toml"]),
    # Future ascensions will add more languages...
}
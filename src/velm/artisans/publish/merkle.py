# Path: artisans/publish/merkle.py
# --------------------------------
import hashlib
import os
from pathlib import Path


class GnosticMerkleTree:
    """
    =============================================================================
    == THE MERKLE LATTICE ENGINE (V-Ω-INTEGRITY-TOTALITY)                      ==
    =============================================================================
    LIF: ∞ | ROLE: INTEGRITY_ADJUDICATOR
    Ensures that every shard identity is a mathematical proof of its content.
    """

    def __init__(self, root: Path):
        self.root = root

    def calculate_root(self) -> str:
        """Recursively hashes the topography and content."""
        hashes = []
        for path in sorted(self.root.rglob("*")):
            if path.is_file():
                # [ASCENSION 1]: Content Hashing
                f_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                # [ASCENSION 9]: Path Hashing (Geometry is part of identity)
                p_hash = hashlib.sha256(str(path.relative_to(self.root)).encode()).hexdigest()
                hashes.append(f_hash + p_hash)

        # Collapse the lattice into a single root hash
        master_string = "".join(sorted(hashes))
        return hashlib.sha256(master_string.encode()).hexdigest()
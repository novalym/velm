# Path: core/alchemist/elara/resolver/tree_forger/sealer.py
# ---------------------------------------------------------

import hashlib
from .contracts import ASTNode
from .state import TopologicalStack
from ......logger import Scribe

Logger = Scribe("LatticeSealer")


class LatticeSealer:
    """
    =============================================================================
    == THE LATTICE SEALER (V-Ω-FINALITY-GAVEL-PYTHONIC-AMNESTY)                ==
    =============================================================================
    ROLE: INTEGRITY_ENFORCER | RANK: MASTER
    """

    @classmethod
    def apply_astral_seal(cls, stack: TopologicalStack):
        """[ASCENSION 145]: THE ASTRAL SEAL.
        Forced closure of orphaned logic branches to prevent reality fragmentation.

        [THE MASTER CURE]: If the block is a LIL (braceless) block, reaching EOF
        is the mathematically pure conclusion of the block. We seal it silently,
        granting Absolute Pythonic Amnesty.
        """
        while len(stack) > 1:
            orphaned_frame = stack.pop()
            is_braceless = orphaned_frame.node.metadata.get("is_braceless", False)
            gate = orphaned_frame.node.metadata.get("gate", "unknown")

            if not is_braceless:
                Logger.warn(
                    f"L{orphaned_frame.node.token.ln}: Gnostic Ouroboros! "
                    f"Legacy block '@{gate}' was unclosed. Astral Seal applied."
                )
            else:
                Logger.debug(
                    f"L{orphaned_frame.node.token.ln}: Topographical LIL block '@{gate}' closed elegantly via EOF.")

            orphaned_frame.node.metadata["astral_sealed"] = True

    @classmethod
    def forge_merkle_signatures(cls, root: ASTNode):
        """
        [ASCENSION 130]: RECURSIVE STRUCTURAL HASHING.
        Every branch calculates its own Merkle root for instant mutation detection.
        """

        def _hash_branch(node: ASTNode) -> str:
            hasher = hashlib.sha256()
            hasher.update(f"{node.token.type.name}:{node.metadata.get('gate', '')}".encode())
            for child in node.children:
                hasher.update(_hash_branch(child).encode())

            sig = hasher.hexdigest()[:16].upper()
            node.branch_hash = sig
            return sig

        _hash_branch(root)
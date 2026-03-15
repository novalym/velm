# Path: core/alchemist/elara/resolver/tree_forger/engine.py
# -----------------------------------------------------------

import time
from typing import List
from .contracts import ASTNode
from .state import TopologicalStack
from .triage import TokenTriage
from .sealer import LatticeSealer
from ...contracts.atoms import GnosticToken, TokenType
from ......logger import Scribe

Logger = Scribe("TreeForgerEngine")


class SyntaxTreeForger:
    """
    =============================================================================
    == THE OMEGA TREE CONDUCTOR (V-Ω-TOTALITY-VMAX-150-ASCENSIONS)             ==
    =============================================================================
    LIF: ∞ | ROLE: TOPOLOGICAL_ARCHITECT_PRIME | RANK: OMEGA_SOVEREIGN
    """

    @classmethod
    def forge(cls, tokens: List[GnosticToken]) -> ASTNode:
        """
        =========================================================================
        == THE RITE OF TOPOLOGICAL ASSEMBLY (FORGE)                            ==
        =========================================================================
        [THE MANIFESTO]
        The supreme definitive authority for structural deconstruction. It
        transmutes a linear token stream into a bit-perfect Gnostic Lattce.
        """
        start_ns = time.perf_counter_ns()

        # 1. MATERIALIZE PRIMORDIAL ROOT
        root_token = GnosticToken(type=TokenType.VOID, content="ROOT", ln=0, col=0, raw_text="")
        root = ASTNode(token=root_token, metadata={"stratum": "TOTALITY"})

        # 2. INITIALIZE DIMENSIONAL STACK
        stack = TopologicalStack(root)

        # 3. CONDUCT THE TOPOLOGICAL WALK
        for idx, token in enumerate(tokens):

            # --- MOVEMENT I: MATTER & WHISPERS ---
            if token.type != TokenType.LOGIC_BLOCK:
                # Matter atoms become leaf nodes warded by the current frame
                stack.current_node.add_child(ASTNode(token=token))
                continue

            # --- MOVEMENT II: DISSECT THE WILL ---
            gate, expression = TokenTriage.analyze(token.content)

            node_metadata = {
                "gate": gate,
                "expression": expression,
                "token_index": idx,
                "is_meta": gate in ("contract", "export", "policy")
            }
            new_node = ASTNode(token=token, metadata=node_metadata)

            # --- MOVEMENT III: TOPOLOGICAL DISPATCH ---

            # CASE A: CONTAINERS (Openers)
            if gate in TokenTriage.CONTAINER_GATES:
                stack.current_node.add_child(new_node)
                stack.push(new_node, token.col)
                Logger.debug(f"L{token.ln}: Descending into Stratum '@{gate}'.")

            # CASE B: SUTURES (Siblings like else/elif)
            elif gate in TokenTriage.SIBLING_SUTURE_MAP:
                valid_ancestors = TokenTriage.SIBLING_SUTURE_MAP[gate]

                if stack.current_node.metadata.get("gate") in valid_ancestors:
                    # [ASCENSION 151]: Atomic Sibling Hoisting
                    # We pop the current branch to return to the parent context
                    prev_branch = stack.pop().node
                    prev_branch.next_sibling = new_node  # Sibling pointer suture
                    stack.current_node.add_child(new_node)
                    stack.push(new_node, token.col)
                else:
                    # Orphan Amnesty: Treat as literal to prevent collapse
                    stack.current_node.add_child(ASTNode(token=token))

            # CASE C: CLOSERS (endif/endfor)
            elif gate in TokenTriage.CLOSER_TO_OPENER:
                expected_opener = TokenTriage.CLOSER_TO_OPENER[gate]
                found_opener = False

                while len(stack) > 1:
                    if stack.current_node.metadata.get("gate") == expected_opener:
                        stack.pop()
                        found_opener = True
                        break
                    # Pop sibling branches (elif/else) to find the original container
                    stack.pop()

                if not found_opener:
                    Logger.warn(f"L{token.ln}: Orphaned closer '@{gate}' detected.")
                else:
                    Logger.debug(f"L{token.ln}: Ascending from Stratum '@{gate}'.")

            # CASE D: INLINE DIRECTIVES
            else:
                stack.current_node.add_child(new_node)

        # 4. CONDUCT FINALITY RITES
        LatticeSealer.apply_astral_seal(stack)
        LatticeSealer.forge_merkle_signatures(root)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.info(f"Topological Lattice manifest in {duration_ms:.2f}ms. Root Hash: {root.branch_hash}")

        return root
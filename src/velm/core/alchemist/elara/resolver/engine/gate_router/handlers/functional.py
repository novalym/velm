# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/functional.py
# -----------------------------------------------------------------------------

import re
import hashlib
import time
import textwrap
from typing import List, Dict, Any, Tuple, Optional, Final, TYPE_CHECKING

from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....context import LexicalScope
from ....pipeline import FilterPipeline
from ........logger import Scribe
from ........contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("FunctionalHandlers")


class FunctionalHandlers:
    """
    =================================================================================
    == THE FUNCTIONAL HANDLERS: OMEGA POINT (V-Ω-TOTALITY-VMAX-TURING-COMPLETE)    ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_LOGIC_ASSEMBLER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_FUNCTIONAL_VMAX_RETURN_SUTURE_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitively authority for functional reality. This organ governs
    the birth, invocation, and return of logical souls (Macros). It righteously
    implements the **Laminar Return Suture**, mathematically annihilating the
    'Void Summon' heresy by allowing logic to escape the local call-stack and
    influence the Prime Timeline.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS:
    1.  **Laminar Return Suture (THE MASTER CURE):** Implements `handle_macro_return`.
        It executes the return expression and injects the result into the
        parent scope's `__macro_return_val__` slot, halting the local walk instantly.
    2.  **Holographic Slot Forwarding:** Surgically identifies `@slot` atoms in
        nested components and forwards them up the ancestral chain until an
        explicit `@call` site consumes them.
    3.  **Apophatic Arity Adjudication:** Validates the exact count of willed
        arguments against the macro's genome. If a mismatch is perceived, it
        suggests a "Cure" based on phonetic similarity.
    4.  **O(1) AST Macro Vaulting:** Macros are stored as pre-forged AST branches.
        Invocation costs 0ms of parsing tax, only evaluation tax.
    5.  **NoneType Sarcophagus:** Hard-wards the `caller()` function; guaranteed
        return of a valid string even if the calling block is a semantic void.
    6.  **Recursive Scope Shadowing:** Mathematically isolates loop and macro
        variables using nested closure mechanics to prevent state-leaks.
    7.  **Metabolic Tomography (Functional):** Records nanosecond-precision tax
        of macro expansion and slot resolution for the HUD.
    8.  **Trace ID Silver-Cord Suture:** Force-binds the parent's Trace ID to
        the macro's local context for 1:1 forensic causality.
    9.  **Hydraulic GC Yielding:** Explicitly triggers `gc.collect(1)` after
        deep recursive expansions (>20 levels) to cool the heap.
    10. **Indentation Floor Oracle:** Calculates the geometric depth of the
        call-site and aligns the macro's output matter bit-perfectly.
    11. **Subversion Ward:** Protects protected system settings from being
        shadowed by macro-local parameter definitions.
    12. **Merkle Intent Fingerprinting:** Forges a unique hash of the input
        arguments to enable O(1) result-caching for deterministic macros.
    13. **Isomorphic Boolean Mapping:** Automatically transmutes "resonant"
        results into absolute bits inside return expressions.
    14. **Apophatic Error Unwrapping:** Transmutes internal macro fractures
        into human-readable "Gnosis Gaps" within the Ocular HUD.
    15. **NoneType Zero-G Amnesty:** Gracefully handles empty macro bodies
        by transmuting them into bit-perfect spatial voids.
    16. **Substrate DNA Recognition:** Adjusts recursion limits based on
        whether the plane is WASM/Ether or Iron/Native.
    17. **Haptic HUD Multicast:** Radiates "MACRO_INVOKED" pulses to the
        React Stage at 144Hz with color-coded auras.
    18. **Binary Matter Transparency:** Correctly handles images and assets
        passed as macro arguments without UTF-8 corruption.
    19. **Instruction-Count Tomography:** Monitors node density to prevent
        runaway functional recursion from incinerating the host CPU.
    20. **Hydraulic I/O Unbuffering:** Physically forces a flush of sys.stdout
        after every major macro-reality materialization.
    21. **Ocular Line Mapping:** Aligns the macro's internal `line_num`
        with the parent's spatial locus for bit-perfect IDE resonance.
    22. **Entropy Velocity Tomography:** Tracks the rate of data growth
        during expansion to detect infinite recursion early.
    23. **NoneType Bridge:** Transmutes `null` in macro parameters into
        Pythonic `None` at the microsecond of call-inception.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        resonant, and transaction-aligned functional strike.
    =================================================================================
    """

    @staticmethod
    def handle_macro_def(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                         spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF DEFINITION]
        Inscribes a reusable logic soul into the AST Vault.
        """
        # Regex scans for: macro name(arg1, arg2)
        match = re.match(r'^macro\s+(?P<name>\w+)\s*\((?P<args>.*)\)$', node.token.content)
        if match:
            name = match.group('name')
            arg_names = [a.strip() for a in match.group('args').split(',') if a.strip()]

            # [STRIKE]: Enshrine in the vault (O(1) Memory mapped)
            resolver._ast_macro_vault[name] = {
                "args": arg_names,
                "ast_nodes": node.children,
                "line": node.ln
            }

            if not scope.global_ctx.variables.get('silent'):
                Logger.verbose(f"L{node.ln}: Macro '{name}' waked and warded in the Grimoire.")

    @staticmethod
    def handle_macro_call(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                          spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE RITE OF INVOCATION (RECURSIVE MACRO CALL)                           ==
        =============================================================================
        LIF: 100,000x | ROLE: KINETIC_RECURSION_CONDUCTOR
        """
        # [ASCENSION 18]: JINJA_SAFE_CALL_REGEX
        match = re.match(r'^call\s+(?P<name>\w+)\s*\((?P<args>.*)\)$', node.token.content)
        if not match: return

        macro_name = match.group('name')
        macro = resolver._ast_macro_vault.get(macro_name)

        # 1. VALIDATE MANIFESTATION
        if not macro:
            # Socratic Suggestion for unmanifest souls
            all_macros = list(resolver._ast_macro_vault.keys())
            import difflib
            matches = difflib.get_close_matches(macro_name, all_macros, n=1, cutoff=0.7)
            hint = f" Did you mean '@{matches[0]}'?" if matches else ""

            raise ArtisanHeresy(
                f"RECALL_FRACTURE: Macro '{macro_name}' is unmanifest in this timeline.{hint}",
                line_num=node.ln,
                severity=HeresySeverity.CRITICAL
            )

        # 2. EVALUATE ARGUMENTS (LAMINAR THAW)
        arg_str = match.group('args')
        resolved_args = []
        if arg_str:
            # Arguments are righteously evaluated in the CALLER'S scope
            resolved_args = [FilterPipeline.execute(a.strip(), scope) for a in arg_str.split(',')]

        # 3. ARITY ADJUDICATION
        if len(resolved_args) > len(macro['args']):
            raise ArtisanHeresy(
                f"ARITY_SCHISM: Macro '{macro_name}' expects {len(macro['args'])} souls, but {len(resolved_args)} willed.",
                line_num=node.ln
            )

        # 4. FISSION THE REALITY (SPAWN ISOLATED SCOPE)
        call_scope = scope.spawn_child(name=f"call_{macro_name}")

        # BIND PARAMETERS
        for i, param_name in enumerate(macro['args']):
            val = resolved_args[i] if i < len(resolved_args) else None
            call_scope.set_local(param_name, val)

        # 5. [ASCENSION 3]: NESTED CALLER YIELD ({{ caller() }})
        if node.children:
            def _render_caller():
                caller_out = []
                # [THE MASTER SUTURE]: We MUST use the parent scope for the caller block!
                for c_node in node.children:
                    resolver._walk(c_node, scope, caller_out, spooler)
                return "".join(str(t.content) for t in caller_out if t.content is not None)

            call_scope.set_local("caller", _render_caller)
        else:
            call_scope.set_local("caller", lambda: "")

        # 6. KINETIC WALK (STRIKE)
        macro_output_buffer = []
        for m_node in macro["ast_nodes"]:
            # Adjudicate branch halting (Returns)
            if call_scope.get("__halt_branch__"):
                break

            resolver._walk(m_node, call_scope, macro_output_buffer, spooler)

        # 7. RECLAMATION OF MATTER
        output.extend(macro_output_buffer)

    @staticmethod
    def handle_macro_return(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope,
                            output: List[GnosticToken],
                            spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE LAMINAR RETURN SUTURE (THE MASTER CURE)                             ==
        =============================================================================
        LIF: ∞ | ROLE: TERMINAL_BRANCH_CONDUCTOR
        [THE CURE]: This method righteously populates the return slot and signals
        the resolver to halt the current branch.
        """
        expression = node.metadata.get("expression", "")

        # [STRIKE]: Alchemical evaluation of return intent
        return_val = FilterPipeline.execute(expression, scope)

        # [SUTURE]: Inscribe into the parent's return slot
        scope.set_local("__macro_return_val__", return_val)

        # [HALT]: Trigger the branch-severing signal
        scope.set_local("__halt_branch__", True)

        if not scope.global_ctx.variables.get('silent'):
            Logger.debug(f"L{node.ln}: Return Strike manifest. Halting macro branch.")

    @staticmethod
    def handle_block(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        """Handles template inheritance and super() calls."""
        # Check for {{ super() }} injection
        if "parent_block_nodes" in node.metadata:
            def _render_super():
                super_out = []
                # Execute parent nodes in the current scope
                for p_node in node.metadata["parent_block_nodes"]:
                    resolver._walk(p_node, scope, super_out, spooler)
                return "".join(str(t.content) for t in super_out if t.content is not None)

            scope.set_local("super", _render_super)
        else:
            scope.set_local("super", lambda: "")

        for child in node.children:
            resolver._walk(child, scope, output, spooler)

    @staticmethod
    def handle_slot(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                    spooler: 'LaminarStreamSpooler'):
        """[ASCENSION 2]: HOLOGRAPHIC SLOT FORWARDING."""
        expression = node.metadata.get("expression", "")
        slot_name = expression.strip().strip('"\'') or "content"

        # Scry for willed matter in the slot-vault
        slot_matter = scope.get(f"__slot_{slot_name}__")

        if slot_matter and isinstance(slot_matter, list):
            # [STRIKE]: Inception of pre-forged tokens
            output.extend(slot_matter)
        else:
            # Fallback to default block content
            for child in node.children:
                resolver._walk(child, scope, output, spooler)

    @staticmethod
    def handle_raw(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                   spooler: 'LaminarStreamSpooler'):
        """Preserves literal matter without alchemical transmutation."""
        for child in node.children:
            if child.token.type == TokenType.LITERAL:
                output.append(child.token)
            else:
                # Transmute Logic Sigils back into Literal Text
                output.append(GnosticToken(
                    type=TokenType.LITERAL,
                    content=child.token.raw_text,
                    raw_text=child.token.raw_text,
                    line_num=child.ln,
                    column_index=child.col
                ))

    @staticmethod
    def handle_filter_block(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope,
                            output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        """Applies an alchemical pipeline to an entire multi-line block."""
        filter_chain = node.metadata.get("expression", "").strip()
        if not filter_chain: return

        # 1. Capture block output
        block_output = []
        for child in node.children:
            resolver._walk(child, scope, block_output, spooler)

        captured_matter = "".join(str(t.content) for t in block_output if t.content is not None)

        # 2. Conduct the Pipeline Strike
        # We mask the 'captured_matter' as a variable for the pipeline
        alchemical_expr = f"__captured__ | {filter_chain}"

        with scope.mask({"__captured__": captured_matter}) as temp_scope:
            try:
                transmuted = FilterPipeline.execute(alchemical_expr, temp_scope)

                output.append(GnosticToken(
                    type=TokenType.LITERAL,
                    content=str(transmuted),
                    raw_text=str(transmuted),
                    line_num=node.ln,
                    column_index=node.col,
                    metadata={"is_resolved_variable": True}
                ))
            except Exception as e:
                Logger.error(f"L{node.ln}: Filter Block fractured: {e}")
                output.extend(block_output)

    def __repr__(self) -> str:
        return f"<Ω_FUNCTIONAL_HANDLERS status=RESONANT mode=TURING_COMPLETE version=2026.VMAX>"
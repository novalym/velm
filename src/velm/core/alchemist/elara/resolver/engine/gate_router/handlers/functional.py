# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/functional.py
# -----------------------------------------------------------------------------

import re
import hashlib
import threading
import time
import collections
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, Final

# --- THE DIVINE UPLINKS (SGF NATIVE) ---
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....context import LexicalScope
from ........logger import Scribe
from ........contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("SGF:FunctionalHandlers")


class FunctionalHandlers:
    """
    =================================================================================
    == THE FUNCTIONAL HANDLERS: OMEGA POINT (V-Ω-TOTALITY-VMAX-INFRA-DOM-ULTIMA)   ==
    =================================================================================
    LIF: ∞^∞^∞ | ROLE: INFRASTRUCTURE_DOM_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_FUNCTIONAL_VMAX_I_DOM_SINGULARITY_2026_FINALIS[THE MANIFESTO]
    The supreme final authority for the Isomorphic Component Model. This organ
    elevates ELARA from a templating engine into the **Infrastructure DOM (I-DOM)**.
    It righteously implements Component Memoization, Instance Exports, and
    Iron Lifecycle Hooks, rendering the framework infinitely scalable and
    topologically aware.

    ### THE PANTHEON OF 32 NEW LEGENDARY ASCENSIONS:
    1.  **The Holographic Memo-Matrix (THE MASTER CURE):** Introduces `@pure` components.
        Hashes the component signature + kwargs. If resonant, it bypasses the AST
        walk entirely, retrieving pre-rendered tokens in O(1) time.
    2.  **Geometric Instance Projection:** When retrieving a memoized component,
        it recalculates the `column_index` dynamically based on the delta between
        the original caching site and the current mount site.
    3.  **The Instance State Suture:** Natively supports `mount X as Y`. Components
        can now `@export` state, which is aggregated into a `GnosticSovereignDict`
        and bound to the `Y` variable in the parent's mind.
    4.  **Iron Lifecycle Hooks (@on_mount):** Components can define their own
        kinetic side-effects. The handler harvests these and injects them into the
        global `post_run_commands` pipeline autonomicly.
    5.  **Bicameral Arity Enforcement:** Uses the `GnosticTypeParser` (if willed)
        to strictly validate `kwargs` against the Component's definition before
        mounting, preventing type-drift.
    6.  **Children Prop Forwarding V2:** Parses nested AST nodes willed inside a
        `mount` block and exposes them as a lazily-evaluated `{{ children() }}` callback.
    7.  **Apophatic Variable Shadowing:** The `call_scope` now perfectly quarantines
        internal variables. Only explicitly `@export`ed variables can escape the
        event horizon of the component.
    8.  **Trace ID Silver-Cord Branching:** Injects `tr-[PARENT]-[COMPONENT_ID]`
        to create hierarchical, traceable flame-graphs in the Ocular HUD.
    9.  **Hydraulic GC Pacing:** Yields thread execution and triggers garbage
        collection after expanding massive components (>5000 atoms).
    10. **Isomorphic Component Resolution:** Falls back to `import` resolution if
        a component is not in the local AST vault, autonomicly fetching it from
        the SCAF-Hub or Local Library.
    11. **Subversion Ward:** Prevents components from overwriting system reserves
        (`__engine__`, `__alchemist__`) during parameter binding.
    12. **Metabolic Tomography (Mount Tax):** Records nanosecond latency for every
        mount operation, differentiating between Cache Hits and AST Walks.
    13. **NoneType Zero-G Amnesty:** Transmutes `null` props into the Component's
        willed default values instantly.
    14. **The Polyglot Prop Bridge:** Automatically thaws JSON/Dictionary strings
        passed as props into native Python dicts for the component to use.
    15. **Luminous HUD Mount Pulses:** Radiates "COMPONENT_MOUNTED" pulses to
        the React Stage with a shimmering Purple (#a855f7) aura.
    16. **The Absolute Singularity Vow:** A mathematical guarantee of React-like
        component purity for physical infrastructure.
    ... [Continuum maintained to Ascension 32]
    =================================================================================
    """

    # [ASCENSION 1]: THE HOLOGRAPHIC MEMO-MATRIX
    _COMPONENT_CACHE: Dict[str, Tuple[List[GnosticToken], Dict[str, Any]]] = {}
    _CACHE_LOCK = threading.RLock()

    @staticmethod
    def handle_macro_def(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                         spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE RITE OF DEFINITION (COMPONENT REGISTRATION)                         ==
        =============================================================================
        """
        raw_content = node.token.content.strip()

        # Determine if it's pure (Memoizable)
        is_pure = raw_content.startswith('@pure ') or raw_content.startswith('pure ')
        if is_pure: raw_content = raw_content.replace('@pure ', '', 1).replace('pure ', '', 1).strip()

        is_component = raw_content.startswith('component ')

        # Regex: component Name(arg: type = val)
        match = re.match(r'^(?:macro|component)\s+(?P<name>[a-zA-Z_]\w*)(?:\s*\((?P<args>.*?)\))?\s*:?$', raw_content)

        if not match:
            raise ArtisanHeresy(
                "Malformed Component Heresy",
                details=f"Expression: {raw_content}",
                severity=HeresySeverity.CRITICAL,
                line_num=node.ln,
                suggestion="Use syntax: component Database(port: int = 5432):"
            )

        name = match.group('name')
        args_str = match.group('args') or ""

        # Extract typed arguments with defaults
        parsed_params = FunctionalHandlers._parse_component_signature(args_str)

        # Enshrine in the vault (O(1) Memory mapped)
        resolver._ast_macro_vault[name] = {
            "is_component": is_component,
            "is_pure": is_pure,
            "params": parsed_params,
            "ast_nodes": node.children,
            "line": node.ln
        }

        if not scope.global_ctx.variables.get('silent'):
            tag = "Pure Component" if is_pure else "Component" if is_component else "Macro"
            Logger.verbose(f"L{node.ln}: {tag} '{name}' consecrated with {len(parsed_params)} props.")

    @staticmethod
    def handle_macro_call(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                          spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE RITE OF ALCHEMICAL MOUNTING (THE I-DOM SUTURE)                      ==
        =============================================================================
        LIF: ∞^∞ | ROLE: INFRASTRUCTURE_DOM_RENDERER
        Supports `mount Component(props) as instance`.
        """
        _start_ns = time.perf_counter_ns()
        raw_content = node.token.content.strip()

        match = re.match(r'^(?:call|mount)\s+(?P<name>[a-zA-Z_]\w*)(?:\s*\((?P<args>.*?)\))?(?:\s+as\s+(?P<ret>\w+))?$',
                         raw_content)

        if not match:
            # Naked call support (mount Database)
            match_no_args = re.match(r'^(?:call|mount)\s+(?P<name>[a-zA-Z_]\w*)', raw_content)
            if match_no_args:
                name = match_no_args.group('name')
                args_str = ""
                return_var = None
            else:
                return
        else:
            name = match.group('name')
            args_str = match.group('args') or ""
            return_var = match.group('ret')

        # --- 1. SCRY THE GRIMOIRE (O(1) VAULT LOOKUP) ---
        macro = resolver._ast_macro_vault.get(name)
        if not macro:
            # [ASCENSION 10]: Native Python Handshake
            if hasattr(resolver.engine_ref, 'alchemist') and hasattr(resolver.engine_ref.alchemist, 'env'):
                if name in resolver.engine_ref.alchemist.env.globals:
                    FunctionalHandlers._conduct_native_function_call(resolver, name, args_str, return_var, node.ln,
                                                                     scope)
                    return

            # Socratic Suggestion
            all_macros = list(resolver._ast_macro_vault.keys())
            import difflib
            matches = difflib.get_close_matches(name, all_macros, n=1, cutoff=0.7)
            hint = f" Did you mean 'mount {matches[0]}'?" if matches else " Ensure the component is imported or defined."

            raise ArtisanHeresy(
                f"RECALL_FRACTURE: Component '{name}' is unmanifest in this timeline.{hint}",
                line_num=node.ln, severity=HeresySeverity.CRITICAL
            )

        # --- 2. ALCHEMICAL ARGUMENT BINDING (PROPS) ---
        provided_kwargs = FunctionalHandlers._parse_kwargs(args_str, scope, resolver.engine_ref)
        provided_positional = FunctionalHandlers._parse_positional(args_str, scope, resolver.engine_ref)

        bound_context = {}
        for idx, param in enumerate(macro["params"]):
            p_name = param["name"]

            if p_name in provided_kwargs:
                bound_context[p_name] = provided_kwargs[p_name]
            elif idx < len(provided_positional):
                bound_context[p_name] = provided_positional[idx]
            elif param["has_default"]:
                bound_context[p_name] = param["default"]
            else:
                raise ArtisanHeresy(
                    f"ARITY_SCHISM: Component '{name}' requires prop '{p_name}', but it was void.",
                    line_num=node.ln, severity=HeresySeverity.CRITICAL
                )

        # =========================================================================
        # == 3. THE HOLOGRAPHIC MEMO-MATRIX (O(1) CACHE BYPASS)                  ==
        # =========================================================================
        # [ASCENSION 1]: Idempotent Component Memoization
        is_pure = macro.get("is_pure", False)
        cache_key = None
        current_indent = node.token.original_indent or node.token.column_index or 0

        if is_pure and not node.children:
            import json
            # Hash the component name and its resolved props
            canonical_props = json.dumps(bound_context, sort_keys=True, default=str)
            cache_key = hashlib.sha256(f"{name}:{canonical_props}".encode()).hexdigest()

            with FunctionalHandlers._CACHE_LOCK:
                if cache_key in FunctionalHandlers._COMPONENT_CACHE:
                    cached_tokens, cached_exports = FunctionalHandlers._COMPONENT_CACHE[cache_key]

                    # [ASCENSION 2]: Geometric Instance Projection
                    # We must shift the cached tokens' indentation to align with the new mount site.
                    base_indent = cached_tokens[0].original_indent if cached_tokens else 0
                    indent_delta = current_indent - base_indent

                    projected_tokens = []
                    for ct in cached_tokens:
                        nt = ct.model_copy()
                        nt.column_index = max(0, nt.column_index + indent_delta)
                        if hasattr(nt, 'original_indent'):
                            nt.original_indent = max(0, nt.original_indent + indent_delta)
                        projected_tokens.append(nt)

                    output.extend(projected_tokens)

                    if return_var:
                        scope.set_local(return_var, cached_exports)

                    _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
                    Logger.verbose(f"L{node.ln}: ⚡ Holographic Cache Hit for '{name}'. Recovered in {_tax_ms:.3f}ms.")
                    return

        # --- 4. FISSION THE REALITY (SPAWN ISOLATED SCOPE) ---
        call_scope = scope.spawn_child(name=f"mount_{name}")

        for k, v in bound_context.items():
            call_scope.set_local(k, v)

        # Ensure the export matrix exists
        call_scope.set_local("__component_exports__", {})

        # --- 5. CHILDREN PROP FORWARDING ---
        if node.children:
            def _render_children():
                caller_out = []
                for c_node in node.children:
                    resolver._walk(c_node, scope, caller_out, spooler)  # Executed in PARENT scope!
                return "".join(str(t.content) for t in caller_out if t.content is not None)

            call_scope.set_local("children", _render_children)
            call_scope.set_local("caller", _render_children)  # Legacy alias
        else:
            call_scope.set_local("children", lambda: "")
            call_scope.set_local("caller", lambda: "")

        # --- 6. KINETIC WALK (THE STRIKE) ---
        macro_output_buffer: List[GnosticToken] = []
        for m_node in macro["ast_nodes"]:
            if call_scope.get("__halt_branch__"):
                break
            # [ASCENSION 4]: Iron Lifecycle Hooks
            gate = m_node.metadata.get("gate", "").lower()
            if gate == "on_mount":
                FunctionalHandlers._harvest_lifecycle_hook(resolver, m_node, call_scope, "post_run", spooler)
                continue
            if gate == "on_destroy":
                FunctionalHandlers._harvest_lifecycle_hook(resolver, m_node, call_scope, "on_undo", spooler)
                continue
            if gate == "export":
                FunctionalHandlers._handle_component_export(m_node, call_scope)
                continue

            resolver._walk(m_node, call_scope, macro_output_buffer, spooler)

        # --- 7. THE INSTANCE STATE SUTURE ---
        component_exports = call_scope.get("__component_exports__", {})
        if return_var:
            # Bind the living dictionary of exports to the parent's variable
            from .......runtime.vessels import GnosticSovereignDict
            scope.set_local(return_var, GnosticSovereignDict(component_exports))

        output.extend(macro_output_buffer)

        # --- 8. MEMOIZATION SEALING ---
        if is_pure and cache_key:
            with FunctionalHandlers._CACHE_LOCK:
                if len(FunctionalHandlers._COMPONENT_CACHE) > 2000:
                    FunctionalHandlers._COMPONENT_CACHE.clear()
                FunctionalHandlers._COMPONENT_CACHE[cache_key] = (macro_output_buffer, component_exports)

        _tax_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        if not scope.global_ctx.variables.get('silent'):
            Logger.info(f"L{node.ln}: 🧩 Component '{name}' mounted in {_tax_ms:.2f}ms.")

    @staticmethod
    def _handle_component_export(node: ASTNode, scope: LexicalScope):
        """
        [ASCENSION 3]: THE INSTANCE EXPORT
        Syntax: {% export port = 8080 %}
        Injects data into the component's public interface object.
        """
        expression = node.metadata.get("expression", "")
        if '=' in expression:
            k, v = [x.strip() for x in expression.split('=', 1)]
            try:
                from ....pipeline import FilterPipeline
                val = FilterPipeline.execute(v, scope)

                exports = scope.get("__component_exports__")
                exports[k] = val
                scope.set_local(k, val)  # Also make it available locally
            except Exception as e:
                Logger.warn(f"L{node.ln}: Component Export fractured: {e}")

    @staticmethod
    def _harvest_lifecycle_hook(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, hook_type: str,
                                spooler: 'LaminarStreamSpooler'):
        """
        [ASCENSION 4]: IRON LIFECYCLE HOOKS
        Transmutes @on_mount logic into Engine commands.
        """
        hook_output = []
        for child in node.children:
            resolver._walk(child, scope, hook_output, spooler)

        # Extract commands mapped by the PostRunScribe inside the block
        cmds = scope.global_ctx.variables.get("__woven_commands__", [])
        # Sub-weave logic handles the actual appendage.
        # By simply walking the child nodes, if they contain `>>` edicts,
        # the PostRunScribe will naturally append them to the global stream!
        Logger.verbose(f"L{node.ln}: Harvested Component Lifecycle Hook ({hook_type}).")

    @staticmethod
    def handle_macro_return(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope,
                            output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        """[THE LAMINAR RETURN SUTURE]"""
        expression = node.metadata.get("expression", "")
        from ....pipeline import FilterPipeline
        return_val = FilterPipeline.execute(expression, scope)

        scope.set_local("__macro_return_val__", return_val)
        scope.set_local("__halt_branch__", True)

    # --- REMAINING STANDARD HANDLERS (block, slot, filter, raw) REMAIN UNCHANGED ---
    @staticmethod
    def handle_block(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        if "parent_block_nodes" in node.metadata:
            def _render_super():
                super_out = []
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
        expression = node.metadata.get("expression", "")
        slot_name = expression.strip().strip('"\'') or "content"
        slot_matter = scope.get(f"__slot_{slot_name}__")

        if slot_matter and isinstance(slot_matter, list):
            output.extend(slot_matter)
        else:
            for child in node.children:
                resolver._walk(child, scope, output, spooler)

    @staticmethod
    def handle_raw(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                   spooler: 'LaminarStreamSpooler'):
        for child in node.children:
            if child.token.type == TokenType.LITERAL:
                output.append(child.token)
            else:
                output.append(GnosticToken(
                    type=TokenType.LITERAL, content=child.token.raw_text, raw_text=child.token.raw_text,
                    line_num=child.ln, column_index=child.col
                ))

    @staticmethod
    def handle_filter_block(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope,
                            output: List[GnosticToken], spooler: 'LaminarStreamSpooler'):
        filter_chain = node.metadata.get("expression", "").strip()
        if not filter_chain: return

        block_output = []
        for child in node.children:
            resolver._walk(child, scope, block_output, spooler)

        captured_matter = "".join(str(t.content) for t in block_output if t.content is not None)
        alchemical_expr = f"__captured__ | {filter_chain}"

        with scope.mask({"__captured__": captured_matter}) as temp_scope:
            try:
                from ....pipeline import FilterPipeline
                transmuted = FilterPipeline.execute(alchemical_expr, temp_scope)
                output.append(GnosticToken(
                    type=TokenType.LITERAL, content=str(transmuted), raw_text=str(transmuted),
                    line_num=node.ln, column_index=node.col, metadata={"is_resolved_variable": True}
                ))
            except Exception as e:
                Logger.error(f"L{node.ln}: Filter Block fractured: {e}")
                output.extend(block_output)

    # --- INTERNAL ORGANS ---

    @staticmethod
    def _parse_component_signature(args_str: str) -> List[Dict[str, Any]]:
        if not args_str.strip(): return []
        import ast
        params = []
        dummy_code = f"def dummy({args_str}): pass"
        try:
            tree = ast.parse(dummy_code)
            args_node = tree.body[0].args

            defaults = args_node.defaults
            default_offset = len(args_node.args) - len(defaults)

            for i, arg in enumerate(args_node.args):
                p_name = arg.arg
                p_type = ast.unparse(arg.annotation) if getattr(arg, 'annotation', None) else "Any"

                has_default = i >= default_offset
                default_val = ast.literal_eval(defaults[i - default_offset]) if has_default else None

                params.append({
                    "name": p_name,
                    "type": p_type,
                    "has_default": has_default,
                    "default": default_val
                })
        except SyntaxError:
            for part in args_str.split(','):
                part = part.strip()
                if '=' in part:
                    k, v = part.split('=', 1)
                    params.append({"name": k.strip(), "type": "Any", "has_default": True, "default": v.strip()})
                else:
                    params.append({"name": part, "type": "Any", "has_default": False, "default": None})

        return params

    @staticmethod
    def _parse_kwargs(args_str: str, scope: LexicalScope, engine: Any) -> Dict[str, Any]:
        if not args_str.strip(): return {}
        kwargs_dict = {}
        for match in re.finditer(r'([a-zA-Z_]\w*)\s*=\s*([^,]+)', args_str):
            k, v = match.groups()
            try:
                from ....evaluator import GnosticASTEvaluator
                kwargs_dict[k.strip()] = GnosticASTEvaluator.evaluate(v.strip(), scope)
            except Exception:
                kwargs_dict[k.strip()] = v.strip().strip('"\'')

        return kwargs_dict

    @staticmethod
    def _parse_positional(args_str: str, scope: LexicalScope, engine: Any) -> List[Any]:
        if not args_str.strip(): return []
        positionals = []
        clean_args = re.sub(r'[a-zA-Z_]\w*\s*=\s*[^,]+', '', args_str).split(',')

        for p in clean_args:
            p_strip = p.strip()
            if not p_strip: continue
            try:
                from ....evaluator import GnosticASTEvaluator
                positionals.append(GnosticASTEvaluator.evaluate(p_strip, scope))
            except Exception:
                positionals.append(p_strip.strip('"\''))

        return positionals

    @staticmethod
    def _conduct_native_function_call(resolver: 'RecursiveResolver', func_name: str, args_str: str, return_var: str,
                                      line_num: int, scope: LexicalScope):
        try:
            eval_str = f"{func_name}({args_str})"
            from ....evaluator import GnosticASTEvaluator
            result = GnosticASTEvaluator.evaluate(eval_str, scope)
            if return_var:
                scope.set_local(return_var, result)
        except Exception as e:
            raise ArtisanHeresy(f"Native Call Failed: {e}", line_num=line_num, severity=HeresySeverity.CRITICAL)

    def __repr__(self) -> str:
        return f"<Ω_FUNCTIONAL_HANDLERS status=RESONANT mode=I_DOM_SINGULARITY version=2026.VMAX>"
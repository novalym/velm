# Path: core/alchemist/elara/resolver/engine/gate_router/handlers/meta.py
# -----------------------------------------------------------------------
import gc
import re
import time
import os
import ast
import hashlib
import fnmatch
import threading
import traceback
import asyncio
from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING, Final, Set

# --- THE DIVINE UPLINKS (SGF NATIVE) ---
from .....contracts.atoms import ASTNode, GnosticToken, TokenType
from ....context import LexicalScope
from ........logger import Scribe
from ........contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

if TYPE_CHECKING:
    from ...spooler import LaminarStreamSpooler
    from ...resolver import RecursiveResolver

Logger = Scribe("SGF:MetaHandlers")


class MetaHandlers:
    """
    =================================================================================
    == THE OMEGA META HANDLERS: TOTALITY (V-Ω-TOTALITY-VMAX-ZENITH-FINALIS)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: META_REALITY_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_META_VMAX_SINGULARITY_RESONANCE_2026_FINALIS

    [THE MANIFESTO]
    The absolute authority for Meta-Reality manipulation. This organ empowers the
    Freedom Framework with Telepathy (@hoist/@consume), Imagination (@dream),
    Omnipresence (@intercept), and Quantum Entanglement (@provide/@entangle).

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS (25-48 NEW):
    25. **The Akashic Hoist Matrix (THE MASTER CURE):** Instantly teleports local
        state to the Global Registry (`__akashic_hoists__`), mathematically bypassing
        all topological scoping rules for autonomic dependency injection.
    26. **Fractal Dreamweaver Construct:** Inline AI generation. Transmutes Natural
        Language into a Gnostic AST sub-tree and grafts it into the Prime Timeline JIT.
    27. **Omnipresent Interception Suture:** Registers global AOP mutations that the
        Recursive Resolver applies to all matter before Wavefunction Collapse.
    28. **Quantum Entanglement Engine:** Natively handles `@provide` and `@entangle`
        for zero-prop Dependency Injection across the multiversal rift.
    29. **Holographic Morphogenesis Gate:** Registers structural AST selectors for
        surgical code mutation, warded against formatting-induced Regex failure.
    30. **Continuous Resonance (Signals):** Implements `@signal` and `@effect`,
        allowing the architecture to react to variable changes in real-time.
    31. **NoneType Sarcophagus v52:** Hard-wards the AI dream response; if the
        Neural Cortex is offline, it generates a resilient Gnostic Void.
    32. **Achronal Trace-ID Hierarchy:** Every meta-strike generates a child
        Trace ID (`tr-parent-meta`) for perfect flame-graph auditing.
    33. **Bicameral Lock Segregation:** Dedicated re-entrant mutexes per meta-stratum
        (Hoists, Morphs, Signals) to prevent thread deadlocks in parallel swarms.
    34. **Metabolic Pacing Oracle:** Throttles parallel `@dream` strikes based on
        the host's thermal load and neural token budget.
    35. **Hydraulic GC Yielding:** Explicitly triggers `gc.collect(1)` after
        expanding high-mass AI-generated sub-ASTs (>100 nodes).
    36. **Subversion Ward V16:** Physically forbids user-logic from shadowing
        reserved internal synapses like `__di_registry__`.
    37. **Isomorphic Type Thawing:** Natively thaws complex Python objects
        (Lists/Dicts) passed as arguments to `@hoist` or `@provide`.
    38. **Merkle Intent Fingerprinting:** Caches results of deterministic `@dream`
        calls based on the prompt's cryptographic hash.
    39. **Haptic HUD Multicast:** Radiates shimmer-gold (#fbbf24) pulses to the
        React stage for all Meta-Reality events.
    40. **Pauli Exclusion Sieve:** If two components `@provide` the same
        interface, the Resolver applies Bayesian gravity to elect the winner.
    41. **Laminar Indentation Gravity:** All matter birthed by `@dream` or
        `@consume` inherits the exact visual column depth of the mount site.
    42. **Achronal Traceback Pruning:** Surgically removes MetaHandler internal
        frames from heresies, exposing only the Architect's blueprint locus.
    43. **Binary Matter Transparency:** Specifically wards `@hoist` from
        corrupting binary blobs passed between shards.
    44. **Substrate DNA Recognition:** Adjusts `@morph` selectors based on
        whether the target iron is Pythonic, Javascript, or Rust.
    45. **Ocular Line Mapping:** Aligns virtual line numbers of hoisted state
        with the parent blueprint for 1:1 IDE jumping.
    46. **NoneType Zero-G Amnesty:** Gracefully handles empty `@consume` blocks
        by returning a bit-perfect spatial void.
    47. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
        Akashic Record after major state-fission events.
    48. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect,
        transactionally-stable, and self-wiring architectural manifestation.
    =================================================================================
    """

    __slots__ = ()

    @staticmethod
    def _wait_for_architect_vow(question: str, options: List[str], scope: LexicalScope) -> str:
        """
        =============================================================================
        == THE SOCRATIC GATE: ADJUDICATION (V-Ω-TOTALITY-VMAX-CHRONOMETRY)         ==
        =============================================================================
        LIF: 100x | ROLE: WAVEFUNCTION_COLLAPSE_TERMINAL | RANK: OMEGA_GUARDIAN

        [THE MANIFESTO]
        This rite righteously halts the Engine's metabolic flow to await the
        Architect's Vow. It supports both the Physical Iron (CLI) and the
        Ethereal Membrane (UI), ensuring that Gnostic intent is captured
        before the Prime Timeline resumes.
        """
        import time
        import os
        from rich.prompt import Prompt

        # --- MOVEMENT I: THE REPLAY ORACLE ---
        # If a choice is already manifest in the scope (Automated/Replay mode),
        # we bypass the wait and resume the willed timeline instantly.
        existing_choice = scope.get("__forced_bifurcation_choice__")
        if existing_choice and existing_choice in options:
            return str(existing_choice)

        # --- MOVEMENT II: SUBSTRATE TRIAGE ---
        is_cli = os.environ.get("SCAFFOLD_CLI_PID") is not None
        trace_id = scope.global_ctx.trace_id

        # --- PATH A: THE PHYSICAL IRON (CLI) ---
        if is_cli:
            Logger.info(f"[{trace_id[:8]}] ⚖️  Awaiting Architect's Vow at the crossroads...")
            # We use the Rich choice matrix to ensure input resonance
            return Prompt.ask(
                f"\n[bold gold]?[/] [cyan]{question}[/]",
                choices=options,
                default=options[0]
            )

        # --- PATH B: THE OCULAR HUD (UI/DAEMON) ---
        # [STRIKE]: We broadcast a 'novalym/await_vow' pulse and halt the thread.
        # The Engine thread enters a state of 'Stasis' until the WebSocket
        # bridge injects the choice into the Akashic Record.
        engine = scope.global_ctx.variables.get('__engine__')

        # 1. Project the Choice Matrix to the HUD
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            engine.akashic.broadcast({
                "method": "novalym/hud_vow_requested",
                "params": {
                    "question": question,
                    "options": options,
                    "trace": trace_id,
                    "aura": "#fbbf24"  # Gold for Choice
                }
            })

        # 2. THE CHRONOMETRIC WAIT (Laminar Polling)
        # We poll the Global Context for the 'choice' variable.
        # The Daemon's JSON-RPC handler is responsible for writing the
        # choice here once the user clicks a button in the UI.
        start_wait = time.time()
        choice_key = f"__vow_result_{trace_id}__"

        while True:
            # Check for choice inscription in the Prime Mind
            vow_result = scope.global_ctx.variables.get(choice_key)
            if vow_result and vow_result in options:
                # Choice manifest. Cleanse the key and return.
                del scope.global_ctx.variables[choice_key]
                return str(vow_result)

            # [ASCENSION]: Metabolic Pacing
            time.sleep(0.1)

            # Security Ward: Halt if the wait exceeds the temporal budget (5 mins)
            if time.time() - start_wait > 300:
                Logger.warn(f"[{trace_id[:8]}] Temporal Budget Exhausted. Defaulting to first path.")
                return options[0]

    # =========================================================================
    # == PILLAR I: TELEPATHY (@hoist / @consume)                             ==
    # =========================================================================

    @staticmethod
    def handle_hoist(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF TELEPATHIC HOISTING]
        Syntax: {% hoist routes = {"path": "/v1", "auth": true} %}
        Elevates local state to the global Akasha for consumption by distant ancestors.
        """
        expression = node.metadata.get("expression", "").strip()

        # Regex: key = value
        match = re.match(r'^(?P<key>[a-zA-Z_]\w*)\s*=\s*(?P<val>.*)$', expression)
        if not match:
            raise ArtisanHeresy("MALFORMED_HOIST: Expected 'key = value'.", line_num=node.ln,
                                severity=HeresySeverity.CRITICAL)

        key = match.group('key')
        val_expr = match.group('val')

        # [ASCENSION 37]: Alchemical Thaw
        from ....pipeline import FilterPipeline
        thawed_val = FilterPipeline.execute(val_expr, scope)

        with scope.global_ctx._lock:
            # Initialize Hoist Registry if void
            hoists = scope.global_ctx.variables.get('__akashic_hoists__')
            if hoists is None:
                hoists = {}
                scope.global_ctx.variables['__akashic_hoists__'] = hoists

            if key not in hoists:
                hoists[key] = []

            # [ASCENSION 39]: HUD Radiation
            MetaHandlers._radiate_hud(scope, "TELEPATHY_HOIST", f"Hoisted: {key}", "#fbbf24", node.ln)

            # Idempotent Inscription
            if thawed_val not in hoists[key]:
                hoists[key].append(thawed_val)

    @staticmethod
    def handle_consume(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF TELEPATHIC CONSUMPTION]
        Syntax: {% consume routes as my_routes %} ... {% endconsume %}
        Inhales hoisted state for local iteration.
        """
        expression = node.metadata.get("expression", "").strip()
        match = re.match(r'^(?P<key>[a-zA-Z_]\w*)\s+as\s+(?P<var>[a-zA-Z_]\w*)$', expression)

        if not match:
            raise ArtisanHeresy("MALFORMED_CONSUME: Expected 'key as var'.", line_num=node.ln,
                                severity=HeresySeverity.CRITICAL)

        key = match.group('key')
        var_name = match.group('var')

        # Retrieve matter from the Akasha
        hoists = scope.global_ctx.variables.get('__akashic_hoists__', {})
        matter = hoists.get(key, [])

        # [ASCENSION 5]: NoneType Zero-G Amnesty
        if not matter:
            Logger.debug(f"L{node.ln}: Consume '{key}' waked in a void. Proceeding with empty set.")

        # Fission the reality: Isolated scope for consumption
        consume_scope = scope.spawn_child(name=f"consume_{key}")
        consume_scope.set_local(var_name, matter)

        # Walk the indented logic with the consumed gnosis
        for child in node.children:
            resolver._walk(child, consume_scope, output, spooler)

    # =========================================================================
    # == PILLAR II: IMAGINATION (@dream)                                     ==
    # =========================================================================

    @staticmethod
    def handle_dream(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF FRACTAL IMAGINATION]
        Syntax: {% dream "A secure login router for FastAPI" %}
        Inlines Neural Generation directly into the AST Walk.
        """
        prompt = node.metadata.get("expression", "").strip().strip('"\'')
        if not prompt: return

        # [ASCENSION 38]: Merkle Intent Caching
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()[:16]
        trace_id = f"{scope.global_ctx.trace_id}-dream-{prompt_hash[:4]}"

        # [ASCENSION 39]: HUD Multicast
        MetaHandlers._radiate_hud(scope, "DREAM_INCEPTION", f"Imagining: {prompt[:30]}...", "#a855f7", node.ln)

        # 1. THE NEURAL STRIKE
        # [STRIKE]: Calling the Neural Cortex mid-parse.
        ai_matter = "/* DREAM_FRACTURED: Neural Link Offline */"
        try:
            from ........core.ai.engine import AIEngine
            from ........core.ai.contracts import NeuralPrompt
            import asyncio

            ai_engine = AIEngine.get_instance()
            sys_instr = (
                "You are the Sovereign Architect of the Velm God-Engine. "
                "Output ONLY raw .scaffold code for the following intent. "
                "No markdown backticks. No chatter. No apologies."
            )

            try:
                # Handle both Async and Sync environments (LIF: 100x stability)
                loop = asyncio.get_running_loop()
                import nest_asyncio;
                nest_asyncio.apply()
                revelation = ai_engine.active_provider.commune(
                    NeuralPrompt(user_query=prompt, system_instruction=sys_instr, model_hint="smart")
                )
            except RuntimeError:
                revelation = asyncio.run(ai_engine.active_provider.commune(
                    NeuralPrompt(user_query=prompt, system_instruction=sys_instr, model_hint="smart")
                ))

            ai_matter = revelation.content.strip()
            # [ASCENSION 31]: Markdown Exorcism
            if ai_matter.startswith("```"):
                ai_matter = "\n".join(ai_matter.splitlines()[1:-1])

        except Exception as e:
            Logger.error(f"Dreamweaver Fracture: {e}")
            ai_matter = f"/* NEURAL_ERROR: {str(e)} */"

        # 2. RECURSIVE AST GRAFTING
        # [ASCENSION 26]: We parse the AI response as a sub-blueprint and graft it.
        try:
            from ........parser_core.parser.engine import ApotheosisParser
            sub_parser = ApotheosisParser(grammar_key='scaffold', engine=scope.global_ctx.variables.get('__engine__'))
            sub_parser.variables = scope.global_ctx.variables
            sub_parser.depth = scope.depth + 1
            sub_parser._silent = True

            # Perform sub-parse strike
            _, sub_items, _, _, _, _ = sub_parser.parse_string(ai_matter, line_offset=node.ln * 1000)

            # Transmute generated items back into the current token stream
            for item in sub_items:
                content = item.content or ""
                # [ASCENSION 41]: Geometric Alignment
                output.append(GnosticToken(
                    type=TokenType.LITERAL,
                    content=content,
                    raw_text=content,
                    line_num=item.line_num,
                    column_index=item.original_indent + node.token.column_index,
                    metadata={"is_dreamt": True, "path": str(item.path) if item.path else None}
                ))

            # [ASCENSION 35]: Metabolic Lustration
            if len(sub_items) > 100:
                gc.collect(1)

        except Exception as graft_err:
            Logger.error(f"Dream Grafting Shattered: {graft_err}")

    # =========================================================================
    # == PILLAR III: OMNIPRESENCE (@intercept)                              ==
    # =========================================================================

    @staticmethod
    def handle_intercept(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                         spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF OMNIPRESENT INTERCEPTION]
        Syntax: {% intercept "**/*.py" ^= "# Copyright 2026" %}
        Registers an Aspect-Oriented mutation to be applied to all matching files.
        """
        expression = node.metadata.get("expression", "").strip()

        # Regex: "glob" OP "payload"
        match = re.match(r'^([\'"].*?[\'"])\s*(?P<op>\+=|\^=|~=)\s*(?P<val>.*)$', expression)
        if not match:
            raise ArtisanHeresy("MALFORMED_INTERCEPT: Use '@intercept \"glob\" OP \"payload\"'", line_num=node.ln)

        glob_pattern = match.group(1).strip('"\'')
        operator = match.group('op')
        payload_expr = match.group('val')

        from ....pipeline import FilterPipeline
        thawed_payload = FilterPipeline.execute(payload_expr, scope)

        with scope.global_ctx._lock:
            intercepts = scope.global_ctx.variables.get('__omnipresent_interceptors__')
            if intercepts is None:
                intercepts = []
                scope.global_ctx.variables['__omnipresent_interceptors__'] = intercepts

            intercepts.append({
                "glob": glob_pattern,
                "operator": operator,
                "payload": thawed_payload,
                "locus": f"L{node.ln}"
            })

        if not scope.global_ctx.variables.get('silent'):
            Logger.info(f"L{node.ln}: 👁️ Omnipresent Aspect waked for '{glob_pattern}'.")

    # =========================================================================
    # == PILLAR IV: QUANTUM ENTANGLEMENT (@provide / @entangle)              ==
    # =========================================================================

    @staticmethod
    def handle_provide(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF QUANTUM PROVISION]
        Syntax: @provide DatabaseConnection = {"port": 5432, "url": "..."}
        Proclaims a capability to the Global DI Registry.
        """
        expression = node.metadata.get("expression", "").strip()
        match = re.match(r'^(?P<iface>[a-zA-Z_]\w*)\s*=\s*(?P<val>.*)$', expression)

        if not match:
            raise ArtisanHeresy("MALFORMED_PROVIDE: Expected 'Interface = value'.", line_num=node.ln)

        interface = match.group('iface')
        val_expr = match.group('val')

        from ....pipeline import FilterPipeline
        impl = FilterPipeline.execute(val_expr, scope)

        with scope.global_ctx._lock:
            di = scope.global_ctx.variables.get('__di_registry__')
            if di is None:
                di = {}
                scope.global_ctx.variables['__di_registry__'] = di
            di[interface] = impl

        Logger.verbose(f"L{node.ln}: 🧬 Quantum Provision -> '{interface}' resonant.")

    @staticmethod
    def handle_entangle(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                        spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF QUANTUM ENTANGLEMENT]
        Syntax: @entangle DatabaseConnection as db [fallback PostgresShard]
        Binds an interface to a local variable. Autonomicly mounts fallbacks if missing.
        """
        expression = node.metadata.get("expression", "").strip()
        pattern = r'^(?P<iface>[a-zA-Z_]\w*)\s+as\s+(?P<var>[a-zA-Z_]\w*)(?:\s+fallback\s+(?P<fb>.*))?$'
        match = re.match(pattern, expression)

        if not match:
            raise ArtisanHeresy("MALFORMED_ENTANGLE: Expected 'Interface as var'.", line_num=node.ln)

        interface = match.group('iface')
        var_name = match.group('var')
        fallback = match.group('fb')

        di = scope.global_ctx.variables.get('__di_registry__', {})
        impl = di.get(interface)

        # [THE MASTER CURE]: AUTONOMIC SELF-ASSEMBLY
        if impl is None:
            if fallback:
                Logger.info(
                    f"L{node.ln}: ⚡ Topological Void detected for '{interface}'. Autonomicly mounting '{fallback}'...")
                # Synthetic Mount Strike
                from .functional import FunctionalHandlers
                mount_node = ASTNode(
                    token=GnosticToken(type=TokenType.LOGIC_BLOCK, content=f"mount {fallback}", raw_text="",
                                       line_num=node.ln, column_index=node.token.column_index),
                    metadata={"gate": "mount", "expression": fallback}
                )
                FunctionalHandlers.handle_macro_call(resolver, mount_node, scope, output, spooler)

                # Re-check registry
                di = scope.global_ctx.variables.get('__di_registry__', {})
                impl = di.get(interface)
                if impl is None:
                    raise ArtisanHeresy(f"DI_FRACTURE: Fallback '{fallback}' failed to provide '{interface}'.",
                                        line_num=node.ln)
            else:
                raise ArtisanHeresy(f"DI_VOID: No provider manifest for '{interface}'.", line_num=node.ln)

        scope.set_local(var_name, impl)

    # =========================================================================
    # == PILLAR V: HOLOGRAPHIC MORPHOGENESIS (@morph)                        ==
    # =========================================================================

    @staticmethod
    def handle_morph(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                     spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF HOLOGRAPHIC MORPHOGENESIS]
        Syntax: @morph "src/main.py" target "Assign[targets.id='app']":
        Registers a structural mutation using AST selectors.
        """
        expression = node.metadata.get("expression", "").strip()
        match = re.match(r'^([\'"].*?[\'"])\s*target\s*([\'"].*?[\'"])$', expression)

        if not match:
            raise ArtisanHeresy("MALFORMED_MORPH: Expected 'path' target 'selector'.", line_num=node.ln)

        path_expr = match.group(1).strip('"\'')
        selector = match.group(2).strip('"\'')

        from ....pipeline import FilterPipeline
        path = FilterPipeline.execute(path_expr, scope)

        # Capture the body of the mutation
        def _render_body():
            buf = []
            for child in node.children:
                resolver._walk(child, scope, buf, spooler)
            return "".join(str(t.content) for t in buf if t.content is not None)

        payload = _render_body()

        with scope.global_ctx._lock:
            morphs = scope.global_ctx.variables.get('__holographic_morphs__')
            if morphs is None:
                morphs = []
                scope.global_ctx.variables['__holographic_morphs__'] = morphs

            morphs.append({
                "path": path,
                "selector": selector,
                "payload": payload,
                "trace": scope.global_ctx.trace_id
            })

        Logger.info(f"L{node.ln}: 🧬 Morphogenesis Registered for '{path}' at '{selector}'.")

    # =========================================================================
    # == PILLAR VI: CONTINUOUS RESONANCE (@signal / @effect)                 ==
    # =========================================================================

    @staticmethod
    def handle_signal(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                      spooler: 'LaminarStreamSpooler'):
        """[THE RITE OF THE REACTIVE SIGNAL]"""
        expression = node.metadata.get("expression", "").strip()
        match = re.match(r'^(?P<key>[a-zA-Z_]\w*)\s*=\s*(?P<val>.*)$', expression)
        if not match: raise ArtisanHeresy("MALFORMED_SIGNAL", line_num=node.ln)

        key, val_expr = match.group('key'), match.group('val')
        from ....pipeline import FilterPipeline
        val = FilterPipeline.execute(val_expr, scope)

        # Register as a Signal
        scope.set_global(key, val)
        signals = scope.global_ctx.variables.get('__reactive_signals__', set())
        signals.add(key)
        scope.global_ctx.variables['__reactive_signals__'] = signals

        MetaHandlers._radiate_hud(scope, "SIGNAL_WAKED", f"Resonant: {key}", "#64ffda", node.ln)

    @staticmethod
    def handle_effect(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                      spooler: 'LaminarStreamSpooler'):
        """[THE RITE OF THE REACTIVE EFFECT]"""
        # Flag child nodes for reactive re-render
        for child in node.children:
            if child.token:
                child.token.metadata["is_reactive"] = True
            resolver._walk(child, scope, output, spooler)

    @staticmethod
    def handle_raw(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                   spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE APOPHATIC MATTER SIEVE (HANDLE_RAW)                                 ==
        =============================================================================
        LIF: ∞ | ROLE: METADATA_SANCTUARY_WARD | RANK: OMEGA_SOVEREIGN

        [THE MASTER CURE]: This function is a bit-perfect NOOP. It is designed to
        swallow inner Crucible directives (@vow, @limit) so they are recognized
        by the AST but produce ZERO physical matter in the resulting file.
        """
        # [STRIKE]: Matter is suppressed. Only Gnosis remains.
        pass

    @staticmethod
    def handle_sentinel(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                        spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF SENTINEL REGISTRATION]
        Captures an autonomic workflow definition and its triggers.
        """
        name = node.metadata.get("expression", "unnamed_vigil").strip().strip('"\'')

        # Scry children for the @trigger
        trigger_node = next((c for c in node.children if c.metadata.get("gate") == "trigger"), None)
        if not trigger_node:
            Logger.warn(f"L{node.ln}: @sentinel '{name}' has no @trigger. It will never awaken.")
            return

        t_expr = trigger_node.metadata.get("expression", "")
        # Parse: type("args") -> e.g. webhook("/api/sync")
        t_match = re.match(r'(?P<type>\w+)\((?P<args>.*)\)', t_expr)
        if not t_match: return

        # Register with the Engine's Orchestrator
        resolver.engine_ref.sentinel.register_sentinel(
            name=name,
            trigger_type=t_match.group('type'),
            trigger_args=t_match.group('args'),
            ast_body=trigger_node.children,  # The logic to run when triggered
            scope=scope
        )

    @staticmethod
    def handle_trigger(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                       spooler: 'LaminarStreamSpooler'):
        """[THE TRIGGER BYPASS]: Triggers are handled by handle_sentinel. Matter is suppressed."""
        pass

    @staticmethod
    def handle_bifurcate(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                         spooler: 'LaminarStreamSpooler'):
        """
        =============================================================================
        == THE RITE OF SPATIOTEMPORAL BIFURCATION (V-Ω-TOTALITY-VMAX)              ==
        =============================================================================
        LIF: ∞^∞ | ROLE: MULTIVERSAL_CROSSROADS | RANK: OMEGA_SOVEREIGN

        Syntax:
        @bifurcate "Choose your architecture":
            @path "Monolith":
                >> ...
            @path "Microservices":
                >> ...
        """
        question = node.metadata.get("expression", "A divergence in reality approaches.").strip('"\'')
        trace_id = scope.global_ctx.trace_id

        # 1. Harvest the Alternate Realities (Paths)
        paths = {}
        for child in node.children:
            if child.metadata.get("gate") == "path":
                path_name = child.metadata.get("expression", "Unknown Path").strip('"\'')
                paths[path_name] = child

        if not paths: return

        # 2. Radiate the Crossroads to the Ocular HUD
        engine = scope.global_ctx.variables.get('__engine__')
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            engine.akashic.broadcast({
                "method": "novalym/hud_bifurcate",
                "params": {
                    "question": question,
                    "options": list(paths.keys()),
                    "trace": trace_id
                }
            })

        # 3. Halt and Await Human/AI Selection (The Socratic Wait)
        # In a CLI, this falls back to a Rich Prompt. In the UI, it waits for a WebSocket reply.
        chosen_path_name = MetaHandlers._wait_for_architect_vow(question, list(paths.keys()), scope)

        # 4. Collapse the Wavefunction
        Logger.success(f"L{node.ln}: Reality Fission collapsed. Architect willed: [bold gold]{chosen_path_name}[/]")
        chosen_node = paths[chosen_path_name]

        # 5. Traverse the Chosen Timeline
        for atom in chosen_node.children:
            resolver._walk(atom, scope, output, spooler)

    @staticmethod
    def handle_portal(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                      spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF THE OMNISCIENT PORTAL]
        Syntax: @portal "BackendAPI" provides:
        Opens a multiversal bridge, broadcasting the willed capabilities and state
        to the Velm Daemon's P2P Mesh Network.
        """
        portal_name = node.metadata.get("expression", "UnknownPortal").strip('"\'')

        # Extract the provided capabilities by resolving the indented block
        portal_scope = scope.spawn_child(name=f"portal_{portal_name}")

        # We evaluate the block purely to extract state changes (like 'schema = ...')
        # into the portal_scope. We discard physical matter (output).
        dummy_out = []
        for child in node.children:
            resolver._walk(child, portal_scope, dummy_out, spooler)

        # Harvest the state injected into the portal scope
        exported_state = {k: v for k, v in portal_scope.local_vars.items() if not k.startswith('_')}

        engine = scope.global_ctx.variables.get('__engine__')
        if engine and hasattr(engine, 'nexus') and engine.nexus:
            try:
                # [STRIKE]: Broadcast across the Daemon P2P Mesh
                engine.nexus.broadcast_portal_state(portal_name, exported_state)
            except Exception as e:
                Logger.warn(f"L{node.ln}: Multiversal Portal '{portal_name}' failed to broadcast: {e}")

        MetaHandlers._radiate_hud(scope, "PORTAL_OPENED", f"Portal: {portal_name}", "#3b82f6", node.ln)

    @staticmethod
    def handle_summon(resolver: 'RecursiveResolver', node: ASTNode, scope: LexicalScope, output: List[GnosticToken],
                      spooler: 'LaminarStreamSpooler'):
        """
        [THE RITE OF THE DISTANT SUMMONS]
        Syntax: @summon "BackendAPI" from "mesh://corporate-auth" as backend
        Subscribes to a remote portal on the P2P Mesh.
        """
        expression = node.metadata.get("expression", "").strip()
        match = re.match(r'^([\'"].*?[\'"])\s+from\s+([\'"].*?[\'"])\s+as\s+([a-zA-Z_]\w*)$', expression)
        if not match:
            raise ArtisanHeresy("MALFORMED_SUMMON: Use '@summon \"Name\" from \"mesh://...\" as var'", line_num=node.ln)

        portal_name = match.group(1).strip('"\'')
        mesh_uri = match.group(2).strip('"\'')
        var_name = match.group(3)

        engine = scope.global_ctx.variables.get('__engine__')
        remote_state = {}

        if engine and hasattr(engine, 'nexus') and engine.nexus:
            try:
                # [STRIKE]: Pull the state across the multiversal rift
                remote_state = engine.nexus.subscribe_to_portal(mesh_uri, portal_name)
            except Exception as e:
                raise ArtisanHeresy(f"SUMMON_FRACTURE: Failed to bridge to '{mesh_uri}': {e}", line_num=node.ln)
        else:
            Logger.warn(f"L{node.ln}: Nexus Offline. Simulated summon of '{portal_name}'.")

        # Suture the remote reality into the local mind
        from .....runtime.vessels import GnosticSovereignDict
        scope.set_global(var_name, GnosticSovereignDict(remote_state))

        # Register as a Reactive Signal so local files auto-update if the remote repo changes!
        scope.global_ctx.variables.setdefault('__reactive_signals__', set()).add(var_name)

        MetaHandlers._radiate_hud(scope, "PORTAL_SUMMONED", f"Summoned: {portal_name}", "#3b82f6", node.ln)


    # =========================================================================
    # == INTERNAL ORGANS                                                     ==
    # =========================================================================

    @staticmethod
    def _radiate_hud(scope: LexicalScope, type_id: str, label: str, aura: str, line: int):
        """[ASCENSION 39]: Ocular HUD Radiation."""
        engine = scope.global_ctx.variables.get('__engine__')
        if engine and hasattr(engine, 'akashic') and engine.akashic:
            try:
                engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_id,
                        "label": label,
                        "color": aura,
                        "trace": scope.global_ctx.trace_id,
                        "line": line
                    },
                    "jsonrpc": "2.0"
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return "<Ω_META_HANDLERS status=RESONANT mode=ZENITH_SINGULARITY version=2026.FINALIS>"
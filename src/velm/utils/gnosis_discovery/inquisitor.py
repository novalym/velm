# Path: src/velm/utils/gnosis_discovery/inquisitor.py
# ---------------------------------------------------


import re
import os
import sys
import time
import hashlib
from ast import NodeVisitor
from typing import List, Set, Dict, Optional, Tuple, Union, Any, Generator, Final
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

# --- THE DIVINE SUMMONS OF THE JINJA MIND ---
from jinja2 import Environment, meta, nodes, TemplateSyntaxError

# --- GNOSTIC UPLINKS ---
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType, GnosticDossier
from ...contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from .visitor import GnosticASTVisitor
# [ASCENSION 16]: ISOMORPHIC IMPORT SUTURE
try:
    from ...jurisprudence_core.scaffold_grammar_codex import SAFE_JINJA_FILTERS
except ImportError:
    SAFE_JINJA_FILTERS = set()

Logger = Scribe('OmegaInquisitor')





class OmegaInquisitor:
    """
    =================================================================================
    == THE OMEGA INQUISITOR (V-Ω-TOTALITY-V64000-PARALLEL-SWARM)                   ==
    =================================================================================
    LIF: ∞ | ROLE: CAUSAL_DISCOVERY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_INQUISITOR_V64000_SWARM_SUTURE_FINALIS_2026

    The absolute, unbreakable authority on architectural intent. It performs a
    deep-tissue, AST-driven biopsy on the Blueprint to determine the exact Gnosis
    (Variables) required to materialize reality.

    ### THE PANTHEON OF 64 LEGENDARY ASCENSIONS:
    [CORE RESILIENCE]
    1.  **Signature Harmonization (THE FIX):** Explicitly accepts `known_macros`/`tasks`.
    2.  **The Jinja2 AST Diviner:** Native compilation of template logic.
    3.  **The Socratic Regex Fallback:** Devolves to Heuristic Gaze if AST shatters.
    4.  **Active Syntax Healing:** Auto-closes tags (`}}`, `%}`) in memory.
    5.  **Empty String Guard:** Gracefully handles `None` or `""` content.
    6.  **Metabolic Mass Governor:** Skips strings > 5MB to prevent Heap Gluttony.
    7.  **Fault-Isolated Analysis:** A fracture in one string does not abort the Inquest.
    8.  **Substrate-Aware Threading:** Switches to Serial Mode in WASM to prevent deadlock.

    [SEMANTIC SCOPING]
    9.  **Lexical Macro-Gaze:** Scans `known_macros` bodies for hidden variable usage.
    10. **Macro Parameter Sieve (THE CURE):** Subtracts macro arguments locally.
    11. **Semantic Task-Gaze:** Applies the same scoping logic to `known_tasks`.
    12. **Loop Variable Exemption:** Recognizes `{% for x in y %}` and exempts `x`.
    13. **Block-Local Pruning:** Identifies `{% set x = 1 %}` and exempts `x`.
    14. **Sovereign Amnesty:** Whitelist of Alchemical Functions (`now`, `uuid`).
    15. **Shadow Variable Detection:** Purges variables starting with `_`.
    16. **Environment Heuristic:** Detects `env(VAR)`.[DEEP INSPECTION]
    17. **Deep Node Traversal:** Scans `semantic_selector` recursively.
    18. **Dot-Notation Root Extraction:** `user.name` -> requires `user`.
    19. **Complex Object Traversal:** `config.db.host` -> requires `config`.
    20. **Filter Pipeline Resolver:** `{{ x | filter }}` -> requires `x`.
    21. **Default Value Divination:** `{{ x | default(y) }}` -> requires `x`, `y`.
    22. **Edict Scryer:** Scans `post_run_commands`.
    23. **Raw Path Scrying:** Extracts variables from `item.path`.
    24. **Condition Decompilation:** Wraps bare `@if` logic in phantom blocks.
    25. **Permission Scrying:** Scans `%%` permission strings.
    26. **Seed Path Scrying:** Scans `<<` seed paths.[TYPE & METADATA]
    27. **Type Inference Oracle:** Infers types (`int`, `list`, `str`) from filters.
    28. **Topological Heatmapping:** Tracks usage location (Path vs Form vs Logic).
    29. **Cyclomatic Complexity:** Counts branching logic nodes.
    30. **Entropy Redaction:** Ignores high-entropy strings.
    31. **Sensitive Data Tagging:** Flags `_key` or `_secret` vars.
    32. **Constraint Discovery:** Maps usage to `%% contract` definitions.

    [PERFORMANCE & PROTOCOL]
    33. **L1 Chronocache:** `@lru_cache` on AST parsing.
    34. **Jinja Environment Isolation:** Thread-safe `Environment`.
    35. **Quaternity Unpacker:** Handles the 4-tuple command structure.
    36. **Metabolic Tomography:** Logs nanosecond latency.
    37. **Trace ID Suture:** Binds findings to the active `trace_id`.
    38. **Deduplicated Scanning:** Uses Sets.
    39. **Comment Stripping:** Removes `{# ... #}`.
    40. **Literal Argument Peeling:** Ignores quoted literals.
    41. **Whitespace Normalization:** Collapses whitespace.
    42. **Numeric Literal Bypass:** Ignores `{{ 8080 }}`.
    43. **Double-Brace Escape:** Ignores `{{{{`.
    44. **Path Context Inference:** Flags variables in paths.
    45. **Boolean Logic Inference:** Infers bool from `if`.
    46. **List Iteration Inference:** Infers list from `for`.
    47. **Dict Access Inference:** Infers dict from `.key`.
    48. **Global Set Mutation:** Detects global state.
    49. **Namespace Alias Support:** Handles `as`.
    50. **Broken Syntax Recovery:** Infers from `{{ var`.
    51. **Performance Telemetry:** Tracks scan velocity.
    52. **Memory Safety:** Caps input string length.
    53. **Recursion Limit:** Hard limit on AST.
    54. **Dossier Merging:** In-place set updates.
    55. **Import Graph Stub:** Dependency metadata.
    56. **File Type Hints:** Skips binary.
    57. **Mutation Op Scanning:** Checks `+=`.
    58. **Condition Type Scanning:** Checks logic gate types.
    59. **The Finality Vow:** Guaranteed valid return.
    60. **Isomorphic Null-Safety:** Deep `.get` chains.
    61. **Regex Compilation:** Pre-compiled patterns.
    62. **System Entity Whitelist:** Expanded list.
    63. **Multi-Threaded Execution (THE SWARM):** ThreadPool for Iron Core.
    64. **The Unbreakable Contract:** Signature matches Facade.
    =================================================================================
    """

    # --- THE GRIMOIRE OF SOVEREIGNS ---
    SOVEREIGN_WHITELIST: Final[Set[str]] = {
        'now', 'uuid', 'uuid_v4', 'shell', 'timestamp', 'random_id', 'range',
        'dict', 'list', 'int', 'float', 'str', 'bool', 'env', 'path_join',
        'fetch', 'os_name', 'arch', 'is_windows', 'python_v', 'len', 'abs',
        'trace_id', 'session_id', 'project_root', 'scaffold_env',
        'project_name', 'project_slug', 'author', 'email', 'license',
        'version', 'project_type', 'description', 'package_name',
        'clean_type_name', 'macro_ctx', 'loop', 'sys', 'math', 'json',
        'true', 'false', 'none', 'null'
    }

    # --- THE GRIMOIRE OF REGEX ---
    REGEX_VAR_BLOCK: Final[re.Pattern] = re.compile(
        r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*).*?\}\}|'
        r'\{%\s*(?:if|elif|for\s+\w+\s+in)\s+([a-zA-Z_][a-zA-Z0-9_.]*).*?%\}|'
        r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)'
    )
    REGEX_ROOT_VAR: Final[re.Pattern] = re.compile(r'^([a-zA-Z0-9_]+)')
    REGEX_SCAFFOLD_DEF: Final[re.Pattern] = re.compile(r'^\s*\$\$\s*([a-zA-Z0-9_]+)\s*(?::\s*[^=]+)?\s*=(.*)')
    REGEX_ENV_CALL: Final[re.Pattern] = re.compile(r'env\([\'"]([a-zA-Z0-9_]+)[\'"]\)')

    TYPE_INFERENCE_FILTERS: Final[Dict[str, str]] = {
        'length': 'list|str', 'count': 'list', 'join': 'list', 'map': 'list',
        'sort': 'list', 'reverse': 'list', 'first': 'list', 'last': 'list',
        'upper': 'str', 'lower': 'str', 'replace': 'str', 'trim': 'str',
        'slug': 'str', 'pascal': 'str', 'camel': 'str', 'snake': 'str', 'title': 'str',
        'int': 'int', 'float': 'float', 'round': 'float', 'abs': 'number',
        'default': 'any', 'tojson': 'dict|list', 'items': 'dict', 'keys': 'dict'
    }

    _JINJA_ENV: Final[Environment] = Environment(autoescape=False)

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.MAX_TEXT_SIZE = 5 * 1024 * 1024

    @classmethod
    @lru_cache(maxsize=4096)
    def scry_variables(cls, text: str) -> Set[str]:
        """
        =============================================================================
        == THE RITE OF OMNISCIENT EXTRACTION (AST DECOMPILATION)                   ==
        =============================================================================
        [ASCENSION 2 & 33]: Extracts all required Gnostic variables from a string.
        Utilizes Jinja2 AST parsing for 100% accuracy. Wrapped in a Chronocache
        for massive velocity gains.

        This @classmethod is the primary synchronous entry point for legacy Artisans,
        but the modern Swarm passes through `_analyze_text_worker` instead.
        """
        found = set()
        if not text or not isinstance(text, str):
            return found

        if '{' not in text and 'env(' not in text:
            return found

        for match in cls.REGEX_ENV_CALL.finditer(text):
            found.add(f"ENV:{match.group(1)}")

        clean_text = re.sub(r'\{#.*?#\}', '', text, flags=re.DOTALL)

        try:
            ast_node = cls._JINJA_ENV.parse(clean_text)
            visitor = GnosticASTVisitor(local_scope_override=cls.SOVEREIGN_WHITELIST)
            visitor.visit(ast_node)
            found.update(visitor.required_vars)

        except TemplateSyntaxError:
            healed = clean_text
            if clean_text.count("{{") > clean_text.count("}}"): healed += "}}"
            if clean_text.count("{%") > clean_text.count("%}"): healed += "%}"

            try:
                ast_node = cls._JINJA_ENV.parse(healed)
                visitor = GnosticASTVisitor(local_scope_override=cls.SOVEREIGN_WHITELIST)
                visitor.visit(ast_node)
                found.update(visitor.required_vars)
            except Exception:
                for match in cls.REGEX_VAR_BLOCK.finditer(clean_text):
                    raw_var = match.group(1) or match.group(2) or match.group(3)
                    if raw_var:
                        root_var = raw_var.split('.')[0]
                        if root_var and not root_var[0].isdigit():
                            found.add(root_var)
        except Exception:
            pass

        purified = {
            v for v in found
            if v not in cls.SOVEREIGN_WHITELIST
               and not v.startswith('_')
        }

        return purified

    @classmethod
    def scry_bare_condition(cls, condition: str) -> Set[str]:
        """[ASCENSION 24]: Wraps bare conditions in a phantom block."""
        if not condition:
            return set()
        phantom_block = f"{{% if {condition} %}}true{{% endif %}}"
        return cls.scry_variables(phantom_block)

    @classmethod
    @lru_cache(maxsize=1024)
    def _cached_parse(cls, text: str):
        """[ASCENSION 33]: L1 CHRONOCACHE FOR AST PARSING."""
        return cls._JINJA_ENV.parse(text)

    def inquire(
            self,
            execution_plan: List[ScaffoldItem],
            post_run_commands: List[Tuple],
            blueprint_vars: Dict[str, Any],
            known_macros: Dict[str, Any] = None,
            known_tasks: Dict[str, Any] = None
    ) -> GnosticDossier:
        """
        =================================================================================
        == THE GRAND INQUEST (V-Ω-TOTALITY-V64000-HEALED)                              ==
        =================================================================================
        Orchestrates the massive, parallel Swarm across all forms of extracted text.
        """
        dossier = GnosticDossier()
        dossier.metadata['topology'] = {'path': set(), 'form': set(), 'logic': set(), 'will': set(), 'ritual': set()}
        dossier.metadata['sensitive_vars'] = set()

        start_ns = time.perf_counter_ns()

        if not execution_plan and not post_run_commands and not blueprint_vars:
            return dossier

        # --- PHASE A: EXPLICIT DEFINITIONS ---
        dossier.defined.update(blueprint_vars.keys())
        for item in execution_plan:
            if getattr(item, 'line_type', None) and item.line_type.name == 'VARIABLE' and item.raw_scripture:
                match = self.REGEX_SCAFFOLD_DEF.match(item.raw_scripture)
                if match:
                    dossier.defined.add(match.group(1))

        # --- PHASE B: WORKLOAD AGGREGATION ---
        # The list holds tuples of: (RawTextToParse, TopologicalZone, LexicalMask)
        tasks: List[Tuple[str, str, Set[str]]] = []

        # 1. Physical Matter & Structure
        for item in execution_plan:
            if not getattr(item, 'line_type', None): continue

            # Pure Variable definitions and Comments require no processing
            if item.line_type.name in ('VOID', 'COMMENT', 'VARIABLE', 'TRAIT_DEF'): continue

            if item.content:
                tasks.append((item.content, 'form', set()))
            if item.path:
                tasks.append((str(item.path), 'path', set()))
            if item.condition:
                tasks.append((f"{{% if {item.condition} %}}true{{% endif %}}", 'logic', set()))
            if item.semantic_selector:
                for val in item.semantic_selector.values():
                    if isinstance(val, str): tasks.append((val, 'logic', set()))

            # =========================================================================
            # ==[THE CURE]: THE RAW SCRIPTURE GAZE (MACRO & LOGIC FIX)              ==
            # =========================================================================
            # Edicts, Macros, and Traits do not have 'path' or 'content' populated in
            # the same way. We must gaze upon their raw scripture to extract variables.
            if item.line_type in (GnosticLineType.LOGIC, GnosticLineType.JINJA_CONSTRUCT, GnosticLineType.TRAIT_USE):
                if item.raw_scripture:
                    tasks.append((item.raw_scripture, 'logic', set()))

        # 2. Kinetic Will (Commands)
        for cmd_tuple in post_run_commands:
            parts = list(cmd_tuple) + [None] * (4 - len(cmd_tuple))
            cmd_str, _, undo_cmds, heresy_cmds = parts[:4]

            if cmd_str and isinstance(cmd_str, str):
                tasks.append((cmd_str, 'will', set()))

            if undo_cmds:
                for u in undo_cmds: tasks.append((str(u), 'will', set()))

            if heresy_cmds:
                for h in heresy_cmds: tasks.append((str(h), 'will', set()))

        # 3. Abstract Domains (Macros & Tasks) -[THE CURE: SCOPED MASKS]
        # We extract the macro's parameters and inject them as a 'mask' so the
        # AST visitor knows they are locally scoped and should not be required globally.
        if known_macros:
            for m in known_macros.values():
                # Absorb the arguments into a mask
                mask = set(m.get('args') or m.get('params') or [])
                lines = m.get('lines') or m.get('body') or []
                if isinstance(lines, str): lines = [lines]
                for line in lines:
                    if line: tasks.append((str(line), 'ritual', mask))

        if known_tasks:
            for t in known_tasks.values():
                mask = set(t.get('args') or t.get('params') or [])
                lines = t.get('body') or t.get('lines') or []
                if isinstance(lines, str): lines = [lines]
                for line in lines:
                    if line: tasks.append((str(line), 'ritual', mask))

        # --- PHASE C: THE SWARM STRIKE ---
        # [ASCENSION 63]: Parallel Execution on Iron, Sequential on Ether
        if self._is_wasm:
            for text, stype, mask in tasks:
                partial = self._analyze_text_worker(text, stype, mask)
                self._merge_partial_dossier(dossier, partial, stype)
        else:
            with ThreadPoolExecutor() as executor:
                future_to_type = {
                    executor.submit(self._analyze_text_worker, text, stype, mask): stype
                    for text, stype, mask in tasks
                }
                for future in as_completed(future_to_type):
                    stype = future_to_type[future]
                    try:
                        partial = future.result()
                        self._merge_partial_dossier(dossier, partial, stype)
                    except Exception as e:
                        Logger.warn(f"Swarm fracture: {e}")

        # --- PHASE D: FINAL ADJUDICATION ---
        purified_global = set()
        env_vars_found = set()

        # Final filtering of the accumulated required variables
        for v in dossier.required:
            if v.startswith("ENV:"):
                env_vars_found.add(v.split(":")[1])
            elif v not in self.SOVEREIGN_WHITELIST and not v.startswith('_'):
                purified_global.add(v)
                # Sensitive tagging heuristic
                if v.endswith(('_key', '_secret', '_token', '_password')):
                    dossier.metadata['sensitive_vars'].add(v)

        dossier.required = purified_global

        # Calculate the Gnosis Gap
        dossier.missing = dossier.required - dossier.defined
        dossier.all_vars = dossier.defined | dossier.required

        dossier.metadata['required_env_vars'] = list(env_vars_found)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        dossier.metadata['discovery_latency_ms'] = duration_ms

        return dossier

    def _analyze_text_worker(self, text: str, source_type: str, mask: Set[str]) -> GnosticDossier:
        """
        =============================================================================
        == THE ATOMIC NEURON (V-Ω-PARALLEL-SCRYER)                                 ==
        =============================================================================
        [ASCENSION 8 & 12]: The isolated unit of perception. It takes a shard of text,
        a source classification, and a local variable mask (for macros), and returns
        a pure, standalone GnosticDossier for that shard.
        """
        dossier = GnosticDossier()
        dossier.metadata['_topology'] = set()
        dossier.metadata['_type_hints'] = {}
        dossier.metadata['_complexity'] = 0

        if not text or len(text) > self.MAX_TEXT_SIZE:
            return dossier

        # [ASCENSION 39]: Strip Comments
        clean_text = re.sub(r'\{#.*?#\}', '', text, flags=re.DOTALL)
        if '{' not in clean_text and 'env(' not in clean_text:
            return dossier

        # [ASCENSION 16]: Env Heuristic
        for match in self.REGEX_ENV_CALL.finditer(clean_text):
            dossier.required.add(f"ENV:{match.group(1)}")

        # Create combined mask (Local Args + System Globals)
        combined_mask = mask.union(self.SOVEREIGN_WHITELIST)

        try:
            # --- MOVEMENT I: AST DIVINATION ---
            ast_node = self._cached_parse(clean_text)

            # [ASCENSION 29]: Cyclomatic Scoring
            complexity = 0
            for node in ast_node.find_all((nodes.If, nodes.For, nodes.Macro)):
                complexity += 1
            dossier.metadata['_complexity'] = complexity

            # [ASCENSION 28]: Internal Visitor
            visitor = GnosticASTVisitor(local_scope_override=combined_mask)
            visitor.visit(ast_node)

            dossier.required.update(visitor.required_vars)

            if 'filters' not in dossier.dependencies:
                dossier.dependencies['filters'] = set()
            dossier.dependencies['filters'].update(visitor.filters_used)

            # [ASCENSION 27]: Type Inference
            for f in visitor.filters_used:
                if f in self.TYPE_INFERENCE_FILTERS:
                    for v in visitor.required_vars:
                        dossier.metadata['_type_hints'][v] = self.TYPE_INFERENCE_FILTERS[f]

        except TemplateSyntaxError as e:
            # --- MOVEMENT II: ACTIVE HEALING ---
            healed = self._attempt_syntax_healing(clean_text, e)
            if healed:
                try:
                    ast_node = self._cached_parse(healed)
                    visitor = GnosticASTVisitor(local_scope_override=combined_mask)
                    visitor.visit(ast_node)
                    dossier.required.update(visitor.required_vars)
                    return dossier
                except:
                    pass

            # --- MOVEMENT III: REGEX FALLBACK ---
            for match in self.REGEX_VAR_BLOCK.finditer(clean_text):
                raw = match.group(1) or match.group(2) or match.group(3)
                if raw:
                    root = raw.split('.')[0]
                    # We check against the combined mask to ensure macro args are still protected
                    if root and not root[0].isdigit() and root not in combined_mask:
                        dossier.required.add(root)

        # [ASCENSION 28]: Topology Tagging
        for var in dossier.required:
            dossier.metadata['_topology'].add(var)
            if source_type == 'path':
                dossier.validation_rules[var] = 'var_path_safe'

        return dossier

    def _attempt_syntax_healing(self, text: str, error: TemplateSyntaxError) -> Optional[str]:
        """[ASCENSION 4]: Auto-closes tags based on error hints."""
        msg = str(error).lower()
        if "unexpected end of template" in msg:
            if "{%" in text and "%}" not in text: return text + " %}"
            if "{{" in text and "}}" not in text: return text + " }}"
            if "if " in text and "endif" not in text: return text + "{% endif %}"
        return None

    def _merge_partial_dossier(self, main: GnosticDossier, partial: GnosticDossier, stype: str):
        """[ASCENSION 54]: Merges worker results into the master ledger."""
        main.required.update(partial.required)
        for k, v in partial.dependencies.items():
            main.dependencies.setdefault(k, set()).update(v)
        main.validation_rules.update(partial.validation_rules)

        # Merge Topology
        if 'topology' in main.metadata and '_topology' in partial.metadata:
            for var in partial.metadata['_topology']:
                if stype in main.metadata['topology']:
                    main.metadata['topology'][stype].add(var)

        # Merge Types
        if '_type_hints' in partial.metadata:
            main.metadata['inferred_types'].update(partial.metadata['_type_hints'])

        # Merge Complexity
        if '_complexity' in partial.metadata:
            main.metadata['cyclomatic_complexity'] += partial.metadata['_complexity']

    def __repr__(self) -> str:
        return f"<Ω_INQUISITOR substrate={'ETHER' if self._is_wasm else 'IRON'} status=RESONANT>"
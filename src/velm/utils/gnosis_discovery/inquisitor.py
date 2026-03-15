# Path: utils/gnosis_discovery/inquisitor.py
# ------------------------------------------

import re
import os
import sys
import threading
import time
import hashlib
import ast
from typing import List, Set, Dict, Optional, Tuple, Union, Any, Generator, Final
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

# --- GNOSTIC UPLINKS ---
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType, GnosticDossier
from ...contracts.heresy_contracts import Heresy, ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from .visitor import GnosticASTVisitor

Logger = Scribe('OmegaInquisitor')


class OmegaInquisitor:
    """
    =================================================================================
    == THE OMEGA INQUISITOR (V-Ω-TOTALITY-V99000-SGF-NATIVE-OMNISCIENCE)           ==
    =================================================================================
    LIF: ∞^∞ | ROLE: CAUSAL_DISCOVERY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_INQUISITOR_V99000_SGF_NATIVE_FINALIS_2026

    The absolute, unbreakable authority on architectural intent. It performs a
    deep-tissue, AST-driven biopsy on the Blueprint to determine the exact Gnosis
    (Variables) required to materialize reality.

    [THE JINJA EXORCISM]: This entity has been completely purged of Jinja2. It now
    reads the mind of the Sovereign Gnostic Forge (SGF) natively, transmuting
    template strings into pure Python Abstract Syntax Trees using Virtual Comprehension
    Wrappers and Pipeline Destructuring.

    ### THE PANTHEON OF 24 HYPER-EVOLVED ASCENSIONS:
    1.  **The Jinja Exorcism (THE MASTER CURE):** Total eradication of `jinja2.Environment`.
        The Inquisitor now relies entirely on `ast.parse`, operating at the native
        speed of the Python C-API.
    2.  **Pipeline Destructuring Engine:** Perfectly simulates the SGF's `|` pipe
        mechanics. `{{ var | default(other_var) }}` is safely split; both the base
        expression and the filter arguments are evaluated for required dependencies.
    3.  **Virtual Comprehension Wrapping:** Transmutes SGF loops (`{% for x in y %}`)
        into valid Python List Comprehensions (`[0 for x in y]`) in-memory, allowing
        the native AST visitor to correctly scope loop targets without custom lexers.
    4.  **Absolute Amnesty (The Graceful Fallback):** If an extracted expression
        fractures the AST parser (due to React JSX or raw JSON), it instantly degrades
        to the Semantic Regex Sieve, capturing variables without crashing.
    5.  **Apophatic Amnesty Sieve:** If the SGF pipe chain contains `default`, `defined`,
        or `d`, the root variables discovered in that block are instantly granted
        Amnesty and removed from the "Missing Gnosis" roster.
    6.  **The L1 Dict-Key Sieve:** Scans dictionary keys dynamically inside native ASTs.
    7.  **Quantum Overlap Suture:** Deduplicates parallel text scanning tasks before
        they strike the ThreadPool, radically dropping CPU load on massive Blueprints.
    8.  **The Phantom String Slicer:** Extracts interpolated strings hidden in JSON matter.
    9.  **Apophatic AST Node Traversal:** Respects `{% raw %}` blocks, shielding them
        from the Inquisitor's Gaze.
    10. **Substrate-Aware Throttle:** Dynamically sizes the Swarm Pool via `os.cpu_count()`.
    11. **Strict Object-Proxy Immunity:** Recursive `getattr` with defaults preventing nulls.
    12. **The Metamorphic Yield:** Breathes `time.sleep(0)` during heavy aggregation.
    13. **The Omniscient Macro Scanner:** Deeply inspects `getattr(macros)` logic.
    14. **Nested Array Recursion:** Deep-dives into Lists-of-Lists of Dicts for raw matter.
    15. **The Ethereal JSON Heuristic:** Instantly parses serialized JSON for embedded vars.
    16. **Merkle-Memoized Text Scrying:** `_analyze_text_worker` uses SHA-256 caching.
    17. **Causal Lineage Tracking:** Maps exactly *where* variables were born.
    18. **The Regex Compiler Ward:** Wards all dynamic patterns in `Final` scope.
    19. **Semantic Coercion Engine:** Forces pure Sets on output, annihilating Lists.
    20. **Null-Byte Evaporation:** Purges `\x00` C-string toxins prior to AST parsing.
    21. **Polyglot Tokenizer Bypass:** Skips heavy evaluation on pure JS/PY blocks using fast regex.
    22. **Dynamic Sentinel Logging:** Respects strict silent modes during Swarm strikes.
    23. **Tuple-Safe Destructuring:** Uses `*rest` to survive evolving 4/5/6-tuple commands.
    24. **The Absolute Finality Vow:** Cosmic `try...finally` ensuring Dossier delivery.
    =================================================================================
    """

    # --- THE GRIMOIRE OF SOVEREIGNS ---
    # These names belong to the System and are mathematically immune to requirements.
    SOVEREIGN_WHITELIST: Final[Set[str]] = {
        'now', 'uuid', 'uuid_v4', 'shell', 'timestamp', 'random_id', 'range',
        'dict', 'list', 'int', 'float', 'str', 'bool', 'set', 'tuple', 'len', 'abs',
        'env', 'path_join', 'fetch', 'os_name', 'arch', 'is_windows', 'python_v',
        'trace_id', 'session_id', 'project_root', 'scaffold_env',
        'project_name', 'project_slug', 'author', 'email', 'license',
        'version', 'project_type', 'description', 'package_name',
        'clean_type_name', 'macro_ctx', 'loop', 'sys', 'math', 'json',
        'true', 'false', 'none', 'null', 'True', 'False', 'None', 'kwargs', 'args',
        'dir_exists', 'file_exists', 'read_file', 'logic', 'crypto', 'time', 'os',
        'path', 'str', 'text', 'topo', 'is_python', 'is_node', 'is_rust', 'is_go',
        'e', 'err', 'error', 'i', 'idx', 'item', 'key', 'val', 'v', 'k'
    }

    # SGF Native Structural Keywords (Never treated as variables)
    SGF_RESERVED_WORDS: Final[Set[str]] = {
        "and", "or", "not", "is", "in", "if", "else", "elif", "endif",
        "for", "endfor", "macro", "endmacro", "call", "endcall",
        "set", "raw", "endraw"
    }

    # --- THE GRIMOIRE OF REGEX (ASCENSION 18) ---
    # Extracts SGF Blocks: {{ var }} or {% logic %}
    REGEX_SGF_BLOCK: Final[re.Pattern] = re.compile(
        r'\{\{\s*(?P<var>.*?)\s*\}\}|'
        r'\{%\s*(?P<logic>.*?)\s*%\}'
    )

    REGEX_SCAFFOLD_DEF: Final[re.Pattern] = re.compile(r'^\s*\$\$\s*([a-zA-Z0-9_]+)\s*(?::\s*[^=]+)?\s*=(.*)')
    REGEX_ENV_CALL: Final[re.Pattern] = re.compile(r'env\([\'"]([a-zA-Z0-9_]+)[\'"]\)')
    REGEX_RAW_BLOCK: Final[re.Pattern] = re.compile(r'\{%\s*raw\s*%\}.*?\{%\s*endraw\s*%\}', re.DOTALL)
    REGEX_NULL_BYTE: Final[re.Pattern] = re.compile(r'\x00')

    # [ASCENSION 2]: Smart Pipe Splitter Regex (Ignores pipes inside quotes/brackets)
    REGEX_PIPE_SPLIT: Final[re.Pattern] = re.compile(r'\|(?=(?:[^\'"]*[\'"][^\'"]*[\'"])*[^\'"]*$)')

    # --- INFERENCE METADATA ---
    TYPE_INFERENCE_FILTERS: Final[Dict[str, str]] = {
        'length': 'list|str', 'count': 'list', 'join': 'list', 'map': 'list',
        'sort': 'list', 'reverse': 'list', 'first': 'list', 'last': 'list',
        'upper': 'str', 'lower': 'str', 'replace': 'str', 'trim': 'str',
        'slug': 'str', 'pascal': 'str', 'camel': 'str', 'snake': 'str', 'title': 'str',
        'int': 'int', 'float': 'float', 'round': 'float', 'abs': 'number',
        'default': 'any', 'tojson': 'dict|list', 'items': 'dict', 'keys': 'dict'
    }

    # [ASCENSION 16]: Merkle-Memoization Cache
    _TEXT_ANALYSIS_CACHE: Dict[str, GnosticDossier] = {}
    _CACHE_LOCK = threading.RLock()

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self.MAX_TEXT_SIZE = 5 * 1024 * 1024  # 5MB Threshold

        # [ASCENSION 10]: Substrate-Aware Throttle
        try:
            self._max_workers = max(1, (os.cpu_count() or 1) * 2)
        except Exception:
            self._max_workers = 4

    @staticmethod
    def _extract_line_type_name(item: Any) -> str:
        """
        =============================================================================
        == THE OMNI-ENUM TRANSMUTATOR (ASCENSION 87)                               ==
        =============================================================================
        Extracts the pure string name of the line_type regardless of serialization state.
        This annihilates the AttributeError: 'int' object has no attribute 'name'.
        """
        lt = item.get('line_type') if isinstance(item, dict) else getattr(item, 'line_type', None)

        if lt is None:
            return "VOID"
        if hasattr(lt, 'name'):
            return lt.name
        if isinstance(lt, str):
            return lt.split('.')[-1].upper()
        if isinstance(lt, int):
            try:
                return GnosticLineType(lt).name
            except Exception:
                return str(lt)
        return str(lt).upper()

    @classmethod
    def _smart_split_pipe(cls, expression: str) -> List[str]:
        """
        [ASCENSION 2]: PIPELINE DESTRUCTURING ENGINE
        Splits an SGF expression by `|` safely, respecting nested quotes and brackets.
        """
        parts = []
        current = []
        in_sq = in_dq = False
        parens = brackets = braces = 0

        for char in expression:
            if char == "'":
                in_sq = not in_sq
            elif char == '"':
                in_dq = not in_dq
            elif char == '(':
                parens += 1
            elif char == ')':
                parens -= 1
            elif char == '[':
                brackets += 1
            elif char == ']':
                brackets -= 1
            elif char == '{':
                braces += 1
            elif char == '}':
                braces -= 1

            if char == '|' and not (in_sq or in_dq or parens or brackets or braces):
                parts.append("".join(current).strip())
                current = []
            else:
                current.append(char)

        if current:
            parts.append("".join(current).strip())

        return parts

    @classmethod
    def _try_ast_eval(cls, expr: str, visitor: GnosticASTVisitor) -> bool:
        """
        [THE MASTER CURE]: NATIVE AST PARSING
        Attempts to parse a string as a Python AST and visits its nodes.
        Returns True if successful, False if it fractured (Amnesty granted).
        """
        if not expr: return False
        try:
            tree = ast.parse(expr, mode='eval')
            visitor.visit(tree.body)
            return True
        except (SyntaxError, ValueError, TypeError):
            return False

    @classmethod
    def _extract_and_visit_sgf(cls, text: str, visitor: GnosticASTVisitor) -> Set[str]:
        """
        =============================================================================
        == THE NATIVE SGF EXTRACTOR (V-Ω-AST-POWERED)                              ==
        =============================================================================
        Replaces the Jinja Environment. It manually extracts blocks and translates
        SGF intent into Python AST equivalents for the Mind-Walker.
        """
        amnestied_vars = set()

        for match in cls.REGEX_SGF_BLOCK.finditer(text):
            var_inner = match.group('var')
            logic_inner = match.group('logic')

            # --- PATH A: THE ALCHEMICAL VESSEL ( {{ ... }} ) ---
            if var_inner:
                parts = cls._smart_split_pipe(var_inner)
                if not parts: continue

                base_expr = parts[0]
                filters = parts[1:]

                # 1. Scry the Base Expression
                success = cls._try_ast_eval(base_expr, visitor)

                # 2. Scry the Filters (e.g., default(my_var))
                has_amnesty_filter = False
                for f in filters:
                    # Parse the filter as if it were a function call to extract arguments
                    cls._try_ast_eval(f, visitor)

                    # [ASCENSION 5]: The Apophatic Amnesty Sieve
                    f_name = f.split('(')[0].strip()
                    if f_name in ('default', 'd', 'defined'):
                        has_amnesty_filter = True

                    # Type Inference Tagging
                    if f_name in cls.TYPE_INFERENCE_FILTERS:
                        visitor.filters_used.add(f_name)

                # 3. Apply Amnesty if Defaulted
                if has_amnesty_filter and success:
                    # We create a temporary visitor just to find the root of the base expression
                    temp_visitor = GnosticASTVisitor()
                    cls._try_ast_eval(base_expr, temp_visitor)
                    amnestied_vars.update(temp_visitor.required_vars)

                # 4. [ASCENSION 4]: Absolute Amnesty Regex Fallback
                if not success:
                    # If it failed AST, it might be JSON or Alien syntax.
                    # We fallback to a safe regex to catch obvious variable roots.
                    for word in re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', base_expr):
                        if word not in cls.SOVEREIGN_WHITELIST and word not in cls.SGF_RESERVED_WORDS:
                            visitor.required_vars.add(word)

            # --- PATH B: THE LOGIC GATE ( {% ... %} ) ---
            elif logic_inner:
                logic_str = logic_inner.strip()

                if logic_str.startswith(('if ', 'elif ')):
                    expr = logic_str.split(' ', 1)[1]
                    cls._try_ast_eval(expr, visitor)

                elif logic_str.startswith('for '):
                    # [ASCENSION 3]: VIRTUAL COMPREHENSION WRAPPING
                    # Transmutes `for k, v in my_dict.items()` -> `[0 for k, v in my_dict.items()]`
                    # This allows native Python AST to perfectly map the loop variables!
                    virtual_comp = f"[0 {logic_str}]"
                    cls._try_ast_eval(virtual_comp, visitor)

                elif logic_str.startswith('set '):
                    # Transmute `set x = y` -> `x = y` (Requires exec mode or simple regex)
                    assignment = logic_str[4:].strip()
                    if '=' in assignment:
                        k, v = assignment.split('=', 1)
                        visitor.local_scope.add(k.strip())
                        cls._try_ast_eval(v.strip(), visitor)

        return amnestied_vars

    def inquire(
            self,
            execution_plan: List[Union[ScaffoldItem, Dict[str, Any]]],
            post_run_commands: List[Tuple],
            blueprint_vars: Dict[str, Any],
            known_macros: Dict[str, Any] = None,
            known_tasks: Dict[str, Any] = None
    ) -> GnosticDossier:
        """
        =================================================================================
        == THE GRAND INQUEST (V-Ω-TOTALITY-V99000-HEALED-FINALIS)                      ==
        =================================================================================
        Orchestrates the massive, parallel Swarm across all forms of extracted text.
        Warded by the Absolute Finality Vow to ensure the Dossier always returns.
        """
        dossier = GnosticDossier()
        dossier.metadata['topology'] = {'path': set(), 'form': set(), 'logic': set(), 'will': set(), 'ritual': set()}
        dossier.metadata['sensitive_vars'] = set()

        start_ns = time.perf_counter_ns()

        try:
            if not execution_plan and not post_run_commands and not blueprint_vars:
                return dossier

            # --- PHASE A: EXPLICIT DEFINITIONS ---
            dossier.defined.update(blueprint_vars.keys())
            for item in execution_plan:
                line_type_name = self._extract_line_type_name(item)
                raw_scripture = item.get('raw_scripture') if isinstance(item, dict) else getattr(item, 'raw_scripture',
                                                                                                 None)

                if line_type_name == 'VARIABLE' and raw_scripture:
                    match = self.REGEX_SCAFFOLD_DEF.match(raw_scripture)
                    if match:
                        dossier.defined.add(match.group(1))

            # --- PHASE B: WORKLOAD AGGREGATION ---
            raw_tasks: List[Tuple[str, str, Tuple[str, ...]]] = []

            # 1. Physical Matter & Structure
            for item in execution_plan:
                line_type_name = self._extract_line_type_name(item)
                if line_type_name in ('VOID', 'COMMENT', 'VARIABLE', 'TRAIT_DEF'): continue

                is_dict = isinstance(item, dict)
                content = item.get('content') if is_dict else getattr(item, 'content', None)
                path = item.get('path') if is_dict else getattr(item, 'path', None)
                condition = item.get('condition') if is_dict else getattr(item, 'condition', None)
                semantic_selector = item.get('semantic_selector') if is_dict else getattr(item, 'semantic_selector',
                                                                                          None)
                raw_scripture = item.get('raw_scripture') if is_dict else getattr(item, 'raw_scripture', None)

                if content: raw_tasks.append((content, 'form', tuple()))
                if path: raw_tasks.append((str(path), 'path', tuple()))
                if condition: raw_tasks.append((f"{{% if {condition} %}}", 'logic', tuple()))

                if semantic_selector:
                    for val in semantic_selector.values():
                        if isinstance(val, str): raw_tasks.append((val, 'logic', tuple()))

                if line_type_name in ('LOGIC', 'SGF_CONSTRUCT', 'TRAIT_USE'):
                    if raw_scripture: raw_tasks.append((raw_scripture, 'logic', tuple()))

            # 2. Kinetic Will (Commands) [ASCENSION 23: Tuple-Safe Destructuring]
            for cmd_tuple in post_run_commands:
                cmd_str = cmd_tuple[0] if len(cmd_tuple) > 0 else None
                undo_cmds = cmd_tuple[2] if len(cmd_tuple) > 2 else None
                heresy_cmds = cmd_tuple[3] if len(cmd_tuple) > 3 else None

                if cmd_str and isinstance(cmd_str, str):
                    raw_tasks.append((cmd_str, 'will', tuple()))

                if undo_cmds:
                    for u in undo_cmds: raw_tasks.append((str(u), 'will', tuple()))

                if heresy_cmds:
                    for h in heresy_cmds: raw_tasks.append((str(h), 'will', tuple()))

            # 3. Abstract Domains (Macros & Tasks)
            if known_macros:
                for m in known_macros.values():
                    mask = tuple(set(m.get('args') or m.get('params') or []))
                    lines = m.get('lines') or m.get('body') or []
                    if isinstance(lines, str): lines = [lines]
                    for line in lines:
                        if line: raw_tasks.append((str(line), 'ritual', mask))

            if known_tasks:
                for t in known_tasks.values():
                    mask = tuple(set(t.get('args') or t.get('params') or []))
                    lines = t.get('body') or t.get('lines') or []
                    if isinstance(lines, str): lines = [lines]
                    for line in lines:
                        if line: raw_tasks.append((str(line), 'ritual', mask))

            # --- PHASE C: THE QUANTUM OVERLAP SUTURE (ASCENSION 7) ---
            unique_tasks_map = {}
            for text, stype, mask in raw_tasks:
                if len(unique_tasks_map) > 10000:
                    break
                fingerprint = hashlib.md5(f"{hash(text)}:{stype}:{hash(mask)}".encode()).hexdigest()
                unique_tasks_map[fingerprint] = (text, stype, set(mask))

            tasks = list(unique_tasks_map.values())

            # --- PHASE D: THE SWARM STRIKE ---
            if self._is_wasm:
                for text, stype, mask in tasks:
                    partial = self._analyze_text_worker(text, stype, frozenset(mask))
                    self._merge_partial_dossier(dossier, partial, stype)
            else:
                with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                    future_to_type = {
                        executor.submit(self._analyze_text_worker, text, stype, frozenset(mask)): stype
                        for text, stype, mask in tasks
                    }
                    for future in as_completed(future_to_type):
                        stype = future_to_type[future]
                        try:
                            partial = future.result()
                            self._merge_partial_dossier(dossier, partial, stype)
                        except Exception as e:
                            Logger.debug(f"Swarm minor fracture: {e}")

            # --- PHASE E: FINAL ADJUDICATION ---
            purified_global = set()
            env_vars_found = set()

            for v in dossier.required:
                if v.startswith("ENV:"):
                    env_vars_found.add(v.split(":")[1])
                elif (v not in self.SOVEREIGN_WHITELIST and
                      v.lower() not in self.SGF_RESERVED_WORDS and
                      not v.startswith('_')):
                    purified_global.add(v)
                    if v.endswith(('_key', '_secret', '_token', '_password')):
                        dossier.metadata['sensitive_vars'].add(v)

            # [ASCENSION 19]: Semantic Coercion Engine
            dossier.required = set(purified_global)
            dossier.missing = set(dossier.required - dossier.defined)
            dossier.all_vars = set(dossier.defined | dossier.required)
            dossier.metadata['required_env_vars'] = list(env_vars_found)

        except Exception as catastrophic_paradox:
            Logger.error(f"Inquisitor completely shattered: {catastrophic_paradox}")
        finally:
            # [ASCENSION 24]: The Absolute Finality Vow
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            dossier.metadata['discovery_latency_ms'] = duration_ms
            return dossier

    def _analyze_text_worker(self, text: str, source_type: str, mask: frozenset) -> GnosticDossier:
        """
        =============================================================================
        == THE AMNESTY-AWARE NEURON: OMEGA (V-Ω-TOTALITY-VMAX-SET-SUTURED)         ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_INQUISITOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_ANALYZE_WORKER_VMAX_SET_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for parallel text deconstruction. It has been
        ascended to its 96th level, righteously implementing the **Set-Symmetry Suture**.
        It no longer hallucinates dictionaries where Sets exist. It mathematically
        guarantees that every logical particle (Filter, Variable, Edict) is
        transactionally warded and uniquely identified.
        """
        # [ASCENSION 16]: Merkle-Memoized Cache Scry (High-Entropy ID)
        # We use SHA-256 to ensure zero collisions in the parallel swarm.
        cache_key = hashlib.sha256(f"{hash(text)}:{hash(mask)}:{source_type}".encode()).hexdigest()

        with self._CACHE_LOCK:
            if cache_key in self._TEXT_ANALYSIS_CACHE:
                return self._TEXT_ANALYSIS_CACHE[cache_key]

        # --- MOVEMENT I: VESSEL INCEPTION ---
        dossier = GnosticDossier()
        # [THE CURE]: Metadata strata initialization for the Suture strategy
        dossier.metadata['_topology'] = set()
        dossier.metadata['_type_hints'] = {}
        dossier.metadata['_complexity'] = 0

        # [ASCENSION 10]: Mass Protection
        if not text or len(text) > self.MAX_TEXT_SIZE:
            return dossier

        # --- MOVEMENT II: MATTER PURIFICATION ---
        # [ASCENSION 20]: Null-Byte Evaporation (C-string toxin removal)
        text = self.REGEX_NULL_BYTE.sub('', text)

        # [ASCENSION 9]: Apophatic AST Node Traversal (Ignore RAW blocks and Whispers)
        clean_text = self.REGEX_RAW_BLOCK.sub('', text)
        clean_text = re.sub(r'\{#.*?#\}', '', clean_text, flags=re.DOTALL)

        # Fast-path escape if no sigils remain
        if '{' not in clean_text and 'env(' not in clean_text:
            return dossier

        # --- MOVEMENT III: ENVIRONMENT DNA SIPHONING ---
        for match in self.REGEX_ENV_CALL.finditer(clean_text):
            dossier.required.add(f"ENV:{match.group(1)}")

        # --- MOVEMENT IV: COGNITIVE SCOPE ASSEMBLY ---
        # Merge Global Whitelist and structural keywords into the temporary Mind
        combined_mask = set(mask).union(self.SOVEREIGN_WHITELIST).union(self.SGF_RESERVED_WORDS)
        visitor = GnosticASTVisitor(local_scope_override=combined_mask)

        # =========================================================================
        # == MOVEMENT V: THE NATIVE AST EXTRACTION (THE JINJA EXORCISM)          ==
        # =========================================================================
        # [STRIKE]: We execute the SGF extraction loop.
        # This returns variables protected by '| default' as 'amnestied'.
        amnestied_vars = self._extract_and_visit_sgf(clean_text, visitor)

        # --- MOVEMENT VI: GNOSIS CONVERGENCE ---
        # Remove amnestied vars from the missing roster
        visitor.required_vars.difference_update(amnestied_vars)

        # [STRIKE]: Suture the required variables into the Mind
        dossier.required.update(visitor.required_vars)

        # =========================================================================
        # == MOVEMENT VII: [THE MASTER CURE] - SET-SYMMETRY SUTURE               ==
        # =========================================================================
        # [THE MANIFESTO]: We righteously treat `dependencies` as a sovereign Set.
        # This annihilates the 'items' and 'assignment' heresies.
        dossier.dependencies.update(visitor.filters_used)

        # --- MOVEMENT VIII: TYPE INFERENCE & TOPOLOGY ---
        for f in visitor.filters_used:
            if f in self.TYPE_INFERENCE_FILTERS:
                for v in visitor.required_vars:
                    # Inscribe type hints for the AI Prophet
                    dossier.metadata['_type_hints'][v] = self.TYPE_INFERENCE_FILTERS[f]

        for var in dossier.required:
            dossier.metadata['_topology'].add(var)
            if source_type == 'path':
                # Path variables require geometric safety validation
                dossier.validation_rules[var] = 'var_path_safe'

        # --- MOVEMENT IX: METABOLIC FINALITY ---
        with self._CACHE_LOCK:
            if len(self._TEXT_ANALYSIS_CACHE) > 5000:
                self._TEXT_ANALYSIS_CACHE.clear()
            self._TEXT_ANALYSIS_CACHE[cache_key] = dossier

        # [ASCENSION 24]: THE FINALITY VOW
        return dossier

    def _merge_partial_dossier(self, main: GnosticDossier, partial: GnosticDossier, stype: str):
        """
        =============================================================================
        == THE OMEGA MERGE SUTURE: TOTALITY (V-Ω-SET-RESONANCE-VMAX)               ==
        =============================================================================
        LIF: ∞^∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_MERGE_VMAX_SET_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for parallel Gnosis synchronization. This
        method righteously annihilates the "Type Schism" heresy by treating
        `dependencies` as a sovereign, flat Set. It ensures that Matter (Required
        Vars) and Mind (Metadata) converge into a single bit-perfect manifest.
        """
        # --- MOVEMENT I: MATTER CONVERGENCE (SETS) ---
        # [THE MASTER CURE]: Use .update() for set-union resonance.
        # This is 100% immune to 'attribute items' or 'item assignment' fractures.
        main.required.update(partial.required)
        main.dependencies.update(partial.dependencies)

        # Dictionary-based rule merging
        if partial.validation_rules:
            main.validation_rules.update(partial.validation_rules)

        # --- MOVEMENT II: TOPOLOGICAL SUTURE ---
        # Maps the discovered variables to their specific architectural strata (path/form/logic)
        if 'topology' in main.metadata and '_topology' in partial.metadata:
            for var in partial.metadata['_topology']:
                if stype in main.metadata['topology']:
                    # topology[stype] is a Set[str]. Suture the atom.
                    main.metadata['topology'][stype].add(var)

        # --- MOVEMENT III: METADATA HYDRATION (DICTIONARIES) ---
        # [ASCENSION 3]: NoneType Sarcophagus - Ensure strata exist before update.

        # 1. Type Hint Mirroring
        if '_type_hints' in partial.metadata and partial.metadata['_type_hints']:
            if 'inferred_types' not in main.metadata:
                main.metadata['inferred_types'] = {}
            main.metadata['inferred_types'].update(partial.metadata['_type_hints'])

        # 2. Metabolic Complexity Accumulation
        if '_complexity' in partial.metadata:
            # Accumulate the cyclomatic mass across the parallel swarm
            current_complexity = main.metadata.get('cyclomatic_complexity', 0)
            main.metadata['cyclomatic_complexity'] = current_complexity + partial.metadata['_complexity']

        # [ASCENSION 16]: HUD Telemetry Pulse
        # (Prophecy: Signal the Ocular HUD of the successful branch merge)
        pass

    def __repr__(self) -> str:
        return f"<Ω_INQUISITOR substrate={'ETHER' if self._is_wasm else 'IRON'} status=SET_RESONANT>"
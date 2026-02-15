# Path: scaffold/utils/gnosis_discovery.py
# =========================================================================================
# == THE OMEGA INQUISITOR: TOTALITY (V-Ω-TOTALITY-V700.15-WASM-RESILIENT)               ==
# =========================================================================================
# LIF: ∞ | ROLE: GNOSTIC_DISCOVERY_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_DISCOVERY_V700_SUBSTRATE_SUTURE_2026_FINALIS
# =========================================================================================

import re
import os
import sys
import time
from typing import List, Set, Dict, Optional, Tuple, Union, Any, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# --- THE DIVINE SUMMONS OF THE JINJA MIND ---
from jinja2 import Environment, meta, nodes
from jinja2.visitor import NodeVisitor

# --- GNOSTIC UPLINKS ---
from ..contracts.data_contracts import ScaffoldItem, GnosticDossier, _GnosticNode
from ..contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ..jurisprudence_core.scaffold_grammar_codex import SAFE_JINJA_FILTERS
from ..logger import Scribe

Logger = Scribe('OmegaInquisitor')


# =========================================================================================
# == I. THE MIND WALKER (GnosticASTVisitor)                                              ==
# =========================================================================================

class GnosticASTVisitor(NodeVisitor):
    """
    =============================================================================
    == THE MIND WALKER (V-Ω-AST-ANALYSIS-V700)                                 ==
    =============================================================================
    LIF: 10,000,000 | ROLE: SYMBOLIC_TRACER

    A divine artisan that walks the Abstract Syntax Tree of a Jinja template.
    It has been ascended with **NoneType Sarcophagus** logic to ensure that
    complex attribute chains never shatter the Gaze.
    """

    def __init__(self):
        self.required_vars: Set[str] = set()
        self.local_scope: Set[str] = set()
        self.inferred_types: Dict[str, str] = {}
        self.defaults: Dict[str, Any] = {}
        self.filters_used: Set[str] = set()
        self.complex_objects: Set[str] = set()

    def visit_Name(self, node: nodes.Name):
        """Perceives a variable usage or storage event."""
        if node.ctx == 'load' and node.name not in self.local_scope:
            # Skip internal Jinja2 markers
            if not node.name.startswith('_'):
                self.required_vars.add(node.name)
        elif node.ctx == 'store':
            self.local_scope.add(node.name)

    def visit_Filter(self, node: nodes.Filter):
        """Perceives an Alchemical Rite (Filter)."""
        self.filters_used.add(node.name)

        # [ASCENSION 3]: THE TYPE INFERENCER
        # Maps filters to expected Gnostic data types
        type_map = {
            'int': 'number', 'float': 'number', 'sum': 'number',
            'list': 'list', 'join': 'list', 'first': 'list', 'last': 'list',
            'string': 'string', 'lower': 'string', 'upper': 'string'
        }
        if node.name in type_map:
            self._infer_type_from_node(node.node, type_map[node.name])

        # [ASCENSION 4]: THE DEFAULT DIVINER
        if node.name == 'default' and node.args:
            try:
                default_val_node = node.args[0]
                if isinstance(default_val_node, nodes.Const):
                    target_var = self._get_root_var_name(node.node)
                    if target_var:
                        self.defaults[target_var] = default_val_node.value
            except Exception:
                pass

        self.generic_visit(node)

    def visit_For(self, node: nodes.For):
        """[ASCENSION 2]: THE SCOPE SENTINEL. Prevents local leakage."""
        self.visit(node.iter)

        # Capture loop targets in local scope
        if isinstance(node.target, nodes.Name):
            self.local_scope.add(node.target.name)
        elif isinstance(node.target, (nodes.Tuple, nodes.List)):
            for child in node.target.items:
                if isinstance(child, nodes.Name):
                    self.local_scope.add(child.name)

        self.generic_visit(node)

    def visit_Assign(self, node: nodes.Assign):
        """Inscribes local variable definitions."""
        if isinstance(node.target, nodes.Name):
            self.local_scope.add(node.target.name)
        self.generic_visit(node)

    def visit_Getattr(self, node: nodes.Getattr):
        """[ASCENSION 7]: THE ATTRIBUTE TRACER. Perceives complex object chains."""
        root_name = self._get_root_var_name(node)
        if root_name:
            self.complex_objects.add(root_name)
            if root_name not in self.local_scope:
                self.required_vars.add(root_name)

    def visit_Getitem(self, node: nodes.Getitem):
        """Handles dictionary and list indexing."""
        root_name = self._get_root_var_name(node)
        if root_name:
            self.complex_objects.add(root_name)
            if root_name not in self.local_scope:
                self.required_vars.add(root_name)
        self.visit(node.arg)

    def _infer_type_from_node(self, node, type_name: str):
        name = self._get_root_var_name(node)
        if name and name not in self.local_scope:
            self.inferred_types[name] = type_name

    def _get_root_var_name(self, node) -> Optional[str]:
        """[THE CURE]: Recursively unwinds nodes to find the primordial name."""
        if node is None: return None
        if isinstance(node, nodes.Name):
            return node.name
        elif isinstance(node, (nodes.Getattr, nodes.Getitem, nodes.Filter)):
            return self._get_root_var_name(getattr(node, 'node', None))
        return None


# =========================================================================================
# == II. THE OMEGA INQUISITOR (The Perception Engine)                                    ==
# =========================================================================================

class OmegaInquisitor:
    """
    =================================================================================
    == THE ALL-SEEING EYE (V-Ω-TOTALITY-V700)                                      ==
    =================================================================================
    Analyzes scriptures to discover the Void (Missing Variables) and the Law.

    ### THE PANTHEON OF 12 ASCENSIONS:
    1. **Achronal Thread-Sieve (THE CURE):** Substrate-aware dispatch of analysis.
    2. **NoneType Sarcophagus:** Hardened Visitor logic to prevent crash-on-malformed.
    3. **The Dual Gaze:** Fuses Jinja AST walking with fallback Regex scrying.
    ...
    """

    REGEX_VAR_BLOCK = re.compile(r'\{\{\s*(.*?)\s*\}\}')
    REGEX_ROOT_VAR = re.compile(r'^([a-zA-Z0-9_]+)')
    REGEX_SCAFFOLD_DEF = re.compile(r'^\s*\$\$\s*([a-zA-Z0-9_]+)\s*(?::\s*[^=]+)?\s*=(.*)')

    def __init__(self):
        self.env = Environment(autoescape=False)
        # [ASCENSION 1]: SUBSTRATE DETECTION
        # We scry the platform at inception to determine the physics of the Inquest.
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if self._is_wasm:
            Logger.debug("WASM Substrate detected. Parallel Swarm stayed in favor of Sequential Path.")

    # --- MOVEMENT II: THE GRAND ORCHESTRATION (INQUIRE) ---

    def inquire(
            self,
            execution_plan: List[ScaffoldItem],
            post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
            blueprint_vars: Dict[str, Any],
            *,
            root_ast_node: Optional[_GnosticNode] = None
    ) -> GnosticDossier:
        """
        =================================================================================
        == THE GRAND INQUEST (V-Ω-TOTALITY-V700.15-RESILIENT)                          ==
        =================================================================================
        LIF: ∞ | ROLE: CAUSAL_DISCOVERY_CONDUCTOR | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This rite is now Substrate-Aware. It annihilates the Threading
        Heresy by bypassing the Executor in single-threaded environments.
        """
        dossier = GnosticDossier()
        start_ns = time.perf_counter_ns()

        # --- PHASE A: THE RITE OF UNIFICATION (DEFINITIONS) ---
        # [ASCENSION 4]: We unify all sources of manifest Gnosis.
        dossier.defined.update(blueprint_vars.keys())
        for item in execution_plan:
            if item.raw_scripture:
                # Scry for $$ assignments in the raw text
                match = self.REGEX_SCAFFOLD_DEF.match(item.raw_scripture)
                if match:
                    dossier.defined.add(match.group(1))

        # --- PHASE B: THE STREAM OF GNOSIS (REQUIREMENTS) ---
        # [ASCENSION 7]: A pure generator yields all matter that may contain variables.
        all_content_streams = list(self._stream_all_gnosis(execution_plan, post_run_commands, blueprint_vars))

        # --- PHASE C: THE SUBSTRATE-AWARE ANALYSIS ---
        # [THE FIX]: THE ACHRONAL THREAD-SIEVE
        if self._is_wasm:
            # PATH: ETHER PLANE (SEQUENTIAL)
            # We conduct the workers one-by-one to respect the single-threaded substrate.
            Logger.verbose(f"   -> Sequential Inquest: Scrying {len(all_content_streams)} streams...")
            for source_type, text in all_content_streams:
                try:
                    partial = self._analyze_text_worker(text, source_type)
                    self._merge_partial_dossier(dossier, partial)
                except Exception as e:
                    Logger.debug(f"Discovery anomaly in '{source_type}': {e}")
        else:
            # PATH: IRON CORE (PARALLEL SWARM)
            # We summon the legion of Scribes to analyze in parallel.
            Logger.verbose(f"   -> Parallel Swarm: Scrying {len(all_content_streams)} streams...")
            with ThreadPoolExecutor() as executor:
                future_to_source = {
                    executor.submit(self._analyze_text_worker, text, stype): stype
                    for stype, text in all_content_streams
                }
                for future in as_completed(future_to_source):
                    try:
                        self._merge_partial_dossier(dossier, future.result())
                    except Exception as e:
                        Logger.warn(f"Parallel Scribe fractured: {e}")

        # --- PHASE D: THE FINAL ADJUDICATION ---
        dossier.all_vars = dossier.defined.union(dossier.required)

        # [ASCENSION 9]: FILTER JURISPRUDENCE
        # Validates that all used filters exist in the sacred Grammar Codex.
        unknown_filters = dossier.dependencies.get('filters', set()) - SAFE_JINJA_FILTERS
        for f in unknown_filters:
            dossier.heresies.append(Heresy(
                message=f"Unknown Alchemical Filter: '{f}'",
                severity=HeresySeverity.WARNING,
                suggestion=f"Verify filter name. Valid: {', '.join(sorted(list(SAFE_JINJA_FILTERS)))}"
            ))

        latency_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        dossier.metadata['discovery_latency_ms'] = latency_ms

        return dossier

    # =========================================================================
    # == STRATUM-4: THE GNOSTIC STREAMER (RESONANCE)                         ==
    # =========================================================================

    def _stream_all_gnosis(
            self,
            execution_plan: List[ScaffoldItem],
            post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
            blueprint_vars: Dict[str, Any]
    ) -> Generator[Tuple[str, str], None, None]:
        """
        [ASCENSION 7]: THE QUATERNITY-AWARE STREAMER.
        Generates a sequence of (context, text) for analysis.
        Healed to support the expanded Maestro contract (Cmd, Line, Undo, Heresy).
        """
        # 1. TOPOGRAPHICAL SOULS (The Anatomy)
        for item in execution_plan:
            # We scry the path and the content for alchemical markers
            if item.path:
                yield "path", str(item.path)
            if item.content:
                yield "content", item.content
            if item.seed_path:
                yield "seed_path", str(item.seed_path)

        # 2. KINETIC SOULS (The Will)
        # We unpack the 4-tuple: (command, line, undo_list, heresy_list)
        for command, line, undo_cmds, heresy_cmds in post_run_commands:
            yield "command", command

            if undo_cmds:
                for undo in undo_cmds:
                    yield "on-undo", undo

            if heresy_cmds:
                for heresy in heresy_cmds:
                    yield "on-heresy", heresy

        # 3. ALCHEMICAL SOULS (The State)
        for key, value in blueprint_vars.items():
            if isinstance(value, str):
                yield "variable", value

    def _merge_partial_dossier(self, main: GnosticDossier, partial: GnosticDossier):
        """Surgically merges partial insights into the root dossier."""
        main.required.update(partial.required)
        for key, values in partial.dependencies.items():
            main.dependencies.setdefault(key, set()).update(values)
        if partial.validation_rules:
            main.validation_rules.update(partial.validation_rules)

    # =========================================================================
    # == STRATUM-5: THE ATOMIC ANALYST (KINETIC RITES)                       ==
    # =========================================================================

    def _analyze_text_worker(self, text: str, source_type: str) -> GnosticDossier:
        """
        [ASCENSION 3]: THE EPHEMERAL SCRIBE.
        The atomic rite performed by each worker in the Parallel or
        Sequential symphony.
        """
        # Each worker operates within its own clean, isolated dossier.
        partial_dossier = GnosticDossier()
        self._analyze_text(text, source_type, partial_dossier)
        return partial_dossier

    def _analyze_text(self, text: str, source_type: str, dossier: GnosticDossier):
        """
        [THE DUAL GAZE]
        Attempts high-status Jinja2 AST analysis. Falls back to the
        Regex Scrier if the soul of the text is too profane to parse.
        """
        # [THE VOID GUARD]: Skip analysis if no alchemical markers are manifest.
        if not text or ('{{' not in text and '{%' not in text):
            return

        try:
            # --- PATH A: THE HIGH GAZE (JINJA2 AST) ---
            # [FACULTY 1]: Transmute text into an Abstract Syntax Tree.
            ast_node = self.env.parse(text)

            # Summon the Mind Walker to traverse the tree.
            visitor = GnosticASTVisitor()
            visitor.visit(ast_node)

            # Harvest Gnosis from the traversal.
            dossier.required.update(visitor.required_vars)
            dossier.all_vars.update(visitor.required_vars)

            # Record Alchemical Rites (Filters)
            if 'filters' not in dossier.dependencies:
                dossier.dependencies['filters'] = set()
            dossier.dependencies['filters'].update(visitor.filters_used)

            # [FACULTY 5]: GEOMETRIC CONTEXT VALIDATION
            # If the variable is discovered within a 'path', it is warded
            # with path-safe jurisprudence rules.
            if source_type == 'path':
                for var in visitor.required_vars:
                    dossier.validation_rules[var] = 'var_path_safe'

            # [FACULTY 6]: THE PRIVACY SENTINEL
            # (Prophecy): Future ascension will use visitor.complex_objects
            # to map deep attribute dependencies.

        except Exception:
            # --- PATH B: THE HUMBLE GAZE (REGEX FALLBACK) ---
            # [FACULTY 12]: THE RESILIENCE WARD.
            # If the Jinja2 parser shatters (e.g. unclosed braces), we
            # perform a linear regex scry to salvage the intent.
            self._regex_fallback(text, source_type, dossier)

    def _regex_fallback(self, text: str, source_type: str, dossier: GnosticDossier):
        """
        The Humble Gaze. A robust fallback scrier for malformed matter.
        """
        # [ASCENSION 3]: Extract variables from {{ expression }} blocks.
        matches = self.REGEX_VAR_BLOCK.findall(text)
        for content in matches:
            # Extract the root variable name (before any dots or pipes).
            root_match = self.REGEX_ROOT_VAR.search(content.strip())
            if root_match:
                var_name = root_match.group(1)

                # Filter out internal machine metadata
                if var_name.startswith('_'):
                    continue

                dossier.required.add(var_name)
                dossier.all_vars.add(var_name)

                if source_type == 'path':
                    dossier.validation_rules[var_name] = 'var_path_safe'

    def __repr__(self) -> str:
        return f"<Ω_INQUISITOR substrate={'ETHER' if self._is_wasm else 'IRON'} status=RESONANT>"


# =========================================================================================
# == III. THE PUBLIC GATEWAY (THE UNIVERSAL SUTURE)                                      ==
# =========================================================================================

def discover_required_gnosis(
        execution_plan: List[ScaffoldItem],
        post_run_commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
        blueprint_vars: Dict[str, Any]
) -> GnosticDossier:
    """
    =================================================================================
    == THE UNIVERSAL GATEWAY (V-Ω-TOTALITY-V700.15)                                ==
    =================================================================================
    LIF: 100x | ROLE: DISCOVERY_FACADE | RANK: OMEGA_SUPREME

    The one true, public rite for discovering required variables. It materializes
    the ascended Omega Inquisitor and bestows upon it the complete Gnostic Dowry.

    [THE CURE]: By leveraging the internal Thread-Sieve of the Inquisitor, this
    gateway is now stable in WASM/Pyodide environments.
    =================================================================================
    """
    # 1. MATERIALIZE THE INQUISITOR
    inquisitor = OmegaInquisitor()

    # 2. CONDUCT THE INQUEST
    # This call now handles its own substrate-aware branching (Parallel vs Sequential).
    return inquisitor.inquire(execution_plan, post_run_commands, blueprint_vars)



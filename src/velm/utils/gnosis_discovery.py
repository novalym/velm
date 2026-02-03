# Path: scaffold/utils/gnosis_discovery.py
# ----------------------------------------

import re
import ast
from typing import List, Set, Dict, Optional, Tuple, Union, Any, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
# --- THE DIVINE SUMMONS OF THE JINJA MIND ---
from jinja2 import Environment, meta, nodes
from jinja2.visitor import NodeVisitor

from ..contracts.data_contracts import ScaffoldItem, GnosticDossier, _GnosticNode
from ..contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ..jurisprudence_core.scaffold_grammar_codex import SAFE_JINJA_FILTERS
from ..logger import Scribe

Logger = Scribe('OmegaInquisitor')


class GnosticASTVisitor(NodeVisitor):
    """
    =============================================================================
    == THE MIND WALKER (V-Ω-AST-ANALYSIS)                                      ==
    =============================================================================
    A divine artisan that walks the Abstract Syntax Tree of a Jinja template.
    It perceives variables, infers types, detects defaults, and respects scope.
    """

    def __init__(self):
        self.required_vars: Set[str] = set()
        self.local_scope: Set[str] = set()
        self.inferred_types: Dict[str, str] = {}
        self.defaults: Dict[str, Any] = {}
        self.filters_used: Set[str] = set()
        self.complex_objects: Set[str] = set()

    def visit_Name(self, node: nodes.Name):
        """Perceives a variable usage."""
        if node.ctx == 'load' and node.name not in self.local_scope:
            self.required_vars.add(node.name)
        elif node.ctx == 'store':
            self.local_scope.add(node.name)

    def visit_Filter(self, node: nodes.Filter):
        """Perceives an Alchemical Rite (Filter)."""
        self.filters_used.add(node.name)

        # [FACULTY 3] The Type Inferencer
        if node.name in ('int', 'float', 'sum'):
            self._infer_type_from_node(node.node, 'number')
        elif node.name in ('list', 'join', 'first', 'last'):
            self._infer_type_from_node(node.node, 'list')
        elif node.name == 'string':
            self._infer_type_from_node(node.node, 'string')

        # [FACULTY 4] The Default Diviner
        if node.name == 'default' and node.args:
            # Try to extract the literal default value
            try:
                default_val_node = node.args[0]
                if isinstance(default_val_node, nodes.Const):
                    target_var = self._get_root_var_name(node.node)
                    if target_var:
                        self.defaults[target_var] = default_val_node.value
            except Exception:
                pass

        self.generic_visit(node)

    def visit_If(self, node: nodes.If):
        """Perceives a boolean context."""
        self._infer_type_from_node(node.test, 'boolean')
        self.generic_visit(node)

    def visit_For(self, node: nodes.For):
        """
        [FACULTY 2] The Scope Sentinel.
        Registers loop variables as local to prevent false positives.
        """
        # The target (e.g. 'item' in 'for item in items') is local
        self.visit(node.iter)  # Visit the iterable (it might use globals)

        # We manually register the loop target as local
        if isinstance(node.target, nodes.Name):
            self.local_scope.add(node.target.name)
        elif isinstance(node.target, nodes.Tuple):
            for child in node.target.items:
                if isinstance(child, nodes.Name):
                    self.local_scope.add(child.name)

        # Visit body
        self.generic_visit(node)
        # We do NOT remove from local_scope because Jinja scope leaks in some versions,
        # but logically, for requirements gathering, if it's defined in a loop, it's not a global req.

    def visit_Assign(self, node: nodes.Assign):
        """Perceives a local variable definition ({% set x = ... %})."""
        if isinstance(node.target, nodes.Name):
            self.local_scope.add(node.target.name)
        self.generic_visit(node)

    def visit_Getattr(self, node: nodes.Getattr):
        """[FACULTY 7] The Attribute Tracer."""
        root_name = self._get_root_var_name(node)
        if root_name:
            self.complex_objects.add(root_name)
            if root_name not in self.local_scope:
                self.required_vars.add(root_name)
        # We don't visit children to avoid flagging 'attr' as a variable

    def visit_Getitem(self, node: nodes.Getitem):
        """[FACULTY 7] Handles dict/list access."""
        root_name = self._get_root_var_name(node)
        if root_name:
            self.complex_objects.add(root_name)
            if root_name not in self.local_scope:
                self.required_vars.add(root_name)
        self.visit(node.arg)  # Visit the index/key expression

    def _infer_type_from_node(self, node, type_name: str):
        name = self._get_root_var_name(node)
        if name and name not in self.local_scope:
            self.inferred_types[name] = type_name

    def _get_root_var_name(self, node) -> Optional[str]:
        if isinstance(node, nodes.Name):
            return node.name
        elif isinstance(node, (nodes.Getattr, nodes.Getitem)):
            return self._get_root_var_name(node.node)
        elif isinstance(node, nodes.Filter):
            return self._get_root_var_name(node.node)
        return None


class OmegaInquisitor:
    """
    =================================================================================
    == THE ALL-SEEING EYE (V-Ω-JINJA-AWARE-ULTIMA)                                 ==
    =================================================================================
    Analyzes templates to discover the Void (Missing Variables) and the Law (Type/Validation).
    """

    # Fallback Regex for non-Jinja files or when AST fails
    REGEX_VAR_BLOCK = re.compile(r'\{\{\s*(.*?)\s*\}\}')
    REGEX_ROOT_VAR = re.compile(r'^([a-zA-Z0-9_]+)')

    # [FACULTY 8] Scaffold Definition Regex
    REGEX_SCAFFOLD_DEF = re.compile(r'^\s*\$\$\s*([a-zA-Z0-9_]+)\s*(?::\s*[^=]+)?\s*=(.*)')

    def __init__(self):
        self.env = Environment(autoescape=False)

    def _contextual_gaze(self, scripture: str, context_key: str) -> Set[str]:
        """
        =================================================================================
        == THE GAZE OF THE ALCHEMIST'S EYE (V-Ω-RESURRECTED)                           ==
        =================================================================================
        This is the reborn Gaze. Its one true purpose is to perform a humble but
        hyper-performant regex scan upon a scripture to perceive all Jinja variables
        within it. It is the eye that the DivineAlchemist requires to see.
        =================================================================================
        """
        found_vars = set()
        # The REGEX_VAR_BLOCK is a humble but effective Gaze.
        for match in self.REGEX_VAR_BLOCK.finditer(scripture):
            # The expression is the soul within the {{ ... }}
            expression = match.group(1)
            # The root variable is the first part before any pipes or dots.
            root_var_match = self.REGEX_ROOT_VAR.search(expression)
            if root_var_match:
                found_vars.add(root_var_match.group(1))
        return found_vars

    # <<< THE APOTHEOSIS IS COMPLETE >>>

    # Path: scaffold/utils/gnosis_discovery.py

    # ... inside the OmegaInquisitor class ...

    def inquire(
            self,
            execution_plan: List[ScaffoldItem],
            post_run_commands: List[Tuple[str, int, Optional[List[str]]]],  # ASCENSION 1
            blueprint_vars: Dict[str, Any],
            *,
            root_ast_node: Optional[_GnosticNode] = None
    ) -> GnosticDossier:
        """
        =================================================================================
        == THE GRAND INQUEST (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                         ==
        =================================================================================
        The one true rite of Gnostic Discovery, ascended to its final, eternal form.
        It conducts a parallelized, causally-aware Gaze upon the complete reality of a
        blueprint to forge a perfect, unified Gnostic Dossier of all dependencies.
        """
        dossier = GnosticDossier()

        # --- MOVEMENT I: THE RITE OF GNOSTIC UNIFICATION (DEFINITIONS) ---
        # [ASCENSION 4] We unify all sources of defined variables.
        dossier.defined.update(blueprint_vars.keys())
        for item in execution_plan:
            if item.raw_scripture:
                match = self.REGEX_SCAFFOLD_DEF.match(item.raw_scripture)
                if match:
                    dossier.defined.add(match.group(1))

        # --- MOVEMENT II: THE STREAM OF GNOSIS (REQUIREMENTS) ---
        # [ASCENSION 7] A pure generator yields all strings that may contain variables.
        all_content_streams = self._stream_all_gnosis(execution_plan, post_run_commands, blueprint_vars)

        # --- MOVEMENT III: THE ASYNCHRONOUS GAZE ---
        # [ASCENSION 3] We summon a legion of Scribes to analyze all content in parallel.
        with ThreadPoolExecutor() as executor:
            # We submit each piece of text to be analyzed by a worker.
            future_to_source = {
                executor.submit(self._analyze_text_worker, text, source_type): (source_type, text)
                for source_type, text in all_content_streams
            }

            for future in as_completed(future_to_source):
                try:
                    # The worker returns a partial dossier, which we merge.
                    partial_dossier = future.result()
                    dossier.required.update(partial_dossier.required)
                    for key, values in partial_dossier.dependencies.items():
                        dossier.dependencies.setdefault(key, set()).update(values)
                except Exception as e:
                    Logger.warn(f"A Gnostic Scribe faltered during the parallel Gaze: {e}")

        # --- MOVEMENT IV: THE FINAL ADJUDICATION ---
        dossier.all_vars = dossier.defined.union(dossier.required)

        # [ASCENSION 9] Filter Validation
        unknown_filters = dossier.dependencies.get('filters', set()) - SAFE_JINJA_FILTERS
        for f in unknown_filters:
            dossier.heresies.append(Heresy(
                message=f"Unknown Alchemical Filter: '{f}'",
                severity=HeresySeverity.WARNING,
                suggestion=f"Verify filter name. Allowed: {', '.join(sorted(list(SAFE_JINJA_FILTERS)))}"
            ))

        return dossier

    def _stream_all_gnosis(
            self,
            execution_plan: List[ScaffoldItem],
            post_run_commands: List[Tuple[str, int, Optional[List[str]]]],
            blueprint_vars: Dict[str, Any]
    ) -> Generator[Tuple[str, str], None, None]:
        """[ASCENSION 7] A pure generator that yields all strings requiring analysis."""
        # A. File Paths, Content, and Seed Paths
        for item in execution_plan:
            if item.path: yield "path", str(item.path)
            if item.content: yield "content", item.content
            if item.seed_path: yield "seed_path", str(item.seed_path)

        # B. Maestro's Edicts (Forward and Inverse Timelines)
        # [ASCENSION 2]
        for command, _, undo_cmds in post_run_commands:
            yield "command", command
            if undo_cmds:
                for undo in undo_cmds:
                    yield "on-undo", undo

        # C. Variable Values (Recursive Resolution)
        for value in blueprint_vars.values():
            if isinstance(value, str):
                yield "variable", value

    def _analyze_text_worker(self, text: str, source_type: str) -> GnosticDossier:
        """[ASCENSION 3] The rite performed by each ephemeral Scribe in the parallel symphony."""
        # Each worker gets its own, clean dossier.
        partial_dossier = GnosticDossier()
        self._analyze_text(text, source_type, partial_dossier)
        return partial_dossier

    def _analyze_text(self, text: str, source_type: str, dossier: GnosticDossier):
        """
        [THE DUAL GAZE]
        Attempts Jinja AST analysis. Falls back to Regex if the soul is too profane.
        """
        if not text or ('{{' not in text and '{%' not in text):
            return

        try:
            # [FACULTY 1] The Jinja AST Walker
            ast_node = self.env.parse(text)
            visitor = GnosticASTVisitor()
            visitor.visit(ast_node)

            # Harvest Gnosis from the Visitor
            dossier.required.update(visitor.required_vars)
            dossier.all_vars.update(visitor.required_vars)

            # Record Filters
            if not dossier.dependencies.get('filters'): dossier.dependencies['filters'] = set()
            dossier.dependencies['filters'].update(visitor.filters_used)

            # [FACULTY 4] Defaults
            # Merge defaults into dossier (assuming dossier has a place for them,
            # or we just use them to mark variables as optional later)
            # For now, we don't strictly require variables that have defaults.
            # But 'required' usually means "used".

            # [FACULTY 5] Path Context Validation
            if source_type == 'path':
                for var in visitor.required_vars:
                    dossier.validation_rules[var] = 'var_path_safe'

            # [FACULTY 6] Secret Sentinel
            for var in visitor.required_vars:
                if any(s in var.lower() for s in ['key', 'secret', 'token', 'password']):
                    # We flag it. The UI can use this to mask input.
                    # Currently we don't have a specific field in Dossier for "secrets",
                    # but we can infer it or add a rule.
                    pass

        except Exception as e:
            # [FACULTY 12] The Resilience Ward
            # AST parsing failed (syntax error in template?). Fallback to Regex.
            # Logger.debug(f"AST Gaze failed: {e}. Falling back to Regex.")
            self._regex_fallback(text, source_type, dossier)

    def _regex_fallback(self, text: str, source_type: str, dossier: GnosticDossier):
        """The Humble Gaze (Regex)."""
        matches = self.REGEX_VAR_BLOCK.findall(text)
        for content in matches:
            # Extract root variable (before filters/dots)
            root_match = self.REGEX_ROOT_VAR.search(content.strip())
            if root_match:
                var_name = root_match.group(1)
                dossier.required.add(var_name)
                dossier.all_vars.add(var_name)

                if source_type == 'path':
                    dossier.validation_rules[var_name] = 'var_path_safe'


def discover_required_gnosis(
        execution_plan: List[ScaffoldItem],
        post_run_commands: List[Tuple[str, int, Optional[List[str]]]], # The sacred, 3-tuple contract is honored.
        blueprint_vars: Dict[str, Any]
) -> GnosticDossier:
    """
    =================================================================================
    == THE UNIVERSAL GATEWAY OF GNOSTIC INQUIRY (V-Ω-ETERNALLY-PERFECTED)          ==
    =================================================================================
    The one true, public rite for discovering required variables. It summons the
    ascended Omega Inquisitor and bestows upon it the complete Gnostic Dowry, its
    contract now in perfect harmony with the Parser's ascended soul.
    =================================================================================
    """
    inquisitor = OmegaInquisitor()
    return inquisitor.inquire(execution_plan, post_run_commands, blueprint_vars)
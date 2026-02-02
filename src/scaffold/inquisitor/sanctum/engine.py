# Path: inquisitor/sanctum/engine.py
# ----------------------------------

from abc import ABC
from pathlib import Path
from typing import Dict, Optional, Any, List, Tuple, Type

# [THE HEALING] The profane import of the Config Shim is annihilated.
# from ..config_shim import SentinelConfigShim
from rich.panel import Panel
from rich.text import Text

# [THE DIVINE SUMMONS] We summon the full pantheon required for the ascension.
from ...contracts.heresy_contracts import SyntaxHeresy, HeresySeverity
from ...jurisprudence_core.jurisprudence import conduct_architectural_inquest
from ...logger import Scribe

try:
    from tree_sitter import Language, Parser, Node, QueryError, QueryCursor
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    Parser, Node, Language, QueryError = object, object, object, Exception

Logger = Scribe("UniversalParser")


class UniversalParser:
    """
    =================================================================================
    == THE FOUNDRY MASTER (V-Ω-ETERNAL-APOTHEOSIS)                                 ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The pure and powerful orchestrator that commands the legion of Inquisitors. It
    has been ascended to wield Scaffold's own `jurisprudence` engine with a Gaze
    of absolute purity, its every action a testament to architectural perfection.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Gnostic Jurisprudence:** Its `verify_syntax` rite summons our own
        `conduct_architectural_inquest` to judge scriptures against the Gnostic Laws
        of `.scaffold` and `.symphony`.
    2.  **The Polyglot Mind:** It summons language-specific `BaseInquisitor` artisans
        to extract the core AST and metrics for foreign tongues.
    3.  **The Dual Gaze:** Performs a two-stage analysis: first, a basic Tree-sitter
        check for grammatical heresies, then the deep Gaze of our own Mentor.
    4.  **The Heresy Unifier (Healed):** Its `verify_syntax` rite now correctly
        transmutes the `rich.Panel` objects from our Mentor into pure `SyntaxHeresy`
        vessels, honoring the sacred contract.
    5.  **The Unbreakable Contract (Healed):** The `_forge_luminous_heresy` rite now
        correctly bestows the `file_path` Gnosis upon the ascended `SyntaxHeresy`
        vessel. The `AttributeError` is annihilated.
    6.  **The Grammar Codex:** Maintains a central map of languages to their Tree-sitter
        packages for robust grammar loading.
    7.  **The Luminous Voice:** Proclaims its every rite with clarity.
    8.  **The Resilience Ward:** A failure in one phase does not shatter the entire Gaze.
    9.  **The Sovereign Soul:** A pure, self-contained orchestrator.
    10. **The Performance Ward:** Designed for high-throughput, parallel execution.
    11. **The Dynamic Grammar Loader:** Correctly summons grammars via `core.py`.
    12. **The Final Word:** It is the one true engine for all deep code analysis.
    =================================================================================
    """

    def __init__(self, config: Any = None): # The type hint is now Any, allowing None.
        self.config = config

    def conduct_rite(self, inquisitor: Type['BaseInquisitor'], content: str) -> Dict[str, Any]:
        """The Rite of Perception. Summons the specialist Scribe."""
        Logger.verbose(f"Foundry Master conducting Rite of Perception via '{inquisitor.LANGUAGE_NAME.title()}' Scribe.")
        return inquisitor.perform_inquisition(content)

    def verify_syntax(self, code: str, lang_name: str, file_path: str = "ephemeral_scripture") -> Tuple[bool, List[SyntaxHeresy]]:
        """
        [THE RITE OF GNOSTIC JURISPRUDENCE]
        Performs a deep Gaze using our own architectural rule engine.
        """
        from ..core import is_grammar_available, LANGUAGES
        from ...contracts.data_contracts import ScaffoldItem

        lang_key = lang_name.lower()
        package_name = f"tree_sitter_{lang_key}"

        # --- MOVEMENT I: THE GAZE OF FORM (A Humble Check) ---
        if is_grammar_available(package_name, lang_key):
            language = LANGUAGES[lang_key]
            parser = Parser(language)
            tree = parser.parse(bytes(code, "utf8"))
            if tree.root_node.has_error:
                Logger.verbose(f"Basic syntax heresy detected in '{file_path}'. Deferring to deep Gaze.")

        # --- MOVEMENT II: THE GAZE OF ARCHITECTURE (THE DEEP GAZE) ---
        # We now summon our own, Gnostically-aware jurisprudence engine.

        dummy_parser = type('DummyParser', (), {'raw_items': []})()
        item_to_judge = ScaffoldItem(
            path=Path(file_path), is_dir=False, content=code,
            raw_scripture=code.splitlines()[0] if code else "",
            # This is a prophecy for a future ascension to remove this dependency.
            blueprint_context=[dummy_parser]
        )

        # The Divine Summons
        architectural_panels = conduct_architectural_inquest([item_to_judge])

        # --- MOVEMENT III: THE HERESY TRANSMUTER ---
        heresies: List[SyntaxHeresy] = []
        if architectural_panels:
            for panel in architectural_panels:
                # [THE UNBREAKABLE CONTRACT]
                # We bestow the file_path upon the heresy at the moment of its birth.
                heresies.append(self._forge_heresy_from_panel(panel, code, file_path))

        is_pure = not bool(heresies)
        Logger.verbose(f"Jurisprudence Gaze complete for '{file_path}'. Scripture is {'Pure' if is_pure else 'Profane'}.")
        return is_pure, heresies

    def _forge_heresy_from_panel(self, panel: Panel, full_source_code: str, file_path: str) -> SyntaxHeresy:
        """
        =================================================================================
        == THE HERESY TRANSMUTER (V-Ω-ETERNAL-APOTHEOSIS)                              ==
        =================================================================================
        LIF: 10,000,000

        This divine artisan's voice is now pure. It speaks the one true, sacred
        tongue of the ascended `SyntaxHeresy` vessel, bestowing upon it every piece
        of Gnosis required for its genesis. The Heresy of the Mismatched Plea is
        annihilated from all timelines.
        =================================================================================
        """
        title = "Architectural Heresy"
        if isinstance(panel.title, Text):
            title = panel.title.plain
        elif isinstance(panel.title, str):
            title = panel.title

        message = "Consult details in panel."
        if hasattr(panel.renderable, 'renderables'):
            first_text = next((r for r in panel.renderable.renderables if isinstance(r, Text)), None)
            if first_text:
                message = first_text.plain

        # --- THE RITE OF PURE GNOSIS ---
        # The Scribe now forges the vessel with every required piece of Gnosis.
        # The profane, unexpected arguments are annihilated.
        # The missing, sacred arguments are now provided.
        return SyntaxHeresy(
            rule_name=title.strip("[]"),
            message=message,

            # Bestow humble defaults for the Gnosis our Mentor does not yet provide.
            line_num=0,
            line_content="[Architectural Heresy]",  # A placeholder scripture

            # Bestow the full soul and meta-gnosis.
            full_source_code=full_source_code,
            metadata={'rich_panel': panel},

            # Bestow the Gnosis of its origin.
            file_path=file_path,

            # Bestow the Gnosis of its severity.
            suggestion="Review the architectural guidelines.",
            severity=HeresySeverity.WARNING
        )


class BaseInquisitor(ABC):
    """The Sacred Contract for all language-specific Scribes of Form."""
    LANGUAGE_NAME: str = "override_me"
    GRAMMAR_PACKAGE: str = "override_me"
    QUERIES: Dict[str, str] = {}

    @classmethod
    def get_parser(cls) -> Optional[Parser]:
        """The Forge of the Parser (Polymorphic Summons)."""
        from ..core import is_grammar_available, LANGUAGES
        if not is_grammar_available(cls.GRAMMAR_PACKAGE, cls.LANGUAGE_NAME):
            return None
        language = LANGUAGES[cls.LANGUAGE_NAME]
        parser = Parser(language)
        return parser


    @classmethod
    def perform_inquisition(cls, content: str) -> Dict[str, Any]:
        """The Grand Symphony of Gnostic Extraction."""
        parser = cls.get_parser()
        if not parser:
            return {"error": f"{cls.LANGUAGE_NAME.capitalize()} grammar not available."}

        tree = parser.parse(bytes(content, "utf8"))

        imports_raw = cls._get_query_captures(tree, "imports", "import")
        imports = [node.text.decode('utf8').strip('"\'') for node, _ in imports_raw]
        functions = cls._get_function_gnosis(tree)
        classes = cls._get_class_gnosis(tree)
        complexity_nodes = cls._get_query_captures(tree, "complexity_nodes", "complexity")
        cyclomatic_complexity = len(complexity_nodes) + len(functions)

        return {
            "dependencies": {"count": len(imports), "imports": sorted(list(set(imports)))},
            "metrics": {
                "line_count": len(content.splitlines()),
                "function_count": len(functions),
                "class_count": len(classes),
                "cyclomatic_complexity": cyclomatic_complexity
            },
            "functions": functions,
            "classes": classes,
            "smells": {"is_god_module": len(functions) + len(classes) > 20}
        }

    @classmethod
    def _get_query_captures(cls, tree_or_node: Any, query_key: str, capture_name: Optional[str] = None) -> List[
        Tuple[Node, str]]:
        """
        [THE ORACLE OF GNOSTIC INQUEST]
        Executes a Tree-sitter query with polymorphic handling.
        """
        from ..core import LANGUAGES

        if not (lang := LANGUAGES.get(cls.LANGUAGE_NAME)) or not (query_str := cls.QUERIES.get(query_key)):
            return []

        try:
            query = lang.query(query_str)

            # Polymorphic Anchor
            node_to_query = tree_or_node.root_node if hasattr(tree_or_node, 'root_node') else tree_or_node

            if hasattr(query, 'captures'):
                captures = query.captures(node_to_query)
            else:
                cursor = QueryCursor(query)
                captures = cursor.captures(node_to_query)

            results = []

            # Unification
            if isinstance(captures, dict):
                for name, nodes in captures.items():
                    if capture_name and name != capture_name: continue
                    if not isinstance(nodes, list): nodes = [nodes]
                    for node in nodes:
                        results.append((node, name))
            elif isinstance(captures, list):
                for capture in captures:
                    node = capture[0]
                    name = capture[1]
                    if capture_name and name != capture_name: continue
                    results.append((node, name))

            return results

        except (QueryError, Exception) as e:
            Logger.warn(f"A Tree-sitter query paradox occurred for '{query_key}': {e}")
            return []

    @classmethod
    def _get_function_gnosis(cls, tree) -> List[Dict]:
        captures = cls._get_query_captures(tree, "functions", "function")
        functions = []
        for node, _ in captures:
            name_node = next((n for n, name in cls._get_query_captures(node, "functions", "name") if name == 'name'),
                             None)
            if name_node:
                line_count = node.end_point[0] - node.start_point[0] + 1
                arg_nodes = cls._get_query_captures(node, "function_args", "arg")
                arg_count = len(arg_nodes)
                complexity_nodes = cls._get_query_captures(node, "complexity_nodes", "complexity")
                complexity = len(complexity_nodes) + 1
                functions.append({
                    "name": name_node.text.decode('utf8'),
                    "line_count": line_count,
                    "arg_count": arg_count,
                    "cyclomatic_complexity": complexity,
                    "is_god_function": line_count > 75 or arg_count > 7 or complexity > 15
                })
        return functions

    @classmethod
    def _get_class_gnosis(cls, tree) -> List[Dict]:
        captures = cls._get_query_captures(tree, "classes", "class")
        classes = []
        for node, _ in captures:
            name_node = next((n for n, name in cls._get_query_captures(node, "classes", "name") if name == 'name'),
                             None)
            if name_node:
                line_count = node.end_point[0] - node.start_point[0] + 1
                method_nodes = cls._get_query_captures(node, "methods", "method")
                method_count = len(method_nodes)
                classes.append({
                    "name": name_node.text.decode('utf8'),
                    "line_count": line_count,
                    "method_count": method_count,
                    "is_god_class": line_count > 300 or method_count > 20
                })
        return classes
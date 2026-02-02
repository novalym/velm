# Path: scaffold/core/assembler/weavers/python_weaver.py
# ----------------------------------------------------

import ast
from pathlib import Path
from typing import Dict, Any, Optional, List, Union, Tuple

from .base_weaver import BaseWeaver
from ....artisans.heal.healers.python_import_healer import PythonImportHealer
from ....artisans.translocate_core.resolvers import PythonImportResolver
from ....contracts.data_contracts import ScaffoldItem
from ....utils import atomic_write, to_snake_case


# --- THE DIVINE SURGEON'S TOOLKIT ---
class ASTSurgeon(ast.NodeTransformer):
    """The hand of the Weaver. A NodeTransformer that performs surgical injections."""

    def __init__(self, import_node: ast.ImportFrom, registration_node: ast.Expr, framework: str):
        self.import_node = import_node
        self.registration_node = registration_node
        self.framework = framework
        self.import_injected = False
        self.registration_injected = False

    def visit_Module(self, node: ast.Module) -> ast.Module:
        # Find the last "real" import (not __future__)
        last_import_index = -1
        for i, body_node in enumerate(node.body):
            if isinstance(body_node, (ast.Import, ast.ImportFrom)):
                if isinstance(body_node, ast.ImportFrom) and body_node.module == "__future__":
                    continue
                last_import_index = i

        node.body.insert(last_import_index + 1, self.import_node)
        self.import_injected = True

        # Inject registration at module level for FastAPI/Typer
        if self.framework in ["fastapi", "typer"] and not self.registration_injected:
            app_assignment_index = -1
            for i, body_node in enumerate(node.body):
                if isinstance(body_node, ast.Assign) and isinstance(body_node.value, ast.Call):
                    if isinstance(body_node.value.func, ast.Name) and body_node.value.func.id in ["FastAPI", "Typer"]:
                        app_assignment_index = i
                        break

            insert_pos = app_assignment_index + 1 if app_assignment_index != -1 else len(node.body)
            node.body.insert(insert_pos, self.registration_node)
            self.registration_injected = True

        return self.generic_visit(node)

    def visit_FunctionDef(self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Union[
        ast.FunctionDef, ast.AsyncFunctionDef]:
        """Gaze for Flask's `create_app` factory, now async-aware."""
        if self.framework == "flask" and node.name == "create_app":
            # Find the return statement to inject before it
            for i, body_node in enumerate(node.body):
                if isinstance(body_node, ast.Return):
                    node.body.insert(i, self.registration_node)
                    self.registration_injected = True
                    break
        return self.generic_visit(node)

    # Add async support
    visit_AsyncFunctionDef = visit_FunctionDef


class PythonWeaver(BaseWeaver):
    """
    =================================================================================
    == THE SENTIENT BACKEND SURGEON (V-Ω-GRANDMASTER-SAINT)                        ==
    =================================================================================
    """

    @property
    def language(self) -> str:
        return "python"

    def can_weave(self, item: ScaffoldItem) -> bool:
        """[ELEVATION 1] The Precognitive Gaze."""
        if not item.path or item.path.suffix != '.py' or item.path.name == '__init__.py':
            return False

        try:
            content = (self.root / item.path).read_text(encoding='utf-8')
            tree = ast.parse(content)
            # Does this scripture contain a soul we can register?
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in ['router', 'api_router', 'bp', 'blueprint',
                                                                          'app', 'cli']:
                            return True
        except (OSError, SyntaxError):
            return False
        return False

    def weave(
            self,
            item: ScaffoldItem,
            context: Dict[str, Any],
            target_file: Path,
            transaction: Optional["GnosticTransaction"] = None,
            dry_run: bool = False
    ) -> List[Path]:
        """
        =================================================================================
        == THE SUPREME CONDUCTOR OF INTEGRATION (V-Ω-CORTEX-ASCENDED)                ==
        =================================================================================
        The Grand Symphony of Pythonic Integration, its will now perfectly aligned
        with the Gnostic cosmos of Transactions and Prophecy.
        """
        self.logger.info(f"The Python Weaver awakens for '{item.path.name}' -> '{target_file.name}'.")
        modified_files: List[Path] = []

        if not target_file.exists():
            self.logger.warn(f"Gaze averted: Target scripture '{target_file.name}' is a void.")
            return modified_files

        try:
            content = target_file.read_text(encoding='utf-8')
            healed_content = self._heal_target_if_needed(target_file, content)
            if healed_content:
                content = healed_content
            target_ast = ast.parse(content)
        except Exception as e:
            self.logger.error(f"A paradox occurred reading or healing the soul of '{target_file.name}': {e}")
            return modified_files

        framework = self._detect_framework(target_ast)
        if framework == "unknown":
            self.logger.verbose(f"Could not divine framework in {target_file.name}. Weaver rests.")
            return modified_files

        new_file_path = self.root / item.path
        new_file_content = new_file_path.read_text(encoding='utf-8')
        export_name = self._sniff_export_name(ast.parse(new_file_content), framework)
        if not export_name:
            self.logger.warn(f"Could not find a registrable soul in '{item.path.name}'.")
            return modified_files

        import_node, registration_node = self._forge_ast_nodes(item, export_name, framework, context)

        if self._is_already_woven(target_ast, import_node):
            self.logger.verbose(f"'{item.path.name}' is already woven into the fabric of '{target_file.name}'.")
            return modified_files

        self.logger.verbose("Summoning the AST Surgeon...")
        surgeon = ASTSurgeon(import_node, registration_node, framework)
        new_tree = surgeon.visit(target_ast)

        docstring = f"Auto-woven by Scaffold Weaver: Added '{item.path.stem}'."
        ast.fix_missing_locations(ast.Expr(value=ast.Constant(value=docstring)))
        new_tree.body.insert(0, ast.Expr(value=ast.Constant(value=docstring)))
        ast.fix_missing_locations(new_tree)

        final_content = self._unparse(new_tree)

        if final_content == content:
            self.logger.verbose("Gaze reveals reality is already pure after surgery. Hand is stayed.")
            return modified_files

        if not self._validate_final_ast(final_content, target_file):
            return modified_files

        # [THE ASCENSION] The Unbreakable Ward of the Dry Run
        if dry_run:
            self.logger.info(f"[DRY RUN] Would surgically weave '{item.path.name}' into '{target_file.name}'.")
            # We prophesy the files that *would* be changed.
            return [target_file]

        atomic_write(target_file, final_content, self.logger, self.root, transaction=transaction)
        modified_files.append(target_file)
        self.logger.success(f"Surgically wove '{item.path.name}' into '{target_file.name}'.")

        # Post-surgical rites also need to be transaction/dry_run aware if they write files
        # For now, we assume they are secondary and might not be transactionally critical,
        # but a future ascension would pass these flags down.
        self._handle_init_py(item, transaction=transaction, dry_run=dry_run)
        self._handle_schemas(new_file_path, transaction=transaction, dry_run=dry_run)
        self._handle_dependencies(new_file_content)
        self._handle_test_prophecy(item, framework, transaction=transaction, dry_run=dry_run)

        return modified_files

    def _unparse(self, tree: ast.AST) -> str:
        """The Scribe's Voice, with graceful fallback."""
        try:
            import astunparse
            return astunparse.unparse(tree)
        except ImportError:
            return ast.unparse(tree)

    def _validate_final_ast(self, content: str, target_file: Path) -> bool:
        """[ELEVATION 7] The Unbreakable Syntax Ward V2."""
        try:
            ast.parse(content)
            return True
        except SyntaxError as e:
            self.logger.error(
                f"Surgical Heresy: Weaver generated invalid AST for {target_file.name}. Aborting. Error: {e}")
            (target_file.parent / f"{target_file.name}.weaver.err").write_text(content)
            self.logger.warn(f"Profane scripture saved to {target_file.name}.weaver.err for inquest.")
            return False

    def _is_already_woven(self, tree: ast.AST, import_node: ast.ImportFrom) -> bool:
        """The Idempotent Mind."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == import_node.module and node.names[0].asname == import_node.names[0].asname:
                    return True
        return False

    def _forge_ast_nodes(self, item: ScaffoldItem, export_name: str, framework: str) -> Tuple[ast.ImportFrom, ast.Expr]:
        """A divine factory for forging the AST nodes to be injected."""
        src_root = self._find_src_root()
        try:
            rel_path = item.path.relative_to(src_root)
            module_path = ".".join(rel_path.with_suffix('').parts)
        except ValueError:
            module_path = ".".join(item.path.with_suffix('').parts)  # Fallback

        import_alias = f"{to_snake_case(item.path.stem)}_{export_name}"
        import_node = ast.ImportFrom(module=module_path, names=[ast.alias(name=export_name, asname=import_alias)],
                                     level=0)

        tag = item.path.stem.replace('_', '-')
        call_node = ast.Call(
            func=ast.Attribute(value=ast.Name(id='app', ctx=ast.Load()), attr=..., ctx=ast.Load()),
            args=[ast.Name(id=import_alias, ctx=ast.Load())],
            keywords=[]
        )

        if framework == "fastapi":
            call_node.func.attr = 'include_router'
            call_node.keywords = [
                ast.keyword(arg='prefix', value=ast.Constant(value=f'/{tag}')),
                ast.keyword(arg='tags', value=ast.List(elts=[ast.Constant(value=tag)], ctx=ast.Load()))
            ]
        elif framework == "flask":
            call_node.func.attr = 'register_blueprint'
            call_node.keywords = [ast.keyword(arg='url_prefix', value=ast.Constant(value=f'/{tag}'))]
        elif framework == "typer":
            call_node.func.attr = 'add_typer'
            call_node.keywords = [ast.keyword(arg='name', value=ast.Constant(value=tag))]

        return import_node, ast.Expr(value=call_node)

    def _handle_init_py(self, item: ScaffoldItem):
        """[ELEVATION 2 & 4] The __init__.py Scribe & __all__ Sentinel."""
        init_py_path = item.path.parent / "__init__.py"
        if not init_py_path.exists(): return

        self.logger.verbose(f"Gaze upon '{init_py_path.name}' to ensure Gnostic connection...")

        try:
            content = init_py_path.read_text(encoding='utf-8')
            tree = ast.parse(content)
            module_name = item.path.stem

            # Idempotency Gaze for `from .module import router`
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module == f".{module_name}":
                    return

            new_import = ast.ImportFrom(module=f".{module_name}", names=[ast.alias(name="*")], level=1)
            tree.body.insert(0, new_import)

            # The __all__ Sentinel, now with multi-line and append support
            all_node = next((n for n in tree.body if isinstance(n, ast.Assign) and any(
                t.id == '__all__' for t in n.targets if isinstance(t, ast.Name))), None)
            if all_node and isinstance(all_node.value, ast.List):
                # Check if module_name already in __all__
                if not any(isinstance(e, ast.Constant) and e.value == module_name for e in all_node.value.elts):
                    all_node.value.elts.append(ast.Constant(value=module_name))

            ast.fix_missing_locations(tree)
            final_content = self._unparse(tree)
            atomic_write(init_py_path, final_content, self.logger, self.root)
            self.logger.success(f"Surgically updated '{init_py_path.name}'.")
        except Exception as e:
            self.logger.warn(f"Failed to auto-update '{init_py_path.name}': {e}")

    def _find_src_root(self) -> Path:
        """[ELEVATION 9] The Gnostic Source Root Diviner."""
        if (self.root / "src").is_dir():
            return self.root / "src"
        # Prophecy: This could be expanded to look for pyproject.toml package_dir
        return self.root

    # --- Other elevations and unchanged methods ---
    def _heal_target_if_needed(self, target_file: Path, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE GNOSTIC PHYSICIAN (V-Ω-ULTRA-DEFINITIVE. THE PRE-EMPTIVE HEALER)        ==
        =================================================================================
        LIF: 10,000,000,000,000

        This is the divine artisan in its final, eternal form. It acts as a Physician
        before acting as a Surgeon. If the target scripture has a wounded soul (broken
        imports), this rite heals it *before* the Weaver attempts to perform its own
        surgical AST modifications, ensuring the Weaver always operates on a pure,
        unbroken reality.

        ### The Pantheon of Ascended Gnosis:

        1.  **The Gaze of Gnostic Causality:** It no longer forges its own Inquisitor.
            It makes a sacred plea to the Assembler's own `ProjectGraph`, receiving
            the one true, pre-existing `symbol_map` of the entire cosmos. The heresy
            of the redundant Gaze is annihilated.

        2.  **The Pure Delegation:** It is a pure Conductor. It forges the `PythonHealer`,
            bestows upon it the Gnostic context, and commands it to perform the Rites
            of Diagnosis and Healing. Its own soul is free of profane logic.

        3.  **The Unbreakable Ward of Paradox:** Its every action is shielded. If the
            healing rite fails for any reason, it does not shatter the Weaver's
            symphony. It proclaims a luminous warning and gracefully allows the
            Weaver to proceed upon the original, unhealed scripture.
        =================================================================================
        """
        self.logger.verbose(f"The Gnostic Physician's Gaze is upon '{target_file.name}'...")
        try:
            # --- MOVEMENT I: THE GAZE OF GNOSTIC CAUSALITY ---
            # We summon the symbol_map from the parent Assembler's ProjectGraph.
            # This is a hyper-performant, cached Gaze, not a full re-scan.
            symbol_map = self.parent_assembler.graph.get_symbol_map_for_language('python')
            if not symbol_map:
                self.logger.verbose("...Symbol map is a void. The Physician rests.")
                return None

            # --- MOVEMENT II: THE DIVINE DELEGATION ---
            # We forge the artisans required for the rite.
            resolver = PythonImportResolver(self.root, symbol_map, {})
            context = {'python_resolver': resolver}
            healer = PythonImportHealer(self.root, context)

            # The Rite of Diagnosis is performed.
            diagnoses = healer.diagnose(target_file, content)

            if not diagnoses:
                self.logger.verbose("...The scripture's soul is pure. No healing required.")
                return None

            self.logger.warn(
                f"The Physician perceived {len(diagnoses)} broken Gnostic connection(s) in '{target_file.name}'. Commencing the Rite of Healing."
            )

            # The Rite of Healing is performed.
            healed_content, was_changed = healer.heal(target_file, content, diagnoses)

            if was_changed and healed_content != content:
                self.logger.success(
                    f"'{target_file.name}' has been healed. The Weaver may now proceed with a pure soul."
                )
                return healed_content

        except Exception as e:
            # --- MOVEMENT III: THE UNBREAKABLE WARD OF PARADOX ---
            self.logger.warn(f"The healing rite was stayed by a paradox: {e}. The Weaver will proceed with caution.")

        return None

    def _handle_schemas(self, new_file_path: Path):
        """
        [ELEVATION 3: THE SCHEMA SCRIBE]
        Finds Pydantic models in the new file and auto-exports them from a
        central `schemas.py` or `models.py`.
        """
        self.logger.verbose(f"The Schema Scribe gazes upon '{new_file_path.name}' for new Gnosis...")
        try:
            content = new_file_path.read_text(encoding='utf-8')
            tree = ast.parse(content)

            pydantic_models = [
                node.name for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef)
                   and any(
                    isinstance(base, ast.Name) and base.id == 'BaseModel'
                    for base in node.bases
                )
            ]

            if not pydantic_models:
                self.logger.verbose("...No new Pydantic models perceived.")
                return

            # Find the central schema file
            schema_file_candidates = ["src/schemas.py", "src/models.py", "app/schemas.py", "app/models.py"]
            target_schema_file = next((self.root / p for p in schema_file_candidates if (self.root / p).exists()), None)

            if not target_schema_file:
                self.logger.verbose("...No central schema sanctum found. The Scribe rests.")
                return

            self.logger.info(f"Perceived new models: {pydantic_models}. Weaving into '{target_schema_file.name}'...")

            schema_content = target_schema_file.read_text(encoding='utf-8')

            # Forge the import statement
            src_root = self._find_src_root()
            try:
                module_path = ".".join(new_file_path.relative_to(src_root).with_suffix('').parts)
            except ValueError:
                module_path = ".".join(new_file_path.with_suffix('').parts)  # Fallback

            import_stmt = f"from {module_path} import {', '.join(pydantic_models)}"

            if import_stmt in schema_content:
                self.logger.verbose("...Schema connections are already pure.")
                return

            # We use a simple but effective append
            final_content = schema_content.strip() + f"\n\n# Auto-woven by Gnostic Assembler\n{import_stmt}\n"
            atomic_write(target_schema_file, final_content, self.logger, self.root)
            self.logger.success(f"Successfully wove new data contracts into '{target_schema_file.name}'.")

        except Exception as e:
            self.logger.warn(f"The Schema Scribe's rite was stayed by a paradox: {e}")

    def _handle_dependencies(self, new_file_content: str):
        """
        [ELEVATION 4: THE DEPENDENCY ORACLE]
        Scans for new third-party imports and proclaims a plea to the Architect.
        """
        self.logger.verbose("The Dependency Oracle awakens its Gaze...")
        try:
            import sys
            std_lib_modules = set(sys.stdlib_module_names) if sys.version_info >= (3, 10) else set()

            tree = ast.parse(new_file_content)
            perceived_imports = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        perceived_imports.add(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    perceived_imports.add(node.module.split('.')[0])

            # This is a humble Gaze; a future ascension would check pyproject.toml
            potential_new_deps = perceived_imports - std_lib_modules - {'fastapi', 'flask', 'typer', 'pydantic', 'src',
                                                                        'app'}

            if potential_new_deps:
                for dep in potential_new_deps:
                    self.logger.info(
                        f"[Oracle] New dependency '{dep}' perceived. Please conduct the rite: [bold green]pip install {dep}[/bold green] or [bold green]poetry add {dep}[/bold green]")

        except Exception as e:
            self.logger.warn(f"The Dependency Oracle's Gaze was clouded by a paradox: {e}")

    def _handle_test_prophecy(self, item: ScaffoldItem, framework: str):
        """
        [ELEVATION 5: THE TEST PROPHET]
        Forges a skeleton test file for the newly woven scripture.
        """
        self.logger.verbose("The Test Prophet awakens to adjudicate the new reality...")

        # Find the tests directory
        test_root = self.root / "tests"
        if not test_root.is_dir():
            self.logger.verbose("...No 'tests' sanctum found. The Prophet rests.")
            return

        # Mirror the source structure
        try:
            src_root = self._find_src_root()
            relative_path = item.path.relative_to(src_root)
            test_file_path = test_root / relative_path.parent / f"test_{item.path.name}"
        except ValueError:
            test_file_path = test_root / f"test_{item.path.name}"

        if test_file_path.exists():
            self.logger.verbose(f"A scripture of adjudication already exists at '{test_file_path.name}'.")
            return

        # Forge the Test Content
        content = ""
        if framework == "fastapi":
            # Gnostic boilerplate for testing a FastAPI router
            content = f"""
            
            from fastapi.testclient import TestClient
            from src.main import app  # A prophecy that this is the entrypoint
            
            client = TestClient(app)
            
            def test_read_main():
                \"\"\"
                A humble vow to ensure the new reality is not a void.
                \"\"\"
                # Prophecy: This assumes a root endpoint exists in the new router.
                # The Architect must refine this Gnosis.
                # url = "/{item.path.stem.replace('_', '-')}/" 
                # response = client.get(url)
                # assert response.status_code == 200
                assert True # A humble first vow
            """
        if content:
            self.logger.info(
                f"The Prophet has forged a new scripture of adjudication at [cyan]{test_file_path.relative_to(self.root)}[/cyan]")
            atomic_write(test_file_path, content, self.logger, self.root)


    def _detect_framework(self, tree: ast.AST) -> str:
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == "fastapi": return "fastapi"
                if node.module == "flask": return "flask"
                if node.module == "typer": return "typer"
                if node.module == "django": return "django"
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ["fastapi", "flask", "typer", "django"]:
                        return alias.name
        return "unknown"

    def _sniff_export_name(self, tree: ast.AST, framework: str) -> Optional[str]:
        targets = {"fastapi": ['router', 'api_router'], "flask": ['bp', 'blueprint'], "typer": ['app', 'cli']}.get(
            framework, [])
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in targets:
                        return target.id
        return targets[0] if targets else None
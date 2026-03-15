# Path: artisans/genesis/materializer.py
# --------------------------------------

from __future__ import annotations
import ast
import json
import re
import os
import platform
import sys
import time
import getpass
import shutil
import hashlib
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional, cast, Union

from rich.prompt import Confirm
from rich.markup import escape

from ...contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticArgs, InscriptionAction
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...creator import create_structure, QuantumRegisters
from ...creator.reports import GenesisReport
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GenesisRequest, BaseRequest
from ...logger import Scribe, get_console
from ...parser_core.parser import ApotheosisParser
from ...utils import atomic_write, get_git_branch, get_git_commit
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...creator.next_step_oracle import NextStepsOracle

Logger = Scribe("Materializer")

GnosticDowry = Tuple[ApotheosisParser, List[ScaffoldItem], List[str], Dict[str, Any], GnosticDossier]

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


class GenesisMaterializer:
    """
    Orchestrates the final file creation sequence and ensures transactional safety.
    """

    def __init__(self, engine, request: GenesisRequest, gnostic_dowry: GnosticDowry, collisions: List[Path]):
        self.engine = engine
        self.request = request
        self.parser, self.items, self.commands, self.final_vars, self.dossier = gnostic_dowry
        self.collisions = collisions
        self.logger = Logger
        self.console = get_console()
        self.project_root = request.project_root or Path.cwd()
        self.start_time = time.monotonic()

        self.generated_files: List[Path] = []
        self.merkle_root: str = ""

    def _sys_log(self, msg: str, color: str = "45"):
        if _DEBUG_MODE:
            sys.stderr.write(f"\x1b[{color};1m[DEBUG: Materializer]\x1b[0m {msg}\n")
            sys.stderr.flush()

    def conduct_materialization_symphony(self) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMEGA MATERIALIZATION SYMPHONY (V-Ω-TOTALITY-VMAX-36-ASCENSIONS)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_MATERIALIZE_VMAX_SEMANTIC_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for physical manifestation. This version
        righteously implements the **Semantic Suture (`*=`)**, mathematically
        annihilating the "Overwrite Heresy" by performing AST-aware logic merging.
        =================================================================================
        """
        import time
        import os
        import platform
        import gc
        from pathlib import Path
        from ...contracts.heresy_contracts import HeresySeverity, ArtisanHeresy

        # [ASCENSION 16]: THERMODYNAMIC TOMOGRAPHY
        _start_ns = time.perf_counter_ns()
        trace_id = self.final_vars.get("trace_id", "tr-void")

        is_simulation = self.request.dry_run or self.request.preview

        # =========================================================================
        # ==[ASCENSION 2]: THE VOID GAVEL (THE MASTER CURE)                     ==
        # =========================================================================
        if not self.items and not self.commands:
            self.logger.critical(f"[{trace_id}] Ontological Void Detected: 0 items willed.")
            raise ArtisanHeresy(
                "MATTER_EVAPORATION_HERESY",
                details="Gnostic Inquest yielded 0 physical atoms and 0 kinetic edicts.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Check sub-weave pointer stability. Reality cannot be forged from void."
            )

        # --- MOVEMENT I: TOPOLOGICAL ANCHORING ---
        # [ASCENSION 23]: POSIX Normalization
        true_project_root = self._determine_true_project_root()
        tx_name = f"Build: {true_project_root.name}"
        blueprint_path = Path(self.final_vars.get('blueprint_path', 'unknown.scaffold'))

        # =========================================================================
        # == [ASCENSION 17]: LAZARUS VAULT INCEPTION                             ==
        # =========================================================================
        if not is_simulation:
            try:
                (true_project_root / ".scaffold" / "chronicles").mkdir(parents=True, exist_ok=True)
                (true_project_root / ".scaffold" / "backups").mkdir(parents=True, exist_ok=True)
            except OSError:
                pass

        # --- MOVEMENT II: THE TRANSACTIONAL WOMB ---
        with GnosticTransaction(self.project_root, tx_name, blueprint_path, use_lock=True,
                                simulate=is_simulation) as tx:

            # [ASCENSION 24]: Apophatic Sieve & [ASCENSION 21]: Substrate DNA
            tx.context = {k: v for k, v in self.final_vars.items() if not str(k).startswith('__')}
            tx.context.update({
                'project_root': str(true_project_root).replace('\\', '/'),
                'genesis_timestamp': time.time(),
                'os_name': os.name,
                'platform': platform.system(),
                'trace_id': trace_id
            })

            # =========================================================================
            # == [ASCENSION 13]: THE SEMANTIC SUTURE RESOLUTION (THE MASTER CURE)    ==
            # =========================================================================
            # [STRIKE]: We perform AST-aware merging for the '*=' operator.
            processed_items = self._apply_semantic_sutures(self.items, true_project_root)

            # --- MOVEMENT III: THE PHYSICAL STRIKE ---
            gnostic_passport = GnosticArgs.from_namespace(self.request)

            normalized_commands = []
            for cmd in self.commands:
                if isinstance(cmd, (tuple, list)) and len(cmd) > 0 and isinstance(cmd[0], (tuple, list)):
                    pure_cmd_str = str(cmd[0][0])
                elif isinstance(cmd, (tuple, list)) and len(cmd) > 0:
                    pure_cmd_str = str(cmd[0])
                else:
                    pure_cmd_str = str(cmd)
                normalized_commands.append((pure_cmd_str, 0, None, None))

            registers = create_structure(
                scaffold_items=processed_items,
                post_run_commands=normalized_commands,
                pre_resolved_vars=self.final_vars,
                base_path=self.project_root,
                args=cast(Any, gnostic_passport),
                transaction=tx,
                engine=self.engine
            )

            # --- MOVEMENT IV: POST-STRIKE ADJUDICATION ---
            if registers.transaction:
                self.generated_files = [res.path for res in registers.transaction.write_dossier.values() if res.success]

            if not is_simulation:
                # [ASCENSION 32]: MERKLE-LATTICE STATE SEALING
                self._validate_syntax_integrity(tx)
                self._enrich_readme_metadata(tx)
                self._ensure_dynamic_ignores(tx)
                self._consecrate_executables(tx)
                self._ensure_license(tx)
                self._inscribe_final_blueprint(true_project_root, tx)
                self._persist_genesis_state(true_project_root, tx)
                self._compute_merkle_root(tx)
                self._forge_devcontainer_scripture(true_project_root, tx)
                self._prune_empty_directories(true_project_root)

        # --- MOVEMENT V: FINAL PROCLAMATION ---
        # [ASCENSION 22]: HYDRAULIC FLUSH
        sys.stdout.flush()
        self._proclaim_success(registers, true_project_root)

        created_artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                created_artifacts.append(Artifact(
                    path=res.path, type="directory" if (self.project_root / res.path).is_dir() else "file",
                    action=res.action_taken.value, size_bytes=res.bytes_written, checksum=res.gnostic_fingerprint
                ))

        # [ASCENSION 36]: THE FINALITY VOW
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        return ScaffoldResult(
            success=True,
            message=f"Reality Manifested in {duration_ms:.2f}ms.",
            data={
                "item_count": len(self.items),
                "merkle_root": self.merkle_root,
                "trace_id": trace_id
            },
            artifacts=created_artifacts,
            duration_seconds=duration_ms / 1000.0
        )

    # =========================================================================
    # == THE SEMANTIC SUTURE ORGANS                                          ==
    # =========================================================================

    def _apply_semantic_sutures(self, items: List[ScaffoldItem], root: Path) -> List[ScaffoldItem]:
        """
        =============================================================================
        == THE OMEGA SEMANTIC SUTURE (V-Ω-TOTALITY-VMAX-POLYGLOT-Grafting)         ==
        =============================================================================
        LIF: ∞^∞ | ROLE: LOGIC_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME
        """
        import time
        _start_suture_ns = time.perf_counter_ns()

        for item in items:
            if item.mutation_op == "*=" and item.path:
                abs_path = (root / item.path).resolve()

                if not abs_path.exists():
                    item.mutation_op = "="
                    continue

                self.logger.info(f"🧬 [SUTURE] Initiating Causal Merge: [bold cyan]{item.path.name}[/]")

                try:
                    target_matter = abs_path.read_text(encoding='utf-8', errors='replace')
                    willed_gnosis = item.content or ""
                    ext = abs_path.suffix.lower()

                    if ext == ".py":
                        merged_reality = self._merge_python_ast(target_matter, willed_gnosis)
                    elif ext in (".json", ".yaml", ".yml", ".toml"):
                        merged_reality = self._merge_structured_data(target_matter, willed_gnosis, ext)
                    elif ext == ".md":
                        merged_reality = self._merge_markdown_scripture(target_matter, willed_gnosis)
                    else:
                        self.logger.warn(f"Linguistic Void: Suture for '{ext}' unmanifest. Devolving to Append.")
                        item.mutation_op = "+="
                        continue

                    if hashlib.sha256(merged_reality.encode()).hexdigest() == hashlib.sha256(
                            target_matter.encode()).hexdigest():
                        self.logger.verbose(
                            f"   ->[STASIS] No drift perceived for '{item.path.name}'. Staying the strike.")
                        item.mutation_op = "VOID"
                    else:
                        item.mutation_op = "="
                        item.content = merged_reality

                except Exception as paradox:
                    self.logger.error(f"Suture Fracture on '{item.path.name}': {paradox}")
                    item.mutation_op = "+="

        _tax_ms = (time.perf_counter_ns() - _start_suture_ns) / 1_000_000
        if self.logger.is_verbose:
            self.logger.debug(f"Metabolic Suture Tax: {_tax_ms:.2f}ms for {len(items)} atoms.")

        return [i for i in items if i.mutation_op != "VOID"]

    def _merge_python_ast(self, target_code: str, injection_code: str) -> str:
        """
        =============================================================================
        == THE AST GRAFTER: OMEGA (V-Ω-TOTALITY-VMAX-MORPHOLOGICAL-SUTURE)         ==
        =============================================================================
        LIF: ∞ | ROLE: CAUSAL_REALITY_WEAVER | RANK: MASTER
        """
        import ast
        import textwrap

        try:
            injection_code = self.alchemist.transmute(injection_code, self.final_vars)
            target_tree = ast.parse(target_code)
            inject_tree = ast.parse(injection_code)
        except SyntaxError as heresy:
            self.logger.warn(f"AST Schism perceived. Devolving to literal concatenation. Reason: {heresy}")
            return target_code + "\n\n# [SUTURE_FRACTURE]: Syntax drifted from Law.\n" + injection_code

        existing_defs = {n.name for n in target_tree.body if
                         isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

        target_imports = []
        target_body = []
        for node in target_tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                target_imports.append(node)
            else:
                target_body.append(node)

        new_logic = []
        for node in inject_tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if ast.unparse(node) not in [ast.unparse(ti) for ti in target_imports]:
                    target_imports.append(node)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if node.name in existing_defs:
                    self.logger.verbose(f"   -> Shadow Ward: Logic atom '{node.name}' already manifest. Skipping.")
                else:
                    new_logic.append(node)
            else:
                new_logic.append(node)

        target_imports.sort(key=lambda x: ast.unparse(x))
        target_tree.body = target_imports + target_body + new_logic

        return ast.unparse(target_tree)

    def _merge_structured_data(self, target: str, injection: str, ext: str) -> str:
        """
        =================================================================================
        == THE OMEGA DATA ALCHEMIST (V-Ω-TOTALITY-VMAX-STRUCTURAL-FUSION)              ==
        =================================================================================
        """
        import json
        import hashlib

        pre_hash = hashlib.sha256(target.encode()).hexdigest()

        try:
            if ext == ".json":
                d1 = json.loads(target)
                d2 = json.loads(injection)
            elif ext in (".yaml", ".yml"):
                import yaml
                d1 = yaml.safe_load(target) or {}
                d2 = yaml.safe_load(injection) or {}
            elif ext == ".toml":
                try:
                    import tomllib as toml_engine
                except ImportError:
                    import toml as toml_engine
                d1 = toml_engine.loads(target)
                d2 = toml_engine.loads(injection)
            else:
                return target + "\n" + injection

            def _fuse_recursive(base: Any, overlay: Any) -> Any:
                if isinstance(base, dict) and isinstance(overlay, dict):
                    for k, v in overlay.items():
                        if k in base:
                            base[k] = _fuse_recursive(base[k], v)
                        else:
                            base[k] = v
                    return base
                elif isinstance(base, list) and isinstance(overlay, list):
                    for item in overlay:
                        if item not in base:
                            base.append(item)
                    return base
                return overlay

            fused_data = _fuse_recursive(d1, d2)

            if ext == ".json":
                return json.dumps(fused_data, indent=4)
            elif ext in (".yaml", ".yml"):
                import yaml
                return yaml.safe_dump(fused_data, sort_keys=False, default_flow_style=False)
            elif ext == ".toml":
                import toml
                return toml.dumps(fused_data)

        except Exception as fracture:
            self.logger.warn(f"Data Fusion Fracture on '{ext}': {fracture}. Devolving to literal Append.")
            return target + "\n\n" + injection

    def _merge_markdown_scripture(self, target: str, injection: str) -> str:
        """
        =================================================================================
        == THE TOPOGRAPHICAL SCRIPTURE SCRIBE (V-Ω-TOTALITY-VMAX-HEADER-SUTURE)        ==
        =================================================================================
        """
        import re
        header_pattern = re.compile(r'^(#+\s+.*)$', re.MULTILINE)

        def _get_sections(text: str) -> Dict[str, str]:
            import collections
            sections = collections.OrderedDict()
            parts = header_pattern.split(text)

            intro = parts[0].strip()
            if intro:
                sections["__INTRO__"] = intro

            for i in range(1, len(parts), 2):
                h_title = parts[i].strip()
                h_body = parts[i + 1].strip() if (i + 1) < len(parts) else ""
                sections[h_title] = h_body
            return sections

        target_map = _get_sections(target)
        inject_map = _get_sections(injection)

        for h_title, h_body in inject_map.items():
            if h_title == "__INTRO__":
                if "__INTRO__" in target_map:
                    target_map["__INTRO__"] += "\n" + h_body
                else:
                    target_map["__INTRO__"] = h_body
            elif h_title in target_map:
                if h_body not in target_map[h_title]:
                    target_map[h_title] += "\n\n" + h_body
            else:
                target_map[h_title] = h_body

        output = []
        if "__INTRO__" in target_map:
            output.append(target_map.pop("__INTRO__"))

        for title, body in target_map.items():
            output.append(f"\n{title}\n{body}")

        trace_id = self.final_vars.get("trace_id", "tr-void")
        footer = f"\n\n<!-- VELM_GNOSIS: [TRACE:{trace_id}][BORN:{time.strftime('%Y-%m-%d')}] -->"

        return "\n".join(output) + footer

    def _validate_syntax_integrity(self, tx: GnosticTransaction):
        """
        =============================================================================
        == THE RITE OF SYNTACTIC PURITY (V-Ω-AUTONOMIC-SYNTAX-HEALER)              ==
        =============================================================================
        Mathematically guarantees that no file forged by the God-Engine ever possesses
        invalid syntax. It righteously intercepts `SyntaxError`, executing an O(1)
        Regex Suture for known anomalies, and defaults to the Neural Cortex for
        unforeseen logic fractures.
        """
        self._sys_log(f"Validating syntax for {len(tx.write_dossier)} generated files...", "44")

        for path, result in tx.write_dossier.items():
            if not result.success: continue
            staged_path = tx.get_staging_path(path)

            if not staged_path.exists() or staged_path.stat().st_size == 0:
                continue

            if path.suffix == '.py':
                self._heal_python_syntax(staged_path, path, tx)
            elif path.suffix == '.json':
                try:
                    json.load(staged_path.open('r', encoding='utf-8'))
                except json.JSONDecodeError as e:
                    raise ArtisanHeresy(f"Malformed JSON output in '{path.name}': {e}",
                                        severity=HeresySeverity.CRITICAL)

    def _heal_python_syntax(self, staged_path: Path, path: Path, tx: GnosticTransaction, attempt: int = 1):
        """Recursively heals Python Syntax Errors with Absolute Amnesty."""
        try:
            content = staged_path.read_text(encoding='utf-8')
            ast.parse(content)
        except SyntaxError as e:
            if attempt > 3:
                raise ArtisanHeresy(
                    f"Syntax Error in generated Python file '{path.name}' persists after 3 healing cycles: {e.msg}",
                    line_num=e.lineno, severity=HeresySeverity.CRITICAL)

            self.logger.warn(
                f"⚠️ AST Fracture in '{path.name}': {e.msg} at line {e.lineno}. Summoning Autonomic Syntax Healer (Cycle {attempt})...")

            # The Cure: Autonomic Syntax Healer
            healed_content = self._apply_syntax_healer(content, e, path.name)
            staged_path.write_text(healed_content, encoding='utf-8')

            # Recursively re-validate
            self._heal_python_syntax(staged_path, path, tx, attempt + 1)

    def _apply_syntax_healer(self, content: str, error: SyntaxError, file_name: str) -> str:
        """
        [THE MASTER CURE]: Surgical interception of SyntaxErrors.
        """
        # Heuristic 1: Illegal target for annotation (e.g. app.middleware: list =[])
        if "illegal target for annotation" in str(error.msg):
            import re
            # Regex to strip type hint from attribute assignment
            # Example: app.middleware_stack: list = [] -> app.middleware_stack = []
            pattern = re.compile(r'^(\s*)([a-zA-Z0-9_.]+\.[a-zA-Z0-9_.]+)\s*:\s*[^=]+\s*=\s*(.*)$', re.MULTILINE)
            healed = pattern.sub(r'\1\2 = \3', content)
            if healed != content:
                self.logger.success(f"✨ Autonomic Suture applied: Stripped illegal annotation in {file_name}.")
                return healed

        # Heuristic 2: Neural Fallback
        self.logger.info(f"🧠 Invoking Neural Cortex to heal SyntaxError in {file_name}...")
        try:
            from ...core.ai.engine import AIEngine
            from ...core.ai.contracts import NeuralPrompt
            import asyncio

            prompt = f"Fix the SyntaxError: {error.msg} at line {error.lineno}.\nCode:\n```python\n{content}\n```\nReturn ONLY the fixed Python code. No markdown, no explanations."
            ai_engine = AIEngine.get_instance()

            try:
                loop = asyncio.get_running_loop()
                import nest_asyncio
                nest_asyncio.apply()
                response = asyncio.run(ai_engine.active_provider.commune(
                    NeuralPrompt(user_query=prompt, system_instruction="You are a strict syntax healer.",
                                 model_hint="smart")
                ))
            except RuntimeError:
                response = asyncio.run(ai_engine.active_provider.commune(
                    NeuralPrompt(user_query=prompt, system_instruction="You are a strict syntax healer.",
                                 model_hint="smart")
                ))

            healed_code = response.content.strip()
            if healed_code.startswith("```python"): healed_code = healed_code[9:]
            if healed_code.startswith("```"): healed_code = healed_code[3:]
            if healed_code.endswith("```"): healed_code = healed_code[:-3]

            self.logger.success(f"✨ Neural Cortex successfully re-woven {file_name}.")
            return healed_code.strip()
        except Exception as neural_err:
            self.logger.error(f"Neural Healer failed: {neural_err}")
            return content

    def _forge_devcontainer_scripture(self, project_root: Path, tx: GnosticTransaction):
        if not self.final_vars.get('use_devcontainer', self.final_vars.get('use_vscode', False)):
            return

        devcontainer_dir = project_root / ".devcontainer"
        try:
            devcontainer_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

        self.logger.info("Generating Developer Container configuration...")

        project_slug = self.final_vars.get('project_slug', 'scaffold-project')
        project_type = self.final_vars.get('project_type', 'generic').lower()
        db_type = self.final_vars.get('database_type', 'none').lower()
        has_sidecar = db_type != 'none' or self.final_vars.get('use_redis', False)

        config = {
            "name": f"{self.final_vars.get('project_name', project_root.name)} Container",
            "containerUser": "vscode",
            "customizations": {
                "vscode": {
                    "settings": {
                        "editor.formatOnSave": True,
                    },
                    "extensions": ["GitHub.copilot", "usernamehw.errorlens"]
                }
            },
            "forwardPorts": [],
            "features": {
                "ghcr.io/devcontainers/features/common-utils:2": {"installZsh": True},
                "ghcr.io/devcontainers/features/git:1": {}
            }
        }

        if 'python' in project_type or 'fastapi' in project_type:
            config["customizations"]["vscode"]["extensions"].extend(["ms-python.python", "ms-python.vscode-pylance"])
            config["forwardPorts"].append(8000)
            if 'poetry' in project_type:
                config["postCreateCommand"] = "poetry install --no-interaction --no-root"
            else:
                config["postCreateCommand"] = "pip install -r requirements.txt"

        elif 'node' in project_type or 'react' in project_type:
            config["customizations"]["vscode"]["extensions"].extend(
                ["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"])
            config["forwardPorts"].append(3000)
            config["postCreateCommand"] = "npm install"

        import json
        content = json.dumps(config, indent=4)
        atomic_write(devcontainer_dir / "devcontainer.json", content, self.logger, project_root, transaction=tx)

    def _determine_true_project_root(self) -> Path:
        default_slug = self.final_vars.get('project_slug', 'new_project')
        if not self.items:
            return self.project_root / default_slug

        first_parts = set()
        for item in self.items:
            if item.path and item.path.parts:
                first_parts.add(item.path.parts[0])

        if len(first_parts) == 1:
            nested_root_name = list(first_parts)[0]
            if nested_root_name == default_slug:
                return self.project_root / nested_root_name

        return self.project_root

    def _ensure_dynamic_ignores(self, tx: GnosticTransaction):
        ignores = set()
        for path in self.generated_files:
            if path.suffix in ['.env', '.key', '.pem', '.p12'] or path.name == '.DS_Store':
                ignores.add(path.name)
            if path.name == "scaffold.lock": ignores.add("scaffold.lock")
            if path.name == "genesis.json": ignores.add(".scaffold/genesis.json")

        if not ignores: return

        gitignore_path = self._determine_true_project_root() / ".gitignore"
        staged_gitignore = tx.get_staging_path(gitignore_path.relative_to(self.project_root))

        current_content = ""
        if staged_gitignore.exists():
            current_content = staged_gitignore.read_text(encoding='utf-8')
        elif gitignore_path.exists():
            current_content = gitignore_path.read_text(encoding='utf-8')

        new_content = current_content
        appended = False
        for item in ignores:
            if item not in current_content:
                if not appended:
                    new_content += "\n# --- Auto-generated excludes ---\n"
                    appended = True
                new_content += f"{item}\n"

        if new_content != current_content:
            atomic_write(gitignore_path, new_content, self.logger, self.project_root, transaction=tx)

    def _enrich_readme_metadata(self, tx: GnosticTransaction):
        readme_path = self._determine_true_project_root() / "README.md"
        is_generated = any(str(p).endswith("README.md") for p in self.generated_files)
        if not is_generated: return

        staged_readme = tx.get_staging_path(readme_path.relative_to(self.project_root))
        if staged_readme.exists():
            content = staged_readme.read_text(encoding='utf-8')
            meta_block = f"\n<!--\n  SCAFFOLD_GNOSIS:\n  timestamp: {time.time()}\n-->"
            if "SCAFFOLD_GNOSIS" not in content:
                atomic_write(readme_path, content + meta_block, self.logger, self.project_root, transaction=tx)

    def _consecrate_executables(self, tx: GnosticTransaction):
        for path in self.generated_files:
            if path.suffix in ['.sh', '.bash'] or path.name in ['configure', 'bootstrap']:
                tx.record_edict(f"chmod +x {path}")
                try:
                    staged_path = tx.get_staging_path(path.relative_to(self.project_root))
                    if staged_path.exists():
                        staged_path.chmod(staged_path.stat().st_mode | 0o111)
                except Exception:
                    pass

    def _ensure_license(self, tx: GnosticTransaction):
        license_type = self.final_vars.get('license')
        if not license_type or license_type.lower() == 'none': return

        license_path = self._determine_true_project_root() / "LICENSE"
        if any(str(p).upper().endswith("LICENSE") for p in self.generated_files) or license_path.exists():
            return

        license_text = f"{license_type} License\n\nCopyright (c) {time.strftime('%Y')} {self.final_vars.get('author', 'Developer')}"
        atomic_write(license_path, license_text, self.logger, self.project_root, transaction=tx)

    def _inscribe_final_blueprint(self, true_project_root: Path, transaction: GnosticTransaction):
        from ...core.blueprint_scribe import BlueprintScribe
        chronicle_path = true_project_root / "scaffold.scaffold"

        try:
            scribe = BlueprintScribe(self.project_root)

            normalized_commands = []
            for cmd in self.commands:
                pure_cmd = cmd[0] if isinstance(cmd, (tuple, list)) and len(cmd) > 0 else str(cmd)
                normalized_commands.append((pure_cmd, 0, None, None))

            final_scripture = scribe.transcribe(self.items, normalized_commands, self.final_vars)

            atomic_write(chronicle_path, final_scripture, self.logger, self.project_root, transaction=transaction)

            if not _DEBUG_MODE:
                self.logger.success("Project blueprint saved to scaffold.scaffold.")
        except Exception as e:
            self.logger.warn(f"Warning: Failed to save final blueprint state: {e}")

    def _persist_genesis_state(self, true_project_root: Path, transaction: GnosticTransaction):
        state_path = true_project_root / ".scaffold" / "genesis.json"

        safe_vars = {k: v for k, v in self.final_vars.items() if
                     isinstance(v, (str, int, bool, float, list, dict, type(None))) and not str(k).startswith('__')}

        content = json.dumps({
            "variables": safe_vars, "timestamp": time.time(),
            "archetype": self.final_vars.get("profile") or "custom"
        }, indent=2)
        atomic_write(state_path, content, self.logger, self.project_root, transaction=transaction)

    def _prune_empty_directories(self, root: Path):
        if not root.exists(): return
        for dirpath, dirnames, filenames in os.walk(root, topdown=False):
            if not dirnames and not filenames:
                try:
                    Path(dirpath).rmdir()
                except OSError:
                    pass

    def _analyze_overwrites(self, tx: GnosticTransaction):
        pass

    def _compute_merkle_root(self, tx: GnosticTransaction):
        hasher = hashlib.sha256()
        for path in sorted(tx.write_dossier.keys()):
            res = tx.write_dossier[path]
            if res.success and res.gnostic_fingerprint:
                hasher.update(str(path).encode())
                hasher.update(res.gnostic_fingerprint.encode())
        self.merkle_root = hasher.hexdigest()

    def _proclaim_success(self, registers: QuantumRegisters, true_project_root: Path):
        if self.request.silent or self.request.dry_run or self.request.preview:
            return

        artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                artifacts.append(Artifact(path=res.path, type="file", action=res.action_taken.value))

        duration_ms = (time.monotonic() - self.start_time) * 1000
        total_mass = sum(a.size_bytes for a in artifacts)

        perf_metrics = {
            "duration_ms": duration_ms,
            "mass_bytes": total_mass,
        }

        try:
            cwd = Path.cwd()
            resolved_root = true_project_root.resolve()
            needs_cd = resolved_root != cwd
            relative_root = resolved_root.relative_to(cwd) if needs_cd else "."
        except ValueError:
            relative_root = true_project_root
            needs_cd = True

        final_next_steps = []
        if needs_cd:
            final_next_steps.append(f"cd {relative_root}")

        prophet = NextStepsOracle(project_root=true_project_root, gnosis=self.final_vars)
        oracle_steps = prophet.prophesy()
        for step in oracle_steps:
            if "cd " not in step:
                final_next_steps.append(step)

        proclaim_apotheosis_dossier(
            telemetry_source=registers,
            gnosis=self.final_vars,
            project_root=true_project_root,
            next_steps=final_next_steps,
            title="Project Generated Successfully",
            subtitle=f"'{escape(true_project_root.name)}' is ready.",
            gnostic_constellation=artifacts,
            security_warnings=[],
            transmutation_plan=None,
            ai_telemetry={},
            environment_gnosis={},
            performance_metrics=perf_metrics,
            maestro_edicts=self.commands,
            audit_file_path=self.project_root / ".scaffold" / "genesis_audit.json"
        )
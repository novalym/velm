# Path: artisans/weave/weaver.py
# ------------------------------


import json
import os
import re
import sys
import time
import subprocess
import threading
import hashlib
import gc
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple, Final
from collections import OrderedDict

from rich.prompt import Confirm

# --- THE DIVINE UPLINKS ---
from ...core.alchemist import get_alchemist
from ...core.kernel.transaction import GnosticTransaction
from ...core.kernel.archivist import GnosticArchivist
from ...contracts.data_contracts import ScaffoldItem, InscriptionAction, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import WeaveRequest
from ...logger import Scribe
from ...parser_core.parser import ApotheosisParser
from ...utils import (
    atomic_write,
    resolve_gnostic_content_v2,
    perform_alchemical_resolution,
    is_binary
)
from ...communion import conduct_sacred_dialogue, GnosticPlea, GnosticPleaType
from ...artisans.patch.mutators import GnosticMutator

INTERNAL_SIGS: Final[Tuple[str, ...]] = (
    "VARIABLE:", "BLOCK_HEADER:", "EDICT:", "SYSTEM_MSG:",
    "TRAIT_DEF:", "CONTRACT:", "SYSTEM_COMMENT:", "LOGIC:"
)

PHANTOM_MARKERS: Final[List[re.Pattern]] = [
    re.compile(r'^\s*#\s*@scaffold:wire.*$', re.MULTILINE),
    re.compile(r'^\s*#\s*@scaffold:lifecycle.*$', re.MULTILINE),
    re.compile(r'^\s*#\s*@scaffold:dependency.*$', re.MULTILINE),
    re.compile(r'^\s*#\s*@scaffold:middleware.*$', re.MULTILINE),
    re.compile(r'^\s*#\s*@scaffold:router.*$', re.MULTILINE),
    re.compile(r'^\s*//\s*@scaffold:wire.*$', re.MULTILINE),
    re.compile(r'^\s*//\s*@scaffold:lifecycle.*$', re.MULTILINE),
]

Logger = Scribe("GnosticWeaver")


class GnosticWeaver:
    """
    =================================================================================
    == THE HIGH PRIEST OF COALESCENCE (V-Ω-TOTALITY-V32-ASCENSIONS-FINALIS)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: REALITY_MERGER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: )(#!()!@#()()!

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **The Chronometric Suture (THE MASTER CURE):** Righteously aligns `_start_ns`
        variable assignment, completely annihilating the Unresolved Reference Heresy.
    2.  **Bicameral Reality Awareness (THE MASTER CURE):** Introduces strict separation
        between Prime Weaves (I/O active) and Nested Weaves (Memory only). This
        mathematically prevents sub-shards from striking the Iron prematurely.
    3.  **The Quaternity Hoist (THE MASTER CURE):** Surgically extracts `post_run_commands`
        from nested AST resolutions and hoists them back to the Prime Timeline,
        guaranteeing `npm install` and other edicts execute flawlessly.
    4.  **The Pointer Preservation Suture:** Uses `.update(final_vars)` instead of
        overwriting `parser.variables` to preserve the physical memory addresses of
        system buffers.
    5.  **Runtime Variable Amnesty (THE FIX):** By disabling `strict_mode` during file
        content transmutation, it mathematically guarantees that `{{ e }}` in catch
        blocks survives compilation and reaches the runtime interpreter intact.
    [... Continuum maintained through 27 other faculties ...]
    =================================================================================
    """

    def __init__(self, engine: Any, project_root: Path):
        self.engine = engine
        self.project_root = project_root
        self.alchemist = get_alchemist()
        self.Logger = Logger
        self._weave_lock = threading.RLock()

        if hasattr(self.alchemist, 'engine') and self.alchemist.engine is None:
            self.alchemist.engine = self.engine

        from ..template_engine import TemplateEngine
        self.template_engine = TemplateEngine(project_root=self.project_root, silent=True)

    def conduct(self, archetype_path: Path, request: WeaveRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMEGA WEAVE CONDUCT (V-Ω-TOTALITY-VMAX-DOUBLE-RESOLVE-ANNIHILATOR)      ==
        =================================================================================
        """
        import time
        import os
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ...contracts.data_contracts import InscriptionAction
        from ...parser_core.parser import ApotheosisParser

        # [ASCENSION 1]: THE CHRONOMETRIC SUTURE (THE BUG FIX)
        _start_ns = time.perf_counter_ns()

        is_simulation = request.dry_run or request.preview
        trace_id = getattr(request, 'trace_id', 'tr-weave-void')

        current_depth = request.variables.get("__weave_depth__", 0)
        if current_depth > 20:
            raise ArtisanHeresy("Ouroboros Paradox: Maximum recursion depth exceeded.",
                                severity=HeresySeverity.CRITICAL)
        request.variables["__weave_depth__"] = current_depth + 1

        self._multicast_pulse("WEAVE_START", f"Weaving {archetype_path.name}", "#a855f7", trace_id)

        if not request.force and not is_simulation:
            self._check_git_cleanliness()

        target_dir = request.target_directory or "."
        meta = getattr(request, 'metadata', {}) or {}

        if meta.get("_is_nested_weave"):
            curr_file = request.variables.get("__current_file__", "")
            curr_dir = request.variables.get("__current_dir__", "")
            if target_dir == curr_dir and curr_file and curr_file != "VOID":
                target_dir = curr_file
                self.Logger.verbose(f"Spatial Reality Suture: Re-anchored target to '{target_dir}'")

        target_dir_posix = str(target_dir).replace('\\', '/').strip(' ./')
        request.variables['target_dir'] = target_dir_posix

        parser = ApotheosisParser(grammar_key='scaffold', engine=self.engine)

        if not request.variables.get('trace_id'):
            request.variables['trace_id'] = trace_id

        try:
            _, raw_items, commands_tuple, _, blueprint_vars, dossier = parser.parse_string(
                archetype_path.read_text(encoding='utf-8', errors='ignore'),
                file_path_context=archetype_path,
                pre_resolved_vars=request.variables,
                depth=current_depth + 1
            )
        except Exception as e:
            raise ArtisanHeresy(f"The Archetype's soul is void or profane: {e}", child_heresy=e)

        known_keys = set(request.variables.keys()) | set(blueprint_vars.keys())
        missing_vars = dossier.required - known_keys
        unified_gnosis = {**blueprint_vars, **request.variables}

        if missing_vars and not request.non_interactive:
            from ...communion import conduct_sacred_dialogue, GnosticPlea, GnosticPleaType
            pleas = [GnosticPlea(key=var, plea_type=GnosticPleaType.TEXT, prompt_text=f"Enter value for '{var}'") for
                     var in sorted(list(missing_vars))]
            success, user_gnosis = conduct_sacred_dialogue(pleas=pleas, title=f"Weaving {archetype_path.stem}")
            if not success: raise ArtisanHeresy("Rite stayed.", severity=HeresySeverity.WARNING)
            unified_gnosis.update(user_gnosis)

        final_vars = perform_alchemical_resolution(dossier, unified_gnosis, blueprint_vars)

        parser.variables.update(final_vars)
        parser.blueprint_vars.update(final_vars)

        try:
            if parser.manifested_matter:
                self.Logger.verbose(
                    f"   ->[SINGULARITY] Preserving Bloom: {len(parser.manifested_matter)} atoms wove in first pass.")
                resolved_items = parser.manifested_matter
            else:
                resolved_items = parser.resolve_reality()

            # [ASCENSION 3]: THE QUATERNITY HOIST (PART 1)
            commands_tuple = parser.post_run_commands
            commands = [cmd[0] for cmd in commands_tuple if cmd]
        except Exception as ast_heresy:
            raise ArtisanHeresy(f"AST Weave Failure: {ast_heresy}", child_heresy=ast_heresy)

        items = [i for i in resolved_items if i.path and not any(str(i.path).startswith(s) for s in INTERNAL_SIGS)]

        with self._weave_lock:
            rebased_items = self._rebase_and_predict_collisions(items, final_vars, target_dir_posix)

        # =========================================================================
        # == MOVEMENT VI: [THE MASTER CURE] - BICAMERAL REALITY AWARENESS        ==
        # =========================================================================
        is_nested_weave = meta.get("_is_nested_weave", False)

        # --- PATH A: THE NESTED REALITY (MEMORY ONLY) ---
        if is_nested_weave:
            resolved_nested_items = []
            if hasattr(self.alchemist, 'env') and hasattr(self.alchemist.env, 'cache'):
                self.alchemist.env.cache.clear()

            for final_path, item in rebased_items:
                time.sleep(0)
                nested_item = item.model_copy(deep=True)
                nested_item.path = final_path

                if not nested_item.metadata: nested_item.metadata = {}
                nested_item.metadata["_blueprint_provenance"] = str(archetype_path)

                if nested_item.content is None and not nested_item.is_dir and not nested_item.is_binary:
                    template_item = self.template_engine.perform_gaze(Path(final_path.name), final_vars)
                    if template_item and template_item.content:
                        raw_base = template_item.content
                    else:
                        base_soul_vessel = resolve_gnostic_content_v2(
                            nested_item, self.alchemist, self.template_engine, final_vars,
                            sanctum=archetype_path.parent, source_override_map={}
                        )
                        raw_base = base_soul_vessel.untransmuted_content or ""

                    pure_base = self._extract_scaffold_soul(raw_base, final_path.name, final_vars)

                    # [ASCENSION 5]: Runtime Amnesty (Strict = False)
                    _strict = self.alchemist.sgf.strict_mode
                    self.alchemist.sgf.strict_mode = False
                    try:
                        nested_item.content = self.alchemist.transmute(pure_base, final_vars)
                    finally:
                        self.alchemist.sgf.strict_mode = _strict

                elif nested_item.content is not None and not nested_item.is_dir and not nested_item.is_binary:
                    # [ASCENSION 5]: Runtime Amnesty (Strict = False)
                    _strict = self.alchemist.sgf.strict_mode
                    self.alchemist.sgf.strict_mode = False
                    try:
                        nested_item.content = self.alchemist.transmute(nested_item.content, final_vars)
                    finally:
                        self.alchemist.sgf.strict_mode = _strict

                if nested_item.content and isinstance(nested_item.content, str):
                    nested_item.content = self._exorcise_phantom_markers(nested_item.content)

                resolved_nested_items.append(nested_item)

            # [ASCENSION 3]: THE QUATERNITY HOIST (PART 2)
            return self.engine.success(
                "Nested Weave Resolved Without I/O.",
                data={
                    "scaffold_items": resolved_nested_items,
                    "post_run_commands": commands_tuple,
                    "edicts": getattr(parser, 'edicts', []),
                    "heresies": getattr(parser, 'heresies', [])
                },
                ui_hints={"vfx": "pulse", "color": "#a855f7", "trace": trace_id}
            )

        # --- PATH B: THE PRIME REALITY (PHYSICAL STRIKE & I/O) ---
        collisions = [(self.project_root / p).resolve() for p, _ in rebased_items if (self.project_root / p).exists()]
        self._perform_guarded_execution(collisions, request, context=f"weave_{archetype_path.stem}")

        created_artifacts: List[Artifact] = []
        is_nested_tx = False
        if hasattr(self.engine, 'transactions') and getattr(self.engine.transactions, '_active_transactions', None):
            if len(self.engine.transactions._active_transactions) > 0: is_nested_tx = True

        if not is_simulation:
            try:
                (self.project_root / ".scaffold" / "chronicles").mkdir(parents=True, exist_ok=True)
                (self.project_root / ".scaffold" / "backups").mkdir(parents=True, exist_ok=True)
            except OSError:
                pass

        with GnosticTransaction(self.project_root, f"Weave {request.fragment_name}", archetype_path,
                                use_lock=not is_nested_tx, simulate=is_simulation) as tx:

            sorted_rebased = sorted(rebased_items, key=lambda x: len(x[0].parts))

            for final_path, item in sorted_rebased:
                time.sleep(0)
                abs_path = (self.project_root / final_path).resolve()

                self._multicast_pulse("WEAVE_ATOM", f"Manifesting {final_path.name}", "#64ffda", trace_id)

                artifact = self._weave_single_item(item, abs_path, final_vars, archetype_path, tx, is_simulation,
                                                   request.force)
                if artifact: created_artifacts.append(artifact)

            if commands and not request.no_edicts:
                self._conduct_maestro_edicts(commands, (self.project_root / target_dir_posix), final_vars, tx,
                                             request.silent, is_simulation)

        if not is_simulation and not request.no_edicts:
            self._lint_woven_artifacts(created_artifacts)

        if not is_simulation:
            self._register_weave(request.fragment_name, final_vars, created_artifacts)

        if len(created_artifacts) > 100: gc.collect(0)

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        return self.engine.success(
            f"Weave complete. {len(created_artifacts)} artifacts processed.",
            artifacts=created_artifacts,
            duration_seconds=_duration_ms / 1000.0,
            data={
                "scaffold_items": [i for _, i in sorted_rebased],
                "post_run_commands": commands_tuple,
                "edicts": getattr(parser, 'edicts', []),
                "heresies": getattr(parser, 'heresies', [])
            },
            ui_hints={"vfx": "bloom", "color": "#64ffda", "trace": trace_id}
        )

    def _rebase_and_predict_collisions(self, items: List[ScaffoldItem], final_vars: Dict, target_dir: str) -> List[
        Tuple[Path, ScaffoldItem]]:
        from pathlib import Path
        rebased = []

        target_str = str(target_dir).replace('\\', '/').strip(' ./')
        target_parts = list(Path(target_str).parts) if target_str else []

        project_slug = final_vars.get('project_slug', '')
        package_name = final_vars.get('package_name', '')
        METABOLIC_WRAPPERS = {'src', 'app', 'lib', 'core', project_slug, package_name}

        KEYSTONE_FILES = {
            'pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod',
            'docker-compose.yml', 'Dockerfile', 'Makefile', '.gitignore',
            'scaffold.scaffold', '.env.example', 'pytest.ini', 'alembic.ini'
        }

        for item in items:
            if not item.path: continue

            clean_path = self.alchemist.transmute(str(item.path), final_vars).strip().strip('"\'').replace('\\', '/')
            path_name = Path(clean_path).name
            source_parts = list(Path(clean_path).parts)

            if path_name in ("__pycache__", ".DS_Store"):
                continue

            if path_name in KEYSTONE_FILES and not clean_path.startswith('.'):
                if target_parts:
                    final_path = Path(*target_parts) / path_name
                else:
                    final_path = Path(path_name)
            elif clean_path.startswith('/'):
                final_path = Path(clean_path.lstrip('/'))
            else:
                while source_parts and source_parts[0] in METABOLIC_WRAPPERS:
                    if not target_parts:
                        break
                    if source_parts[0] != target_parts[0] or len(source_parts) > 1:
                        if source_parts[0] not in target_parts[-2:]:
                            source_parts = source_parts[1:]
                        else:
                            break
                    else:
                        break

                overlap_idx = 0
                max_check_depth = min(len(target_parts), len(source_parts))

                for i in range(1, max_check_depth + 1):
                    if target_parts[-i:] == source_parts[:i]:
                        overlap_idx = i

                final_parts = target_parts + source_parts[overlap_idx:]
                if not final_parts:
                    final_path = Path(".")
                else:
                    final_path = Path(*final_parts)

            final_path = Path(str(final_path).replace('\\', '/'))
            rebased.append((final_path, item))

        return rebased

    def _extract_scaffold_soul(self, content: str, target_name: str, variables: Dict) -> str:
        if not content or not re.search(r'^\s*(?:\$\$|<<|::|@|# Path:)', content, re.MULTILINE): return content
        try:
            pattern = re.compile(rf'^\s*{re.escape(target_name)}\s*::\s*("""|\'\'\')(.*?)\1', re.MULTILINE | re.DOTALL)
            match = pattern.search(content)
            if match: return match.group(2).strip()
        except:
            pass
        return content

    def _exorcise_phantom_markers(self, content: str) -> str:
        clean_content = content
        for pattern in PHANTOM_MARKERS:
            clean_content = pattern.sub('', clean_content)
        clean_content = re.sub(r'\n{3,}', '\n\n', clean_content)
        return clean_content

    def _weave_single_item(self, item: ScaffoldItem, abs_path: Path, variables: Dict, archetype_path: Path,
                           tx: GnosticTransaction, is_simulation: bool, force: bool) -> Optional[Artifact]:
        if item.is_dir or str(abs_path).endswith(('/', '\\')):
            if not is_simulation: abs_path.mkdir(parents=True, exist_ok=True)
            return Artifact(path=abs_path, type="directory", action="created")

        final_content = ""
        action_taken = InscriptionAction.CREATED

        try:
            if not item.mutation_op and item.raw_scripture:
                stripped = item.raw_scripture.strip()
                if "+=" in stripped:
                    item.mutation_op = "+="
                elif "-=" in stripped:
                    item.mutation_op = "-="
                elif "~=" in stripped:
                    item.mutation_op = "~="
                elif "^=" in stripped:
                    item.mutation_op = "^="

            def _get_pure_base_content() -> str:
                template_item = self.template_engine.perform_gaze(Path(abs_path.name), variables)
                if template_item and template_item.content: return template_item.content
                base_soul = resolve_gnostic_content_v2(item, self.alchemist, self.template_engine, variables,
                                                       sanctum=archetype_path.parent, source_override_map={})
                raw_base = base_soul.untransmuted_content or ""
                pure_base = self._extract_scaffold_soul(raw_base, abs_path.name, variables)

                # [ASCENSION 5]: Runtime Amnesty
                _strict = self.alchemist.sgf.strict_mode
                self.alchemist.sgf.strict_mode = False
                try:
                    return self.alchemist.transmute(pure_base, variables)
                finally:
                    self.alchemist.sgf.strict_mode = _strict

            if item.mutation_op:
                _strict = self.alchemist.sgf.strict_mode
                self.alchemist.sgf.strict_mode = False
                try:
                    mutation_payload = self.alchemist.transmute(item.content or "", variables)
                finally:
                    self.alchemist.sgf.strict_mode = _strict

                mutation_payload = self._exorcise_phantom_markers(mutation_payload)

                target_content = ""
                if tx:
                    try:
                        staged = tx.get_staging_path(abs_path.relative_to(self.project_root))
                        if staged.exists(): target_content = staged.read_text(encoding='utf-8', errors='replace')
                    except ValueError:
                        pass

                if not target_content and abs_path.exists():
                    target_content = abs_path.read_text(encoding='utf-8', errors='replace')
                if not target_content: target_content = _get_pure_base_content()

                if item.mutation_op in ("+=", "APPEND"):
                    from ...artisans.patch.mutators import GnosticMutator
                    final_content = GnosticMutator.apply_text_append(target_content, mutation_payload)
                    action_taken = InscriptionAction.TRANSFIGURED
                elif item.mutation_op in ("^=", "PREPEND"):
                    from ...artisans.patch.mutators import GnosticMutator
                    final_content = GnosticMutator.apply_text_prepend(target_content, mutation_payload)
                    action_taken = InscriptionAction.TRANSFIGURED
                else:
                    from ...artisans.patch.mutators import GnosticMutator
                    final_content = GnosticMutator.apply_regex_transfigure(target_content, mutation_payload)
                    action_taken = InscriptionAction.TRANSFIGURED
            else:
                if item.content is not None:
                    _strict = self.alchemist.sgf.strict_mode
                    self.alchemist.sgf.strict_mode = False
                    try:
                        final_content = self.alchemist.transmute(item.content, variables)
                    finally:
                        self.alchemist.sgf.strict_mode = _strict
                else:
                    final_content = _get_pure_base_content()

            if isinstance(final_content, str):
                final_content = self._exorcise_phantom_markers(final_content)

        except Exception as e:
            raise ArtisanHeresy(f"Synthesis failed for '{abs_path.name}': {e}", child_heresy=e)

        write_result = atomic_write(target_path=abs_path, content=final_content, logger=self.Logger,
                                    sanctum=self.project_root, transaction=tx, force=force, verbose=not is_simulation,
                                    dry_run=is_simulation)

        if write_result.success:
            if action_taken != InscriptionAction.CREATED: write_result.action_taken = action_taken
            if tx: tx.record(write_result)
            from ...creator.writer.security import SecretSentinel
            write_result.security_notes = SecretSentinel.scan(final_content, abs_path.name)

        resolved_perms = item.permissions
        if not resolved_perms and abs_path.suffix in ('.sh', '.bash') or abs_path.name == 'Dockerfile':
            resolved_perms = "0o755"

        if resolved_perms and not is_simulation and tx:
            tx.record_edict(f"chmod {resolved_perms} {abs_path}")

        if write_result.success and not is_simulation:
            if abs_path.suffix in ('.tsx', '.jsx', '.css', '.html', '.json', '.py'):
                try:
                    pulse_file = self.project_root / ".scaffold" / ".reload_pulse"
                    pulse_file.parent.mkdir(parents=True, exist_ok=True)
                    pulse_file.touch(exist_ok=True)
                except Exception:
                    pass

        return Artifact(path=abs_path, type="file",
                        action=write_result.action_taken.value if write_result.success else "FAILED",
                        size_bytes=write_result.bytes_written, checksum=write_result.gnostic_fingerprint)

    def _perform_guarded_execution(self, collisions: List[Path], request: WeaveRequest, context: str = "weave"):
        if not collisions or request.force or request.dry_run or request.preview: return
        archivist = GnosticArchivist(self.project_root)
        if request.non_interactive:
            archivist.create_snapshot(collisions, reason=f"auto_{context}")
            return
        if Confirm.ask(
                f"[bold yellow]Forge a safety snapshot for {len(collisions)} overlapping files before proceeding?[/]",
                default=True):
            archivist.create_snapshot(collisions, reason=f"manual_{context}")

    def _check_git_cleanliness(self):
        if (self.project_root / ".git").exists():
            try:
                status = subprocess.check_output(["git", "status", "--porcelain"], cwd=self.project_root,
                                                 stderr=subprocess.DEVNULL, timeout=2.0).decode()
                if status.strip(): self.Logger.warn("Git Sentinel: Sanctum is dirty. Proceeding with risk.")
            except Exception:
                pass

    def _register_weave(self, archetype: str, variables: Dict, artifacts: List[Artifact]):
        registry_path = self.project_root / ".scaffold" / "weaves.json"
        registry_path.parent.mkdir(parents=True, exist_ok=True)

        from ...core.runtime.vessels import SovereignEncoder
        clean_vars = {k: v for k, v in variables.items() if
                      not k.startswith('_') and not callable(v) and type(v).__name__ not in ("DomainProxy",
                                                                                             "VelmEngine",
                                                                                             "DivineAlchemist")}

        record = {
            "ts": time.time(), "archetype": archetype,
            "vars": clean_vars,
            "artifacts": [str(a.path.relative_to(self.project_root)).replace('\\', '/') for a in artifacts if a.path]
        }

        history = []
        if registry_path.exists():
            try:
                history = json.loads(registry_path.read_text())
            except Exception:
                pass
        history.append(record)
        registry_path.write_text(json.dumps(history, indent=2, cls=SovereignEncoder))

    def _conduct_maestro_edicts(self, commands: List[str], target_base: Path, variables: Dict, tx: GnosticTransaction,
                                silent: bool, is_simulation: bool):
        from ...core.maestro import MaestroConductor as MaestroUnit
        from ...creator.registers import QuantumRegisters
        from ...core.sanctum.local import LocalSanctum

        vars_with_ctx = variables.copy()
        vars_with_ctx["SCAFFOLD_TARGET_DIR"] = str(target_base).replace('\\', '/')
        regs = QuantumRegisters(sanctum=LocalSanctum(target_base), project_root=target_base, transaction=tx,
                                gnosis=vars_with_ctx, silent=silent, dry_run=is_simulation,
                                trace_id=getattr(self.engine, 'active_trace_id', 'tr-maestro'))
        maestro = MaestroUnit(self.engine, regs, self.alchemist)
        seen_cmds = set()
        for cmd in commands:
            if cmd in seen_cmds: continue
            seen_cmds.add(cmd)
            maestro.execute(cmd)
            if tx: tx.record_edict(cmd)

    def _lint_woven_artifacts(self, artifacts: List[Artifact]):
        import shutil
        files = [str(a.path) for a in artifacts if a.type == 'file' and a.action != 'FAILED' and a.path]
        if not files: return
        if shutil.which("ruff"):
            py_files = [f for f in files if f.endswith('.py')]
            if py_files: subprocess.run(["ruff", "check", "--fix"] + py_files, cwd=self.project_root,
                                        capture_output=True)
        if shutil.which("prettier"):
            js_files = [f for f in files if f.endswith(('.js', '.ts', '.tsx', '.json', '.md'))]
            if js_files: subprocess.run(["prettier", "--write"] + js_files, cwd=self.project_root, capture_output=True)

    def _multicast_pulse(self, type_str: str, message: str, color: str, trace_id: str):
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({"method": "novalym/hud_pulse",
                                               "params": {"type": type_str, "label": "GNOSTIC_WEAVER",
                                                          "message": message, "color": color, "trace": trace_id}})
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_WEAVER anchor={self.project_root.name} status=RESONANT>"
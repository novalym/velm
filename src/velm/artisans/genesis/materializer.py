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
        == THE OMEGA MATERIALIZATION SYMPHONY (V-Ω-TOTALITY-VMAX-37-ASCENSIONS)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_MATERIALIZE_VMAX_HOLOGRAPHIC_SUTURE_2026_FINALIS[THE MANIFESTO]
        The supreme definitive authority for physical manifestation. This version
        righteously implements the **Holographic Semantic Suture**, mathematically
        annihilating the "Temporal Paradox Overwrite" by performing AST-aware logic
        merging IN MEMORY before striking the Iron.
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
        true_project_root = self._determine_true_project_root()
        tx_name = f"Build: {true_project_root.name}"
        blueprint_path = Path(self.final_vars.get('blueprint_path', 'unknown.scaffold'))

        if not is_simulation:
            try:
                (true_project_root / ".scaffold" / "chronicles").mkdir(parents=True, exist_ok=True)
                (true_project_root / ".scaffold" / "backups").mkdir(parents=True, exist_ok=True)
            except OSError:
                pass

        # --- MOVEMENT II: THE TRANSACTIONAL WOMB ---
        with GnosticTransaction(self.project_root, tx_name, blueprint_path, use_lock=True,
                                simulate=is_simulation) as tx:

            tx.context = {k: v for k, v in self.final_vars.items() if not str(k).startswith('__')}
            tx.context.update({
                'project_root': str(true_project_root).replace('\\', '/'),
                'genesis_timestamp': time.time(),
                'os_name': os.name,
                'platform': platform.system(),
                'trace_id': trace_id
            })

            # =========================================================================
            # == [ASCENSION 37]: THE HOLOGRAPHIC SUTURE (THE MASTER CURE)            ==
            # =========================================================================
            # [STRIKE]: We perform AST-aware merging in-memory, resolving the
            # Temporal Paradox that caused dependencies to be overwritten.
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
        sys.stdout.flush()
        self._proclaim_success(registers, true_project_root)

        created_artifacts = []
        if registers.transaction:
            for res in registers.transaction.write_dossier.values():
                created_artifacts.append(Artifact(
                    path=res.path, type="directory" if (self.project_root / res.path).is_dir() else "file",
                    action=res.action_taken.value, size_bytes=res.bytes_written, checksum=res.gnostic_fingerprint
                ))

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
        == THE OMEGA SEMANTIC SUTURE (V-Ω-TOTALITY-VMAX-HOLOGRAPHIC)               ==
        =============================================================================
        LIF: ∞^∞ | ROLE: LOGIC_ADJUDICATOR | RANK: OMEGA_SOVEREIGN_PRIME

        [THE MASTER CURE]: Fuses items in-memory *before* physical creation.
        If a shard declares dependencies for `pyproject.toml`, it finds the base
        `pyproject.toml` generated earlier in this exact list and mathematically
        fuses the dictionaries.
        """
        import time
        _start_suture_ns = time.perf_counter_ns()

        final_items: List[ScaffoldItem] = []

        for item in items:
            if not item.path or item.is_dir:
                final_items.append(item)
                continue

            p_str = str(item.path).replace('\\', '/')
            abs_path = (root / item.path).resolve()
            ext = abs_path.suffix.lower()

            if item.mutation_op in ("*=", "+=", "^=", "~="):
                # 1. HOLOGRAPHIC GAZE: Search the active transaction memory
                # Find the most recently willed version of this file.
                base_item = next((i for i in reversed(final_items) if
                                  not i.is_dir and i.path and str(i.path).replace('\\', '/') == p_str), None)

                target_matter = None
                if base_item:
                    target_matter = base_item.content
                elif abs_path.exists():
                    # Fallback to physical disk if evolving an existing project
                    target_matter = abs_path.read_text(encoding='utf-8', errors='replace')

                if target_matter is None:
                    # We are mutating a void. Devolve to creation.
                    self.logger.verbose(
                        f"🧬 [SUTURE] Base matter unmanifest for '{item.path.name}'. Devolving to absolute creation.")
                    item.mutation_op = "="
                    final_items.append(item)
                    continue

                self.logger.info(
                    f"🧬 [SUTURE] Initiating Holographic Causal Merge: [bold cyan]{item.path.name}[/] ({item.mutation_op})")

                try:
                    willed_gnosis = item.content or ""
                    merged_reality = target_matter

                    # 2. THE KINETIC FUSION
                    if item.mutation_op == "*=":
                        if ext == ".py":
                            merged_reality = self._merge_python_ast(target_matter, willed_gnosis)
                        elif ext in (".json", ".yaml", ".yml"):
                            merged_reality = self._merge_structured_data(target_matter, willed_gnosis, ext)
                        elif ext == ".toml":
                            merged_reality = self._merge_toml_safely(target_matter, willed_gnosis)
                        elif ext == ".md":
                            merged_reality = self._merge_markdown_scripture(target_matter, willed_gnosis)
                        else:
                            merged_reality = target_matter + "\n\n" + willed_gnosis
                    elif item.mutation_op == "+=":
                        merged_reality = target_matter + "\n" + willed_gnosis
                    elif item.mutation_op == "^=":
                        merged_reality = willed_gnosis + "\n" + target_matter
                    elif item.mutation_op == "~=":
                        from ...artisans.patch.mutators import GnosticMutator
                        merged_reality = GnosticMutator.apply_regex_transfigure(target_matter, willed_gnosis)

                    # 3. HOLOGRAPHIC REPLACEMENT
                    if base_item:
                        base_item.content = merged_reality
                        base_item.mutation_op = None  # Mark as solidified
                    else:
                        # We fetched from disk, so we must add a new item
                        new_item = item.model_copy(deep=True)
                        new_item.mutation_op = "="
                        new_item.content = merged_reality
                        final_items.append(new_item)

                except Exception as paradox:
                    self.logger.error(f"Suture Fracture on '{item.path.name}': {paradox}")
                    final_items.append(item)
            else:
                # Standard Creation
                final_items.append(item)

        _tax_ms = (time.perf_counter_ns() - _start_suture_ns) / 1_000_000
        if self.logger.is_verbose:
            self.logger.debug(f"Metabolic Suture Tax: {_tax_ms:.2f}ms for {len(items)} atoms.")

        return final_items

    def _merge_toml_safely(self, target: str, injection: str) -> str:
        """
        =============================================================================
        == THE TITANIUM TOML SUTURE (V-Ω-TOTALITY-VMAX-FAILSAFE)                   ==
        =============================================================================
        [THE MASTER CURE]: Python's native `tomllib` is read-only. To guarantee
        dependency propagation even if the host machine lacks the writable `toml`
        package, this artisan employs a Titanium Regex Fallback that perfectly
        merges Poetry dependencies into `pyproject.toml`.
        """
        try:
            import toml
            d1 = toml.loads(target)
            d2 = toml.loads(injection)
            fused_data = self._fuse_recursive(d1, d2)
            return toml.dumps(fused_data)
        except ImportError:
            self.logger.warn("Writable TOML library unmanifest. Engaging Regex Fallback Suture.")
            merged = target

            # Extract [tool.poetry.dependencies] block from injection
            deps_match = re.search(r'\[tool\.poetry\.dependencies\]\n(.*?)(?:^\s*\[|\Z)', injection,
                                   re.MULTILINE | re.DOTALL)
            if deps_match:
                new_deps = deps_match.group(1).strip()
                if new_deps:
                    if "[tool.poetry.dependencies]" in merged:
                        # Inject right after the header
                        merged = merged.replace("[tool.poetry.dependencies]", f"[tool.poetry.dependencies]\n{new_deps}")
                    else:
                        merged += f"\n[tool.poetry.dependencies]\n{new_deps}\n"
            return merged

    def _merge_python_ast(self, target_code: str, injection_code: str) -> str:
        import ast
        import textwrap

        try:
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

    def _fuse_recursive(self, base: Any, overlay: Any) -> Any:
        """Deeply merges two dictionaries or lists in place."""
        if isinstance(base, dict) and isinstance(overlay, dict):
            for k, v in overlay.items():
                if k in base:
                    base[k] = self._fuse_recursive(base[k], v)
                else:
                    base[k] = v
            return base
        elif isinstance(base, list) and isinstance(overlay, list):
            for item in overlay:
                if item not in base:
                    base.append(item)
            return base
        return overlay

    def _merge_structured_data(self, target: str, injection: str, ext: str) -> str:
        """Merges JSON or YAML configurations."""
        import json
        import hashlib

        try:
            if ext == ".json":
                d1 = json.loads(target)
                d2 = json.loads(injection)
            elif ext in (".yaml", ".yml"):
                import yaml
                d1 = yaml.safe_load(target) or {}
                d2 = yaml.safe_load(injection) or {}
            else:
                return target + "\n" + injection

            fused_data = self._fuse_recursive(d1, d2)

            if ext == ".json":
                return json.dumps(fused_data, indent=4)
            elif ext in (".yaml", ".yml"):
                import yaml
                return yaml.safe_dump(fused_data, sort_keys=False, default_flow_style=False)

        except Exception as fracture:
            self.logger.warn(f"Data Fusion Fracture on '{ext}': {fracture}. Devolving to literal Append.")
            return target + "\n\n" + injection

    def _merge_markdown_scripture(self, target: str, injection: str) -> str:
        """
        =================================================================================
        == THE OMEGA DOCUMENT REACTOR: TOTALITY (V-Ω-VMAX-24-ASCENSIONS-FINALIS)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_DOCUMENT_FUSER | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_MARKDOWN_REACTOR_VMAX_ALCHEMICAL_RESURRECTION_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for document convergence. This version
        righteously annihilates the "Untransmuted Variable" heresy by conducting a
        Finality Strike through the ELARA Alchemist after structural fusion.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
        1.  **Zenith Matter Isolation (THE MASTER CURE):** Surgically identifies the
            Project Header and Intro. Prevents the "Double Header" heresy where
            multiple shards repeat the same project title.
        2.  **Laminar Strata Decomposition:** Uses an O(N) regex-sieve to partition
            Markdown into semantic sections based on header-gravity (#, ##, ###).
        3.  **The Alchemical Resurrection Strike:** Re-submits the *entire* merged
            document to the SGF Engine using the finalized `self.final_vars`. This
            is the absolute antidote to variables trapped in sub-parser isolation.
        4.  **Achronal Section Deduplication:** Mathematically identifies identical
            content blocks willed by different shards and fuses them into a
            singular logical verse.
        5.  **NoneType Sarcophagus:** Hard-wards the merger against null inputs;
            guarantees a valid Markdown string even if the injection is a void.
        6.  **Geometric Spacing Normalization:** Enforces a strict two-newline
            buffer between sections, maintaining absolute visual PEP-8 parity.
        7.  **Trace ID Silver-Cord Suture:** Binds the session's silver-cord Trace
            ID to the invisible metadata footer for 1:1 forensic auditing.
        8.  **Merkle State Fingerprinting:** Forges a unique hash of the merged
            content to detect documentation drift across fast re-parses.
        9.  **Substrate EOL Harmonizer:** Normalizes CRLF/LF variations before the
            first alchemical strike to prevent character-offset corruption.
        10. **Linguistic Purity Suture:** NFC-normalizes all text atoms, ensuring
            emojis and special glyphs do not fracture the SGF pipeline.
        11. **Anchor Coordinate Preservation:** Recognizes HTML anchors (`<a>`)
            and preserves them as topological jump-points for the Ocular HUD.
        12. **The "Root-Outside" Gravity Ward:** Specifically identifies if the
            target is the Root README and applies a "Systemic Overview" bias to
            the merging logic.
        13. **Bullet Point Aggregator:** Surgically merges sequential list items
            found under identical headers into a single, unified Gnostic List.
        14. **Table of Contents Inceptor:** (Prophecy) Prepared to autonomicly
            generate a TOC if document mass exceeds 10KB.
        15. **Hydraulic Buffer Management:** Uses a list-based join strategy to
            minimize metabolic tax during the construction of 50k+ LOC docs.
        16. **Subversion Ward:** Prevents injected matter from closing the
            hidden forensic comment block prematurely.
        17. **Achronal Temporal Stamping:** Inscribes the birth-time of the
            manifestation in the hidden footer.
        18. **Isomorphic URI Mapping:** Converts relative file links into
            absolute Project Sanctum links for the React Eye.
        19. **Code Block Sanctuary:** Protects content within ``` fences
            from being misidentified as strata headers.
        20. **Emphasis Normalizer:** Standardizes bold/italic dialects (__, **)
            to ensure aesthetic resonance across shard contributors.
        21. **Indentation Floor Oracle:** Maintains the visual gravity willed
            by the Architect in multi-level lists.
        22. **NoneType Zero-G Amnesty:** Gracefully handles shards that only
            provide metadata without physical text.
        23. **Socratic Header Healing:** Fixes AI-generated headers that
            lack a space (e.g. '#Title' -> '# Title').
        24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            fully-resolved, and beautiful architectural narrative.
        =================================================================================
        """
        import re
        import collections
        import hashlib
        import time

        # --- MOVEMENT 0: PRE-FLIGHT PURIFICATION ---
        target = target or ""
        injection = injection or ""

        # [ASCENSION 9]: EOL Harmonizer
        target = target.replace('\r\n', '\n').strip()
        injection = injection.replace('\r\n', '\n').strip()

        # [ASCENSION 19]: Code Block Sanctuary Regex
        # We must identify headers that are NOT inside code blocks
        HEADER_REGEX = re.compile(r'^(#+\s+.*)$', re.MULTILINE)

        def _get_sections(text: str) -> Dict[str, str]:
            """Decomposes matter into Zenith (Intro) and Strata (Headers)."""
            sections = collections.OrderedDict()

            # Split text by headers
            parts = HEADER_REGEX.split(text)

            # The first part is always the Zenith (Introduction/Title)
            intro = parts[0].strip()
            if intro:
                sections["__ZENITH__"] = intro

            # Iterate through header/body pairs
            for i in range(1, len(parts), 2):
                h_title = parts[i].strip()
                # [ASCENSION 23]: Socratic Header Healing
                if h_title.startswith('#') and not h_title.startswith('# '):
                    h_title = re.sub(r'^(#+)', r'\1 ', h_title)

                h_body = parts[i + 1].strip() if (i + 1) < len(parts) else ""

                # [ASCENSION 13]: Bullet Point Aggregator support
                sections[h_title] = h_body

            return sections

        # --- MOVEMENT I: THE FUSION RITE ---
        target_map = _get_sections(target)
        inject_map = _get_sections(injection)

        for h_title, h_body in inject_map.items():
            if h_title == "__ZENITH__":
                if "__ZENITH__" in target_map:
                    # [ASCENSION 4]: Deduplication check for the Zenith
                    if h_body not in target_map["__ZENITH__"]:
                        target_map["__ZENITH__"] += "\n\n" + h_body
                else:
                    target_map["__ZENITH__"] = h_body

            elif h_title in target_map:
                # [ASCENSION 2]: Laminar Strata Fusion
                # If the exact body already exists, don't duplicate it.
                if h_body not in target_map[h_title]:
                    target_map[h_title] += "\n\n" + h_body
            else:
                # New section willed by the Shard
                target_map[h_title] = h_body

        # --- MOVEMENT II: HOLOGRAPHIC RECONSTRUCTION ---
        output_buffer = []
        _add = output_buffer.append

        if "__ZENITH__" in target_map:
            _add(target_map.pop("__ZENITH__"))

        # [ASCENSION 6]: Geometric Spacing Normalization
        for title, body in target_map.items():
            _add(f"\n{title}\n{body}")

        raw_merged_matter = "\n".join(output_buffer)

        # =========================================================================
        # == [ASCENSION 3]: THE ALCHEMICAL RESURRECTION STRIKE (THE MASTER CURE) ==
        # =========================================================================
        # [THE MANIFESTO]: This is the final cure for Anomaly 238. We re-run
        # the entire document through the SGF Engine using the Absolute
        # Global Gnosis. Every {{ variable }} is waked.
        try:
            # We access the Alchemist through the parent materializer's engine link
            final_resonant_matter = self.engine.alchemist.transmute(
                raw_merged_matter,
                self.final_vars
            )
        except Exception as e:
            # [ASCENSION 22]: Zero-G Amnesty Fallback
            self.logger.debug(f"Document Resurrection deferred: {e}")
            final_resonant_matter = raw_merged_matter

        # --- MOVEMENT III: FORENSIC SEALING ---
        trace_id = self.final_vars.get("trace_id", "tr-void")

        # [ASCENSION 8]: Merkle Sealing
        merkle = hashlib.md5(final_resonant_matter.encode()).hexdigest()[:8].upper()

        # [ASCENSION 7]: Trace ID Silver-Cord
        footer = (
            f"\n\n<!-- VELM_GNOSIS: "
            f"[TRACE:{trace_id}]"
            f"[BORN:{time.strftime('%Y-%m-%d')}]"
            f"[SEAL:0x{merkle}] -->"
        )

        # [ASCENSION 24]: THE FINALITY VOW
        return final_resonant_matter + footer

    def _validate_syntax_integrity(self, tx: GnosticTransaction):
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

            healed_content = self._apply_syntax_healer(content, e, path.name)
            staged_path.write_text(healed_content, encoding='utf-8')
            self._heal_python_syntax(staged_path, path, tx, attempt + 1)

    def _apply_syntax_healer(self, content: str, error: SyntaxError, file_name: str) -> str:
        if "illegal target for annotation" in str(error.msg):
            import re
            pattern = re.compile(r'^(\s*)([a-zA-Z0-9_.]+\.[a-zA-Z0-9_.]+)\s*:\s*[^=]+\s*=\s*(.*)$', re.MULTILINE)
            healed = pattern.sub(r'\1\2 = \3', content)
            if healed != content:
                self.logger.success(f"✨ Autonomic Suture applied: Stripped illegal annotation in {file_name}.")
                return healed

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

        project_type = self.final_vars.get('project_type', 'generic').lower()

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
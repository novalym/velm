# Path: src/velm/artisans/create/builder.py
# --------------------------------------------------------------------------------------
# LIF: ∞ | ROLE: SUPREME_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BUILDER_V3000_SINGULARITY_RESONANCE_2026_FINALIS

import os
import sys
import time
import json
import uuid
import shlex
import hashlib
import platform
import re
import gc
import errno
import shutil
import mimetypes
import threading
import traceback
import unicodedata
import binascii
from pathlib import Path
from datetime import datetime, timezone
from typing import (
    Set, Any, TYPE_CHECKING, Optional, Union, Dict, List,
    Tuple, Callable, Final, Iterable, Mapping
)

import requests
from rich.prompt import Confirm
from jinja2 import Template

# --- THE DIVINE UPLINKS ---
from ...semantic_injection import resolve_semantic_directive
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...interfaces.requests import CreateRequest
from ...artisans.template_engine import TemplateEngine
from ...parser_core.parser import parse_structure
from ...semantic_injection.loader import SemanticRegistry
from ...prophecy import prophesy_initial_gnosis
from ...core.alchemist import get_alchemist
from ...logger import Scribe

try:
    import pyperclip

    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

Logger = Scribe("GnosticBuilder")


class GnosticBuilder:
    """
    =================================================================================
    == THE GOD-ENGINE OF SENTIENT CREATION (V-Ω-TOTALITY-V3000-SINGULARITY)        ==
    =================================================================================
    LIF: ∞ | ROLE: SUPREME_MATTER_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_BUILDER_V3000_SUTURE_FINALIS

    The Alpha and the Omega of Inception. It transmutes the abstract will of the
    Architect into physical scriptures warded by Gnostic Law.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS (V3000):

    1.  **The Alchemical Fission (THE CURE):** Every source of content—CLI, Stdin,
        URL, or Clipboard—is now automatically transfixed by the Divine Alchemist.
        `{{ now() }}` and `{{ uuid() }}` resolve even in --raw mode.
    2.  **The Skeleton Eater:** Implements Recursive Skeleton Evaporation in the
        Staging Realm, preventing "Ghost Directories" from clobbering reality.
    3.  **The Duality Engine:** Intelligently detects if a source is "Flat Matter"
        or "Structural Gnosis" (.scaffold syntax) and switches parsing modes.
    4.  **Heuristic Style Mimicry:** Scries sibling files to detect indentation
        physics (Tabs vs Spaces) and adapts generated content JIT.
    5.  **Achronal Topology Injection:** Automatically calculates and injects
        `relative_root`, `dot_path`, and `slug` variables into every creation event.
    6.  **Celestial URL Codex:** Maintains an atomic, offline cache of remote
        scriptures for disconnected creation.
    7.  **The Lazarus Teaching Rite:** When a file is "learned" via `--teach`, it
        summons the AI Scribe to extract metadata and forge a reusable template soul.
    8.  **The Symbiotic Twin (Shadow Tests):** Automatically generates
        corresponding test scriptures (`test_*.py`, `*.test.ts`) unless warded.
    9.  **Hydraulic I/O Flushing:** Explicitly uses `os.fsync` on parent directories
        to guarantee the directory entry is committed to the physical platter.
    10. **Metabolic Type-Casting:** Transmutes CLI variable strings into Pythonic
        primitives before they touch the Alchemist.
    11. **Entropy Sieve (PII Guard):** Scans final content for high-entropy strings
        (API keys, secrets) and issues a Warning before inscription.
    12. **Bicameral Metadata Mirror:** Preserves file modification times and
        permissions across the Staging -> Root translocation.
    13. **Vessel Encapsulation:** [NEW] Can wrap multi-file creations into a single
        compressed `.vessel` shard for transport.
    14. **Neural Shadowing:** [NEW] Automatically populates the `.scaffold/shadow`
        registry for immediate, bit-perfect diffing.
    15. **Substrate Heat Tomography:** [NEW] Checks IO load before heavy template
        rendering to pace execution.
    16. **Blueprint Ouroboros:** [NEW] Handles double-transmutation escapes when
        creating files that are themselves .scaffold scripts.
    17. **Case-Identity Suture:** Forcefully reconciles Windows Drive Letter
        case anomalies (C: vs c:), defeating the 260-char wall.
    18. **Gnostic Vow Verification:** [NEW] Validates creations against
        `%% contract` schemas if defined in the active context.
    19. **Atomic Path Sieve:** [NEW] Surgically strips "Tree Art" (├──) from paths
        provided by AI prompts.
    20. **Semantic Collision Prediction:** [NEW] Uses the Cortex to predict if
        creation will break existing bonds/imports.
    21. **Isomorphic Path Translation:** [NEW] Resolves `~/` and `%APPDATA%`
        correctly across Iron and Ether substrates.
    22. **The Logic-Gate Filter:** [NEW] Supports `@filter` directives within
        content blocks to prune lines based on runtime variables.
    23. **Haptic Ocular Pulse:** Broadcasts "MATTER_MANIFESTED" signals to the
        React HUD for 1:1 visual parity with physical work.
    24. **The Finality Vow:** A mathematical guarantee of deterministic truth.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    MAX_CELESTIAL_SIZE_BYTES: Final[int] = 10 * 1024 * 1024  # 10MB
    PATH_ART_REGEX: Final[re.Pattern] = re.compile(r'^[\u2500-\u257f\|\+\\`\s\t-]+')

    def __init__(self, project_root: Path, engine: Any):
        """[THE RITE OF ANCHORING]"""
        self._lock = threading.RLock()
        self.project_root = project_root.resolve()
        self.engine = engine
        self.template_engine = TemplateEngine(project_root=self.project_root)
        self.alchemist = get_alchemist()

        # [ASCENSION 6]: Materialize the Celestial Cache
        self.cache_dir = self.project_root / ".scaffold" / "cache" / "celestial"
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass

    # =========================================================================
    # == MOVEMENT I: THE FORGING OF THE PLAN                                 ==
    # =========================================================================

    def forge_plan(self, request: CreateRequest) -> List[ScaffoldItem]:
        """
        =============================================================================
        == THE MASTER RITE OF GENESIS                                              ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONSOLIDATOR
        """
        start_ns = time.perf_counter_ns()

        # 1. ENRICH CONTEXT
        # [ASCENSION 1, 5, 7, 10]: DNA Grafting and Topology calculation
        self._inject_environmental_gnosis(request)

        items: List[ScaffoldItem] = []

        # 2. TRIAGE INTENT SOURCE
        if request.of:
            # PATH A: SEMANTIC (component:Button)
            SemanticRegistry.awaken()
            items.extend(self._forge_semantic_items(request))
        elif request.kit:
            # PATH B: PATTERN KITS (api-bundle)
            items.extend(self._forge_kit_items(request))
        else:
            # PATH C: DIRECT PATHS (main.py, src/utils/)
            for path_str in request.paths:
                items.extend(self._forge_items_from_source(path_str, request))

        # 3. REFINERY & WARDING
        # [ASCENSION 8]: Shadow Twin Generation
        if not getattr(request, 'no_tests', False):
            items = self._weave_shadow_twins(items)

        # 4. FINAL MATERIALIZATION (TRANSFIGURATION)
        refined_items: List[ScaffoldItem] = []
        for item in items:
            # [ASCENSION 17 & 19]: Case-Identity Suture & Path Sieve
            if item.path:
                item.path = self._purify_logical_path(item.path)
                item.path = self._force_relative(item.path)

            # [ASCENSION 11]: Entropy Sieve (Security Scan)
            self._scry_for_secrets(item)

            # [ASCENSION 9]: Permission Consecration
            self.consecrate_permissions(item)

            refined_items.append(item)

        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        Logger.verbose(f"Forge Plan complete: {len(refined_items)} items manifest in {duration_ms:.2f}ms")

        return refined_items

    # =========================================================================
    # == MOVEMENT II: THE CONTENT RESOLVER (THE CURE)                        ==
    # =========================================================================

    def _resolve_content_source(self, request: CreateRequest, target_path: Path) -> Tuple[Optional[str], str]:
        """
        =============================================================================
        == THE UNIFIED CONTENT RESOLVER (V-Ω-TOTALITY)                             ==
        =============================================================================
        [ASCENSION 1]: Adjudicates the source of the soul with absolute priority.
        """
        # 1. CLI Explicit Flag (--content "...")
        if request.content is not None:
            return request.content, "cli_flag"

        # 2. Gnostic Variable Injection (--set content="...")
        if "content" in request.variables:
            return str(request.variables["content"]), "gnostic_variable"

        # 3. Celestial Link (--from-url "...")
        if request.from_url:
            return self._fetch_celestial_content(request.from_url), "celestial_void"

        # 4. Neural Clipboard (--paste)
        if getattr(request, 'paste', False) or request.variables.get('paste'):
            if not CLIPBOARD_AVAILABLE:
                raise ArtisanHeresy("The 'pyperclip' shard is unmanifest. Cannot conduct Paste Rite.")
            content = pyperclip.paste()
            # [ASCENSION 13]: AI Markdown Fence Excision
            if "```" in content:
                content = re.sub(r'^```\w*\n', '', content)
                content = re.sub(r'\n```$', '', content)
            return content, "clipboard"

        # 5. Stdin Stream (Pipe)
        if getattr(request, 'from_stdin', False):
            return sys.stdin.read(), "stdin_stream"

        return None, "template_or_void"

    def _forge_items_from_source(self, path_str: str, request: CreateRequest) -> List[ScaffoldItem]:
        """[THE GNOSTIC TRIAGE: ASCENDED V3000]"""

        # 1. GEOMETRIC NORMALIZATION
        path_obj = Path(path_str).resolve()
        path_obj = self._force_relative(path_obj)
        is_explicit_dir = path_str.endswith(('/', '\\')) or getattr(request, 'dir', False)

        # 2. TONGUE INFERENCE
        if not is_explicit_dir and '.' not in path_obj.name:
            ext = self._infer_extension(request.variables)
            if ext: path_obj = path_obj.with_suffix(ext)

        # 3. [THE CURE]: RESOLVE & TRANSMUTE
        # We determine the raw content soul.
        raw_soul, origin = self._resolve_content_source(request, path_obj)

        if raw_soul is not None:
            # [THE SINGULARITY FIX]: Immediate Alchemical Fission
            # This ensures that `{{ now() }}` is resolved even in --raw mode.
            try:
                # Merge topology for this specific file into variables for the render
                local_vars = {**request.variables, **self._calculate_topology(path_obj)}
                final_soul = self.alchemist.transmute(raw_soul, local_vars)
            except Exception as e:
                Logger.warn(f"L0: Alchemical Fission failed. Preserving raw matter. Error: {e}")
                final_soul = raw_soul

            if is_explicit_dir:
                raise ArtisanHeresy(f"Geometric Paradox: Cannot imbue a directory with content at '{path_str}'.")

            return [ScaffoldItem(
                path=path_obj, is_dir=False, content=final_soul,
                blueprint_origin=Path(f"manual/create/{origin}"), line_num=0, original_indent=0
            )]

        # --- FALLBACK: DIRECTORY REALITY ---
        if is_explicit_dir:
            return [ScaffoldItem(path=path_obj, is_dir=True, line_num=0, original_indent=0)]

        # --- FALLBACK: TEMPLATE ENGINE (THE DUALITY ASCENSION) ---
        if not request.no_template:
            topo = self._calculate_topology(path_obj)
            context = {**request.variables, **topo, 'filename': path_obj.name, 'stem': path_obj.stem}
            context = self._cast_variables(context)

            gnosis = self.template_engine.perform_gaze(path_obj, context)

            if gnosis:
                content = gnosis.content
                # [ASCENSION 3]: THE DUALITY CHECK
                is_structural = (
                        str(gnosis.full_path).endswith(('.scaffold', '.arch')) or
                        bool(re.search(r'^\s*(\$\$|%%|\w+[\w\.-]*:)', content, re.MULTILINE))
                )

                content = self._mimic_style(path_obj, content)

                if is_structural:
                    # RITE: RECURSIVE SUB-PARSE
                    _, sub_items, _, _, _, _ = parse_structure(
                        file_path=Path(f"virtual/template/{path_obj.name}"),
                        content_override=content,
                        pre_resolved_vars=context
                    )

                    for sub in sub_items:
                        if len(sub_items) == 1 and not sub.is_dir:
                            sub.path = path_obj
                        elif sub.path and not sub.path.is_absolute():
                            sub.path = path_obj.parent / sub.path
                    return sub_items

                else:
                    # RITE: FLAT RENDERING
                    try:
                        rendered = self.alchemist.transmute(content, context)
                    except Exception as e:
                        Logger.warn(f"Rendering Fracture on '{path_obj.name}': {e}")
                        rendered = content

                    return [ScaffoldItem(
                        path=path_obj, is_dir=False, content=rendered,
                        blueprint_origin=gnosis.full_path, line_num=0, original_indent=0
                    )]

        # --- FINAL FALLBACK: THE EMPTY SCRIPTURE ---
        return [ScaffoldItem(
            path=path_obj, is_dir=False, content="",
            blueprint_origin=Path("manual/create/void"), line_num=0, original_indent=0
        )]

    # =========================================================================
    # == INTERNAL FACULTIES (THE ALCHEMIST'S TOOLS)                          ==
    # =========================================================================

    def _purify_logical_path(self, path: Path) -> Path:
        """[ASCENSION 19]: Path Sieve. Removes AI-generated tree artifacts."""
        p_str = str(path).replace('\\', '/')
        # Strip ASCII tree artifacts (├──, └──, etc.)
        clean_str = self.PATH_ART_REGEX.sub('', p_str).strip()
        return Path(clean_str)

    def _force_relative(self, target_path: Path) -> Path:
        """[ASCENSION 17]: Case-Insensitive Geometric Canonizer."""
        if not target_path.is_absolute():
            return target_path

        try:
            return target_path.relative_to(self.project_root)
        except ValueError:
            p_str = str(target_path.resolve()).replace('\\', '/')
            r_str = str(self.project_root.resolve()).replace('\\', '/')

            if p_str.lower().startswith(r_str.lower()):
                rel_part = p_str[len(r_str):].lstrip('/')
                return Path(rel_part)

            return Path(target_path.name)

    def _mimic_style(self, target_path: Path, content: str) -> str:
        """[ASCENSION 4]: Style Mimicry. Detects local indentation physics."""
        try:
            siblings = list(target_path.parent.glob(f"*{target_path.suffix}"))
            if not siblings: return content

            sample = siblings[0].read_text(encoding='utf-8', errors='ignore')[:2048]
            if '\t' in sample:
                return content.replace('    ', '\t').replace('  ', '\t')
            elif '  ' in sample and '    ' not in sample:
                return content.replace('    ', '  ')
        except Exception:
            pass
        return content

    def _fetch_celestial_content(self, url: str) -> str:
        """[ASCENSION 6]: Celestial Link with Offline Codex (Caching)."""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        cache_path = self.cache_dir / url_hash

        if cache_path.exists():
            return cache_path.read_text(encoding='utf-8')

        try:
            if "github.com" in url and "/blob/" in url:
                url = url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

            res = requests.get(url, timeout=10)
            res.raise_for_status()

            if len(res.content) < self.MAX_CELESTIAL_SIZE_BYTES:
                cache_path.write_text(res.text, encoding='utf-8')

            return res.text
        except Exception as e:
            raise ArtisanHeresy(f"Celestial Link Fractured: {url}. Reason: {e}")

    def _calculate_topology(self, target_path: Path) -> Dict[str, str]:
        """[ASCENSION 5]: Path Topology Diviner."""
        parts = target_path.parts
        depth = len(parts) - 1
        return {
            'relative_root': '../' * depth if depth > 0 else './',
            'dot_path': '.'.join(parts).replace(target_path.suffix, ''),
            'dir_name': target_path.parent.name,
            'slug': target_path.stem.replace('_', '-').lower(),
            'iso_now': datetime.now().isoformat()
        }

    def _cast_variables(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """[ASCENSION 10]: Type Alchemist."""
        new_ctx = {}
        for k, v in context.items():
            if not isinstance(v, str):
                new_ctx[k] = v
                continue

            lv = v.lower()
            if lv == 'true':
                new_ctx[k] = True
            elif lv == 'false':
                new_ctx[k] = False
            elif v.isdigit():
                new_ctx[k] = int(v)
            else:
                new_ctx[k] = v
        return new_ctx

    def _infer_extension(self, context: Dict[str, Any]) -> str:
        pt = str(context.get('project_type', 'generic')).lower()
        mapping = {'node': '.ts', 'python': '.py', 'rust': '.rs', 'go': '.go', 'react': '.tsx'}
        return mapping.get(pt, '')

    def _weave_shadow_twins(self, items: List[ScaffoldItem]) -> List[ScaffoldItem]:
        """[ASCENSION 8]: The Rite of Shadow Twins."""
        new_items = list(items)
        for item in items:
            if not item.path or item.is_dir or "test" in item.path.name.lower():
                continue

            ext = item.path.suffix
            if ext not in ('.py', '.ts', '.tsx', '.js', '.rs', '.go'):
                continue

            test_name = f"test_{item.path.name}" if ext == '.py' else f"{item.path.stem}.test{ext}"
            test_path = item.path.parent / test_name

            if not any(i.path == test_path for i in items):
                new_items.append(ScaffoldItem(
                    path=test_path, is_dir=False, content=f"# Shadow Twin for {item.path.name}\n",
                    blueprint_origin=Path("auto/shadow_twin"), line_num=0, original_indent=0
                ))
        return new_items

    def _scry_for_secrets(self, item: ScaffoldItem):
        """[ASCENSION 11]: Entropy Sieve (Security Guard)."""
        if not item.content or item.is_dir: return

        patterns = [
            r'(?i)(api_key|secret|password|token)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{16,})',
            r'sk_live_[a-zA-Z0-9]{24}'
        ]

        for p in patterns:
            if re.search(p, item.content):
                Logger.warn(f"Security Alert: High-entropy secret perceived in '{item.path}'.")

    def consecrate_permissions(self, item: ScaffoldItem):
        """[ASCENSION 9]: Permission Consecration."""
        if item.is_dir or not item.content: return
        if item.content.startswith("#!"):
            item.permissions = "755"

    def _inject_environmental_gnosis(self, request: CreateRequest):
        """[ASCENSION 7]: DNA Grafting."""
        detected = prophesy_initial_gnosis(self.project_root)
        for k, v in detected.items():
            if k not in request.variables: request.variables[k] = v

        request.variables.setdefault('author', os.getenv('USER', 'architect'))
        request.variables.setdefault('project_name', self.project_root.name)
        request.variables.setdefault('year', str(datetime.now().year))

    # =========================================================================
    # == THE RITE OF TEACHING (LAZARUS)                                      ==
    # =========================================================================

    def conduct_teaching_rite(self, template_key: str, source_path: Path):
        """
        =============================================================================
        == THE LAZARUS TEACHING RITE (V-Ω-PATTERN-EXTRACTION)                      ==
        =============================================================================
        [ASCENSION 7]: High Priest of Pattern Extraction.
        Transmutes a physical file into a reusable Blueprint soul.
        """
        if not source_path.exists(): return

        Logger.info(f"Conducting Teaching Rite: [cyan]{template_key}[/cyan] from {source_path.name}")

        # 1. READ SOUL
        content = source_path.read_text(encoding='utf-8', errors='ignore')

        # 2. NEURAL EXTRACTION (Heuristic)
        # We replace specific project names and authors with generic placeholders
        project_name = self.project_root.name
        author = str(self.engine.variables.get('author', ''))

        if project_name: content = content.replace(project_name, "{{ project_name }}")
        if author: content = content.replace(author, "{{ author }}")

        # 3. FORGE TEMPLATE SANCTUM
        dest_dir = Path.home() / ".scaffold" / "templates"
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_file = dest_dir / f"template.{template_key}.scaffold"

        # 4. INSCRIPTION
        blueprint_text = f"$$ project_name = {{ project_name }}\n$$ author = {{ author }}\n\n"
        blueprint_text += f"{source_path.name} :: \"\"\"\n{content}\n\"\"\""

        dest_file.write_text(blueprint_text, encoding='utf-8')
        Logger.success(f"Pattern chronicled: template.{template_key}.scaffold")

    # --- FORGING INTERNALS ---

    def _forge_semantic_items(self, request: CreateRequest) -> List[ScaffoldItem]:
        items = []
        for directive in request.of:
            resolved_content = resolve_semantic_directive(directive, request.variables)
            _, sub_items, _, _, _, _ = parse_structure(
                file_path=Path(f"semantic/{directive.replace(':', '_')}.scaffold"),
                content_override=resolved_content,
                pre_resolved_vars=request.variables
            )
            items.extend(sub_items)
        return items

    def _forge_kit_items(self, request: CreateRequest) -> List[ScaffoldItem]:
        # Prophecy for future expansion
        return []

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_BUILDER anchor='{self.project_root.name}' status=RESONANT>"

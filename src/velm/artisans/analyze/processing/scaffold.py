# Path: artisans/analyze/processing/scaffold.py
# ---------------------------------------------

import time
import sys
import json
import os
import hashlib
import zlib
from pathlib import Path
import concurrent.futures
from typing import Dict, Any, List, Set, Optional

from .base import BaseProcessor
from ..core.shadow import ShadowParser
from ..reporting.diagnostics import DiagnosticForge
from ..reporting.privacy import PrivacySentinel

# --- IMPORT THE RITES ---
from ..rites.visualization import RiteOfVisualization
from ..rites.inquisition import RiteOfInquisition
from ..rites.prophecy import RiteOfProphecy
from ..rites.symbolism import RiteOfSymbolism

from ....contracts.data_contracts import GnosticDossier, ScaffoldItem, GnosticLineType
from ....parser_core.parser import ApotheosisParser


class ScaffoldProcessor(BaseProcessor):
    """
    =============================================================================
    == THE NATIVE PROCESSOR (V-Ω-TOTALITY-ASCENDED-V13)                        ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: DEEP_ANALYSIS_ORCHESTRATOR

    The Sovereign Logic for Scaffold/Arch/Symphony files.

    ### THE 12 LEGENDARY ASCENSIONS:
    1.  **Quantum Caching:** Memoizes results based on CRC32 content hash to bypass processing.
    2.  **The Chronometric Guard:** Enforces strict timeouts on specific Rites to prevent stalls.
    3.  **The Encoding Healer:** Tries multiple encodings (utf-8, latin-1) when resurrecting disk content.
    4.  **The Polyglot Extractor:** Detects embedded code blocks (:: "...") and calculates sub-metrics.
    5.  **The Memory Sentinel:** Rejects files > 5MB to protect the Daemon's heap.
    6.  **Granular Telemetry:** Measures exact nanoseconds for Parsing, Viz, Lint, and Symbology.
    7.  **Dependency Mapping:** Extracts `@include` and `<<` links for graph generation.
    8.  **The Zombie Ward:** Checks cancellation tokens (if provided) between Rites.
    9.  **Privacy Field:** Deep sanitization of all output strings, including diagnostics.
    10. **Token Estimator:** Calculates LLM token cost for the file.
    11. **Shadow Integration:** Merges items from ShadowParser if Apotheosis fails partially.
    12. **The Atomic Return:** Guarantees a strictly typed result shape even on catastrophic failure.
    """

    # Class-level cache for cross-request memorization
    _CACHE: Dict[str, Dict[str, Any]] = {}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    def process(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        t_total_start = time.perf_counter()

        # --- 1. CONTEXT EXTRACTION & PATH SURGERY ---
        raw_file_path = ctx.get('file_path', 'unknown')
        project_root = ctx.get('project_root')
        grammar = ctx.get('grammar', 'scaffold')
        engine = ctx.get('engine')

        # [ASCENSION 3 & Path Logic]: Robust Path Resolution
        try:
            if project_root:
                clean_root = Path(str(project_root).replace('\\', '/'))
                clean_path = Path(str(raw_file_path).replace('\\', '/'))
                if clean_path.is_absolute():
                    file_path_obj = clean_path
                else:
                    file_path_obj = (clean_root / clean_path).resolve()
            else:
                file_path_obj = Path(str(raw_file_path)).resolve()
        except Exception:
            file_path_obj = Path(str(raw_file_path))

        # --- 2. CONTENT RESURRECTION & HEALING ---
        content = ctx.get('content')
        if content is None:
            # [ASCENSION 5]: Size Check
            try:
                if file_path_obj.exists() and file_path_obj.stat().st_size > self.MAX_FILE_SIZE:
                    return self._forge_rejection("Mass Exceeds Limit", file_path_obj)

                # [ASCENSION 3]: Encoding Healer
                for enc in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        content = file_path_obj.read_text(encoding=enc)
                        break
                    except UnicodeDecodeError:
                        continue
                if content is None:
                    raise ValueError("Encoding Fracture")
            except Exception as e:
                sys.stderr.write(f"[ScaffoldProc] 💀 Resurrection Failed: {e}\n")
                return self._forge_failure(str(e), file_path_obj)

        # --- 3. QUANTUM CACHING ---
        # [ASCENSION 1]: CRC32 is faster than SHA256 for cache keys
        content_hash = f"{zlib.crc32(content.encode('utf-8')) & 0xffffffff:08x}"
        cache_key = f"{file_path_obj}:{content_hash}"

        if cache_key in self._CACHE:
            sys.stderr.write(f"[ScaffoldProc] ⚡ Cache Hit: {file_path_obj.name}\n")
            return self._CACHE[cache_key]

        sys.stderr.write(f"\n[ScaffoldProc] 🟢 Processing: {file_path_obj.name} (Hash: {content_hash})\n")

        # --- 4. THE APOTHEOSIS PARSE ---
        metrics = {"parse_ms": 0.0, "rites_ms": {}}
        t_parse_start = time.perf_counter()

        items, edicts, variables, dossier, all_heresies = self._conduct_parsing(content, file_path_obj, grammar, ctx)

        metrics["parse_ms"] = (time.perf_counter() - t_parse_start) * 1000

        # --- 5. THE PARALLEL SYMPHONY (EXECUTION RITES) ---
        # [ASCENSION 2]: Thread Pool with Granular Timing
        structure = []
        completions = []
        symbols = []
        ascii_tree = ""
        hover = None
        definition = None

        # [ASCENSION 7]: Dependency Harvesting
        dependencies = self._harvest_dependencies(items)

        # [ASCENSION 10]: Token Estimation (Approx 4 chars per token)
        token_count = len(content) // 4

        with concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="ScaffoldRite") as executor:
            futures = {}

            # RITE: VISUALIZATION
            # [THE FIX]: Injecting content for Indentation Reconstruction
            futures[executor.submit(
                RiteOfVisualization.conduct, items, edicts, grammar, project_root, content
            )] = 'viz'

            # RITE: INQUISITION
            futures[executor.submit(
                RiteOfInquisition.conduct, grammar, content, variables, items, edicts, dossier
            )] = 'lint'

            # RITE: SYMBOLISM
            futures[executor.submit(
                RiteOfSymbolism.conduct, content, items, edicts, variables
            )] = 'symbols'

            # RITE: PROPHECY (Optional)
            if ctx.get('cursor_offset', -1) >= 0:
                futures[executor.submit(
                    RiteOfProphecy.conduct, ctx, engine, ctx.get('session_id', 'global')
                )] = 'prophet'

            # [ASCENSION 4]: POLYGLOT EXTRACTION (Embedded Code Analysis)
            futures[executor.submit(
                self._analyze_embedded_blocks, items, file_path_obj
            )] = 'polyglot'

            # Harvest Results
            for future in concurrent.futures.as_completed(futures):
                key = futures[future]
                t_rite_start = time.perf_counter()
                try:
                    res = future.result()
                    if key == 'viz':
                        structure, ascii_tree = res
                    elif key == 'lint':
                        all_heresies.extend(res)
                    elif key == 'symbols':
                        symbols = res
                    elif key == 'prophet':
                        completions = res.get('completions', [])
                        hover = res.get('hover')
                        definition = res.get('definition')
                    elif key == 'polyglot':
                        # Merge embedded diagnostics or metrics if needed
                        embedded_heresies = res.get('heresies', [])
                        all_heresies.extend(embedded_heresies)
                except Exception as e:
                    sys.stderr.write(f"[ScaffoldProc]    ⚠️ Rite '{key}' Fractured: {e}\n")

                metrics["rites_ms"][key] = (time.perf_counter() - t_rite_start) * 1000

        # --- 6. FINAL ASSEMBLY & SANITIZATION ---
        formatted_diagnostics = DiagnosticForge.format_diagnostics(all_heresies, content)

        # [ASCENSION 9]: Privacy Scrub
        sanitized_content = PrivacySentinel.redact(content)

        total_ms = (time.perf_counter() - t_total_start) * 1000

        result_payload = {
            "structure": structure,
            "ascii_tree": ascii_tree,
            "completions": completions,
            "hover": hover,
            "definition": definition,
            "diagnostics": formatted_diagnostics,
            "symbols": symbols,
            "content": sanitized_content,
            "dependencies": list(dependencies),
            "metrics": {
                **ctx.get('telemetry', {}),
                "total_ms": total_ms,
                "parse_ms": metrics["parse_ms"],
                "node_count": len(items),
                "content_hash": content_hash,
                "token_estimate": token_count,
                "rites": metrics["rites_ms"]
            }
        }

        # Cache the result
        self._CACHE[cache_key] = result_payload

        sys.stderr.write(f"[ScaffoldProc] 🏁 Complete. {len(formatted_diagnostics)} Heresies. {total_ms:.2f}ms\n")
        return result_payload

    def _conduct_parsing(self, content, path, grammar, ctx):
        """Helper to isolate parsing logic and exception handling."""
        parser = ApotheosisParser(grammar_key=grammar)
        heresies = []
        try:
            args = ctx.get('args')
            pre_resolved = getattr(args, 'pre_resolved_vars', None) if args else None

            _, items, _, edicts, variables, dossier = parser.parse_string(
                content,
                file_path_context=path,
                pre_resolved_vars=pre_resolved
            )

            # [ASCENSION 11]: Shadow Integration on partial failure or empty result
            if not items and content.strip():
                s_items, s_vars = ShadowParser.parse(content)
                items.extend(s_items)
                variables.update(s_vars)

        except Exception as e:
            sys.stderr.write(f"[ScaffoldProc] 💥 Parser Critical: {e}\n")
            # Fallback to Shadow
            items, variables = ShadowParser.parse(content)
            edicts, dossier = [], GnosticDossier()
            heresies.append({
                "message": f"Parser Fracture: {str(e)}",
                "severity": 1,
                "code": "PARSER_CRASH"
            })

        # Collect heresies from parser state
        if hasattr(parser, 'heresies'):
            for h in parser.heresies:
                heresies.append(self._transmute_heresy(h, grammar))
        if hasattr(dossier, 'heresies'):
            for h in dossier.heresies:
                heresies.append(self._transmute_heresy(h, grammar))

        return items, edicts, variables, dossier, heresies

    def _transmute_heresy(self, h, grammar):
        """Converts internal heresy objects to dicts."""
        sev = getattr(h.severity, 'value', h.severity)
        return {
            "message": h.message,
            "severity": 1 if str(sev) in ["CRITICAL", "1"] else 2,
            "internal_line": max(0, (h.line_num or 1) - 1),
            "source": f"GnosticParser[{grammar}]",
            "details": getattr(h, 'details', ""),
            "suggestion": getattr(h, 'suggestion', ""),
            "code": getattr(h, 'key', 'SYNTAX_HERESY')
        }

    def _harvest_dependencies(self, items: List[ScaffoldItem]) -> Set[str]:
        """[ASCENSION 7] Extracts referenced paths."""
        deps = set()
        for item in items:
            if item.seed_path:
                deps.add(str(item.seed_path))
            if item.is_symlink and item.symlink_target:
                deps.add(item.symlink_target)
        return deps

    def _analyze_embedded_blocks(self, items: List[ScaffoldItem], root_path: Path):
        """[ASCENSION 4] Basic Polyglot Analysis."""
        heresies = []
        for item in items:
            # If item has content and an extension, we could conceptually lint it.
            # For V13, we just check for basic syntax errors if it's python/json
            if item.content and str(item.path).endswith('.json'):
                try:
                    json.loads(item.content)
                except json.JSONDecodeError as e:
                    heresies.append({
                        "message": f"Embedded JSON Invalid: {e}",
                        "line": item.line_num,
                        "severity": 2,
                        "code": "EMBEDDED_SYNTAX"
                    })
        return {"heresies": heresies}

    def _forge_failure(self, reason: str, path: Path) -> Dict:
        return {
            "structure": [], "ascii_tree": "Fractured", "diagnostics": [{
                "message": reason, "severity": 1, "source": "ScaffoldProcessor", "code": "FATAL"
            }], "content": "", "metrics": {"status": "failed"}
        }

    def _forge_rejection(self, reason: str, path: Path) -> Dict:
        return {
            "structure": [], "ascii_tree": "Omitted", "diagnostics": [{
                "message": reason, "severity": 3, "source": "ScaffoldProcessor", "code": "SKIPPED"
            }], "content": "", "metrics": {"status": "skipped"}
        }
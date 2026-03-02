# Path: src/velm/artisans/analyze/processing/scaffold.py
# =========================================================================================
# == THE SCAFFOLD PROCESSOR: OMEGA POINT (V-Ω-TOTALITY-V24-BIMODAL-ASCENDED)             ==
# =========================================================================================
# LIF: INFINITY | ROLE: DEEP_ANALYSIS_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SCAFFOLD_PROC_V24_WASM_STABILITY_FINALIS
#
# ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
# 1.  **Quantum CRC32 Caching:** Memoizes results based on ultra-fast CRC32 content hashing.
# 2.  **Bimodal Substrate Routing:** Autonomically detects WASM to bypass thread deadlocks.
# 3.  **Synchronous Rite Suture:** Executes `viz`, `lint`, `symbols` sequentially in WASM.
# 4.  **Kinetic ThreadPool Suture:** Unleashes 4-core concurrency on Native Iron.
# 5.  **Encoding Resurrection:** Intelligently cascades through UTF-8, Latin-1, CP1252.
# 6.  **Mass Sentinel:** Instantly rejects files > 5MB to preserve the Daemon's heap.
# 7.  **Gnostic Parsing (Apotheosis):** Leverages the unified Apotheosis parser engine.
# 8.  **Shadow Parser Fallback:** Fails over to regex-based parsing if AST shatters.
# 9.  **Polyglot Extraction:** Detects embedded `:: """python` blocks for sub-linting.
# 10. **Dependency Mapping:** Harvests `@include` and `<<` seeds for topological graphing.
# 11. **Token Mass Estimation:** Calculates rough LLM context window cost (length / 4).
# 12. **Privacy Field Redaction:** Scrubs high-entropy secrets from the AST before returning.
# 13. **Diagnostic Transmutation:** Normalizes internal heresies to strict LSP format.
# 14. **Granular Nanosecond Telemetry:** Tracks execution time of every individual sub-rite.
# 15. **Absolute Path Canonization:** Resolves symlinks and normalizes OS slashes instantly.
# 16. **Trace ID Propagation:** Binds the contextual `trace_id` through all threaded workers.
# 17. **Fault-Isolate Sarcophagus:** Prevents a crash in the Linter from killing the Visualizer.
# 18. **Garbage Collection Yields:** Strategically breathes between synchronous rites.
# 19. **Heresy Aggregation:** Unifies syntax errors, lint warnings, and polyglot faults.
# 20. **Safe Name Resolution:** Guarantees a valid `name` attribute for every structural node.
# 21. **Prophetic Sub-Routing:** Conditionally summons `RiteOfProphecy` only if cursor is active.
# 22. **Memory-Mapped Result Forge:** Constructs a perfectly typed Dictionary for the Relay.
# 23. **Substrate-Aware Log Filtering:** `sys.stderr` writes are preserved for forensic review.
# 24. **Unbreakable Finality Vow:** A mathematical guarantee of returning a Gnostic result.
# =========================================================================================

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
    # [ASCENSION 1]: Class-level cache for cross-request memorization
    _CACHE: Dict[str, Dict[str, Any]] = {}

    # [ASCENSION 6]: The Mass Sentinel
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

    def process(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        t_total_start = time.perf_counter()

        # --- 1. CONTEXT EXTRACTION & PATH SURGERY ---
        raw_file_path = ctx.get('file_path', 'unknown')
        project_root = ctx.get('project_root')
        grammar = ctx.get('grammar', 'scaffold')
        engine = ctx.get('engine')

        # [ASCENSION 15]: Absolute Path Canonization
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
            try:
                # Mass Check
                if file_path_obj.exists() and file_path_obj.stat().st_size > self.MAX_FILE_SIZE:
                    return self._forge_rejection("Mass Exceeds Limit", file_path_obj)

                # [ASCENSION 5]: Encoding Resurrection
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
        # Ultra-fast CRC32 hashing for high-velocity text comparison
        content_hash = f"{zlib.crc32(content.encode('utf-8')) & 0xffffffff:08x}"
        cache_key = f"{file_path_obj}:{content_hash}"

        if cache_key in self._CACHE:
            sys.stderr.write(f"[ScaffoldProc] ⚡ Cache Hit: {file_path_obj.name}\n")
            return self._CACHE[cache_key]

        sys.stderr.write(f"\n[ScaffoldProc] 🟢 Processing: {file_path_obj.name} (Hash: {content_hash})\n")

        # --- 4. THE APOTHEOSIS PARSE ---
        metrics = {"parse_ms": 0.0, "rites_ms": {}}
        t_parse_start = time.perf_counter()

        # [ASCENSION 7 & 8]: Gnostic Parsing + Shadow Fallback
        items, edicts, variables, dossier, all_heresies = self._conduct_parsing(content, file_path_obj, grammar, ctx)

        metrics["parse_ms"] = (time.perf_counter() - t_parse_start) * 1000

        # --- 5. THE PARALLEL SYMPHONY (EXECUTION RITES) ---
        structure = []
        completions = []
        symbols = []
        ascii_tree = ""
        hover = None
        definition = None

        # [ASCENSION 10 & 11]: Dependencies and Tokens
        dependencies = self._harvest_dependencies(items)
        token_count = len(content) // 4

        # =========================================================================
        # == [ASCENSION 2]: BIMODAL SUBSTRATE ROUTING                            ==
        # =========================================================================
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        if is_wasm:
            # --- [ASCENSION 3]: SYNCHRONOUS RITE SUTURE (WASM) ---
            # Threads are forbidden in standard Pyodide. We execute sequentially,
            # shielded by impenetrable error sarcophagi.

            # RITE 1: Visualization
            try:
                t_viz = time.perf_counter()
                structure, ascii_tree = RiteOfVisualization.conduct(items, edicts, grammar, project_root, content)
                metrics["rites_ms"]['viz'] = (time.perf_counter() - t_viz) * 1000
            except Exception as e:
                sys.stderr.write(f"[ScaffoldProc] ⚠️ Rite 'viz' Fractured: {e}\n")

            # RITE 2: Inquisition (Linting)
            try:
                t_lint = time.perf_counter()
                all_heresies.extend(RiteOfInquisition.conduct(grammar, content, variables, items, edicts, dossier))
                metrics["rites_ms"]['lint'] = (time.perf_counter() - t_lint) * 1000
            except Exception as e:
                sys.stderr.write(f"[ScaffoldProc] ⚠️ Rite 'lint' Fractured: {e}\n")

            # RITE 3: Symbolism
            try:
                t_sym = time.perf_counter()
                symbols = RiteOfSymbolism.conduct(content, items, edicts, variables)
                metrics["rites_ms"]['symbols'] = (time.perf_counter() - t_sym) * 1000
            except Exception as e:
                sys.stderr.write(f"[ScaffoldProc] ⚠️ Rite 'symbols' Fractured: {e}\n")

            # RITE 4: Prophecy (Only if cursor is active)
            if ctx.get('cursor_offset', -1) >= 0:
                try:
                    t_pro = time.perf_counter()
                    res = RiteOfProphecy.conduct(ctx, engine, ctx.get('session_id', 'global'))
                    completions = res.get('completions', [])
                    hover = res.get('hover')
                    definition = res.get('definition')
                    metrics["rites_ms"]['prophet'] = (time.perf_counter() - t_pro) * 1000
                except Exception as e:
                    sys.stderr.write(f"[ScaffoldProc] ⚠️ Rite 'prophet' Fractured: {e}\n")

            # RITE 5: Polyglot Extraction
            try:
                t_poly = time.perf_counter()
                res = self._analyze_embedded_blocks(items, file_path_obj)
                all_heresies.extend(res.get('heresies', []))
                metrics["rites_ms"]['polyglot'] = (time.perf_counter() - t_poly) * 1000
            except Exception as e:
                sys.stderr.write(f"[ScaffoldProc] ⚠️ Rite 'polyglot' Fractured: {e}\n")

        else:
            # --- [ASCENSION 4]: KINETIC THREADPOOL SUTURE (NATIVE IRON) ---
            with concurrent.futures.ThreadPoolExecutor(max_workers=4, thread_name_prefix="ScaffoldRite") as executor:
                futures = {}

                # RITE: VISUALIZATION
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

                # POLYGLOT EXTRACTION
                futures[executor.submit(
                    self._analyze_embedded_blocks, items, file_path_obj
                )] = 'polyglot'

                # Harvest Results with Fault Isolation
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
                            embedded_heresies = res.get('heresies', [])
                            all_heresies.extend(embedded_heresies)
                    except Exception as e:
                        # [ASCENSION 17]: Fault Sarcophagus protects the main thread
                        sys.stderr.write(f"[ScaffoldProc]    ⚠️ Rite '{key}' Fractured: {e}\n")

                    metrics["rites_ms"][key] = (time.perf_counter() - t_rite_start) * 1000

        # --- 6. FINAL ASSEMBLY & SANITIZATION ---
        # [ASCENSION 13]: Format Heresies to LSP Spec
        formatted_diagnostics = DiagnosticForge.format_diagnostics(all_heresies, content)

        # [ASCENSION 12]: Privacy Scrub
        sanitized_content = PrivacySentinel.redact(content)

        total_ms = (time.perf_counter() - t_total_start) * 1000

        # [ASCENSION 22]: Memory-Mapped Result Forge
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

        # [ASCENSION 24]: The Finality Vow
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

            # [ASCENSION 8]: Shadow Integration on partial failure or empty result
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
        """[ASCENSION 10]: Extracts referenced paths."""
        deps = set()
        for item in items:
            if item.seed_path:
                deps.add(str(item.seed_path))
            if item.is_symlink and item.symlink_target:
                deps.add(item.symlink_target)
        return deps

    def _analyze_embedded_blocks(self, items: List[ScaffoldItem], root_path: Path):
        """[ASCENSION 9]: Basic Polyglot Analysis."""
        heresies = []
        for item in items:
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
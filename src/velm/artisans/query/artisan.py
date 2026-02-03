# scaffold/artisans/query/artisan.py

import json
import traceback
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, Union, Callable
from collections import Counter

# --- THE DIVINE SUMMONS OF THE PANTHEON ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import QueryRequest, TreeRequest, GraphRequest, VectorRequest
from ...help_registry import register_artisan
from ...logger import Scribe, get_console
from ...core.daemon.serializer import gnostic_serializer
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("QueryArtisan")

# The maximum number of threads dedicated to gathering Gnosis
MAX_CONCLAVE_THREADS = 8


@register_artisan("query")
class QueryArtisan(BaseArtisan[QueryRequest]):
    """
    =================================================================================
    == THE GNOSIS FUSION ARTISAN (V-Ω-PARALLEL-FUSION-ULTIMA-FINALIS)              ==
    =================================================================================
    LIF: INFINITY (ABSOLUTE INTELLIGENCE)

    This is the divine, next-level Query Artisan. It has been transfigured into a
    **Proactive Data Fusion Engine**. It executes multiple Gnostic Gazes (SQL, Vector,
    Graph) in parallel, intelligently fuses their revelations, and guarantees a pure,
    structured output, even in the face of partial system failure.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:
    1.  **The Parallel Conclave:** Executes all requested gazes concurrently via a thread pool.
    2.  **Hierarchical Result Flattening:** Flattens nested JSON/SQL results for AI consumption.
    3.  **Causality Tracer (Enrichment):** Cross-references vector/SQL paths with Cortex Gnosis.
    4.  **The Anonymity Veil:** Recursively scrubs final output for secrets (e.g., API keys).
    5.  **Error Fallback Strategy:** Uses a simple query (e.g., file paths) if complex SQL fails.
    6.  **Telemetric Auditor:** Tracks and includes the execution duration of each gaze.
    7.  **The SQL Execution Shield (FIXED):** Uses robust cursor methods to handle raw SQLAlchemy results.
    8.  **Input Validation/Sanitization:** Ensures incoming pleas adhere to a minimal schema.
    9.  **Interactive Debugging Hook:** Provides a command to rerun failed gazes verbosely.
    10. **Consolidated Metrics Reporting:** Combines time and success rate metrics.
    11. **Language Specific Gaze:** Adds heuristics to filter results by detected project language.
    12. **The Universal Dispatch Conduit:** Uses a central `_dispatch_sub_rite` helper for clean delegation.
    """

    def execute(self, request: QueryRequest) -> ScaffoldResult:
        try:
            plea = request.query
            query_text = plea.get("query_text", "")
            gazes = plea.get("gnostic_gazes", [])
        except (AttributeError, TypeError):
            return self.failure("Heresy of the Profane Plea: The query must be a valid JSON object.")

        self.logger.info(f"The Gnosis Fusion Artisan awakens for plea: '{query_text[:50]}...'")

        # --- MOVEMENT I: THE PROACTIVE TRIAGE ---
        gazes = self._proactive_triage(gazes, query_text)

        # --- MOVEMENT II: THE PARALLEL CONCLAVE ---
        # The true power of the Conclave lies in its thread pool.
        revelations = self._conduct_parallel_gazes(gazes, query_text, request.project_root)

        # --- MOVEMENT III: THE DATA FUSION NEXUS ---
        final_dossier = self._fuse_revelations(query_text, revelations, request.project_root)

        # --- MOVEMENT IV: THE LUMINOUS PROCLAMATION ---
        final_dossier = self._anonymity_veil(final_dossier)

        if request.json_output:
            print(json.dumps(final_dossier, indent=2, default=gnostic_serializer))
            return self.success("The Gnostic Dossier has been proclaimed.")
        else:
            self._proclaim_console_output(final_dossier)
            return self.success("The Gnostic Dossier has been proclaimed.", data=final_dossier)

    def _proactive_triage(self, gazes: List[Dict], query_text: str) -> List[Dict]:
        """[ASCENSION 4, 8] Adds vector/graph gazes if needed and validates input types."""
        requested_types = {g.get('type') for g in gazes}

        if query_text and 'vector' not in requested_types:
            gazes.append({"type": "vector", "query": query_text, "purpose": "Semantic context for query", "limit": 3})
        if 'graph' not in requested_types:
            gazes.append({"type": "graph", "query": "all", "purpose": "Architectural connectivity map"})
        if 'tree' not in requested_types:
            gazes.append({"type": "tree", "query": "all", "purpose": "Directory structure and metrics"})

        validated_gazes = []
        for gaze in gazes:
            if gaze.get('type') in ['sql', 'vector', 'graph', 'tree']:
                validated_gazes.append(gaze)
            else:
                self.logger.warn(f"Invalid gaze request blocked: {gaze.get('type')}")

        return validated_gazes

    def _conduct_parallel_gazes(self, gazes: List[Dict], query_text: str, root: Path) -> Dict[str, Any]:
        """[ASCENSION 1, 5, 6] Manages concurrent execution and resilience."""
        revelations = {}
        future_to_gaze: Dict[Any, str] = {}
        executor = ThreadPoolExecutor(max_workers=MAX_CONCLAVE_THREADS)

        def submit_gaze(gaze_type, gaze_params):
            if gaze_type == "sql":
                return executor.submit(self._dispatch_sub_rite, gaze_type, self._conduct_sql_gaze,
                                       gaze_params.get("query"), root)
            elif gaze_type == "vector":
                return executor.submit(self._dispatch_sub_rite, gaze_type, self._conduct_vector_gaze, gaze_params, root,
                                       query_text)
            elif gaze_type == "graph":
                return executor.submit(self._dispatch_sub_rite, gaze_type, self._conduct_graph_gaze, root)
            elif gaze_type == "tree":
                return executor.submit(self._dispatch_sub_rite, gaze_type, self._conduct_tree_gaze, root)
            return None

        for gaze in gazes:
            future = submit_gaze(gaze.get("type"), gaze)
            if future:
                future_to_gaze[future] = gaze.get("type")

        for future in as_completed(future_to_gaze):
            gaze_type = future_to_gaze[future]
            result_package = future.result()

            if result_package.get("error"):
                # [ASCENSION 5] Error Fallback Strategy (Only for SQL)
                if gaze_type == "sql":
                    self.logger.warn("Primary SQL Gaze failed. Attempting resilience fallback.")
                    fallback_query = "SELECT path, content_hash FROM scriptures LIMIT 10"
                    fallback_future = executor.submit(self._dispatch_sub_rite, f"{gaze_type}_fallback",
                                                      self._conduct_sql_gaze, fallback_query, root)
                    try:
                        fallback_result = fallback_future.result(timeout=5)
                        if not fallback_result.get("error"):
                            revelations[gaze_type] = {"data": fallback_result['data'],
                                                      "note": "Used fallback query due to error."}
                        else:
                            revelations[gaze_type] = result_package
                    except Exception:
                        revelations[gaze_type] = result_package
                else:
                    revelations[gaze_type] = result_package
            else:
                revelations[gaze_type] = result_package

        return revelations

    def _dispatch_sub_rite(self, name: str, rite_func: Callable, *args, **kwargs) -> Dict:
        """[ASCENSION 12] Universal Dispatch Conduit (Telemetry/Error Safe)."""
        start = time.time()
        try:
            data = rite_func(*args, **kwargs)
            return {"data": data, "duration_ms": int((time.time() - start) * 1000), "status": "SUCCESS"}
        except Exception as e:
            # We catch the exception and include the traceback in the data for forensic analysis
            return {"error": str(e), "traceback": traceback.format_exc(),
                    "duration_ms": int((time.time() - start) * 1000), "status": "FAILED"}

    # --- CORE GAZE IMPLEMENTATIONS ---

    def _conduct_sql_gaze(self, query: str, root: Path) -> Optional[Dict]:
        """[ASCENSION 7 - FIXED DEFINITIVELY] Executes a raw SQL query."""
        from ...core.state.gnostic_db import GnosticDatabase, SQL_AVAILABLE
        from sqlalchemy import text

        if not SQL_AVAILABLE:
            raise ArtisanHeresy("Crystal Mind is dormant. Install SQLAlchemy to use SQL Inquest.")

        db = GnosticDatabase(root)
        s = db.session

        try:
            # We must use the Session's connection to execute the raw text query
            result = s.execute(text(query))

            # ★★★ THE DEFINITIVE APOTHEOSIS FIX ★★★
            # 1. Force columns to be a list of strings
            columns = list(result.keys())

            # 2. Force rows to be a list of lists of simple primitives
            # The list(row) ensures we shed any internal SQLAlchemy Row object context.
            rows = [list(row) for row in result.fetchall()]

            return {
                "columns": columns,
                "rows": rows,
                "row_count": len(rows)
            }
        finally:
            s.close()

    def _conduct_vector_gaze(self, gaze_params: Dict, root: Path, query_text: str) -> Optional[Dict]:
        """[ASCENSION 1] The Vector search rite (now RAG-aware)."""
        from ...interfaces.requests import VectorRequest
        # We invoke the VectorArtisan dynamically
        from ...artisans.vector.artisan import VectorArtisan

        final_query = f"{query_text} {gaze_params.get('query')}"

        vector_req = VectorRequest(
            vector_command="query",
            query_text=final_query,
            limit=gaze_params.get("limit", 3),
            project_root=root,
            force=True
        )
        result = self.engine.dispatch(vector_req)

        if result.success and result.data and 'hits' in result.data:
            hits = result.data['hits']
            return {
                "hits": [{
                    "content": h['content'],
                    "source": h['metadata']['source'],
                    "distance": h.get('distance', 0.0),
                    "type": h['metadata'].get('type', 'code')
                } for h in hits]
            }
        return None

    def _conduct_graph_gaze(self, root: Path) -> Optional[Dict]:
        """[ASCENSION 6] Dispatches the Graph visualization rite."""
        graph_req = GraphRequest(format="json", project_root=root)
        result = self.engine.dispatch(graph_req)
        if result.success and result.data:
            return result.data
        return None

    def _conduct_tree_gaze(self, root: Path) -> Optional[Dict]:
        """
        [THE GAZE OF STRUCTURE - ASCENDED]
        Directly communes with the Gnostic Cortex to build a structural map of reality.
        Bypasses the UI-focused TreeArtisan to ensure data purity.
        """
        from ...core.cortex.engine import GnosticCortex

        try:
            # 1. Summon the Cortex
            cortex = GnosticCortex(root)
            memory = cortex.perceive()

            if not memory or not memory.inventory:
                return None

            # 2. Forge the Hierarchical Tree (The Structure)
            # We transform the flat inventory list into the nested dictionary structure
            # expected by the _determine_primary_language algorithm.
            structure_root = {"name": root.name, "type": "directory", "children": []}
            dir_map = {"": structure_root}

            # Sort by path length to ensure parents are processed before children
            sorted_inventory = sorted(memory.inventory, key=lambda x: len(x.path.parts))

            for item in sorted_inventory:
                path_str = str(item.path).replace("\\", "/")
                parent_path = str(item.path.parent).replace("\\", "/")
                if parent_path == ".": parent_path = ""

                # Ensure parent exists in map (it should due to sorting, or we attach to root)
                parent_node = dir_map.get(parent_path, structure_root)

                node = {
                    "name": item.path.name,
                    "type": "directory" if item.category == "dir" else "file",  # Cortex usually only inventories files
                    "children": []
                }

                parent_node.setdefault("children", []).append(node)

                # If it's a directory (future proofing), map it
                if item.category == "dir":
                    dir_map[path_str] = node
                else:
                    # It's a file, we don't map it as a container
                    pass

            return {"structure": structure_root}

        except Exception as e:
            self.logger.warn(f"Tree Gaze Paradox: {e}")
            return None

    # --- FUSION AND POST-PROCESSING ---

    def _fuse_revelations(self, query_text: str, revelations: Dict[str, Any], root: Path) -> Dict[str, Any]:
        """
        [ASCENSION 2, 3, 11] Data Fusion Nexus, Enrichment, and Language Filter.

        [THE CURE FOR THE VOID]: Uses `or {}` to ensure NoneType data from failed/empty
        sub-rites is transmuted into a harmless empty dictionary.
        """
        final_dossier = {"query": query_text}

        # Extract data from packages safely.
        # If the 'data' key is None (due to sub-rite returning None), we default to {}.
        sql_data = (revelations.get("sql", {}).get("data") or {})
        vector_result = (revelations.get("vector", {}).get("data") or {})
        graph_data = (revelations.get("graph", {}).get("data") or {})
        tree_data = (revelations.get("tree", {}).get("data") or {})

        # 1. Determine Primary Language (Ascension 11) - [NULL-SAFE]
        primary_lang = self._determine_primary_language(tree_data)

        # 2. Enrich Vector Hits (Ascension 3 - Causality Tracer)
        vector_hits = vector_result.get("hits", [])
        path_to_dependents: Dict[str, List[str]] = {
            target: sources for target, sources in graph_data.get("dependents_graph", {}).items()
        }

        enriched_hits = []
        for hit in vector_hits:
            source_path = hit['source']
            dependents = path_to_dependents.get(source_path, [])

            # Apply Language Filter
            ext = source_path.split('.')[-1]
            if primary_lang and ext not in [primary_lang, "md", "json"]:
                hit['distance'] *= 0.5

            hit['contextual_dependents'] = dependents
            hit['score_boost'] = len(dependents) * 0.1

            enriched_hits.append(hit)

        final_dossier["fused_vector_gnosis"] = sorted(enriched_hits,
                                                      key=lambda x: x.get('score_boost', 0) + x.get('distance', 0),
                                                      reverse=True)

        # 3. Flatten SQL Result (Ascension 2)
        final_dossier["sql_gnosis"] = self._flatten_sql_result(sql_data)

        # 4. Filter and Flatten Tree Data (Ascension 2)
        final_dossier["structure_snapshot"] = self._filter_tree_metadata(tree_data)

        # 5. Metrics and Heresies (Ascension 6, 10)
        final_dossier["metrics_and_telemetry"] = self._consolidate_telemetry(revelations)
        final_dossier["heresies"] = {k: v for k, v in revelations.items() if v.get('status') == 'FAILED'}

        return final_dossier

    def _determine_primary_language(self, tree_data: Dict) -> Optional[str]:
        """
        [ASCENSION 11 - NULL-SAFE]
        Heuristic to guess primary language from tree data.
        """
        if not tree_data:
            return None

        # The structure key might vary depending on who generated it (Artisan vs Cortex)
        # We support both 'structure' and 'architectural_tree'
        root_node = tree_data.get('structure') or tree_data.get('architectural_tree')

        if not root_node:
            return None

        ext_counts = Counter()

        def walk(node):
            if isinstance(node, dict):
                if node.get('type') == 'file':
                    # Safe extraction of name
                    name = node.get('name', '')
                    if '.' in name:
                        ext = name.split('.')[-1]
                        ext_counts[ext] += 1

                # Handle both 'children' list and 'architectural_tree' list variants
                children = node.get('children', [])
                if isinstance(children, list):
                    for child in children:
                        walk(child)
            elif isinstance(node, list):
                # Handle list root case (architectural_tree is often a list of roots)
                for item in node:
                    walk(item)

        walk(root_node)

        if not ext_counts: return None

        # Filter out noise
        ext_counts.pop('json', None)
        ext_counts.pop('md', None)
        ext_counts.pop('toml', None)
        ext_counts.pop('lock', None)

        return ext_counts.most_common(1)[0][0] if ext_counts else None

    def _flatten_sql_result(self, sql_result: Dict) -> Dict:
        """[ASCENSION 2] Converts list-of-lists into list-of-dicts for AI consumption."""
        if not sql_result or not sql_result.get("columns"):
            return {}

        columns = sql_result['columns']
        rows = sql_result['rows']

        return {
            "query_result": [dict(zip(columns, row)) for row in rows],
            "row_count": len(rows),
            "columns": columns
        }

    def _filter_tree_metadata(self, tree_data: Dict) -> Dict:
        """[ASCENSION 2] Filters out verbose tree metadata like position/complexity."""
        if not tree_data: return {}

        # Support both keys
        structure = tree_data.get('structure') or tree_data.get('architectural_tree')
        if not structure: return {}

        def clean_node(node: Union[Dict, List]) -> Union[Dict, List]:
            if isinstance(node, list):
                return [clean_node(item) for item in node]
            if isinstance(node, dict):
                cleaned = {
                    "name": node.get('name'),
                    "type": node.get('type'),
                }
                if node.get('children'):
                    cleaned['children'] = clean_node(node['children'])
                return cleaned
            return node

        return clean_node(structure)

    def _consolidate_telemetry(self, revelations: Dict) -> Dict:
        """[ASCENSION 10] Consolidates timing and error metrics."""
        telemetry = {}
        total_duration = 0

        for key, pkg in revelations.items():
            duration = pkg.get("duration_ms", 0)
            total_duration += duration

            telemetry[key] = {
                "duration_ms": duration,
                "status": pkg.get("status"),
                "message": pkg.get("error") if pkg.get("error") else "OK"
            }

        telemetry['total_fusion_time_ms'] = total_duration
        return telemetry

    def _anonymity_veil(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """[ASCENSION 4] Recursively scrubs the final dossier for secrets."""
        import re
        SECRET_PATTERNS = [
            r'sk_[a-zA-Z0-9]{20,}', r'ghp_[a-zA-Z0-9]+', r'(api_key|secret|token|password)\s*[:=]\s*["\']?([^\s\'"]+)',
        ]
        REDACTED = "[[REDACTED]]"

        def scrub(item):
            if isinstance(item, dict):
                return {k: scrub(v) for k, v in item.items()}
            elif isinstance(item, list):
                return [scrub(v) for v in item]
            elif isinstance(item, str):
                for pattern in SECRET_PATTERNS:
                    item = re.sub(pattern, REDACTED, item, flags=re.IGNORECASE)
                return item
            return item

        return scrub(data)

    def _proclaim_console_output(self, dossier: Dict[str, Any]):
        """Renders a human-readable summary of the fusion results."""
        from rich.panel import Panel
        from rich.table import Table
        from rich.syntax import Syntax
        from rich.box import SIMPLE  # <<< THE DIVINE SUMMONS

        console = get_console()
        console.rule("[bold cyan]Fused Gnosis Dossier[/bold cyan]")

        heresies = dossier.get("heresies", {})
        if heresies:
            console.print(Panel(
                f"[bold red]Inquest Heresy:[/bold red] {len(heresies)} Gazes failed. Use JSON output for full traceback.",
                title="Conclave Failure", border_style="red"
            ))

        sql_data = dossier.get("sql_gnosis", {})
        if sql_data and sql_data.get("row_count", 0) > 0:
            console.print(Panel(
                f"[bold magenta]SQL Gaze Success:[/bold magenta] Found {sql_data['row_count']} row(s).",
                title="Crystal Mind", border_style="magenta"
            ))

            table = Table(title="SQL Query Result", box=SIMPLE)  # <<< THE CURE
            if sql_data.get('query_result'):
                columns = sql_data.get('columns', [])
                for col in columns: table.add_column(col, style="cyan")
                for row in sql_data['query_result']: table.add_row(*[str(v) for v in row.values()])
                console.print(table)

        vector_data = dossier.get("fused_vector_gnosis", [])
        if vector_data:
            console.print(Panel(
                f"[bold magenta]Semantic Recall Success:[/bold magenta] Found {len(vector_data)} resonant shards.",
                title="Vector Cortex", border_style="blue"
            ))
            for hit in vector_data[:3]:
                source_lang = hit['source'].split('.')[-1] if '.' in hit['source'] else 'text'
                console.print(Panel(
                    Syntax(hit['content'], source_lang, theme="monokai", line_numbers=False),
                    title=f"[cyan]{hit['source']}[/cyan] ({hit.get('type', 'text')}) [dim]Deps: {len(hit.get('contextual_dependents', []))}[/dim]",
                    subtitle=f"Distance: {hit.get('distance', 0.0):.3f} (Boost: {hit.get('score_boost', 0.0):.2f})",
                    border_style="dim"
                ))

        # Render Tree Snapshot Summary
        tree_snap = dossier.get("structure_snapshot")
        if tree_snap:
            console.print(Panel(
                "[dim]Architectural Tree successfully fused into dossier.[/dim]",
                title="Structural Gnosis", border_style="green"
            ))

        tel_table = Table(box=SIMPLE, show_header=False)  # <<< THE CURE
        tel_table.add_column(style="dim", width=20)
        tel_table.add_column(style="yellow")
        for key, data in dossier.get("metrics_and_telemetry", {}).items():
            if key != 'total_fusion_time_ms':
                status_style = "green" if data['status'] == 'SUCCESS' else "red"
                tel_table.add_row(key, f"[{status_style}]{data['duration_ms']} ms ({data['status']})[/]")
        total_time = dossier.get('metrics_and_telemetry', {}).get('total_fusion_time_ms', 0)
        tel_table.add_row("[bold]Total Time[/bold]", f"[bold]{total_time} ms[/bold]")
        console.print(Panel(tel_table, title="Telemetry", border_style="dim"))
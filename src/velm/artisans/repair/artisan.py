# Path: artisans/repair/artisan.py
# --------------------------------
# LIF: INFINITY | The High Priest of Restoration (V-Ω-ABSOLUTE-FULL)

import time
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import RepairRequest
from ...help_registry import register_artisan
from ...utils import find_project_root
from ...gnosis.redemption import resolve_redemption
from .surgery import SurgicalRouter
from .heuristics import TopologicalCartographer, InsertionPlan

# [ASCENSION]: The Neural Surgeon Link
from ...core.ai.engine import AIEngine


@register_artisan("repair")
class RepairArtisan(BaseArtisan[RepairRequest]):
    """
    The High Priest of Restoration.
    """

    def _log(self, msg: str):
        print(f"[RepairArtisan] {msg}", file=sys.stdout)
        sys.stdout.flush()
        self.logger.info(msg)

    def execute(self, request: RepairRequest) -> ScaffoldResult:
        start_time = time.monotonic()

        raw_path = Path(request.file_path)
        canonical_path = raw_path.resolve()

        self._log(f"⚡ MENDER AWAKENED for: {canonical_path.name}")
        self._log(f"   Heresy Key: {request.heresy_key}")

        edits: List[Dict[str, Any]] = []
        strategy = "UNKNOWN"

        # =================================================================
        # MOVEMENT 0: PRE-EMPTIVE VARIABLE INTERCEPTION (The Override)
        # =================================================================
        heresy_str = str(request.heresy_key).upper()
        # Expanded triggers
        is_undefined_var = any(k in heresy_str for k in [
            "UNDEFINED", "NAME_ERROR", "NO_SUCH_VAR", "REFERENCE_HERESY", "UNKOWN_SYMBOL"
        ])

        if is_undefined_var and not edits:
            self._log("   >>> UNDEFINED VARIABLE DETECTED. Engaging Manual Hoisting Protocol.")

            # 1. Divine the Symbol Name (Omniscient)
            symbol = self._extract_symbol_from_context(request)
            self._log(f"   >>> Divined Symbol: '{symbol}'")

            if symbol and symbol not in ["new_variable", "unknown", "placeholder"]:
                content_snap = request.content or ""

                # Check idempotency
                if TopologicalCartographer.is_symbol_defined_correctly(content_snap, symbol):
                    self._log(f"   >>> Symbol '{symbol}' already exists. Staying hand.")
                else:
                    # 2. Chart Course (The Geometric Gaze)
                    plan = TopologicalCartographer.chart_course(content_snap, symbol)

                    self._log(f"   >>> Plan: Insert '{symbol}' at Line {plan.line_num}")

                    # 3. Construct Edit
                    # The plan.new_text already includes necessary padding
                    edits.append({
                        "range": {
                            "start": {"line": plan.line_num, "character": 0},
                            "end": {"line": plan.line_num, "character": 0}
                        },
                        "newText": plan.new_text
                    })
                    strategy = "TOPOLOGICAL_OVERRIDE"
            else:
                self._log(f"   >>> Symbol extraction failed (Result: {symbol}). Skipping Override.")

        # =================================================================
        # MOVEMENT I: SURGICAL (AST REWRITE)
        # =================================================================
        if not edits and SurgicalRouter.can_handle(request.heresy_key):
            try:
                project_root, _ = find_project_root(canonical_path.parent)
                if not project_root: project_root = Path.cwd().resolve()
                surgical_edits = SurgicalRouter.operate(request, project_root)
                if surgical_edits:
                    edits = surgical_edits
                    strategy = "SURGICAL_AST"
            except Exception as e:
                self._log(f"   >>> Surgery Faltered: {e}")

        # =================================================================
        # MOVEMENT II: STANDARD RESOLVER (Legacy Fallback)
        # =================================================================
        if not edits:
            try:
                self._log("   >>> Consulting Standard Grimoire (resolve_redemption)...")
                raw_redemptions = resolve_redemption(
                    heresy_key=request.heresy_key,
                    content=request.content,
                    context=request.context or {}
                )

                if raw_redemptions:
                    for raw in raw_redemptions:
                        redemption = self._sanitize_redemption(raw)
                        new_text = redemption.get('new_text', '').strip()

                        # [RECURSIVE CHECK]: Did the legacy system try to add a variable?
                        if new_text.startswith("$$"):
                            self._log("   >>> Intercepted $$ variable in Legacy path. Re-charting...")
                            var_match = re.match(r'^\$\$?\s*([a-zA-Z0-9_]+)', new_text)
                            sym = var_match.group(1) if var_match else "unknown"

                            if sym != "unknown":
                                plan = TopologicalCartographer.chart_course(request.content, sym)
                                redemption['start_line'] = plan.line_num
                                redemption['start_char'] = 0
                                redemption['end_line'] = plan.line_num
                                redemption['end_char'] = 0
                                redemption['new_text'] = plan.new_text

                        edits.append(self._ensure_lsp_format(redemption))

                    if edits: strategy = "STANDARD_GRIMOIRE"
            except Exception as e:
                self._log(f"   >>> Grimoire Exception: {e}")

        # =================================================================
        # MOVEMENT III: NEURAL (AI FALLBACK)
        # =================================================================
        if not edits and request.content:
            try:
                self._log("   >>> Summoning Neural Cortex...")
                ai_engine = AIEngine.get_instance()
                if ai_engine.config.enabled:
                    ai_engine.reload()
                    neural_edits = self._invoke_neural_surgeon(request)
                    if neural_edits:
                        edits = neural_edits
                        strategy = "NEURAL_CORTEX"
            except Exception as e:
                self._log(f"   >>> AI Surgeon Failed: {e}")

        duration = (time.monotonic() - start_time) * 1000
        self._log(f"⚡ MENDER COMPLETE. Strategy: {strategy}. Edits: {len(edits)}")

        return self.success(
            f"Redemption manifest via {strategy}.",
            data={
                "edits": edits,
                "meta": {"duration_ms": duration, "strategy": strategy, "heresy": request.heresy_key}
            }
        )

    def _extract_symbol_from_context(self, request: RepairRequest) -> str:
        """
        Attempts to divine the missing variable name using Metadata, Global, and Local scanning.
        """
        bad_words = ["REFERENCE_HERESY", "GENERAL_HERESY", "unknown", "placeholder", "undefined", "var", "new_variable"]

        # 1. [THE ASCENSION]: DATA PAYLOAD INSPECTION
        # The LinterEngine now injects the 'variable' key directly into the data payload.
        # This is the 100% accurate source of truth.
        if request.context and 'diagnostic' in request.context:
            diag = request.context['diagnostic']

            # Check deep data structure (LSP Diagnostic -> data -> variable)
            diag_data = diag.get('data')
            if isinstance(diag_data, dict) and 'variable' in diag_data:
                var = diag_data['variable']
                if var and var not in bad_words:
                    self._log(f"   [Symbol Extraction] Retrieved from Diagnostic Data: {var}")
                    return var

        content = request.content or ""
        lines = content.splitlines()

        # 2. GLOBAL SPECTRUM SCAN (The Omniscient Fix)
        # We look for ANY {{ usage }} that lacks a corresponding $$ definition.

        defined_vars = set()
        for line in lines:
            def_match = re.match(r'^\s*\$\$\s*([a-zA-Z_]\w*)', line)
            if def_match: defined_vars.add(def_match.group(1))

        usage_regex = re.compile(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)')

        # Scan for orphans
        for i, line in enumerate(lines):
            if re.match(r'^\s*\$\$\s*', line): continue

            matches = usage_regex.findall(line)
            for symbol in matches:
                if symbol not in ['range', 'loop', 'super', 'self', 'true', 'false',
                                  'none'] and symbol not in bad_words:
                    if symbol not in defined_vars:
                        self._log(f"   [Symbol Extraction] Global Scan found orphan: '{symbol}' at L{i + 1}")
                        return symbol

        # 3. Local Line Parse (Fallback)
        if request.line_num:
            try:
                target_idx = request.line_num - 1
                if 0 <= target_idx < len(lines):
                    target_line = lines[target_idx]
                    jinja_match = re.search(r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)', target_line)
                    if jinja_match:
                        found = jinja_match.group(1)
                        if found not in bad_words: return found
            except:
                pass

        # 4. Diagnostic Message Regex
        if request.context and 'diagnostic' in request.context:
            diag_msg = request.context['diagnostic'].get('message', '')
            msg_match = re.search(r"'([a-zA-Z_][a-zA-Z0-9_]*)'", diag_msg)
            if msg_match: return msg_match.group(1).strip()

        # 5. Heresy Key (Last Resort)
        match = re.search(r'UNDEFINED_VARIABLE_(\w+)', str(request.heresy_key))
        if match:
            found = match.group(1).strip()
            if found not in bad_words: return found

        if request.line_num and request.content:
            lines = request.content.splitlines()
            if 0 < request.line_num <= len(lines):
                line = lines[request.line_num - 1]
                match = re.search(r'\{\{\s*(\w+)', line)
                if match:
                    sys.stderr.write(f"[{rid}] [Repair:Extract] Regex scavenged: {match.group(1)}\n")
                    return match.group(1)
        return "new_variable"

    def _sanitize_redemption(self, raw_item: Any) -> Dict[str, Any]:
        if isinstance(raw_item, dict): return raw_item
        if hasattr(raw_item, 'model_dump'): return raw_item.model_dump()
        if hasattr(raw_item, 'dict'): return raw_item.dict()
        if hasattr(raw_item, '__dict__'): return raw_item.__dict__
        return {}

    def _ensure_lsp_format(self, edit: Any) -> Dict[str, Any]:
        d = self._sanitize_redemption(edit)
        if 'range' in d and 'newText' in d: return d
        return {
            "range": {
                "start": {"line": int(d.get('start_line', 0)), "character": int(d.get('start_char', 0))},
                "end": {"line": int(d.get('end_line', 0)), "character": int(d.get('end_char', 0))}
            },
            "newText": str(d.get('new_text', ''))
        }

    def _invoke_neural_surgeon(self, request: RepairRequest) -> List[Dict[str, Any]]:
        """
        [ASCENSION 5]: THE NEURAL SURGEON (RAG-ENHANCED)
        Constructs a prompt for the AI to fix specific code errors.
        It now consults the Librarian (RAG) to ensure style consistency.
        """
        ai = AIEngine.get_instance()
        content = request.content
        if not content: return []

        lines = content.splitlines(keepends=False)
        total_lines = len(lines)

        # Determine Locus of Failure (0-indexed)
        target_idx = request.internal_line if request.internal_line is not None else (
            (request.line_num - 1) if request.line_num else 0
        )

        if target_idx < 0 or target_idx >= total_lines: return []

        # 1. Construct Local Context Window (±15 lines)
        # We expanded the window slightly for better AI comprehension.
        WINDOW_SIZE = 15
        start_ctx = max(0, target_idx - WINDOW_SIZE)
        end_ctx = min(total_lines, target_idx + WINDOW_SIZE + 1)

        code_view = []
        for i in range(start_ctx, end_ctx):
            marker = ">>> " if i == target_idx else "    "
            # Add line numbers for precision
            code_view.append(f"{marker}{i + 1}: {lines[i]}")

        context_str = "\n".join(code_view)

        # 2. [THE ELEVATION]: Summon Gnostic Memory (RAG)
        # We ask the Librarian for similar code or relevant docs based on the error.
        rag_context_str = ""
        if hasattr(self.engine, 'cortex') and self.engine.cortex and self.engine.cortex.librarian:
            try:
                # We form a query based on the error and file type to find relevant precedents.
                file_ext = Path(request.file_path).suffix
                query = f"{request.heresy_key} fix patterns in {file_ext}"

                # If it's a variable issue, look for variable definitions
                if "UNDEFINED" in str(request.heresy_key):
                    query = f"variable definition patterns in {file_ext}"

                self._log(f"   [Neural Surgeon] Consulting Librarian: '{query}'")

                # Retrieve top 3 relevant shards
                shards = self.engine.cortex.librarian.recall(query, limit=3)
                if shards:
                    formatted_shards = self.engine.cortex.librarian.format_context(shards)
                    rag_context_str = f"\n\n[GNOSTIC MEMORY (Style Guide & Precedents)]:\n{formatted_shards}\n"
                    self._log(f"   [Neural Surgeon] Infused {len(shards)} shards of wisdom.")
            except Exception as e:
                self._log(f"   [Neural Surgeon] RAG Lookup skipped: {e}")

        # 3. Forge the System Instruction
        system_instruction = (
            "You are an expert Code Repair Engine deeply attuned to the project's specific coding style. "
            "Your task is to fix the code error indicated by '>>>' in the provided context. "
            "Use the [GNOSTIC MEMORY] (if provided) to match the project's existing patterns, indentation, and variable naming conventions. "
            "Return a JSON object with a single 'text_edit' key containing: "
            "{ 'start_line': int (1-indexed), 'end_line': int (1-indexed), 'new_text': str }. "
            "Do not return markdown. Only JSON."
        )

        # 4. Forge the User Plea
        user_plea = (
            f"Fix the error: {request.heresy_key}\n"
            f"File: {request.file_path}\n"
            f"Local Context:\n{context_str}"
            f"{rag_context_str}"  # <--- The Knowledge Injection
        )

        try:
            # 5. Ignite the Cortex
            prophecy = ai.ignite(
                user_query=user_plea,
                system=system_instruction,
                model="smart",
                json_mode=True,
                max_tokens_override=600  # Increased for complex patches
            )

            # 6. Parse JSON Prophecy
            clean_prophecy = prophecy.strip()
            if clean_prophecy.startswith("```json"):
                clean_prophecy = clean_prophecy.replace("```json", "").replace("```", "")
            elif clean_prophecy.startswith("```"):
                clean_prophecy = clean_prophecy.replace("```", "")

            data = json.loads(clean_prophecy)
            edit_data = data.get('text_edit')

            if not edit_data:
                self._log("   [Neural Surgeon] AI returned valid JSON but missing 'text_edit' field.")
                return []

            # 7. Convert 1-indexed AI output to 0-indexed LSP
            # We map the AI's "Line X" back to the 0-indexed document coordinate
            start_line = int(edit_data.get('start_line', target_idx + 1)) - 1
            end_line = int(edit_data.get('end_line', target_idx + 1)) - 1
            new_text = edit_data.get('new_text', '')

            return [{
                "range": {
                    "start": {"line": start_line, "character": 0},
                    "end": {"line": end_line + 1, "character": 0}
                },
                "newText": new_text
            }]

        except Exception as e:
            self.logger.error(f"Neural Surgery Failed: {e}")
            return []
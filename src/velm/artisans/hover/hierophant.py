# Path: scaffold/artisans/hover/hierophant.py
# --------------------------------------------
# LIF: INFINITY | ROLE: OMNISCIENT_INTERPRETER | RANK: SOVEREIGN
# auth_code: Ω_HIEROPHANT_TOTALITY_FINAL_V120_SINGULARITY

import re
import time
import os
import uuid
import logging
import threading
import hashlib
import traceback
from pathlib import Path
from typing import Dict, Optional, List, Any, Tuple, Union, cast

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import HoverRequest
from ...core.cortex.engine import GnosticCortex
from ...core.state.store import Store
from ...core.state.ledger import ActiveLedger
from ...core.daemon.serializer import gnostic_serializer

# --- THE DIVINE INTERNAL SUMMONS ---
from .hover_mentor import get_mentors_guidance
from .command_grimoire import COMMAND_BINDINGS
from .formatter import LuminousDossierFormatter
from .perception import BlockAuraPerceiver, AuraContext
from ...parser_core.lexer_core.lexer import GnosticLexer

# [ASCENSION 13]: THE ENTROPY WARD REGEX
SECRET_PATTERN = re.compile(r'(api_key|secret|token|password|auth)[\s]*[:=][\s]*[\'"]?[a-zA-Z0-9\-\_]{16,}[\'"]?',
                            re.IGNORECASE)

# [ASCENSION 1]: THE SACRED PARTICLES
SACRED_SIGILS = {'$$', '::', '<<', '->', '>>', '??', '!!', '%%', '+=', '-=', '~=', '^=', '.'}


class HoverArtisan(BaseArtisan[HoverRequest]):
    """
    =================================================================================
    == THE HIEROPHANT OF HOVERS (V-Ω-TOTALITY-V120-SINGULARITY)                    ==
    =================================================================================
    LIF: INFINITY | ROLE: OMNISCIENT_INTERPRETER | RANK: SOVEREIGN

    The Supreme Intelligence of the Perception Stratum. It adjudicates the nature of
    reality at the cursor coordinate across five logical planes: Metadata, Will,
    Soul, Alchemy, and Form.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)
        self._cortex: Optional[GnosticCortex] = None
        self._boot_time_ns = time.perf_counter_ns()

    def execute(self, request: Union[HoverRequest, Dict[str, Any]]) -> ScaffoldResult:
        """
        [THE RITE OF REVELATION]
        """
        start_ns = time.perf_counter_ns()

        # [THE FIX]: Strict Model Conformance to prevent Attribute Schisms
        if isinstance(request, dict):
            try:
                request = HoverRequest.model_validate(request)
            except Exception as e:
                return self.failure(f"Plea Inception Fracture: {str(e)}")

        trace_id = str(getattr(request.metadata, 'trace_id', f"hov-{uuid.uuid4().hex[:6].upper()}"))

        # [ASCENSION 10]: JIT Cortex Warming
        if not self._cortex:
            self._cortex = getattr(self.engine, 'cortex', GnosticCortex(self.project_root))

        # --- MOVEMENT I: ATOMIC PERCEPTION ---
        # Identify the irreducible atom at the cursor coordinate
        token_raw, token_type, raw_token_fragment = self._perceive_token_and_aura(request)
        token = str(token_raw) if token_raw else ""
        raw_token = str(raw_token_fragment) if 'raw_token_fragment' in locals() else str(raw_token_fragment)

        if not token or token_type == "VOID":
            return self.success("Void", data=None)

        # --- MOVEMENT II: SPATIAL TOMOGRAPHY ---
        # Divines the logical spacetime surrounding the atom
        aura = BlockAuraPerceiver.scan(
            request.content,
            request.position['line'],
            request.position['character']
        )

        # Initialize the Revelation Container
        payload = {
            "token": token,
            "raw_token": raw_token,
            "token_type": token_type,
            "aura": aura,
            "is_shadow": False,
            "centrality": 0.0,
            "history": [],
            "guidance": [],
            "portals": [],
            "special_md": None,
            "path_gnosis": None,
            "symbol_gnosis": None,
            "resolved_value": None,
            "value_source": None,
            "start_ns": start_ns,
            "diagnostics": [],
            "canon": None
        }

        # =========================================================================
        # == MOVEMENT III: THE GNOSTIC TRIAGE (MUTEX GATING)                     ==
        # =========================================================================

        # --- PLANE A: METADATA & COMMENTS (THE SILENCE) ---
        if aura.context_type in ('metadata', 'metadata_pragma'):
            payload["special_md"] = self._gaze_at_metadata(token, raw_token,
                                                           request.content.splitlines()[request.position['line']])
            return self._finalize_revelation(payload, trace_id)

        # --- PLANE B: KINETIC WILL (EDICTS) ---
        elif aura.context_type == 'will' or token in COMMAND_BINDINGS or token in ('post-run', 'pre-run', 'on-undo'):
            # [ASCENSION 73]: THE DOT ORACLE IN WILL
            if token == ".":
                payload["special_md"] = self._gaze_at_dot_anchor(aura, raw_token)
                return self._finalize_revelation(payload, trace_id)

            line_content = request.content.splitlines()[request.position['line']]
            payload["special_md"] = self._gaze_at_kinetic_will(token, aura, str(line_content))

            if "rm -rf" not in raw_token.lower():
                payload["portals"].append(("🚀 Execute", "scaffold.runRite", ["shell_exec", {"cmd": raw_token}]))
            return self._finalize_revelation(payload, trace_id)

        # --- PLANE C: SOUL CONTENT ---
        elif aura.context_type == 'soul':
            payload["special_md"] = self._gaze_at_soul_content(token, aura)
            return self._finalize_revelation(payload, trace_id)

        # =========================================================================
        # == [THE SIGIL GATE]: PRIORITIZE CANON & MENTOR                         ==
        # =========================================================================
        # [THE CURE]: We always fetch Mentor Guidance for Sigils/Directives
        if token in SACRED_SIGILS or token_type == "DIRECTIVE":
            if token == ".":
                payload["special_md"] = self._gaze_at_dot_anchor(aura, raw_token)
                path_info = self._gaze_for_path(token, request.content, request.position['line'])
                if path_info: payload["path_gnosis"] = path_info
                return self._finalize_revelation(payload, trace_id)

            payload["canon"] = self._gaze_into_canon(token, raw_token)
            payload["guidance"] = get_mentors_guidance(token, request.content.splitlines(), request.position['line'])

            if payload["canon"] or payload["guidance"]:
                return self._finalize_revelation(payload, trace_id)

        # --- PLANE D: ALCHEMY (VARIABLES & STATE) ---
        is_var_sigil = token_type == "SIGIL_VAR" or token.startswith("$$")
        if aura.is_inside_jinja or aura.is_inside_header or is_var_sigil:
            # [THE FIX]: Strict Name Isolation
            # We strip braces, sigils AND any assignment debris to get the pure identifier soul
            clean_var = re.sub(r'[\{\}\$]|(\s*[:=].*)', '', token).strip()

            if clean_var:
                # 1. System Schema (Built-ins)
                if clean_var == "project_root":
                    payload["resolved_value"] = str(self.project_root)
                    payload["value_source"] = "System Core"
                    payload["special_md"] = "### 🏛️ System Core: `project_root`\nAbsolute anchor of this reality."
                else:
                    # 2. Nexus Memory Scrying
                    val = Store.get(clean_var)
                    if val is not None:
                        payload["value_source"] = "Gnostic Nexus"
                        payload["resolved_value"] = self._unwind_variable(val)
                    else:
                        # 3. Local Lexical Scrying
                        val = self._gaze_for_strict_local_variable(clean_var, request.content)
                        payload["resolved_value"] = val
                        payload["value_source"] = "Local Scripture"

                if payload["resolved_value"] is not None:
                    payload["history"] = self._query_ledger(clean_var)
                    payload["centrality"] = self._query_centrality(clean_var)
                    payload["portals"].append(("🔍 Trace", "scaffold.blame", [clean_var]))
                    return self._finalize_revelation(payload, trace_id)

            # [ASCENSION 2]: THE ALCHEMICAL VOID
            if (aura.is_inside_header or aura.is_inside_jinja) and clean_var:
                payload["special_md"] = f"### 🌑 Alchemical Void\n**Target:** `{clean_var}`\n\nUndefined variable."
                similars = self._prophesy_similar_symbols(clean_var)
                if similars: payload["special_md"] += f"\n\n**Did you mean?** {', '.join([f'`{s}`' for s in similars])}"

                # Socratic Inquest
                payload["guidance"] = ["Summon the **Alchemist** to materialize this unit of Gnosis."]
                return self._finalize_revelation(payload, trace_id)

        # --- PLANE E: FORM (PATHS) ---
        path_info = self._gaze_for_path(token, request.content, request.position['line'])
        if path_info:
            payload["path_gnosis"] = path_info
            if path_info['exists']:
                payload["portals"].append(("📂 Reveal", "fs/reveal", [str(path_info['abs_path'])]))
                payload["portals"].append(("🔍 Trace", "scaffold.blame", [str(path_info['abs_path'])]))
                payload["portals"].append(("🕸️ Graph", "scaffold.showGraph", [str(path_info['abs_path'])]))
            return self._finalize_revelation(payload, trace_id)

        # --- PLANE F: SOUL (CORTEX SYMBOLS) ---
        if self._cortex and self._cortex._memory and token_type == "SYMBOL":
            try:
                payload["symbol_gnosis"] = self._gaze_into_cortex(token)
                if payload["symbol_gnosis"]:
                    payload["portals"].append(("🔍 Trace", "scaffold.blame", [token]))
                    return self._finalize_revelation(payload, trace_id)
            except Exception as e:
                payload["diagnostics"].append(f"Cortex Gaze fractured: {str(e)}")

        return self._finalize_revelation(payload, trace_id)

    # =========================================================================
    # == IV. THE REVELATION FINALIZER                                        ==
    # =========================================================================

    def _finalize_revelation(self, payload: Dict[str, Any], trace_id: str) -> ScaffoldResult:
        """[THE FINAL SEAL - V120]"""
        if payload.get("resolved_value"):
            payload["resolved_value"] = SECRET_PATTERN.sub("[REDACTED]", str(payload["resolved_value"]))

        formatter = LuminousDossierFormatter(self.project_root)
        markdown = formatter.forge_reality_report(payload)

        # [ASCENSION 74]: Latency Heatmap
        duration_ms = (time.perf_counter_ns() - payload["start_ns"]) / 1_000_000
        lat_color = "green" if duration_ms < 10 else "yellow" if duration_ms < 50 else "red"

        # [ASCENSION 80]: Process-Thread Correlation
        pid = os.getpid()
        thread_name = threading.current_thread().name

        footer = (
            f"\n\n---\n\n"
            f"<span style='color:{lat_color}'>`[{duration_ms:.2f}ms]`</span> "
            f"`0x{trace_id}` | `PID:{pid}` | `T:{thread_name}` | `vV120_TOTALITY`"
        )

        # Sarcophagus Injection
        if payload.get("diagnostics"):
            markdown += "\n\n### ⚠️ Sub-Oracle Analysis\n- " + "\n- ".join(payload["diagnostics"])

        markdown += footer

        # [ASCENSION 12]: Haptic UI Hints
        ui_hints = {"trace_id": trace_id, "duration": duration_ms}
        if payload.get("resolved_value"):
            ui_hints.update({"icon": "diamond", "color": "cyan"})
        elif "Void" in str(payload.get("special_md", "")):
            ui_hints.update({"icon": "alert", "color": "red", "shake": True})
        elif payload.get("canon") or payload.get("guidance"):
            ui_hints.update({"icon": "scroll", "color": "purple"})

        return self.success("Gnosis Found", data={"contents": markdown, "portals": payload["portals"]},
                            ui_hints=ui_hints)

    # =========================================================================
    # == V. SPECIALIZED GAZES                                                ==
    # =========================================================================

    def _gaze_at_dot_anchor(self, aura: AuraContext, raw_line: str) -> str:
        """[ASCENSION 73]: THE MOLECULAR DOT ORACLE."""
        root_name = self.project_root.name if self.project_root else "Void"
        abs_path = str(self.project_root) if self.project_root else "Unanchored"

        # [THE CURE]: Detect Command Molecule (e.g. 'git add .')
        molecule_match = re.search(r'(\w+)\s+(\w+)?\s*\.\s*$', raw_line.strip())
        context_hint = ""
        if molecule_match:
            cmd = molecule_match.group(1)
            context_hint = f"\n\n**Command Context:** Argument for `{cmd}`."

        if aura.context_type == 'will':
            return (
                f"### 📍 Kinetic Anchor: `.`\n"
                f"**Meaning:** Represents the current project sanctum (`{root_name}`)."
                f"{context_hint}\n\n"
                f"Points to the **Absolute Root**: `{abs_path}`."
            )
        else:
            return (
                f"### 🏗️ Spatial Anchor: `.`\n"
                f"**Nature:** Root Sanctum\n"
                f"**Coordinate:** `{abs_path}`"
            )

    def _gaze_into_canon(self, token: str, raw_token: str) -> Optional[Dict]:
        """[RITE]: CANON_LOOKUP."""
        introspect = self.engine.registry.get_request_type("introspect")
        if introspect:
            try:
                res = self.engine.dispatch(introspect(topic="all"))
                if res.success and res.data:
                    return CanonExplorer.find_law(raw_token, res.data) or \
                        CanonExplorer.find_law(token, res.data)
            except:
                pass
        return None

    def _gaze_at_metadata(self, token: str, raw_token: str, line: str) -> str:
        if "@description" in line: return "### 📜 Gnostic Metadata: Description\n\nDefines project intent."
        return "### 💬 Commentary\n\n*A silent whisper in the code.*"

    def _gaze_at_kinetic_will(self, token: str, aura: Any, line: str) -> str:
        token_str = str(token)
        if token_str in COMMAND_BINDINGS:
            g = COMMAND_BINDINGS[token_str]
            return f"### {g['title']}\n\n**Safety:** {'🟢 SAFE' if g['safety'] == 'SAFE' else '🔴 DEST'}\n\n{g['desc']}"
        return f"### 🚀 Kinetic Edict: `{token_str}`\n\nAutomation manifest."

    def _gaze_at_soul_content(self, token: str, aura: Any) -> str:
        return f"### 👻 Scripture Soul\n\nInscribed Content residing within the file."

    def _gaze_for_path(self, token: str, content: str, line_idx: int) -> Optional[Dict]:
        """[ASCENSION 2]: TOPOLOGICAL GAZE."""
        if "{{" in token or "}}" in token or token.startswith('$$'): return None
        if token in SACRED_SIGILS and token != ".": return None

        clean_token = token.strip("\"'").strip()
        if not clean_token: return None
        if len(clean_token) < 1: return None

        is_directory_intent = clean_token.endswith('/') or clean_token == "."

        try:
            abs_path = self.project_root if clean_token == "." else (self.project_root / clean_token).resolve()

            if abs_path and abs_path.exists():
                is_dir = abs_path.is_dir()
                inner_count = 0
                if is_dir:
                    try:
                        inner_count = len(list(abs_path.iterdir()))
                    except:
                        pass

                return {
                    "exists": True, "is_dir": is_dir,
                    "nature": "Sanctum (Directory)" if is_dir else "Scripture (File)",
                    "size": abs_path.stat().st_size if not is_dir else None,
                    "abs_path": abs_path,
                    "inner_count": inner_count,
                    "is_shadow": ".scaffold/staging" in str(abs_path)
                }

            if '/' not in clean_token and '.' not in clean_token and not is_directory_intent:
                return None

            return {"exists": False, "is_dir": is_directory_intent, "nature": "Void Path", "abs_path": abs_path}
        except:
            return None

    def _gaze_into_cortex(self, token: str) -> Optional[Dict]:
        if not self._cortex or not self._cortex._memory or token not in self._cortex._memory.symbol_map:
            return None

        def_path_str = self._cortex._memory.symbol_map[token]
        file_ast = self._cortex._memory.project_gnosis.get(str(def_path_str), {})
        all_symbols = file_ast.get('functions', []) + file_ast.get('classes', [])
        symbol_data = next((i for i in all_symbols if i.get('name') == token), None)

        if not symbol_data: return None
        return {
            "origin": str(def_path_str),
            "signature": symbol_data.get('signature', token),
            "docstring": symbol_data.get('docstring', ''),
            "centrality": self._query_centrality(token)
        }

    def _unwind_variable(self, val: Any) -> Any:
        def _unwind(v, depth):
            if depth > 10: return v
            if isinstance(v, str) and v.strip().startswith("$$"):
                next_var = v.replace("$$", "").strip()
                return _unwind(Store.get(next_var), depth + 1)
            return v

        return _unwind(val, 0)

    def _query_ledger(self, token: str) -> List[str]:
        history = []
        for entry in list(ActiveLedger._entries):
            if token in str(entry.forward_state):
                ts = time.strftime('%H:%M:%S', time.localtime(entry.timestamp))
                history.append(f"Modified by **{entry.operation.name}** at `{ts}`")
        return history[-3:]

    def _query_centrality(self, token: str) -> float:
        if self._cortex and self._cortex._memory and token in self._cortex._memory.symbol_map:
            path_str = self._cortex._memory.symbol_map[token]
            gnosis = self._cortex._memory.find_gnosis_by_path(Path(path_str))
            return gnosis.centrality_score if gnosis else 0.0
        return 0.0

    def _gaze_for_strict_local_variable(self, token: str, content: str) -> Optional[str]:
        # [ASCENSION 21]: Lexical Scrying Fix
        # Correctly handles the name extraction without being greedy.
        regex = re.compile(fr'^\s*(?:\$\$|let|def|const)?\s*{re.escape(token)}\s*(?::\s*[^=]+)?\s*=\s*(.*)',
                           re.MULTILINE)
        match = regex.search(content)
        return match.group(1).strip().strip("'\"").split('#')[0].strip() if match else None

    def _prophesy_similar_symbols(self, token: str) -> List[str]:
        from difflib import get_close_matches
        all_keys = list(Store.all_keys())
        if self._cortex and self._cortex._memory: all_keys.extend(list(self._cortex._memory.symbol_map.keys()))
        return get_close_matches(token, list(set(all_keys)), n=3, cutoff=0.6)

    def _perceive_token_and_aura(self, request: HoverRequest) -> Tuple[Optional[str], str, str]:
        """[ASCENSION 16]: Molecular Token Fusion."""
        try:
            line_idx, char_idx = int(request.position['line']), int(request.position['character'])
            lines = request.content.splitlines()
            if line_idx >= len(lines): return None, "VOID", ""
            raw_line = lines[line_idx]

            grammar = "symphony" if str(request.file_path).endswith(('.symphony', '.arch')) else "scaffold"
            lexer = GnosticLexer(grammar_key=grammar)
            tokens = lexer.tokenize(raw_line)

            target_idx = -1
            target = None
            for i, t in enumerate(tokens):
                if t.pos <= char_idx <= (t.pos + len(t.value)):
                    target = t;
                    target_idx = i;
                    break

            if not target: return None, "VOID", ""
            val = str(target.value).strip()

            if target_idx > 0:
                prev = tokens[target_idx - 1]
                molecule = f"{prev.value} {val}"
                if molecule in COMMAND_BINDINGS: return molecule, "KEYWORD", molecule

            if val.startswith('$$'): return val, "SIGIL_VAR", val
            if val.startswith('@'): return val.lstrip('@'), "DIRECTIVE", val
            if val in (">>", "??", "%%", "!!"): return val, "SIGIL_MAESTRO", val
            if "#" in raw_line and char_idx > raw_line.find("#"): return val, "COMMENT", val

            return val, "SYMBOL", val
        except:
            return None, "VOID", ""

# === SCRIPTURE SEALED: THE TOTALITY IS ATTAINED ===
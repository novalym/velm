# Path: core/artisans/analyze/static_inquisitor/detectors/variables.py
# --------------------------------------------------------------------

import re
import difflib
import sys
import os
from typing import List, Dict, Any, Optional, Tuple, Set

from .base import BaseDetector
from .....contracts.data_contracts import ScaffoldItem, GnosticDossier, GnosticLineType


class VariableDetector(BaseDetector):
    """
    =============================================================================
    == THE KEEPER OF NAMES (V-Ω-TOTAL-RECALL-ASCENDED)                         ==
    =============================================================================
    LIF: INFINITY | ROLE: SYMBOLIC_VERIFIER | RANK: SOVEREIGN

    [THE CURE]: This version annihilates the Path-Object/String-Type schism
    that causes "Zero Atoms" in Daemon mode. It speaks directly to stderr.
    """

    WHITELIST = {
        'project_name', 'project_slug', 'author', 'year', 'description',
        'scaffold_version', 'cwd', 'now', 'scaffold_env', 'filename',
        'git_user', 'git_email', 'os', 'env'
    }

    def _log(self, rid: str, msg: str):
        """Forceful stderr communication."""
        sys.stderr.write(f"[{rid}] [VariableDetector] {msg}\n")
        sys.stderr.flush()

    def detect(self, content: str, variables: Dict, items: List[ScaffoldItem],
               edicts: List, dossier: GnosticDossier) -> List[Dict[str, Any]]:

        # Identify Request ID for Traceability
        rid = os.environ.get("GNOSTIC_JOB_ID", "local")
        self._log(rid, "🟢 Commencing Inquest...")

        diagnostics = []
        seen_heresies = set()

        # [ASCENSION 1]: CANONICAL CONTEXT
        # Transmute all defined keys to a safe set of strings
        known_vars = dossier.defined.union(variables.keys()).union(self.WHITELIST)
        required_vars = dossier.required

        self._log(rid, f"   Required: {list(required_vars)}")
        self._log(rid, f"   Known:    {len(known_vars)} keys manifest.")

        # -------------------------------------------------------------------------
        # 1. UNDEFINED VARIABLES: THE SEARCH FOR VOID
        # -------------------------------------------------------------------------
        unknown_vars = required_vars - known_vars

        if not unknown_vars:
            self._log(rid, "   ✅ No undefined variables perceived via AST.")

        for var_name in unknown_vars:
            self._log(rid, f"   Hunting for phantom: '{var_name}'")

            # PHASE 1: Structural Gaze
            found_item, start_col, line_offset, match_context = self._locate_usage(var_name, items, rid)

            final_line_idx = 0
            severity_label = "CRITICAL"

            if found_item:
                base_line = max(0, found_item.line_num - 1)
                final_line_idx = base_line + line_offset
                severity_label = "CRITICAL" if found_item.line_type == GnosticLineType.FORM else "WARNING"
                self._log(rid, f"   🎯 Found in AST at Ln {final_line_idx + 1}")
            else:
                # PHASE 2: Global Fallback (Regex Scry)
                self._log(rid, f"   ⚠️ AST miss for '{var_name}'. Engaging Global Fallback Scan...")
                raw_line_idx, raw_col, raw_ctx = self._scan_raw_content(content, var_name)

                if raw_line_idx is not None:
                    final_line_idx = raw_line_idx
                    start_col = raw_col
                    match_context = raw_ctx
                    severity_label = "WARNING"
                    self._log(rid, f"   🎯 Found in Raw Text at Ln {final_line_idx + 1}")
                else:
                    self._log(rid, f"   ❌ Variable '{var_name}' required but not found in Matter. Skipping.")
                    continue

            # Levinsthein Prophecy
            all_known = list(known_vars)
            similar = difflib.get_close_matches(var_name, all_known, n=1, cutoff=0.6)
            hint = f" Did you mean '{similar[0]}'?" if similar else ""

            sig = f"{final_line_idx}:{start_col}:{var_name}"
            if sig in seen_heresies: continue
            seen_heresies.add(sig)

            diagnostics.append(self._forge_diagnostic(
                key="UNDEFINED_VARIABLE_REFERENCE_HERESY",
                line=final_line_idx,
                item=found_item,
                data={
                    "variable": var_name,
                    "heresy_key": "UNDEFINED_VARIABLE_REFERENCE_HERESY",
                    "severity_override": severity_label,
                    "precise_range": {"start": start_col, "end": start_col + len(var_name)},
                    "details": f"Variable '{var_name}' is summoned but undefined.\nMatch: {match_context}\n{hint}"
                }
            ))

        # -------------------------------------------------------------------------
        # 2. UNUSED VARIABLES: THE SEARCH FOR WASTE
        # -------------------------------------------------------------------------
        unused_vars = (dossier.defined - dossier.required) - self.WHITELIST
        for var_name in unused_vars:
            def_item = next(
                (i for i in items if i.line_type == GnosticLineType.VARIABLE and var_name in (i.raw_scripture or "")),
                None)

            line_idx = max(0, def_item.line_num - 1) if def_item else 0

            diagnostics.append(self._forge_diagnostic(
                key="UNUSED_GNOSIS_HERESY",
                line=line_idx,
                item=def_item,
                data={
                    "variable": var_name,
                    "heresy_key": "UNUSED_GNOSIS_HERESY",
                    "details": f"Variable '$$ {var_name}' is defined but never summoned.",
                    "severity_override": "WARNING"
                }
            ))

        self._log(rid, f"🏁 Inquest Complete. Perceived {len(diagnostics)} heresies.")
        return diagnostics

    def _scan_raw_content(self, content: str, var_name: str) -> Tuple[Optional[int], int, str]:
        """[ASCENSION 11]: Regex-based text scryer."""
        escaped_var = re.escape(var_name)
        # Matches {{ var }} or {{var}} or {{ var | filter }}
        pattern = re.compile(r'\{\{\s*' + escaped_var + r'\s*(?:\}\}|\|)')

        lines = content.splitlines()
        for i, line in enumerate(lines):
            if line.strip().startswith('#'): continue
            match = pattern.search(line)
            if match:
                # We return the start of the variable itself, not the {{ braces
                var_start = line.find(var_name, match.start())
                return i, var_start, line.strip()
        return None, 0, ""

    def _locate_usage(self, var_name: str, items: List[ScaffoldItem], rid: str) -> Tuple[
        Optional[ScaffoldItem], int, int, str]:
        """[ASCENSION 1]: Path-Normalized Structural Scryer."""
        escaped_var = re.escape(var_name)

        # Pattern to find if line is a definition of THIS variable
        def_pattern = re.compile(r'^\s*(\$\$|let|def|const)\s+' + escaped_var + r'\s*(?:[:=]|$)')

        for item in items:
            # 1. Skip definition lines to avoid self-reporting
            if item.line_type == GnosticLineType.VARIABLE:
                if def_pattern.match(item.raw_scripture or ""):
                    continue

            # 2. Check Path (NORMALIZED)
            if item.path:
                # [ASCENSION 1]: FORCE STRING NORMALIZATION
                path_str = str(item.path).replace('\\', '/').lower()

                # Check for {{ var }} or {{var}} in path string
                u1 = "{{" + var_name.lower() + "}}"
                u2 = "{{ " + var_name.lower() + " }}"

                if u1 in path_str or u2 in path_str:
                    col = path_str.find(var_name.lower())
                    return item, col, 0, f"Path: {path_str}"

            # 3. Check Header (Raw Scripture)
            scripture = item.raw_scripture or ""
            if var_name in scripture:
                # Logic to ensure it's inside braces...
                if f"{{{{ {var_name}" in scripture or f"{{{{{var_name}" in scripture:
                    col = scripture.find(var_name)
                    return item, col, 0, scripture.strip()

            # 4. Check Content Block
            if item.content:
                c_lines = item.content.splitlines()
                for i, c_line in enumerate(c_lines):
                    if var_name in c_line:
                        # Simple check for Jinja presence
                        if "{{" in c_line and "}}" in c_line:
                            col = c_line.find(var_name)
                            # Block string offset logic
                            extra_offset = 1 if '"""' in scripture or "'''" in scripture else 0
                            return item, col, extra_offset + i, c_line.strip()

        return None, 0, 0, ""
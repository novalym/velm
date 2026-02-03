# // artisans/analyze/completion_codex/symphony.py

import re
from pathlib import Path
from typing import List, Dict, Any, Optional


class SymphonyCompletionScribe:
    """
    =================================================================================
    == THE MASTER PROPHET OF SYMPHONIC WILL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)      ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000,000,000

    This divine artisan has been made whole. It receives the full Gnostic Context
    from the Conductor, allowing it to perform Surgical Short-Circuits based on
    the Architect's keystrokes.
    =================================================================================
    """

    def __init__(self, introspection_data: Dict[str, Any]):
        self.gnosis = introspection_data.get("symphony_language", {})
        # We inherit the Alchemist's Grimoire from the Scaffold definition to enable
        # variable/filter completion within Symphony files.
        self.alchemist_gnosis = introspection_data.get("scaffold_language", {}).get("alchemist_grimoire", {})

        # [ASCENSION 1]: O(1) Vow Lookup Map
        # Flattens the categorical hierarchy into a high-speed access hash map.
        self.vow_map = {
            vow['token']: vow
            for category in self.gnosis.get("vows", {}).get("categories", [])
            for vow in category.get("pantheon", [])
        }

    def _snippet(self, label: str, kind: int, detail: str, insert_text: str, doc: str = "") -> Dict:
        """Forges a standard LSP Snippet completion item."""
        return {
            "label": label,
            "kind": kind,
            "detail": detail,
            "insertText": insert_text,
            "insertTextFormat": 2,  # Snippet
            "documentation": {"kind": "markdown", "value": doc} if doc else None
        }

    def _prophesy_variable_context(self, line_prefix: str, all_vars: List[str]) -> List[Dict[str, Any]]:
        """
        [ASCENSION 5]: THE ALCHEMIST'S SOUL
        Prophesies variables, filters, and functions within a `{{...}}` block.
        """
        jinja_start = line_prefix.rfind('{{')
        if jinja_start == -1: return []
        expression_prefix = line_prefix[jinja_start + 2:].strip()

        # 1. Filters (|) - If the user has typed a pipe
        pipe_pos = expression_prefix.rfind('|')
        if pipe_pos != -1:
            filter_prefix = expression_prefix[pipe_pos + 1:].lstrip()
            suggestions = []
            for group in self.alchemist_gnosis.get("filters", []):
                for token in group.get("tokens", []):
                    if token.startswith(filter_prefix.lower()):
                        doc = f"### Filter: `| {token}`\n\n**Gnosis:** {group.get('description', 'N/A')}"
                        suggestions.append(self._snippet(f"| {token}", 3, group.get("description"), f" {token} ", doc))
            return suggestions

        # 2. Attributes (.) - If the user is accessing a property
        dot_pos = expression_prefix.rfind('.')
        if dot_pos != -1:
            attr_prefix = expression_prefix[dot_pos + 1:]
            common_attrs = ["name", "id", "description", "path", "key", "value", "items", "keys", "values"]
            return [{"label": a, "kind": 5, "detail": "Attribute", "insertText": a}
                    for a in common_attrs if a.startswith(attr_prefix.lower())]

        # 3. Variables & Functions - Root expression context
        suggestions = []
        for var in all_vars:
            if var.startswith(expression_prefix):
                suggestions.append({"label": var, "kind": 6, "detail": "Blueprint Variable", "insertText": f"{var} "})

        for func in self.alchemist_gnosis.get("functions", []):
            if func['name'].startswith(expression_prefix.lower()):
                doc = f"### Function: `{func['name']}`\n\n{func.get('description')}"
                suggestions.append(self._snippet(func['name'], 2, func.get("description"), f"{func['name']}()", doc))

        return suggestions

    def get_completions(
            self,
            line_prefix: str,
            all_vars: List[str],
            project_root: Path,
            context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        The Master Prophet. Performs a deep lexical gaze to provide hyper-contextual completions.
        """
        try:
            stripped_prefix = line_prefix.strip()
            tokens = stripped_prefix.split()
            num_tokens = len(tokens)
            first_token = tokens[0] if num_tokens > 0 else ""

            # [ASCENSION 2]: THE TRIGGER SHORT-CIRCUIT
            # If the Architect typed a specific sigil, we immediately narrow the prophecy.
            trigger = context.get('triggerCharacter') if context else None

            # --- GAZE I: THE REALM OF THE ALCHEMIST ---
            # Triggered by '{' or typing inside {{
            if trigger == '{' or (line_prefix.rfind('{{') != -1 and line_prefix.rfind('}}') < line_prefix.rfind('{{')):
                return self._prophesy_variable_context(line_prefix, all_vars)

            # --- GAZE II: THE REALM OF THE VOW (??) ---
            if trigger == '?' or first_token.startswith("??") or stripped_prefix == '?':
                return self._prophesy_vow_context(stripped_prefix)

            # --- GAZE III: THE REALM OF THE STATE (%%) ---
            if trigger == '%' or first_token.startswith("%%") or stripped_prefix == '%':
                return self._prophesy_state_context(stripped_prefix)

            # --- GAZE IV: THE REALM OF THE DIRECTIVE (@) ---
            if trigger == '@' or first_token.startswith("@"):
                return self._prophesy_directive_context(stripped_prefix)

            # --- GAZE V: THE REALM OF THE BLANK SLATE (ROOT) ---
            # If the line is empty, offer the fundamental laws.
            if not stripped_prefix:
                return self._prophesy_root_completions()

            # --- GAZE VI: POLYGLOT PARAMS ---
            # e.g. py(venv=...)
            poly_match = re.match(r'^(\w+)\((.*)', stripped_prefix)
            if poly_match:
                lang, params_prefix = poly_match.groups()
                # Check if lang is valid polyglot type
                if lang in [l.get('token') for l in self.gnosis.get("polyglot_rites", {}).get("languages", [])]:
                    return self._prophesy_polyglot_param_completions(params_prefix)

            # --- GAZE VII: PREFIX MATCHING (FALLBACK) ---
            # If the user typed "py" without a trigger, suggest "py:".
            if num_tokens == 1 and not line_prefix.endswith(' '):
                return [s for s in self._prophesy_root_completions() if s['label'].startswith(stripped_prefix)]

            return []

        except Exception as e:
            # [ASCENSION 12]: The Unbreakable Try-Catch
            return [{"label": f"SymphonyProphetHeresy: {e}", "kind": 23}]

    # ... (Helper methods below) ...

    def _prophesy_root_completions(self) -> List[Dict]:
        """Prophesies the fundamental edicts from the Gnosis."""
        suggestions = []

        # 1. The Core Edicts (>>, ??, %%)
        edicts = self.gnosis.get("edicts", {}).get("pantheon", [])
        for edict in edicts:
            insert_text = edict.get("token", "")
            if insert_text == ">>":
                insert_text = ">> ${1:command}"
            elif insert_text == "??":
                insert_text = "?? ${1:succeeds}"
            elif insert_text == "%%":
                insert_text = "%% ${1:sanctum}: ${2:./path}"

            doc = f"### {edict['name']} (`{edict['token']}`)\n\n{edict['description']}"
            suggestions.append(self._snippet(edict['token'], 15, edict['name'], insert_text, doc))

        # 2. The Polyglot Rites (py:, js:, etc.)
        languages = self.gnosis.get("polyglot_rites", {}).get("languages", [])
        for lang in languages:
            doc = f"### Polyglot Rite: `{lang['token']}`\n\nExecute a block of **{lang['name']}** code."
            suggestions.append(
                self._snippet(f"{lang['token']}:", 15, f"{lang['name']} Block", f"{lang['token']}:\n\t${{0}}", doc))
        return suggestions

    def _prophesy_vow_context(self, prefix: str) -> List[Dict]:
        """
        [ASCENSION 4]: THE VOW DISCRIMINATOR.
        Returns only Vow (??) suggestions.
        """
        # Strip the sigil to find the partial term (e.g. "??file" -> "file")
        clean_prefix = prefix.lstrip('?').strip()
        suggestions = []

        # If we have a colon, we might be inside args, but V1 doesn't support arg completion yet.
        if ':' in prefix: return []

        for vow_name, vow_data in self.vow_map.items():
            # If the user typed "??file", match "file_exists"
            # If the user just typed "??", match everything
            if not clean_prefix or vow_name.startswith(clean_prefix):
                syntax = vow_data.get('syntax', vow_name)
                desc = vow_data.get('description', 'Gnostic Vow')
                # If syntax has args, add colon and space
                insert_text = f"{vow_name}: " if ":" in syntax else vow_name
                doc = f"### Vow: `{vow_name}`\n\n{desc}\n\n**Syntax:** `{syntax}`"
                suggestions.append(self._snippet(vow_name, 3, desc, insert_text, doc))
        return suggestions

    def _prophesy_state_context(self, prefix: str) -> List[Dict]:
        """[ASCENSION 9]: STATE PROPHET (%%)"""
        clean_prefix = prefix.lstrip('%').strip()
        states = ["sanctum", "proclaim", "let", "env", "cd"]
        suggestions = []
        for s in states:
            if s.startswith(clean_prefix):
                suggestions.append(self._snippet(s, 3, "State Directive", f"{s}: ${{1}}"))
        return suggestions

    def _prophesy_directive_context(self, prefix: str) -> List[Dict]:
        """[ASCENSION 10]: DIRECTIVE GUIDE (@)"""
        query = prefix.lstrip('@')
        suggestions = []
        # Merge logic flow and composition directives
        directives = self.gnosis.get("logic_flow", {}).get("pantheon", []) + \
                     self.gnosis.get("composition", {}).get("pantheon", [])

        for directive in directives:
            token = directive.get("token", "").split(' ')[0]
            # Match @if against @if
            if token.startswith(f"@{query}"):
                name = directive.get("name", "")
                desc = directive.get("description", "")
                syntax = directive.get("syntax", "")

                # Smart Snippets
                insert_text = token
                if token == "@if":
                    insert_text = "@if {{ ${1:condition} }}:"
                elif token == "@for":
                    insert_text = "@for ${1:item} in ${2:list}:"
                elif token == "@try":
                    insert_text = "@try:\n\t${1}\n@catch:\n\t${2}\n@endtry"

                doc = f"### {name} (`{token}`)\n\n{desc}\n\n**Syntax:**\n```symphony\n{syntax}\n```"
                suggestions.append(self._snippet(token, 15, name, insert_text, doc))
        return suggestions

    def _prophesy_polyglot_param_completions(self, prefix: str) -> List[Dict]:
        """[ASCENSION 3]: POLYGLOT PARAMETER HINTS"""
        suggestions = []
        typed_params = set(re.findall(r'(\w+)=', prefix))
        params = self.gnosis.get("polyglot_rites", {}).get("parameters", [])
        for param_info in params:
            param = param_info['token']
            if param not in typed_params:
                insert_text = f"{param}=${{1}}"
                doc = f"**Parameter:** `{param}`\n\n{param_info['description']}"
                suggestions.append(self._snippet(f"{param}=", 18, param_info['description'], insert_text, doc))
        return suggestions


# =================================================================================
# == THE PUBLIC GATEWAY                                                          ==
# =================================================================================

def get_symphony_completions(
        line_prefix: str,
        all_vars: List[str],
        project_root: Path,
        introspection_data: Dict[str, Any],
        # [THE ASCENSION]: Context Injection for Trigger-Aware Triage
        context: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    The one true, public gateway to the Scribe of Symphonic Prophecy.
    NOW ASCENDED to accept the Gnostic Context.
    """
    try:
        scribe = SymphonyCompletionScribe(introspection_data)
        return scribe.get_completions(line_prefix, all_vars, project_root, context)
    except Exception as e:
        return [{"label": f"SymphonyProphetHeresy: {e}", "kind": 23}]
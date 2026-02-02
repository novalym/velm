# scaffold/artisans/analyze/completion_codex/scaffold.py

"""
=================================================================================
== THE SPECIALIST PROPHET OF FORM (V-Ω-SCAFFOLD-UNIFIED)                       ==
=================================================================================
LIF: 10,000,000,000,000

This artisan is the Sovereign Prophet for the Scaffold language.
It has absorbed the souls of the Variable and Directive Scribes.
It relies ONLY on the `introspection_data` bestowed by the Conductor.
It has NO dependencies on sibling files within the codex.
=================================================================================
"""
import os
import re
from pathlib import Path
from typing import List, Dict, Any


class GnosticCartographer:
    """
    =================================================================================
    == THE GNOSTIC CARTOGRAPHER (V-Ω-SOVEREIGN)                                    ==
    =================================================================================
    A pure, sovereign, and stateless artisan that provides filesystem completions.
    It is summoned by the Master Prophet to gaze upon the mortal realm of the
    filesystem with unbreakable resilience and Gnostic awareness of ignored sanctums.
    =================================================================================
    """

    def __init__(self, project_root: Path, engine: Optional[Any] = None):
        """
        =================================================================================
        == THE INCEPTION OF THE CARTOGRAPHER (V-Ω-ETERNAL-ANCHOR)                      ==
        =================================================================================
        LIF: 10x | Engine-Aware | Multiverse-Ready

        Consecrates the Cartographer, anchoring it to the project's physical root
        and bestowing upon it the Gaze of the Engine.
        """
        from ....utils import get_ignore_spec

        # [THE GNOSTIC ANCHOR]: We resolve to absolute path to prevent relativity heresies.
        self.project_root = project_root.resolve()

        # [THE TELEPATHIC LINK]: Link to the master engine for Shadow Layer access.
        self.engine = engine

        # [THE GAZE OF AVERSION]: Ingest the sacred laws of ignored scriptures.
        self.ignore_spec = get_ignore_spec(self.project_root)

        Logger.verbose(f"Cartographer initialized for root: {self.project_root.name}")

    def gaze(self, partial_path: str, session_id: str = "global") -> List[Dict[str, Any]]:
        """
        =================================================================================
        == THE OMNISCIENT GAZE (V-Ω-UNION-SCRYING-ULTIMA-FINALIS)                      ==
        =================================================================================
        LIF: INFINITY | AUTH_CODE: ()@#()#@()

        The definitive realization of path-scrying. It merges the Mortal Realm (Matter)
        with the Ethereal Plane (Shadow) to provide a unified map of the project cosmos.
        """
        completions = []
        try:
            # --- MOVEMENT I: THE RITE OF NORMALIZATION ---
            # Unify slashes and handle the tilde (Home) expansion.
            raw_path = partial_path.replace('\\', '/')
            if raw_path.startswith('~'):
                path_in_progress = str(Path.home() / raw_path[2:])
            else:
                path_in_progress = raw_path

            # --- MOVEMENT II: THE GNOSTIC DECONSTRUCTION ---
            # We split the plea into the base directory we are searching and the
            # prefix we are matching.
            search_dir_abs = self.project_root.resolve()
            file_prefix = path_in_progress

            if '/' in path_in_progress:
                dir_part, file_prefix = path_in_progress.rsplit('/', 1)
                # Resolve the search directory relative to the project root
                search_dir_abs = (self.project_root / dir_part).resolve()

            # The project-relative path of the directory we are scrying
            try:
                rel_search_dir = search_dir_abs.relative_to(self.project_root).as_posix()
                if rel_search_dir == ".":
                    rel_search_dir = ""
            except ValueError:
                # Path is outside the root, we cannot scry here.
                return []

            # --- MOVEMENT III: THE UNION GAZE (MATTER & SHADOW) ---
            # items_map: name -> {kind, is_shadow}
            items_map: Dict[str, Dict[str, Any]] = {}

            # 1. Harvest from Matter (The Physical Disk)
            if search_dir_abs.is_dir():
                for item in search_dir_abs.iterdir():
                    # Gaze of Aversion: Do not proclaim what is forbidden
                    if self.ignore_spec:
                        try:
                            rel_item = str(item.relative_to(self.project_root))
                            if self.ignore_spec.match_file(rel_item):
                                continue
                        except ValueError:
                            pass

                    if item.name.lower().startswith(file_prefix.lower()):
                        is_dir = item.is_dir()
                        items_map[item.name] = {
                            "kind": 19 if is_dir else 17,
                            "is_shadow": False
                        }

            # 2. Harvest from Shadow (The Ethereal Plane)
            # We summon the ShadowVault to see what the AI has dreamed for this dir.
            try:
                # Assuming the vault is accessible via the artisan's engine context
                if hasattr(self, 'engine') and hasattr(self.engine, 'vault'):
                    vault = self.engine.vault
                    # The vault returns a set of file names dreaming in this relative dir
                    shadow_names = vault.list_dir(session_id, rel_search_dir)

                    for s_name in shadow_names:
                        if s_name.lower().startswith(file_prefix.lower()):
                            # Shadow usually represents files, but can represent dirs
                            # [THE FIX]: Deduplicate. Shadow takes precedence over Matter.
                            items_map[s_name] = {
                                "kind": 17,  # Most shadows are scriptures
                                "is_shadow": True
                            }
            except Exception:
                # If the vault is unreachable, the Gaze falls back to pure matter.
                pass

            # --- MOVEMENT IV: THE RITE OF LUMINOUS SORTING ---
            # We sort by: 1. Folder status (Folders first), 2. Name (Alpha)
            sorted_names = sorted(
                items_map.keys(),
                key=lambda n: (items_map[n]["kind"] != 19, n.lower())
            )

            # --- MOVEMENT V: THE FORGING OF THE PROPHECIES ---
            for name in sorted_names:
                info = items_map[name]
                is_dir = info["kind"] == 19

                # [ASCENSION 5]: Slash-Aware Continuity
                label = name + ("/" if is_dir else "")
                insert_text = name + ("/" if is_dir else "")

                detail = "Sanctum (Directory)" if is_dir else "Scripture (File)"
                if info["is_shadow"]:
                    detail = f"👻 [Shadow] {detail}"

                completions.append({
                    "label": label,
                    "kind": info["kind"],
                    "detail": detail,
                    "insertText": insert_text,
                    # [ASCENSION 4]: Sort priority - Folder bits (0) < File bits (1)
                    "sortText": f"{'0' if is_dir else '1'}_{name}"
                })

        except Exception as e:
            # The Gaze is shielded from all paradox to ensure
            # the UI remains responsive even in chaos.
            pass

        return completions


class ScaffoldCompletionScribe:
    """
    =================================================================================
    == THE MASTER PROPHET OF FORM (V-Ω-ETERNAL-UNIFIED)                            ==
    =================================================================================
    This divine Scribe has absorbed the Gnosis of Variables and Directives.
    It receives the complete, living Gnosis of the Scaffold language and the
    UI Component Codex from the `introspect` Oracle.
    =================================================================================
    """

    def __init__(self, introspection_data: Dict[str, Any]):
        self.scaffold_gnosis = introspection_data.get("scaffold_language", {})
        self.ui_gnosis = introspection_data.get("ui_components", {})
        self.semantic_gnosis = self.scaffold_gnosis.get("semantic_cortex", {})
        self.alchemist_gnosis = self.scaffold_gnosis.get("alchemist_grimoire", {})
        self.all_vars: List[str] = []

    def _snippet(self, label: str, kind: int, detail: str, insert_text: str, doc: str = "") -> Dict:
        return {
            "label": label, "kind": kind, "detail": detail,
            "insertText": insert_text, "insertTextFormat": 2,
            "documentation": {"kind": "markdown", "value": doc} if doc else None
        }

    # =============================================================================
    # == I. THE PROPHECY OF ROOTS                                                ==
    # =============================================================================

    def prophesy_root_completions(self) -> List[Dict]:
        """Prophesies the fundamental sigils for a blank line."""
        suggestions = []

        # 1. Sigils ($$, ::, <<, %%)
        sigils = self.scaffold_gnosis.get("sigils", [])
        for sigil in sigils:
            token, name, desc, usage, example = sigil.get("token"), sigil.get("name"), sigil.get(
                "description"), sigil.get("usage"), sigil.get("example", {}).get("scripture")
            insert_text = f"{token} ${{1}}"
            if token == "$$":
                insert_text = "$$ ${1:name} = ${2:value}"
            elif token == "::":
                insert_text = ":: \"${1:content}\""
            elif token == "<<":
                insert_text = "<< ${1:./path}"

            doc = f"### {name} (`{token}`)\n\n{desc}\n\n**Usage:**\n```scaffold\n{usage}\n```"
            suggestions.append(self._snippet(token, 15, name, insert_text, doc))

        # 2. Root Directives (@if, @include)
        for directive in self.scaffold_gnosis.get("directives", {}).get("pantheon", []):
            token = directive.get("token", "").split(' ')[0]  # Get primary token like '@if'
            if "/" in token: continue
            name, desc, syntax = directive.get("name"), directive.get("description"), directive.get("syntax")
            insert_text = f"{token} ${{1}}"
            if token == "@if": insert_text = "@if {{ ${1:condition} }}\n\t${0}\n@endif"
            doc = f"### {name} (`{token}`)\n\n{desc}\n\n**Syntax:**\n```scaffold\n{syntax}\n```"
            suggestions.append(self._snippet(token, 15, name, insert_text, doc))

        return suggestions

    # =============================================================================
    # == II. THE PROPHECY OF SOULS (CONTENT)                                     ==
    # =============================================================================

    def prophesy_soul_context(
            self,
            content_prefix: str,
            sigil: str,
            cartographer: GnosticCartographer
    ) -> List[Dict[str, Any]]:
        """Prophesies completions for the soul of a scripture (`::` or `<<`)."""
        if sigil == '<<':
            return cartographer.gaze(content_prefix.lstrip())

        if sigil == '::':
            stripped_content = content_prefix.lstrip()

            # Gaze 1: The Gaze of the Semantic Cortex (`@...`)
            if stripped_content.startswith('@'):
                # UI Components
                ui_match = re.match(r'@ui/component\(\s*(?:name\s*=\s*)?["\']([^"\']*)?$', stripped_content)
                if ui_match:
                    return self._prophesy_ui_components(ui_match.group(1) or "")

                # Directives
                return self.prophesy_directive_context(stripped_content)

            # Gaze 2: The Gaze of the Alchemist (`{{...}}`)
            jinja_start = content_prefix.rfind('{{')
            if jinja_start != -1 and content_prefix.rfind('}}') < jinja_start:
                return self.prophesy_variable_context(content_prefix)

            # Gaze 3: The Gaze of the Root (Anticipation)
            if not stripped_content:
                suggestions = []
                domains = self.semantic_gnosis.get("domains", [])
                for domain in domains:
                    doc = f"### Semantic Domain: `@{domain}`\n\nSummons a hyper-intelligent artisan from the **@{domain}** domain to generate a complex reality from a single plea."
                    suggestions.append(self._snippet(
                        f"@{domain}", 15, f"Summon the @{domain} Semantic Artisan", f"@{domain}/${{1:rite}}", doc
                    ))
                return suggestions

        return []

    # =============================================================================
    # == III. THE PROPHECY OF VARIABLES (ABSORBED)                               ==
    # =============================================================================

    def prophesy_variable_context(self, line_prefix: str) -> List[Dict[str, Any]]:
        """
        [THE ABSORBED ALCHEMIST]
        Prophesies variables, filters, and attributes.
        """
        jinja_start = line_prefix.rfind('{{')
        if jinja_start == -1: return []
        expression_prefix = line_prefix[jinja_start + 2:].strip()

        # 1. Filters (|)
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

        # 2. Attributes (.)
        dot_pos = expression_prefix.rfind('.')
        if dot_pos != -1:
            # Basic attribute heuristic
            attr_prefix = expression_prefix[dot_pos + 1:]
            common_attrs = ["name", "id", "description", "path", "key", "value"]
            return [{"label": a, "kind": 5, "detail": "Attribute", "insertText": a}
                    for a in common_attrs if a.startswith(attr_prefix.lower())]

        # 3. Variables & Functions (Root)
        suggestions = []

        # Blueprint Variables
        for var in self.all_vars:
            if var.startswith(expression_prefix):
                suggestions.append(
                    {"label": var, "kind": 6, "detail": "Blueprint Variable", "insertText": f"{var} }}}}"})

        # Alchemist Functions
        for func in self.alchemist_gnosis.get("functions", []):
            if func['name'].startswith(expression_prefix.lower()):
                doc = f"### Function: `{func['name']}`\n\n{func.get('description')}"
                suggestions.append(self._snippet(func['name'], 2, func.get("description"), f"{func['name']}()", doc))

        return suggestions

    # =============================================================================
    # == IV. THE PROPHECY OF DIRECTIVES (ABSORBED)                               ==
    # =============================================================================

    def prophesy_directive_context(self, prefix: str) -> List[Dict[str, Any]]:
        """
        [THE ABSORBED SEMANTICIST]
        Prophesies @domains and @domain/directives.
        """
        at_pos = prefix.rfind('@')
        if at_pos == -1: return []
        query = prefix[at_pos + 1:]

        suggestions = []

        # Domain Level
        if '/' not in query:
            for domain in self.semantic_gnosis.get("domains", []):
                if domain.startswith(query):
                    suggestions.append(
                        {"label": f"@{domain}/", "kind": 19, "detail": "Semantic Domain", "insertText": f"@{domain}/"})
            return suggestions

        # Directive Level
        parts = query.split('/', 1)
        if len(parts) == 2:
            domain, rite_prefix = parts
            # Directives are stored as flat strings "domain/rite" in the introspection data list
            for full_directive in self.semantic_gnosis.get("directives", []):
                # full_directive looks like "@ui/component"
                clean_directive = full_directive.lstrip('@')  # ui/component
                if clean_directive.startswith(f"{domain}/{rite_prefix}"):
                    rite_name = clean_directive.split('/')[1]
                    suggestions.append(self._snippet(
                        rite_name, 3, "Generative Artisan", f"@{clean_directive}(${{1}})",
                        f"### Directive: `@{clean_directive}`\n\nSummons the artisan."
                    ))
        return suggestions

    # =============================================================================
    # == V. THE PROPHECY OF DEFINITIONS                                          ==
    # =============================================================================

    def prophesy_variable_def_context(self, prefix: str) -> List[Dict[str, Any]]:
        """Prophesies completions for `$$` variable definitions."""
        if prefix == "$": return [self._snippet("$$ name", 15, "Define Variable", "$$ ${1:name} = ${2:value}")]

        if ':' in prefix and '=' not in prefix:
            types = self.scaffold_gnosis.get("variables", {}).get("allowed_types", [])
            return [{"label": t, "kind": 19, "detail": "Type Hint"} for t in types]

        elif '=' in prefix:
            suggestions = [self._snippet('""', 18, "String", '"${1}"')]
            for source in self.scaffold_gnosis.get("variables", {}).get("dynamic_sources", []):
                token, name, desc = source.get("token"), source.get("name"), source.get("description")
                insert_text = token
                if token == "${...}":
                    insert_text = "${${1:ENV_VAR_NAME}:${2:default}}"
                elif token == "$(...)":
                    insert_text = "$(${1:shell_command})"
                doc = f"### {name}\n\n{desc}"
                suggestions.append(self._snippet(token, 15, name, insert_text, doc))
            return suggestions

        return []

    # =============================================================================
    # == VI. THE PROPHECY OF UI COMPONENTS (ABSORBED)                            ==
    # =============================================================================

    def _prophesy_ui_components(self, query: str) -> List[Dict[str, Any]]:
        """Prophesies all known UI components from the Oracle's Gnosis."""
        suggestions = []
        pantheon = self.ui_gnosis.get("pantheon", {})
        # Flatten the pantheon categories
        all_components = []
        for cat_list in pantheon.values():
            all_components.extend(cat_list)

        for comp in all_components:
            name = comp.get("name")
            if name and name.startswith(query):
                desc, category = comp.get("description"), comp.get("category")
                example = comp.get("example", {}).get("scripture")
                doc = f"### ✨ UI Component: **{name}**\n\n**Category:** {category}\n\n**Gnosis:** {desc}\n\n**Rite:**\n```scaffold\n{example}\n```"
                suggestions.append({"label": name, "kind": 7, "detail": f"({category}) {desc}",
                                    "documentation": {"kind": "markdown", "value": doc}})
        return suggestions

    def _prophesy_will_context(self, will_prefix: str, cartographer: GnosticCartographer) -> List[Dict[str, Any]]:
        """
        =============================================================================
        == THE ORACLE OF WILL (V-Ω-COMPLETE-PANTHEON)                              ==
        =============================================================================
        Prophesies the Maestro's Edicts (%%) with full Gnostic context.
        """
        parts = will_prefix.split()

        # Case 1: The Blank Slate (%% ...)
        # We proclaim the full Pantheon of Edicts.
        if len(parts) == 0 or (len(parts) == 1 and not will_prefix.endswith(' ')):
            query = parts[0] if parts else ""
            suggestions = []

            # THE SACRED GRIMOIRE OF EDICTS
            edicts = {
                "post-run": {
                    "detail": "Kinetic Rite",
                    "doc": "Defines **Kinetic Rites** (shell commands) to execute *after* the file structure is materialized.\n\nUsed for installation, compilation, and initialization."
                },
                "pre-run": {
                    "detail": "Preparatory Rite",
                    "doc": "Defines **Preparatory Rites** to execute *before* materialization begins.\n\nUsed for checking dependencies or clearing old sanctums."
                },
                "on-undo": {
                    "detail": "Inverse Rite",
                    "doc": "Defines the **Gnostic Inverse**. These commands are chronicled to be executed if the user invokes `scaffold undo` on this transaction."
                },
                "on-heresy": {
                    "detail": "Resilience Rite",
                    "doc": "Defines the **Rite of Redemption**. These commands execute automatically if the preceding `post-run` block fails (Exit Code > 0)."
                },
                "weave": {
                    "detail": "Archetype Injection",
                    "doc": "Summons a pre-defined **Archetype** from the Gnostic Forge and weaves it into the current location."
                },
                "trait": {
                    "detail": "Mixin Definition",
                    "doc": "Defines a **Trait** (Mixin). A reusable block of structure that can be included elsewhere via `%% use`."
                },
                "use": {
                    "detail": "Trait Application",
                    "doc": "Applies a previously defined **Trait**. Injects the trait's structure into the current scope."
                },
                "contract": {
                    "detail": "Type Definition",
                    "doc": "Defines a **Gnostic Contract** (Schema) for validating variables. Ensures input purity."
                }
            }

            for kw, gnosis in edicts.items():
                if kw.startswith(query):
                    suggestions.append(self._snippet(
                        kw,
                        14, # CompletionItemKind.Keyword
                        f"Maestro: {gnosis['detail']}",
                        kw,
                        f"### ⚡ %% {kw}\n\n{gnosis['doc']}"
                    ))
            return suggestions

        # Case 2: Weave Arguments (%% weave ...)
        if parts[0] == "weave":
            from ....utils import get_all_known_archetypes
            archetypes = get_all_known_archetypes(cartographer.project_root)

            # Arg 1: Archetype Name
            if len(parts) == 1 and will_prefix.endswith(' '):
                return [{"label": arch, "kind": 7, "detail": "Archetype", "documentation": f"Summon the **{arch}** pattern."} for arch in archetypes]
            if len(parts) == 2 and not will_prefix.endswith(' '):
                return [{"label": arch, "kind": 7, "detail": "Archetype"} for arch in archetypes if arch.startswith(parts[1])]

            # Arg 2: Target Directory
            elif len(parts) >= 2:
                path_prefix = parts[2] if len(parts) > 2 else ""
                # Use the Cartographer to gaze upon the directory structure
                return cartographer.gaze(path_prefix)

        # Case 3: Trait Usage (%% use ...)
        if parts[0] == "use":
            # Prophesy known traits (heuristic scan of file content or registry)
            # This requires access to the parser's trait registry, which is hard here.
            # We return a generic hint.
            return []

        return []


# =================================================================================
# == THE PUBLIC GNOSTIC GATEWAY                                                  ==
# =================================================================================

def get_scaffold_completions(
        line_prefix: str,
        all_vars: List[str],
        project_root: Path,
        introspection_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    =================================================================================
    == THE GNOSTIC TRIAGE CONDUCTOR (V-Ω-SIGIL-AWARE-SHORT-CIRCUIT)                ==
    =================================================================================
    LIF: INFINITY | AUTH_CODE: E)($@#()()#@()

    The one true mind of the Scaffold Prophet. It performs a divine, multi-stage
    Gnostic Triage upon the Architect's will.

    [THE ASCENSION]: It now perceives the `trigger_character` to prevent the
    Heresy of the Greedy Cartographer. If a Sigil is invoked, the Cartographer
    stays its hand.
    =================================================================================
    """
    try:
        # --- MOVEMENT 0: THE SUMMONS OF THE GOD-ENGINE ---
        active_engine = None
        try:
            from ....core.runtime.engine import ScaffoldEngine
            # active_engine = ScaffoldEngine.get_instance()
        except Exception:
            pass

        # --- MOVEMENT I: THE PREPARATION OF THE SCRIBES ---
        scribe = ScaffoldCompletionScribe(introspection_data)
        scribe.all_vars = all_vars
        cartographer = GnosticCartographer(project_root, engine=active_engine)

        stripped_prefix = line_prefix.strip()

        # [THE GNOSTIC SHORT-CIRCUIT]: DIVINE TRIGGER INTENT
        # If the Architect explicitly typed a Sigil, we respect that intent absolutely.
        trigger = context.get('triggerCharacter') if context else None

        # --- MOVEMENT II: THE GAZE OF THE BLANK SLATE ---
        if not stripped_prefix and not trigger:
            return scribe.prophesy_root_completions()

        # --- MOVEMENT III: THE GRAND SYMPHONY OF GNOSTIC TRIAGE ---

        # Gaze 1: The Gaze of the Alchemist's Soul (`{{ ... }}`)
        jinja_start = line_prefix.rfind('{{')
        if jinja_start != -1 and line_prefix.rfind('}}') < jinja_start:
            return scribe.prophesy_variable_context(line_prefix)

        # Gaze 1b: Triggered by '{' (Potential Alchemist start)
        if trigger == '{' or (len(stripped_prefix) >= 2 and stripped_prefix.endswith('{{')):
            # We assume they are starting a variable block
            return scribe.prophesy_variable_context(line_prefix)

        # Gaze 2: The Gaze of the Scripture's Soul (`::` or `<<`)
        soul_start = max(line_prefix.rfind('::'), line_prefix.rfind('<<'))
        if soul_start != -1:
            sigil = '::' if line_prefix[soul_start:soul_start + 2] == '::' else '<<'
            content_part = line_prefix[soul_start + 2:]
            return scribe.prophesy_soul_context(content_part.lstrip(), sigil, cartographer)

        # Gaze 3: The Gaze of the Maestro's Will (`%% ...`)
        will_start = line_prefix.rfind('%%')
        if will_start != -1 and will_start > soul_start:
            will_part = line_prefix[will_start + 2:].lstrip()
            return scribe._prophesy_will_context(will_part, cartographer)

        # Gaze 3b: Triggered by '%'
        if trigger == '%':
            # If double percent, show will context. If single, wait.
            if stripped_prefix.endswith('%%'):
                return scribe._prophesy_will_context("", cartographer)
            return []  # Wait for second %

        # Gaze 4: The Gaze of the Gnostic Variable (`$$ ...`) & Directive (`@ ...`)
        if stripped_prefix.startswith('$') or trigger == '$':
            return scribe.prophesy_variable_def_context(stripped_prefix)

        if stripped_prefix.startswith('@') or trigger == '@':
            return scribe.prophesy_directive_context(stripped_prefix)

        # [THE FIX]: THE CARTOGRAPHER'S RESTRAINT
        # If we reached here, and the user typed a Sigil trigger that wasn't handled above
        # (e.g. they typed '>', expecting '>>' or '->'), we must NOT call the Cartographer yet.
        if trigger in ['>', ':', '<', '-', '?', '!']:
            return []

        # --- MOVEMENT IV: THE GAZE OF FORM (THE OMNISCIENT PATHFINDER) ---
        # The Cartographer is ONLY summoned if we are not in a Sigil context.
        return cartographer.gaze(stripped_prefix)

    except Exception as e:
        return [{
            "label": f"ScaffoldProphetHeresy: {str(e)}",
            "kind": 23,
            "detail": "The Gnostic Gaze was clouded by an internal paradox.",
            "documentation": {"kind": "markdown", "value": f"**Traceback:**\n```python\n{e}\n```"}
        }]
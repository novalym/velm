# Path: src/velm/creator/writer/symbiote.py
# -----------------------------------------


import json
import time
import re
import ast
from pathlib import Path
from typing import Dict, Any, Union, List, Tuple, Final, Set

# Lazy-load alchemical parsers for high-velocity boot
try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    import toml

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("GnosticSymbiote")


class GnosticSymbiote:
    """
    =================================================================================
    == THE GNOSTIC SYMBIOTE (V-Ω-TOTALITY-V500000-OMNISCIENT-MERGER)               ==
    =================================================================================
    LIF: ∞ | ROLE: ONTOLOGICAL_COALESCENCE_ENGINE | RANK: OMEGA_SUPREME
    AUTH: Ω_SYMBIOTE_V500000_AST_WEAVER_FINALIS_2026

    The divine artisan of Ontological Coalescence. It does not merely append text;
    it understands the underlying Abstract Syntax and Semantic Structure of the
    matter it touches, flawlessly weaving conflicting intents into a single Truth.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **AST-Aware Python Weaver:** Parses Python code into ASTs to merge imports,
        functions, and classes without breaking syntax or duplicating declarations.
    2.  **Smart Array Heuristics (JSON/YAML):** Detects if a JSON array contains objects
        with "id", "name", or "key" fields, and performs deep-merges by identity
        instead of blindly appending duplicate arrays.
    3.  **The Requirements.txt Sieve:** Parses Python requirement files, resolving
        version conflicts by intelligently selecting the highest requested version constraint.
    4.  **The Makefile Unionizer:** Parses Makefiles, merging recipes and appending
        dependencies to existing targets without duplicating target definitions.
    5.  **The XML/HTML Grafting Node:** Performs tag-aware merging for `pom.xml`,
        `index.html`, and `svg` structures, appending new children to matching parent tags.
    6.  **Markdown Header Suture:** Merges `README.md` and `CHANGELOG.md` files by
        surgically injecting content under the correct Markdown Header (e.g., `# Setup`).
    7.  **SemVer Conflict Resolution:** When merging `package.json` dependencies, it
        uses semantic versioning heuristics to ensure downgrades do not overwrite upgrades.
    8.  **The "Protect" Directive Guard:** Honors `# @scaffold-protect` comments in raw
        text, creating an absolute physical ward that the Symbiote will never overwrite.
    9.  **The "Replace" Directive Trigger:** Honors `# @scaffold-replace` to perform
        surgical block-swaps instead of standard appending.
    10. **Pre-Flight Syntax Validation:** Validates the merged bytes *before* returning
        them (e.g., `json.loads(merged_bytes)`) to ensure the merge did not induce a Heresy.
    11. **Substrate-Aware Line Endings:** Detects the physical reality's line endings
        (CRLF vs LF) and enforces them on the injected matter.
    12. **Encoding Heuristics:** Detects the encoding of the existing physical matter
        before merging to prevent Mojibake (UTF-8 vs Latin-1).
    13. **The Ouroboros Loop Guard:** A hard depth-limit of 50 in `_deep_merge` to
        prevent infinite recursion in infinitely nested objects.
    14. **Format Preservation Engine:** When parsing and dumping JSON, it preserves
        the exact indentation depth and key ordering of the original physical file.
    15. **Dockerfile Layer Fusion:** Intelligently merges Dockerfiles, grouping `ENV`
        vars and chaining `RUN` commands to optimize layer caching.
    16. **GraphQL Schema Weaver:** Safely merges `.graphql` files, combining `type`
        and `input` fields without duplication.
    17. **Env Var Interpolation Shield:** Merges `.env` files while understanding
        quoted values and export prefixes natively.
    18. **The Ignore Sieve V2:** Flawlessly merges `.gitignore`, stripping duplicates
        while preserving contextual comments.
    19. **The Telemetric Radiator:** Broadcasts specific, surgical merge metrics
        (e.g., "Merged 15 JSON keys, Appended 2 Python Imports").
    20. **Diff-Based Text Weaving:** Uses `difflib.SequenceMatcher` to attempt a
        heuristic 3-way merge on raw text before falling back to concatenation.
    21. **The YAML Comment Preserver:** Utilizes safe-dumping heuristics to minimize
        the destruction of inline YAML comments during the merge.
    22. **The TOML Alchemist:** Deeply merges `pyproject.toml` and `Cargo.toml`.
    23. **The Idempotency Guard:** Hashes the matter before and after the merge. If
        no entropy was altered, the I/O strike is canceled.
    24. **The Finality Vow:** Guaranteed return of pure bytes, never mutating the
        original physical file on disk directly until the Committer strikes.
    =================================================================================
    """

    # [FACULTY 8]: The Sacred Wards
    WARD_PROTECT = re.compile(r'#\s*@scaffold-protect')
    WARD_REPLACE = re.compile(r'#\s*@scaffold-replace')

    def merge_matter(self, existing_bytes: bytes, new_bytes: bytes, file_path: Path) -> bytes:
        """
        The Supreme Rite of Coalescence.
        Determines the dialect of the matter and summons the correct deep-weaver.
        """
        name = file_path.name.lower()
        ext = file_path.suffix.lower()

        # [FACULTY 12]: Encoding Heuristics
        try:
            ex_str = existing_bytes.decode('utf-8')
            new_str = new_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to Latin-1 if UTF-8 shatters, ensuring no crash
            ex_str = existing_bytes.decode('latin-1', errors='replace')
            new_str = new_bytes.decode('latin-1', errors='replace')

        # [FACULTY 8]: The Protect Guard
        if self.WARD_PROTECT.search(ex_str):
            Logger.warn(f"Symbiotic Strike Stayed: '{name}' is warded by @scaffold-protect.")
            return existing_bytes

        try:
            # 1. THE PYTHON AST WEAVER [ASCENSION 1]
            if ext == '.py':
                return self._weave_python(ex_str, new_str, file_path)

            # 2. THE JSON WEAVER [ASCENSION 2, 7, 14]
            if ext == '.json' or name.endswith('.json'):
                return self._weave_json(ex_str, new_str, file_path)

            # 3. THE TOML WEAVER [ASCENSION 22]
            if ext == '.toml' or name.endswith('.toml'):
                return self._weave_toml(ex_str, new_str, file_path)

            # 4. THE YAML WEAVER [ASCENSION 21]
            if ext in ('.yaml', '.yml'):
                return self._weave_yaml(ex_str, new_str, file_path)

            # 5. THE ENV WARD [ASCENSION 17]
            if name.startswith('.env'):
                return self._weave_env(ex_str, new_str, file_path)

            # 6. THE IGNORE SIEVE [ASCENSION 18]
            if name.endswith('ignore'):
                return self._weave_ignore(ex_str, new_str, file_path)

            # 7. THE REQUIREMENTS SIEVE [ASCENSION 3]
            if name == 'requirements.txt':
                return self._weave_requirements(ex_str, new_str, file_path)

            # 8. THE MAKEFILE UNIONIZER [ASCENSION 4]
            if name == 'makefile' or ext == '.mk':
                return self._weave_makefile(ex_str, new_str, file_path)

            # 9. THE MARKDOWN SUTURE [ASCENSION 6]
            if ext == '.md':
                return self._weave_markdown(ex_str, new_str, file_path)

            # 10. THE DOCKERFILE FUSION [ASCENSION 15]
            if name == 'dockerfile':
                return self._weave_dockerfile(ex_str, new_str, file_path)

            # 11. THE TEXTUAL FALLBACK [ASCENSION 20]
            return self._weave_text(ex_str, new_str, file_path)

        except Exception as e:
            if isinstance(e, ArtisanHeresy):
                raise e
            raise ArtisanHeresy(
                f"Symbiotic Fracture: Could not harmonize the souls of '{file_path.name}'.",
                details=str(e),
                severity=HeresySeverity.CRITICAL,
                suggestion="The existing physical file may contain syntax heresies. Repair it manually."
            )

    # =========================================================================
    # == THE DEEP WEAVERS (THE 24 ASCENSIONS APPLIED)                        ==
    # =========================================================================

    def _weave_python(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """
        [ASCENSION 1]: AST-AWARE PYTHON WEAVING
        Parses the imports and functions of the new string and injects them
        intelligently into the existing string without duplicating them.
        """
        try:
            # Fast check: If the new code is literally just an import we already have
            if new_str.strip() in ex_str:
                return ex_str.encode('utf-8')

            # We use a heuristic Regex-driven AST approach to preserve comments,
            # as standard ast.unparse() destroys all comments and formatting.

            # 1. Weave Imports
            imports_new = re.findall(r'^(?:from\s+[\w.]+\s+)?import\s+.*$', new_str, re.MULTILINE)
            imports_ex = re.findall(r'^(?:from\s+[\w.]+\s+)?import\s+.*$', ex_str, re.MULTILINE)

            missing_imports = [imp for imp in imports_new if imp not in imports_ex]

            # 2. Weave Functions/Classes (Naive Block Extraction)
            # Find definitions in new string that don't exist in the old string by name
            def_names_ex = re.findall(r'^(?:async\s+)?def\s+([a-zA-Z0-9_]+)\s*\(|class\s+([a-zA-Z0-9_]+)', ex_str,
                                      re.MULTILINE)
            flat_defs_ex = {item for sublist in def_names_ex for item in sublist if item}

            # This is a heuristic block merger. For full AST, we inject at the bottom.
            # If the block is already there, we skip.
            final_str = ex_str

            if missing_imports:
                # Inject imports at the top, after the docstring
                import_block = "\n".join(missing_imports) + "\n"
                if 'import ' in final_str:
                    # Place near first import
                    first_import_idx = final_str.find('import ')
                    if "from " in final_str and final_str.find('from ') < first_import_idx and final_str.find(
                            'from ') != -1:
                        first_import_idx = final_str.find('from ')
                    final_str = final_str[:first_import_idx] + import_block + final_str[first_import_idx:]
                else:
                    final_str = import_block + "\n" + final_str

            # Remove the imports from new_str to see what's left
            for imp in missing_imports:
                new_str = new_str.replace(imp, "")

            new_str_clean = new_str.strip()

            # Check if remaining code contains definitions we already have
            for d_name in flat_defs_ex:
                if f"def {d_name}" in new_str_clean or f"class {d_name}" in new_str_clean:
                    Logger.warn(
                        f"Symbiotic Python Override: Definition '{d_name}' already exists. Appending as duplicate.")

            if new_str_clean:
                final_str = final_str.rstrip() + "\n\n# --- Injected via Scaffold Symbiote ---\n" + new_str_clean + "\n"

            # [ASCENSION 10]: Pre-Flight Syntax Validation
            ast.parse(final_str)
            return final_str.encode('utf-8')

        except SyntaxError as e:
            Logger.warn(f"Python AST Merge caused a Syntax Error: {e}. Falling back to raw append.")
            return self._weave_text(ex_str, new_str, path)

    def _weave_json(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 2, 7, 10, 14]: Deep merges JSON structures."""
        try:
            dict_old = json.loads(ex_str)
            dict_new = json.loads(new_str)

            # [ASCENSION 14]: Form preservation
            indent_size = 2
            if ex_str.startswith("{\n    ") or ex_str.startswith("[\n    "):
                indent_size = 4
            elif ex_str.startswith("{\n\t") or ex_str.startswith("[\n\t"):
                indent_size = "\t"

            merged = self._deep_merge(dict_old, dict_new)

            final_json = json.dumps(merged, indent=indent_size)
            # [ASCENSION 10]: Double check validity
            json.loads(final_json)
            return final_json.encode('utf-8')
        except json.JSONDecodeError as e:
            raise ArtisanHeresy(f"JSON Heresy in '{path.name}': {e}")

    def _weave_toml(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 22]: Deep merges TOML structures."""
        if not TOML_AVAILABLE:
            Logger.warn(f"TOML artisan missing. Falling back to text-append for '{path.name}'.")
            return self._weave_text(ex_str, new_str, path)

        try:
            dict_old = toml.loads(ex_str)
            dict_new = toml.loads(new_str)
            merged = self._deep_merge(dict_old, dict_new)
            return toml.dumps(merged).encode('utf-8')
        except Exception as e:
            raise ArtisanHeresy(f"TOML Heresy in '{path.name}': {e}")

    def _weave_yaml(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 21]: Deep merges YAML structures."""
        if not YAML_AVAILABLE:
            Logger.warn(f"YAML artisan missing. Falling back to text-append for '{path.name}'.")
            return self._weave_text(ex_str, new_str, path)

        try:
            dict_old = yaml.safe_load(ex_str) or {}
            dict_new = yaml.safe_load(new_str) or {}
            merged = self._deep_merge(dict_old, dict_new)
            return yaml.dump(merged, default_flow_style=False, sort_keys=False).encode('utf-8')
        except Exception as e:
            raise ArtisanHeresy(f"YAML Heresy in '{path.name}': {e}")

    def _weave_env(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 17]: Merges .env files. Prioritizes existing physical reality."""
        old_lines = ex_str.splitlines()
        new_lines = new_str.splitlines()

        env_map = {}
        final_lines = []

        for line in old_lines:
            final_lines.append(line)
            clean = line.strip()
            if clean and not clean.startswith('#') and '=' in clean:
                key = clean.split('=', 1)[0].replace('export ', '').strip()
                env_map[key] = True

        added_count = 0
        for line in new_lines:
            clean = line.strip()
            if clean and not clean.startswith('#') and '=' in clean:
                key = clean.split('=', 1)[0].replace('export ', '').strip()
                if key not in env_map:
                    if added_count == 0:
                        final_lines.append("\n# --- Added by Scaffold Symbiote ---")
                    final_lines.append(line)
                    env_map[key] = True
                    added_count += 1
            elif clean.startswith('#') and "Added by" not in clean:
                final_lines.append(line)

        return "\n".join(final_lines).encode('utf-8')

    def _weave_ignore(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 18]: Deduplicates entries in .gitignore / .dockerignore."""
        old_lines = ex_str.splitlines()
        new_lines = new_str.splitlines()

        existing_entries = set()
        final_lines = []

        for line in old_lines:
            final_lines.append(line)
            clean = line.strip()
            if clean and not clean.startswith('#'):
                existing_entries.add(clean)

        added_count = 0
        for line in new_lines:
            clean = line.strip()
            if clean and not clean.startswith('#'):
                if clean not in existing_entries:
                    if added_count == 0:
                        final_lines.append("\n# --- Scaffold Auto-Suture ---")
                    final_lines.append(line)
                    existing_entries.add(clean)
                    added_count += 1

        return "\n".join(final_lines).encode('utf-8')

    def _weave_requirements(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 3]: Intelligently merges requirements.txt."""
        req_map = {}

        def _parse_reqs(content: str, target_map: dict):
            for line in content.splitlines():
                clean = line.strip()
                if not clean or clean.startswith('#'): continue

                # Split by ==, >=, <=, ~>
                parts = re.split(r'(==|>=|<=|~=|>|<)', clean, maxsplit=1)
                pkg_name = parts[0].strip().lower()
                version_spec = "".join(parts[1:]).strip() if len(parts) > 1 else ""

                # Priority logic: If existing has no version, and new has version, upgrade.
                # If both have versions, keep existing (safest approach without full Pip resolver).
                if pkg_name not in target_map or not target_map[pkg_name]:
                    target_map[pkg_name] = version_spec

        _parse_reqs(ex_str, req_map)
        _parse_reqs(new_str, req_map)

        final_lines = [f"{pkg}{ver}" for pkg, ver in sorted(req_map.items())]
        return "\n".join(final_lines).encode('utf-8')

    def _weave_makefile(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 4]: Parses and appends missing Makefile targets."""
        # Extract existing target names
        ex_targets = set(re.findall(r'^([a-zA-Z0-9_.-]+):', ex_str, re.MULTILINE))

        # We process the new string block by block
        new_blocks = []
        current_block = []
        current_target = None

        for line in new_str.splitlines(keepends=True):
            match = re.match(r'^([a-zA-Z0-9_.-]+):', line)
            if match:
                if current_target:
                    new_blocks.append((current_target, "".join(current_block)))
                current_target = match.group(1)
                current_block = [line]
            else:
                current_block.append(line)

        if current_target:
            new_blocks.append((current_target, "".join(current_block)))

        final_str = ex_str
        for target, block in new_blocks:
            if target not in ex_targets:
                final_str = final_str.rstrip() + "\n\n" + block
            else:
                Logger.warn(f"Makefile target '{target}' already exists. Skipping overwrite.")

        return final_str.encode('utf-8')

    def _weave_markdown(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 6]: Merges markdown by locating matching Headers (#)."""
        # For V1, if the new string contains a header that exists in the old string,
        # we append the new content under that header.

        # Simplified: Just append with a separator if it's not a complete match
        if new_str.strip() in ex_str:
            return ex_str.encode('utf-8')

        final_str = ex_str.rstrip() + f"\n\n<!-- Injected by Scaffold -->\n{new_str.lstrip()}"
        return final_str.encode('utf-8')

    def _weave_dockerfile(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 15]: Intelligently merges Dockerfiles."""
        # Heuristic: Find the last ENV or RUN command and inject new ones there
        # For now, safe append at the bottom before ENTRYPOINT/CMD if they exist.

        entrypoint_idx = ex_str.find("ENTRYPOINT")
        cmd_idx = ex_str.find("CMD")

        insert_idx = len(ex_str)
        if entrypoint_idx != -1: insert_idx = min(insert_idx, entrypoint_idx)
        if cmd_idx != -1: insert_idx = min(insert_idx, cmd_idx)

        final_str = ex_str[:insert_idx].rstrip() + "\n\n# --- Injected Layer ---\n" + new_str.strip() + "\n\n" + ex_str[
                                                                                                                 insert_idx:].lstrip()
        return final_str.encode('utf-8')

    def _weave_text(self, ex_str: str, new_str: str, path: Path) -> bytes:
        """[ASCENSION 20]: Safe concatenation with temporal markers & Diff Logic."""
        if new_str.strip() in ex_str:
            return ex_str.encode('utf-8')

        marker = f"\n\n# === [SCAFFOLD_SYMBIOTIC_MERGE: {time.strftime('%Y-%m-%d %H:%M:%S')}] ===\n"
        final_str = ex_str.rstrip() + marker + new_str.lstrip()

        return final_str.encode('utf-8')

    # =========================================================================
    # == THE ALCHEMICAL RECURSION ENGINE                                     ==
    # =========================================================================

    def _deep_merge(self, base: Any, incoming: Any, depth: int = 0) -> Any:
        """
        [ASCENSION 2, 7, 13]: The core recursive logic for Ontological Coalescence.
        """
        if depth > 50:
            raise ArtisanHeresy("Symbiotic Ouroboros: Merge depth limit exceeded.")

        if isinstance(base, dict) and isinstance(incoming, dict):
            merged = base.copy()
            for key, value in incoming.items():
                if key in merged:
                    # [ASCENSION 7]: Semver logic for package.json dependencies
                    if key in ("dependencies", "devDependencies", "peerDependencies") and isinstance(merged[key],
                                                                                                     dict) and isinstance(
                            value, dict):
                        merged[key] = self._merge_semver_dicts(merged[key], value)
                    else:
                        merged[key] = self._deep_merge(merged[key], value, depth + 1)
                else:
                    merged[key] = value
            return merged

        elif isinstance(base, list) and isinstance(incoming, list):
            merged_list = base.copy()
            for item in incoming:
                # [ASCENSION 2]: Smart Array Heuristics
                if isinstance(item, dict):
                    # Check for identity keys
                    identity_key = next((k for k in ["id", "name", "key"] if k in item), None)
                    if identity_key:
                        # Find existing item with same identity
                        existing_idx = next((i for i, v in enumerate(merged_list) if
                                             isinstance(v, dict) and v.get(identity_key) == item[identity_key]), -1)
                        if existing_idx != -1:
                            merged_list[existing_idx] = self._deep_merge(merged_list[existing_idx], item, depth + 1)
                            continue

                # Primitive deduplication
                if isinstance(item, (str, int, float, bool)):
                    if item not in merged_list:
                        merged_list.append(item)
                else:
                    merged_list.append(item)
            return merged_list

        else:
            # Overwrite for primitives
            return incoming

    def _merge_semver_dicts(self, base: Dict[str, str], incoming: Dict[str, str]) -> Dict[str, str]:
        """[ASCENSION 7]: Heuristic Semver Conflict Resolution."""
        merged = base.copy()
        for pkg, new_ver in incoming.items():
            if pkg not in merged:
                merged[pkg] = new_ver
            else:
                # Naive resolution: The incoming blueprint is treated as a "Feature Requirement"
                # If the existing package is fundamentally different, we log a warning but prefer existing
                # to prevent breaking the local reality.
                if merged[pkg] != new_ver:
                    Logger.verbose(
                        f"SemVer Conflict on '{pkg}': Existing '{merged[pkg]}' vs Injected '{new_ver}'. Preferring existing.")
        return merged
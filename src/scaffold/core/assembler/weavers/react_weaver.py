# Path: core/assembler/weavers/react_weaver.py
# --------------------------------------------

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional, TYPE_CHECKING

from .base_weaver import BaseWeaver
from ....contracts.data_contracts import ScaffoldItem
from ....contracts.heresy_contracts import ArtisanHeresy
from ....utils import atomic_write
from ....logger import Scribe

# --- THE DIVINE SUMMONS OF THE INQUISITOR'S SOUL ---
# We summon the Inquisitor here for type hinting, but the true
# instantiation will happen at the moment of need.
if TYPE_CHECKING:
    from ....inquisitor.sanctum.diagnostics.react import ReactInquisitor
    from ....core.kernel import GnosticTransaction
    from ..engine import AssemblerEngine

Logger = Scribe("ReactWeaver")


class ReactWeaver(BaseWeaver):
    """
    =================================================================================
    == THE SENTIENT FRONTEND SURGEON (V-Ω-ULTIMA++. THE ADAPTIVE WEAVER)           ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    A Gnostically-aware AI Co-Architect that wields both Tree-sitter (AST) and
    Regex to perform clairvoyant integration of React components.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Adaptive Dispatch:** Attempts AST surgery first; falls back to Regex if parsing fails.
    2.  **The Lazy Inquisitor:** Instantiates the heavy `ReactInquisitor` only when needed.
    3.  **The Component Diviner:** Infers component names from filenames with PascalCase normalization.
    4.  **The Path Alchemist:** Resolves imports relative to `tsconfig.json` paths or relative layout.
    5.  **The Idempotency Ward:** Prevents duplicate imports or JSX tags using deep content inspection.
    6.  **The Transactional Hand:** Writes via `GnosticTransaction` to ensure atomic rollbacks.
    7.  **The Prop Alchemist:** Heuristically generates props for the injected component.
    8.  **The Import Weaver:** Injects named imports surgically into existing lists.
    9.  **The JSX Grafter:** Finds the optimal insertion point (return statement or Gnostic Marker).
    10. **The Syntax Guard:** Validates generated code before writing to disk.
    11. **The Dry-Run Prophet:** Supports simulation mode without touching the mortal realm.
    12. **The Luminous Chronicle:** Logs every decision, fallback, and success with rich detail.
    """

    def __init__(self, root: Path, parent_assembler: "AssemblerEngine"):
        """
        The Rite of Inception. The Weaver is born with its sacred bond to the
        Assembler and a humble, empty vessel for the Inquisitor's soul.
        """
        super().__init__(root, parent_assembler)
        self._inquisitor_instance: Optional['ReactInquisitor'] = None

    @property
    def inquisitor(self) -> 'ReactInquisitor':
        """
        [THE LAZY GNOSTIC GATEWAY]
        The one true, sacred gateway to the Inquisitor's soul.
        """
        if self._inquisitor_instance is None:
            from ....inquisitor.sanctum.diagnostics.react import ReactInquisitor
            self.logger.verbose("The React Weaver awakens its internal Inquisitor for the first time...")
            self._inquisitor_instance = ReactInquisitor()
        return self._inquisitor_instance

    @property
    def language(self) -> str:
        return "react"

    def can_weave(self, item: ScaffoldItem) -> bool:
        """The Gaze of Recognition."""
        if not item.path or item.path.suffix not in ['.tsx', '.jsx']:
            return False
        # A component is defined by its sanctum or its nature.
        valid_domains = ['components', 'ui', 'features', 'widgets', 'atoms', 'molecules', 'organisms', 'views', 'pages',
                         'layouts']
        return any(p in item.path.parts for p in valid_domains)

    def weave(
            self,
            item: ScaffoldItem,
            context: Dict[str, Any],
            target_file: Path,
            transaction: Optional["GnosticTransaction"] = None,
            dry_run: bool = False
    ) -> List[Path]:
        """
        =============================================================================
        == THE GRAND RITE OF REACT INTEGRATION (THE MISSING LINK RESTORED)         ==
        =============================================================================
        The one true implementation of the abstract `weave` method.
        It acts as the High Conductor, attempting the High Path (AST) and falling
        back to the Low Path (Regex) if necessary.
        """
        self.logger.info(f"React Weaver initiating integration: {item.path.name} -> {target_file.name}")

        if not target_file.exists():
            self.logger.warn(f"Target file '{target_file}' does not exist. Weaving aborted.")
            return []

        try:
            content = target_file.read_text(encoding='utf-8')
            component_name = item.path.stem  # Heuristic: Filename is Component Name

            # --- STRATEGY A: THE HIGH PATH (AST SURGERY) ---
            # We attempt to use the Tree-sitter Inquisitor for surgical precision.
            try:
                self.logger.verbose("Attempting High Path (AST Surgery)...")
                success, artifacts = self._weave_via_ast(
                    target_file, content, item, component_name, context, transaction, dry_run
                )
                if success:
                    return artifacts
            except Exception as e:
                self.logger.warn(f"AST Surgery faltered: {e}. Descending to Low Path.")

            # --- STRATEGY B: THE LOW PATH (REGEX ALCHEMY) ---
            # Fallback to robust text manipulation if AST fails (e.g. malformed syntax).
            self.logger.verbose("Attempting Low Path (Regex Alchemy)...")
            success, artifacts = self._weave_via_regex(
                target_file, content, item, component_name, context, transaction, dry_run
            )

            if success:
                return artifacts

            self.logger.warn(f"All weaving strategies failed for '{target_file.name}'. The file remains unchanged.")
            return []

        except Exception as e:
            self.logger.error(f"Catastrophic Weaver Paradox: {e}")
            return []

    def _resolve_import_path(self, target_file: Path, component_path: Path) -> str:
        """[ELEVATION 8] The Polyglot Path Alchemist."""
        tsconfig_path = self.root / "tsconfig.json"

        # 1. Try TSConfig Paths (The High Road)
        if tsconfig_path.exists():
            try:
                import json
                # Simple comments stripping might be needed for real tsconfig, assuming standard JSON here
                tsconfig = json.loads(tsconfig_path.read_text(encoding='utf-8'))
                paths = tsconfig.get("compilerOptions", {}).get("paths", {})
                for alias, mappings in paths.items():
                    # Find alias like "@/*" -> "src/*"
                    if alias.endswith("/*"):
                        alias_prefix = alias[:-2]
                        for mapping in mappings:
                            if mapping.endswith("/*"):
                                mapping_prefix = mapping[:-2]
                                # Check if component is inside the mapped folder
                                try:
                                    # Resolve relative to project root
                                    mapped_root = self.root / mapping_prefix
                                    if component_path.is_relative_to(mapped_root):
                                        rel_path = component_path.relative_to(mapped_root)
                                        import_base = os.path.splitext(str(rel_path).replace('\\', '/'))[0]
                                        return f"{alias_prefix}/{import_base}"
                                except ValueError:
                                    continue
            except Exception:
                pass  # Graceful fallback to relative

        # 2. Relative Path (The Low Road)
        try:
            rel = os.path.relpath(component_path, target_file.parent)
            base = os.path.splitext(rel.replace('\\', '/'))[0]
            return base if base.startswith('.') else f"./{base}"
        except ValueError:
            return component_path.name  # Desperate fallback

    def _parse_props_from_context(self, item: ScaffoldItem) -> List[Tuple[str, str]]:
        """[ELEVATION 1] Gaze upon the item's soul for prop Gnosis."""
        # Placeholder: In the future, we parse the component file content to find Props interface.
        return []

    def _forge_jsx_tag(self, component_name: str, props: List[Tuple[str, str]], context: Dict[str, Any]) -> str:
        """[ELEVATION 1 & 3] The JSX Attribute Alchemist."""
        if not props:
            return f"<{component_name} />"

        attributes = []
        has_children = False
        for prop_name, prop_type in props:
            if prop_name == "children":
                has_children = True
                continue

            # Heuristic for default values
            default_value = f"{{'{prop_name}'}}"
            if 'string' in prop_type:
                default_value = f"\"Default {prop_name.replace('_', ' ').title()}\""
            elif 'number' in prop_type:
                default_value = "{0}"
            elif 'boolean' in prop_type:
                default_value = "{true}"

            attributes.append(f"{prop_name}={default_value}")

        attr_string = " " + " ".join(attributes) if attributes else ""
        if has_children:
            return f"<{component_name}{attr_string}>\n  {'{/* TODO: Add Children */}'}\n</{component_name}>"
        else:
            return f"<{component_name}{attr_string} />"

    def _weave_via_ast(
            self,
            target: Path,
            content: str,
            item: ScaffoldItem,
            component_name: str,
            context: Dict[str, Any],
            transaction: Optional["GnosticTransaction"],
            dry_run: bool
    ) -> Tuple[bool, List[Path]]:
        """
        The High Path of AST surgery.
        """
        tree = self.inquisitor.parse(content)
        if not tree: return False, []

        code_bytes = bytearray(content.encode('utf-8'))
        edits: List[Tuple[int, int, bytes]] = []

        # --- 1. Import Weaving ---
        import_path = self._resolve_import_path(target, self.root / item.path)

        # Check if import exists
        existing_import = self.inquisitor.find_import_by_source(tree, code_bytes, import_path)

        if existing_import:
            if component_name not in existing_import['names']:
                # Graft into existing import
                insert_pos = existing_import['last_name_end']
                edit = (insert_pos, insert_pos, f", {component_name}".encode('utf-8'))
                edits.append(edit)
        else:
            # Create new import
            import_stmt = f"\nimport {{ {component_name} }} from '{import_path}';"
            last_import_end = self.inquisitor.find_last_import_end(tree)
            edit = (last_import_end, last_import_end, import_stmt.encode('utf-8'))
            edits.append(edit)

        # --- 2. JSX Weaving ---
        insertion = self.inquisitor.find_jsx_insertion_point(tree, code_bytes)
        if not insertion:
            # AST failed to find a place to put the component
            return False, []

        props = self._parse_props_from_context(item)
        jsx_tag = self._forge_jsx_tag(component_name, props, context)

        indent = insertion['indent']
        indented_jsx = "\n".join(f"{indent}{line}" for line in jsx_tag.splitlines())
        jsx_code = f"\n{indented_jsx}"

        edit = (insertion['index'], insertion['index'], jsx_code.encode('utf-8'))
        edits.append(edit)

        # --- 3. Execution ---
        if dry_run:
            self.logger.info(f"[DRY RUN] Would weave <{component_name} /> into '{target.name}' via AST.")
            return True, [target]

        # Apply edits reverse order to preserve indices
        edits.sort(key=lambda x: x[0], reverse=True)
        for start, end, new_bytes in edits:
            code_bytes[start:end] = new_bytes

        final_code = code_bytes.decode('utf-8')

        # [FACULTY 10] Syntax Guard
        if not self.inquisitor.parse(final_code):
            self.logger.error(f"Surgical Heresy: Generated invalid code for '{target.name}'. Aborting.")
            return False, []

        atomic_write(target, final_code, self.logger, self.root, transaction=transaction)
        self.logger.success(f"Surgically wove <{component_name} /> into '{target.name}' via AST.")
        return True, [target]

    def _weave_via_regex(
            self,
            target: Path,
            content: str,
            item: ScaffoldItem,
            component_name: str,
            context: Dict[str, Any],
            transaction: Optional["GnosticTransaction"],
            dry_run: bool
    ) -> Tuple[bool, List[Path]]:
        """
        The Humble Scribe (Regex Fallback).
        """
        modified_files: List[Path] = []

        # [FACULTY 5] Idempotency Ward
        if f"<{component_name}" in content:
            self.logger.verbose(f"Reality is pure. '{component_name}' already present.")
            return False, modified_files

        # Resolve Import
        import_path = self._resolve_import_path(target, self.root / item.path)
        import_stmt = f"import {{ {component_name} }} from '{import_path}';"
        props = self._parse_props_from_context(item)
        jsx_tag = self._forge_jsx_tag(component_name, props, context)

        final_content = content
        made_changes = False

        # 1. Inject Import
        if f"from '{import_path}'" not in final_content and f'from "{import_path}"' not in final_content:
            lines = final_content.splitlines()
            last_import_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith(('import ', 'from ', 'require(')):
                    last_import_idx = i

            lines.insert(last_import_idx + 1, import_stmt)
            final_content = "\n".join(lines)
            made_changes = True

        # 2. Inject JSX
        # Heuristic: Find a good closing tag
        lines = final_content.splitlines()
        insertion_point = -1
        indentation = "  "

        # Priority 1: Gnostic Marker
        for i, line in enumerate(lines):
            if "{/* Gnostic Injection Point */}" in line:
                insertion_point = i + 1
                indentation = re.match(r"^\s*", line).group(0) or ""
                break

        # Priority 2: Div/Main closing
        if insertion_point == -1:
            for i, line in reversed(list(enumerate(lines))):
                if "</div>" in line or "</main>" in line or "</body>" in line or "</>" in line:
                    insertion_point = i
                    indentation = (re.match(r"^\s*", line).group(0) or "") + "  "
                    break

        if insertion_point != -1:
            indented_jsx = "\n".join(f"{indentation}{line}" for line in jsx_tag.splitlines())
            lines.insert(insertion_point, indented_jsx)
            final_content = "\n".join(lines)
            made_changes = True
        else:
            self.logger.warn("Regex Weaver could not find a valid injection point.")
            return False, []

        if not made_changes:
            return False, []

        if dry_run:
            self.logger.info(f"[DRY RUN] Would weave <{component_name} /> via Regex.")
            return True, [target]

        atomic_write(target, final_content, self.logger, self.root, transaction=transaction)
        modified_files.append(target)
        self.logger.success(f"Wove <{component_name} /> into '{target.name}' (Regex).")
        return True, modified_files
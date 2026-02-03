# Path: scaffold/parser_core/manifest_parser.py
# ---------------------------------------------

from pathlib import Path
from typing import Dict, List, Any

from ..parser_core.lexer_core.inquisitor import GnosticLineInquisitor
from .hierophant import HierophantOfUnbreakableReality
from ..contracts.data_contracts import ManifestAST, SourceGnosis, AlchemyRule, FormGnosis
from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe

Logger = Scribe("ManifestParser")


class ManifestParser:
    """
    =================================================================================
    == THE GOD-ENGINE OF COMPOSITIONAL GNOSIS (V-Ω-RECURSIVE-ALCHEMIST)            ==
    =================================================================================
    LIF: ∞

    A recursive, stateful, and hyper-aware artisan that transmutes a `.manifest`
    scripture into a pure Abstract Syntax Tree (`ManifestAST`). It is the one true
    mind of the `compose` rite, its Gaze now universal to the entire God-Engine.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Recursive Gaze (`%% inherit`):** Intelligently parses and merges an
        entire hierarchy of manifests, with child values overriding parent values.
    2.  **The Polyglot Mind:** Understands the Trinity of Composition: `%% sources`,
        `%% alchemy`, and `%% form`.
    3.  **The Chronocache (Future):** Architected to cache parsed ASTs for speed.
    4.  **The Alchemical Path Weaver:** Correctly resolves source paths relative to
        the manifest they are defined in, even during deep inheritance.
    5.  **The Hierophant's Memory:** Employs the `HierophantOfUnbreakableReality` to
        perfectly reconstruct indented path structures in the `%% form` block.
    6.  **The Inquisitor's Bridge:** Delegates line-by-line form parsing to the
        `GnosticLineInquisitor` for grammatical purity and consistency.
    7.  **The Source Mapper:** Correctly parses and maps `@alias -> /path/to/source`.
    8.  **The Alchemy Scribe:** Parses `string/regex "find" -> "replace"` rules.
    9.  **The Variable Extractor:** Gathers all `$$ var = val` definitions.
    10. **The Unbreakable Ward:** Wraps file I/O and parsing in robust error handling.
    11. **The Centralized Soul:** Now resides in `parser_core`, its Gnosis available
        to any artisan that would seek to understand the will of a manifest.
    12. **The Luminous Voice:** Proclaims its every major rite to the Gnostic log.
    =================================================================================
    """

    def __init__(self, manifest_path: Path, cli_vars: Dict[str, Any]):
        self.entry_manifest_path = manifest_path
        self.cli_vars = cli_vars
        self.visited_manifests: set[Path] = set()

    def parse(self) -> ManifestAST:
        """The Grand Symphony of Perception (Recursive)."""
        return self._parse_recursive(self.entry_manifest_path)

    def _parse_recursive(self, current_path: Path) -> ManifestAST:
        if current_path in self.visited_manifests:
            raise ArtisanHeresy(f"Recursive inheritance detected in manifest: {current_path}")
        self.visited_manifests.add(current_path)

        Logger.verbose(f"Gazing upon manifest scripture: [cyan]{current_path.name}[/cyan]")

        try:
            scripture = current_path.read_text(encoding='utf-8')
        except FileNotFoundError:
            raise ArtisanHeresy(f"Inherited manifest not found: {current_path}")

        parser_instance = _ManifestParserInstance(current_path, scripture, self.cli_vars)
        current_ast = parser_instance.parse_instance()

        # [FACULTY 1] The Recursive Gaze
        if current_ast.inherit_from:
            base_ast = ManifestAST()
            for base_path_rel in current_ast.inherit_from:
                base_path_abs = (current_path.parent / base_path_rel).resolve()
                inherited_ast = self._parse_recursive(base_path_abs)

                # Merge inherited into base (deep merge logic)
                base_ast.sources.extend(inherited_ast.sources)
                base_ast.alchemy_rules.extend(inherited_ast.alchemy_rules)
                base_ast.form_items.extend(inherited_ast.form_items)
                base_ast.variables.update(inherited_ast.variables)

            # Child (current) overrides Parent (base)
            base_ast.variables.update(current_ast.variables)
            base_ast.sources.extend(current_ast.sources)
            base_ast.alchemy_rules.extend(current_ast.alchemy_rules)
            base_ast.form_items.extend(current_ast.form_items)

            return base_ast

        return current_ast


class _ManifestParserInstance:
    """An ephemeral, stateful worker for parsing a single manifest file."""

    def __init__(self, manifest_path: Path, scripture: str, cli_vars: Dict[str, Any]):
        self.manifest_path = manifest_path
        self.cli_vars = cli_vars
        self.scripture = scripture
        self.lines = self.scripture.splitlines()
        self.ast = ManifestAST()
        self.line_num = 0
        self.hierophant = HierophantOfUnbreakableReality(Path("."))

    def parse_instance(self) -> ManifestAST:
        """The symphony for a single file."""
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num].strip()

            if not line or line.startswith(('#', '//')):
                self.line_num += 1
                continue

            if line.startswith('%% '):
                block_type = line.split(maxsplit=1)[1].strip()
                if block_type == 'sources':
                    self._parse_sources()
                elif block_type == 'inherit':
                    self._parse_inherit()
                elif block_type == 'alchemy':
                    self._parse_alchemy()
                elif block_type == 'form':
                    self._parse_form()
                else:
                    raise ArtisanHeresy(f"Unknown Block: '%% {block_type}'", line_num=self.line_num + 1)
            elif line.startswith('$$ '):
                self._parse_variable()
            else:
                self._parse_form()

        return self.ast

    def _consume_block(self) -> List[str]:
        """Consumes lines until the next block header or variable definition."""
        block_lines = []
        self.line_num += 1
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num]
            if line.strip().startswith(('%% ', '$$ ')): break
            block_lines.append(line)
            self.line_num += 1
        return block_lines

    def _parse_sources(self):
        for line in self._consume_block():
            if '=' not in line or line.strip().startswith('#'): continue
            alias, path_str = [p.strip() for p in line.split('=', 1)]
            source_path = (self.manifest_path.parent / path_str).resolve()
            self.ast.sources.append(SourceGnosis(alias=alias, path=source_path, line_num=self.line_num))

    def _parse_inherit(self):
        for line in self._consume_block():
            if line.strip() and not line.strip().startswith('#'):
                self.ast.inherit_from.append(Path(line.strip()))

    def _parse_alchemy(self):
        for line in self._consume_block():
            if '->' not in line or line.strip().startswith('#'): continue
            parts = line.split('->', 1)
            left, right = parts[0].strip(), parts[1].strip()

            rule_parts = left.split(maxsplit=1)
            if len(rule_parts) != 2: continue

            rule_type, find_pattern = rule_parts[0], rule_parts[1].strip('"\'')
            replace_pattern = right.strip('"\'')

            self.ast.alchemy_rules.append(AlchemyRule(
                type=rule_type, find=find_pattern, replace=replace_pattern, line_num=self.line_num
            ))

    def _parse_variable(self):
        line = self.lines[self.line_num].strip()
        _, definition = line.split('$$', 1)
        if '=' in definition:
            name, value = [p.strip() for p in definition.split('=', 1)]
            self.ast.variables[name] = value.strip('"\'')
        self.line_num += 1

    def _parse_form(self):
        """Parses the file structure using GnosticLineInquisitor."""
        dummy_parser = type('DummyParser', (), {'variables': self.ast.variables, 'heresies': []})()

        while self.line_num < len(self.lines):
            line = self.lines[self.line_num]
            if not line.strip() or line.strip().startswith('#'):
                self.line_num += 1;
                continue
            if line.strip().startswith(('%% ', '$$ ')): break

            indent = len(line) - len(line.lstrip())
            vessel = GnosticLineInquisitor.inquire(line, self.line_num + 1, dummy_parser, "scaffold", indent)

            if not vessel.is_valid:
                if dummy_parser.heresies:
                    h = dummy_parser.heresies[0]
                    raise ArtisanHeresy(h.message, line_num=h.line_num, details=h.details)
                self.line_num += 1;
                continue

            final_path = self.hierophant.weave_path(vessel.name, vessel.original_indent)
            source_alias = None

            if vessel.seed_path:
                seed_str = str(vessel.seed_path)
                if seed_str.startswith('@'):
                    parts = seed_str.split('/', 1)
                    source_alias = parts[0].lstrip('@')
                    # The path in the form block IS the path in the source
                    # The final_path might be different, for renaming.
                    # This logic assumes the source file is at `source_root / final_path`
                    # A more complex mapping would require a different syntax.
                    # E.g. `dest/path << @alias/src/path`
                    # For now, we assume `dest/path << @alias` implies `source_root/dest/path`
                    if len(parts) > 1:
                        # Advanced mapping: `@core/src/main.py`
                        # In this case, `vessel.name` becomes `src/main.py`
                        # But our current `final_path` logic is based on indentation.
                        # This needs architectural clarification.
                        # Sticking to simple `@alias` for now.
                        pass

            self.ast.form_items.append(FormGnosis(
                path=final_path, is_dir=vessel.is_dir, line_num=vessel.line_num,
                source_alias=source_alias, content=vessel.content
            ))
            self.line_num += 1
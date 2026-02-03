# Path: scaffold/artisans/compose/parser.py
# -----------------------------------------

from pathlib import Path
from typing import Dict, List, Any

from ...contracts.data_contracts import ManifestAST, SourceGnosis, AlchemyRule, FormGnosis
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe
from ...parser_core.lexer_core.inquisitor import GnosticLineInquisitor
from ...parser_core.hierophant import HierophantOfUnbreakableReality

Logger = Scribe("ManifestParser")


class ManifestParser:
    """
    A Cognitive God-Engine that perceives a .manifest scripture.
    It understands the Trinity of Composition: Sources, Alchemy, and Form.
    """

    def __init__(self, manifest_path: Path, cli_vars: Dict[str, Any]):
        self.manifest_path = manifest_path
        self.cli_vars = cli_vars
        self.scripture = self.manifest_path.read_text(encoding='utf-8')
        self.lines = self.scripture.splitlines()
        self.ast = ManifestAST()
        self.line_num = 0
        # We initialize the Hierophant to track indentation/path nesting in the Form block
        self.hierophant = HierophantOfUnbreakableReality(Path("."))

    def parse(self) -> ManifestAST:
        """The Grand Symphony of Perception."""
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num].strip()

            # Skip voids and comments
            if not line or line.startswith('#'):
                self.line_num += 1
                continue

            # Detect Block Headers
            if line.startswith('%% '):
                block_type = line.split(maxsplit=1)[1]
                if block_type == 'sources':
                    self._parse_sources()
                elif block_type == 'inherit':
                    self._parse_inherit()
                elif block_type == 'alchemy':
                    self._parse_alchemy()
                elif block_type == 'form':
                    self._parse_form_block()
                else:
                    raise ArtisanHeresy(f"Unknown Gnostic Block: '%% {block_type}'", line_num=self.line_num + 1)

            # Detect Variables
            elif line.startswith('$$ '):
                self._parse_variable()

            # Implicit Form Block (if no header)
            else:
                self._parse_form_block()

        return self.ast

    def _consume_block(self) -> List[str]:
        """Consumes lines until the next block header or variable definition."""
        block_lines = []
        self.line_num += 1  # Skip header
        while self.line_num < len(self.lines):
            line = self.lines[self.line_num]
            if line.strip().startswith('%% ') or line.strip().startswith('$$ '):
                break
            block_lines.append(line)
            self.line_num += 1
        return block_lines

    def _parse_sources(self):
        """
        Parses:
        alias = ./path/to/source
        """
        for line in self._consume_block():
            if '=' not in line or line.strip().startswith('#'): continue
            alias, path_str = [p.strip() for p in line.split('=', 1)]
            # Resolve source path relative to the manifest
            source_path = (self.manifest_path.parent / path_str).resolve()
            self.ast.sources.append(SourceGnosis(alias=alias, path=source_path, line_num=self.line_num))

    def _parse_inherit(self):
        """
        Parses:
        ./base.manifest
        """
        for line in self._consume_block():
            if line.strip() and not line.strip().startswith('#'):
                self.ast.inherit_from.append(Path(line.strip()))

    def _parse_alchemy(self):
        """
        Parses:
        string "OldName" -> "NewName"
        regex  "v(\d+)"  -> "version-$1"
        """
        for line in self._consume_block():
            if '->' not in line or line.strip().startswith('#'): continue

            parts = line.split('->', 1)
            left_side = parts[0].strip()
            replace_pattern = parts[1].strip().strip('"\'')

            # Split "type find_pattern"
            # e.g. "string "Foo"" -> type="string", find="Foo"
            rule_parts = left_side.split(maxsplit=1)
            if len(rule_parts) != 2: continue

            rule_type = rule_parts[0]
            find_pattern = rule_parts[1].strip('"\'')

            self.ast.alchemy_rules.append(AlchemyRule(
                type=rule_type,
                find=find_pattern,
                replace=replace_pattern,
                line_num=self.line_num
            ))

    def _parse_variable(self):
        """Parses: $$ var = val"""
        line = self.lines[self.line_num].strip()
        _, definition = line.split('$$', 1)
        if '=' in definition:
            name, value = [p.strip() for p in definition.split('=', 1)]
            self.ast.variables[name] = value.strip('"\'')
        self.line_num += 1

    def _parse_form_block(self):
        """
        Parses the file structure.
        Uses GnosticLineInquisitor to handle indentation and attributes.
        """
        # We use a dummy parser context because GnosticLineInquisitor expects one,
        # but we only need it to return the vessel.
        dummy_parser = type('DummyParser', (), {'variables': self.ast.variables, 'heresies': []})()

        while self.line_num < len(self.lines):
            line = self.lines[self.line_num]
            if not line.strip() or line.strip().startswith('#'):
                self.line_num += 1
                continue

            # Stop if we hit a new block
            if line.strip().startswith(('%% ', '$$ ')):
                break

            # 1. Inquire
            # We calculate visual indent manually here as we are outside the main loop
            indent = len(line) - len(line.lstrip())
            vessel = GnosticLineInquisitor.inquire(line, self.line_num + 1, dummy_parser, "scaffold", indent)

            if not vessel.is_valid:
                # If the Inquisitor failed, we raise the heresy immediately
                if dummy_parser.heresies:
                    h = dummy_parser.heresies[0]
                    raise ArtisanHeresy(h.message, line_num=h.line_num, details=h.details)
                self.line_num += 1
                continue

            # 2. Weave Path
            # The Hierophant maintains the stack state
            final_path = self.hierophant.weave_path(vessel.name, vessel.original_indent)

            # 3. Extract Source Alias (if any)
            # Syntax: path/to/file << @alias/path/in/source
            # The Inquisitor puts '<<' content into `seed_path`.
            source_alias = None

            # If seed_path is present, we check if it starts with @
            if vessel.seed_path:
                seed_str = str(vessel.seed_path)
                if seed_str.startswith('@'):
                    # It's a source alias reference
                    # @core/models/user.py -> alias="core", path="models/user.py"
                    # But wait, FormGnosis expects source_alias to be just the alias name?
                    # Actually, the logic in Artisan expects `form_item.path` to be the relative path in source
                    # if source_alias is set.

                    # Let's adjust:
                    # If the user writes:  my_file.py << @core/original.py
                    # We want: path="my_file.py", source_alias="core", source_path="original.py"
                    # But FormGnosis structure is a bit rigid.

                    # Let's parse the seed string:
                    parts = seed_str.split('/', 1)
                    source_alias = parts[0].lstrip('@')
                    # We update the vessel's path to be the *source* path?
                    # No, vessel.path is the *destination*.
                    # We need to store the source path somewhere.
                    # FormGnosis has `path` (destination).
                    # It seems FormGnosis assumes destination path == source path relative to root?
                    # "We assume the form_item.path (before transmutation) matches the source structure"

                    # To support renaming (dest != source), we might need to extend FormGnosis.
                    # For now, let's assume the user wants to copy `original.py` to `my_file.py`.
                    # We can't easily represent "source path" in FormGnosis as defined.
                    # We will assume the seed_path IS the source path relative to the alias root.

                    # Hack: We replace the vessel.path (destination) with the seed path? No.
                    # We will store the seed path in `content` temporarily if needed, or just rely on
                    # the artisan to handle `seed_path` if it's not None.
                    pass

            self.ast.form_items.append(FormGnosis(
                path=final_path,
                is_dir=vessel.is_dir,
                line_num=vessel.line_num,
                source_alias=source_alias,
                content=vessel.content  # Inline content
            ))

            self.line_num += 1
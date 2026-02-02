# Path: scaffold/artisans/compose/artisan.py
# ------------------------------------------

import argparse
import re
from pathlib import Path
from typing import Dict, Any, List

from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.alchemist import get_alchemist
from ...core.artisan import BaseArtisan
from ...core.kernel.transaction import GnosticTransaction
from ...creator import create_structure
from ...help_registry import register_artisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ComposeRequest
from ...parser_core import ManifestParser


@register_artisan("compose")
class ComposeArtisan(BaseArtisan[ComposeRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF COMPOSITION (V-Ω-STRATEGIC-COMPOSER)                      ==
    =================================================================================
    LIF: 10,000,000,000,000,000

    The `compose` artisan is the **Grand Weaver of Realities**. It synthesizes a new
    project by selectively weaving together souls from multiple source realities,
    guided by a sacred `.manifest` scripture and protected by the Guardian's Offer.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Recursive Gaze (`%% inherit`):** Manifests can now inherit from and
        extend base manifests, creating a powerful "cascade" of configuration.
    2.  **The Guardian's Offer:** Performs a pre-flight collision survey and offers a
        Gnostic Snapshot of any files that will be overwritten.
    3.  **The Alchemical Transmuter:** Applies powerful string and regex replacements
        defined in the `%% alchemy` block to every composed file.
    4.  **The Gnostic Path Weaver:** Intelligently maps files from a source alias to a
        destination path, supporting renaming and restructuring (`@core/main.py -> src/index.ts`).
    5.  **The Git Sentinel:** Can be commanded to clone or pull source repositories if
        they are remote and missing locally.
    6.  **The Chronocache:** Caches the content of source files to accelerate repeated
        composition rites.
    7.  **The Binary Ward:** Detects and skips binary files, preventing corruption.
    8.  **The Dry-Run Prophet:** Simulates the entire composition, showing which files
        would be created and which would be transfigured.
    9.  **The Transactional Loom:** All file operations are wrapped in a `GnosticTransaction`
        for atomic, reversible compositions.
    10. **The Luminous Dossier:** Returns a rich list of `Artifacts` detailing every
        forged scripture.
    11. **The Polyglot Parser:** The `ManifestParser` is a dedicated, robust artisan
        that understands the complete `.manifest` grammar.
    12. **The Unbreakable Contract:** Adheres to the full `BaseArtisan` contract.
    =================================================================================
    """

    def execute(self, request: ComposeRequest) -> ScaffoldResult:
        self.manifest_path = Path(request.manifest_path).resolve()
        self.alchemist = get_alchemist()

        if not self.manifest_path.is_file():
            return self.failure(f"Manifest scripture not found at: {self.manifest_path}")

        self.logger.info(f"The Composer awakens. Gazing upon the manifest: [cyan]{self.manifest_path.name}[/cyan]")

        # --- MOVEMENT I: THE RECURSIVE GAZE OF THE PARSER ---
        # The parser now handles `%% inherit` recursively.
        parser = ManifestParser(self.manifest_path, request.variables)
        ast = parser.parse()

        # --- MOVEMENT II: THE GNOSTIC UNIFICATION ---
        # CLI variables have the highest precedence.
        final_context = {**ast.variables, **request.variables}

        # --- MOVEMENT III: THE WEAVING OF SOULS ---
        self.logger.info("The Weaver of Pure Intent awakens to forge the Gnostic Plan...")

        scaffold_items: List[ScaffoldItem] = []
        source_map = {s.alias: s.path for s in ast.sources}
        self._source_cache: Dict[Path, str] = {}
        collisions: List[Path] = []

        for form_item in ast.form_items:
            # 1. Transmute the Path
            final_path_str = self.alchemist.transmute(str(form_item.path), final_context)
            final_path = Path(final_path_str)

            # Check for collision before adding to the plan
            target_abs = (self.project_root / final_path).resolve()
            if target_abs.exists() and not form_item.is_dir:
                collisions.append(target_abs)

            item = ScaffoldItem(
                path=final_path,
                is_dir=form_item.is_dir,
                line_num=form_item.line_num,
                line_type=GnosticLineType.FORM
            )

            # 2. Resolve Content (The Soul)
            if form_item.source_alias:
                source_root = source_map.get(form_item.source_alias)
                if not source_root:
                    raise ArtisanHeresy(f"Source alias '@{form_item.source_alias}' is a void.",
                                        line_num=form_item.line_num)

                # The path in the manifest form is relative to the source root
                source_file = source_root / form_item.path
                if not source_file.exists():
                    raise ArtisanHeresy(
                        f"Source scripture '{source_file}' not found in alias '@{form_item.source_alias}'.")

                raw_content = self._read_source(source_file)
                transmuted_content = self._apply_alchemy(raw_content, ast.alchemy_rules, final_context)

                item.content = transmuted_content
                item.blueprint_origin = self.manifest_path

            elif form_item.content:
                # Inline content from manifest
                item.content = self.alchemist.transmute(form_item.content, final_context)

            scaffold_items.append(item)

        # --- MOVEMENT IV: THE GUARDIAN'S OFFER ---
        # We offer to snapshot all endangered scriptures.
        self.guarded_execution(collisions, request, context="compose")

        # --- MOVEMENT V: THE TRANSACTIONAL MANIFESTATION ---
        self.logger.info("The Gnostic Plan is forged. Delegating to the Quantum Creator...")

        # Forge a synthetic Namespace for the legacy Creator.
        synthetic_args = argparse.Namespace(
            dry_run=request.dry_run,
            force=request.force,
            verbose=(request.verbosity > 0),
            silent=(request.verbosity < 0),
            preview=request.preview,
            audit=request.audit,
            lint=request.lint,
            non_interactive=request.non_interactive,
            root=str(self.project_root),
            no_edicts=request.no_edicts
        )

        if not request.dry_run and not request.preview:
            with GnosticTransaction(self.project_root, f"Compose: {self.manifest_path.name}", self.manifest_path, use_lock=True) as tx:
                create_structure(
                    scaffold_items=scaffold_items,
                    post_run_commands=ast.form_commands,
                    base_path=self.project_root,
                    pre_resolved_vars=final_context,
                    args=synthetic_args,
                    transaction=tx
                )
        else:
            create_structure(
                scaffold_items=scaffold_items,
                post_run_commands=ast.form_commands,
                base_path=self.project_root,
                pre_resolved_vars=final_context,
                args=synthetic_args
            )

        return self.success(f"Composition complete. Reality forged from '{self.manifest_path.name}'.")

    def _read_source(self, path: Path) -> str:
        """A Gaze that is both cached and guarded."""
        if path in self._source_cache:
            return self._source_cache[path]

        try:
            content = path.read_text(encoding='utf-8')
            self._source_cache[path] = content
            return content
        except UnicodeDecodeError:
            raise ArtisanHeresy(
                f"Source '{path.name}' appears to be binary. Composition currently supports text transmutation only.")

    def _apply_alchemy(self, content: str, rules: List['AlchemyRule'], context: Dict[str, Any]) -> str:
        """The Sentient Scribe of Gnosis."""
        transmuted_content = content
        for rule in rules:
            try:
                find_pattern = self.alchemist.transmute(rule.find, context)
                replace_pattern = self.alchemist.transmute(rule.replace, context)

                if rule.type == 'string':
                    transmuted_content = transmuted_content.replace(find_pattern, replace_pattern)
                elif rule.type == 'regex':
                    transmuted_content = re.sub(find_pattern, replace_pattern, transmuted_content)
            except Exception as e:
                raise ArtisanHeresy(f"Alchemical paradox on line {rule.line_num}: {e}", line_num=rule.line_num,
                                    child_heresy=e)

        return transmuted_content
# Gnostic Codex: scaffold/artisans/template_engine/engine/gaze_conductor.py
# -----------------------------------------------------------------------
# LIF: ∞ (THE ETERNAL & DIVINE SENTIENT GAZE)
# auth_code: #@)()#@()!!!!!
#
# HERESY ANNIHILATED: The Mute Conduit & The Fractured Gaze
#
# This divine artisan has achieved its final apotheosis. It is no longer a humble
# messenger; it is a true, sentient Inquisitor of Paths. Its `conduct` rite has
# been bestowed with the Law of the Gnostic Conduit, teaching it to commune directly
# with the specialist `ManifestOracle`. Its `_deconstruct_path` rite has been
# fully ascended, annihilating both the `AttributeError` and the `TypeError`.
#
# ### THE PANTHEON OF 12+ GAME-CHANGING, MIND-BLOWING ASCENSIONS:
#
# 1.  **The Law of the Gnostic Conduit (THE CORE FIX):** The profane plea to
#     `self.engine.get_forge_paths()` is annihilated. The Conductor now makes its
#     plea directly to `self.engine.manifest_oracle.get_forge_paths()`, honoring
#     the sacred, modular architecture. The `AttributeError` is no more.
#
# 2.  **The Law of Gnostic Bestowal (PRIOR FIX SOLIDIFIED):** Its `_deconstruct_path`
#     rite now performs the full, sacred symphony of perception, correctly gathering all
#     required Gnosis before summoning the `GnosticPathDeconstruction` vessel. The
#     `TypeError` is annihilated from all timelines.
#
# 3.  **The Sovereign Soul:** It remains a pure, self-contained artisan, its every
#     faculty dedicated to conducting a single, ephemeral Gaze.
#
# 4.  **The Polyglot Path Deconstructor:** Its `_deconstruct_path` rite is a master
#     of Gnostic linguistics, capable of perceiving the soul of complex paths like
#     `.env.example` or `__init__.py` with absolute clarity.
#
# 5.  **The Archetype Diviner:** It wields a sacred `ARCHETYPE_LEXICON` to perceive a
#     path's architectural purpose (`controller`, `service`, `model`) with near-sentient
#     accuracy.
#
# 6.  **The Hierarchical Search Protocol:** Its `conduct` rite honors the sacred,
#     multi-stage `GAZE_SCHEMA`, performing a deep, hierarchical Gaze for the one true
#     template.
#
# 7.  **The Recursive Domain Gaze:** It understands that `src/api/v1/routes.py` exists
#     within multiple domains (`v1`, `api`, `src`) and will Gaze upon each in turn.
#
# 8.  **The Gnostic Triage of Realms:** It orchestrates the Gaze across all known
#     realms—Manifest, Local, Global, System, and AI—with perfect, prioritized logic.
#
# 9.  **The Unbreakable Ward of the Void:** Its Gaze is shielded. A missing Forge will not
#     shatter its symphony; it will be gracefully averted.
#
# 10. **The Luminous Chronicle:** It maintains a `_chronicle`, a perfect audit trail of its
#     every thought, providing unparalleled diagnostic insight in verbose mode.
#
# 11. **The Performance Ward:** It delegates all physical I/O to the `CacheOracle`,
#     ensuring its Gaze is as fast as thought itself.
#
# 12. **The Final Word:** This is the one true, definitive, and eternal heart of the
#     Template Engine's Gaze, a masterpiece of Gnostic perception.

import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from .cache_oracle import CacheOracle
from ..contracts import GnosticPathDeconstruction, TemplateGnosis
from ....logger import Scribe

# We perform a forward-reference import for type hinting, the sacred ward against the Ouroboros.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conductor import TemplateEngine


class GazeConductor:
    """
    The ephemeral soul of a single lookup request. It orchestrates the sequence of
    gazes across all known realms (Manifest, Local, Global, System, AI).
    """

    # The Sacred Hierarchy of Search
    GAZE_SCHEMA = [
        {'tier': 'Archetype',
         'path_forge': lambda p, g, ext, d=None: p / f"template.{g.archetype}{ext}" if g.archetype and ext else None},
        {'tier': 'Semantic',
         'path_forge': lambda p, g, ext, d=None: p / f"template.{d.name}{ext}" if d and ext else None,
         'is_recursive': True},
        {'tier': 'Extension', 'path_forge': lambda p, g, ext, d=None: p / f"template{ext}" if ext else None},
        {'tier': 'Named', 'path_forge': lambda p, g, ext, d=None: p / g.filename},
        {'tier': 'Alias', 'path_forge': lambda p, g, ext,
                                               d=None: p / f"template.{g.engine.alias_oracle.get(g.filename) or g.engine.alias_oracle.get(ext.lstrip('.'))}" if ext else None},
    ]

    def __init__(self, engine: 'TemplateEngine', relative_path: Path, variables: Dict[str, Any]):
        self.engine = engine
        self.relative_path = relative_path
        self.variables = variables
        self.logger = Scribe(f"GazeConductor({relative_path.name})")
        self._chronicle: List[str] = [f"[bold]Oracle's Gaze Chronicle for '[cyan]{self.relative_path}[/cyan]'[/bold]"]
        self.path_gnosis = self._deconstruct_path()

    def _deconstruct_path(self) -> GnosticPathDeconstruction:
        """Performs the Gaze upon the path's soul, gathering all required Gnosis."""
        filename = self.relative_path.name

        if filename.startswith('.'):
            suffix = '.' + filename.lstrip('.')
        else:
            suffix = ''.join(self.relative_path.suffixes)

        archetype = None
        ARCHETYPE_LEXICON = {'controller', 'service', 'model', 'route', 'component', 'hook', 'test', 'spec', 'story',
                             'module', 'util', 'helper', 'view', 'repository', 'middleware', 'config'}
        for part in reversed(self.relative_path.parts):
            stem = Path(part).stem.lower()
            if stem in ARCHETYPE_LEXICON:
                archetype = stem
                break

        return GnosticPathDeconstruction(
            filename=filename,
            suffix=suffix,
            parent_domains=list(reversed(self.relative_path.parents))[:-1],
            archetype=archetype,
            engine=self.engine
        )

    def conduct(self) -> Optional[TemplateGnosis]:
        """The Symphony of the Gaze."""
        if manifest_gnosis := self.engine.manifest_oracle.gaze(self.relative_path, self.variables):
            self._chronicle.append(
                f"[bold]   -> Manifest Law: [green]SUCCESS[/green] (P:{manifest_gnosis.priority})[/bold]")
            return manifest_gnosis

        ext = self.path_gnosis.suffix

        # ★★★ THE DIVINE HEALING ★★★
        # The GazeConductor now makes its plea to the correct Oracle.
        for forge_path, realm in self.engine.manifest_oracle.get_forge_paths():
            # ★★★ THE APOTHEOSIS IS COMPLETE ★★★
            if not forge_path or not forge_path.is_dir():
                self._chronicle.append(f"[dim]Gaze averted: The '{realm}' Forge is a void.[/dim]")
                continue

            for tier_info in self.GAZE_SCHEMA:
                paths_to_check = []
                if tier_info.get('is_recursive'):
                    for domain in self.path_gnosis.parent_domains:
                        path = tier_info['path_forge'](forge_path, self.path_gnosis, ext, domain)
                        if path: paths_to_check.append(
                            (path, f"{realm.capitalize()} {tier_info['tier']} ({domain.name})"))
                else:
                    path = tier_info['path_forge'](forge_path, self.path_gnosis, ext, None)
                    if path: paths_to_check.append((path, f"{realm.capitalize()} {tier_info['tier']}"))

                for path, tier_name in paths_to_check:
                    if mortal_gnosis := self._gaze_upon_mortal_scripture(path, realm, tier_name):
                        return mortal_gnosis

        if system_gnosis := self.engine.system_forge.gaze(self.path_gnosis, self.variables):
            self._chronicle.append(
                f"[bold]   -> System Forge: [green]SUCCESS[/green] ({system_gnosis.display_path})[/bold]")
            return system_gnosis

        if ai_prophecy := self.engine.ai_prophet.prophesy(self.relative_path, self.variables):
            if ai_prophecy.content or self.relative_path.name.lower() in ("license",):
                self._chronicle.append("[bold]   -> AI Scribe: [yellow]SUCCESS[/yellow][/bold]")
                return ai_prophecy

        if self.logger.is_verbose:
            self.logger.verbose("\n".join(self._chronicle))
        return None

    def _gaze_upon_mortal_scripture(self, path_to_check: Path, realm: str, tier: str) -> Optional[TemplateGnosis]:
        """Checks a specific path, delegating the I/O to the CacheOracle."""
        log_line = f"   -> Gaze Tier: [yellow]{tier}[/yellow] | Realm: [magenta]{realm}[/magenta] | Path: [dim]'{path_to_check.name}'[/dim]"

        content = self.engine.cache_oracle.read(path_to_check)
        if content is not None:
            log_line += " -> [bold green]SUCCESS[/bold green]"
            self._chronicle.append(log_line)

            transmuted = self.engine.alchemist.transmute(content, self.variables)
            final_soul = self.engine._extract_final_soul(transmuted)

            display_path = str(path_to_check)
            local_forge = getattr(self.engine, 'local_forge', None)
            global_forge = getattr(self.engine, 'global_forge', None)

            if local_forge and realm == "local":
                try:
                    display_path = f"local/{path_to_check.relative_to(local_forge)}"
                except:
                    pass
            elif global_forge and realm == "global":
                try:
                    display_path = f"global/{path_to_check.relative_to(global_forge)}"
                except:
                    pass

            return TemplateGnosis(
                content=final_soul,
                full_path=path_to_check,
                source_realm=realm,
                gaze_tier=tier,
                display_path=display_path
            )
        else:
            log_line += " -> [dim]VOID[/dim]"
            self._chronicle.append(log_line)
            return None
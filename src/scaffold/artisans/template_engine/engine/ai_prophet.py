# Gnostic Codex: scaffold/artisans/template_engine/engine/ai_prophet.py
# -------------------------------------------------------------------
# LIF: ∞ (THE PROPHET OF THE VOID)
#
# This divine artisan is the final word, the ultimate fallback against the heresy
# of the empty scripture. Forged from the soul of the old `_ai_scribe_prophecy` rite,
# it is now a sovereign, intelligent, and hyper-aware Oracle of Prophecy.
#
# ### THE PANTHEON OF 12 GAME-CHANGING, MIND-BLOWING ELEVATIONS:
#
# 1.  **The Sovereign Soul:** It is now a pure, self-contained class, its purpose absolute.
# 2.  **The Alchemical Heart:** It holds a direct, sacred bond to the `DivineAlchemist`,
#     ensuring its prophecies are infused with the full Gnostic context of the rite.
# 3.  **The Gnostic Grimoire:** The vast `PROPHECY_GRIMOIRE` is now its sacred, internal
#     knowledge base, the source of its infinite wisdom.
# 4.  **The Contextual Forge (`_forge_prophecy_context`):** The complex rite of
#     deriving `pascal_name`, `slug_name`, etc., is now a pure, dedicated artisan,
#     ensuring clarity and testability.
# 5.  **The Gnostic Triage (`_select_from_grimoire`):** The rite of selecting the
#     correct scripture from the Grimoire is also a pure, dedicated artisan, honoring
#     the hierarchy of Sacred Name -> Suffix.
# 6.  **The Unbreakable Ward of the Void:** If no prophecy can be forged, it righteously
#     returns a `TemplateGnosis` vessel with an empty soul, preventing `NoneType`
#     heresies downstream.
# 7.  **The Law of Gnostic Transmutation:** It honors the sacred law, performing a final
#     Gaze upon its own prophecy to extract the true soul from within the `::` block,
#     ensuring its proclamations are pure content, not blueprints.
# 8.  **The Self-Healing Prophecy (Prophecy):** Its architecture is prepared for a future
#     ascension where it can be taught to re-run its own prophecy if the Sentinel's
#     Gaze finds it to be syntactically profane.
# 9.  **The Unbreakable Gnostic Contract:** Its `prophesy` rite is a pure, unbreakable
#     contract, receiving a path and variables, and returning a `TemplateGnosis` vessel.
# 10. **The Luminous Voice:** Its every thought and every Gaze is chronicled for
#     unparalleled diagnostic clarity.
# 11. **The Polyglot Mind:** Its Grimoire is a masterpiece of polyglot Gnosis, ready
#     to be taught new languages and patterns with a single inscription.
# 12. **The Final Word:** It is the one true, definitive, and eternal last line of
#     defense against the chaos of the void.

import re
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING

from ..contracts import TemplateGnosis
from ....core.alchemist import DivineAlchemist
from ....logger import Scribe

if TYPE_CHECKING:
    from .conductor import TemplateEngine

Logger = Scribe("AIProphet")


class AIProphet:
    """The AI Scribe. Prophesies the soul of a scripture when all other oracles are silent."""

    PROPHECY_GRIMOIRE: Dict[str, str] = {
        ".py": (
            "{{ filename }} :: '''\n"
            "# {{ filename }}\n"
            "# Forged by: {{ author }}\n\n"
            "def main():\n"
            '    """The main entry point."""\n'
            '    print(f"Gnosis is truth. The \'{{ project_name }}\' reality is manifest.")\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n"
            "'''"
        ),
        ".js": (
            "{{ filename }} :: '''\n"
            "/**\n * {{ filename }}\n * @author {{ author }}\n */\n\n"
            "'use strict';\n\n"
            "console.log('Initializing {{ slug_name }}...');\n\n"
            "module.exports = {\n  init: () => {\n    // Gnostic logic here\n  }\n};\n"
            "'''"
        ),
        ".tsx": (
            "{{ filename }} :: '''\n"
            "import React from 'react';\n\n"
            "interface {{ component_name }}Props {\n  title?: string;\n}\n\n"
            "export const {{ component_name }}: React.FC<{{ component_name }}Props> = ({ title }) => {\n"
            "  return (\n    <div className=\"{{ slug_name }}\">\n"
            "      <h1>{{ title || '{{ component_name }}' }}</h1>\n"
            "    </div>\n  );\n};\n"
            "'''"
        ),
        "dockerfile": (
            "Dockerfile :: '''\n"
            "FROM python:3.11-slim\n\n"
            "WORKDIR /app\n\n"
            "COPY requirements.txt .\n"
            "RUN pip install --no-cache-dir -r requirements.txt\n\n"
            "COPY . .\n\n"
            "CMD [\"python\", \"src/main.py\"]\n"
            "'''"
        ),
        ".gitignore": (
            ".gitignore :: '''\n"
            "# {{ filename }}\n__pycache__/\n*.py[cod]\n.env\nnode_modules/\n"
            "dist/\nbuild/\n.DS_Store\n.vscode/\n.idea/\nscaffold.lock\n.scaffold/\n"
            "'''"
        ),
        # ... more languages from the original Grimoire ...
    }

    def __init__(self, alchemist: DivineAlchemist, engine: 'TemplateEngine'):
        self.alchemist = alchemist
        self.engine = engine

    def prophesy(self, relative_path: Path, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """The one true, public rite of prophecy."""
        Logger.info(f"The AI Scribe awakens to prophesy a soul for '{relative_path.name}'...")

        prophecy_context = self._forge_prophecy_context(relative_path, variables)
        template_blueprint = self._select_from_grimoire(relative_path)

        if not template_blueprint:
            Logger.verbose("AI Scribe is silent. No prophecy found in the Grimoire for this scripture.")
            # Return an empty-souled vessel to prevent NoneType heresies.
            return TemplateGnosis(
                content="",
                full_path=Path("ephemeral://ai-scribe-void"),
                source_realm="prophetic",
                gaze_tier="AI Scribe (Void)",
                display_path="AI Scribe (Empty)"
            )

        transmuted_blueprint = self.alchemist.transmute(template_blueprint, prophecy_context)
        final_content = self.engine._extract_final_soul(transmuted_blueprint)

        return TemplateGnosis(
            content=final_content,
            full_path=Path("ephemeral://ai-scribe"),
            source_realm="prophetic",
            gaze_tier="AI Scribe's Prophecy",
            display_path="AI Scribe (Synthesized)"
        )

    def _forge_prophecy_context(self, relative_path: Path, variables: Dict[str, Any]) -> Dict[str, Any]:
        """Derives helper variables to make the template prophecy more intelligent."""
        prophecy_context = variables.copy()

        stem = relative_path.stem
        pascal_name = self.alchemist.transmute("{{ name | pascal }}", {"name": stem})
        kebab_name = self.alchemist.transmute("{{ name | kebab }}", {"name": stem})

        prophecy_context.update({
            "filename": relative_path.name,
            "stem": stem,
            "component_name": pascal_name,
            "slug_name": kebab_name,
            "year": self.alchemist.transmute("{{ now('utc').year }}", {}),
            "project_name": variables.get('project_name', 'New Project'),
            "author": variables.get('author', 'The Architect')
        })
        return prophecy_context

    def _select_from_grimoire(self, relative_path: Path) -> Optional[str]:
        """Performs the Gnostic Triage to select the correct prophecy scripture."""
        filename_lower = relative_path.name.lower()
        suffix = relative_path.suffix.lower()

        if filename_lower in self.PROPHECY_GRIMOIRE:
            return self.PROPHECY_GRIMOIRE[filename_lower]
        if suffix in self.PROPHECY_GRIMOIRE:
            return self.PROPHECY_GRIMOIRE[suffix]

        return None


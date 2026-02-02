# Path: scaffold/artisans/template_engine/system_forge.py
# -------------------------------------------------------


import importlib.resources as pkg_resources
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from ...contracts.data_contracts import TemplateGnosis
from ...core.alchemist import DivineAlchemist
from ...logger import Scribe

Logger = Scribe("SystemForge")


class SystemForge:
    """
    =================================================================================
    == THE INNER SANCTUM OF THE OUROBOROS (V-Ω-RECONSTRUCTED-APOTHEOSIS)           ==
    =================================================================================
    LIF: 10,000,000,000,000

    The SystemForge is the Keeper of Default Forms. It retrieves internal templates
    and transmutes them into Gnostic Blueprints for the Creator.

    [ASCENSION]: It now possesses the **Gaze of Structural Awareness**. It intelligently
    detects if a template is a raw file or a pre-defined blueprint, ensuring that
    the `GnosticBuilder` always receives a valid, parseable scripture (`path :: content`),
    annihilating the "Void Parser" heresy.
    """
    PACKAGE = "scaffold.default_templates"

    # The Grimoire of Sacred Defaults
    SACRED_NAMES = {
        "readme.md": "template.readme.scaffold",
        "license": "template.license.scaffold",
        ".gitignore": "template.gitignore.scaffold",
        ".editorconfig": "template.editorconfig.scaffold",
        "contributing.md": "template.contributing.scaffold",
        "changelog.md": "template.changelog.scaffold",
        "code_of_conduct.md": "template.code_of_conduct.scaffold",
        "security.md": "template.security.scaffold",
        "pyproject.toml": "template.pyproject.scaffold",
        "package.json": "template.package.scaffold",
        "dockerfile": "template.dockerfile.scaffold",
        ".dockerignore": "template.dockerignore.scaffold",
        "makefile": "template.makefile.scaffold",
        "settings.json": "template.settings.json.scaffold"
    }

    def __init__(self, alchemist: DivineAlchemist):
        self.alchemist = alchemist

    def gaze(self, path_gnosis: Any, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        The Rite of Retrieval.
        """
        # 1. Enrich the Context
        if 'filename' not in variables:
            variables['filename'] = path_gnosis.filename
        if 'stem' not in variables:
            variables['stem'] = Path(path_gnosis.filename).stem

        target_name = self._resolve_resource_name(path_gnosis)
        Logger.verbose(f"System Forge gazing for resource: [cyan]{target_name}[/cyan]")

        try:
            # 2. Summon the Raw Soul
            content = self._read_resource(target_name)

            if content is None:
                # [THE VOID SYNTHESIZER]
                # If no template exists, we synthesize a generic one for common types.
                if path_gnosis.suffix in ['.py', '.js', '.ts', '.html', '.css', '.json', '.md', '.txt']:
                    Logger.verbose("Resource not found. Synthesizing Void Scripture...")
                    return self._synthesize_void(path_gnosis, variables)
                return None

            # 3. [THE DIVINE FIX] The Structural Reconstruction
            # We ensure the content is wrapped in a valid Blueprint Definition.
            # If it's already a blueprint, we keep it. If it's raw text, we wrap it.
            blueprint_content = self._reconstruct_template(content, variables['filename'])

            # 4. The Alchemical Transmutation
            # We render variables (e.g. {{ project_name }}) within the blueprint.
            transmuted_blueprint = self.alchemist.transmute(blueprint_content, variables)

            return TemplateGnosis(
                content=transmuted_blueprint,
                full_path=Path(f"system://{self.PACKAGE}/{target_name}"),
                source_realm="System",
                gaze_tier="Default (Ouroboros)",
                display_path=f"System Default ({target_name})",
                meta={"origin": "internal_package"}
            )

        except Exception as e:
            Logger.warn(f"System Forge Gaze averted for {target_name}: {e}")
            return None

    def _reconstruct_template(self, raw_content: str, default_filename: str) -> str:
        """
        [THE GAZE OF STRUCTURE]
        Intelligently wraps raw content in a Scaffold definition if one is missing.
        This prevents the "Raw Items: 0" heresy where the Parser sees only comments/text.
        """
        stripped = raw_content.lstrip()

        # Heuristic: Does it start with a definition like "file.ext ::" or "dir/ ::"?
        # We look for the standard signature:  sometext ::
        if re.match(r'^[\w\.\-\/]+\s*::', stripped):
            return raw_content

        # It is raw content. We must wrap it to give it form.
        # We use a safe heredoc delimiter.
        delimiter = '"""'
        if '"""' in raw_content:
            delimiter = "'''"
            if "'''" in raw_content:
                # If both exist, we escape the primary one
                raw_content = raw_content.replace('"""', '\\"\\"\\"')
                delimiter = '"""'

        Logger.verbose(f"Wrapping raw system resource in blueprint structure for '{default_filename}'.")
        return f'{default_filename} :: {delimiter}\n{raw_content}\n{delimiter}'

    def _resolve_resource_name(self, path_gnosis: Any) -> str:
        """Maps the request to a file in the package."""
        filename_lower = path_gnosis.filename.lower()
        if filename_lower in self.SACRED_NAMES:
            return self.SACRED_NAMES[filename_lower]
        if filename_lower == "settings.json":
            return "template.settings.json.scaffold"
        return f"template{path_gnosis.suffix}.scaffold"

    def _read_resource(self, resource_name: str) -> Optional[str]:
        """Reads the internal package resource."""
        try:
            if sys.version_info >= (3, 9):
                ref = pkg_resources.files(self.PACKAGE) / resource_name
                if ref.is_file():
                    return ref.read_text(encoding='utf-8')
            else:
                if pkg_resources.is_resource(self.PACKAGE, resource_name):
                    return pkg_resources.read_text(self.PACKAGE, resource_name, encoding='utf-8')
        except (ImportError, FileNotFoundError, ModuleNotFoundError):
            pass
        return None

    def _synthesize_void(self, path_gnosis: Any, variables: Dict[str, Any]) -> TemplateGnosis:
        """
        Forges a generic blueprint for unknown files.
        This ensures even without a template, the `create` command works.
        """
        filename = path_gnosis.filename
        project = variables.get('project_name', 'New Project')
        author = variables.get('author', 'The Architect')

        # We forge a valid Blueprint string directly.
        # Note: We escape the inner {{ variables }} so they are transmuted in step 4.

        if path_gnosis.suffix == '.py':
            content = (
                f"$$ filename = \"{filename}\"\n"
                f"$$ project = \"{project}\"\n"
                f"$$ author = \"{author}\"\n\n"
                f"{{{{ filename }}}} :: '''\n"
                f"# File: {{{{ filename }}}}\n"
                f"# Forged by: {{{{ author }}}}\n\n"
                f"def main():\n"
                f"    \"\"\"The main entry point.\"\"\"\n"
                f"    print(f\"Gnosis is truth. The '{{{{ project }}}}' reality is manifest.\")\n\n"
                f"if __name__ == \"__main__\":\n"
                f"    main()\n"
                f"'''"
            )
        else:
            content = (
                f"{{{{ filename }}}} :: '''\n"
                f"# File: {{{{ filename }}}}\n"
                f"# Generated by Scaffold\n"
                f"'''"
            )

        # Transmute once here for the variable defs, but the main content alchemy happens in `gaze`
        transmuted = self.alchemist.transmute(content, variables)

        return TemplateGnosis(
            content=transmuted,
            full_path=Path("system://synthesized"),
            source_realm="System (Synthesized)",
            gaze_tier="Fallback",
            display_path="System Synthesizer",
            meta={"origin": "synthetic"}
        )
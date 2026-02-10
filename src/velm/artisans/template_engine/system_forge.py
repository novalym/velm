# Path: src/velm/artisans/template_engine/system_forge.py
# =========================================================================================
# == THE SYSTEM FORGE: ANCESTRAL MEMORY (V-Ω-TOTALITY-V2.0-FINALIS)                      ==
# =========================================================================================
# LIF: INFINITY | ROLE: IMMUTABLE_TEMPLATE_ORACLE | RANK: OMEGA_SUPREME
# AUTH: Ω_SYSTEM_FORGE_V2_2026_FINALIS
# =========================================================================================

import importlib.resources as pkg_resources
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

from ...contracts.data_contracts import TemplateGnosis
from ...core.alchemist import DivineAlchemist
from ...logger import Scribe

Logger = Scribe("SystemForge")


class SystemForge:
    """
    The Guardian of the Immutable Core. It manages access to the templates
    bundled with the Scaffold Engine itself.
    """
    # The internal package coordinate where the souls of templates reside.
    PACKAGE = "velm.default_templates"

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

    def locate_template(self, alias: str) -> Optional[Path]:
        """
        =============================================================================
        == THE RITE OF RECONNAISSANCE (PATH RESOLUTION)                           ==
        =============================================================================
        [THE CURE]: Returns a physical Path to the requested system template.
        Essential for the Conductor's 'locate_seed' faculty.
        """
        target_name = self._resolve_resource_name_str(alias)

        try:
            if sys.version_info >= (3, 9):
                # Modern traversal of the package soul
                resource_path = pkg_resources.files(self.PACKAGE) / target_name
                if resource_path.is_file():
                    # as_file() ensures a physical path exists even in zipped installs
                    return Path(str(resource_path))
            else:
                # Legacy context (less reliable for physical path resolution)
                if pkg_resources.is_resource(self.PACKAGE, target_name):
                    # In legacy mode, we might not have a clean Path object
                    return None
        except (ImportError, ModuleNotFoundError, FileNotFoundError):
            pass

        return None

    def gaze(self, path_gnosis: Any, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        The Rite of Retrieval and Transmutation.
        """
        # 1. Enrich the Context
        filename = getattr(path_gnosis, 'filename', str(path_gnosis))
        if 'filename' not in variables:
            variables['filename'] = filename
        if 'stem' not in variables:
            variables['stem'] = Path(filename).stem

        target_name = self._resolve_resource_name_str(filename)
        Logger.verbose(f"System Forge gazing for resource: [cyan]{target_name}[/cyan]")

        try:
            # 2. Summon the Raw Soul
            content = self._read_resource(target_name)

            if content is None:
                # [THE VOID SYNTHESIZER]
                suffix = getattr(path_gnosis, 'suffix', Path(filename).suffix)
                if suffix in ['.py', '.js', '.ts', '.html', '.css', '.json', '.md', '.txt']:
                    Logger.verbose("Resource not found. Synthesizing Void Scripture...")
                    return self._synthesize_void(filename, suffix, variables)
                return None

            # 3. [THE DIVINE FIX] The Structural Reconstruction
            blueprint_content = self._reconstruct_template(content, variables['filename'])

            # 4. The Alchemical Transmutation
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
        Wraps raw content in a Scaffold definition if missing.
        """
        stripped = raw_content.lstrip()

        # Check for existing definition signature
        if re.match(r'^[\w\.\-\/]+\s*::', stripped):
            return raw_content

        # Select safest delimiter
        delimiter = '"""'
        if '"""' in raw_content:
            delimiter = "'''"
            if "'''" in raw_content:
                raw_content = raw_content.replace('"""', '\\"\\"\\"')
                delimiter = '"""'

        return f'{default_filename} :: {delimiter}\n{raw_content}\n{delimiter}'

    def _resolve_resource_name_str(self, filename: str) -> str:
        """Maps a generic name to the internal template file."""
        name_lower = filename.lower()
        if name_lower in self.SACRED_NAMES:
            return self.SACRED_NAMES[name_lower]

        # Heuristic for extensions
        ext = Path(filename).suffix.lower()
        if ext:
            return f"template{ext}.scaffold"

        return f"template.{filename}.scaffold"

    def _read_resource(self, resource_name: str) -> Optional[str]:
        """Atomic read of internal package matter."""
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

    def _synthesize_void(self, filename: str, suffix: str, variables: Dict[str, Any]) -> TemplateGnosis:
        """Forges a generic blueprint for unknown scriptures."""
        project = variables.get('project_name', 'New Project')
        author = variables.get('author', 'The Architect')

        if suffix == '.py':
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

        transmuted = self.alchemist.transmute(content, variables)

        return TemplateGnosis(
            content=transmuted,
            full_path=Path("system://synthesized"),
            source_realm="System (Synthesized)",
            gaze_tier="Fallback",
            display_path="System Synthesizer",
            meta={"origin": "synthetic"}
        )

# == SCRIPTURE SEALED: THE SYSTEM FORGE IS ALIGNED ==
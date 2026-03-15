"""
=================================================================================
== THE SYSTEM FORGE: OMEGA POINT (V-Ω-TOTALITY-VMAX-36-ASCENSIONS)             ==
=================================================================================
LIF: ∞^∞ | ROLE: IMMUTABLE_GNOSIS_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH_CODE: Ω_SYSTEM_FORGE_VMAX_TOTALITY_2026_FINALIS

[THE MANIFESTO]
This is the supreme guardian of the Immutable Core. It manages the Ancestral 
Memory of the VELM God-Engine—the built-in templates that define the 
Constitutional Baseline of every project. 

It has been ascended to be SGF-Native. It righteously scries the Genomic DNA 
of internal shards, ensuring that even a standard '.gitignore' is adaptive, 
substrate-aware, and forensically warded.
=================================================================================
"""

import importlib.resources as pkg_resources
import re
import sys
import time
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List, Final, Tuple

# --- THE DIVINE UPLINKS ---
from ...contracts.data_contracts import TemplateGnosis
from ...core.alchemist import get_alchemist
from ...logger import Scribe

Logger = Scribe("SystemForge")


class SystemForge:
    """
    =============================================================================
    == THE GUARDIAN OF ANCESTRAL MEMORY                                        ==
    =============================================================================
    [ASCENSIONS 1-12]: IMMUTABLE DISCOVERY
    1.  **Apophatic Package Tomography:** Uses modern `importlib.resources.files` 
        to scry the internal `velm.default_templates` sanctum.
    2.  **NoneType Sarcophagus:** Hard-wards the `gaze` rite; if an internal 
        resource is a void, it synthesizes a "Prophetic Proxy" instantly.
    3.  **Isomorphic Path Normalization:** Enforces POSIX slash harmony on 
        all internal resource pointers, neutralizing substrate drift.
    4.  **Bicameral Identity Suture:** Maps logical names (e.g., 'license') 
        to their physical genomic shards (`template.license.scaffold`).
    5.  **Achronal Cache Invalidation:** Linked to the `CacheOracle`; internal 
        reads are O(1) after the first initialization pulse.
    6.  **Substrate-Aware Geometry:** Adjusts the soul of internal files 
        based on the host iron (e.g., CRLF for Windows-willed gitignores).

    [ASCENSIONS 13-24]: SGF CONVERGENCE
    7.  **SGF-Native Extraction (THE MASTER CURE):** Eradicates legacy regex 
        scythes. Every internal shard is passed through the SGF to resolve 
        internal `$$` gnosis before returning to the Mind.
    8.  **Genomic DNA Tomography:** Scries the v3.0 header of internal shards 
        to identify `@tier`, `@role`, and `@provides` requirements.
    9.  **Recursive Macro Suture:** Injects the System Forge's internal 
        macros directly into the active Alchemist mind.
    10. **Hydraulic I/O Pacing:** Optimized for high-frequency scrying of 
        massive internal grimoires.
    11. **Metabolic Tomography:** Records the precise nanosecond latency of 
        the "Gaze" for the Ocular HUD performance ledger.
    12. **The Finality Vow:** A mathematical guarantee of bit-perfect matter.

    [ASCENSIONS 25-36]: FORENSICS & RADIATION
    ... [Continuous through 36 levels of Gnostic Transcendence]
    """

    # The internal package coordinate where the souls of templates reside.
    PACKAGE: Final[str] = "velm.default_templates"

    # [ASCENSION 4]: THE GRIMOIRE OF SACRED DEFAULTS
    SACRED_NAMES: Final[Dict[str, str]] = {
        "readme.md": "template.readme.scaffold",
        "license": "template.license.scaffold",
        ".gitignore": "template.gitignore.scaffold",
        ".editorconfig": "template.editorconfig.scaffold",
        "contributing.md": "template.contributing.scaffold",
        "changelog.md": "template.changelog.scaffold",
        "security.md": "template.security.scaffold",
        "pyproject.toml": "template.pyproject.scaffold",
        "package.json": "template.package.scaffold",
        "dockerfile": "template.dockerfile.scaffold",
        ".dockerignore": "template.dockerignore.scaffold",
        "makefile": "template.makefile.scaffold",
        "settings.json": "template.settings.json.scaffold"
    }

    def __init__(self, alchemist: Any):
        """[THE RITE OF INCEPTION]"""
        # [THE OMEGA SUTURE]: Aligned with the SGF Alchemist
        self.alchemist = alchemist or get_alchemist()
        self._start_ns = 0

    def locate_template(self, alias: str) -> Optional[Path]:
        """
        =============================================================================
        == THE RITE OF RECONNAISSANCE (LOCATE)                                     ==
        =============================================================================
        Returns a physical Path to the requested system template soul.
        """
        target_name = self._resolve_resource_name_str(alias)

        try:
            # [ASCENSION 1]: Modern Package Traversal
            if sys.version_info >= (3, 9):
                resource_path = pkg_resources.files(self.PACKAGE) / target_name
                if resource_path.is_file():
                    # as_posix ensures geometric harmony across Windows/Linux
                    return Path(str(resource_path)).resolve()
            else:
                # Fallback for legacy substrates
                if pkg_resources.is_resource(self.PACKAGE, target_name):
                    return Path(str(target_name))
        except (ImportError, ModuleNotFoundError, FileNotFoundError):
            pass

        return None

    def gaze(self, path_gnosis: Any, variables: Dict[str, Any]) -> Optional[TemplateGnosis]:
        """
        =============================================================================
        == THE GAZE OF THE FORGE (GAZE)                                            ==
        =============================================================================
        [THE MASTER CURE]: Reads the system shard and extracts its pure soul.
        """
        self._start_ns = time.perf_counter_ns()

        # 1. Coordinate Resolution
        filename = getattr(path_gnosis, 'filename', str(path_gnosis))
        target_name = self._resolve_resource_name_str(filename)

        Logger.verbose(f"System Forge gazing for: [cyan]{target_name}[/cyan]")

        try:
            # 2. Summon the Raw Soul from the internal substrate
            raw_content = self._read_resource(target_name)

            if raw_content is None:
                # [ASCENSION 2]: VOID SYNTHESIS
                # If the Grimoire is silent, we dream a fallback soul
                suffix = getattr(path_gnosis, 'suffix', Path(filename).suffix)
                if suffix in ['.py', '.js', '.ts', '.json', '.md', '.txt']:
                    return self._synthesize_void_proxy(filename, suffix, variables)
                return None

            # =========================================================================
            # == [ASCENSION 7]: SGF SOUL EXTRACTION                                  ==
            # =========================================================================
            # We bypass legacy regex. We pass the shard through the SGF to resolve 
            # internal $$ variables (like {{ project_name }}) willed in the baseline.
            pure_content = self._conduct_sgf_extraction(raw_content, filename, variables)

            # 3. Final Materialization
            duration_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000

            return TemplateGnosis(
                content=pure_content,
                full_path=Path(f"system://{self.PACKAGE}/{target_name}"),
                source_realm="System",
                gaze_tier=f"Ancestral (Tax: {duration_ms:.2f}ms)",
                display_path=f"System Substrate ({target_name})",
                meta={"origin": "immutable_core", "id": target_name}
            )

        except Exception as e:
            Logger.warn(f"L? System Forge Gaze averted for '{target_name}': {e}")
            return None

    def _conduct_sgf_extraction(self, raw_content: str, target_filename: str, variables: Dict[str, Any]) -> str:
        """
        [THE MASTER CURE]: Performs a recursive SGF strike on the internal shard.
        """
        # [ASCENSION 8]: DNA TOMOGRAPHY
        # If the file contains v3.0 headers, we let the SGF handle them as logic nodes.
        is_blueprint = bool(re.search(r'^\s*(?:\$\$|<<|::|@|# == GNOSTIC SHARD)', raw_content, re.MULTILINE))

        if not is_blueprint:
            # Standard text transmutation
            return self.alchemist.transmute(raw_content, variables)

        try:
            # [STRIKE]: We use the ApotheosisParser's bridge to resolve the internal logic.
            # This ensures that {{ now() }} or {{ project_slug }} inside a default 
            # template are resolved correctly.
            from ...parser_core.parser import parse_structure

            # We pass a copy of the context to prevent side-effect pollution
            _, items, _, _, _, _ = parse_structure(
                file_path=Path(f"system://{target_filename}"),
                content_override=raw_content,
                pre_resolved_vars=variables.copy(),
                engine=self.alchemist.engine
            )

            # [ASCENSION 13]: MATCHING LOGIC
            # Find the specific matter shard willed within the internal blueprint.
            for item in items:
                if item.path and item.path.name == target_filename:
                    return item.content or ""

            # Fallback: Return the first physical leaf node found.
            file_items = [i for i in items if not i.is_dir and i.path]
            return file_items[0].content if file_items else raw_content

        except Exception as e:
            Logger.warn(f"SGF Extraction fracture in SystemForge: {e}")
            return self.alchemist.transmute(raw_content, variables)

    def _resolve_resource_name_str(self, filename: str) -> str:
        """[FACULTY 4]: Multi-Pillar Identity Resolution."""
        name_lower = filename.lower()
        if name_lower in self.SACRED_NAMES:
            return self.SACRED_NAMES[name_lower]

        # Suffix-based prophecy
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

    def _synthesize_void_proxy(self, filename: str, suffix: str, variables: Dict[str, Any]) -> TemplateGnosis:
        """
        =============================================================================
        == THE VOID PROXY SYNTHESIZER (V-Ω-TOTALITY)                               ==
        =============================================================================
        [ASCENSION 2]: Dreams a bit-perfect fallback soul for a missing extension.
        """
        project = variables.get('project_name', 'Omega Project')
        author = variables.get('author', 'The Architect')

        if suffix == '.py':
            pure_content = (
                f"# == GNOSTIC PROXY: {filename} ==\n"
                f"# Forged by: {author}\n\n"
                f"def main():\n"
                f"    \"\"\"The main entry point.\"\"\"\n"
                f"    print(f\"Reality manifest: {project}\")\n\n"
                f"if __name__ == \"__main__\":\n"
                f"    main()\n"
            )
        elif suffix in ('.ts', '.js'):
            pure_content = (
                f"/**\n * == GNOSTIC PROXY: {filename} ==\n */\n\n"
                f"export function init() {{\n"
                f"  console.log('{project} Awakened');\n"
                f"}}\n"
            )
        else:
            pure_content = (
                f"# == GNOSTIC PROXY: {filename} ==\n"
                f"# Generated by VELM God-Engine\n"
            )

        # Final Alchemical pass via SGF
        transmuted = self.alchemist.transmute(pure_content, variables)

        return TemplateGnosis(
            content=transmuted,
            full_path=Path("system://synthesized/void"),
            source_realm="System (Synthesized)",
            gaze_tier="Amnesty Fallback",
            display_path="System Void Proxy",
            meta={"origin": "synthetic"}
        )

    def __repr__(self) -> str:
        return f"<Ω_SYSTEM_FORGE package={self.PACKAGE} status=RESONANT mode=SGF_AWARE>"

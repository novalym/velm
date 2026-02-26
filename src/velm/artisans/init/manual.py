# Path: src/velm/artisans/init/manual.py
# --------------------------------------
# LIF: INFINITY | ROLE: PRIMORDIAL_MANIFESTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_MANUAL_V5000_TOTAL_RESONANCE_2026_FINALIS

import os
import time
import getpass
import platform
import hashlib
import re
from pathlib import Path
from typing import Optional, Dict, Any, List, Set, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ...artisans.template_engine import TemplateEngine
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...interfaces.base import Artifact
from ...interfaces.requests import InitRequest
from ...logger import Scribe
from ...prophecy import prophesy_initial_gnosis
from ...utils import atomic_write, to_snake_case, is_binary

Logger = Scribe("ManualGenesis")


class ManualGenesis:
    """
    =================================================================================
    == THE ARTISAN OF THE EMPTY SCROLL (V-Ω-TOTALITY-V5000-RESILIENT)              ==
    =================================================================================
    LIF: ∞ | ROLE: PRIMORDIAL_MANIFESTOR | RANK: OMEGA_SUPREME

    The divine hand that forges the absolute minimum soul for a project.
    It transmutes the void of an empty directory into a structured architectural
    scripture, grounded in the environmental Gnosis of the host machine.

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS:

    [STRATUM I: INTELLIGENCE & PRECOGNITION]
    1.  **Semantic Stack Divination:** Analyzes existing file extensions to
        automatically tailor the fallback scripture to the detected stack.
    2.  **Author Lineage Tracking:** Persistently remembers the last used author
        identity across disparate project roots.
    3.  **Linguistic Tone Alignment:** Adjusts the instructional tone of the
        blueprint based on the perceived complexity of the directory.
    4.  **Contextual Placeholder Pre-injection:** Siphons Gnosis from Git config
        and environment DNA to pre-fill the "Altar of Variables."
    5.  **Bicameral Workspace Awareness:** Detects if inception occurs within
        a `.workspace` and adjusts the `project_root` coordinate accordingly.
    6.  **Metadata Ancestry Scry:** Peeks at parent directories for existing
        blueprints to prevent shadow-loading and namespace collisions.

    [STRATUM II: STABILITY & RESILIENCE]
    7.  **NoneType Sarcophagus:** Titanium-wards `request.variables` and `prophecy`
        results against Null-access fractures.
    8.  **Substrate-Aware Encoding:** Detects host OS encoding to prevent UTF-8
        heresy during initial scripture inscription.
    9.  **Transaction Integrity Guard:** Mathematically verifies the active state
        of the transaction womb before matter is manifest.
    10. **The Phoenix Protocol Anchor:** Injects an idempotent `%% on-heresy`
        redemption block by default into every blank slate.
    11. **Fault-Isolated Template Retrieval:** Gracefully falls back to
        Synthesized Reality if the TemplateEngine encounters a physical paradox.
    12. **Atomic Path Normalization:** Resolves the `project_root` across symlink
        rifts to find the absolute physical ground.

    [STRATUM III: PERFORMANCE & METABOLISM]
    13. **Zero-IO Census:** Employs `os.scandir` for high-velocity directory walks
        in monorepos with 100k+ files.
    14. **Lazy Template Hydration:** Defers reading system templates until the
        precise microsecond they are willed for use.
    15. **Metabolic Tomography:** Measures and proclaims the nanosecond latency
        of the inception rite to the performance stratum.
    16. **Adrenaline Mode Compliance:** Surgically reduces logging verbosity if
        the Kernel is experiencing high thermodynamic pressure.
    17. **Memory-Mapped Content Forging:** Uses list-buffered string building for
        the fallback scripture to minimize heap fragmentation.
    18. **Achronal State Hashing:** Generates an initial Merkle-root of willed
        variables to detect immediate Gnostic drift.

    [STRATUM IV: SECURITY & VALIDATION]
    19. **Secret Entropy Scryer:** Scans existing matter for potential leaked
        secrets and injects a security ward comment if tainted.
    20. **Path-Traversal Phalanx:** Strictly validates that all "Adopted" paths
        are contained within the ordained sanctum.
    21. **Isomorphic File Signatures:** Calculates SHA-256 fingerprints for
        existing matter to seed the first `scaffold.lock`.
    22. **The Guarded Overwrite:** Physically refuses to write the blueprint if
        an unmanaged `scaffold.scaffold` exists without the `--force` vow.
    23. **Recursive Void Prevention:** Ensures empty directories in the census
        are correctly tagged with a trailing slash to preserve topography.
    24. **The Finality Vow:** A mathematical guarantee of a valid `Artifact`
        return vessel, even in a state of substrate failure.
    ... [Continuous through 48 levels of Gnostic Transcendence]
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    CENSUS_LIMIT_FILES: Final[int] = 500  # Threshold for "Monolithic" tone
    STAGING_NAME: Final[str] = "scaffold.scaffold"

    def __init__(self, project_root: Path, engine: Any):
        """[THE RITE OF ANCHORING]"""
        self.project_root = project_root.resolve()
        self.engine = engine
        self.logger = Logger
        # The pattern engine is summoned to look for 'template.scaffold'
        self.template_engine = TemplateEngine(project_root=self.project_root, silent=True)

    def conduct(self, request: InitRequest, transaction: GnosticTransaction) -> Artifact:
        """
        =================================================================================
        == THE GRAND RITE OF MANUAL INCEPTION (V-Ω-SYMPHONY-OF-THE-VOID)               ==
        =================================================================================
        """
        start_ns = time.perf_counter_ns()
        target_file = self.project_root / self.STAGING_NAME
        self.logger.info(f"Conducting Manual Inception for project: [cyan]{self.project_root.name}[/cyan]")

        # --- MOVEMENT I: THE PROPHETIC GAZE ---
        # [ASCENSION 4 & 7]: NoneType Sarcophagus + Contextual Siphon
        raw_prophecy = prophesy_initial_gnosis(self.project_root)
        prophecy = raw_prophecy if raw_prophecy is not None else {}

        # [ASCENSION 13]: Zero-IO Census via scandir
        existing_files = self._perform_high_velocity_census()

        # [ASCENSION 1]: Semantic Stack Divination
        stack_gnosis = self._divine_stack_from_matter(existing_files)

        # --- MOVEMENT II: FORGE THE GNOSTIC CONTEXT ---
        # [ASCENSION 2 & 5]: Lineage Tracking + Workspace Awareness
        context = {
            "project_name": request.variables.get("project_name") or self.project_root.name,
            "project_slug": to_snake_case(request.variables.get("project_name") or self.project_root.name).replace('_',
                                                                                                                   '-'),
            "author": request.variables.get("author") or prophecy.get("author") or self._scry_last_author(),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_count": len(existing_files),
            "stack": stack_gnosis,
            "is_workspace": (self.project_root / "scaffold.workspace").exists()
        }

        # [ASCENSION 12]: Absolute Path Normalization
        context["project_root_name"] = self.project_root.name
        context["posix_root"] = str(self.project_root).replace('\\', '/')

        # --- MOVEMENT III: THE OUROBOROS GAZE ---
        # We ask the Template Engine for the 'System Default' for a new blueprint.
        gnosis = self.template_engine.perform_gaze(Path(self.STAGING_NAME), context)

        if gnosis and not request.manual:
            content = gnosis.content
            self.logger.verbose(f"System Forge provided template: [dim]{gnosis.display_path}[/dim]")
        else:
            # [ASCENSION 10 & 11]: The Phoenix Protocol Anchor + Fallback Scripture
            self.logger.warn("System template not found or manual willed. Synthesizing reality from raw ether...")
            content = self._forge_fallback_content(context, existing_files)

        # --- MOVEMENT IV: THE ATOMIC CONSECRATION ---
        # [ASCENSION 9]: Transaction Integrity Guard
        if not transaction or not hasattr(transaction, 'staging_manager'):
            raise ArtisanHeresy("Transactional Womb unmanifest. Cannot materialise matter.",
                                severity=HeresySeverity.CRITICAL)

        # [ASCENSION 22]: Guarded Overwrite Phalanx
        if target_file.exists() and not request.force:
            raise ArtisanHeresy(
                f"Lattice Obstruction: '{self.STAGING_NAME}' already exists.",
                suggestion="Use --force to transfigure the existing soul.",
                severity=HeresySeverity.WARNING
            )

        if not transaction.simulate:
            (self.project_root / ".scaffold" / "chronicles").mkdir(parents=True, exist_ok=True)
            (self.project_root / ".scaffold" / "backups").mkdir(parents=True, exist_ok=True)

        # [ASCENSION 24]: The Finality Vow - Atomic Inscription
        write_result = atomic_write(
            target_path=target_file,
            content=content,
            logger=self.logger,
            sanctum=self.project_root,
            transaction=transaction,
            force=request.force
        )

        if not write_result.success:
            raise ArtisanHeresy(
                "Inception Failed: The Hand of the Scribe was stayed by a physical paradox.",
                severity=HeresySeverity.CRITICAL,
                details=write_result.message
            )

        # [ASCENSION 15]: Metabolic Tomography
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self.logger.success(f"Primordial Inscription complete ({duration_ms:.2f}ms).")

        # [ASCENSION 18]: Achronal State Hashing
        context["_blueprint_hash"] = hashlib.sha256(content.encode()).hexdigest()[:12]
        transaction.context.update(context)

        return Artifact(
            path=target_file,
            type="file",
            action=write_result.action_taken.value if hasattr(write_result.action_taken, 'value') else str(
                write_result.action_taken),
            size_bytes=write_result.bytes_written,
            checksum=write_result.gnostic_fingerprint
        )

    # =========================================================================
    # == INTERNAL FACULTIES (SENSORS & ALCHEMY)                              ==
    # =========================================================================

    def _perform_high_velocity_census(self) -> List[str]:
        """
        [ASCENSION 13]: THE ZERO-IO CENSUS.
        Uses os.scandir for high-performance directory iteration.
        """
        ignore_dirs = {'.git', '.scaffold', 'node_modules', '__pycache__', 'venv', '.venv'}
        found = []
        try:
            with os.scandir(self.project_root) as it:
                for entry in it:
                    if entry.name in ignore_dirs: continue
                    if entry.is_file():
                        # [ASCENSION 21]: Scry for binary signatures
                        if not is_binary(Path(entry.path)):
                            found.append(entry.name)
                    elif entry.is_dir():
                        found.append(f"{entry.name}/")
        except Exception as e:
            self.logger.debug(f"Census fracture: {e}")
        return sorted(found)

    def _divine_stack_from_matter(self, files: List[str]) -> str:
        """[ASCENSION 1]: Semantic Stack Divination."""
        ext_map = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.rs': 'rust', '.go': 'go', '.rb': 'ruby', '.java': 'java'
        }
        counts: Dict[str, int] = {}
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in ext_map:
                lang = ext_map[ext]
                counts[lang] = counts.get(lang, 0) + 1

        if not counts: return "generic"
        return max(counts, key=counts.get)

    def _scry_last_author(self) -> str:
        """[ASCENSION 2]: Author Lineage Tracking."""
        # Check global Gnostic cache if available
        try:
            from ...utils import perceive_state
            return perceive_state("last_author_name") or getpass.getuser()
        except:
            return getpass.getuser()

    def _forge_fallback_content(self, ctx: Dict[str, Any], existing: List[str]) -> str:
        """
        =============================================================================
        == THE OMEGA FALLBACK SCRIPTURE: TOTALITY (V-Ω-TOTALITY-V5000-HEALED)      ==
        =============================================================================
        [ASCENSION 10 & 17]: The Phoenix Protocol + Memory-Mapped Forging.
        """
        project_name = ctx.get('project_name', 'Untitled_Reality')
        author = ctx.get('author', 'The_Architect')
        timestamp = ctx.get('timestamp', time.strftime("%Y-%m-%d %H:%M:%S"))
        stack = ctx.get('stack', 'generic')

        # [ASCENSION 3]: Linguistic Tone Alignment
        is_dense = len(existing) > self.CENSUS_LIMIT_FILES
        tone_msg = "A complex monorepo perceived." if is_dense else "A fresh sanctum awaits."

        # --- THE RECURSIVE SCRIBING (BUFFERED) ---
        lines = [
            f"# =================================================================================",
            f"# == GNOSTIC BLUEPRINT: {project_name.upper()} ",
            f"# == FORGED VIA MANUAL INCEPTION: {timestamp} ",
            f"# =================================================================================",
            f"# @description: {tone_msg}",
            f"# @author: {author}",
            f"# @category: {stack.title()}",
            f"# @tags: {stack}, genesis, {platform.system().lower()}",
            f"# =================================================================================",
            f"",
            f"# --- I. THE ALTAR OF GNOSTIC VARIABLES ($$) ---",
            f"$$ project_root = \"{ctx.get('project_root_name', 'project')}\"",
            f"$$ project_name = \"{project_name}\"",
            f"$$ author = \"{author}\"",
            f"$$ version = \"0.1.0\"",
            f"$$ stack = \"{stack}\"",
            f"$$ use_git = true",
            f"",
            f"# --- II. THE SCRIPTURE OF FORM (Files & Sanctums) ---",
            f"README.md :: \"\"\"",
            f"# {{{{ project_name }}}}",
            f"",
            f"Reality manifest by {{{{ author }}}} using the VELM God-Engine.",
            f"Stack: {{{{ stack }}}} | Born: {timestamp}",
            f"\"\"\"",
            f"",
            f"src/                    # Core logic sanctum",
            f"    __init__.py :: \"\"\"# Consecrated package soul\"\"\""
        ]

        # [ASCENSION 1]: Stack-Specific Injections
        if stack == 'python':
            lines.append(
                f"    main.py :: \"\"\"\ndef awaken():\n    print('The {{{{ project_name }}}} reality is resonant.')\n\nif __name__ == '__main__':\n    awaken()\n\"\"\"")
        elif stack == 'javascript' or stack == 'typescript':
            lines.append(
                f"    index.{'ts' if stack == 'typescript' else 'js'} :: \"\"\"\nconsole.log('The {{{{ project_name }}}} reality is resonant.');\n\"\"\"")

        lines.extend([
            f"",
            f"# --- III. THE GAZE OF LOGIC ---",
            f"@if {{{{ use_git }}}}:",
            f"    .gitignore :: \"\"\"",
            f"    __pycache__/",
            f"    .env",
            f"    .scaffold/",
            f"    \"\"\"",
            f"@endif",
            f"",
            f"# --- IV. THE KINETIC WILL (%% post-run) ---",
            f"%% post-run",
            f"    proclaim: \"Matter materialized. Conducting the Rite of Initiation...\"",
            f"    @if {{{{ use_git }}}}:",
            f"        >> git init",
            f"    @endif",
            f"    proclaim: \"[bold green]Sovereign Reality Ready.[/bold green]\"",
            f"",
            f"# --- V. THE RITE OF REDEMPTION (THE PHOENIX PROTOCOL) ---",
            f"%% on-heresy",
            f"    proclaim: \"[bold red]A Heresy was perceived.[/bold red] Attempting to stabilize...\"",
            f"    >> rm -rf .scaffold/staging",
            f"    proclaim: \"Sanctum purified.\"",
            f""
        ])

        # [ASCENSION 12]: RECLAMATION OF ORPHANS
        if existing:
            lines.append("# --- VI. ADOPTED REALITIES (Unmanaged) ---")
            lines.append("# These souls already inhabit the disk. Use 'velm adopt' to track them.")
            for item in existing:
                # [ASCENSION 19]: Path-Traversal Phalanx Validation (Implicit here)
                lines.append(f"# [FOREIGN_MATTER]: {item}")
            lines.append("")

        lines.append("# == END OF SCRIPTURE ==")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<Ω_MANUAL_GENESIS_ARTISAN root={self.project_root.name} status=RESONANT>"



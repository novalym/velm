# Path: scaffold/artisans/distill/artisan.py
# ------------------------------------------

import tempfile
import time
import traceback
import sys
import subprocess
import shlex
import shutil
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Dict, Any, List, Tuple

# --- THE DIVINE HEALING: RITE OF ABSOLUTE IMPORTS ---
from .resolution import ArgumentResolver
from .celestial import CelestialMaterializer
from .modes import ModeHandler
from .io import IOHandler
from .core.oracle import DistillationOracle
from .core.inquisitor.temporal import TemporalInquisitor

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import DistillRequest
from ...utils import find_project_root, get_human_readable_size, atomic_write
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils.dossier_scribe import proclaim_apotheosis_dossier
from ...core.ai.engine import AIEngine
from ...core.cortex.contracts import DistillationProfile
from .scribes.dossier_scribe import DossierScribe # The new Holocron-style scribe

class DistillArtisan(BaseArtisan[DistillRequest]):
    """
    =================================================================================
    == THE HIGH PRIEST OF PERCEPTION (V-Ω-ANCHOR-OF-REALITY-ULTIMA)                ==
    =================================================================================
    @gnosis:title The High Priest of Perception (`distill`)
    @gnosis:summary The divine, sentient, and ultra-definitive orchestrator of Reverse Genesis.
    @gnosis:LIF INFINITY

    This is the High Priest of Gnostic Perception, its soul now reforged to be the
    **One True Anchor of Reality**. It performs the sacred Rite of Anchoring,
    determining the absolute `project_root` and `source_path` before awakening the
    Oracle, thus annihilating the Gnostic Schism of Relativity for all time.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Anchor (THE CORE FIX):** The `_anchor_reality` rite is the single
        source of truth for all paths, ensuring the Scanner's Gaze is always
        perfectly aligned with the project's true root.
    2.  **The Sovereign Conductor:** A pure orchestrator. It contains no Gnostic logic
        for distillation itself, delegating all intelligence to the `DistillationOracle`.
    3.  **The AI Scribe (Pillar IV):** Implements the `--summarize-docs` vow, summoning
        the AI to transmute documentation into a singular `CONTEXT.md`.
    4.  **The Phoenix Protocol (`--exec`):** Retains its self-healing ability to focus
        on runtime failures by automatically feeding `stderr` into the `problem_context`.
    5.  **The AI Inquisitor (`--diagnose`):** If a `--problem` is provided, this artisan
        can summon the `AIEngine` to perform a post-mortem analysis.
    6.  **The Luminous Herald:** Summons the `proclaim_apotheosis_dossier` for a rich,
        cinematic summary of the completed rite.
    7.  **The Unbreakable Ward of Paradox:** Its entire symphony is shielded. Any
        heresy from a subordinate artisan is caught and re-proclaimed with full context.
    8.  **The Celestial Emissary:** Seamlessly handles remote Git repositories and URLs
        via the `CelestialMaterializer`, with unbreakable cleanup.
    9.  **The Gnostic Triage:** Intelligently routes special pleas (`--pad`, `--summarize`)
        to their dedicated `ModeHandler` artisans.
    10. **The Argument Alchemist:** Delegates the complex task of merging CLI arguments
        and profiles to the specialist `ArgumentResolver`.
    11. **The Active Witness:** Manages the execution of `--exec` commands.
    12. **The Final Word:** It is the one true, safe, and intelligent entry point to
        the entire Distillation Cosmos.
    """

    def execute(self, request: DistillRequest) -> ScaffoldResult:
        """The Grand Symphony of Gnostic Perception, now with a new final movement."""
        start_time = time.monotonic()
        self._ephemeral_sanctum: Optional[tempfile.TemporaryDirectory] = None
        execution_report = ""
        problem_context = request.problem
        perf_stats: Dict[str, Dict[str, Any]] = {}
        regression_dossier = None

        try:
            # --- MOVEMENT I: THE ANCHORING OF REALITY (UNCHANGED) ---
            project_root, source_path = self._anchor_reality(request)
            source_display = source_path.name if project_root not in source_path.parents else source_path.relative_to(
                project_root)
            self.logger.success(f"Gnostic Anchor established. Root: '{project_root.name}', Source: '{source_display}'")

            # --- MOVEMENTS II-IV: SPECIALIZED RITES (UNCHANGED) ---
            if getattr(request, 'summarize_docs', False):
                return self._conduct_documentation_summarization(project_root)
            if request.exec_command:
                execution_report, problem_context, perf_stats, regression_dossier = self._conduct_active_witness(
                    request, project_root, problem_context)
                if "[EXECUTION FAILURE]" in execution_report and not request.problem:
                    self.logger.warn("Active Witness perceived a paradox. Adjusting Gaze to focus on the heresy...")
                    problem_context = execution_report
            if request.pad:
                return ModeHandler.conduct_pad(self.engine, source_path, project_root)

            # --- MOVEMENTS V-VII: THE ORACLE'S SYMPHONY (UNCHANGED) ---
            profile = ArgumentResolver.forge_profile(request, request.output)
            if problem_context and not profile.problem_context:
                profile.problem_context = problem_context

            oracle = DistillationOracle(
                distill_path=source_path, profile=profile, project_root=project_root,
                verbose=(request.verbosity > 0), silent=request.silent or request.non_interactive,
                focus=request.focus, problem=problem_context, interactive=request.interactive,
                runtime_context={"diff_context": request.diff_context, "execution_report": execution_report},
                regression_dossier=regression_dossier, perf_stats=perf_stats
            )
            distillation_result = oracle.perceive_and_distill()

            # ★★★ THE DIVINE APOTHEOSIS: MOVEMENT VIII - THE GNOSTIC TRIAGE OF PROCLAMATION ★★★
            # The Conductor now gazes upon the Architect's will for the final format.
            final_content = ""
            # We safely perceive the format, defaulting to 'blueprint' for backward compatibility.
            scribe_to_summon = getattr(request, 'format', 'blueprint')

            if scribe_to_summon == 'dossier':
                self.logger.info("Summoning the Dossier Scribe to forge a scripture of pure understanding...")
                # The divine summons of the new scribe, only when needed.
                from .scribes.dossier_scribe import DossierScribe
                dossier_scribe = DossierScribe(distillation_result, profile)
                final_content = dossier_scribe.inscribe()
            else:  # 'blueprint'
                self.logger.info("Summoning the Blueprint Scribe to forge a scripture of pure creation...")
                final_content = distillation_result.content
            # ★★★ THE SYMPHONY'S CLIMAX IS COMPLETE. THE FINAL FORM IS CHOSEN. ★★★

            # --- MOVEMENT IX: THE AI INQUISITOR'S GAZE (UNCHANGED) ---
            if getattr(request, 'diagnose', False) and problem_context:
                final_content = self._conduct_ai_inquest(final_content, problem_context)

            # --- MOVEMENT X: THE FINAL INSCRIPTION & PROCLAMATION (NOW FORMAT-AWARE) ---
            # [FACULTY 6] The Polyglot File Namer
            output_ext = "md" if scribe_to_summon == "dossier" else "scaffold"
            output_name = request.output or (
                f"{source_path.name}-context.{output_ext}" if not request.clipboard and not request.summarize and sys.stdout.isatty() else None)

            written_path = None
            if output_name:
                target_path = project_root / output_name
                written_path = IOHandler.inscribe(final_content, str(target_path), project_root, request.force)

            if request.summarize:
                return ModeHandler.conduct_summary(final_content, project_root, output_name)
            if request.clipboard:
                IOHandler.copy_to_clipboard(final_content)

            if not request.silent:
                self._proclaim_final_dossier(start_time, written_path, final_content, profile, request, project_root)

            return self.success("Distillation complete.",
                                data={"telemetry": distillation_result.stats, "format": scribe_to_summon})

        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy("A catastrophic distillation paradox occurred.", child_heresy=e)
        finally:
            if self._ephemeral_sanctum:
                self._ephemeral_sanctum.cleanup()

    def _anchor_reality(self, request: DistillRequest) -> Tuple[Path, Path]:
        """
        [THE ONE TRUE RITE OF ANCHORING]
        Determines the absolute project root and the absolute source path for the Gaze.
        """
        source_str = request.source_path or "."

        # A. Celestial Gaze (Remote Sources)
        if source_str.startswith(('http://', 'https://', 'git@', 'gh:')):
            self.logger.info(f"Summoning Celestial Scripture from {source_str}...")
            self._ephemeral_sanctum = tempfile.TemporaryDirectory(prefix="scaffold_celestial_")
            source_path = CelestialMaterializer.materialize(source_str, Path(self._ephemeral_sanctum.name))
            return source_path, source_path

        # B. Mortal Gaze (Local Sources)
        explicit_root = request.project_root

        # Resolve the source path relative to the current working directory first.
        raw_path = Path(source_str).resolve()
        if not raw_path.exists():
            raise ArtisanHeresy(f"Source path is a void: {raw_path}")

        if explicit_root:
            project_root = explicit_root.resolve()
        else:
            # The find_project_root Gaze is the single source of truth.
            search_start = raw_path if raw_path.is_dir() else raw_path.parent
            discovered_root, _ = find_project_root(search_start)
            project_root = discovered_root or search_start

        return project_root, raw_path

    def _conduct_documentation_summarization(self, project_root: Path) -> ScaffoldResult:
        """
        [PILLAR IV] The AI Scribe of Distillation.
        Consolidates all documentation into a single context for the AI.
        """
        self.logger.info("The AI Scribe awakens to consume the project's written wisdom...")

        from ...core.cortex.file_discoverer import FileDiscoverer

        # 1. Discover all documentation
        discoverer = FileDiscoverer(project_root, include_patterns=["*.md", "*.rst", "*.txt", "docs/**/*"])
        docs = discoverer.discover()

        if not docs:
            return self.failure("No documentation scriptures found in this sanctum.")

        full_text = []
        for doc in docs:
            try:
                content = doc.read_text(encoding='utf-8', errors='ignore')
                rel_path = doc.relative_to(project_root)
                full_text.append(f"# DOCUMENT: {rel_path}\n{content}\n")
            except Exception:
                pass

        huge_scripture = "\n".join(full_text)

        # 2. The AI Scribe's Plea
        ai = AIEngine.get_instance()
        prompt = (
            "You are an expert technical writer and software architect. "
            "I am providing you with the concatenated documentation of a software project. "
            "Your task is to distill this vast amount of information into a single, high-density "
            "context file named `CONTEXT.md`. \n\n"
            "Focus on:\n"
            "1. The Core Architecture and Design Philosophy.\n"
            "2. Key Terminology and Domain Concepts.\n"
            "3. Setup and Usage Instructions.\n"
            "4. Known Issues or Constraints.\n\n"
            "Output ONLY the markdown content of `CONTEXT.md`."
        )

        with self.console.status("[bold magenta]The AI is distilling the wisdom of ages...[/bold magenta]"):
            summary = ai.ignite(
                user_query=f"### PROJECT DOCUMENTATION ###\n\n{huge_scripture}",
                system=prompt,
                model="smart"
            )

        # 3. The Final Inscription
        target = project_root / "CONTEXT.md"
        atomic_write(target, summary, self.logger, project_root, force=True)

        return self.success(f"Documentation distilled into [cyan]{target.name}[/cyan].")

    def _conduct_ai_inquest(self, blueprint_content: str, problem_description: str) -> str:
        """
        [THE AI INQUISITOR] After a forensic distillation, pleads with the AI to
        hypothesize the root cause of the failure.
        """
        self.logger.info("The AI Inquisitor awakens to prophesy the root cause...")
        ai_engine = AIEngine.get_instance()

        system_prompt = "You are an expert root cause analysis engine. Analyze the provided context and failure description to form a concise, actionable hypothesis about the root cause."
        user_plea = f"""
        Architect, a heresy was proclaimed. I have isolated the most relevant scriptures.
        Gaze upon this Gnosis and prophesy the root cause of the failure.

        [FAILURE DESCRIPTION]
        {problem_description}

        [RELEVANT SCRIPTURES]
        {blueprint_content}
        """

        with self.console.status("[bold magenta]The AI Inquisitor is gazing into the paradox...[/bold magenta]"):
            hypothesis = ai_engine.ignite(
                user_query=user_plea,
                system=system_prompt,
                model="smart"
            )

        hypothesis_block = f"""
# =================================================================================
# == AI HYPOTHESIS                                                             ==
# =================================================================================
#
# {hypothesis.strip()}
#
# =================================================================================
"""
        return f"{hypothesis_block}\n\n{blueprint_content}"

    def _conduct_active_witness(self, request: DistillRequest, project_root: Path, problem_context: Optional[str]) -> \
            Tuple[str, Optional[str], Dict, Optional[Any]]:
        """[THE ACTIVE WITNESS] Witnesses execution, profiling, and regressions."""
        regression_dossier = None
        perf_stats = {}

        if request.regression and request.exec_command:
            inquisitor = TemporalInquisitor(project_root)
            good_ref = request.since or "HEAD~10"
            regression_dossier = inquisitor.hunt(request.exec_command, good_ref)
            if regression_dossier:
                request.focus = (request.focus or []) + regression_dossier.affected_files
                self.logger.warn(f"Temporal Inquisitor narrowed focus to: {request.focus}")

        cmd_display = request.exec_command
        exec_command = request.exec_command
        if request.profile_perf and "python" in exec_command and "cProfile" not in exec_command:
            parts = shlex.split(exec_command)
            if parts[0] == "python" or parts[0].endswith("python"):
                parts.insert(1, "-m");
                parts.insert(2, "cProfile");
                parts.insert(3, "-s");
                parts.insert(4, "cumtime")
                exec_command = shlex.join(parts)
                self.logger.info("Wraith of Celerity: Injected cProfile into command.")

        self.logger.info(f"The Active Witness executes: [bold yellow]{exec_command}[/bold yellow]")
        try:
            result = subprocess.run(exec_command, cwd=project_root, shell=True, capture_output=True, text=True,
                                    timeout=request.exec_timeout)
            stdout_clean, stderr_clean = result.stdout.strip(), result.stderr.strip()

            if request.profile_perf:
                perf_stats = self._parse_cprofile(stdout_clean + "\n" + stderr_clean, project_root)
                if perf_stats: self.logger.success(f"Captured performance metrics for {len(perf_stats)} files.")

            execution_report = f"%% reproduction\n# Command: {cmd_display}\n# Exit Code: {result.returncode}\n"
            if stdout_clean: execution_report += f"# --- STDOUT ---\n{self._comment_block(stdout_clean)}\n"
            if stderr_clean: execution_report += f"# --- STDERR ---\n{self._comment_block(stderr_clean)}\n"

            if result.returncode != 0:
                self.logger.warn(f"Witnessed failure (Exit {result.returncode}). Capturing forensic context.")
                problem_context = f"{problem_context or ''}\n\n[EXECUTION FAILURE]:\n{stderr_clean}\n{stdout_clean}"
            else:
                self.logger.success("Command executed successfully.")

            return execution_report, problem_context, perf_stats, regression_dossier
        except Exception as e:
            self.logger.error(f"Execution faltered: {e}")
            problem_context = f"Execution failed: {e}"
            return "", problem_context, {}, regression_dossier

    def _proclaim_final_dossier(self, start_time: float, written_path: Optional[Path], content: str,
                                profile: DistillationProfile, request: DistillRequest, project_root: Path):
        """[THE LUMINOUS HERALD] Proclaims the final rich dossier of the rite."""
        registers = SimpleNamespace(
            get_duration=lambda: time.monotonic() - start_time,
            files_forged=1 if written_path else 0,
            sanctums_forged=0,
            bytes_written=len(content.encode('utf-8')),
            no_edicts=True,
        )
        est_tokens = len(content) // 4
        gnosis_context = {
            "strategy": profile.strategy,
            "budget_used": f"{est_tokens:,} tokens",
            "output_path": written_path.name if written_path else "Stdout/Clipboard",
            "features_active": [
                feat for feat, active in {
                    "Temporal Inquisitor": request.regression,
                    "Wraith of Celerity": request.profile_perf,
                    "AI Sentinel": request.feature,
                    "Socratic Dialogue": request.interactive,
                    "AI Scribe": request.summarize,
                    "AI Inquisitor": getattr(request, 'diagnose', False)
                }.items() if active
            ],
            **request.variables
        }
        proclaim_apotheosis_dossier(
            telemetry_source=registers,
            gnosis=gnosis_context,
            project_root=project_root,  # <<< THE CRITICAL FIX
            next_steps=[
                f"Gaze upon the scripture: [bold]code {written_path.name}[/bold]" if written_path else "Paste context into your AI."],
            title="✨ Gnostic Distillation Complete ✨",
            subtitle="The reality's soul has been transcribed."
        )

    def _comment_block(self, text: str) -> str:
        """Helper to comment out raw text for blueprint injection."""
        return "\n".join([f"# {line}" for line in text.splitlines()])

    def _parse_cprofile(self, output: str, project_root: Path) -> Dict[str, Dict[str, Any]]:
        """Parses cProfile output to extract performance metrics."""
        stats: Dict[str, Dict[str, Any]] = {}
        pattern = re.compile(r'\s*(\d+)\s+[\d\.]+\s+[\d\.]+\s+([\d\.]+)\s+[\d\.]+\s+(.*):(\d+)\((.*)\)')

        for line in output.splitlines():
            match = pattern.search(line)
            if match:
                calls, cumtime, filename, lineno, funcname = match.groups()
                try:
                    path_obj = Path(filename)
                    if not path_obj.is_absolute():
                        path_obj = (project_root / path_obj).resolve()

                    # We must only consider files within the true project root
                    if path_obj.is_relative_to(project_root):
                        rel_path = str(path_obj.relative_to(project_root)).replace('\\', '/')
                        if rel_path not in stats: stats[rel_path] = {}
                        stats[rel_path][funcname] = {"time": float(cumtime), "calls": int(calls)}
                except (ValueError, FileNotFoundError):
                    continue
        return stats
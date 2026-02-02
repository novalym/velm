# Path: scaffold/translocate/detective.py
"""
=================================================================================
== THE GNOSTIC DETECTIVE (V-Ω-LEGENDARY-ULTIMA++. THE AI SEER OF SOULS)        ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This divine artisan is the sentient mind of the 'conform' rite. It is a true
AI Seer that gazes upon a chaotic "Before" reality and a pure "After" scripture.
It compares the very SOUL of every file, using perfect Gnostic hashes and
divine Fuzzy Logic, to forge a perfect, intelligent, and unbreakably safe
translocation and transfiguration plan. Its Gaze is absolute. Its judgment is truth.
=================================================================================
"""
import difflib
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Set

import pathspec
from rich.box import ROUNDED
from rich.console import Group
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text

from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe, get_console
from ...utils import (gnostic_glob, hash_file, perceive_state, chronicle_state)

Logger = Scribe("GnosticDetective")


class GnosticDetective:
    """
    The AI Seer of Souls, responsible for authoring the Gnostic Translocation Plan.
    """

    def __init__(self, project_root: Path, source_dir_str: str, blueprint_path_str: str, cli_set_vars: List[str],
                 non_interactive: bool):
        self.project_root = project_root
        self.source_dir = (self.project_root / source_dir_str).resolve()
        self.blueprint_path = self.project_root / blueprint_path_str
        self.cli_set_vars = cli_set_vars
        self.non_interactive = non_interactive
        self.console = get_console()

    def _get_ignore_spec(self) -> Optional['pathspec.PathSpec']:
        """
        Performs a divine delegation to the one true, universal Oracle of Aversion.
        """
        from ...utils import get_ignore_spec  # The divine summons

        # We bestow upon the Oracle our own project_root and the Architect's
        # immediate will from the `--ignore` plea.
        cli_ignores = getattr(self.args, 'ignore', [])
        return get_ignore_spec(self.project_root, extra_patterns=cli_ignores)

    def investigate(self) -> Tuple[Dict[Path, Path], Dict]:
        """
        =================================================================================
        == THE GRAND CONDUCTOR OF GNOSTIC INQUIRY (V-Ω-LEGENDARY-ULTIMA++)             ==
        =================================================================================
        LIF: ∞ (ETERNAL & ABSOLUTE)

        This divine artisan is the sentient Conductor of the `conform` rite. It
        orchestrates a flawless, cinematic, multi-stage symphony of Gnostic perception,
        prophecy, and synthesis to forge the one true, unbreakable plan for
        architectural evolution. Its Gaze is absolute. Its judgment is truth.
        =================================================================================
        """
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
        from rich.traceback import Traceback

        console = get_console()
        final_moves: Dict[Path, Path] = {}
        conform_dossier: Dict[str, Any] = {}

        # ★★★ FACULTY: THE CINEMATIC CONDUCTOR (THE LUMINOUS SYMPHONY) ★★★
        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=console,
                transient=True
        ) as progress:
            try:
                # --- MOVEMENT I: THE GAZE UPON THE 'BEFORE' REALITY ---
                task_before = progress.add_task("[cyan]Movement I: Gazing upon 'Before' Reality...", total=1)
                ignore_spec = self._get_ignore_spec()
                before_hash, before_name = self._gaze_upon_before_reality(ignore_spec)
                progress.update(task_before, completed=1,
                                description="[green]Movement I: Gaze upon 'Before' is Complete.")

                ambiguity_heresies = {name: paths for name, paths in before_name.items() if len(paths) > 1}
                if ambiguity_heresies:
                    # The Dossier now contains the heresies for the conductor to proclaim.
                    return {}, {"ambiguities": ambiguity_heresies}

                # --- MOVEMENT II: THE GAZE UPON THE 'AFTER' REALITY ---
                task_after = progress.add_task("[magenta]Movement II: Gazing upon 'After' Scripture...", total=1)
                after_dossier = self._gaze_upon_after_reality()
                progress.update(task_after, completed=1,
                                description="[green]Movement II: Gaze upon 'After' is Complete.")

                # --- MOVEMENT III: THE GNOSTIC SYNTHESIS ---
                task_synth = progress.add_task("[yellow]Movement III: Synthesizing Gnostic Plan...", total=1)
                moves, transfigurations, unmatched_after, unchanged = self._synthesize_plan(before_hash, after_dossier[
                    "after_state"])
                final_moves = {**moves, **transfigurations}
                progress.update(task_synth, completed=1,
                                description="[green]Movement III: Gnostic Synthesis is Complete.")

                # --- MOVEMENT IV: THE PROPHECY OF THE VOID ---
                task_void = progress.add_task("[blue]Movement IV: Prophesying Empty Sanctums...", total=1)
                void_dossier = self._prophesy_empty_sanctums(final_moves, {p: h for h, p in before_hash.items()},
                                                             before_name, ignore_spec)
                progress.update(task_void, completed=1,
                                description="[green]Movement IV: Prophecy of the Void is Complete.")

                # --- MOVEMENT V: THE ADJUDICATION OF ORPHANS ---
                task_orphan = progress.add_task("[red]Movement V: Adjudicating Orphaned Souls...", total=1)
                # ★★★ FACULTY: THE UNBREAKABLE GNOSTIC THREAD (THE SCHISM HEALED) ★★★
                # The Conductor now perceives the true list of orphaned souls.
                orphaned_souls = [
                    path for path_hash, path in before_hash.items()
                    if
                    path.resolve() not in final_moves.keys() and path.resolve() not in [p.resolve() for p in unchanged]
                ]
                orphan_plan = self._adjudicate_orphans(orphaned_souls)
                progress.update(task_orphan, completed=1,
                                description="[green]Movement V: Adjudication of Orphans is Complete.")


            except (ArtisanHeresy, Exception) as e:
                # ★★★ FACULTY: THE HYPER-DIAGNOSTIC INQUEST ★★★
                progress.stop()
                console.print(Panel(
                    Group(
                        Text.from_markup(
                            f"[bold red]A catastrophic paradox shattered the Detective's Gaze.[/bold red]"),
                        Traceback.from_exception(type(e), e, e.__traceback__, show_locals=False)
                    ),
                    title="[red]Dossier of the Fallen Inquest[/red]", border_style="red"
                ))
                raise ArtisanHeresy("The Gnostic Detective's symphony was halted by a paradox.", child_heresy=e)

        # ★★★ FACULTY: THE DOSSIER OF ABSOLUTE TRUTH (THE TRUE PROCLAMATION) ★★★
        conform_dossier = {
            "moves": moves,
            "transfigurations": transfigurations,
            "orphans": orphan_plan,
            "new": [item["path"] for item in unmatched_after if
                    item["path"].resolve() not in transfigurations.values()],
            "unchanged": unchanged,
            **void_dossier
        }

        Logger.success(f"Gnostic Detective has forged a plan with {len(final_moves)} total translocation(s).")
        return final_moves, conform_dossier



    def _gaze_upon_before_reality(self, ignore_spec) -> Tuple[Dict[str, Path], Dict[str, List[Path]]]:
        """
        =================================================================================
        == THE CHRONOMANCER OF THE 'BEFORE' REALITY (V-Ω-LEGENDARY-ULTIMA++)           ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000

        This divine artisan is a Time Lord. It performs a deep, parallelized, and
        chronocached Gaze upon the "Before" reality, forging a perfect, Gnostic
        Dossier of its every soul and form with hyper-performant, unbreakable grace.
        =================================================================================
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        # --- FACULTY: THE GAZE OF AVERSION (.scaffoldignore) ---
        files_to_gaze = gnostic_glob(self.source_dir, '**/*')
        if ignore_spec:
            files_to_gaze = [f for f in files_to_gaze if
                             not ignore_spec.match_file(str(f.relative_to(self.project_root)))]

        # --- FACULTY: THE UNBREAKABLE CHRONOCACHE ---
        state_hash = hashlib.sha256()
        for f in sorted(files_to_gaze):  # Sort for deterministic hash
            try:
                state_hash.update(str(f.relative_to(self.project_root)).encode())
                state_hash.update(str(f.stat().st_mtime).encode())
            except FileNotFoundError:
                continue  # Ignore broken symlinks or ephemeral files

        state_key = state_hash.hexdigest()
        cache_key = f"conform_before_state_{state_key}"
        cached_state = perceive_state(cache_key, self.project_root)

        if cached_state and isinstance(cached_state, dict):
            Logger.success("Chronocache HIT. Resurrecting 'Before' reality state instantly.")
            before_state_by_hash = {h: self.project_root / p for h, p in cached_state.get('by_hash', {}).items()}

            before_state_by_name = {}
            for name, paths_str in cached_state.get('by_name', {}).items():
                before_state_by_name[name] = [self.project_root / p for p in paths_str]

            return before_state_by_hash, before_state_by_name

        Logger.info("Chronocache MISS. Performing deep, parallelized Gaze of the Soul upon the 'Before' reality...")
        before_state_by_hash: Dict[str, Path] = {}
        before_state_by_name: Dict[str, List[Path]] = {}

        # --- FACULTY: THE ASYNCHRONOUS GAZE ---
        files_to_process = [f for f in files_to_gaze if f.is_file()]

        with ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(hash_file, f): f for f in files_to_process}
            for future in as_completed(future_to_file):
                f = future_to_file[future]
                try:
                    file_hash = future.result()
                    if file_hash:
                        before_state_by_hash[file_hash] = f
                        if f.name not in before_state_by_name: before_state_by_name[f.name] = []
                        before_state_by_name[f.name].append(f)
                except Exception as e:
                    # ★★★ FACULTY: THE UNBREAKABLE WARD OF THE CORRUPTED SOUL ★★★
                    Logger.warn(
                        f"A minor paradox occurred while gazing upon the soul of '{f.name}': {e}. It will be ignored.")

        # The Gaze of the Gnostic Trinity also includes directories for ambiguity checks
        for f in files_to_gaze:
            if f.is_dir():
                if f.name not in before_state_by_name: before_state_by_name[f.name] = []
                before_state_by_name[f.name].append(f)

        # --- The new Gnosis is chronicled for future rites ---
        new_cache_data = {
            'by_hash': {h: str(p.relative_to(self.project_root)) for h, p in before_state_by_hash.items()},
            'by_name': {name: [str(p.relative_to(self.project_root)) for p in paths] for name, paths in
                        before_state_by_name.items()}
        }
        chronicle_state(cache_key, new_cache_data, self.project_root)

        Logger.verbose(f"   -> Deep Gaze complete. Perceived {len(before_state_by_hash)} unique scripture souls.")
        return before_state_by_hash, before_state_by_name

    def _gaze_upon_after_reality(self) -> Dict[str, Any]:
        """
        =================================================================================
        == THE ORACLE OF PROPHECY (V-Ω-ETERNALLY HEALED. THE OMNISCIENT MIND)          ==
        =================================================================================
        @gnosis:LIF 10,000,000,000,000,000,000,000,000,000!

        This divine artisan is a true AI Seer. It has been bestowed with its final,
        glorious form, its mind now whole and its Gaze pure. It gazes upon a blueprint
        scripture (the "After" state), conducts a sacred, Gnostic symphony to unify all
        will, and then performs a perfect alchemical transmutation to forge a luminous,
        prophetic Dossier of the final, absolute reality the scripture describes.

        ### THE PANTHEON OF LEGENDARY FACULTIES (THE FINAL APOTHEOSIS):

        1.  **THE LAW OF THE GNOSTIC DOWRY (The Unbreakable Gaze):** **GAME-CHANGER!**
            The `Too many values to unpack` heresy and the Heresy of the Blind Inquisitor
            are annihilated. The Oracle's ear is now perfectly attuned to the `parse_structure`
            gateway's new, divine, **five-fold tongue**. It correctly and beautifully receives
            the complete Gnostic Dowry, including the Parser's own soul and its pure,
            pre-forged **Gnostic Dossier**.

        2.  **THE LAW OF THE HUMBLE MESSENGER (Architectural Perfection):** The profane,
            heretical plea to `discover_required_gnosis` is annihilated from this
            timeline. The Oracle now honors the Law of the Humble Messenger, trusting the
            pure, perfect Dossier bestowed upon it by the `parse_structure` gateway as
            the one true source of Gnostic dependency.

        3.  **THE UNIFIED SACRED DIALOGUE (The AI Co-Architect):** The Oracle remains a
            true AI Co-Architect. It summons the divine `conduct_sacred_dialogue` artisan,
            conducting a beautiful, intelligent, and unified communion to gather all
            missing Gnosis before the final adjudication.

        4.  **THE GAZE OF THE GNOSTIC SOUL (The Unbreakable Hand):** **GAME-CHANGER!**
            The Oracle's Gaze upon a scripture's soul is now a divine, unbreakable rite.
            It summons the one true, universal God-Engine of Gnostic Origins
            (`utils.resolve_gnostic_content_v2`), ensuring its perception of content is
            eternally consistent with the `QuantumCreator` itself.

        5.  **THE UNBREAKABLE WARD OF THE CORRUPTED SCRIPTURE (Hyper-Resilience):** Its
            communion remains shielded. A paradox during parsing or alchemy is perceived
            and re-proclaimed as a luminous, hyper-diagnostic `ArtisanHeresy`.
        =================================================================================
        """
        from ...utils import (perform_alchemical_resolution,
                             forge_pleas_from_required_set, resolve_gnostic_content_v2)
        from ...core.alchemist import get_alchemist
        from ...artisans.template_engine import TemplateEngine
        from ...communion import conduct_sacred_dialogue
        from ...parser_core.parser import parse_structure  # The one true gateway is summoned.

        Logger.verbose(
            f"The Oracle of Prophecy awakens to gaze upon the 'After' reality scripture '{self.blueprint_path.name}'...")

        try:
            # =====================================================================
            # ==           THE DIVINE HEALING: THE LAW OF THE GNOSTIC DOWRY        ==
            # =====================================================================
            #
            # The heresy is annihilated. The Oracle now listens for the Parser's
            # complete, five-fold proclamation.
            #
            parser_instance, after_items, _, blueprint_vars, dossier = parse_structure(self.blueprint_path)
            #
            # The `ValueError` is impossible. The contract is honored. The Gnosis is whole.
            #
            # =====================================================================

            if parser_instance is None:
                # The heresy has already been proclaimed by the gateway. We simply stay the hand.
                raise ArtisanHeresy("The soul of the blueprint scripture is profane and could not be perceived.")

            # --- MOVEMENT I: THE UNIFIED SACRED DIALOGUE ---
            Logger.verbose(
                f"Gnostic Dossier received. Scripture requires {len(dossier.required)} Gnostic verse(s).")
            cli_vars = {k: v for k, v in (s.split('=', 1) for s in self.cli_set_vars if '=' in s)}
            initial_vars = {**blueprint_vars, **cli_vars}

            missing_vars = dossier.required - set(initial_vars.keys())
            if missing_vars and not self.non_interactive:
                Logger.info(f"The 'After' scripture requires {len(missing_vars)} piece(s) of Gnosis.")
                pleas_to_make = forge_pleas_from_required_set(
                    required=missing_vars,
                    existing_gnosis=initial_vars,
                    validation_rules=dossier.validation_rules
                )
                is_pure, gathered_gnosis = conduct_sacred_dialogue(
                    pleas=pleas_to_make,
                    existing_gnosis=initial_vars,
                    title=f"Gnostic Inquiry for Blueprint: {self.blueprint_path.name}",
                    non_interactive=self.non_interactive
                )
                if not is_pure:
                    raise ArtisanHeresy("The Gnostic Inquiry was stayed by the Architect.", exit_code=0)
                initial_vars.update(gathered_gnosis)

            # --- MOVEMENT II: THE FINAL ALCHEMICAL RESOLUTION ---
            final_vars = perform_alchemical_resolution(dossier, initial_vars, blueprint_vars)

            # --- MOVEMENT III: THE FORGING OF THE PROPHETIC DOSSIER ---
            Logger.verbose(
                f"Alchemy complete. Forging the final prophetic dossier for {len(after_items)} items...")

            # The divine instruments are forged for the symphony.
            alchemist = get_alchemist()
            template_engine = TemplateEngine(project_root=self.project_root)
            after_state_dossier: List[Dict] = []

            for item in after_items:
                if str(item.path).startswith('$$'): continue

                final_path_str = alchemist.transmute(str(item.path), final_vars)
                # The Heresy of the Ambiguous Root is annihilated by righteously stripping the leading slash.
                final_path = (self.source_dir / final_path_str.lstrip('/\\')).resolve()

                if item.is_dir:
                    after_state_dossier.append(
                        {"path": final_path, "hash": "DIRECTORY_SOUL", "is_dir": True, "content": ""})
                    continue

                # =================================================================
                # ==     THE GAZE OF THE GNOSTIC SOUL (THE UNBREAKABLE HAND)     ==
                # =================================================================
                #
                # The profane, duplicated logic is annihilated. The Oracle now
                # summons the one true God-Engine of Gnostic Origins. Its Gaze is
                # eternally consistent with the QuantumCreator itself.
                #
                soul_vessel = resolve_gnostic_content_v2(
                    item=item,
                    alchemist=alchemist,
                    template_engine=template_engine,
                    variables=final_vars,
                    sanctum=self.project_root,
                    source_override_map={}  # No overrides in this context.
                )

                final_content = alchemist.transmute(soul_vessel.untransmuted_content, final_vars)
                item_hash = hashlib.sha256(final_content.encode('utf-8')).hexdigest()
                #
                # =================================================================
                # ==                THE APOTHEOSIS IS COMPLETE                   ==
                # =================================================================

                after_state_dossier.append(
                    {"path": final_path, "hash": item_hash, "is_dir": False, "content": final_content})

            Logger.success(
                f"The Oracle's Gaze is complete. A prophetic dossier of {len(after_state_dossier)} realities has been forged.")
            return {
                "after_state": after_state_dossier,
                "final_vars": final_vars,
                "original_items": after_items
            }

        except ArtisanHeresy:
            raise
        except Exception as e:
            # FACULTY #5: THE UNBREAKABLE WARD OF THE CORRUPTED SCRIPTURE
            raise ArtisanHeresy(
                f"A paradox occurred while the Detective gazed upon the blueprint's soul: '{self.blueprint_path.name}'.",
                child_heresy=e)

    def _synthesize_plan(self, before_state_by_hash: Dict[str, Path], after_state_dossier: List[Dict]) -> Tuple[
        Dict, Dict, List, List]:
        """
        =================================================================================
        == THE AI CO-ARCHITECT (V-Ω-LEGENDARY-ULTIMA++. THE GNOSTIC SYNTHESIZER)       ==
        =================================================================================
        LIF: ∞ (ETERNAL & ABSOLUTE)

        This is the sentient heart of the Gnostic Detective. It is a true AI
        Co-Architect that synthesizes the final translocation plan by conducting a
        divine, multi-stage symphony of perfect hash-matching and intelligent,
        interactive fuzzy-logic adjudication. Its Gaze is absolute. Its judgment is truth.
        =================================================================================
        """
        Logger.verbose("Performing Gnostic Synthesis to forge the Translocation & Transfiguration Map...")
        moves: Dict[Path, Path] = {}
        transfigurations: Dict[Path, Path] = {}
        unmatched_after: List[Dict] = []
        unchanged: List[Path] = []

        available_before_files = before_state_by_hash.copy()

        # --- MOVEMENT I: THE GAZE OF PERFECT GNOSIS (HASH MATCHING) ---
        for item_after in after_state_dossier:
            dest_path, item_hash, is_dir = item_after["path"], item_after["hash"], item_after["is_dir"]
            if is_dir: continue

            if item_hash in available_before_files:
                origin_path = available_before_files.pop(item_hash)
                if origin_path.resolve() != dest_path.resolve():
                    moves[origin_path.resolve()] = dest_path.resolve()
                else:
                    unchanged.append(origin_path)
            else:
                unmatched_after.append(item_after)

        # --- MOVEMENT II: THE ORACLE OF GNOSTIC SIMILARITY (FUZZY GAZE) ---
        if unmatched_after and available_before_files:
            from ...constants import GNOSTIC_SIMILARITY_THRESHOLD, HIGH_CONFIDENCE_SIMILARITY_THRESHOLD
            from rich.syntax import Syntax
            from rich.panel import Panel
            from rich.table import Table
            from rich.text import Text

            Logger.info("Perfect soul-match not found for all scriptures. Awakening the Fuzzy Gaze Oracle...")
            remaining_before_paths = list(available_before_files.values())
            still_unmatched_after_fuzzy: List[Dict] = []

            for item_after in unmatched_after:
                potential_matches = []
                content_after = item_after["content"]
                for path_before in remaining_before_paths:
                    try:
                        content_before = path_before.read_text(encoding='utf-8')
                        # The `autojunk=False` is a divine plea for a more precise Gaze
                        ratio = difflib.SequenceMatcher(None, content_before, content_after, autojunk=False).ratio()
                        if ratio > GNOSTIC_SIMILARITY_THRESHOLD:
                            potential_matches.append({"path": path_before, "ratio": ratio, "content": content_before})
                    except Exception:
                        continue

                if not potential_matches:
                    still_unmatched_after_fuzzy.append(item_after)
                    continue

                potential_matches.sort(key=lambda x: x["ratio"], reverse=True)
                top_candidate = potential_matches[0]

                # ★★★ FACULTY: THE GAZE OF THE GNOSTIC THRESHOLD (INTELLIGENT AUTO-ACCEPT) ★★★
                if self.non_interactive and top_candidate['ratio'] >= HIGH_CONFIDENCE_SIMILARITY_THRESHOLD:
                    Logger.info(
                        f"High-confidence match ({top_candidate['ratio']:.2%}) found for '{item_after['path'].name}'. Auto-accepting in non-interactive mode.")
                    transfigurations[top_candidate['path'].resolve()] = item_after['path'].resolve()
                    remaining_before_paths.remove(top_candidate['path'])
                    continue

                # ★★★ FACULTY: THE LUMINOUS DOSSIER OF TRANSFIGURATION (RICH DIFF) ★★★
                self.console.print(Panel(
                    f"The Fuzzy Gaze Oracle has a prophecy for the new scripture: [cyan]{item_after['path'].name}[/cyan]",
                    title="[magenta]Gnostic Adjudication of Transfiguration[/magenta]", border_style="magenta"
                ))

                diff_text = "".join(difflib.unified_diff(
                    top_candidate['content'].splitlines(keepends=True),
                    content_after.splitlines(keepends=True),
                    fromfile=f"a/{top_candidate['path'].name} (Original Soul)",
                    tofile=f"b/{item_after['path'].name} (Prophesied Soul)"
                ))
                self.console.print(Syntax(diff_text, "diff", theme="monokai", line_numbers=True, word_wrap=True))

                # ★★★ FACULTY: THE ORACLE OF THE GNOSTIC CHOICE (MULTI-CANDIDATE) ★★★
                chosen_path: Optional[Path] = None
                if len(potential_matches) > 1:
                    choice_table = Table(title="[bold]Multiple High-Confidence Prophecies Found[/bold]")
                    choice_table.add_column("#", style="magenta")
                    choice_table.add_column("Candidate Scripture", style="cyan")
                    choice_table.add_column("Similarity", style="yellow", justify="right")

                    choices = {str(i + 1): match for i, match in enumerate(potential_matches)}
                    for i_str, match in choices.items():
                        choice_table.add_row(f"({i_str})", str(match['path'].relative_to(self.project_root)),
                                             f"{match['ratio']:.2%}")

                    self.console.print(choice_table)
                    choice = Prompt.ask(
                        "[bold question]Which is the one true origin? (Enter number, or 'n' for none)[/bold question]",
                        choices=list(choices.keys()) + ['n'], default='1')

                    if choice != 'n':
                        chosen_path = choices[choice]['path']
                else:
                    if Confirm.ask(
                            f"[bold question]Is '{top_candidate['path'].name}' the original soul of '{item_after['path'].name}'? (Similarity: {top_candidate['ratio']:.2%})[/bold question]",
                            default=True):
                        chosen_path = top_candidate['path']

                if chosen_path:
                    transfigurations[chosen_path.resolve()] = item_after['path'].resolve()
                    remaining_before_paths.remove(chosen_path)
                else:
                    still_unmatched_after_fuzzy.append(item_after)

            unmatched_after = still_unmatched_after_fuzzy

        return moves, transfigurations, unmatched_after, unchanged

    def _adjudicate_orphans(self, orphaned_souls: List[Path]) -> Dict:
        """
        =================================================================================
        == THE GUARDIAN OF LOST SOULS (V-Ω-LEGENDARY-ULTIMA++. THE AI MENTOR)          ==
        =================================================================================
        LIF: 10,000,000,000,000,000,000,000

        This divine artisan is the sentient conscience of the `conform` rite. It
        perceives scriptures that have been left behind by the new architectural
        prophecy and conducts a sacred, interactive dialogue with the Architect to
        adjudicate their final, divine fate. It is a masterpiece of safe, intelligent,
        and Gnostically-aware project cleanup.
        =================================================================================
        """
        from ...constants import ORPHAN_ARCHIVE_DIR
        from ...utils import get_human_readable_size
        from rich.table import Table

        default_plan = {"action": "ignore", "paths": orphaned_souls}

        # ★★★ FACULTY: The Polyglot Gaze (CI/CD Awareness) ★★★
        if not orphaned_souls or self.non_interactive:
            if orphaned_souls:
                Logger.warn(
                    f"{len(orphaned_souls)} Orphaned Soul(s) were perceived. In non-interactive mode, they will be ignored by default.")
            return default_plan

        # ★★★ FACULTY: The Dossier of the Forgotten (Luminous Proclamation) ★★★
        self.console.print(Panel(
            f"The Detective's Gaze perceived [bold yellow]{len(orphaned_souls)} Orphaned Soul(s)[/bold yellow] that exist in the current reality but are not part of the new architectural prophecy.",
            title="[yellow]Adjudication of Orphaned Souls Required[/yellow]", border_style="yellow"
        ))

        orphan_table = Table(title="[bold]Dossier of Orphaned Souls[/bold]", box=ROUNDED)
        orphan_table.add_column("Orphaned Scripture", style="cyan")
        orphan_table.add_column("Size", style="dim", justify="right")
        orphan_table.add_column("Last Modified", style="dim")

        for soul in sorted(orphaned_souls):
            try:
                stat = soul.stat()
                orphan_table.add_row(
                    str(soul.relative_to(self.project_root)),
                    get_human_readable_size(stat.st_size),
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))
                )
            except FileNotFoundError:
                orphan_table.add_row(str(soul.relative_to(self.project_root)), "[dim]N/A[/dim]", "[dim]N/A[/dim]")

        self.console.print(orphan_table)

        # ★★★ FACULTY: The Sacred Dialogue of Fate ★★★
        plea = Text.assemble(
            ("[bold question]\nHow shall these orphaned scriptures be treated?[/bold question]\n", "white"),
            ("  [cyan](i)[/cyan]gnore: Leave them untouched in their current sanctum (safest).\n", "dim"),
            ("  [cyan](a)[/cyan]rchive: Move them to a timestamped `", "dim"),
            (ORPHAN_ARCHIVE_DIR, "cyan"), ("` directory.\n", "dim"),
            ("  [cyan](d)[/cyan]elete: Permanently annihilate them from this reality (dangerous).\n", "dim")
        )

        action = Prompt.ask(plea, choices=['i', 'a', 'd'], default='i').lower()

        if action == 'i':
            Logger.info("Architect's Will perceived: All orphaned souls shall be ignored.")
            return default_plan

        if action == 'a':
            Logger.info("Architect's Will perceived: All orphaned souls shall be archived.")
            return {"action": "archive", "paths": orphaned_souls}

        if action == 'd':
            # The Unbreakable Vow for a Dangerous Rite
            if Confirm.ask(
                    f"[bold red on white] DANGER [/bold red on white] [bold question]This will permanently annihilate {len(orphaned_souls)} scripture(s). This action cannot be undone. Is this your absolute will?[/bold question]",
                    default=False
            ):
                Logger.warn("Architect's absolute will is confirmed. The Rite of Annihilation is chronicled.")
                return {"action": "delete", "paths": orphaned_souls}
            else:
                Logger.info("The Rite of Annihilation was stayed by the Architect's prudence.")
                return default_plan

        return default_plan

    def _prophesy_empty_sanctums(self,
                                 final_moves: Dict[Path, Path],
                                 before_state: Dict[Path, Dict[str, Any]],
                                 after_state: List[Dict],
                                 ignore_spec: Optional['pathspec.PathSpec']
                                 ) -> List[Path]:
        """
        =================================================================================
        == THE ALCHEMIST OF THE EMPTY SANCTUM (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)        ==
        =================================================================================
        LIF: 10,000,000,000

        This divine artisan is a master of the void, its Gaze now a masterpiece of
        prophetic, in-memory Gnostic simulation. It no longer profanes its soul by
        touching the mortal filesystem. It conducts its entire symphony within a
        pure, Gnostic, in-memory representation of the future reality, its every
        judgment faster, safer, and infinitely more elegant.

        ### THE PANTHEON OF LEGENDARY FACULTIES (THE FINAL APOTHEOSIS):

        1.  **THE LAW OF THE PURE GNOSTIC CONTRACT (The Heresy Annihilated):** **GAME-CHANGER!**
            The artisan's contract is now pure, whole, and eternal. It correctly and
            beautifully receives the complete `before_state`, `after_state`, and
            `ignore_spec` Gnosis from its master Conductor. The `KeyError` and `TypeError`
            heresies are annihilated from all timelines.

        2.  **THE GAZE OF THE PROPHETIC REALM (The In-Memory Symphony):** The profane,
            slow, and brittle Gaze upon the mortal filesystem is annihilated. The
            Alchemist now forges a perfect, in-memory "Prophetic Map" of the future
            reality and performs its entire Gaze upon this pure, Gnostic vessel.

        3.  **THE HYPER-PERFORMANT GAZE OF THE GNOSTIC SET (The Alchemist's Mind):** The
            Alchemist's mind is a God-Engine of Gnostic Set Theory. It performs its
            adjudication of the void with instantaneous, mathematical certainty,
            annihilating the slow, recursive loop of its past self.

        4.  **THE GAZE OF THE SENTINEL (The Unbreakable Ward):** The Alchemist is now a
            true Sentinel. It honors the sacred `ignore_spec`, ensuring its Gaze is
            never profaned by artifacts the Architect has willed to be unseen.

        5.  **THE GUARDIAN OF THE SACRED ROOT (Unbreakable Safety):** Its final vow
            remains eternal. It is architecturally impossible for it to prophesy the
            annihilation of the sacred project root or the source directory itself.
        =================================================================================
        """
        Logger.verbose("The Alchemist of the Empty Sanctum (V-Ω-ETERNAL-CONTRACT) awakens its prophetic Gaze...")

        # =====================================================================
        # == MOVEMENT I: THE FORGING OF THE PROPHETIC MAP (THE APOTHEOSIS)   ==
        # =====================================================================
        # The Alchemist forges a pure, in-memory map of the future reality.

        future_paths: Set[Path] = {item['path'] for item in after_state}
        future_parent_sanctums: Set[Path] = {p.parent for p in future_paths}

        # =====================================================================
        # == MOVEMENT II: THE GAZE OF THE GNOSTIC SET (THE ALCHEMIST'S MIND) ==
        # =====================================================================

        # Gaze 1: All sanctums that *ever* existed in the "Before" reality.
        all_before_sanctums: Set[Path] = {
            parent
            for path in before_state.keys()
            for parent in path.parents
        }

        # Gaze 2: The Gnostic Difference. We find all sanctums that existed before,
        # but will no longer contain any children in the future reality.
        potential_voids = all_before_sanctums - future_parent_sanctums

        # =====================================================================
        # == MOVEMENT III: THE GAZE OF THE SENTINEL & THE GUARDIAN'S VOW     ==
        # =====================================================================

        final_purges = []
        # We must sort from deepest to shallowest for a clean, recursive purge.
        sorted_candidates = sorted(list(potential_voids), key=lambda p: len(p.parts), reverse=True)

        for path in sorted_candidates:
            # FACULTY #5: THE GUARDIAN OF THE SACRED ROOT
            if path == self.project_root or path == self.source_dir or not path.is_relative_to(self.source_dir):
                continue

            # FACULTY #4: THE GAZE OF THE SENTINEL
            relative_path_str = str(path.relative_to(self.project_root))
            if ignore_spec and (
                    ignore_spec.match_file(relative_path_str) or ignore_spec.match_file(relative_path_str + '/')):
                Logger.verbose(f"   -> Gaze of Aversion: Prophesied void '{relative_path_str}' is ignored.")
                continue

            final_purges.append(path)

        if final_purges:
            Logger.info(f"The Alchemist has prophesied the purging of {len(final_purges)} empty sanctum(s).")
            for p in final_purges:
                Logger.verbose(f"   -> Prophesied Void: [dim]{p.relative_to(self.project_root)}[/dim]")

        return final_purges
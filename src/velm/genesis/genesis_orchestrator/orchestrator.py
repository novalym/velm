# Path: scaffold/genesis/genesis_orchestrator/orchestrator.py
# -----------------------------------------------------------
from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING, List, Tuple

from rich.panel import Panel
from rich.prompt import Confirm

from ...contracts.data_contracts import GnosticProphecy, ScaffoldItem
from ...contracts.heresy_contracts import Heresy, ArtisanHeresy
from ...core.blueprint_scribe import BlueprintScribe
from ...logger import Scribe, get_console
from ...utils import generate_derived_names, to_string_safe, chronicle_state
from ..genesis_profiles import PROFILES
from .oracle import GnosticHierarchyOracle

# --- THE DIVINE INHERITANCE (THE MIXINS) ---
from .pleas import PleasMixin
from .prophecy import ProphecyMixin
from .review import ReviewMixin
from .jurisprudence import JurisprudenceMixin

if TYPE_CHECKING:
    from ..genesis_engine.engine import GenesisEngine

Logger = Scribe("GenesisOrchestrator")


class GenesisDialogueOrchestrator(PleasMixin, ProphecyMixin, ReviewMixin, JurisprudenceMixin):
    """
    =================================================================================
    == THE GENESIS DIALOGUE ORCHESTRATOR (V-Ω-MODULAR-GOD-ENGINE-ULTIMA-FORCE)     ==
    =================================================================================
    LIF: 100,000,000,000,000,000,000 (THE OMNISCIENT CONDUCTOR)

    The Sovereign Conductor of the Sacred Dialogue. It unifies the faculties of
    Plea Generation, Prophecy, Review, and Jurisprudence into a single, sentient
    entity.

    ### THE PANTHEON OF 12 NEW ELEVATIONS:
    1.  **The State Alias (The Unified Soul):** `final_gnosis` and `session_gnosis` are
        now quantum-entangled (point to the same object), preventing split-brain heresies.
    2.  **The Auto-Recalibrator:** Automatically updates `project_slug` and `clean_type_name`
        whenever the `project_name` or `project_type` changes during dialogue.
    3.  **The Profile Hydrator:** Instantly absorbs Gnosis from the selected profile
        at the moment of inception, ensuring defaults are correct before the first question.
    4.  **The CLI Injector:** Merges CLI `--set` overrides immediately, granting them
        supreme authority over the default values.
    5.  **The Chronometer:** Tracks the precise duration of the Sacred Dialogue.
    6.  **The Audit Trail:** Maintains a history of answered pleas (`answered_keys`).
    7.  **The Silent Ward:** Automatically configures itself for non-interactive mode
        if the parent engine demands silence.
    8.  **The Prophecy Deriver:** If no prophecy is provided, it summons the `prophesy_initial_gnosis`
        artisan to forge one from the environment.
    9.  **The Heresy Vessel:** Initializes the `adjudicated_heresies` list to catch
        paradoxes during the prophetic phase.
    10. **The Plan Container:** Initializes `prophesied_items` and `prophesied_commands`
        to ensure the Review Mixin never gazes into a void.
    11. **The Safe Stringifier:** Uses `to_string_safe` on all initial inputs to
        prevent type heresies in the text processing layers.
    12. **The Unbreakable Contract:** The `__init__` method is now a fortress, handling
        every possible state of input (None, Partial, Full) with divine grace.
    """

    def __init__(
            self,
            parent_engine: 'GenesisEngine',
            prophecy: Optional[GnosticProphecy] = None,
            final_gnosis: Optional[Dict[str, Any]] = None
    ):
        """
        The Rite of Inception.
        """
        self.engine = parent_engine
        self.console = get_console()
        self.start_time = time.time()

        # --- STATE CONTAINERS (ELEVATION #9 & #10) ---
        self.adjudicated_heresies: List[Heresy] = []
        self.prophesied_items: List[ScaffoldItem] = []
        self.prophesied_commands: List[str] = []
        self.answered_keys: List[str] = []  # ELEVATION #6

        # Check for force or non-interactive at inception
        self.force_mode = getattr(self.engine.cli_args, 'force', False)
        self.non_interactive = getattr(self.engine.cli_args, 'non_interactive', False) or self.force_mode

        # --- PATH A: INJECTED MODE (TUI) ---
        if prophecy and final_gnosis is not None:
            self.prophecy = prophecy
            self.session_gnosis = final_gnosis.copy()  # Copy to prevent external mutation
            Logger.verbose("Orchestrator initialized in Injected Mode (TUI).")

        # --- PATH B: AUTONOMOUS MODE (CLI) ---
        else:
            Logger.verbose("Orchestrator initialized in Autonomous Mode (CLI). Deriving Prophecy...")
            # ELEVATION #8: The Prophecy Deriver
            from ...prophecy import prophesy_initial_gnosis
            raw_defaults = prophesy_initial_gnosis(self.engine.project_root)
            self.prophecy = GnosticProphecy(
                defaults=raw_defaults,
                chronicle={}
            )
            self.session_gnosis = raw_defaults.copy()
            Logger.success(f"Prophecy derived. {len(self.session_gnosis)} default variables loaded.")

        # --- ELEVATION #1: THE STATE ALIAS (UNIFIED SOUL) ---
        # This ensures that mixins accessing 'final_gnosis' see the living 'session_gnosis'
        self.final_gnosis = self.session_gnosis

        # --- ELEVATION #3: THE PROFILE HYDRATOR ---
        # We check if a profile was requested via CLI args on the engine
        cli_args = getattr(self.engine, 'cli_args', argparse.Namespace())
        if hasattr(cli_args, 'profile') and cli_args.profile:
            self.session_gnosis['profile'] = cli_args.profile
            self._hydrate_profile_overrides(cli_args.profile)

        # --- ELEVATION #4: THE CLI INJECTOR ---
        # CLI overrides have the highest precedence. We merge them now.
        if hasattr(cli_args, 'set') and cli_args.set:
            cli_vars = {k: v for k, v in (s.split('=', 1) for s in cli_args.set)}
            self.session_gnosis.update(cli_vars)

        # --- ELEVATION #2: THE AUTO-RECALIBRATOR (INITIAL) ---
        # We must set initial derived values to prevent "NoneType" errors in prompts.
        self._recalibrate_gnosis()

        # --- CONSECRATION OF THE INTERNAL ORACLE ---
        self.oracle = GnosticHierarchyOracle(cli_args, self.session_gnosis, self.prophecy, self)

    def _hydrate_profile_overrides(self, profile_name: str):
        """[ELEVATION #3] Absorbs Gnosis from a Profile."""
        if profile_name in PROFILES:
            overrides = PROFILES[profile_name].get('gnosis_overrides', {})
            # We only apply overrides that haven't been set yet (respecting current state)
            # OR we force them? Usually, Profile > System Default.
            for k, v in overrides.items():
                if k not in self.session_gnosis:
                    self.session_gnosis[k] = v
            Logger.verbose(f"Hydrated {len(overrides)} overrides from profile '{profile_name}'.")

    def _recalibrate_gnosis(self):
        """
        [ELEVATION #2] THE AUTO-RECALIBRATOR.
        Updates derived state (slugs, clean types) based on current variables.
        """
        # 1. Project Slug
        raw_name = to_string_safe(self.session_gnosis.get('project_name', self.engine.project_root.name))
        if raw_name == "." or not raw_name: raw_name = "my-new-project"

        derived = generate_derived_names(raw_name)
        self.current_project_slug = derived.get('name_slug', 'my-app')

        # Update session state to match
        self.session_gnosis['project_slug'] = self.current_project_slug
        self.session_gnosis.update(derived)

        # 2. Clean Type Name
        ptype = self.session_gnosis.get('project_type', 'generic')
        self.current_clean_type_name = str(ptype).split(' ')[0].lower()
        self.session_gnosis['clean_type_name'] = self.current_clean_type_name

    def _get_plea_default_value(self, key: str, default_val_override: Optional[Any] = None) -> Any:
        return self.oracle.get_default(key, default_val_override)

    def conduct_cinematic_symphony(self) -> Tuple[bool, Dict[str, Any]]:
        """
        THE GRAND RITE OF INTERACTIVE GENESIS.
        """

        # [THE FORCE BYPASS]
        if self.force_mode:
            Logger.info("Force mode active. Bypassing Sacred Dialogue. The Prophecy shall be absolute.")
            # Ensure critical defaults are set if missing from prophecy
            self._ensure_critical_defaults()
            self._conduct_prophetic_symphony()
            return True, self.session_gnosis

        self.console.print(Panel(
            "Welcome to the Rite of Gnostic Genesis. Let us forge the soul of your new reality, together.",
            title="[bold magenta]Sentient Guide Awakens[/bold magenta]"
        ))

        # Lazy import to avoid circular dependency
        from .genesis_pleas import GENESIS_PLEAS_GRIMOIRE
        from ...communion import conduct_sacred_dialogue

        # The Score
        dialogue_movements = [
            ("I. The Soul of the Project", ['project_name', 'author', 'description', 'project_type']),
            ("II. The Gnostic Toolchain", ['use_poetry', 'database_type', 'frontend_framework', 'testing_framework']),
            ("III. Architectural Philosophy",
             ['project_structure_pattern', 'auth_method', 'env_vars_setup', 'default_port']),
            ("IV. The DevOps Realm",
             ['license', 'use_git', 'initial_commit_message', 'use_ci', 'use_docker', 'observability_setup',
              'cloud_provider']),
            ("V. The Co-Architect's Communion",
             ['use_vscode', 'project_goals', 'custom_globals', 'ai_code_generation_consent',
              'generate_ai_description']),
        ]

        try:
            for title, keys_in_movement in dialogue_movements:

                # [RECALIBRATE BEFORE EACH MOVEMENT]
                # Ensure previous answers influence current prompts (e.g. slug in prompts)
                self._recalibrate_gnosis()

                all_possible_pleas = self.build_core_pleas()
                pleas_to_make = [
                    p for p in all_possible_pleas
                    if p.key in keys_in_movement and p.key not in self.session_gnosis
                ]

                if not pleas_to_make:
                    newly_adjudicated_heresies = self._adjudicate_gnostic_purity(self.session_gnosis)
                    self._proclaim_mentorship_dossier(newly_adjudicated_heresies, keys_in_movement)
                    continue

                self.console.rule(f"[bold cyan]{title}[/bold cyan]", style="cyan")

                is_pure, gathered_gnosis = conduct_sacred_dialogue(
                    pleas=pleas_to_make,
                    existing_gnosis=self.session_gnosis,
                    title=title,
                    non_interactive=False
                )

                if not is_pure:
                    raise KeyboardInterrupt("Rite Aborted")

                # Update State
                self.session_gnosis.update(gathered_gnosis)
                self.answered_keys.extend(gathered_gnosis.keys())  # Elevation #6

                # Recalibrate after answers
                self._recalibrate_gnosis()

                newly_adjudicated_heresies = self._adjudicate_gnostic_purity(self.session_gnosis)
                self._proclaim_mentorship_dossier(newly_adjudicated_heresies, list(gathered_gnosis.keys()))
                self._display_dialogue_summary(f"Dossier for {title}", gathered_gnosis, list(gathered_gnosis.keys()))

            self.console.rule("[bold magenta]Altar of Final Adjudication[/bold magenta]", style="magenta")

            all_active_keys = [p['key'] for p in GENESIS_PLEAS_GRIMOIRE if p['key'] in self.session_gnosis]
            self._display_dialogue_summary("Grand Dossier of Gnostic Will", self.session_gnosis, all_active_keys)

            if not Confirm.ask(
                    "\n[bold question]This Gnosis is whole and pure. Shall the Great Work of creation begin?[/bold question]",
                    default=True):
                return False, self.session_gnosis

            # Chronomancer's Hand
            if self.session_gnosis.get("author"):
                chronicle_state("last_author_name", self.session_gnosis.get("author"))

            # The Final Delegation to the Prophet
            self._conduct_prophetic_symphony()

            return True, self.session_gnosis

        except (KeyboardInterrupt, EOFError):
            self.console.print("\n[yellow]The Architect has stayed the Rite of Genesis.[/yellow]")
            return False, self.session_gnosis

    def _ensure_critical_defaults(self):
        """Ensures that in Force mode, we don't crash on missing keys."""
        defaults = {
            "project_name": self.engine.project_root.name,
            "project_slug": self.engine.project_root.name.lower().replace(" ", "-"),
            "author": "The Architect",
            "description": "A new reality forged by Scaffold.",
            "project_type": "generic",
            "use_git": True,
            "license": "MIT"
        }
        for k, v in defaults.items():
            if k not in self.session_gnosis:
                self.session_gnosis[k] = v
        self._recalibrate_gnosis()

    def _conduct_prophetic_symphony(self):
        """
        THE GRAND ORCHESTRATOR OF PROPHECY.
        Synthesizes the final plan.
        """
        Logger.info("The Grand Orchestrator of Prophecy awakens...")
        try:
            # 1. Final Alchemy
            self._recalibrate_gnosis()
            gnosis = self.session_gnosis
            Logger.verbose(f"Alchemy Complete. Slug: {self.current_project_slug}")

            # 2. Prophecy
            self.adjudicated_heresies = self._adjudicate_gnostic_purity(gnosis)
            self.prophesied_items, prophecies_for_review = self._prophesy_structure(gnosis)
            self.prophesied_commands = self._prophesy_commands(gnosis)

            # 3. Review
            if not self.non_interactive:
                self._present_interactive_blueprint_review(
                    prophecies_for_review,
                    self.prophesied_commands,
                    self.adjudicated_heresies
                )
            else:
                Logger.info("Silent Prophecy Complete.")

        except Exception as e:
            raise ArtisanHeresy(f"A catastrophic paradox occurred during the Prophetic Symphony: {e}", child_heresy=e)

    # --- HELPER ARTISANS (Export/Import State) ---

    def _archive_session_gnosis(self, path: Optional[Path] = None) -> None:
        import json
        target = path or self.engine.project_root / ".scaffold/genesis_state.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        pure_gnosis = {k: v for k, v in self.session_gnosis.items() if
                       isinstance(v, (str, int, bool, float, list, dict))}
        target.write_text(json.dumps(pure_gnosis, indent=2), encoding='utf-8')
        Logger.verbose(f"Session Gnosis preserved at: {target}")

    def _resurrect_session_gnosis(self, path: Optional[Path] = None) -> bool:
        import json
        target = path or self.engine.project_root / ".scaffold/genesis_state.json"
        if not target.exists(): return False
        try:
            data = json.loads(target.read_text(encoding='utf-8'))
            self.session_gnosis.update(data)
            self._recalibrate_gnosis()
            Logger.success(f"Resurrected {len(data)} Gnostic truths.")
            return True
        except Exception:
            return False

    def _export_prophecy_to_blueprint(self, path: Path):
        scribe = BlueprintScribe(self.engine.project_root)
        content = scribe.transcribe(
            items=self.prophesied_items,
            commands=self.prophesied_commands,
            gnosis=self.session_gnosis,
            rite_type="Genesis Crystal"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        Logger.success(f"Prophecy crystallized into blueprint: [cyan]{path}[/cyan]")
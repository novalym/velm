# Path: scaffold/artisans/watchman/artisan.py
# -------------------------------------------
import time
from pathlib import Path
from typing import Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import WatchmanRequest
from ...help_registry import register_artisan
from ...contracts.heresy_contracts import ArtisanHeresy

# Local Modules
from .profiles import resolve_profile, WATCH_PROFILES
from .ui import SentinelUI
from .engine import KineticEngine, GnosticHandler, Observer


@register_artisan("watch")
class WatchmanArtisan(BaseArtisan[WatchmanRequest]):
    """
    =============================================================================
    == THE WATCHMAN (V-Ω-SENTINEL-PRIME)                                       ==
    =============================================================================
    LIF: 10,000,000,000

    The Sovereign of Local Vigilance.
    It unifies the Profile System with the Kinetic Engine to provide an
    instant, configured, and resilient file-watching experience.
    """

    def execute(self, request: WatchmanRequest) -> ScaffoldResult:
        if Observer is object:
            return self.failure("The Watchman requires 'watchdog'. pip install watchdog")

        # --- MOVEMENT I: THE RESOLUTION OF INTENT ---
        # The 'target' in the request is polymorphic. Is it a profile or a glob?
        # Note: Grimoire maps the positional arg to 'target'.
        # We need to check if 'target' is available on the request object.
        # Based on the previous Request definition, we might need to adjust or read 'glob_pattern'
        # if the grimoire mapped it there.
        # Let's assume the request object has `glob_pattern` populated from the positional arg.

        target_input = request.glob_pattern  # Mapped from 'target' in Grimoire

        profile = resolve_profile(target_input)

        final_glob = target_input
        final_command = request.command_to_run
        ignore_list = []
        profile_name = None

        if profile:
            self.logger.info(f"Watchman recognized profile: [magenta]{profile.name}[/magenta]")
            final_glob = profile.glob
            # Allow CLI override of command even with profile
            if not final_command:
                final_command = profile.command
            ignore_list = profile.ignore or []
            profile_name = profile.name
        else:
            # Custom Mode
            if not final_command:
                # Try to be smart? No, explicit is better.
                # Check if they just typed "scaffold watch" with no args?
                if not target_input:
                    return self._suggest_profiles()

                return self.failure(
                    f"No profile named '{target_input}' found, and no --exec command provided.",
                    suggestion=f"Use `scaffold watch <profile>` or `scaffold watch <glob> --exec <cmd>`."
                )

        # --- MOVEMENT II: THE CONSECRATION OF THE UI ---
        ui = SentinelUI(self.console)

        # Determine Clear Screen behavior
        # We pass this via extra_args or assume default behavior
        should_clear = not getattr(request, 'no_clear', False)  # Inferred flag

        ui.header(final_glob, final_command, profile_name)

        # --- MOVEMENT III: THE ENGINE AWAKENS ---
        engine = KineticEngine(
            command=final_command,
            root=self.project_root,
            restart=getattr(request, 'restart', True)
        )

        def on_trigger_callback(path: Path):
            if should_clear:
                ui.header(final_glob, final_command, profile_name)
            ui.on_trigger(str(path.relative_to(self.project_root)))
            # Engine execution happens inside the handler thread for responsiveness
            # But UI updates for success/fail happen here?
            # The Handler calls engine.trigger() which blocks until done.
            # We can instrument KineticEngine to callback UI.
            # For simplicity, KineticEngine returns code.

            # Note: This runs in the Timer thread. Rich is thread-safe mostly.

            # To get the result code, we'd need to modify the flow.
            # The Handler calls this BEFORE triggering.
            pass

            # We need a slightly smarter handler to report success/fail back to UI

        # Let's patch the handler logic here or rely on the engine logs.
        # Actually, let's subclass the Handler inline or inject a wrapper.

        # Real-time UI wrapper
        def ui_wrapper(path: Path):
            if should_clear: ui.header(final_glob, final_command, profile_name)
            ui.on_trigger(str(path.relative_to(self.project_root)))

            start = time.time()
            code = engine.trigger(path)
            duration = time.time() - start

            if code == 0:
                ui.on_success(duration)
            else:
                ui.on_failure(duration, code)

        handler = GnosticHandler(
            engine=engine,
            glob=final_glob,
            ignore=ignore_list,
            debounce=request.debounce,
            callback=ui_wrapper
        )

        observer = Observer()
        observer.schedule(handler, str(self.project_root), recursive=True)
        observer.start()

        self.console.print("[dim]The Sentinel is active. Watching for flux...[/dim]")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            self.console.print("\n[yellow]The Vigil is ended.[/yellow]")

        observer.join()
        return self.success("Vigil concluded.")

    def _suggest_profiles(self) -> ScaffoldResult:
        """[FACULTY 2] Smart Suggestions based on project content."""
        from rich.table import Table

        table = Table(title="Available Watch Profiles", border_style="cyan")
        table.add_column("Profile", style="magenta")
        table.add_column("Pattern", style="yellow")
        table.add_column("Command", style="green")
        table.add_column("Description")

        # Detect relevant ones
        relevant = []
        for key, p in WATCH_PROFILES.items():
            is_relevant = False
            # Simple heuristic
            if key == "rust" and (self.project_root / "Cargo.toml").exists(): is_relevant = True
            if key == "node" and (self.project_root / "package.json").exists(): is_relevant = True
            if key == "python" and ((self.project_root / "pyproject.toml").exists() or list(
                self.project_root.glob("*.py"))): is_relevant = True
            if key == "go" and (self.project_root / "go.mod").exists(): is_relevant = True

            if is_relevant:
                relevant.append(p)
                table.add_row(f"★ {p.name}", p.glob, p.command, p.help_text, style="bold")
            else:
                table.add_row(p.name, p.glob, p.command, p.help_text, style="dim")

        self.console.print(table)

        suggestion = "Use `scaffold watch <profile>`."
        if relevant:
            suggestion = f"Detected {relevant[0].name} project. Try: `scaffold watch {relevant[0].name}`"

        return self.failure("No target specified.", suggestion=suggestion)
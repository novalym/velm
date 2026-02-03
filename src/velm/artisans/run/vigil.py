# Path: artisans/run/vigil.py
# ---------------------------

import threading
import time
from pathlib import Path
from typing import Optional

from ...core.artisan import BaseArtisan
from ...interfaces.requests import RunRequest
from ...logger import Scribe, get_console
from ...utils import hash_file

class ChronomancerVigil:
    """
    =================================================================================
    == THE CHRONOMANCER'S VIGIL (V-Ω-ETERNAL-APOTHEOSIS. THE SELF-HEALING LOOP)    ==
    =================================================================================
    This divine artisan is the living soul of the `--vigil` vow. It is a self-aware,
    self-healing, and unbreakable temporal loop. It conducts an initial rite and then
    fixes its Gaze upon the scripture's soul, automatically re-conducting the rite
    whenever the Architect's will is transfigured. Its purpose is singular and pure.
    =================================================================================
    """

    def __init__(self, conductor: 'BaseArtisan', scripture_path: Path, request: RunRequest, true_sanctum: Path):
        self.conductor = conductor
        self.scripture_path = scripture_path
        self.request = request
        self.true_sanctum = true_sanctum
        self.logger = Scribe("ChronomancerVigil")
        self.console = get_console()

    def conduct(self):
        """The one true rite of the Vigil."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        self.logger.info(f"The Eternal Sentinel awakens its Gaze upon [cyan]{self.scripture_path.name}[/cyan]...")
        self.console.print(
            "\n[bold green]👁️  The Sentinel is watching for changes to the scripture. Press Ctrl+C to rest.[/bold green]")

        class VigilHandler(FileSystemEventHandler):
            def __init__(self, artisan: 'ChronomancerVigil', initial_hash: str):
                self.artisan = artisan
                self.last_hash = initial_hash
                self._debounce_timer: Optional[threading.Timer] = None

            def on_modified(self, event):
                if Path(event.src_path).resolve() == self.artisan.scripture_path.resolve():
                    if self._debounce_timer: self._debounce_timer.cancel()
                    self._debounce_timer = threading.Timer(0.5, self._run_if_changed)
                    self._debounce_timer.start()

            def _run_if_changed(self):
                try:
                    new_hash = hash_file(self.artisan.scripture_path)
                    if new_hash != self.last_hash:
                        self.last_hash = new_hash
                        self.artisan.console.clear()
                        self.artisan.console.rule(
                            f"[yellow]Change perceived at {time.strftime('%H:%M:%S')}. Re-conducting rite...[/yellow]")

                        run_request = self.artisan.request.model_copy(update={"vigil": False})

                        # We summon the master Conductor's `execute` method directly.
                        # This is an in-process, recursive plea.
                        self.artisan.conductor.execute(run_request)
                    else:
                        self.artisan.logger.verbose(
                            "Vigil perceived a modification, but the scripture's soul is unchanged (hash match).")
                except Exception as e:
                    self.artisan.logger.error(f"A paradox occurred during the vigil's re-run. The Gaze remains fixed.",
                                              exc_info=True)
                    self.artisan.console.print(f"\n[bold red]Heresy perceived during re-run:[/bold red] {e}")

        try:
            # Movement I: The Initial Rite
            initial_content_hash = hash_file(self.scripture_path)
            self.conductor.execute(self.request.model_copy(update={"vigil": False}))

            # Movement II: The Forging of the Eye
            handler = VigilHandler(self, initial_content_hash)
            observer = Observer()
            observer.schedule(handler, str(self.scripture_path.parent), recursive=False)
            observer.start()

            # Movement III: The Eternal Gaze
            while True:
                self.console.print("[dim].[/dim]", end="")
                time.sleep(5)

        except KeyboardInterrupt:
            self.logger.info("Architect's will for rest is perceived.")
        finally:
            if 'observer' in locals() and observer.is_alive():
                observer.stop()
                observer.join()
            self.console.print()
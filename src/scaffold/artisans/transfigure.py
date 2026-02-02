# Path: scaffold/artisans/transfigure.py
# --------------------------------------

import difflib
import hashlib
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Tuple, Optional

from .. import utils
from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.alchemist import get_alchemist
from ..core.artisan import BaseArtisan
from ..core.kernel.transaction import GnosticTransaction
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import TransfigureRequest
from ..logger import Scribe

try:
    from rich.panel import Panel
    from rich.text import Text
    from rich.table import Table
    from rich.console import Group as RenderGroup
    from rich.syntax import Syntax
except ImportError:
    Panel = Text = Table = RenderGroup = Syntax = object

Logger = Scribe("Transfigurator")

@register_artisan("transfigure")
class TransfigureArtisan(BaseArtisan[TransfigureRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC INSCRIPTION (V-Ω-GUARDED-TRANSMUTATION)           ==
    =================================================================================
    LIF: 10,000,000,000,000

    This artisan performs the **Rite of Transfiguration**. It surgically modifies the
    soul (content) of a single scripture with atomic precision, Gnostic intelligence,
    and now, **Unbreakable Safety**.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Gaze of Intent:** Resolves content from Template, String, File, or Stdin.
    2.  **The Alchemical Mixer:** Injects variables (`{{ var }}`) into the new soul.
    3.  **The Guardian's Offer (New):** Automatically offers a pre-flight snapshot
        if the target exists, protecting against accidental lobotomy.
    4.  **The Mode Selector:** Supports `Append`, `Prepend`, or `Overwrite` (Default).
    5.  **The Atomic Hand:** Uses `atomic_write` for safe filesystem operations.
    6.  **The Transactional Soul:** Records the change in `scaffold.lock` for undo.
    7.  **The Idempotency Check:** Calculates hashes to avoid redundant writes.
    8.  **The Interactive Editor:** Can summon `code`/`vim` for manual intervention.
    9.  **The Git Sentinel:** Can refuse to touch untracked files (`--guardian`).
    10. **The Syntax Inquisitor:** Lints the new content for secrets or complexity.
    11. **The Dry-Run Prophet:** Renders a luminous Diff of the proposed change.
    12. **The Void Creator:** Can optionally forge the file if it does not exist.
    =================================================================================
    """

    def __init__(self, engine):
        super().__init__(engine)
        self.alchemist = None
        self.global_forge: Optional[Path] = None
        self.local_forge: Optional[Path] = None
        self.args: Optional[TransfigureRequest] = None

    def execute(self, request: TransfigureRequest) -> ScaffoldResult:
        self.args = request
        self.alchemist = get_alchemist()
        self.global_forge = Path.home() / ".scaffold" / "templates"
        self.local_forge = self.project_root / ".scaffold" / "templates"

        target_path = (self.project_root / request.path_to_scripture).resolve()

        # 1. The Interactive Rite
        if request.interactive:
            self._open_in_editor(target_path)
            return self.success(f"Interactive rite complete for {target_path.name}")

        # 2. Perceive the New Soul
        intended_soul, origin = self._perceive_soul_of_intent()

        # 3. Validate Target Existence
        if not target_path.exists():
            if not request.create_if_void:
                raise ArtisanHeresy(
                    f"Cannot transfigure a void. The scripture '{target_path.name}' does not exist.",
                    suggestion="Use `--create-if-void` to forge it from nothing."
                )
            original_content = ""
            target_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            if target_path.is_dir():
                raise ArtisanHeresy("Heresy of Form: Cannot transfigure a sanctum (directory).")
            try:
                original_content = target_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                raise ArtisanHeresy("Binary Soul Detected: Cannot transfigure a binary file.")

        # 4. The Git Sentinel
        if request.guardian:
            if not self._is_tracked_by_git(target_path):
                raise ArtisanHeresy(f"Sentinel's Ward: '{target_path.name}' is not tracked by Git. The rite is stayed.")

        # 5. Calculate the Transmutation
        final_content = ""
        rite_description = ""

        if request.append:
            final_content = original_content + intended_soul
            rite_description = "Soul Appended"
        elif request.prepend:
            final_content = intended_soul + original_content
            rite_description = "Soul Prepended"
        else:
            final_content = intended_soul
            rite_description = "State Ensured (Overwrite)"

        # 6. Idempotency Check
        final_fingerprint = hashlib.sha256(final_content.encode('utf-8')).hexdigest()
        current_fingerprint = hashlib.sha256(original_content.encode('utf-8')).hexdigest()

        if final_fingerprint == current_fingerprint:
            if request.lint:
                self._lint_scripture(final_content, target_path.name)
            return self.success(f"Gnostic State Confirmed for '{target_path.name}'. No transmutation required.")

        # [ELEVATION 13] THE GUARDIAN'S OFFER
        # If the scripture exists and we are about to change it, we invoke the Universal Guardian.
        # This handles --force (skip), --non-interactive (auto), and interactive prompt.
        if target_path.exists():
            self.guarded_execution([target_path], request, context="transfigure")

        # 7. The Dry-Run Prophet
        if request.preview or request.dry_run:
            self._show_diff(original_content, final_content, target_path.name)
            return self.success("Dry Run: Transfiguration simulated.")

        # 8. The Transactional Symphony
        with GnosticTransaction(self.project_root, f"Transfigure {target_path.name}", Path("manual/transfigure"), use_lock=False) as tx:
            write_result = utils.atomic_write(
                target_path=target_path,
                content=final_content,
                logger=Logger,
                verbose=request.verbosity > 0,
                sanctum=self.project_root,
                backup=request.backup, # Keeps local .bak support alongside the global snapshot
                force=request.force
            )

            if not write_result.success:
                raise ArtisanHeresy("Atomic Inscription failed.")

            tx.record(write_result)

        # 9. Post-Rite Inquisition
        if request.lint:
            self._lint_scripture(final_content, target_path.name)

        return self.success(
            f"Transfiguration complete: {rite_description}",
            data={"fingerprint": final_fingerprint[:12], "origin": origin},
            artifacts=[Artifact(path=target_path, type="file", action="modified")]
        )

    def _resolve_template_soul(self) -> Tuple[Optional[str], str]:
        """Finds the template in Local or Global forge."""
        target_path = Path(self.args.path_to_scripture)

        def _read_safely(path: Path) -> Optional[str]:
            try:
                return path.read_text(encoding='utf-8')
            except Exception:
                return None

        # 1. Check Local Forge (Project Specific)
        local_path = self.local_forge / target_path
        if local_path.is_file():
            c = _read_safely(local_path)
            if c: return c, f"Local Soul ({local_path.relative_to(self.project_root)})"

        # 2. Check Global Forge (User Specific - Named)
        global_named_path = self.global_forge / target_path.name
        if global_named_path.is_file():
            c = _read_safely(global_named_path)
            if c: return c, f"Immortal Soul ({target_path.name})"

        # 3. Check Global Forge (Extension Based)
        ext = target_path.suffix
        if ext:
            # e.g. template.py
            global_ext_path = self.global_forge / f"template{ext}"
            if global_ext_path.is_file():
                c = _read_safely(global_ext_path)
                if c: return c, f"Common Form (template{ext})"

        return None, "The Void"

    def _perceive_soul_of_intent(self) -> Tuple[str, str]:
        """Resolves the content to be written from various sources."""
        raw_content: Optional[str] = None
        origin: str = "Unknown"

        if self.args.from_template:
            raw_content, origin = self._resolve_template_soul()
            if raw_content is None:
                raise ArtisanHeresy(f"No template soul found for '{self.args.path_to_scripture}'.")
        elif self.args.content is not None:
            raw_content, origin = self.args.content, "Direct Gnosis"
        elif self.args.from_source is not None:
            source_path = self.project_root / self.args.from_source
            if not source_path.is_file():
                raise ArtisanHeresy(f"Source void at: {source_path}")
            raw_content, origin = source_path.read_text(encoding='utf-8'), f"Scripture ({self.args.from_source})"
        elif self.args.from_stdin:
            if sys.stdin.isatty():
                Logger.warn("Reading from Stdin (TTY)... Press Ctrl+D to end.")
            raw_content, origin = sys.stdin.read(), "Celestial River (stdin)"
        else:
            return "", "The Void (Interactive)"

        # Transmute variables
        transmuted_content = self.alchemist.transmute(raw_content, self.args.variables)
        return transmuted_content, origin

    def _open_in_editor(self, file_path: Path):
        editor = os.getenv('SCAFFOLD_EDITOR') or os.getenv('VISUAL') or os.getenv('EDITOR')
        if not editor:
            Logger.error("No editor set ($EDITOR).")
            return
        try:
            subprocess.run(shlex.split(editor) + [str(file_path)], check=True)
        except Exception as e:
            raise ArtisanHeresy(f"Editor summon failed: {e}")

    def _is_tracked_by_git(self, path: Path) -> bool:
        try:
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", str(path)],
                cwd=self.project_root,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def _show_diff(self, old: str, new: str, filename: str):
        diff = "".join(difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=f"a/{filename}",
            tofile=f"b/{filename}"
        ))
        self.console.print(Panel(Syntax(diff, "diff", theme="monokai"), title="Prophecy of Change"))

    def _lint_scripture(self, content: str, filename: str):
        """A humble inquisition for common heresies."""
        heresies = []
        if re.search(r'sk_test_[a-zA-Z0-9]+|api_key|secret_key|password|token\s*[:=]\s*["\']\w+', content, re.I):
            heresies.append("Static Secret Detected")
        if len(content.splitlines()) > 300:
            heresies.append("Monolithic Soul (>300 lines)")

        if heresies:
            t = Table(title="Gnostic Guidance", show_header=False)
            for h in heresies: t.add_row(f"• {h}")
            self.console.print(Panel(t, border_style="yellow"))
        else:
            Logger.success(f"Soul of '{filename}' is pure.")
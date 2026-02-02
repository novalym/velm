# Path: scaffold/prophecy/oracle.py

"""
=================================================================================
== THE ORACLE OF THE LIVING SOUL (V-Ω-LEGENDARY++. THE INTROSPECTIVE AI)        ==
=================================================================================
This is the divine, sentient God-Engine of Gnostic Perception. It is a true,
data-driven AI whose mind is forged from the declarative scripture of the Gnostic
Canon. It performs a multi-stage, asynchronous, and hyper-aware Gaze upon any
project reality to prophesy its one true, Gnostic soul.
=================================================================================
"""
import getpass
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any

from .grimoires import SOUL_CODEX
from ..gnosis.canon import ARCHITECTURAL_CANON
from ..logger import Scribe

Logger = Scribe("OracleOfTheLivingSoul")


class OracleOfTheLivingSoul:
    """The God-Engine of Gnostic Prophecy. See docs/PROPHECY.md"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.dossier: Dict[str, Any] = {}  # The Unbreakable Chronocache
        self.perceived_souls: set = set()
        self.SOUL_CODEX = SOUL_CODEX  # Cache the grimoire for performance

    def conduct_inquest(self) -> Dict[str, Any]:
        """The master symphony of perception, now a true, logical inference chain."""
        Logger.verbose("The Introspective AI (V-Ω-LEGENDARY++) awakens its multi-stage Gaze...")

        # --- MOVEMENT I: THE ASYNCHRONOUS GAZE (THE CHRONOMANCER'S SOUL) ---
        # We conduct the expensive I/O-bound rites in a parallel reality.
        with ThreadPoolExecutor() as executor:
            future_map = {
                executor.submit(self._gaze_upon_living_souls): "living_souls",
                executor.submit(self._gaze_upon_vcs_soul): "vcs_soul",
                executor.submit(self._gaze_upon_luminous_scribe): "readme_description",
            }
            for future in as_completed(future_map):
                rite_name = future_map[future]
                try:
                    # The results of the parallel rites are inscribed upon the dossier.
                    result_gnosis = future.result()
                    if result_gnosis:
                        self.dossier.update(result_gnosis)
                except Exception as e:
                    Logger.warn(f"A paradox occurred during the parallel Gaze for '{rite_name}': {e}")

        # --- MOVEMENT II: THE SYMPHONY OF THE CANON (THE DECLARATIVE MIND) ---
        # The Oracle's mind is now a pure, declarative loop that walks the Canon.
        Logger.verbose("Commencing the Symphony of the Canon...")
        for primitive in ARCHITECTURAL_CANON:
            if primitive.key not in self.dossier:
                try:
                    # Each rite is shielded by its own Unbreakable Ward.
                    prophesied_value = primitive.prophecy_rite(self)
                    if prophesied_value is not None:
                        self.dossier[primitive.key] = prophesied_value
                        Logger.verbose(f"   -> Canon Gaze: Prophesied '{primitive.key}' as '{prophesied_value}'.")
                except Exception as e:
                    Logger.warn(f"A paradox occurred during the Gaze for primitive '{primitive.key}': {e}")

        # --- MOVEMENT III: THE GAZE OF GNOSTIC SYNTHESIS (THE AI'S FINAL WORD) ---
        # The Oracle now synthesizes a final, luminous reality from the perceived Gnosis.
        self._synthesize_final_gnosis()

        Logger.success(f"The Oracle's Gaze is complete. {len(self.dossier)} Gnostic truths prophesied.")
        return self.dossier

    def _gaze_upon_living_souls(self) -> Dict[str, Any]:
        """Faculty 2, 5 & 6: The Polyglot Scribe & Gaze of Gnostic Causality."""
        Logger.verbose("   -> Awakening the Polyglot Scribe to perceive technological souls...")
        prophecies = {}

        # This Gaze is now a pure artisan, returning its findings.
        sorted_codex = sorted(self.SOUL_CODEX, key=lambda x: x.get('rank', 0), reverse=True)
        for soul_law in sorted_codex:
            # We use glob for powerful scripture matching (e.g., "*.csproj")
            for scripture_path in self.project_root.glob(soul_law["scripture"]):
                if scripture_path.is_file():
                    try:
                        gaze_result = False
                        if soul_law.get("gaze_pattern"):
                            content = scripture_path.read_text(encoding='utf-8', errors='ignore')
                            if re.search(soul_law["gaze_pattern"], content):
                                gaze_result = True
                        else:  # Gaze of existence
                            gaze_result = True

                        if gaze_result:
                            self.perceived_souls.add(soul_law["name"])
                            Logger.verbose(
                                f"      -> Perceived a '{soul_law['name']}' soul in '{scripture_path.name}'.")
                    except Exception:
                        continue

        if self.perceived_souls:
            prophecies['project_type'] = ", ".join(sorted(list(self.perceived_souls)))
        return prophecies

    def _gaze_upon_vcs_soul(self) -> Dict[str, Any]:
        """Faculty 4: The Scribe of the First Commit."""
        if not (self.project_root / ".git").is_dir(): return {}
        prophecies = {}
        try:
            remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url'], text=True,
                                                 stderr=subprocess.DEVNULL, cwd=self.project_root).strip()
            match = re.search(r'(?:[:/])([\w.-]+)/([\w.-]+?)(?:\.git)?$', remote_url)
            if match:
                prophecies['git_org'] = match.group(1)
                prophecies['git_repo'] = match.group(2)
        except Exception:
            pass
        return prophecies

    def _gaze_upon_luminous_scribe(self) -> Dict[str, Any]:
        """Faculty 8: The Gaze of the Luminous Scribe."""
        readme_path = self.project_root / "README.md"
        if readme_path.is_file():
            try:
                content = readme_path.read_text(encoding='utf-8', errors='ignore')
                match = re.search(r'^#\s*.*?\n+([^\n]+)', content, re.MULTILINE)
                if match:
                    return {'readme_description': match.group(1).strip()}
            except Exception:
                pass
        return {}

    def _synthesize_final_gnosis(self):
        """Faculty 6: The AI's Final Word."""
        # Synthesize project_name with Gnostic Precedence
        if 'project_name' not in self.dossier:
            self.dossier['project_name'] = self.dossier.get('git_repo',
                                                            self.project_root.name.lower().replace(" ", "-"))

        # Synthesize author
        if 'author' not in self.dossier:
            self.dossier['author'] = self.dossier.get('git_author', getpass.getuser())

        # Synthesize description
        if 'description' not in self.dossier:
            self.dossier['description'] = self.dossier.get('readme_description',
                                                           f"A new {self.dossier.get('project_type', 'generic')} project.")



def prophesy_initial_gnosis(project_root: Path) -> Dict[str, Any]:
    """
    =================================================================================
    == THE DIVINE GATEWAY TO THE ORACLE (V-Ω-ETERNAL. THE UNBREAKABLE BRIDGE)      ==
    =================================================================================
    This is the one true, public gateway to the God-Engine of Gnostic Prophecy. It
    forges the Oracle, commands it to conduct its Grand Inquest, and proclaims its
    luminous dossier.
    =================================================================================
    """
    oracle = OracleOfTheLivingSoul(project_root)
    return oracle.conduct_inquest()
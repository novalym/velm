# Path: artisans/tutorial/quest_giver.py
# --------------------------------------

import json
import subprocess
from pathlib import Path
from typing import Optional, Dict


class QuestGiver:
    """
    Manages the state of the student's journey.
    Handles 'Sabotage' (breaking code) and 'Verification' (running tests).
    """

    def __init__(self, root: Path, data_dir: str):
        self.root = root
        self.data_dir = root / data_dir
        self.progress_file = self.data_dir / "progress.json"
        self.curriculum_file = self.data_dir / "curriculum.json"

    def load_next_quest(self) -> Optional[Dict]:
        if not self.curriculum_file.exists(): return None

        curriculum = json.loads(self.curriculum_file.read_text())
        progress = self._load_progress()

        completed_ids = set(progress.get("completed", []))
        for quest in curriculum["quests"]:
            if quest["id"] not in completed_ids:
                return quest
        return None

    def apply_quest_state(self, quest: Dict):
        """
        The Rite of Sabotage.
        Replaces the target file's content with a broken version (or inserts a bug).
        For V1, we simply append a syntax error or assert False.
        """
        target = self.root / quest["target_file"]
        if not target.exists(): return

        # Backup original
        backup = self.data_dir / f"{quest['id']}_original_{target.name}"
        if not backup.exists():
            import shutil
            shutil.copy2(target, backup)

        # Apply Sabotage (Mock: Replace content with a challenge)
        # In a real version, we'd use AST to replace a function body with `raise NotImplementedError`
        content = target.read_text()
        sabotaged = content + "\n\n# QUEST: Fix this line to proceed!\nraise NotImplementedError('You must implement this!')"
        target.write_text(sabotaged)

    def verify_quest(self) -> bool:
        """Runs the test suite."""
        # Simple heuristic: Run pytest or npm test
        try:
            # We assume the user has fixed it, so we run tests.
            # Real impl needs to target specific tests for the quest.
            if (self.root / "pyproject.toml").exists():
                subprocess.run(["pytest"], cwd=self.root, check=True, capture_output=True)
            elif (self.root / "package.json").exists():
                subprocess.run(["npm", "test"], cwd=self.root, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def advance_progress(self):
        quest = self.load_next_quest()
        if quest:
            prog = self._load_progress()
            prog.setdefault("completed", []).append(quest["id"])
            self.progress_file.write_text(json.dumps(prog))

            # Restore file? Or leave it fixed? Leave it fixed.

    def _load_progress(self) -> Dict:
        if self.progress_file.exists():
            return json.loads(self.progress_file.read_text())
        return {}
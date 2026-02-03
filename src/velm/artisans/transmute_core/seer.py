# Path: artisans/transmute_core/seer.py
# -------------------------------------

import hashlib
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, List, Set, TYPE_CHECKING

from ...contracts.data_contracts import ScaffoldItem
from ...logger import Scribe
from ...utils import hash_file, is_binary

if TYPE_CHECKING:
    from ...artisans.transmute import TransmuteArtisan

Logger = Scribe("GnosticSeer")


@dataclass
class DiskState:
    """The Gnostic Dossier of a single scripture's state in the Mortal Realm."""
    exists: bool
    content_hash: str
    content: Optional[str]
    permissions: Optional[str]
    is_binary: bool
    is_link: bool
    mtime: float
    dependencies: Optional[List[str]]


class GnosticSeer:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC PROPHECY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)          ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000

    This is not a helper class. It is a divine, sentient AI, the central intelligence
    of the Transmutation Rite. It performs a Three-Fold Gaze upon the Past (Lockfile),
    the Future (Blueprint), and the Present (Disk) to forge a perfect, Gnostic Plan
    of Change.

    Its soul has been purified of the "Virtual Root" heresy. It now operates with an
    unbreakable understanding of Absolute Relativity, ensuring its every judgment is
    founded on the one true, immutable reality of the project's sanctum.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Gnostic Anchor:** It perceives the `$$ project_root` or a common path prefix
        from the blueprint and uses it to harmonize the coordinate systems of the Future
        (blueprint) and the Past (lockfile), annihilating the "Mass Move" heresy.

    2.  **The Asynchronous Gaze:** It commands a legion of ephemeral Scribes in a
        parallel reality (`ThreadPoolExecutor`) to gaze upon the filesystem, making
        its perception of the Present near-instantaneous.

    3.  **The Gnostic Triage of Change:** Its `_adjudicate_changes` rite is a masterpiece
        of Gnostic jurisprudence, flawlessly distinguishing between Creation,
        Transfiguration, Annihilation, Conflict, and pure Harmony.

    4.  **The Translocation Oracle:** Its `_detect_translocations` Gaze is one of deep
        wisdom. It perceives a "move" not by its path, but by its soul (hash),
        allowing it to track a scripture's Gnostic essence across any change of form.

    5.  **The Idempotency Ward:** Its Gaze is temporal. It compares the Future hash not just
        against the Past, but against the Present, staying its hand if the Architect's
        will is already manifest, thus preventing redundant writes.

    6.  **The Luminous Dossier:** Its `_forge_update_dossier` rite forges a rich, cinematic
        diff, transforming a simple "update" plan into a luminous prophecy of change.

    7.  **The Unbreakable Gaze:** Its every interaction with the mortal realm (filesystem)
        is shielded by an unbreakable ward, ensuring a single corrupted file cannot
        shatter the entire Gaze.

    8.  **The Gnostic Unification (`_get_item_hash`):** It performs a sacred communion with
        the one true `resolve_gnostic_content_v2` artisan, ensuring its Gaze for a
        scripture's soul is eternally consistent with the Quantum Creator's Hand.

    9.  **The Polyglot Soul:** Its core logic is founded on the universal Gnosis of the
        content hash, making it inherently language-agnostic.

    10. **The Scribe's Voice:** Its every thought is proclaimed to the Gnostic Chronicle,
        making its symphony of perception luminous and transparent for the Architect's
        inquest.

    11. **The Pure Contract:** Its `__init__` and `prophesy` rites are pure, unbreakable
        contracts, their Gnosis whole and their purpose absolute.

    12. **The Sovereign Mind:** It is a pure, self-contained God-Engine, its soul
        unburdened by the profane concerns of execution. It perceives and plans; the
        Transmutator acts.
    =================================================================================
    """

    def __init__(self, artisan: 'TransmuteArtisan', lock_data: Dict, new_plan_items: List[ScaffoldItem],
                 new_vars: Dict):
        """The Rite of Gnostic Inception. The Seer is born with its sacred mission."""
        self.artisan = artisan
        self.project_root = artisan.project_root.resolve()
        self.logger = artisan.logger
        self.new_plan_items = new_plan_items
        self.new_vars = new_vars

        # [THE GNOSTIC ANCHOR]
        self.blueprint_root_prefix = self._find_blueprint_root_prefix(new_plan_items, new_vars)
        if self.blueprint_root_prefix:
            self.logger.info(
                f"Gnostic Anchor perceived. Blueprint paths will be normalized relative to '{self.blueprint_root_prefix}'.")

        # --- THE COORDINATE SYSTEM HARMONIZATION (THE APOTHEOSIS) ---
        # The Gaze of the Past (Lockfile) and the Gaze of the Future (Blueprint)
        # must be normalized to the same coordinate system to prevent a Gnostic Schism.
        raw_lock_manifest = lock_data.get('manifest', {})
        self.lock_manifest = {self._normalize_path(Path(k)): v for k, v in raw_lock_manifest.items()}
        self.new_items_map = {self._normalize_path(item.path): item for item in new_plan_items if item.path}
        # --- THE SCHISM IS HEALED ---

        self.disk_cache: Dict[str, DiskState] = {}
        self.intended_hashes: Dict[str, str] = {}
        self.plan = {"create": [], "delete": [], "move": {}, "update": [], "conflict": [], "unchanged": []}

        self.logger.verbose(f"Seer's Gaze Anchored at Root='{self.project_root.name}' (Absolute Relativity)")


    def _find_blueprint_root_prefix(self, items: List[ScaffoldItem], variables: Dict) -> Optional[str]:
        """[THE GAZE OF THE GNOSTIC ANCHOR V2] Perceives the blueprint's virtual root."""
        # Highest precedence: An explicit `$$ project_root = "name"` variable.
        blueprint_root_var = variables.get('project_root')
        if blueprint_root_var and isinstance(blueprint_root_var, str):
            # Ensure it ends with a slash for consistent stripping.
            return str(Path(blueprint_root_var).as_posix()) + '/'

        if not items: return None
        paths = [item.path for item in items if item.path and len(item.path.parts) > 0]
        if not paths: return None

        try:
            # os.path.commonpath is the most robust way to find a common prefix.
            common_str = os.path.commonpath([str(p) for p in paths])
        except ValueError:
            return None  # Can happen on Windows with different drives, irrelevant here.

        if not common_str or common_str == '.':
            return None

        # We only consider it a true root if it's a single directory.
        common_path = Path(common_str)
        if len(common_path.parts) == 1 and common_path.is_dir:
            prefix = common_path.as_posix() + "/"
            # Final check: does this prefix actually apply to all paths?
            if all(str(p).replace("\\", "/").startswith(prefix) for p in paths):
                return prefix

        return None

    def _normalize_path(self, path: Path) -> str:
        """Strips the virtual root prefix from a blueprint path."""
        path_str = path.as_posix()
        if self.blueprint_root_prefix and path_str.startswith(self.blueprint_root_prefix):
            return path_str[len(self.blueprint_root_prefix):]
        return path_str

    def prophesy(self) -> Dict:
        """The one true, public rite of Gnostic Prophecy."""
        self.logger.verbose("The Gnostic Seer begins its Three-Fold Gaze...")
        self._calculate_intended_state()
        paths_to_gaze = set(self.new_items_map.keys()) | set(self.lock_manifest.keys())
        self._perform_parallel_gaze(paths_to_gaze)
        self._adjudicate_changes()
        self._detect_translocations()
        self.logger.success("The Seer's Prophecy is forged.")
        return self.plan

    def _calculate_intended_state(self):
        """[THE GAZE OF THE ALCHEMIST] Pre-computes the hash of every intended file."""
        self.logger.verbose("Calculating the Gnostic Fingerprint of the Future reality...")
        for path_str, item in self.new_items_map.items():
            self.intended_hashes[path_str] = self._get_item_hash(item)

    def _perform_parallel_gaze(self, paths: Set[str]):
        """[FACULTY 2] Asynchronously scans all relevant files on disk."""
        if not paths:
            self.logger.verbose("The Present is a void. No scriptures to gaze upon.")
            return
        self.logger.verbose(f"Gazing upon {len(paths)} locations in the Mortal Realm...")
        with ThreadPoolExecutor() as executor:
            future_to_path = {executor.submit(self._gaze_at_single_path, p): p for p in paths}
            for future in as_completed(future_to_path):
                self.disk_cache[future_to_path[future]] = future.result()

    def _gaze_at_single_path(self, path_str: str) -> DiskState:
        """[FACULTY 7] Performs a Gaze upon a single path with an Unbreakable Ward."""
        try:
            full_path = self.project_root / path_str
            if not full_path.exists() or not full_path.is_file():
                return DiskState(False, "", None, None, False, False, 0, None)

            is_bin = is_binary(full_path)
            current_hash = hash_file(full_path)
            mtime = full_path.stat().st_mtime
            perms = oct(full_path.stat().st_mode)[-3:]
            content = None
            if not is_bin and full_path.stat().st_size < 1_000_000:
                try:
                    content = full_path.read_text(encoding='utf-8', errors='replace')
                except Exception:
                    pass
            return DiskState(True, current_hash, content, perms, is_bin, full_path.is_symlink(), mtime, None)
        except Exception as e:
            self.logger.warn(f"A minor paradox occurred gazing upon '{path_str}': {e}")
            return DiskState(False, "", None, None, False, False, 0, None)

    def _adjudicate_changes(self):
        """
        =================================================================================
        == THE GRAND ADJUDICATOR (V-Ω-ETERNAL-APOTHEOSIS. THE LAW OF ENTITY DISTINCTION) ==
        =================================================================================
        This is the divine artisan in its final, eternal form. It has been bestowed with
        the Gnostic wisdom to distinguish between a Scripture (a file) and a Sanctum
        (a directory). Its Gaze upon a Sanctum is now one of simple existence, as their
        souls are not chronicled in the lockfile. This annihilates the "Phantom Directory
        Creation" heresy for all time. The Vow of Harmony remains its highest law.
        =================================================================================
        """
        all_paths = set(self.lock_manifest.keys()) | set(self.new_items_map.keys())

        for path_str in all_paths:
            in_future = path_str in self.new_items_map
            in_past = path_str in self.lock_manifest
            disk_state = self.disk_cache.get(path_str)
            exists_in_present = disk_state and disk_state.exists

            item_future = self.new_items_map.get(path_str)

            # --- THE DIVINE ADJUDICATION OF SANCTUMS (THE APOTHEOSIS) ---
            if item_future and item_future.is_dir:
                # A directory's existence is not chronicled in the lockfile's manifest.
                # Its fate is judged solely by its presence in the mortal realm.
                if not exists_in_present:
                    self.plan["create"].append({"item": item_future, "reason": "New sanctum in prophecy."})
                else:
                    # If it exists, it is UNCHANGED. We do not track directory modifications.
                    self.plan["unchanged"].append({"item": item_future, "reason": "Sanctum is already manifest."})
                # The Gaze upon the Sanctum is complete. We avert our gaze from the Scripture-specific laws below.
                continue
            # --- THE HERESY IS ANNIHILATED ---

            hash_future = self.intended_hashes.get(path_str)
            hash_past = self.lock_manifest.get(path_str, {}).get("sha256")
            hash_present = disk_state.content_hash if exists_in_present else None

            # --- MOVEMENT I: THE UNBREAKABLE VOW OF HARMONY ---
            if in_future and in_past and hash_future == hash_past and hash_future == hash_present:
                self.plan["unchanged"].append({"item": item_future, "reason": "Reality is in perfect harmony."})
                continue

            # --- MOVEMENT II: THE GNOSTIC TRIAGE OF CHANGE (FOR SCRIPTURES) ---
            if in_future and not in_past:  # CREATE or UPDATE UNTRACKED
                if not exists_in_present:
                    self.plan["create"].append({"item": item_future, "reason": "New scripture in prophecy."})
                elif hash_present != hash_future:
                    self.plan["update"].append(self._forge_update_dossier(item_future, disk_state))
                else:
                    self.plan["unchanged"].append({"item": item_future, "reason": "Untracked file matches prophecy."})

            elif not in_future and in_past:  # DELETE or CONFLICT
                if exists_in_present and hash_present != hash_past:
                    self.plan["conflict"].append(
                        {"path": path_str, "reason": "Manually modified; now removed from blueprint."})
                else:
                    # This logic path is for files only now.
                    self.plan["delete"].append(
                        {"path": Path(path_str), "hash": hash_past, "reason": "No longer in prophecy."})


            elif in_future and in_past:  # UPDATE or CONFLICT
                if hash_present == hash_past and hash_future != hash_past:
                    self.plan["update"].append(self._forge_update_dossier(item_future, disk_state))
                else:
                    self.plan["conflict"].append(
                        {"path": path_str, "reason": "Blueprint and disk have both diverged from history."})


    def _detect_translocations(self):
        """[FACULTY 4] The Translocation Oracle. Perceives moves by their soul (hash)."""
        deleted_hashes = {d['hash']: d['path'] for d in self.plan['delete'] if d.get('hash')}
        creations_to_check = list(self.plan["create"])

        if not creations_to_check or not deleted_hashes: return

        self.logger.verbose(
            f"The Translocation Oracle gazes upon {len(creations_to_check)} new souls and {len(deleted_hashes)} ghosts...")
        for create_entry in creations_to_check:
            item = create_entry["item"]
            path_key = self._normalize_path(item.path)
            item_hash = self.intended_hashes.get(path_key)

            if item_hash and item_hash in deleted_hashes:
                origin_path = deleted_hashes[item_hash]
                dest_path = item.path  # The path object from the item is already correct (e.g., `scaffold/main.py`)

                self.logger.info(f"Translocation Perceived: Soul of '{origin_path}' reborn as '{dest_path.name}'.")
                self.plan["move"][str(origin_path)] = str(dest_path)

                self.plan["create"].remove(create_entry)
                self.plan["delete"] = [d for d in self.plan["delete"] if d['path'] != origin_path]
                del deleted_hashes[item_hash]

    def _get_item_hash(self, item: ScaffoldItem) -> str:
        """[FACULTY 8] Performs a sacred communion to perceive the true soul of an item."""
        from ...utils.resolve_gnostic_content import resolve_gnostic_content_v2
        try:
            from ...artisans.template_engine import TemplateEngine
            te = TemplateEngine(project_root=self.project_root, silent=True)
            soul_vessel = resolve_gnostic_content_v2(item, self.artisan.alchemist, te, self.new_vars, self.project_root,
                                                     {})

            if soul_vessel.is_binary_copy:
                return hash_file(soul_vessel.binary_source_path)

            final_content = self.artisan.alchemist.transmute(soul_vessel.untransmuted_content, self.new_vars)
            return hashlib.sha256(final_content.encode('utf-8')).hexdigest()
        except Exception as e:
            self.logger.warn(f"Could not calculate intended hash for '{item.path}': {e}")
            return f"__HERESY_HASH_{os.urandom(8).hex()}__"

    def _forge_update_dossier(self, item: ScaffoldItem, disk: DiskState) -> Dict:
        """[FACULTY 6] Creates a rich dossier for Transfiguration rites."""
        import difflib
        old_content = disk.content or ""
        new_content = ""
        try:
            from ...utils.resolve_gnostic_content import resolve_gnostic_content_v2
            from ...artisans.template_engine import TemplateEngine
            te = TemplateEngine(project_root=self.project_root, silent=True)
            soul = resolve_gnostic_content_v2(item, self.artisan.alchemist, te, self.new_vars, self.project_root, {})
            if not soul.is_binary_copy:
                new_content = self.artisan.alchemist.transmute(soul.untransmuted_content, self.new_vars)
        except Exception:
            pass

        is_lobotomy = bool(old_content.strip()) and not bool(new_content.strip())
        diff = ""
        if not disk.is_binary:
            old_lines = old_content.replace('\r\n', '\n').splitlines(keepends=True)
            new_lines = new_content.replace('\r\n', '\n').splitlines(keepends=True)
            if old_lines != new_lines:
                diff_gen = difflib.unified_diff(old_lines, new_lines, fromfile=f"a/{item.path}",
                                                tofile=f"b/{item.path}")
                diff = "".join(diff_gen)
            elif self.intended_hashes.get(self._normalize_path(item.path)) != disk.content_hash:
                diff = "[dim italic]Content identical. Normalizing line endings or whitespace.[/dim italic]"
        return {"item": item, "old_content": old_content, "diff": diff, "is_lobotomy": is_lobotomy}
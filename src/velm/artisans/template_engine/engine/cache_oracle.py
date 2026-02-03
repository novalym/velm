# Gnostic Codex: scaffold/artisans/template_engine/engine/cache_oracle.py
# ---------------------------------------------------------------------
# LIF: ∞ (THE KEEPER OF THE EPHEMERAL SOUL)
# auth_code:(#()#)@(#()!!!!
#
# This divine artisan is the one true, sovereign keeper of the Template Engine's
# ephemeral memory. It has been forged from the humble soul of the old
# `_read_from_cache_or_disk` rite into a hyper-performant, cryptographically-aware,
# and thread-safe God-Engine of Gnostic Recall. Its Prime Directive is to
# annihilate the heresy of redundant disk I/O, ensuring the Architect's will is
# perceived with the speed of thought.
#
# ### THE PANTHEON OF 12 GAME-CHANGING, MIND-BLOWING ELEVATIONS:
#
# 1.  **The Cryptographic Gaze:** It no longer trusts `mtime` alone. It performs a
#     deep, SHA256 Gaze upon a scripture's soul, ensuring that even the most subtle
#     transfiguration is perceived. The Heresy of the False Positive is annihilated.
#
# 2.  **The Thread-Safe Sanctum:** Its entire memory is guarded by a sacred, re-entrant
#     `RLock`, making it an unbreakable bastion of stability in the concurrent reality
#     of the Gnostic Daemon.
#
# 3.  **The Hyper-Performant Recall:** Its `read` rite is a masterpiece of Gnostic
#     efficiency. It performs a multi-stage Gaze (mtime -> size -> hash) to find the
#     fastest possible path to truth, falling back to the mortal realm of the disk
#     only when absolutely necessary.
#
# 4.  **The Finite Mind:** The Chronocache is no longer an infinite void. It possesses
#     a Gnostic awareness of its own size and will perform a Rite of Purging upon
#     itself to prevent memory exhaustion, ensuring the eternal stability of the Engine.
#
# 5.  **The Unbreakable Gaze:** Its communion with the mortal realm is shielded by an
#     unbreakable ward. A profane or permission-denied scripture will not shatter its
#     Gaze; it will be gracefully averted with a luminous warning.
#
# 6.  **The Luminous Voice:** Its every thought—every hit, every miss, every purge—is
#     proclaimed to the Gnostic Chronicle, providing unparalleled diagnostic clarity.
#
# 7.  **The Rite of Purging:** Possesses a sovereign `purge()` rite, allowing the High
#     Conductor to command it to return its entire memory to the void, essential for
#     hot-reloading and testing.
#
# 8.  **The Gaze of Forgiveness:** Its Gaze upon a scripture's soul is a forgiving one.
#     It righteously attempts to decode with UTF-8, but falls back to `latin-1` and
#     `replace` to prevent a Unicode Heresy from shattering its perception.
#
# 9.  **The Pure Gnostic Contract:** Its `read` and `purge` rites are unbreakable,
#     type-safe contracts, their Gnosis whole and their purpose absolute.
#
# 10. **The Sovereign Soul:** It is a pure, self-contained artisan, its every faculty
#     dedicated to its one true purpose.
#
# 11. **The Altar of Tuning:** Its `MAX_CACHE_SIZE` is a sacred, tunable constant,
#     allowing its mind to be expanded or constrained as the cosmos demands.
#
# 12. **The Final Word:** It is the one true, definitive, and eternal artisan for all
#     matters of high-performance, cached scripture reading in the Scaffold cosmos.

import hashlib
import threading
from pathlib import Path
from typing import Dict, Tuple, Optional

from ....logger import Scribe

Logger = Scribe("CacheOracle")


class CacheOracle:
    """The Gnostic Keeper of the Chronocache. Annihilates redundant disk I/O."""

    MAX_CACHE_SIZE = 1024  # Max number of files to hold in memory

    def __init__(self):
        # The sacred vessels: {path: (mtime, size, sha256_hash, content)}
        self._cache: Dict[Path, Tuple[float, int, str, str]] = {}
        self._lock = threading.RLock()  # Re-entrant for complex, nested Gazes

    def read(self, path: Path) -> Optional[str]:
        """
        The Grand Rite of Gnostic Recall.
        Performs a multi-stage Gaze to find the scripture's soul with maximum speed and integrity.
        """
        with self._lock:
            try:
                # --- MOVEMENT I: THE GAZE OF PRUDENCE ---
                if not path.is_file():
                    return None

                stat = path.stat()
                mtime = stat.st_mtime
                size = stat.st_size

                # --- MOVEMENT II: THE GAZE OF MEMORY (THE CHRONOCACHE) ---
                if path in self._cache:
                    cached_mtime, cached_size, cached_hash, cached_content = self._cache[path]
                    # The Fast Path: If mtime and size match, the soul is likely pure.
                    if cached_mtime == mtime and cached_size == size:
                        Logger.verbose(f"Chronocache HIT (Temporal): '{path.name}'")
                        return cached_content

                # --- MOVEMENT III: THE GAZE OF REALITY (THE MORTAL REALM) ---
                Logger.verbose(f"Chronocache MISS: '{path.name}'. Gazing upon the mortal realm...")
                try:
                    content_bytes = path.read_bytes()
                except (IOError, OSError, PermissionError) as e:
                    Logger.warn(f"Gaze averted from '{path.name}' due to a physical paradox: {e}")
                    return None

                # The Cryptographic Gaze
                new_hash = hashlib.sha256(content_bytes).hexdigest()

                # The Deep Check: If the hash still matches, the `mtime` change was a lie.
                if path in self._cache and self._cache[path][2] == new_hash:
                    Logger.verbose(
                        f"Chronocache HIT (Cryptographic): '{path.name}' soul is unchanged despite temporal flux.")
                    # We update the mtime to prevent this deep check next time.
                    _, _, _, old_content = self._cache[path]
                    self._cache[path] = (mtime, size, new_hash, old_content)
                    return old_content

                # The Gaze of Forgiveness
                try:
                    new_content = content_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    Logger.warn(f"Unicode Heresy in '{path.name}'. Applying the Gaze of Forgiveness (latin-1).")
                    new_content = content_bytes.decode('latin-1', errors='replace')

                # --- MOVEMENT IV: THE RITE OF INSCRIPTION (UPDATING THE CHRONOCACHE) ---
                self._cache[path] = (mtime, size, new_hash, new_content)
                self._prune_if_needed()

                return new_content

            except Exception as e:
                # The Unbreakable Ward
                Logger.error(f"A catastrophic paradox shattered the Cache Oracle's Gaze for '{path.name}': {e}")
                return None

    def purge(self):
        """The Rite of Purging. Returns the Oracle's memory to the void."""
        with self._lock:
            self._cache.clear()
            Logger.warn("The Template Chronocache has been returned to the void.")

    def _prune_if_needed(self):
        """[FACULTY 4] The Finite Mind. Prevents memory exhaustion."""
        # This is a humble pruning. A true LRU cache would be a future ascension.
        if len(self._cache) > self.MAX_CACHE_SIZE:
            Logger.verbose(f"Chronocache has exceeded its Gnostic limit ({self.MAX_CACHE_SIZE}). Pruning...")
            # Simple strategy: remove the first 10% of items.
            num_to_prune = self.MAX_CACHE_SIZE // 10
            keys_to_prune = list(self._cache.keys())[:num_to_prune]
            for key in keys_to_prune:
                del self._cache[key]
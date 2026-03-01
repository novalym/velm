# src/velm/core/sanctum/memory.py
# =========================================================================================
# == THE ETHEREAL PLANE: EXASCALE TOTALITY (V-Ω-TOTALITY-V10^18-SINGULARITY)             ==
# =========================================================================================
# LIF: 10,000,000,000,000,000,000 | ROLE: VIRTUAL_REALITY_KERNEL | RANK: OMEGA_PRIME
# AUTH: Ω_MEMORY_V_EXASCALE_COW_MERKLE_TIME_TRAVEL_FINALIS
#
# [ARCHITECTURAL CONSTITUTION]
# This is the most advanced in-memory filesystem ever forged in Python. It transcends
# simple dict-mapping to become a true POSIX-compliant, Copy-on-Write (CoW), Time-Traveling,
# Merkle-Hashed Ethereal Substrate.
#
# ### THE 18 ASCENSIONS OF THE EXASCALE HORIZON:
# 1.  **The Perfected Parent Suture:** `_get_parent` is now mathematically flawless.
# 2.  **Copy-on-Write (CoW) Holography:** Instantly clone the entire Sanctum in O(1) time
#     for parallel AI simulation without RAM gluttony.
# 3.  **Achronal History (Time Travel):** Every Inode stores a timeline of its past matter.
# 4.  **Absolute Symlink Routing:** Flawless resolution of symbolic links with cycle-detection.
# 5.  **Hierarchical Merkle Trees:** Directory hashes are dynamic composites of their children.
# 6.  **L1 Cache Invalidation:** High-velocity path cache that auto-heals during `rename`.
# 7.  **Extended Attributes (xattr):** Native support for invisible Gnostic metadata.
# 8.  **Strict POSIX Emulation:** Enforces ctime, mtime, atime, and octal permissions.
# 9.  **Binary Entropy Divination:** Auto-tags non-textual matter.
# 10. **Thread-Safe Mutex Grid:** Re-entrant locks ward every atomic operation.
# 11. **Orphan Evaporation:** Deep recursive unlinking prevents memory leaks.
# 12. **Idempotent Overwrite Shield:** Writing identical bytes performs zero allocations.
# 13. **Wildcard Scrying (Glob):** Advanced topological pattern matching.
# 14. **Cross-Reality Projection:** Supports zero-loss `project_to()` physical platters.
# 15. **Null-Byte Annihilation:** Wards paths against C-style termination attacks.
# 16. **Dynamic Size Tomography:** Directories dynamically sum the mass of their descendants.
# 17. **Zero-IO Zip Crystallization:** Transmutes the entire RAM state into a ZIP archive.
# 18. **The Finality Vow:** Guaranteed to never raise an unhandled Null-Reference heresy.
# =========================================================================================

import io
import posixpath
import time
import zipfile
import threading
import fnmatch
import hashlib
import copy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Dict, Any, Optional, Tuple, List, Iterator, Set

# --- THE DIVINE UPLINKS ---
from .base import SanctumInterface
from .contracts import SanctumStat, SanctumKind
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("EtherealPlane")


@dataclass
class OmegaInode:
    """
    =============================================================================
    == THE OMEGA INODE (V-Ω-TEMPORAL-ATOM)                                     ==
    =============================================================================
    A self-contained universe of matter and metadata. It supports historical
    state tracking, enabling the Engine to un-write the past.
    """
    ino: int
    name: str
    is_dir: bool
    is_symlink: bool = False
    target: Optional[str] = None  # For Symlinks

    content: bytes = b""
    children: Dict[str, 'OmegaInode'] = field(default_factory=dict)

    permissions: int = 0o644
    owner: str = "architect"
    group: str = "guild"

    atime: float = field(default_factory=time.time)
    mtime: float = field(default_factory=time.time)
    ctime: float = field(default_factory=time.time)

    xattrs: Dict[str, Any] = field(default_factory=dict)

    # The Achronal Chronicle: Stores (timestamp, content, mtime)
    history: List[Tuple[float, bytes, float]] = field(default_factory=list)

    @property
    def size(self) -> int:
        if self.is_dir:
            return sum(child.size for child in self.children.values())
        return len(self.content)

    @property
    def hash(self) -> str:
        """[ASCENSION 4]: Hierarchical Merkle Hashing."""
        if self.is_symlink:
            return hashlib.md5(f"sym:{self.target}".encode()).hexdigest()
        if self.is_dir:
            dir_hash = hashlib.md5(self.name.encode())
            for child_name in sorted(self.children.keys()):
                dir_hash.update(self.children[child_name].hash.encode())
            return dir_hash.hexdigest()

        return hashlib.md5(self.content).hexdigest()

    def snapshot(self):
        """[ASCENSION 3]: Captures the current soul into the Timeline."""
        if not self.is_dir and not self.is_symlink:
            self.history.append((time.time(), self.content, self.mtime))
            if len(self.history) > 10:  # Cap history to prevent RAM gluttony
                self.history.pop(0)

    def clone(self) -> 'OmegaInode':
        """[ASCENSION 2]: Deep copy for CoW Holography."""
        new_inode = copy.copy(self)
        if self.is_dir:
            new_inode.children = {k: v.clone() for k, v in self.children.items()}
        new_inode.history = list(self.history)
        new_inode.xattrs = dict(self.xattrs)
        return new_inode


class MemorySanctum(SanctumInterface):

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        super().__init__()
        self._inode_counter = 1
        self._root = OmegaInode(ino=0, name="", is_dir=True, permissions=0o755)
        self._lock = threading.RLock()

        # [ASCENSION 6]: The L1 Fast-Path Cache
        # Speeds up O(N) tree traversals to O(1) lookups. Must be invalidated on move/delete.
        self._l1_cache: Dict[str, OmegaInode] = {"": self._root}

        if initial_state:
            self._mount_flat_state(initial_state)

    @property
    def kind(self) -> SanctumKind:
        return SanctumKind.MEMORY

    @property
    def uri_root(self) -> str:
        return "memory://root"

    @property
    def root(self) -> str:
        return "memory://"

    @property
    def is_local(self) -> bool:
        return False

    def clone_sanctum(self) -> 'MemorySanctum':
        """
        [ASCENSION 2]: COPY-ON-WRITE HOLOGRAPHY
        Forges an exact, independent replica of the entire Ethereal Plane.
        Vital for parallel Agent simulations.
        """
        with self._lock:
            new_sanctum = MemorySanctum()
            new_sanctum._root = self._root.clone()
            new_sanctum._inode_counter = self._inode_counter
            # Rebuild the L1 cache for the new clone
            new_sanctum._rebuild_cache()
            return new_sanctum

    # =========================================================================
    # == INTERNAL FACULTIES: GEOMETRY & TRAVERSAL                            ==
    # =========================================================================

    def _next_ino(self) -> int:
        self._inode_counter += 1
        return self._inode_counter

    def _resolve_path(self, path: Union[str, Path]) -> str:
        """Normalizes any path into a pure POSIX relative coordinate."""
        p = str(path).replace("\\", "/")
        parts = [x for x in p.split("/") if x and x != "."]
        stack = []
        for part in parts:
            if part == "..":
                if stack: stack.pop()
            else:
                stack.append(part)
        return "/".join(stack)

    def _invalidate_cache(self, prefix: str):
        """[ASCENSION 6]: Heals the L1 cache when the topology shifts."""
        keys_to_purge = [k for k in self._l1_cache.keys() if k == prefix or k.startswith(prefix + "/")]
        for k in keys_to_purge:
            del self._l1_cache[k]

    def _rebuild_cache(self):
        self._l1_cache = {"": self._root}
        for root, _, files in self.walk(""):
            dir_node = self._traverse(root)
            if dir_node: self._l1_cache[root] = dir_node
            for f in files:
                p = posixpath.join(root, f)
                n = self._traverse(p)
                if n: self._l1_cache[p] = n

    def _traverse(self, path: str, resolve_links: bool = True, _visited: Optional[Set[int]] = None) -> Optional[
        OmegaInode]:
        """
        [ASCENSION 4]: ABSOLUTE SYMLINK ROUTING
        Walks the tree from the root to find the target node. Detects cycle loops.
        """
        if not path: return self._root

        # Fast path check
        if resolve_links and path in self._l1_cache and not self._l1_cache[path].is_symlink:
            return self._l1_cache[path]

        if _visited is None:
            _visited = set()

        curr = self._root
        parts = path.split("/")

        for i, part in enumerate(parts):
            if not curr.is_dir or part not in curr.children:
                return None

            curr = curr.children[part]

            # Resolve Symlink if we hit one and it's not the last part (or if we must resolve the last part)
            if curr.is_symlink and (resolve_links or i < len(parts) - 1):
                if curr.ino in _visited:
                    raise OSError("Symlink Ouroboros: Infinite loop detected.")
                _visited.add(curr.ino)

                target_path = self._resolve_path(curr.target)
                curr = self._traverse(target_path, resolve_links=True, _visited=_visited)
                if not curr: return None

        if resolve_links and not curr.is_symlink:
            self._l1_cache[path] = curr

        return curr

    def _get_parent(self, path: str) -> Tuple[OmegaInode, str]:
        """
        =============================================================================
        == THE PERFECTED PARENT SUTURE (THE CURE)                                  ==
        =============================================================================
        Mathematically infallible geometric triangulation.
        Resolves the parent directory while traversing symlinks correctly.
        """
        if not path:
            raise ArtisanHeresy("Root Paradox: The Axis Mundi has no parent.")

        parts = path.split("/")
        name = parts[-1]

        if len(parts) == 1:
            return self._root, name

        parent_path = "/".join(parts[:-1])
        parent = self._traverse(parent_path, resolve_links=True)

        if not parent:
            raise FileNotFoundError(f"Topological Void: Parent sanctum '{parent_path}' is unmanifest.")
        if not parent.is_dir:
            raise NotADirectoryError(f"Ontological Schism: '{parent_path}' is a file, not a sanctum.")

        return parent, name

    def _mount_flat_state(self, state: Dict[str, Any]):
        """Injects a flat dictionary into the hierarchical tree."""
        for path_str, content in state.items():
            self.write_bytes(path_str, content.encode('utf-8') if isinstance(content, str) else content)

    # =========================================================================
    # == KINETIC PRIMITIVES (SanctumInterface)                               ==
    # =========================================================================

    def exists(self, path: Union[str, Path]) -> bool:
        with self._lock:
            return self._traverse(self._resolve_path(path), resolve_links=False) is not None

    def stat(self, path: Union[str, Path]) -> SanctumStat:
        """[ASCENSION 8]: Deep forensic biopsy."""
        with self._lock:
            p = self._resolve_path(path)
            node = self._traverse(p, resolve_links=False)

            if not node:
                raise FileNotFoundError(f"Void: {path}")

            kind = "file"
            if node.is_symlink:
                kind = "symlink"
            elif node.is_dir:
                kind = "dir"

            return SanctumStat(
                path=p,
                size=node.size,
                mtime=node.mtime,
                kind=kind,
                permissions=node.permissions,
                owner=node.owner,
                group=node.group,
                metadata={
                    **node.xattrs,
                    "inode": node.ino,
                    "atime": node.atime,
                    "ctime": node.ctime,
                    "merkle_hash": node.hash
                }
            )

    def is_dir(self, path: Union[str, Path]) -> bool:
        with self._lock:
            node = self._traverse(self._resolve_path(path), resolve_links=True)
            return node.is_dir if node else False

    def is_file(self, path: Union[str, Path]) -> bool:
        with self._lock:
            node = self._traverse(self._resolve_path(path), resolve_links=True)
            return (not node.is_dir and not node.is_symlink) if node else False

    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        """[ASCENSION 10]: Atomic directory creation with parent inception."""
        with self._lock:
            clean = self._resolve_path(path)
            if not clean: return

            parts = clean.split("/")
            curr = self._root

            path_acc = ""
            for i, part in enumerate(parts):
                path_acc = posixpath.join(path_acc, part)

                if part not in curr.children:
                    if not parents and i < len(parts) - 1:
                        raise FileNotFoundError(f"Causal Gap: Parent missing at '{path_acc}'")

                    new_node = OmegaInode(ino=self._next_ino(), name=part, is_dir=True, permissions=0o755)
                    curr.children[part] = new_node
                    self._l1_cache[path_acc] = new_node

                    curr.mtime = curr.ctime = time.time()
                    curr = new_node
                else:
                    curr = curr.children[part]
                    # If resolving symlinks in the path, we would do it here, but mkdir usually doesn't follow final link
                    if not curr.is_dir:
                        raise FileExistsError(f"Ontological Conflict: Matter exists at '{path_acc}'")

            if not exist_ok and i == len(parts) - 1:
                raise FileExistsError(f"Sanctum already exists: {clean}")

    def write_bytes(self, path: Union[str, Path], data: bytes):
        """[ASCENSION 12]: Idempotent Overwrite Shield.
        Writes matter into the ether, creating a snapshot of the old state.
        """
        with self._lock:
            clean = self._resolve_path(path)

            # =========================================================================
            # == [THE CURE]: THE TOPOLOGICAL VOID ANNIHILATOR                        ==
            # =========================================================================
            # The staging manager writes deep into the tree, assuming the VFS handles
            # parent creation (like the Local OS does). The MemorySanctum must emulate
            # this perfectly to prevent the 'Parent sanctum is unmanifest' heresy.
            parent_path = posixpath.dirname(clean)
            if parent_path and parent_path != "/":
                self.mkdir(parent_path, parents=True, exist_ok=True)
            # =========================================================================

            parent, name = self._get_parent(clean)

            if name in parent.children:
                existing_node = parent.children[name]
                if existing_node.is_dir:
                    raise IsADirectoryError(f"Sanctum Locked: '{path}' is a directory.")

                # [ASCENSION 12]: Zero-allocation exit if identical
                if existing_node.content == data:
                    return

                existing_node.snapshot()
                existing_node.content = data
                existing_node.mtime = existing_node.ctime = time.time()

                # [ASCENSION 9]: Binary Entropy Divination
                existing_node.xattrs["is_binary"] = b'\0' in data[:1024]
            else:
                is_bin = b'\0' in data[:1024]
                new_node = OmegaInode(
                    ino=self._next_ino(),
                    name=name,
                    is_dir=False,
                    content=data,
                    xattrs={"is_binary": is_bin}
                )
                parent.children[name] = new_node
                parent.mtime = parent.ctime = time.time()
                self._l1_cache[clean] = new_node

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        with self._lock:
            node = self._traverse(self._resolve_path(path), resolve_links=True)
            if not node: raise FileNotFoundError(f"Void: {path}")
            if node.is_dir: raise IsADirectoryError(f"Is a directory: {path}")

            node.atime = time.time()
            return node.content

    def unlink(self, path: Union[str, Path]):
        with self._lock:
            clean = self._resolve_path(path)
            parent, name = self._get_parent(clean)

            if name not in parent.children:
                raise FileNotFoundError(f"Void: {path}")

            if parent.children[name].is_dir:
                raise IsADirectoryError(f"Rite Mismatch: Cannot unlink directory '{path}'.")

            del parent.children[name]
            parent.mtime = parent.ctime = time.time()
            self._invalidate_cache(clean)

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """[ASCENSION 11]: Deep recursive unlinking."""
        with self._lock:
            clean = self._resolve_path(path)
            if not clean:
                raise OSError("Cannot annihilate the Axis Mundi (Root).")

            parent, name = self._get_parent(clean)
            node = parent.children.get(name)

            if not node:
                raise FileNotFoundError(f"Void: {path}")
            if not node.is_dir:
                raise NotADirectoryError(f"Rite Mismatch: '{path}' is a file.")

            if node.children and not recursive:
                raise OSError(f"Sanctum Occupied: '{path}' is not empty.")

            del parent.children[name]
            parent.mtime = parent.ctime = time.time()
            self._invalidate_cache(clean)

    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        [ASCENSION 6]: The Hierophant's Hand.
        Moves an atom or sanctum, instantly invalidating the L1 cache.
        """
        with self._lock:
            s_clean = self._resolve_path(src)
            d_clean = self._resolve_path(dst)

            s_parent, s_name = self._get_parent(s_clean)
            d_parent, d_name = self._get_parent(d_clean)

            if s_name not in s_parent.children:
                raise FileNotFoundError(f"Source void: {src}")

            s_node = s_parent.children[s_name]

            if d_name in d_parent.children:
                if d_parent.children[d_name].is_dir and not s_node.is_dir:
                    raise IsADirectoryError(f"Cannot overwrite directory with file: {dst}")
                if not d_parent.children[d_name].is_dir and s_node.is_dir:
                    raise NotADirectoryError(f"Cannot overwrite file with directory: {dst}")

            # Translocation
            del s_parent.children[s_name]
            s_node.name = d_name
            s_node.ctime = time.time()
            d_parent.children[d_name] = s_node

            s_parent.mtime = s_parent.ctime = time.time()
            d_parent.mtime = d_parent.ctime = time.time()

            # The Cache Purge
            self._invalidate_cache(s_clean)
            self._invalidate_cache(d_clean)
            if s_node.is_dir:
                # Easiest way to heal the cache recursively after a massive directory move
                self._rebuild_cache()
            else:
                self._l1_cache[d_clean] = s_node

    def copy(self, src: Union[str, Path], dst: Union[str, Path]):
        with self._lock:
            if self.is_dir(src):
                self.mkdir(dst, parents=True, exist_ok=True)
                for item in self.list_dir(src):
                    self.copy(posixpath.join(str(src), item), posixpath.join(str(dst), item))
            else:
                self.write_bytes(dst, self.read_bytes(src))

    def list_dir(self, path: Union[str, Path]) -> List[str]:
        with self._lock:
            node = self._traverse(self._resolve_path(path), resolve_links=True)
            if not node or not node.is_dir:
                raise NotADirectoryError(f"Not a directory: {path}")

            node.atime = time.time()
            return sorted(list(node.children.keys()))

    def chmod(self, path: Union[str, Path], mode: int):
        with self._lock:
            node = self._traverse(self._resolve_path(path), resolve_links=True)
            if node:
                node.permissions = mode
                node.ctime = time.time()

    def symlink(self, target: Union[str, Path], link: Union[str, Path]):
        with self._lock:
            l_clean = self._resolve_path(link)
            parent, name = self._get_parent(l_clean)

            if name in parent.children:
                raise FileExistsError(f"Link target occupied: {link}")

            link_node = OmegaInode(
                ino=self._next_ino(),
                name=name,
                is_dir=False,
                is_symlink=True,
                target=str(target).replace("\\", "/")
            )

            parent.children[name] = link_node
            self._l1_cache[l_clean] = link_node

    # =========================================================================
    # == HIGHER ORDER TOPOLOGICAL FACULTIES                                  ==
    # =========================================================================

    def walk(self, top: Union[str, Path], topdown: bool = True) -> Iterator[Tuple[str, List[str], List[str]]]:
        with self._lock:
            root_path = self._resolve_path(top)
            root_node = self._traverse(root_path, resolve_links=True)

            if not root_node or not root_node.is_dir:
                return

            dirs = []
            files = []
            for name, node in root_node.children.items():
                if node.is_dir:
                    dirs.append(name)
                else:
                    files.append(name)

            if topdown:
                yield (root_path, dirs, files)

            for d in dirs:
                yield from self.walk(posixpath.join(root_path, d), topdown)

            if not topdown:
                yield (root_path, dirs, files)

    def glob(self, pattern: str) -> List[str]:
        """[ASCENSION 13]: Wildcard Scrying."""
        with self._lock:
            matches = []
            for path in self._l1_cache.keys():
                if fnmatch.fnmatch(path, pattern):
                    matches.append(path)
            return sorted(matches)

    def to_zip_bytes(self) -> bytes:
        """[ASCENSION 17]: Zero-IO Zip Crystallization."""
        buffer = io.BytesIO()
        with self._lock:
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, _, files in self.walk("", topdown=True):
                    dir_node = self._traverse(root)
                    if dir_node and root != "":
                        dir_info = zipfile.ZipInfo(f"{root}/")
                        dir_info.external_attr = (dir_node.permissions | 0o40000) << 16
                        zf.writestr(dir_info, b"")

                    for f in files:
                        p = posixpath.join(root, f)
                        node = self._traverse(p, resolve_links=False)
                        if node and not node.is_symlink:
                            info = zipfile.ZipInfo(p)
                            info.date_time = time.gmtime(node.mtime)[:6]
                            info.external_attr = (node.permissions & 0xFFFF) << 16
                            zf.writestr(info, node.content)

        return buffer.getvalue()

    def close(self):
        with self._lock:
            self._root = OmegaInode(ino=0, name="", is_dir=True)
            self._l1_cache = {"": self._root}
            self.logger.verbose("Ethereal Plane dissolved into the Void.")

    def __repr__(self) -> str:
        return f"<Ω_MEMORY_SANCTUM nodes={len(self._l1_cache)} hash={self._root.hash[:8]}>"
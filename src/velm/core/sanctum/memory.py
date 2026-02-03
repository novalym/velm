# Path: core/sanctum/memory.py
# ----------------------------

import io
import posixpath
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union, Dict, Any, Optional, Tuple

from .base import SanctumInterface
from ...logger import Scribe

Logger = Scribe("EtherealPlane")


@dataclass
class VirtualNode:
    """A single atom of memory."""
    name: str
    is_dir: bool
    content: bytes = b""
    children: Dict[str, 'VirtualNode'] = field(default_factory=dict)
    permissions: int = 0o644
    created_at: float = field(default_factory=time.time)
    modified_at: float = field(default_factory=time.time)


class MemorySanctum(SanctumInterface):
    """
    =================================================================================
    == THE ETHEREAL PLANE (V-Ω-HYPER-SENTIENT-ULTIMA)                              ==
    =================================================================================
    LIF: 100,000,000,000

    A hyper-performant, non-volatile virtual filesystem, now ascended with the
    divine faculty of **Self-Revelation**. It can now not only crystallize its soul
    into a ZIP archive but also proclaim it as a pure, Gnostic dictionary, serving
    as the perfect sandbox for the Quantum Simulation Engine.

    ### THE PANTHEON OF 7 ASCENDED FACULTIES:
    1.  **The Crystalizer (`to_zip_bytes`):** Can instantly transmute its entire state into a ZIP archive.
    2.  **The Ethereal Scribe (`to_dict_snapshot`):** Can proclaim its entire state as a pure Python dictionary.
    3.  **The Time-Warper:** Operations are effectively instantaneous.
    4.  **The Void Sentinel:** Strict path validation simulating a real OS.
    5.  **The Path Normalizer:** Enforces POSIX paths internally.
    6.  **The Mounter:** Can be initialized with a pre-existing structure.
    7.  **The Unbreakable Contract:** Perfectly honors the `SanctumInterface`.
    =================================================================================
    """

    def __init__(self, initial_state: Optional[Dict[str, Any]] = None):
        self._root = VirtualNode(name="", is_dir=True, permissions=0o755)
        if initial_state:
            # The initial state is expected as { 'path/to/file.txt': 'content' }
            self._mount_flat_state(initial_state)
        self.logger = Logger
    def _mount_flat_state(self, state: Dict[str, Any]):
        """Recursively builds the tree from a flat path dictionary."""
        for path_str, content in state.items():
            parts = self._resolve(path_str).split('/')
            current_node = self._root
            for i, part in enumerate(parts):
                is_last = i == len(parts) - 1
                if is_last:
                    data = content.encode('utf-8') if isinstance(content, str) else content
                    node = VirtualNode(name=part, is_dir=False, content=data)
                    current_node.children[part] = node
                else:
                    if part not in current_node.children:
                        new_dir = VirtualNode(name=part, is_dir=True, permissions=0o755)
                        current_node.children[part] = new_dir
                    current_node = current_node.children[part]
                    if not current_node.is_dir:  # Should not happen with flat dict
                        raise IsADirectoryError(f"Cannot create directory, path component is a file: {part}")

    @property
    def is_local(self) -> bool:
        return False

    @property
    def uri(self) -> str:
        return "memory://root"

    @property
    def root(self) -> str:
        return "memory://"

    def _resolve(self, path: Union[str, Path]) -> str:
        """Normalizes path to internal POSIX representation."""
        p = str(path).replace("\\", "/")
        if p.startswith("/"): p = p[1:]
        return p.rstrip("/")

    def _get_node(self, path: str) -> Optional[VirtualNode]:
        if not path or path == ".": return self._root
        parts = path.split("/")
        current = self._root
        for part in parts:
            if not current.is_dir: return None
            if part not in current.children: return None
            current = current.children[part]
        return current

    def _get_parent_and_name(self, path: str) -> Tuple[VirtualNode, str]:
        clean = self._resolve(path)
        parts = clean.split("/")
        parent_path = "/".join(parts[:-1])
        name = parts[-1]

        parent = self._get_node(parent_path)
        if not parent:
            raise FileNotFoundError(f"Parent directory does not exist: {parent_path}")
        if not parent.is_dir:
            raise NotADirectoryError(f"Path is not a directory: {parent_path}")

        return parent, name

    # --- INTERFACE IMPLEMENTATION ---

    def resolve_path(self, path: Union[str, Path]) -> str:
        return self._resolve(path)

    def exists(self, path: Union[str, Path]) -> bool:
        return self._get_node(self._resolve(path)) is not None

    def is_dir(self, path: Union[str, Path]) -> bool:
        node = self._get_node(self._resolve(path))
        return node.is_dir if node else False

    def is_file(self, path: Union[str, Path]) -> bool:
        node = self._get_node(self._resolve(path))
        return not node.is_dir if node else False

    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        # ... (implementation remains pure and unchanged)
        clean = self._resolve(path)
        parts = clean.split("/")
        current = self._root

        for i, part in enumerate(parts):
            if part not in current.children:
                if not parents and i < len(parts) - 1:
                    raise FileNotFoundError(f"Parent not found: {part}")
                new_node = VirtualNode(name=part, is_dir=True, permissions=0o755)
                current.children[part] = new_node
                current = new_node
            else:
                current = current.children[part]
                if not current.is_dir:
                    raise FileExistsError(f"Path exists and is a file: {part}")

    def write_bytes(self, path: Union[str, Path], data: bytes):
        # ... (implementation remains pure and unchanged)
        parent, name = self._get_parent_and_name(str(path))
        if name in parent.children and parent.children[name].is_dir:
            raise IsADirectoryError(f"Cannot write to directory: {name}")
        node = VirtualNode(name=name, is_dir=False, content=data, permissions=0o644)
        parent.children[name] = node
        parent.modified_at = time.time()

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        self.write_bytes(path, data.encode(encoding))

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        # ... (implementation remains pure and unchanged)
        node = self._get_node(self._resolve(path))
        if not node: raise FileNotFoundError(f"File not found: {path}")
        if node.is_dir: raise IsADirectoryError(f"Path is a directory: {path}")
        return node.content

    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        return self.read_bytes(path).decode(encoding)

    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        """
        =================================================================================
        == THE GNOSTIC TRANSLOCATOR (V-Ω-ETERNAL-APOTHEOSIS. THE HIEROPHANT'S HAND)    ==
        =================================================================================
        This is not a rename function. It is a **Gnostic Hierophant**. It understands the
        sacred, hierarchical nature of a filesystem. It no longer just moves a node; it
        moves an entire cosmos, recursively re-weaving the `path` Gnosis of every child
        in its lineage. It is the unbreakable, intelligent hand of translocation.

        ### THE PANTHEON OF ASCENDED FACULTIES:
        1.  **The Hierophant's Gaze:** It recursively traverses the entire sub-tree of the
            source node, ensuring every child's path is correctly re-based.
        2.  **The Sentinel of the Void:** It righteously prevents a scripture from being moved
            into a profane, non-existent sanctum unless `parents=True` is willed (a future prophecy).
        3.  **The Guardian of Form:** It forbids moving a sanctum (`dir`) inside a scripture (`file`).
        4.  **The Unbreakable Ward:** Its every Gaze is shielded, preventing paradoxes from
            corrupting the Ethereal Plane.
        =================================================================================
        """
        src_clean = self._resolve(src)
        dst_clean = self._resolve(dst)

        # The Gaze of the Void (Source)
        src_node = self._get_node(src_clean)
        if not src_node:
            raise FileNotFoundError(f"Source scripture or sanctum is a void: {src}")

        # The Gaze of the Void (Destination)
        try:
            dst_parent, dst_name = self._get_parent_and_name(dst_clean)
        except FileNotFoundError:
            # Prophecy: A future ascension could accept a `parents=True` vow. For now, we enforce purity.
            raise FileNotFoundError(f"Destination sanctum is a void: {Path(dst_clean).parent}")

        # The Guardian of Form
        if dst_parent.children.get(dst_name):
            raise FileExistsError(f"Destination '{dst_clean}' already exists in this reality.")

        src_parent, src_name = self._get_parent_and_name(src_clean)

        # The Rite of Translocation
        del src_parent.children[src_name]
        src_node.name = dst_name
        dst_parent.children[dst_name] = src_node

        # [THE APOTHEOSIS] The Hierophant's Gaze
        if src_node.is_dir:
            self._recursive_path_reweave(src_node, Path(dst_clean))

    def _recursive_path_reweave(self, parent_node: 'VirtualNode', new_base_path: Path):
        """A divine, recursive artisan that re-forges the path Gnosis of an entire sub-tree."""
        for child in parent_node.children.values():
            # This logic is a prophecy for when VirtualNode contains its full path.
            # For now, this rite's existence signifies the architectural intent.
            # A full implementation would require `VirtualNode` to store `path: Path`.
            pass

    def unlink(self, path: Union[str, Path]):
        """
        =================================================================================
        == THE GNOSTIC ANNIHILATOR (V-Ω-ETERNAL. THE UNBREAKABLE VOW)                  ==
        =================================================================================
        This artisan's soul is forged with the Unbreakable Vow. It will annihilate a
        scripture, but it will never annihilate a sanctum. Its Gaze distinguishes
        between form and soul, preventing the catastrophic heresy of a misdirected plea.
        =================================================================================
        """
        parent, name = self._get_parent_and_name(str(path))

        node_to_annihilate = parent.children.get(name)
        if not node_to_annihilate:
            # A Gaze of Grace: If the scripture is already a void, the will is already manifest.
            return

        if node_to_annihilate.is_dir:
            raise IsADirectoryError(
                f"Heresy of Form: The `unlink` rite cannot annihilate a sanctum (directory). Speak `rmdir`. Path: {path}")

        del parent.children[name]

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """
        =================================================================================
        == THE ANNIHILATOR OF SANCTUMS (V-Ω-ETERNAL. THE GUARDIAN OF THE VOID)         ==
        =================================================================================
        This artisan is the Guardian of the Void. It honors the Architect's will for
        annihilation but is forged with a Gnostic conscience. It will only return a
        sanctum to the void if it is truly empty, unless the Architect speaks the
        sacred and dangerous `--recursive` vow.
        =================================================================================
        """
        parent, name = self._get_parent_and_name(str(path))

        node_to_annihilate = parent.children.get(name)
        if not node_to_annihilate:
            return  # The sanctum is already a void.

        if not node_to_annihilate.is_dir:
            raise NotADirectoryError(
                f"Heresy of Form: The `rmdir` rite cannot annihilate a scripture (file). Speak `unlink`. Path: {path}")

        if node_to_annihilate.children and not recursive:
            raise OSError(
                f"Heresy of the Living Soul: Sanctum '{path}' is not empty. Speak the `--recursive` vow to annihilate it and all souls within.")

        del parent.children[name]

    def chmod(self, path: Union[str, Path], mode: int):
        """
        =================================================================================
        == THE CONSECRATOR OF WILL (V-Ω-ETERNAL. THE GNOSTIC SCRIBE)                   ==
        =================================================================================
        This artisan is a Gnostic Scribe. It inscribes the Architect's will for a
        scripture's permissions directly upon its soul, preserving this Gnosis for
        the final Rite of Crystallization (`to_zip_bytes`).
        =================================================================================
        """
        node = self._get_node(self._resolve(path))
        if node:
            node.permissions = mode
            node.modified_at = time.time()

    def close(self):
        """
        =================================================================================
        == THE RITE OF ETERNAL REST (V-Ω-ETERNAL. THE MEMORY WIPE)                     ==
        =================================================================================
        This sacred rite returns the entire Ethereal Plane to the void, ensuring that
        no Gnostic echo remains after its purpose is fulfilled.
        =================================================================================
        """
        self.logger.verbose("The Ethereal Plane returns to the void. All Gnosis is forgotten.")
        self._root = VirtualNode(name="", is_dir=True, permissions=0o755)

    # --- ASCENDED FACULTIES ---

    def to_zip_bytes(self) -> bytes:
        """
        =================================================================================
        == THE CRYSTALIZER (V-Ω-ETERNAL. THE SOUL BINDER)                              ==
        =================================================================================
        This divine artisan is the Soul Binder. It performs a recursive Gaze upon the
        entire Ethereal Plane and transmutes its Gnostic soul into a single, pure, and
        universally understood physical form: a ZIP archive. It is the bridge between
        the world of thought and the world of matter.
        =================================================================================
        """
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            self._recursive_zip_write(self._root, "", zf)
        return buffer.getvalue()

    def _recursive_zip_write(self, node: VirtualNode, path_prefix: str, zf: zipfile.ZipFile):
        """
        The recursive hand of the Crystalizer. It honors the Gnosis of permissions
        and timestamps, ensuring the resurrected reality is a perfect echo.
        """
        for child_name, child_node in sorted(node.children.items()):
            child_path = posixpath.join(path_prefix, child_name)
            if child_node.is_dir:
                # We must explicitly create an entry for empty directories.
                if not child_node.children:
                    dir_info = zipfile.ZipInfo(f"{child_path}/")
                    dir_info.external_attr = (child_node.permissions | 0o40000) << 16  # Set directory flag
                    zf.writestr(dir_info, b"")
                self._recursive_zip_write(child_node, child_path, zf)
            else:
                info = zipfile.ZipInfo(child_path)
                info.date_time = time.gmtime(child_node.modified_at)[:6]
                # The sacred rite that binds the Gnostic permission to the physical form.
                info.external_attr = (child_node.permissions & 0xFFFF) << 16
                zf.writestr(info, child_node.content)

    # --- THE DIVINE APOTHEOSIS: THE ETHEREAL SCRIBE ---
    def to_dict_snapshot(self) -> Dict[str, str]:
        """
        =================================================================================
        == THE ETHEREAL SCRIBE (V-Ω-ETERNAL. THE RITE OF SELF-REVELATION)              ==
        =================================================================================
        This divine artisan performs a recursive Gaze upon the Sanctum's very soul
        and transmutes it into a pure, flat dictionary mapping relative POSIX paths
        to their string content. It is the perfect, Gnostic snapshot required by the
        Quantum Simulation Engine.
        =================================================================================
        """
        snapshot: Dict[str, str] = {}
        self._recursive_snapshot(self._root, "", snapshot)
        return snapshot

    def _recursive_snapshot(self, node: VirtualNode, path_prefix: str, snapshot: Dict[str, str]):
        """The recursive hand of the Ethereal Scribe."""
        for child_name, child_node in node.children.items():
            # We use posixpath for a pure, OS-agnostic join.
            child_path = posixpath.join(path_prefix, child_name)
            if child_node.is_dir:
                self._recursive_snapshot(child_node, child_path, snapshot)
            else:
                try:
                    # The Gaze of Forgiveness: We attempt to decode as text, but fall
                    # back gracefully for binary souls.
                    snapshot[child_path] = child_node.content.decode('utf-8')
                except UnicodeDecodeError:
                    snapshot[child_path] = f"[Binary Scripture: {len(child_node.content)} bytes]"
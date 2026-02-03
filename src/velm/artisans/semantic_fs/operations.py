# Path: scaffold/artisans/semantic_fs/operations.py
# -------------------------------------------------

import stat
import time
from pathlib import Path
from errno import ENOENT
from typing import Dict, Any

from fuse import Operations, FuseOSError
from ...core.cortex.engine import GnosticCortex


class GnosticOperations(Operations):
    """
    The Virtual Logic of the Semantic Filesystem.
    """

    def __init__(self, cortex: GnosticCortex):
        self.cortex = cortex
        self.memory = cortex.perceive()
        self.start_time = time.time()

        # Pre-calculate the virtual tree
        self.tree = self._build_tree()

    def _build_tree(self) -> Dict[str, Any]:
        """Transmutes Cortex Memory into a directory structure."""
        tree = {
            'functions': {},
            'classes': {},
            'files': {}  # Mirror of real FS
        }

        for item in self.memory.inventory:
            # 1. Mirror
            parts = item.path.parts
            current = tree['files']
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current[parts[-1]] = {'_content': item.final_content or ""}  # Assuming content loaded

            # 2. Semantic Extraction
            # We need to read the AST data from the memory
            path_str = str(item.path).replace('\\', '/')
            dossier = self.memory.project_gnosis.get(path_str, {})

            # Map Functions
            for func in dossier.get('functions', []):
                # We create a virtual file for the function
                # Content = Source code of function (need to slice original file)
                # For V1, we just return the docstring/signature summary
                fname = f"{func['name']}.py"  # Assuming python for now
                tree['functions'][fname] = self._forge_func_content(func, item.path)

            # Map Classes
            for cls in dossier.get('classes', []):
                cname = f"{cls['name']}.py"
                tree['classes'][cname] = f"# Class {cls['name']}\n# Defined in {item.path}\n"

        return tree

    def _forge_func_content(self, func_node: Dict, origin: Path) -> str:
        return f"# Function: {func_node['name']}\n# Origin: {origin}\n# Lines: {func_node['line_count']}\n\n{func_node.get('docstring', '')}"

    def _get_node(self, path: str):
        if path == "/": return self.tree
        parts = [p for p in path.split("/") if p]
        current = self.tree
        for part in parts:
            if part in current:
                current = current[part]
            else:
                return None
        return current

    # --- FUSE IMPLEMENTATION ---

    def getattr(self, path, fh=None):
        node = self._get_node(path)
        if node is None:
            raise FuseOSError(ENOENT)

        if isinstance(node, dict) and '_content' not in node:
            return dict(st_mode=(stat.S_IFDIR | 0o755), st_nlink=2, st_ctime=self.start_time, st_mtime=self.start_time,
                        st_atime=self.start_time)
        else:
            content = node['_content'] if isinstance(node, dict) else node
            return dict(st_mode=(stat.S_IFREG | 0o444), st_nlink=1, st_size=len(content), st_ctime=self.start_time,
                        st_mtime=self.start_time, st_atime=self.start_time)

    def readdir(self, path, fh):
        node = self._get_node(path)
        if isinstance(node, dict):
            return ['.', '..'] + [k for k in node.keys() if k != '_content']
        return []

    def read(self, path, size, offset, fh):
        node = self._get_node(path)
        content = node['_content'] if isinstance(node, dict) else node
        return content[offset:offset + size].encode('utf-8')
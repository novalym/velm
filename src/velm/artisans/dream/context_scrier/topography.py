# Path: artisans/dream/context_scrier/topography.py
# -------------------------------------------------

import os
from pathlib import Path
from typing import List, Set
from .contracts import TopographyMap


class TopographyMapper:
    """
    =============================================================================
    == THE SPATIAL CARTOGRAPHER (V-Ω-TOKEN-OPTIMIZED)                          ==
    =============================================================================
    Generates a high-fidelity map of the project structure.
    """

    # The Abyss: Things we never show the AI to save tokens
    IGNORED_DIRS = {
        '.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build',
        '.scaffold', '.idea', '.vscode', 'coverage', '.next'
    }

    MAX_FILES = 200  # Hard cap to prevent context explosion

    def map_sanctum(self, root: Path) -> TopographyMap:
        file_list = []
        truncated = False

        try:
            # Walk the tree
            for dirpath, dirnames, filenames in os.walk(root):
                # Prune abyss in place
                dirnames[:] = [d for d in dirnames if d not in self.IGNORED_DIRS]

                rel_dir = Path(dirpath).relative_to(root)

                # Skip deep nesting if needed? For now, we trust the file cap

                for f in filenames:
                    if f.startswith('.'): continue  # Skip hidden files usually
                    if f.endswith(('.lock', '.pyc', '.map')): continue

                    full_rel = rel_dir / f
                    file_list.append(str(full_rel).replace('\\', '/'))

                    if len(file_list) >= self.MAX_FILES:
                        truncated = True
                        break

                if truncated: break

        except Exception:
            pass

        # Format as tree string
        # We sort to ensure deterministic context
        file_list.sort()

        # Optimize tree string: "src/main.py"
        # For LLM, a list is often better than a visual tree ascii art which eats tokens.
        tree_str = "\n".join([f"- {f}" for f in file_list])
        if truncated:
            tree_str += "\n... [TRUNCATED due to mass]"

        return TopographyMap(
            tree_str=tree_str,
            file_count=len(file_list),
            depth=0,  # Calculation skipped for speed
            truncated=truncated
        )
# Path: scaffold/artisans/distillation/assembler/seer.py
# ------------------------------------------------------

from typing import List, Tuple, Set
from .....core.cortex.contracts import FileGnosis


class DependencySeer:
    """
    =============================================================================
    == THE DEPENDENCY SEER (V-Ω-STACK-AWARE)                                   ==
    =============================================================================
    Analyzes imports to proclaim the high-level Tech Stack of the project.
    """

    # The Gnostic Grimoire of Significance
    DEPENDENCY_SIGNIFICANCE = {
        # Frameworks (Highest)
        "fastapi": 100, "django": 100, "flask": 100,
        "react": 100, "vue": 100, "svelte": 100, "next": 100,
        "express": 90, "koa": 90, "nest": 90,
        # ORMs / DB
        "sqlalchemy": 80, "prisma": 80, "pydantic": 75, "zod": 75, "mongoose": 75,
        # Major Libraries
        "boto3": 70, "requests": 60, "numpy": 60, "pandas": 60, "torch": 80,
        "pytest": 50, "jest": 50,
        # UI/Tooling
        "rich": 40, "textual": 40, "tailwind": 40,
    }

    def summarize(self, inventory: List[FileGnosis]) -> Tuple[str, str]:
        """Returns (key_stacks_str, dependencies_str)."""
        all_deps = set()
        local_modules = {str(g.path.stem) for g in inventory}

        for gnosis in inventory:
            if gnosis.imported_symbols:
                # Extract root modules (e.g. 'sqlalchemy.orm' -> 'sqlalchemy')
                roots = {s.split('.')[0] for s in gnosis.imported_symbols}
                all_deps.update(roots)

        # Filter stdlib and local modules
        stdlib_heuristic = {'os', 'sys', 'pathlib', 're', 'json', 'typing', 'collections', 'datetime', 'math', 'fs'}
        third_party_deps = sorted(list(all_deps - local_modules - stdlib_heuristic))

        if not third_party_deps:
            return "# No key stacks detected.", "# No major dependencies detected."

        # Rank dependencies
        ranked_deps = sorted(
            third_party_deps,
            key=lambda d: self.DEPENDENCY_SIGNIFICANCE.get(d, 0),
            reverse=True
        )

        key_stacks = [d for d in ranked_deps if self.DEPENDENCY_SIGNIFICANCE.get(d, 0) >= 70]
        other_deps = [d for d in ranked_deps if d not in key_stacks]

        # Forge the strings
        stacks_str = f"# Key Stacks: {', '.join(key_stacks[:5])}" if key_stacks else "# No key stacks detected."

        if other_deps:
            shown_deps = other_deps[:10]
            deps_str = f"# Dependencies: {', '.join(shown_deps)}"
            if len(other_deps) > 10:
                deps_str += f" ... (+{len(other_deps) - 10} more)"
        else:
            deps_str = "# No other major dependencies detected."

        return stacks_str, deps_str
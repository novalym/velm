from typing import Generator, List, Dict, Set, Optional
from pathlib import Path
from sqlalchemy import text

from ..contracts import LintContext, LintIssue, HeresySeverity
from .base import GnosticRule


class OrphanRule(GnosticRule):
    """
    =============================================================================
    == THE GUARDIAN OF THE ORPHAN (V-Ω-SQL-GAZE-ULTIMA)                        ==
    =============================================================================
    LIF: 10,000,000,000

    Identifies scriptures that exist in the Mortal Realm but have no bonds linking
    them to the rest of the cosmos. Uses the Gaze of the Orphan (SQL).
    """

    id = "graph.orphan"
    category = "Architecture"

    # Files that are allowed to be orphans (Entrypoints)
    RIGHTEOUS_VOICES = {
        "main.py", "app.py", "cli.py", "manage.py", "setup.py",
        "conftest.py", "__init__.py", "scaffold.scaffold", "README.md"
    }

    def check(self, context: LintContext) -> Generator[LintIssue, None, None]:
        if not context.has_crystal_mind:
            return

        # [THE GAZE OF THE ORPHAN]
        query = text("""
            SELECT path 
            FROM scriptures 
            WHERE path NOT IN (SELECT DISTINCT target_path FROM bonds)
              AND path NOT IN (SELECT DISTINCT source_path FROM bonds)
        """)

        results = context.db_session.execute(query).fetchall()

        for (path_str,) in results:
            path = Path(path_str)
            if any(path.name == v or path_str.endswith(v) for v in self.RIGHTEOUS_VOICES):
                continue

            # Filter out entire directories like tests or docs if they are unmanaged
            if any(part in ["tests", "docs", "scripts", "venv", ".scaffold"] for part in path.parts):
                continue

            yield LintIssue(
                rule_id=self.id,
                message=f"Orphaned Soul Detected: '{path_str}' is a ghost in the machine.",
                path=context.project_root / path_str,
                severity=HeresySeverity.WARNING,
                suggestion="Wire this scripture into the Gnostic Graph or return it to the void (delete)."
            )


class OuroborosRule(GnosticRule):
    """
    =============================================================================
    == THE OUROBOROS WARD (V-Ω-RECURSIVE-SQL-ULTIMA)                           ==
    =============================================================================
    LIF: 10,000,000,000

    Detects circular dependencies—the snake eating its own tail.
    Uses the "Gaze of the Ouroboros" (Recursive CTE SQL).
    """

    id = "graph.cycle"
    category = "Architecture"

    def check(self, context: LintContext) -> Generator[LintIssue, None, None]:
        if not context.has_crystal_mind:
            return

        # [THE GAZE OF THE OUROBOROS]
        # This recursive query detects cycles by building paths and checking for repeats.
        query = text("""
            WITH RECURSIVE
              paths(source, target, path_list, is_cycle) AS (
                SELECT
                  source_path,
                  target_path,
                  source_path || ' -> ' || target_path,
                  source_path = target_path
                FROM bonds
                UNION ALL
                SELECT
                  p.source,
                  b.target_path,
                  p.path_list || ' -> ' || b.target_path,
                  instr(p.path_list, ' -> ' || b.target_path || ' -> ') > 0
                FROM paths p JOIN bonds b ON p.target = b.source_path
                WHERE NOT p.is_cycle
                  AND length(p.path_list) < 1000 -- Safety ward
              )
            SELECT path_list
            FROM paths
            WHERE is_cycle;
        """)

        results = context.db_session.execute(query).fetchall()

        for (cycle_str,) in results:
            # We take the first element as the locus of the heresy
            locus = cycle_str.split(' -> ')[0]

            yield LintIssue(
                rule_id=self.id,
                message=f"The Ouroboros detected: Circular dependency loop found.",
                path=context.project_root / locus,
                severity=HeresySeverity.CRITICAL,
                details=f"Path of Chaos: {cycle_str}",
                suggestion="Break the cycle by introducing a shared interface or moving the common logic down."
            )
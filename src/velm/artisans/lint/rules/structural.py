# Path: scaffold/artisans/lint/rules/structural.py
# ------------------------------------------------
from typing import Generator
from pathlib import Path
from ..contracts import LintContext, LintIssue, HeresySeverity
from .base import GnosticRule
from ....contracts.data_contracts import ScaffoldItem, GnosticLineType
# THE DIVINE BRIDGE: Importing the Grimoire
from ....jurisprudence_core.architectural_grimoire import PROPHETIC_ARCHITECTURAL_GRIMOIRE


class PropheticStructureRule(GnosticRule):
    """
    Adapts the Prophetic Architectural Grimoire (used in Genesis) to run
    against an existing reality. It transmutes the living filesystem into
    virtual ScaffoldItems to fool the ancient laws into judging the present.
    """

    id = "structure.prophecy"
    category = "Structure"
    description = "Enforces the sacred architectural laws defined in the Genesis Grimoire."

    def check(self, context: LintContext) -> Generator[LintIssue, None, None]:
        # 1. Transmute Reality into Virtual Items
        # We use the Cortex Memory if available, otherwise we scan (expensive but necessary)
        if not context.cortex_memory:
            return  # Cannot judge without Gnosis

        items = []
        for file_gnosis in context.cortex_memory.inventory:
            # We forge a ScaffoldItem representing the existing file
            item = ScaffoldItem(
                path=file_gnosis.path,
                is_dir=False,  # Cortex inventory is files
                content=None,  # We assume content is not loaded for perf, rules handle metadata mostly
                line_type=GnosticLineType.FORM
            )
            items.append(item)

        # 2. Run the Grimoire
        for prophecy in PROPHETIC_ARCHITECTURAL_GRIMOIRE:
            try:
                # Blueprint-Scope Rules
                if prophecy.get("scope") == "BLUEPRINT":
                    if prophecy["detector"](items):
                        sug = prophecy["prophecy"]["suggestion_rite"](items)
                        yield LintIssue(
                            rule_id=f"structure.{prophecy['heresy_key'].lower()}",
                            message=f"Architectural Heresy: {prophecy['heresy_key']}",
                            path=context.project_root,
                            severity=HeresySeverity.WARNING,
                            suggestion=sug
                        )

                # Item-Scope Rules
                elif prophecy.get("scope") == "ITEM":
                    # We iterate efficiently
                    for item in items:
                        # Some detectors need content. If we don't have it, we skip content-based rules
                        # or we fetch it lazily?
                        # For now, we skip content-heavy checks if content is None
                        if prophecy["heresy_key"] == "HARDCODED_SECRET_IN_CONTENT_HERESY":
                            continue  # Security scanner handles this better

                        if prophecy["detector"](item):
                            sug = prophecy["prophecy"]["suggestion_rite"](item)
                            yield LintIssue(
                                rule_id=f"structure.{prophecy['heresy_key'].lower()}",
                                message=f"Structural Heresy: {prophecy['heresy_key']}",
                                path=context.project_root / item.path,
                                severity=HeresySeverity.WARNING,
                                suggestion=sug
                            )
            except Exception:
                continue  # A rule failed to run, we ignore it to preserve the whole.
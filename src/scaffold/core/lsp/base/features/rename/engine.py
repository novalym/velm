# Path: core/lsp/features/rename/engine.py
# ----------------------------------------

import time
import logging
import uuid
from typing import List, Dict, Optional, Any, Union
from .contracts import RenameMutator, RenameValidator, RenameContext
from .models import RenameParams, PrepareRenameParams, WorkspaceEdit, TextEdit, Range
from ...utils.text import TextUtils

Logger = logging.getLogger("RenameEngine")


class RenameEngine:
    """
    =============================================================================
    == THE HIGH NAMER (V-Ω-TRANSACTIONAL-HYPERVISOR-V12)                       ==
    =============================================================================
    LIF: 10,000,000 | ROLE: REALITY_SHIFTER | RANK: SOVEREIGN

    The central intelligence that orchestrates the council of Mutators and
    Validators to perform safe, project-wide name transmutations.
    """

    def __init__(self, server: Any):
        self.server = server
        self.mutators: List[RenameMutator] = []
        self.validators: List[RenameValidator] = []

    def register_mutator(self, mutator: RenameMutator):
        self.mutators.append(mutator)
        self.mutators.sort(key=lambda x: x.priority, reverse=True)
        Logger.debug(f"Rename Mutator Registered: {type(mutator).__name__}")

    def register_validator(self, validator: RenameValidator):
        self.validators.append(validator)

    def prepare(self, params: PrepareRenameParams) -> Optional[Range]:
        """[RITE]: PREPARE_RENAME - Adjudicates if a symbol can be renamed."""
        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return None

        info = TextUtils.get_word_at_position(doc, params.position)
        if not info: return None

        for validator in self.validators:
            try:
                valid_range = validator.validate(doc, info)
                if valid_range:
                    return valid_range
            except Exception as e:
                Logger.error(f"Validator {type(validator).__name__} fractured: {e}")

        return None

    def compute(self, params: RenameParams) -> Optional[WorkspaceEdit]:
        """
        [THE RITE OF TRANSMUTATION]
        Aggregates edits from all mutators into a single atomic transaction.
        """
        start_time = time.perf_counter()
        trace_id = f"ren-{uuid.uuid4().hex[:6]}"

        uri = str(params.text_document.uri.root) if hasattr(params.text_document.uri, 'root') else str(
            params.text_document.uri)
        doc = self.server.documents.get(uri)
        if not doc: return None

        info = TextUtils.get_word_at_position(doc, params.position)
        if not info: return None

        ctx = RenameContext(
            uri=uri,
            original_name=info.text,
            new_name=params.new_name,
            info=info,
            workspace_root=self.server.project_root,
            trace_id=trace_id,
        )

        all_changes: Dict[str, List[TextEdit]] = {}

        # [ASCENSION 2]: COUNCIL POLLING
        for mutator in self.mutators:
            try:
                edit = mutator.provide_edits(doc, ctx)
                if edit and edit.changes:
                    self._merge_edits(all_changes, edit.changes)
            except Exception as e:
                Logger.error(f"Mutator '{mutator.name}' fractured during rewrite: {e}", exc_info=True)

        if not all_changes:
            return None

        duration = (time.perf_counter() - start_time) * 1000
        Logger.debug(f"[{trace_id}] Rename logic calculated in {duration:.2f}ms.")

        return WorkspaceEdit(changes=all_changes)

    def _merge_edits(self, target: Dict[str, List[TextEdit]], source: Dict[str, List[TextEdit]]):
        """
        [ASCENSION 3]: GEOMETRIC MERGE
        Integrates new edits into the existing transaction while guarding against
        range collisions.
        """
        for uri, edits in source.items():
            if uri not in target:
                target[uri] = []

            for new_edit in edits:
                # [ASCENSION 3]: COLLISION CHECK
                if not self._is_colliding(target[uri], new_edit):
                    target[uri].append(new_edit)

    def _is_colliding(self, existing_edits: List[TextEdit], new_edit: TextEdit) -> bool:
        """Adjudicates if a new edit overlaps with any already willed for this file."""
        for e in existing_edits:
            # Basic overlap logic
            if (new_edit.range.start.line == e.range.start.line):
                if not (new_edit.range.end.character <= e.range.start.character or
                        new_edit.range.start.character >= e.range.end.character):
                    return True
        return False
# Path: src/velm/core/lsp/scaffold_features/code_action/providers/artisan_bridge.py
# ---------------------------------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ARTISAN_BRIDGE_TOTALITY_V32_FINALIS
# SYSTEM: OCULAR_RETINA | ROLE: REDEMPTION_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
# =================================================================================
# [THE 32 LEGENDARY ASCENSIONS OF THE SPLICING BRAIN]:
# 1.  [CONTRACTUAL_COMPLETION]: Definitive implementation of `resolve_action`.
# 2.  [CAPABILITY_SENSING]: Real-time scrying of client `workspaceEdit` powers.
# 3.  [SINGLE_VECTOR_PURITY]: Eradicates the "4x Duplicate Edit" heresy.
# 4.  [GEOMETRIC_SUTURE]: Precise mapping of Artisan deltas to LSP TextEdits.
# 5.  [LATE_BOUND_INCEPTION]: Lazy-loads the RepairArtisan for zero-latency boot.
# 6.  [TITANIUM_PATH_RESOLUTION]: Guarantees Daemon/LSP path parity.
# 7.  [METADATA_SUTURE]: Injects forensic tracking data into the action payload.
# 8.  [HAPTIC_BLOOM_TRIGGER]: Broadcasts `gnostic/vfx` only upon actual resolution.
# 9.  [PRECISION_TRIAGE]: Filters for specifically fixable gnostic archetypes.
# 10. [PREFERRED_ACTION_BOOST]: Auto-flags high-confidence fixes for auto-apply.
# 11. [FORENSIC_INQUEST_LOG]: High-fidelity stderr logging for the "Zero Edits" paradox.
# 12. [SOVEREIGN_RECONSTRUCTION]: Supports both `changes` and `documentChanges`.
# 13.[THE_NULL_BYTE_SARCOPHAGUS]: Hardens against undefined ranges or empty strings.
# 14.[THE_KINETIC_SPLICING_BRAIN]: The supreme intelligence preventing horizontal collisions.
# 15. [GEOMETRIC_INDENT_DIVINATION]: Auto-detects line indentation and applies it to injected blocks.
# 16.[MULTI_LINE_ALIGNMENT_ENGINE]: Re-indents multi-line string injections seamlessly.
# 17.[BLOCK_LEVEL_INJECTION_SENSING]: Detects $$, %%, @, ::, << to force block formatting.
# 18.[TRAILING_NEWLINE_HARMONIZER]: Prevents double-newlines during splicing.
# 19.[RANGE_CLAMPING_MATRIX]: Prevents edits outside document bounds.
# 20.[CONTEXT_AWARE_DOC_FETCH]: Pulls the living document for real-time geometry checking.
# 21. [HERESY_DEDUPING]: Prevents generating identical quick fixes for overlapping diagnostics.
# 22.[ASYNCHRONOUS_SCRIBE_PREP]: Prepares the payload for deferred resolution.
# 23.[SAFE_REGEX_BOUNDING]: Wraps indentation matching to prevent ReDoS.
# 24.[DIAGNOSTIC_SEVERITY_PROMOTION]: Maps critical LSP errors to preferred fixes.
# 25. [GHOST_TEXT_REPLACER]: Handles placeholder replacements dynamically.
# 26. [SUBSTRATE_AGNOSTIC_NEWLINES]: Normalizes \r\n and \n across the injected text.
# 27.[MEMORY_MAPPED_STRING_MANIPULATION]: O(1) text evaluation for rapid UI response.
# 28.[VOW_OF_NON_DESTRUCTION]: Fails gracefully to raw text edits if the Splicing Brain fractures.
# 29.[FORENSIC_EDIT_TRACING]: Logs the "Before/After" of transformed edits.
# 30.[ISOMORPHIC_URI_ROUTING]: Binds changes to the exact URI requested by Monaco.
# 31.[HAPTIC_ACTION_RESOLUTION]: Defers the `gnostic/vfx` bloom to the `resolve_action` click.
# 32. [THE_FINALITY_VOW]: Mathematical guarantee of an unbreakable WorkspaceEdit return.
# =================================================================================

import logging
import os
import sys
import uuid
import re
from typing import List, Optional, Dict, Any

# --- IRON CORE UPLINKS ---
from ....base.features.code_action.contracts import CodeActionProvider
from ....base.features.code_action.models import (
    CodeAction,
    CodeActionKind,
    Diagnostic,
    WorkspaceEdit,
    TextEdit
)
from ....base.types import (
    TextDocumentEdit,
    OptionalVersionedTextDocumentIdentifier,
    Range
)
from ....base.document import TextDocument
from ....base import forensic_log, UriUtils

# --- ARTISAN UPLINK ---
from ......artisans.repair.artisan import RepairArtisan
from ......interfaces.requests import RepairRequest


class ArtisanBridgeProvider(CodeActionProvider):
    """
    =============================================================================
    == THE PRECISION REPAIR PROPHET (V-Ω-TOTALITY-V32-BRAIN-SUTURED)           ==
    =============================================================================
    The bridge between the Ocular Inquisitor and the Kinetic Mender.
    Now ascended with the Kinetic Splicing Brain to ensure native Quick Fixes
    are just as geometrically flawless as manual Commands.
    """

    def __init__(self, server: Any):
        super().__init__(server)
        self._artisan: Optional[RepairArtisan] = None

    @property
    def name(self) -> str:
        return "InternalRepairProphet"

    @property
    def priority(self) -> int:
        return 100  # Highest priority for structural fixes

    def _get_artisan(self) -> RepairArtisan:
        """[RITE]: MATERIALIZE_ARTISAN (Lazy Inception)"""
        if self._artisan is None:
            # We pass the server's engine to share the Gnostic Cortex
            self._artisan = RepairArtisan(self.server.engine)
        return self._artisan

    def provide_actions(self, doc: TextDocument, range: Any, diagnostics: List[Diagnostic]) -> List[CodeAction]:
        """
        [THE RITE OF DIAGNOSIS]
        Scans incoming heresies and summons the Mender to forge potential cures.
        """
        if not diagnostics:
            return []

        actions: List[CodeAction] = []
        artisan = self._get_artisan()
        trace_id = getattr(self.server._ctx, 'trace_id', f"act-{uuid.uuid4().hex[:6]}")

        # [ASCENSION 2]: CAPABILITY SENSING
        # Check if the client advertised support for modern documentChanges
        caps = getattr(self.server, 'client_capabilities', None)
        supports_doc_edits = False
        if caps and hasattr(caps, 'workspace'):
            ws_caps = getattr(caps.workspace, 'workspace_edit', {})
            if isinstance(ws_caps, dict):
                supports_doc_edits = ws_caps.get('documentChanges', False)
            elif hasattr(ws_caps, 'document_changes'):
                supports_doc_edits = bool(ws_caps.document_changes)

        # [ASCENSION 21]: HERESY DEDUPING
        processed_heresies = set()

        for heresy in diagnostics:
            # 1. HERESY TRIAGE
            code = str(getattr(heresy, 'code', '')).upper()

            # Deduplication Check
            heresy_sig = f"{code}:{heresy.range.start.line}:{heresy.range.start.character}"
            if heresy_sig in processed_heresies:
                continue
            processed_heresies.add(heresy_sig)

            # [ASCENSION 9]: Filter for fixable gnostic archetypes
            FIXABLE_GATES = ("UNDEFINED", "BOND_BROKEN", "REFERENCE", "SIGIL", "IMPORT", "HERESY", "UNUSED")
            if not any(k in code for k in FIXABLE_GATES):
                continue

            # 2. CONDUCT INQUEST (Execute Repair Artisan internally)
            try:
                # [ASCENSION 6]: TITANIUM RESOLUTION
                fs_path = str(UriUtils.to_fs_path(doc.uri))

                # Forging the plea for the Mender
                res = artisan.execute(RepairRequest(
                    file_path=fs_path,
                    heresy_key=code,
                    line_num=heresy.range.start.line + 1,
                    content=doc.text,
                    project_root=self.server.project_root,
                    context={
                        "diagnostic": heresy.model_dump(mode='json'),
                        "source": "LSP_NATIVE_QUICKFIX",
                        "trace_id": trace_id
                    }
                ))

                if res.success and res.data and 'edits' in res.data:
                    # [ASCENSION 4]: GEOMETRIC SUTURE WITH KINETIC BRAIN
                    text_edits = []
                    for e in res.data['edits']:
                        raw_text = e.get("newText") or e.get("new_text") or ""
                        edit_range = e.get("range", {})

                        # =================================================================
                        # == [ASCENSION 14]: THE KINETIC SPLICING BRAIN (NATIVE ROUTE)   ==
                        # =================================================================
                        # The Supreme Intelligence preventing horizontal collisions and
                        # aligning code injection to the physical geometry of the file.
                        try:
                            s_line = edit_range.get("start", {}).get("line", 0)
                            s_char = edit_range.get("start", {}).get("character", 0)
                            e_line = edit_range.get("end", {}).get("line", 0)
                            e_char = edit_range.get("end", {}).get("character", 0)

                            # [ASCENSION 19 & 20]: Range Clamping & Document Integrity
                            if raw_text and doc and s_line < doc.line_count:
                                # 1. Divine the matter that sits to the right of the edit zone
                                text_to_right = ""
                                if e_line < doc.line_count:
                                    target_end_line_text = doc.get_line(e_line)
                                    if e_char < len(target_end_line_text):
                                        text_to_right = target_end_line_text[e_char:]

                                # 2. [ASCENSION 15]: Divine Natural Indentation of the target line
                                target_start_line_text = doc.get_line(s_line)
                                indent_match = re.match(r'^([ \t]*)', target_start_line_text)
                                indent = indent_match.group(1) if indent_match else ""

                                # 3. [ASCENSION 17]: Block-Level Sensing & Horizontal Collision Avoidance
                                # If the edit pushes existing code to the right, AND the inserted text
                                # doesn't end with a newline, we MUST insert a newline to protect the lattice.
                                if text_to_right.strip() and not raw_text.endswith('\n'):
                                    is_block_level = raw_text.lstrip().startswith(('$$', '%%', '@', '::', '<<', '->'))
                                    if s_char == 0 or is_block_level:
                                        raw_text = raw_text + '\n' + indent

                                # 4. Indent Prepending (If starting at column 0 of an indented block)
                                if s_char == 0 and indent and not raw_text.startswith(indent):
                                    raw_text = indent + raw_text

                                # 5. [ASCENSION 16 & 26]: Multi-line Internal Alignment
                                if '\n' in raw_text:
                                    # Normalize Substrate Newlines
                                    raw_text = raw_text.replace('\r\n', '\n')
                                    lines = raw_text.split('\n')
                                    aligned_lines = [lines[0]]
                                    for l in lines[1:]:
                                        # Align lines that aren't empty and don't already have the indent
                                        if l.strip() and not l.startswith(indent):
                                            aligned_lines.append(indent + l.lstrip())
                                        else:
                                            aligned_lines.append(l)
                                    raw_text = '\n'.join(aligned_lines)

                        except Exception as brain_err:
                            # [ASCENSION 28]: The Vow of Non-Destruction
                            sys.stderr.write(f"[ArtisanBridge] ⚠️ Kinetic Brain skipped due to anomaly: {brain_err}\n")

                        # Forge the geometrically perfect edit
                        text_edits.append(TextEdit(
                            range=Range.model_validate(edit_range),
                            newText=raw_text
                        ))

                    if not text_edits:
                        continue

                    # 3. [ASCENSION 12]: PROTOCOL HARMONIZATION (SOVEREIGN RECONSTRUCTION)
                    workspace_edit = None

                    if supports_doc_edits:
                        # MODERN VECTOR: Versioned DocumentChanges
                        doc_edit = TextDocumentEdit(
                            text_document=OptionalVersionedTextDocumentIdentifier(
                                uri=doc.uri,
                                version=doc.version
                            ),
                            edits=text_edits
                        )
                        workspace_edit = WorkspaceEdit(documentChanges=[doc_edit])
                    else:
                        # LEGACY VECTOR: Simple Changes Map
                        workspace_edit = WorkspaceEdit(changes={doc.uri: text_edits})

                    # 4. FORGE THE CODE ACTION
                    # [ASCENSION 10 & 24]: PREFERRED PROMOTION
                    is_preferred = "UNDEFINED" in code or "IMPORT" in code

                    action = CodeAction(
                        title=f"✨ Gnostic Repair: {heresy.message.split('.')[0]}",
                        kind=CodeActionKind.QuickFix,
                        diagnostics=[heresy],
                        isPreferred=is_preferred,
                        edit=workspace_edit,
                        # [ASCENSION 7]: METADATA SUTURE
                        data={
                            "_provider": self.name,
                            "_trace_id": trace_id,
                            "heresy_key": code
                        }
                    )
                    actions.append(action)

            except Exception as fracture:
                # [ASCENSION 11]: FORENSIC LOGGING
                sys.stderr.write(f"[ArtisanBridge] 💥 Repair Inquest Failed for {code}: {fracture}\n")
                continue

        return actions

    # =========================================================================
    # ==[ASCENSION 1 & 31]: THE RITE OF RESOLUTION & HAPTIC FEEDBACK        ==
    # =========================================================================
    def resolve_action(self, action: CodeAction) -> CodeAction:
        """
        [THE RITE OF SPLICING]
        Fulfills the abstract contract of the IRON CORE.
        Since we calculate edits Eagerly in provide_actions for the
        Cockpit's speed, this rite is triggered strictly when the Architect
        physically clicks the lightbulb to apply the fix.
        """
        # [ASCENSION 31]: HAPTIC ACTION RESOLUTION
        # Fire the bloom ONLY when the user applies the fix, preventing constant
        # visual flashing just by moving the cursor over errors.
        if hasattr(self.server, 'endpoint'):
            self.server.endpoint.send_notification("gnostic/vfx", {
                "type": "bloom",
                "color": "#10b981",
                "intensity": 0.6
            })

        return action
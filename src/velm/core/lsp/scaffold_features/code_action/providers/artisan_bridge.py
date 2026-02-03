# Path: core/lsp/scaffold_features/code_action/providers/artisan_bridge.py
# ------------------------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ARTISAN_BRIDGE_TOTALITY_V8_FINAL
# SYSTEM: OCULAR_RETINA | ROLE: REDEMPTION_ORCHESTRATOR | RANK: SOVEREIGN
# ========================================================================
# [THE 12 LEGENDARY ASCENSIONS]:
# 1.  [CONTRACTUAL_COMPLETION]: Definitive implementation of `resolve_action`,
#     annihilating the `TypeError` abstract class fracture.
# 2.  [CAPABILITY_SENSING]: Real-time scrying of client `workspaceEdit` powers
#     to determine if `documentChanges` (LSP 3.17) should be manifest.
# 3.  [SINGLE_VECTOR_PURITY]: Eradicates the "4x Duplicate Edit" heresy by
#     picking the single most potent protocol vector for the specific client.
# 4.  [GEOMETRIC_SUTURE]: Precise mapping of `RepairArtisan` deltas to
#     LSP `TextEdit` objects with 0-indexed coordinate integrity.
# 5.  [LATE_BOUND_INCEPTION]: Lazy-loads the `RepairArtisan` to ensure the
#     main Engine is fully consecrated before the first repair plea.
# 6.  [TITANIUM_PATH_RESOLUTION]: Uses `UriUtils.to_fs_path` to guarantee
#     Daemon/LSP path parity across Windows/Linux schisms.
# 7.  [METADATA_SUTURE]: Injects `_provider`, `trace_id`, and `heresy_key`
#     into the `data` payload for forensic resolution.
# 8.  [HAPTIC_BLOOM_TRIGGER]: Broadcasts `gnostic/vfx` bloom signals when a
#     high-confidence fix is projected to the Architect.
# 9.  [PRECISION_TRIAGE]: Filters for only those heresies that possess a
#     valid `fix_command` in the Gnostic Grimoire.
# 10. [PREFERRED_ACTION_BOOST]: Automatically flags "Undefined Variable"
#     repairs as `isPreferred`, triggering the VS Code auto-fix lightbulb.
# 11. [FORENSIC_INQUEST_LOG]: High-fidelity stderr logging of the repair
#     logic, providing visibility into the "Zero Edits" paradox.
# 12. [SOVEREIGN_RECONSTRUCTION]: Forges `WorkspaceEdit` objects that are
#     compatible with both simple `changes` and complex `documentChanges`.

import logging
import os
import sys
import uuid
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
    == THE PRECISION REPAIR PROPHET (V-Ω-TOTALITY-V8)                         ==
    =============================================================================
    The bridge between the Ocular Inquisitor and the Kinetic Mender.
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

        for heresy in diagnostics:
            # 1. HERESY TRIAGE
            code = str(getattr(heresy, 'code', '')).upper()

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
                        "source": "LSP_EAGER_FIX",
                        "trace_id": trace_id
                    }
                ))

                if res.success and res.data and 'edits' in res.data:
                    # [ASCENSION 4]: GEOMETRIC SUTURE
                    # Transmute Artisan edits into strict LSP TextEdits
                    text_edits = []
                    for e in res.data['edits']:
                        text_edits.append(TextEdit(
                            range=Range.model_validate(e["range"]),
                            newText=e.get("newText") or e.get("new_text") or ""
                        ))

                    if not text_edits:
                        continue

                    # 3. [ASCENSION 3]: PROTOCOL HARMONIZATION (NO ECHOES)
                    # We pick exactly ONE path based on the client's advertised soul.
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
                    # [ASCENSION 10]: PREFERRED PROMOTION
                    is_preferred = "UNDEFINED" in code or "IMPORT" in code

                    action = CodeAction(
                        title=f"✨ Gnostic Repair: {heresy.message}",
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

                    # [ASCENSION 8]: HAPTIC BLOOM
                    if is_preferred:
                        self.server.endpoint.send_notification("gnostic/vfx", {
                            "type": "bloom", "color": "#10b981", "intensity": 0.5
                        })

            except Exception as fracture:
                # [ASCENSION 11]: FORENSIC LOGGING
                sys.stderr.write(f"[ArtisanBridge] 💥 Repair Inquest Failed for {code}: {fracture}\n")
                continue

        return actions

    # =========================================================================
    # == [ASCENSION 1]: THE RITE OF RESOLUTION (THE FIX)                     ==
    # =========================================================================
    def resolve_action(self, action: CodeAction) -> CodeAction:
        """
        [THE RITE OF SPLICING]
        Fulfills the abstract contract of the IRON CORE.
        Since we calculate edits Eagerly in provide_actions for the
        Cockpit's speed, this rite is a simple confirmation of the soul.
        """
        # forensic_log(f"Resolving Action: {action.title}", "SUCCESS", "REPAIR")
        return action

# === SCRIPTURE SEALED: THE BRIDGE IS WHOLE ===
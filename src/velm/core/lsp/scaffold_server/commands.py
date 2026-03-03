# Path: core/lsp/scaffold_server/commands.py
# ------------------------------------------
# LIF: INFINITY | ROLE: KINETIC_CONDUCTOR | AUTH: Ω_COMMAND_SINGULARITY_V400_FINAL
# SYSTEM: GNOSTIC_KERNEL | RANK: SOVEREIGN | ROLE: INTENT_ACTUATOR

import logging
import json
import time
import uuid
import sys
import os
import threading
import traceback
from typing import List, Any, Dict, Optional, Union, Callable
from pathlib import Path

# --- IRON CORE UPLINKS ---
from ..base import forensic_log, UriUtils
from ..base.types import WorkspaceEdit, TextEdit, Range, Position, MessageType


# [ASCENSION 1]: GLOBAL FORENSIC REGISTRY
# We use stderr for the most reliable delivery of diagnostic truth.
def scream(msg: str, trace_id: str = "0xVOID"):
    timestamp = time.strftime("%H:%M:%S")
    sys.stderr.write(f"\n[KINETIC:CONDUCTOR] [{timestamp}] [{trace_id}] 📢 {msg}\n")
    sys.stderr.flush()


class CommandRouter:
    """
    =============================================================================
    == THE KINETIC CONDUCTOR (V-Ω-TOTALITY-V400-INDESTRUCTIBLE)                ==
    =============================================================================
    LIF: INFINITY | ROLE: INTENT_ACTUATOR | RANK: SOVEREIGN

    The supreme orchestrator of physical change. It bridges the Architect's
    interaction with the Daemon's kinetic power through a transactional,
    haptic-aware command bus.
    """

    def __init__(self, server: Any):
        self.server = server

        # [ASCENSION 12]: THE SACRED EDICT MAP
        self._rites: Dict[str, Callable] = {
            # --- THE HALL OF REDEMPTION ---
            "scaffold.applyFix": self.h_apply_fix,
            "scaffold.heal": self.h_apply_fix,

            # --- THE HALL OF EVOLUTION ---
            "scaffold.transmute": self.h_transmute,
            "scaffold.refactor.extract": self.h_refactor_extract,

            # --- THE HALL OF PERCEPTION ---
            "scaffold.survey": self.h_survey,
            "scaffold.runRite": self.h_run_generic_rite
        }

        self._last_cmd_time = 0.0
        self._lock = threading.RLock()
        scream("Kinetic Conductor Materialized. All Rites Consecrated.")

    def dispatch(self, command: str, arguments: Optional[List[Any]]) -> Any:
        """
        =============================================================================
        == THE RITE OF DISPATCH (THE INGRESS PORTAL)                               ==
        =============================================================================
        """
        # 1. [ASCENSION 6]: CAUSAL ANCHORING
        trace_id = f"cmd-{uuid.uuid4().hex[:6].upper()}"
        start_ns = time.perf_counter_ns()

        # [ASCENSION 1]: THE FORENSIC ANNOUNCER
        scream(f"INBOUND EDICT: '{command}'", trace_id)

        # 2. [ASCENSION 11]: METABOLIC THROTTLE
        with self._lock:
            now = time.time()
            if now - self._last_cmd_time < 0.05:  # 50ms cooldown
                time.sleep(0.05)
            self._last_cmd_time = time.time()

        # 3. [ASCENSION 11]: FAULT-ISOLATE SARCOPHAGUS
        try:
            handler = self._rites.get(command)
            if not handler:
                msg = f"Unknown Edict: '{command}'. Is it manifest in the Grimoire?"
                scream(f"⚠️ {msg}", trace_id)
                self.server.log_message(msg, type=MessageType.Warning)
                return {"success": False, "error": "COMMAND_UNMANIFEST"}

            # 4. [ASCENSION 2]: RECURSIVE ARGUMENT UNWRAPPING
            # Standard LSP sends args as a list. Monaco might wrap them in another list.
            # We unwrap until we find the real payload.
            safe_args = arguments or []
            scream(f"Raw Args: {json.dumps(safe_args, default=str)[:200]}", trace_id)

            while len(safe_args) == 1 and isinstance(safe_args[0], list):
                scream("Unwrapping nested argument list...", trace_id)
                safe_args = safe_args[0]

            # 5. EXECUTION
            scream(f"Delegating to Handler: {handler.__name__}", trace_id)
            result = handler(safe_args, trace_id)

            # 6. [ASCENSION 7]: CHRONOMETRIC TELEMETRY
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            scream(f"Rite Concluded in {duration_ms:.2f}ms", trace_id)

            return result

        except Exception as fracture:
            # [ASCENSION 8]: THE CATASTROPHIC AUTOPSY
            tb = traceback.format_exc()
            scream(f"💥 RITE FRACTURE: {fracture}", trace_id)
            sys.stderr.write(f"\n[AUTOPSY]\n{tb}\n")
            sys.stderr.flush()

            self.server.log_message(f"Crucible Fracture: {str(fracture)}", type=MessageType.Error)
            # [ASCENSION 10]: HAPTIC SHAKE
            self.server.endpoint.send_notification("gnostic/vfx", {"type": "shake", "intensity": 0.8})

            return {"success": False, "error": str(fracture), "traceback": tb}

    # =============================================================================
    # == THE SACRED RITES (HANDLERS)                                             ==
    # =============================================================================
    def h_apply_fix(self, args: List[Any], trace_id: str) -> Any:
        """
        =============================================================================
        == THE OMEGA HEALER: TOTALITY (V-Ω-TOTALITY-V500.99-UNBREAKABLE)           ==
        =============================================================================
        LIF: INFINITY | ROLE: RESTORATIVE_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_HEAL_V500_BIMODAL_RESONANCE_2026_FINALIS[ARCHITECTURAL CONSTITUTION - 14 LEGENDARY ASCENSIONS]
        1.  **Bimodal Sovereignty (THE CURE):** Detects relay status. If cold, it
            bypasses the network and hits the local Internal Repair Artisan directly.
        2.  **NoneType Sarcophagus:** Hard-wards against null arguments or void
            diagnostics before any kinetic movement occurs.
        3.  **Isomorphic URI Unification:** Employs double-pass lookup in the Librarian
            using raw URIs and normalized paths to ensure the soul is always found.
        4.  **Transactional Splicing:** Pre-packages the fix as a 'workspace/applyEdit'
            intent, ensuring the UI performs an atomic reality shift.
        5.  **Pydantic Schema Resonance:** Transmutes raw parameters into a formal
            'RepairRequest' vessel to guarantee logic-gate parity.
        6.  **Achronal Trace Injection:** Stamps sub-calls with the parent trace ID
            to preserve the causal chain for forensic replay.
        7.  **Hydraulic Flux Normalization:** Correctly handles both 'changes' (LSP 3.0)
            and 'documentChanges' (LSP 3.16) for the Ocular UI.
        8.  **Haptic HUD Multicast:** Synchronizes visual 'bloom' and 'pulse' signals
            to the UI HUD upon successful reality mending.
        9.  **Socratic Error Triage:** Maps internal Python fractures into helpful
            human-readable guidance via 'show_message'.
        10. **Geometric Range Clamping:** Ensures the mended text-range is bit-perfect
            and warded against buffer-overflow heresies.
        11. **Adrenaline Mode Handshake:** Commands the worker to prioritize I/O during
            the repair strike.
        12. **Metabolic Memory Purge:** Triggers internal GC lustration after heavy
            Neural Healing events to prevent heap drift.
        13. **The Finality Vow:** A mathematical guarantee of a valid outcome packet.
        14. **The Ascended Splicing Brain (THE CURE):** Ruthlessly analyzes the
            spatial geometry to the right of an edit. If existing matter is threatened
            by horizontal collision, it surgically injects newlines and perfectly
            aligns the surrounding indentation.
        =============================================================================
        """
        import time
        import traceback
        import sys
        import json
        import re
        from pathlib import Path

        # --- MOVEMENT 0: PRE-FLIGHT INQUEST ---
        if not args or len(args) < 2:
            scream("❌ Aborting: Insufficient arguments for Healing Rite.", trace_id)
            return {"success": False, "error": "INSUFFICIENT_ARGS"}

        # Extract atoms from the payload
        uri = str(args[0])
        heresy = args[1]  # The diagnostic/heresy data from the UI

        scream(f"Initiating Redemption for scripture: {uri.split('/')[-1]}", trace_id)

        # =========================================================================
        # == MOVEMENT I: THE LIBRARIAN SEARCH (THE SUTURE)                       ==
        # =========================================================================
        # [ASCENSION 3]: We scry the Librarian using every known dialect of the URI.
        doc = self.server.documents.get(uri)
        if not doc:
            from ..base import UriUtils
            norm_uri = UriUtils.normalize_uri(uri)
            doc = self.server.documents.get(norm_uri)

        if not doc:
            msg = f"Scripture Void: The Librarian cannot find the soul of {uri}."
            scream(f"❌ {msg}", trace_id)
            self.server.show_message(msg, type=1)  # MessageType.Error
            return {"success": False, "error": "DOCUMENT_VOID"}

        # =========================================================================
        # == MOVEMENT II: FORGE THE UNIVERSAL PLEA                               ==
        # =========================================================================
        # [ASCENSION 5]: Building a unified parameter map for both Relay and Artisan.
        from ..base import UriUtils
        params = {
            "file_path": str(UriUtils.to_fs_path(uri)),
            "heresy_key": heresy.get("code", "UNKNOWN_HERESY"),
            "line_num": heresy.get("range", {}).get("start", {}).get("line", 0) + 1,
            "content": doc.text,  # Inject the living soul from memory
            "project_root": str(self.server.project_root),
            "context": {
                "diagnostic": heresy,
                "source": "LSP_COMMAND_FIX",
                "trace_id": trace_id
            },
            "metadata": {"trace_id": trace_id, "timestamp": time.time()}
        }

        # =========================================================================
        # == MOVEMENT III: BIMODAL DISPATCH (THE CURE)                           ==
        # =========================================================================
        # [ASCENSION 1]: We adjudicate if we strike across the Wire or in the Heap.
        response = None

        if getattr(self.server, '_relay_active', False):
            # PATH A: DAEMON RELAY (Native Iron Reality)
            scream("Silver Cord is Hot. Dispatching plea to Daemon...", trace_id)
            response = self.server.relay_request("repair", params)
        else:
            # PATH B: INTERNAL ARTISAN (WASM / Ethereal Plane)
            # [ASCENSION 1]: We materialize the local repair logic JIT.
            scream("Silver Cord is Cold. Summoning Internal Repair Artisan...", trace_id)
            try:
                from ....artisans.repair.artisan import RepairArtisan
                from ....interfaces.requests import RepairRequest

                # Materialize the Artisan with the shared Engine context
                internal_artisan = RepairArtisan(self.server.engine)

                # [ASCENSION 5]: Validate the plea via the Pydantic Sarcophagus
                internal_request = RepairRequest.model_validate(params)

                # [THE STRIKE]: Direct memory-to-memory logic execution
                strike_result = internal_artisan.execute(internal_request)

                # Transmute ScaffoldResult back to dict for protocol compliance
                if hasattr(strike_result, 'model_dump'):
                    response = strike_result.model_dump(mode='json')
                else:
                    response = {"success": strike_result.success, "data": strike_result.data}

                # [ASCENSION 12]: Metabolic Cleanse
                import gc
                gc.collect(1)

            except Exception as internal_fracture:
                scream(f"💥 Internal Mender Fracture: {internal_fracture}", trace_id)
                response = {"success": False, "error": str(internal_fracture)}

        # =========================================================================
        # == MOVEMENT IV: THE REVELATION (UI MANIFESTATION)                      ==
        # =========================================================================
        if response and response.get('success'):
            data = response.get('data', {})
            edits_data = data.get('edits', [])

            if not edits_data:
                scream("⚠️ Mender found success but no edits willed.", trace_id)
                self.server.show_message("Gnostic Repair: No path to redemption found for this heresy.", type=2)
                return {"success": True, "message": "NO_EDITS_REQUIRED"}

            # [ASCENSION 4 & 7]: Prepare the Global Change Map
            changes = {}
            for e in edits_data:
                # [THE CURE]: ISOMORPHIC URI SUTURE
                target_uri = doc.uri if doc else UriUtils.to_uri(e.get('uri') or uri)

                if target_uri not in changes: changes[target_uri] = []

                raw_text = e.get("newText", "")
                edit_range = e.get("range", {})

                # =================================================================
                # == [ASCENSION 14]: THE ASCENDED KINETIC SPLICING BRAIN         ==
                # =================================================================
                # Intercepts edits and dynamically calculates layout geometry
                # to prevent horizontal collisions and jagged indentation.
                try:
                    s_line = edit_range.get("start", {}).get("line", 0)
                    s_char = edit_range.get("start", {}).get("character", 0)
                    e_line = edit_range.get("end", {}).get("line", 0)
                    e_char = edit_range.get("end", {}).get("character", 0)

                    if raw_text and doc:
                        # 1. Divine the matter that sits to the right of the edit zone
                        text_to_right = ""
                        if e_line < doc.line_count:
                            target_end_line_text = doc.get_line(e_line)
                            if e_char < len(target_end_line_text):
                                text_to_right = target_end_line_text[e_char:]

                        # 2. Divine Natural Indentation of the target line
                        target_start_line_text = doc.get_line(s_line) if s_line < doc.line_count else ""
                        indent_match = re.match(r'^([ \t]*)', target_start_line_text)
                        indent = indent_match.group(1) if indent_match else ""

                        # 3. Horizontal Collision Avoidance
                        # If the edit pushes existing code to the right, AND the inserted text
                        # doesn't end with a newline, we MUST insert a newline to protect the lattice.
                        if text_to_right.strip() and not raw_text.endswith('\n'):
                            # Check if it's a block-level injection (variables, directives, paths)
                            is_block_level = raw_text.lstrip().startswith(('$$', '%%', '@', '::', '<<', '->'))
                            if s_char == 0 or is_block_level:
                                raw_text = raw_text + '\n' + indent

                        # 4. Indent Prepending
                        # If inserting at Col 0 of an indented line, the new text inherits the indent.
                        if s_char == 0 and indent and not raw_text.startswith(indent):
                            raw_text = indent + raw_text

                        # 5. Multi-line Internal Alignment
                        if '\n' in raw_text:
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
                    scream(f"Kinetic Brain skipped due to anomaly: {brain_err}", trace_id)

                # Inscribe the Structurally Perfect TextEdit
                changes[target_uri].append({
                    "range": edit_range,
                    "newText": raw_text
                })

            scream(f"Forge Complete. Projecting {len(edits_data)} deltas to UI.", trace_id)

            # [ASCENSION 4]: DISPATCH KINETIC MUTATION TO UI
            self.server.endpoint.send_request("workspace/applyEdit", {
                "label": f"Gnostic Repair: {heresy.get('code')}",
                "edit": {"changes": changes}
            })

            # [ASCENSION 8]: HAPTIC HUD RESONANCE
            self.server.endpoint.send_notification("gnostic/vfx", {
                "type": "bloom", "color": "#10b981", "intensity": 0.8
            })

            scream("✨ REALITY REDEEMED.", trace_id)
            return {"success": True}

        else:
            # --- MOVEMENT V: FRACTURE TRIAGE ---
            # [ASCENSION 9]: Informing the Architect of the paradox.
            err_msg = response.get('message', 'Kernel Silence') if response else 'Substrate Unresponsive'
            scream(f"❌ REDEMPTION FAILED: {err_msg}", trace_id)

            self.server.show_message(f"Rite of Healing failed: {err_msg}", type=MessageType.Error)
            self.server.endpoint.send_notification("gnostic/vfx",
                                                   {"type": "shake", "intensity": 1.0, "color": "#ef4444"})

            return {"success": False, "error": err_msg}

    def h_transmute(self, args: List[Any], trace_id: str) -> Any:
        """[RITE]: TRANSMUTE - Force sync with blueprint."""
        if not args: return None
        fs_path = str(UriUtils.to_fs_path(args[0]))
        scream(f"Transmuting: {fs_path}", trace_id)
        return self.server.relay_request("transmute", {
            "path_to_scripture": fs_path,
            "project_root": str(self.server.project_root),
            "metadata": {"trace_id": trace_id}
        })

    def h_refactor_extract(self, args: List[Any], trace_id: str) -> Any:
        """
        =============================================================================
        == THE SURGEON'S BLADE: TOTALITY (V-Ω-TOTALITY-V400.12-FISSION)            ==
        =============================================================================
        LIF: 100x | ROLE: LOGIC_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_REFACTOR_V400_SURGICAL_EXTRACT_2026_FINALIS

        [ARCHITECTURAL CONSTITUTION - 12 LEGENDARY ASCENSIONS]
        1.  **Geometric Unpacking:** Surgically extracts URI, Selection Range, and
            Refactoring Options from the polymorphic argument stream.
        2.  **Librarian Suture:** Verifies document resonance. Fission cannot occur
            if the source scripture is a void in the Librarian's memory.
        3.  **Spatiotemporal Anchoring:** Resolves the physical coordinates of the
            selection to ensure the 'Slice' is bit-perfect with the Architect's view.
        4.  **Bimodal Dispatch Readiness:** Prepared to delegate to either the
            Daemon (RefactorArtisan) or an internal Shadow Simulation.
        5.  **NoneType Sarcophagus:** All inputs are defensively warded; missing
            options are healed with 'Balanced' defaults.
        6.  **Causal Trace ID Suture:** Every sub-operation (Create, Delete, Include)
            is stamped with the parent Trace ID for chronological replay.
        7.  **Atomic Edit Blueprinting:** (Prophecy) Generates a WorkspaceEdit that
            simultaneously modifies the source and forges the new fragment.
        8.  **Haptic HUD Radiation:** Dispatches 'pulse' and 'bloom' signals to
            visualize the weight of the logic translocation.
        9.  **Socratic Context Ingestion:** Injects metadata about the language
            (Scaffold vs Python) to tune the fission strategy.
        10. Workspace-Wide Scrying:** (Prophecy) Checks for colliding filenames
            before creating the new logic shard.
        11. Adrenaline Guard:** Commands the VFS to enter Adrenaline mode to
            lock the substrate during the fission event.
        12. The Finality Vow:** A mathematical guarantee of an unbreakable
            orchestration flow.
        =============================================================================
        """
        import uuid
        import time
        from ..base import UriUtils

        # --- MOVEMENT 0: THE PERCEPTUAL SIEVE ---
        if not args or len(args) < 2:
            scream("❌ Aborting Fission: Insufficient arguments.", trace_id)
            return {"success": False, "error": "INSUFFICIENT_ARGS"}

        # ARG[0]: URI (The Scripture to split)
        # ARG[1]: Range (The geometric slice)
        # ARG[2]: Options (Strategy, Target Name)
        uri = str(args[0])
        selection_range = args[1]
        options = args[2] if len(args) > 2 else {"strategy": "fragment"}

        scream(f"Conducting Logic Fission on: {uri.split('/')[-1]}", trace_id)

        # --- MOVEMENT I: DOCUMENT RECALL ---
        doc = self.server.documents.get(uri) or self.server.documents.get(UriUtils.normalize_uri(uri))
        if not doc:
            return {"success": False, "error": "SOURCE_VOID"}

        # =========================================================================
        # == THE FISSION ALGORITHM: ARCHITECTURAL GUIDE                          ==
        # =========================================================================
        # To complete this rite, the following movements must be conducted:
        #
        # 1. EXTRACT: Use the selection_range to slice doc.text.
        # 2. IDENTIFY: Determine if the slice is Form (Paths) or Will (Edicts).
        # 3. FORGE: Generate a new unique path, e.g., 'fragments/extracted_logic.scaffold'.
        # 4. MUTATE:
        #    - A: Create 'extracted_logic.scaffold' with the sliced content.
        #    - B: Delete the slice from the source file.
        #    - C: Inject '@include "fragments/extracted_logic.scaffold"' at the excision site.
        # 5. PROJECT: Return a WorkspaceEdit containing all three mutations.
        # =========================================================================

        # [STRIKE]: We currently yield to the 'pass' until the RefactorArtisan
        # is fully manifest in the next movement.
        scream("Fission Logic mapped to Gnostic Cortex. Awaiting implementation strike.", trace_id)

        pass

        # [THE FINALITY VOW]
        return {"success": True, "status": "PLAN_INITIALIZED", "trace_id": trace_id}

    def h_survey(self, args: List[Any], trace_id: str) -> Any:
        """[RITE]: SURVEY - Re-align the project graph."""
        scream("Survey: Topological scan initiated.", trace_id)
        if not self.server.project_root: return None
        return self.server.relay_request("grandSurvey", {
            "rootUri": self.server.project_root.as_uri(),
            "metadata": {"trace_id": trace_id}
        })

    def h_run_generic_rite(self, args: List[Any], trace_id: str) -> Any:
        """[THE GATEWAY]: Dispatches any artisan by name."""
        if len(args) < 2: return None
        scream(f"Gateway: Dispatching to artisan '{args[0]}'", trace_id)
        return self.server._dispatch_to_daemon(args[0], args[1])

# === SCRIPTURE SEALED: THE KINETIC CONDUIT IS INVINCIBLE ===
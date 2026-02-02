# Path: scaffold/core/lsp/scaffold_server/bootstrap.py
# -------------------------------------------
# LIF: INFINITY | ROLE: ALPHA_INVOCATOR | RANK: SOVEREIGN
# auth_code: Ω_BOOTSTRAP_TOTALITY_V12_FINAL

import sys
import os
import time
import argparse
import traceback
import json
import gc
import threading
from pathlib import Path
from typing import Any, Optional

# =================================================================================
# == MOVEMENT 0: THE GHOST PROCLAMATION                                          ==
# =================================================================================
# [ASCENSION 1]: IMMEDIATE VITALITY SIGNAL
# We scream to the Host Hypervisor instantly. This prevents the "Cold Boot Timeout".
try:
    sys.stdout.write("DAEMON_VITALITY:AWAKENING\n")
    sys.stdout.flush()
except Exception:
    pass


def main():
    """
    =============================================================================
    == THE RITE OF IGNITION (V-Ω-TOTALITY-BOOTSTRAP-V12-FINAL)                 ==
    =============================================================================
    LIF: INFINITY | ROLE: ALPHA_INVOCATOR | RANK: SOVEREIGN

    Orchestrates the birth of the Gnostic Oracle.
    [THE CURE]: This version eradicates the "Reflection Echo" by centralizing
    provider registration within the specialized Engine factories.
    """
    boot_start_time = time.perf_counter()

    # --- MOVEMENT I: KERNEL PREPARATION ---
    # [ASCENSION 4]: WINDOWS IO STABILIZATION
    if sys.platform == "win32":
        import msvcrt
        try:
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        except Exception:
            pass

    # [ASCENSION 3]: HYPER-V METABOLIC SUPPRESSION
    gc.disable()

    # --- MOVEMENT II: ARGUMENT TRIAGE ---
    parser = argparse.ArgumentParser(description="Scaffold Gnostic Oracle")
    parser.add_argument("--root", help="The physical project anchor.")
    parser.add_argument("--verbose", action="store_true", help="Enable forensic sight.")
    args, _ = parser.parse_known_args()

    # [ASCENSION 13]: ISOMORPHIC PATH SOLVENT
    project_root = Path(args.root).resolve() if args.root else Path.cwd()
    if not project_root.exists(): project_root = Path.cwd()

    # DNA INJECTION
    os.environ["SCAFFOLD_PROJECT_ROOT"] = str(project_root).replace('\\', '/')
    if args.verbose:
        os.environ["SCAFFOLD_LOG_LEVEL"] = "DEBUG"
        os.environ["PYTHONUNBUFFERED"] = "1"

    try:
        # --- MOVEMENT III: LATE-BOUND INCEPTION (THE IMPORT WAVE) ---
        # [ASCENSION 9]: JIT SKILL AWAKENING
        from .engine import ScaffoldLSPServer
        from .lifecycle import OracleLifecycle
        from .sync import ScriptureSiphon
        from .inquest import OcularInquest
        from .relay import DaemonRelay
        from .adrenaline import AdrenalineConductor
        from .commands import CommandRouter
        from .mirror import MirrorProjector
        from .auth import SentinelGuard
        from .telemetry import OracleTelemetry
        from ..base import forensic_log

        # Feature Engines (The Brain Lobes)
        from ..scaffold_features.completion.engine import ScaffoldCompletionEngine
        from ..scaffold_features.hover.engine import ScaffoldHoverEngine
        from ..scaffold_features.definition.engine import ScaffoldDefinitionEngine
        from ..scaffold_features.symbols.engine import ScaffoldSymbolEngine
        from ..scaffold_features.code_action.engine import ScaffoldCodeActionEngine
        from ..scaffold_features.references.engine import ScaffoldReferenceEngine
        from ..scaffold_features.signature_help.engine import ScaffoldSignatureEngine
        from ..scaffold_features.inlay_hint.engine import ScaffoldInlayHintEngine
        from ..scaffold_features.inline_completion.engine import ScaffoldInlineCompletionEngine
        from ..scaffold_features.refactoring.engine import RefactoringEngine
        from ..scaffold_features.folding_range.engine import ScaffoldFoldingEngine
        from ..scaffold_features.selection_range.engine import ScaffoldSelectionRangeEngine
        from ..scaffold_features.document_link.engine import ScaffoldDocumentLinkEngine
        from ..scaffold_features.call_hierarchy.engine import ScaffoldCallHierarchyEngine
        from ..scaffold_features.type_hierarchy.engine import ScaffoldTypeHierarchyEngine

        from ..base.features.semantic_tokens.engine import SemanticTokensEngine
        from ..base.features.rename.engine import RenameEngine
        from ..base.features.workspace.engine import WorkspaceEngine
        from ..base.features.formatting.engine import FormattingEngine
        from ..base.features.diagnostics.manager import DiagnosticManager

        # Engine Core
        from ...runtime.engine import ScaffoldEngine

        # [ASCENSION 7]: IDENTITY ASSUMPTION
        try:
            import setproctitle
            setproctitle.setproctitle(f"scaffold: oracle-lsp [{project_root.name}]")
        except ImportError:
            pass

        # --- MOVEMENT IV: SOUL MATERIALIZATION ---
        # [ASCENSION 8]: SINGLETON ENGINE IGNITION
        engine = ScaffoldEngine(
            project_root=project_root,
            log_level="DEBUG" if args.verbose else "INFO",
            silent=True,
            auto_register=True
        )

        # --- MOVEMENT V: MIND MATERIALIZATION (SERVER) ---
        server = ScaffoldLSPServer(engine=engine)
        server.project_root = project_root

        # [ASCENSION 5]: FAULT-ISOLATED ORGAN GRAFTING
        # We wrap the materialization to ensure a fracture in one organ doesn't kill boot.
        try:
            server.lifecycle = OracleLifecycle(server)
            server.telemetry = OracleTelemetry(server)
            server.guard = SentinelGuard(server)
            server.adrenaline = AdrenalineConductor(server)
            server.relay = DaemonRelay(server)
            server.siphon = ScriptureSiphon(server)
            server.inquest = OcularInquest(server)
            server.mirror = MirrorProjector(server)
            server.commands = CommandRouter(server)
            server.diagnostics = DiagnosticManager(server)
        except Exception as organ_failure:
            sys.stderr.write(f"[BOOT] ⚠️ Organ Grafting Fracture: {organ_failure}\n")

        # --- MOVEMENT VI: FEATURE FORGING (THE SINGULARITY) ---
        # =========================================================================
        # [THE CURE]: SOVEREIGN DELEGATION
        # We NO LONGER manually register providers here.
        # We call the .forge() methods, which are responsible for their own
        # internal councils and deduplication.
        # =========================================================================

        server.completion = ScaffoldCompletionEngine.forge(server)
        server.hover = ScaffoldHoverEngine.forge(server)
        server.definition = ScaffoldDefinitionEngine.forge(server)
        server.symbols = ScaffoldSymbolEngine.forge(server)
        server.code_action = ScaffoldCodeActionEngine.forge(server)
        server.references = ScaffoldReferenceEngine.forge(server)
        server.signature_help = ScaffoldSignatureEngine.forge(server)
        server.inlay_hints = ScaffoldInlayHintEngine.forge(server)
        server.inline_completion = ScaffoldInlineCompletionEngine.forge(server)
        server.refactoring = RefactoringEngine.forge(server)
        server.folding_range = ScaffoldFoldingEngine.forge(server)
        server.selection_range = ScaffoldSelectionRangeEngine.forge(server)
        server.document_link = ScaffoldDocumentLinkEngine.forge(server)
        server.call_hierarchy = ScaffoldCallHierarchyEngine.forge(server)
        server.type_hierarchy = ScaffoldTypeHierarchyEngine.forge(server)

        # Agnostic Strata
        server.semantic_tokens = SemanticTokensEngine(server)
        server.rename = RenameEngine(server)
        server.workspace = WorkspaceEngine(server)
        server.formatting = FormattingEngine(server)

        # [ASCENSION 4]: CONSTITUTIONAL HANDSHAKE
        # Pre-fills the REQUEST_MAP to prevent Attribute Schisms.
        server.consecrate()

        # --- MOVEMENT VII: VITALITY IGNITION ---
        # [ASCENSION 11]: FORENSIC BOOT MARKER
        try:
            marker_dir = project_root / ".scaffold" / "debug"
            marker_dir.mkdir(parents=True, exist_ok=True)
            (marker_dir / "lsp_boot.marker").write_text(str(time.time()))
        except Exception:
            pass

        # Ignite Telemetry Heartbeat
        server.telemetry.ignite()

        # [ASCENSION 12]: THE SINGULARITY SEAL
        # The Mind is ready. Release the metabolic brakes.
        gc.collect()
        gc.enable()

        total_boot_ms = (time.perf_counter() - boot_start_time) * 1000
        forensic_log(f"Singularity Achieved. Oracle manifest in {total_boot_ms:.2f}ms.", "SUCCESS", "BOOT")

        # =========================================================================
        # == MOVEMENT VIII: THE ALPHA INVOCATION                                 ==
        # =========================================================================
        # Hand over control to the Stdio Siphon.
        server.run()

    except KeyboardInterrupt:
        sys.exit(0)

    except Exception as catastrophic_failure:
        # [ASCENSION 21]: THE FORENSIC AUTOPSY
        sys.stderr.write(f"\n[Oracle:Fatal] 💀 Ignition Fracture: {str(catastrophic_failure)}\n")
        trace = traceback.format_exc()
        sys.stderr.write(trace)
        sys.stderr.flush()

        try:
            log_root = Path(args.root).resolve() if args.root else Path.cwd()
            crash_log = log_root / ".scaffold" / "lsp_boot_death.log"
            crash_log.parent.mkdir(parents=True, exist_ok=True)
            with open(crash_log, "a", encoding="utf-8") as f:
                f.write(f"\n[{time.ctime()}] FATAL INCEPTION FRACTURE:\n{trace}\n")
        except Exception:
            pass

        sys.exit(1)


if __name__ == "__main__":
    main()

# === SCRIPTURE SEALED: THE SINGULARITY IS ACTIVE ===
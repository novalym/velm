# Path: artisans/initialize/artisan.py
# ------------------------------------
# LIF: 100x | AUTH_CODE: Ω_INITIALIZE_SINGULARITY_V12
# SYSTEM: BOOT_LOADER | ROLE: INCEPTION_AUTHORITY
# =================================================================================

import os
import sys
import time
import threading
import urllib.parse
import platform
import json
import traceback
from pathlib import Path
from typing import Any, Dict, Optional

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import InitializeRequest
from ...help_registry import register_artisan
from ...logger import Scribe
from ...core.daemon.registry.consecrator import PantheonConsecrator


@register_artisan("initialize")
class InitializeArtisan(BaseArtisan[InitializeRequest]):
    """
    =============================================================================
    == THE GATEKEEPER OF INCEPTION (V-Ω-TOTALITY-SAFEGUARDED)                  ==
    =============================================================================
    LIF: 10,000,000,000 | ROLE: HANDSHAKE_AUTHORITY

    Conducts the First Rite. Anchors the Daemon to Reality.
    Ensures the return value is ALWAYS a ScaffoldResult object.
    """

    def __init__(self, engine: Any):
        # We manually initialize to avoid property setter collisions in base class
        self.engine = engine

        # [ASCENSION 7]: LOGGER SOVEREIGNTY
        self._scribe = Scribe("InitializeArtisan")

        self._induction_active = False
        self._is_initialized = False
        self.nexus = None

    def execute(self, request: InitializeRequest) -> ScaffoldResult:
        """
        Conducts the Inception Rite. Blocks until the Reality is Stable.
        """
        # [ASCENSION 2]: IDEMPOTENCY SHIELD
        if self._is_initialized:
            self._scribe.warn("Inception Rite already manifest. Ignoring redundant plea.")
            # [THE FIX]: Return a proper ScaffoldResult
            return self.success("Already Initialized", data=self._generate_capabilities())

        # [ASCENSION 5]: TRACE INJECTION
        sys.stderr.write(f"\n[Daemon] 🟢 INCEPTION_RITE_RECEIVED. PID: {os.getpid()}\n")
        sys.stderr.flush()

        # --- MOVEMENT I: SPATIAL ANCHORING ---
        root_path = self._resolve_root(request.rootUri, request.rootPath)

        if root_path:
            # 1. ANCHOR THE ENGINE
            self.engine.project_root = str(root_path).replace('\\', '/')

            # [ASCENSION 9]: PHYSICAL ANCHORING
            try:
                os.chdir(root_path)
                self._scribe.system(f"Reality Anchored: [cyan]{root_path}[/cyan]")
            except Exception as e:
                self._scribe.error(f"Failed to anchor process to disk: {e}")

            # [ASCENSION 10]: ENVIRONMENTAL GRAFTING
            os.environ["SCAFFOLD_PROJECT_ROOT"] = str(root_path)
            os.environ["GNOSTIC_SESSION_ACTIVE"] = "1"
        else:
            self._scribe.warn("Reality Unanchored: No root path provided in handshake.")

        # --- MOVEMENT II: CONSECRATION ---

        # Late-bound Nexus Fusion
        if not self.nexus:
            self.nexus = getattr(self.engine, 'nexus', None)

        if self.nexus:
            try:
                # [ASCENSION 3]: SYNCHRONOUS CONSECRATION
                self._scribe.info("Consecrating Pantheon (Foreground Layer)...")

                # Blocks until skill map is populated
                newly_manifest = PantheonConsecrator.ignite(self.nexus)
                total_manifest = len(self.nexus.REQUEST_MAP)

                if newly_manifest > 0:
                    self._scribe.success(f"Pantheon Aligned: {newly_manifest} new skills. Total: {total_manifest}")
                else:
                    self._scribe.success(f"Pantheon Verified: {total_manifest} Rites fully operational.")

                # [ASCENSION 6]: PULSE EMISSION
                if hasattr(self.nexus, 'gatekeeper'):
                    self.nexus.logger.system("Cortex Heartbeat Verified.")

            except Exception as e:
                # [ASCENSION 11]: BOOT ERROR CAPTURE
                self._scribe.error(f"Consecration Fracture: {e}")
                self._dump_boot_error(e)
        else:
            self._scribe.warn("Nexus link not manifest. Skills may be dormant.")

        # --- MOVEMENT III: SHADOW WARMUP ---

        # [ASCENSION 4]: BACKGROUND WARMUP
        if not self._induction_active:
            self._induction_active = True
            threading.Thread(
                target=self._perform_shadow_induction,
                args=(root_path, request.clientInfo),
                name="Shadow-Induction-Worker",
                daemon=True
            ).start()

        self._is_initialized = True

        # Stabilization Breath
        time.sleep(0.05)

        # [THE FIX]: TYPE-SAFE PROCLAMATION
        # We wrap the dictionary capabilities in a proper ScaffoldResult object.
        return self.success(
            "Initialization Complete",
            data=self._generate_capabilities()
        )

    def _generate_capabilities(self) -> Dict[str, Any]:
        """
        [THE PROCLAMATION]
        Defines the laws of the Gnostic Interface for the LSP Client.
        """
        return {
            "capabilities": {
                "textDocumentSync": {
                    "openClose": True,
                    "change": 1,  # Full Sync
                    "save": {"includeText": True}
                },
                "hoverProvider": True,
                "completionProvider": {
                    "resolveProvider": True,
                    "triggerCharacters": [".", "@", "$", ":", "/", "%", "?", "!", ">", "|"]
                },
                "definitionProvider": True,
                "typeDefinitionProvider": True,
                "referencesProvider": True,
                "documentSymbolProvider": True,
                "workspaceSymbolProvider": True,
                "implementationProvider": True,
                "codeActionProvider": True,
                "executeCommandProvider": {
                    "commands": ["scaffold.applyFix", "scaffold.runRite", "scaffold.heal"]
                },
                "workspace": {
                    "workspaceFolders": {
                        "supported": True,
                        "changeNotifications": True
                    }
                }
            },
            "serverInfo": {
                "name": "Velm God-Engine",
                "version": "2.3.0-HEALED",
                "auth_code": "Ω_INIT_PURE_V12"
            }
        }

    def _resolve_root(self, root_uri: Optional[str], root_path: Optional[str]) -> Optional[Path]:
        """
        [ASCENSION 8]: PATH CANONIZATION
        Robustly resolves the project root across Windows/Linux schisms.
        """
        resolved: Optional[Path] = None

        # Strategy A: URI
        if root_uri:
            try:
                parsed = urllib.parse.urlparse(root_uri)
                path_str = urllib.parse.unquote(parsed.path)
                # Windows Fix: Remove leading slash from '/C:/Users...'
                if platform.system() == 'Windows' and path_str.startswith('/') and len(path_str) > 2 and path_str[
                    2] == ':':
                    path_str = path_str[1:]
                resolved = Path(path_str).resolve()
            except Exception:
                pass

        # Strategy B: Raw Path
        if not resolved and root_path:
            try:
                resolved = Path(root_path).resolve()
            except Exception:
                pass

        # Strategy C: CWD
        if not resolved:
            resolved = Path.cwd()

        return resolved

    def _perform_shadow_induction(self, root: Optional[Path], client_info: Optional[Dict]):
        """
        [THE RITE OF AWAKENING]
        Performed in the background to warm the cache and greet the Architect.
        """
        time.sleep(0.2)
        try:
            client_name = client_info.get("name", "Architect") if client_info else "Architect"
            self._scribe.success(f"Neural Link established with {client_name}.")

            if root and root.exists():
                # [ASCENSION 12]: MERKLE CACHE WARMING
                if hasattr(self.engine, 'surveyor'):
                    # Pre-warm surveyor cache
                    self.engine.surveyor.conduct_survey(f"file:///{str(root).replace('\\', '/')}")

                self._broadcast_window_log(f"Gnostic Engine v2.3.0 Online. Reality Anchor: {root.name}", 3)

        except Exception as e:
            self._scribe.error(f"Induction Anomaly: {e}")
        finally:
            self._induction_active = False

    def _dump_boot_error(self, error: Exception):
        """[ASCENSION 11]: THE FORENSIC SCRIPTORIUM"""
        try:
            dump = {
                "error": str(error),
                "traceback": traceback.format_exc(),
                "timestamp": time.time()
            }
            error_file = Path(".scaffold/boot_error.json")
            error_file.parent.mkdir(parents=True, exist_ok=True)
            error_file.write_text(json.dumps(dump, indent=2))
        except:
            pass

    def _broadcast_window_log(self, message: str, level: int = 3):
        """Helper to send logs back to the client via the Akashic Record."""
        try:
            if hasattr(self.engine, 'akashic'):
                self.engine.akashic.broadcast({
                    "method": "window/logMessage",
                    "params": {
                        "type": level,
                        "message": f"[Daemon] {message}"
                    }
                })
        except:
            pass
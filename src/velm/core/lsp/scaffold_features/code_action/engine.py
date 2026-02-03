# Path: core/lsp/scaffold_features/code_action/engine.py
# ------------------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ACTION_ENGINE_HYDRATED_V1

import time
import logging
import concurrent.futures
import uuid
from typing import List, Any
from ...base.features.code_action.engine import CodeActionEngine
from ...base.types import CodeAction, Diagnostic, CodeActionParams
from .providers.syntax_medic import SyntaxMedicProvider
from .providers.artisan_bridge import ArtisanBridgeProvider
from .providers.refactor_surgeon import RefactorSurgeonProvider
from .providers.neural_healer import NeuralHealerProvider

Logger = logging.getLogger("ScaffoldCodeActionEngine")


class ScaffoldCodeActionEngine(CodeActionEngine):
    """
    =============================================================================
    == THE SCAFFOLD CODE ACTION ENGINE (V-Ω-HYDRATED)                          ==
    =============================================================================
    Extends the base engine to ensure types are respected.
    """

    @staticmethod
    def forge(server: Any) -> 'ScaffoldCodeActionEngine':
        engine = ScaffoldCodeActionEngine(server)
        server.register_capability(lambda caps: setattr(caps, 'code_action_provider', {
            "codeActionKinds": ["quickfix", "refactor", "refactor.extract"]
        }))

        engine.register(SyntaxMedicProvider(server))
        engine.register(ArtisanBridgeProvider(server))
        engine.register(RefactorSurgeonProvider(server))
        engine.register(NeuralHealerProvider(server))

        return engine

    def compute(self, params: Any) -> List[CodeAction]:
        """
        [THE RITE OF DISCOVERY - HYDRATED]
        """
        # 1. EXTRACT URI & DOC (Safe Access)
        try:
            uri = str(params.text_document.uri)
        except:
            uri = str(params.get('textDocument', {}).get('uri', ''))

        doc = self.server.documents.get(uri)
        if not doc: return []

        # 2. HYDRATE DIAGNOSTICS (THE CURE)
        # The params.context.diagnostics might be a list of Dicts.
        # Providers expect List[Diagnostic] objects.
        raw_diagnostics = []
        try:
            raw_diagnostics = params.context.diagnostics
        except:
            raw_diagnostics = params.get('context', {}).get('diagnostics', [])

        hydrated_diagnostics = []
        for d in raw_diagnostics:
            try:
                if isinstance(d, dict):
                    hydrated_diagnostics.append(Diagnostic.model_validate(d))
                else:
                    hydrated_diagnostics.append(d)
            except:
                pass

        # 3. DISPATCH
        # We manually invoke providers here to control the arguments precisely
        all_actions = []
        target_range = params.range if hasattr(params, 'range') else None

        # If range is missing or dict, try to hydrate (Base engine handles this, but let's be safe)

        for provider in self.providers:
            try:
                actions = provider.provide_actions(doc, target_range, hydrated_diagnostics)
                if actions:
                    all_actions.extend(actions)
            except Exception as e:
                Logger.error(f"Provider {provider.name} fractured: {e}")

        return all_actions
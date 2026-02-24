# artisans/dream/agentic_limb/reflex/phalanxes.py
# -----------------------------------------------
"""
=================================================================================
== THE INTENT PHALANX (V-Ω-UNIVERSAL-ROUTER-STRICT-TYPED)                      ==
=================================================================================
@gnosis:title IntentPhalanx
@gnosis:summary The command center. It maps the purified LexicalIntent to the
                exact Pydantic vessel required by the God-Engine.
@gnosis:LIF INFINITY

[THE CURE]: Ascended to support absolute static typing. The `Literal` heresy
is annihilated via explicit type casting.
=================================================================================
"""
from typing import Optional, Literal, cast
from .....interfaces.requests import (
    RefactorRequest, WeaveRequest, LintRequest, AnalyzeRequest,
    TranslocateRequest, SaveRequest, HistoryRequest, TreeRequest,
    GraphRequest, RunRequest, CloudRequest, IdentityRequest,
    AdoptRequest, VerifyRequest, GuiRequest, BaseRequest
)
from .tokenizer import LexicalIntent

# --- THE GNOSTIC TYPE ANCHORS ---
CloudProviderLiteral = Literal["aws", "oracle", "hetzner", "azure", "docker", "local", "ovh"]


class IntentPhalanx:

    @staticmethod
    def route(intent: LexicalIntent) -> Optional[BaseRequest]:
        """Routes the purified intent to the correct Request Vessel."""
        if not intent.primary_action or intent.confidence < 0.75:
            return None

        # Inject willed flags globally
        base_flags = intent.flags
        action = intent.primary_action

        # Helpers for safe extraction
        first_path = intent.target_paths[0] if intent.target_paths else None
        first_noun = intent.target_nouns[0] if intent.target_nouns else None
        first_quote = intent.target_quotes[0] if intent.target_quotes else None

        # --- I. ARCHITECTURAL TRANSMUTATION ---
        if action == "refactor":
            target = first_path or "scaffold.scaffold"
            return RefactorRequest(blueprint_path=target, **base_flags)

        elif action == "weave":
            target = first_noun or first_quote
            if target: return WeaveRequest(fragment_name=target, **base_flags)

        elif action == "create":
            # Let the Neural Prophet handle complex creations unless it's explicitly quoted
            if first_quote:
                # Fallback to general RunRequest for custom commands
                return RunRequest(target=first_quote, **base_flags)
            return None

        # --- II. ADJUDICATION & HEALING ---
        elif action == "lint":
            target = first_path or "."
            if "secur" in intent.raw_text.lower() or "audit" in intent.raw_text.lower():
                return AnalyzeRequest(path_to_scripture=target, semantic_depth="full", **base_flags)
            return LintRequest(target_paths=[target], fix=True, **base_flags)

        elif action == "verify":
            target = first_path or "."
            return VerifyRequest(target_path=target, fix_suggestions=True, **base_flags)

        # --- III. KINETIC MUTATION ---
        elif action == "move":
            if len(intent.target_paths) >= 2:
                return TranslocateRequest(paths=[intent.target_paths[0], intent.target_paths[1]], **base_flags)

        elif action == "delete":
            # Too dangerous to reflex without paths
            if first_path:
                return RunRequest(target=f"rm -rf {first_path}", **base_flags)

        # --- IV. CHRONOLOGY & STATE ---
        elif action == "undo":
            return HistoryRequest(command="undo", **base_flags)

        elif action == "save":
            msg = first_quote or " ".join(intent.target_nouns) or "Checkpoint willed by Architect"
            return SaveRequest(intent=msg, **base_flags)

        elif action == "adopt":
            target = first_path or "."
            return AdoptRequest(target_path=target, **base_flags)

        # --- V. PERCEPTION & VISUALIZATION ---
        elif action == "tree":
            return TreeRequest(depth=2, **base_flags)

        elif action == "graph":
            return GraphRequest(**base_flags)

        elif action == "distill":
            target = first_path or "."
            return AnalyzeRequest(path_to_scripture=target, semantic_depth="structure", **base_flags)

        # --- VI. EXECUTION ---
        elif action == "run":
            cmd = first_quote or " ".join(intent.target_nouns)
            if not cmd: cmd = "pytest"  # Default heuristic fallback
            return RunRequest(target=cmd, **base_flags)

        # --- VII. CLOUD & IDENTITY ---
        elif action == "cloud":
            # [ASCENSION]: The Strict Type Transmutation
            cloud_provider: CloudProviderLiteral = "ovh"
            raw = intent.raw_text.lower()
            for prov in ["aws", "azure", "hetzner", "ovh", "docker", "local", "oracle"]:
                if prov in raw:
                    # We cast the raw string to the sacred Literal to appease the Static Inquisitor
                    cloud_provider = cast(CloudProviderLiteral, prov)

            return CloudRequest(command="provision", provider=cloud_provider, **base_flags)

        elif action == "identity":
            # [ASCENSION]: The Strict Identity Transmutation
            id_provider: str = "ovh"
            raw = intent.raw_text.lower()
            if "whoami" in raw or "status" in raw:
                return IdentityRequest(action="whoami", provider="ovh", **base_flags)

            for prov in ["aws", "azure", "hetzner", "ovh"]:
                if prov in raw:
                    id_provider = prov

            return IdentityRequest(action="handshake", provider=id_provider, **base_flags)

        # --- VIII. USER INTERFACE ---
        elif action == "gui":
            return GuiRequest(**base_flags)

        return None
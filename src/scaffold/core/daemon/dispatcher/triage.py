# Path: core/daemon/dispatcher/triage.py
# --------------------------------------
import re
import difflib
from functools import lru_cache
from typing import Dict, Type, Any, Tuple, Optional, List
from pydantic import ValidationError

from .constants import FAST_RITES
from ....interfaces.requests import BaseRequest
from ....logger import Scribe

Logger = Scribe("TriageOfficer")


class TriageOfficer:
    """
    =================================================================================
    == THE TRIAGE OFFICER (V-Ω-FUZZY-LOGIC-ASCENDED)                               ==
    =================================================================================
    @gnosis:title The Triage Officer
    @gnosis:summary The Gatekeeper of Intent. Validates, Normalizes, and Enriches.
    @gnosis:LIF 10,000,000,000

    The Triage Officer stands between the Raw JSON Stream and the Gnostic Logic.
    It ensures that only pure, validated Truth enters the execution pipeline.
    """

    def __init__(self, request_map: Dict[str, Type[BaseRequest]]):
        self.request_map = request_map
        # Pre-compute keys for fuzzy matching speed
        self._known_keys = list(request_map.keys())

    @lru_cache(maxsize=128)
    def normalize_command(self, raw_command: str) -> str:
        """
        [ASCENSION 3]: MEMOIZED NORMALIZATION.
        Strips LSP prefixes and sanitizes input.
        Cached for O(1) lookups on repeated calls.
        """
        if not raw_command:
            return "unknown"

        # [ASCENSION 8]: SAFETY SANITIZATION
        # Remove null bytes and non-printable chars
        clean = re.sub(r'[\x00-\x1f\x7f]', '', str(raw_command))

        # [ASCENSION 7]: NAMESPACE STRIPPING
        # 'textDocument/hover' -> 'hover'
        # 'scaffold/shadow' -> 'shadow'
        if '/' in clean:
            return clean.split('/')[-1]

        return clean

    def validate(self,
                 command: str,
                 params: Dict[str, Any],
                 context: Dict[str, Any]) -> Tuple[Optional[BaseRequest], bool]:
        """
        [THE GRAND RITE OF INSPECTION]

        Returns:
            (RequestObject, IsFastLane)
            If RequestObject is None, the rite is unknown.
        """
        # [ASCENSION 12]: THE VOID GUARD
        if not command:
            return None, False

        # 1. LOOKUP (THE RESOLUTION)
        RequestClass = self._resolve_request_class(command)

        if not RequestClass:
            # [ASCENSION 1]: GRACEFUL UNKNOWN HANDLING
            # Instead of crashing, we analyze the unknown.
            self._analyze_unknown(command)
            return None, False

        # 2. ENRICHMENT (THE GRAFT)
        # [ASCENSION 4]: CONTEXTUAL GRAFTING
        # We inject environmental DNA (Root, Trace) into the params if missing.
        final_params = params.copy()

        if "project_root" not in final_params and context.get("active_root"):
            final_params["project_root"] = str(context["active_root"])

        if "metadata" not in final_params:
            final_params["metadata"] = {}

        # [ASCENSION 7]: TRACE ID GRAFTING
        if context.get("trace_id") and "trace_id" not in final_params["metadata"]:
            final_params["metadata"]["trace_id"] = context["trace_id"]

        # 3. VALIDATION (THE TEST)
        try:
            # [ASCENSION 5]: TYPE ALCHEMY (Implicit in Pydantic V2)
            request_obj = RequestClass.model_validate(final_params)

        except ValidationError as ve:
            # [ASCENSION 6]: SCHEMA FORENSICS
            # We log exactly why it failed to help the Architect debug.
            error_details = self._format_validation_error(ve)
            Logger.error(f"Schema Heresy in '{command}': {error_details}")
            raise ve

        # 4. CLASSIFICATION (THE SPEED)
        is_fast = command in FAST_RITES

        return request_obj, is_fast

    def _resolve_request_class(self, command: str) -> Optional[Type[BaseRequest]]:
        """
        [ASCENSION 9]: ALIASING ENGINE
        Finds the Request Class, checking direct matches and aliases.
        """
        # 1. Direct Match
        if command in self.request_map:
            return self.request_map[command]

        # 2. Normalized Match (e.g., 'scaffold/analyze' matches 'analyze')
        # This handles cases where the map has 'analyze' but client sends 'scaffold/analyze'
        # or vice versa.
        for key, cls in self.request_map.items():
            if key.split('/')[-1] == command:
                return cls

        return None

    def _analyze_unknown(self, command: str):
        """
        [ASCENSION 2]: FUZZY PROPHECY
        If a command is unknown, we look for siblings in the Grimoire.
        """
        matches = difflib.get_close_matches(command, self._known_keys, n=1, cutoff=0.7)
        if matches:
            Logger.warn(f"Unknown Rite '{command}'. Did you mean '{matches[0]}'?")
        else:
            Logger.warn(f"Unknown Rite '{command}'. No similar rites found in Grimoire.")

    def _format_validation_error(self, ve: ValidationError) -> str:
        """
        [ASCENSION 6]: FORENSIC REPORTING
        Formats Pydantic errors into human-readable strings.
        """
        errors = []
        for e in ve.errors():
            loc = ".".join(str(l) for l in e['loc'])
            msg = e['msg']
            errors.append(f"{loc}: {msg}")
        return " | ".join(errors)

    def get_rite_schema(self, command: str) -> Optional[Dict[str, Any]]:
        """
        [ASCENSION 10]: INTROSPECTION HOOK
        Returns the JSON Schema for a given command. Used by `help` artisan.
        """
        cls = self._resolve_request_class(command)
        if cls:
            return cls.model_json_schema()
        return None


# Path: src/velm/core/runtime/vessels.py
# -----------------------------------------------------------------------------------------
# == THE GNOSTIC SOVEREIGN MATRIX (V-Ω-TOTALITY-V400.0-SINGULARITY-FINALIS)             ==
# =========================================================================================
# LIF: INFINITY | ROLE: RESILIENT_DATA_SUBSTRATE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SOVEREIGN_MATRIX_V400_PYDANTIC_HEALED_)(@)(!@#(#@)
# =========================================================================================

import json
import math
from typing import Any, Dict, Optional, Iterable

# --- PYDANTIC CORE UPLINKS ---
# We use these to teach Pydantic how to perceive our Sovereign soul.
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler


class GnosticSovereignDict(dict):
    """
    =================================================================================
    == THE GNOSTIC SOVEREIGN MATRIX                                                ==
    =================================================================================
    LIF: ∞ | The Unbreakable Vessel of Intent.

    A transcendent dictionary subclass that implements Recursive Voiding and
    Pydantic V2 Core Integration. It is the final cure for the 'NoneType' heresy.
    """

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        [THE CURE]: This method tells Pydantic V2 that this class should be
        treated as a dict during validation, but instantiated as a
        GnosticSovereignDict. This annihilates the 'non-annotated attribute' error.
        """
        return core_schema.dict_schema(
            keys_schema=core_schema.any_schema(),
            values_schema=core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: dict(x),
                return_schema=core_schema.dict_schema()
            ),
            cls=cls
        )

    def __init__(self, *args, **kwargs):
        """[THE RITE OF INCEPTION]: Ingests matter and forges the Shadow Map."""
        # 1. Standard Dictionary Inception
        if args and isinstance(args[0], dict):
            processed_args = [
                {k: self._enshrine_matter(v) for k, v in args[0].items()}
            ]
            super().__init__(*processed_args)
        else:
            super().__init__(*args, **kwargs)
            for k, v in self.items():
                self[k] = self._enshrine_matter(v)

        # 2. Forge the Case-Insensitive Resonance Map
        self._shadow_map: Dict[str, Any] = {
            str(k).lower(): k for k in self.keys()
        }

    def __getitem__(self, key: Any) -> Any:
        """The Rite of Retrieval. Warded against absence across infinite depth."""
        if key in self:
            return super().__getitem__(key)

        if isinstance(key, str):
            lower_key = key.lower()
            if lower_key in self._shadow_map:
                return super().__getitem__(self._shadow_map[lower_key])

        return GnosticSovereignDict()

    def _enshrine_matter(self, val: Any) -> Any:
        """Transmutes raw matter into Sovereign matter."""
        if val is None:
            return GnosticSovereignDict()
        if isinstance(val, dict) and not isinstance(val, GnosticSovereignDict):
            return GnosticSovereignDict(val)
        if isinstance(val, list):
            return [self._enshrine_matter(i) for i in val]
        return val

    def __getattr__(self, name: str) -> Any:
        """Maps dot-notation to the Sovereign internal map."""
        if name.startswith('__'):
            return super().__getattribute__(name)
        return self[name]

    # --- THE TRUTH & APPEARANCE PROTOCOLS ---

    def __bool__(self) -> bool:
        """The Law of Identity: A Void is False."""
        return len(self.keys()) > 0

    def __str__(self) -> str:
        """The Law of Appearance: A Void is Invisible."""
        if not self: return ""
        return json.dumps(self.model_dump(), indent=2)

    def __repr__(self) -> str:
        if not self: return "[GNOSTIC_VOID]"
        return f"<GnosticSovereignDict: {super().__repr__()}>"

    def __iter__(self) -> Iterable:
        """Prevents iteration heresies on missing variables."""
        if not self: return iter([])
        return super().__iter__()

    def __len__(self) -> int:
        return super().__len__()

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Transmutes back to raw matter for serialization."""
        return {k: (v.model_dump() if isinstance(v, GnosticSovereignDict) else v)
                for k, v in self.items()}

    def get(self, key: Any, default: Any = "") -> Any:
        """Resilient implementation of .get()"""
        val = self[key]
        if isinstance(val, GnosticSovereignDict) and not val:
            return default
        return val

# == SCRIPTURE SEALED: THE DATA SUBSTRATE HAS ACHIEVED SINGULARITY ==
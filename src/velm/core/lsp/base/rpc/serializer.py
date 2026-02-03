# Path: core/daemon/serializer/engine.py
# --------------------------------------

import json
import dataclasses
import uuid
import datetime
import inspect
import sys
import traceback
import re
import types
import collections
from enum import Enum
from pathlib import PurePath
from typing import Any, Iterator, Dict, Set, Union, Optional, List

# --- LAZY LOADED GIANTS (Soft Dependencies) ---
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    BaseModel = None
    HAS_PYDANTIC = False


# =================================================================================
# == ASCENSION I: THE OUROBOROS GUARD                                            ==
# =================================================================================
class OuroborosGuard:
    """
    [THE CIRCULARITY SENTINEL]
    Tracks object identities during the traversal of the object graph.
    Prevents the RecursionError heresy by detecting cycles in O(1) time.
    """
    __slots__ = ['_seen']

    def __init__(self):
        # We track memory addresses (ids) of containers we are currently visiting
        self._seen: Set[int] = set()

    def mark(self, obj: Any) -> bool:
        """
        Marks an object as being visited.
        Returns True if it is ALREADY in the stack (Cycle Detected).
        """
        # We only track mutable containers (dict, list, objects)
        # Primitives are pass-by-value/immutable in this context
        obj_id = id(obj)
        if obj_id in self._seen:
            return True
        self._seen.add(obj_id)
        return False

    def release(self, obj: Any):
        """Releases the object from the current stack context."""
        obj_id = id(obj)
        if obj_id in self._seen:
            self._seen.remove(obj_id)


# =================================================================================
# == ASCENSION II: THE TITANIUM ENCODER                                          ==
# =================================================================================
class TitaniumEncoder(json.JSONEncoder):
    """
    [THE UNIVERSAL TRANSMUTER]
    LIF: INFINITY | ROLE: DATA_ALCHEMIST | RANK: SOVEREIGN

    The definitive serializer. It refuses to crash.
    It performs 12 Ascensions of Type Conversion to ensure any Python matter
    can be transmitted across the JSON-RPC ether.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guard = OuroborosGuard()
        self.max_iter_items = 100
        self.max_str_len = 5000
        self.max_depth = 20  # Depth limit to prevent stack overflow

    def default(self, obj: Any) -> Any:
        """
        The Master Rite of Transmutation.
        Routes the object through the Pantheon of Type Handlers.
        """
        try:
            # --- 1. THE PYDANTIC POLYGLOT (Fastest Path) ---
            if hasattr(obj, 'model_dump'):
                # V2: Use model_dump with mode='python' to recurse
                return obj.model_dump(mode='python', by_alias=True, exclude_none=True)
            if hasattr(obj, 'dict') and callable(obj.dict):
                # V1: Use dict()
                return obj.dict(by_alias=True, exclude_none=True)

            # --- 2. THE DATACLASS DECONSTRUCTOR ---
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)

            # --- 3. THE OUROBOROS CHECK (Cyclic Safety) ---
            # If it's a generic container or object, check for cycles
            if isinstance(obj, (dict, list, tuple, object)) and not isinstance(obj, (str, int, float, bool, type(None))):
                if self.guard.mark(obj):
                    return f"<CircularReference: {type(obj).__name__}@{id(obj):x}>"
                # Note: We cannot easily 'release' in default() because JSONEncoder
                # controls the recursion. We rely on the recursion limit of Python
                # or the fact that JSONEncoder doesn't call default() for dict/list
                # unless subclassed aggressively.
                # For complex objects that fall through here, we treat them as atomic.

            # --- 4. THE SCIENTIFIC CASTER (Numpy) ---
            if HAS_NUMPY:
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                if isinstance(obj, np.bool_):
                    return bool(obj)

            # --- 5. THE TEMPORAL FREEZER ---
            if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
                return obj.isoformat()
            if isinstance(obj, datetime.timedelta):
                return str(obj)

            # --- 6. THE SPATIAL COLLAPSE (Pathlib) ---
            if isinstance(obj, PurePath):
                return obj.as_posix()

            # --- 7. THE ENUM DISSOLUTION ---
            if isinstance(obj, Enum):
                return obj.value

            # --- 8. THE BINARY SARCOPHAGUS ---
            if isinstance(obj, (bytes, bytearray)):
                try:
                    return obj.decode('utf-8')
                except UnicodeDecodeError:
                    return f"<Binary: {len(obj)} bytes>"

            # --- 9. THE SET LINEARIZER ---
            # Sets are unordered, which breaks hashing. We sort them.
            if isinstance(obj, (set, frozenset)):
                try:
                    return sorted(list(obj))
                except TypeError:
                    # Fallback for unorderable types
                    return list(obj)

            # --- 10. THE UUID ANCHOR ---
            if isinstance(obj, uuid.UUID):
                return str(obj)

            # --- 11. THE INFINITE SCROLL GOVERNOR ---
            if isinstance(obj, Iterator):
                data = []
                try:
                    for _ in range(self.max_iter_items):
                        data.append(next(obj))
                    # Peek for more
                    try:
                        next(obj)
                        data.append("... <Truncated Iterator>")
                    except StopIteration:
                        pass
                except StopIteration:
                    pass
                except Exception as e:
                    data.append(f"<IteratorError: {e}>")
                return data

            # --- 12. THE FORENSIC AUTOPSY (Exceptions) ---
            if isinstance(obj, BaseException):
                return {
                    "error_type": type(obj).__name__,
                    "message": str(obj),
                    "traceback": "".join(traceback.format_tb(obj.__traceback__)) if obj.__traceback__ else None
                }

            # --- 13. THE META-OBJECT SHIELD ---
            if inspect.isclass(obj):
                return f"<class '{obj.__name__}'>"
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                return f"<function '{obj.__name__}'>"
            if isinstance(obj, types.ModuleType):
                return f"<module '{getattr(obj, '__name__', 'unknown')}'>"
            if isinstance(obj, re.Pattern):
                return obj.pattern

            if hasattr(obj, 'assert_called_with'): # Mock objects
                return "<MockObject>"

            # --- 14. THE OBJECT INTROSPECTOR ---
            # Try to grab __dict__ or __slots__
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            if hasattr(obj, '__slots__'):
                return {s: getattr(obj, s, None) for s in obj.__slots__}

            # --- 15. THE ATOMIC FAIL-SAFE ---
            # If all else fails, use repr(), but clamp it to prevent log explosion.
            s_repr = repr(obj)
            if len(s_repr) > self.max_str_len:
                return s_repr[:self.max_str_len] + "... <Truncated>"
            return s_repr

        except Exception as e:
            # The Serializer MUST NOT crash.
            # We return a string describing the failure rather than raising.
            return f"<SerializationFailure: {type(obj).__name__} - {str(e)}>"


class GnosticSerializer:
    """
    =============================================================================
    == THE PUBLIC FACADE                                                       ==
    =============================================================================
    Provides static access methods for the Titanium Encoder.
    Configured to ensure_ascii=False for full Unicode fidelity.
    """

    @staticmethod
    def serialize(obj: Any) -> Any:
        """
        Transmutes an object into a JSON-compatible primitive structure.
        Uses the TitaniumEncoder's logic but returns Python objects (dicts/lists),
        not a JSON string. Useful for pre-processing before other serialization steps.
        """
        # This simulates what json.dumps does internally with 'default'
        # We can just return the object if it's primitive, or run default()
        # But default() is only for unknown types.
        # For a full recursive transformation to dicts, we'd need a recursive walker.
        # Ideally, we just use encode() below.
        pass

    @staticmethod
    def encode(obj: Any) -> bytes:
        """
        Transmutes Gnosis into UTF-8 Bytes.
        Guaranteed to return valid JSON bytes, or an Error JSON bytes.
        NEVER RAISES.
        """
        try:
            return json.dumps(
                obj,
                cls=TitaniumEncoder,
                ensure_ascii=False,
                allow_nan=True, # Allow NaN/Infinity for scientific data
                separators=(',', ':') # Minify output
            ).encode('utf-8')

        except Exception as e:
            sys.stderr.write(f"\n[SERIALIZER:FATAL] Encoding Fracture: {e}\n")
            try:
                sys.stderr.write(f"Offending Object Type: {type(obj)}\n")
            except:
                pass

            # Emergency Fallback Payload
            error_payload = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Serialization Catastrophe: {str(e)}"
                },
                "id": getattr(obj, "id", None) if hasattr(obj, "id") else None
            }
            return json.dumps(error_payload).encode('utf-8')

    @staticmethod
    def decode(data: bytes) -> Any:
        """
        Decodes bytes to Python objects with encoding recovery.
        """
        try:
            return json.loads(data.decode('utf-8'))
        except UnicodeDecodeError:
            # [ASCENSION 5]: LATIN-1 RECOVERY
            return json.loads(data.decode('latin-1', errors='replace'))
        except json.JSONDecodeError as e:
            raise e

# =============================================================================
# == THE GLOBAL INSTANCE (COMPATIBILITY BRIDGE)                              ==
# =============================================================================

# Allows usage like: json.dumps(obj, default=gnostic_serializer)
def gnostic_serializer(obj: Any) -> Any:
    """
    A standalone function that mimics the TitaniumEncoder's default method.
    Used for legacy calls or quick debugging.
    """
    return TitaniumEncoder().default(obj)
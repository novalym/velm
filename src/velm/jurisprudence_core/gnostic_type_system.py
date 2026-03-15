# Path: src/velm/jurisprudence_core/gnostic_type_system.py
# --------------------------------------------------------
import unicodedata
import ast
import re
import uuid
import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional, Set, Union


# =========================================================================
# == STRATUM 0: THE ONTOLOGICAL HERESY (FORENSIC TRACING)                ==
# =========================================================================

class OntologicalHeresy(ValueError):
    """
    [ASCENSION 16]: CAUSAL TRACE TOMOGRAPHY
    A transcendent ValueError that tracks exactly *where* in a deeply nested
    data structure the physical laws of the contract were broken.
    """

    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message
        super().__init__(f"Lattice Fracture at [{path}]: {message}")


def adjudicate_gnostic_purity(value: Any, rule_string: str) -> Tuple[bool, Optional[str]]:
    """The Universal Adjudicator."""
    if not rule_string: return True, None
    try:
        gnostic_type = GnosticTypeParser.parse(rule_string)
        gnostic_type.validate(value, "root", {})
        return True, None
    except OntologicalHeresy as e:
        return False, str(e)
    except Exception as e:
        return False, f"A meta-heresy occurred during type adjudication: {e}"


# =========================================================================
# == STRATUM 1: THE BASE CONTRACT OF REALITY                             ==
# =========================================================================

class TypeNode(ABC):
    """The Ancestral Soul of all Gnostic Types."""

    def __init__(self, constraints: Dict[str, Any] = None):
        self.constraints = constraints or {}

    @abstractmethod
    def validate(self, value: Any, path: str, contracts: Dict[str, Any]) -> Any:
        """Adjudicates the value. Returns pure matter or raises OntologicalHeresy."""
        pass

    @abstractmethod
    def to_json_schema(self, contracts: Dict[str, Any]) -> Dict[str, Any]:
        """Transmutes the Type into OpenAI-compatible JSON Schema."""
        pass

    def _check_numeric_constraints(self, value: Union[int, float], path: str):
        c = self.constraints
        if 'min' in c and value < c['min']:
            raise OntologicalHeresy(path, f"Value {value} violates minimum floor of {c['min']}.")
        if 'max' in c and value > c['max']:
            raise OntologicalHeresy(path, f"Value {value} violates maximum ceiling of {c['max']}.")

    def _check_length_constraints(self, value: Any, path: str):
        c = self.constraints
        length = len(value)
        if 'min_len' in c and length < c['min_len']:
            raise OntologicalHeresy(path, f"Length {length} violates minimum boundary of {c['min_len']}.")
        if 'max_len' in c and length > c['max_len']:
            raise OntologicalHeresy(path, f"Length {length} violates maximum boundary of {c['max_len']}.")


# =========================================================================
# == STRATUM 2: THE PRIMORDIAL ATOMS                                     ==
# =========================================================================

class AnyType(TypeNode):
    """The Void. Accepts all matter."""

    def validate(self, value: Any, path: str, contracts: Dict) -> Any: return value

    def to_json_schema(self, contracts: Dict) -> Dict: return {}


class StringType(TypeNode):
    """
    =================================================================================
    == THE OMEGA STRING TYPE: TOTALITY (V-Ω-TOTALITY-VMAX-INFINTY-ASCENDED)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TEXTUAL_REALITY_WARDEN | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_STRING_VMAX_TOTALITY_2026_FINALIS

    The supreme authority for textual matter. It has been hyper-revolved to
    possess 'NoneType Evaporation' and 'Amnesty Gating', ensuring that
    the project's soul is never shattered by a void.
    =================================================================================
    """

    def validate(self, value: Any, path: str, contracts: Dict[str, Any]) -> str:
        """
        =============================================================================
        == THE RITE OF TEXTUAL PURIFICATION (VALIDATE)                             ==
        =============================================================================
        """
        # =========================================================================
        # == [ASCENSION 1]: NONETYPE EVAPORATION (THE MASTER CURE)               ==
        # =========================================================================
        # If the value is a Void (None), we righteously evaporate it into a string.
        # This is the definitive cure for the L215/L221 Schism.
        if value is None:
            return ""

        # =========================================================================
        # == [ASCENSION 2]: LINGUISTIC AMNESTY (REDACTION SHIELD)                ==
        # =========================================================================
        # If the matter has already been warded by the Secret Sieve, we stay the
        # hand of further audit to prevent false-positive entropy alerts.
        if isinstance(value, str) and value.startswith("[REDACTED_"):
            return value

        # =========================================================================
        # == [ASCENSION 5]: APOPHATIC PRIMITIVE ALCHEMY                          ==
        # =========================================================================
        # If the soul is a primitive (Int, Float, Bool), we transmute it to text.
        # Otherwise, we raise an Ontological Heresy.
        if not isinstance(value, str):
            if isinstance(value, (int, float, bool)):
                value = str(value)
            else:
                raise OntologicalHeresy(
                    path=path,
                    message=f"Ontological Error: Expected String, perceived {type(value).__name__}."
                )

        # =========================================================================
        # == [ASCENSION 3 & 4]: THE RITE OF LUSTRATION (UNICODE PURITY)          ==
        # =========================================================================
        # 1. Normalize to Canonical Form C (NFC)
        purified_matter = unicodedata.normalize('NFC', value)

        # 2. Annihilate Zero-Width toxins and control characters
        # [THE CURE]: Uses a non-greedy regex sieve.
        purified_matter = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff]', '', purified_matter)

        # 3. [ASCENSION 9]: EOL Harmonization
        purified_matter = purified_matter.replace('\r\n', '\n').replace('\r', '\n')

        # =========================================================================
        # == [ASCENSION 6]: GEOMETRIC BOUNDARY VALIDATION                        ==
        # =========================================================================
        # Check willed constraints (min_len, max_len)
        self._check_length_constraints(purified_matter, path)

        # =========================================================================
        # == [ASCENSION 11]: TEMPLATE GAZE DETECTION                            ==
        # =========================================================================
        # If the string contains sigils, we tag it for alchemical awareness.
        if "{{" in purified_matter or "{%" in purified_matter:
            # (Prophecy: Framework for JIT-triggering the Alchemist from within types)
            pass

        # [ASCENSION 24]: THE FINALITY VOW
        return purified_matter

    def to_json_schema(self, contracts: Dict[str, Any]) -> Dict[str, Any]:
        """[THE REVELATION]: Transmutes the Word into an Ocular JSON Schema."""
        schema = {"type": "string"}

        if 'min_len' in self.constraints: schema["minLength"] = self.constraints['min_len']
        if 'max_len' in self.constraints: schema["maxLength"] = self.constraints['max_len']
        if 'pattern' in self.constraints: schema["pattern"] = self.constraints['pattern']

        return schema

    def __repr__(self) -> str:
        return "<Ω_STRING_TYPE status=RESONANT mode=TOTALITY>"


class IntegerType(TypeNode):
    def validate(self, value: Any, path: str, contracts: Dict) -> int:
        if isinstance(value, bool): raise OntologicalHeresy(path, "Expected Integer, perceived Boolean.")
        if isinstance(value, str) and value.lstrip('-').isdigit(): value = int(value)
        if not isinstance(value, int): raise OntologicalHeresy(path,
                                                               f"Expected Integer, perceived {type(value).__name__}.")
        self._check_numeric_constraints(value, path)
        return value

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "integer"}


class FloatType(TypeNode):
    def validate(self, value: Any, path: str, contracts: Dict) -> float:
        if isinstance(value, bool): raise OntologicalHeresy(path, "Expected Float, perceived Boolean.")
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise OntologicalHeresy(path, f"Expected Float, perceived {type(value).__name__}.")
        self._check_numeric_constraints(value, path)
        return value

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "number"}


class BoolType(TypeNode):
    def validate(self, value: Any, path: str, contracts: Dict) -> bool:
        if isinstance(value, bool): return value
        if isinstance(value, str):
            v_low = value.lower()
            if v_low in ('true', 'yes', 'on', '1'): return True
            if v_low in ('false', 'no', 'off', '0'): return False
        if isinstance(value, int) and value in (0, 1): return bool(value)
        raise OntologicalHeresy(path, f"Expected Boolean, perceived {type(value).__name__}.")

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "boolean"}


# =========================================================================
# == STRATUM 3: THE OMNISCIENT DOMAINS (THE ASCENSIONS)                  ==
# =========================================================================

class LiteralType(TypeNode):
    """[ASCENSION 3]: Absolute Enumeration."""

    def __init__(self, allowed_values: List[Any]):
        super().__init__()
        self.allowed_values = allowed_values

    def validate(self, value: Any, path: str, contracts: Dict) -> Any:
        if value not in self.allowed_values:
            raise OntologicalHeresy(path, f"Value '{value}' is profane. Must be one of: {self.allowed_values}")
        return value

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"enum": self.allowed_values}


class RegexType(TypeNode):
    """[ASCENSION 11]: Regex Wards."""

    def __init__(self, pattern: str):
        super().__init__()
        self.pattern_str = pattern
        self.pattern = re.compile(pattern)

    def validate(self, value: Any, path: str, contracts: Dict) -> str:
        val = StringType().validate(value, path, contracts)
        if not self.pattern.match(val):
            raise OntologicalHeresy(path, f"Value '{val}' breaches cryptographic ward '{self.pattern_str}'.")
        return val

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "string", "pattern": self.pattern_str}


class ByteSizeType(TypeNode):
    """[ASCENSION 8]: Metabolic Mass Coercion."""

    def validate(self, value: Any, path: str, contracts: Dict) -> int:
        if isinstance(value, int): return value
        val_str = StringType().validate(value, path, contracts).upper().strip()
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGTPE]?B?)$', val_str)
        if not match: raise OntologicalHeresy(path, f"Invalid byte mass geometry: '{value}'")
        num, unit = float(match.group(1)), match.group(2)
        multiplier = {"B": 1, "KB": 1024, "K": 1024, "MB": 1024 ** 2, "M": 1024 ** 2, "GB": 1024 ** 3, "G": 1024 ** 3,
                      "TB": 1024 ** 4, "T": 1024 ** 4}
        return int(num * multiplier.get(unit, 1))

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "string", "description": "Byte size (e.g. '10MB', '5G')"}


class ExistingFileType(TypeNode):
    """[ASCENSION 1]: Physical Substrate Validation."""

    def validate(self, value: Any, path: str, contracts: Dict) -> str:
        val = StringType().validate(value, path, contracts)
        if not Path(val).is_file():
            raise OntologicalHeresy(path, f"Physical Illusion: File '{val}' is unmanifest on the substrate.")
        return val

    def to_json_schema(self, contracts: Dict) -> Dict: return {"type": "string", "format": "file-path"}


class ExistingDirType(TypeNode):
    """[ASCENSION 1]: Physical Substrate Validation."""

    def validate(self, value: Any, path: str, contracts: Dict) -> str:
        val = StringType().validate(value, path, contracts)
        if not Path(val).is_dir():
            raise OntologicalHeresy(path, f"Physical Illusion: Sanctum (Dir) '{val}' is unmanifest.")
        return val

    def to_json_schema(self, contracts: Dict) -> Dict: return {"type": "string", "format": "dir-path"}


class SecretType(TypeNode):
    """[ASCENSION 7]: The Secret Veil."""

    def __init__(self, inner: TypeNode):
        super().__init__()
        self.inner = inner

    def validate(self, value: Any, path: str, contracts: Dict) -> Any:
        # Validates normally, but logic downstream knows to cloak it.
        return self.inner.validate(value, path, contracts)

    def to_json_schema(self, contracts: Dict) -> Dict:
        schema = self.inner.to_json_schema(contracts)
        schema["writeOnly"] = True
        return schema


# --- STANDARD DOMAINS ---
class EmailType(RegexType):
    def __init__(self): super().__init__(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    def to_json_schema(self, contracts: Dict) -> Dict: return {"type": "string", "format": "email"}


class UUIDType(TypeNode):
    def validate(self, value: Any, path: str, contracts: Dict) -> str:
        try:
            return str(uuid.UUID(str(value)))
        except ValueError:
            raise OntologicalHeresy(path, f"'{value}' is not a true UUID.")

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "string", "format": "uuid"}


class SemVerType(RegexType):
    def __init__(self): super().__init__(
        r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-zA-Z0-9-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-zA-Z0-9-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')


class PortType(IntegerType):
    def validate(self, value: Any, path: str, contracts: Dict) -> int:
        val = super().validate(value, path, contracts)
        if not (1 <= val <= 65535): raise OntologicalHeresy(path, f"Port {val} is out of geometric bounds (1-65535).")
        return val


# =========================================================================
# == STRATUM 4: THE STRUCTURAL LATTICES (COMPLEX TYPES)                  ==
# =========================================================================

class ListType(TypeNode):
    def __init__(self, item_type: TypeNode, constraints: Dict = None):
        super().__init__(constraints)
        self.item_type = item_type

    def validate(self, value: Any, path: str, contracts: Dict) -> List[Any]:
        if not isinstance(value, list): raise OntologicalHeresy(path,
                                                                f"Expected List, perceived {type(value).__name__}.")
        self._check_length_constraints(value, path)
        return [self.item_type.validate(item, f"{path}[{i}]", contracts) for i, item in enumerate(value)]

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "array", "items": self.item_type.to_json_schema(contracts)}


class TupleType(TypeNode):
    """[ASCENSION 10]: Tuple Geometry."""

    def __init__(self, item_types: List[TypeNode]):
        super().__init__()
        self.item_types = item_types

    def validate(self, value: Any, path: str, contracts: Dict) -> Tuple:
        if not isinstance(value, (list, tuple)): raise OntologicalHeresy(path,
                                                                         f"Expected Tuple/List, perceived {type(value).__name__}.")
        if len(value) != len(self.item_types):
            raise OntologicalHeresy(path,
                                    f"Tuple dimension mismatch. Expected {len(self.item_types)}, perceived {len(value)}.")

        return tuple(t.validate(v, f"{path}[{i}]", contracts) for i, (t, v) in enumerate(zip(self.item_types, value)))

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {
            "type": "array",
            "prefixItems": [t.to_json_schema(contracts) for t in self.item_types],
            "items": False  # No additional items allowed
        }


class DictType(TypeNode):
    def __init__(self, key_type: TypeNode, val_type: TypeNode, constraints: Dict = None):
        super().__init__(constraints)
        self.key_type = key_type
        self.val_type = val_type

    def validate(self, value: Any, path: str, contracts: Dict) -> Dict[Any, Any]:
        if not isinstance(value, dict): raise OntologicalHeresy(path,
                                                                f"Expected Dict, perceived {type(value).__name__}.")
        self._check_length_constraints(value, path)
        return {
            self.key_type.validate(k, f"{path}.<key({k})>", contracts): self.val_type.validate(v, f"{path}.{k}",
                                                                                               contracts)
            for k, v in value.items()
        }

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"type": "object", "additionalProperties": self.val_type.to_json_schema(contracts)}


class UnionType(TypeNode):
    def __init__(self, types: List[TypeNode]):
        super().__init__()
        self.types = types

    def validate(self, value: Any, path: str, contracts: Dict) -> Any:
        errors = []
        for t in self.types:
            try:
                return t.validate(value, path, contracts)
            except OntologicalHeresy as e:
                errors.append(e.message)

        raise OntologicalHeresy(path, f"Matter '{value}' failed Multiversal Union. Schisms: {' | '.join(errors)}")

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"anyOf": [t.to_json_schema(contracts) for t in self.types]}


class IntersectionType(TypeNode):
    """[ASCENSION 9]: Metaprogramming Intersection."""

    def __init__(self, types: List[TypeNode]):
        super().__init__()
        self.types = types

    def validate(self, value: Any, path: str, contracts: Dict) -> Any:
        # Value must pass ALL types. We return the result of the last validation.
        # (Useful for combining InlineRecordTypes)
        final_val = value
        for t in self.types:
            final_val = t.validate(final_val, path, contracts)
        return final_val

    def to_json_schema(self, contracts: Dict) -> Dict:
        return {"allOf": [t.to_json_schema(contracts) for t in self.types]}


class OptionalType(TypeNode):
    """[ASCENSION 15]: The Null-Coalescing Guardian."""

    def __init__(self, inner_type: TypeNode):
        super().__init__()
        self.inner_type = inner_type

    def validate(self, value: Any, path: str, contracts: Dict) -> Any:
        if value is None or value == "": return None
        return self.inner_type.validate(value, path, contracts)

    def to_json_schema(self, contracts: Dict) -> Dict:
        schema = self.inner_type.to_json_schema(contracts)
        if isinstance(schema.get("type"), str):
            schema["type"] = [schema["type"], "null"]
        return schema


class InlineRecordType(TypeNode):
    """[ASCENSION 12]: Inline Anonymous Structs."""

    def __init__(self, fields: Dict[str, TypeNode]):
        super().__init__()
        self.fields = fields

    def validate(self, value: Any, path: str, contracts: Dict) -> Dict[str, Any]:
        if not isinstance(value, dict): raise OntologicalHeresy(path,
                                                                f"Expected Inline Struct (Dict), perceived {type(value).__name__}.")

        validated = {}
        for fname, ftype in self.fields.items():
            if fname in value:
                validated[fname] = ftype.validate(value[fname], f"{path}.{fname}", contracts)
            elif not isinstance(ftype, OptionalType):
                raise OntologicalHeresy(path, f"Inline Struct is missing critical atom: '{fname}'")
        return validated

    def to_json_schema(self, contracts: Dict) -> Dict:
        props = {k: v.to_json_schema(contracts) for k, v in self.fields.items()}
        required = [k for k, v in self.fields.items() if not isinstance(v, OptionalType)]
        return {"type": "object", "properties": props, "required": required}


class ContractRefType(TypeNode):
    """The Sovereign Domain Ward."""

    def __init__(self, contract_name: str):
        super().__init__()
        self.contract_name = contract_name

    def validate(self, value: Any, path: str, contracts: Dict) -> Any:
        if self.contract_name not in contracts:
            # Duck-Typing Bypass if contract unmanifest
            return value

        if not isinstance(value, dict):
            raise OntologicalHeresy(path,
                                    f"Contract '{self.contract_name}' demands an Object, perceived {type(value).__name__}.")

        contract = contracts[self.contract_name]
        validated_obj = {}
        all_fields = contract.get_all_fields(contracts)

        for field_name, field_def in all_fields.items():
            if field_name in value:
                validated_obj[field_name] = field_def.gnostic_type.validate(
                    value[field_name], f"{path}.{field_name}", contracts
                )
            elif not field_def.is_optional and field_def.default_value is None:
                raise OntologicalHeresy(path,
                                        f"Contract '{self.contract_name}' demands the presence of atom '{field_name}'.")
            elif field_def.default_value is not None:
                validated_obj[field_name] = field_def.default_value

        return validated_obj

    def to_json_schema(self, contracts: Dict) -> Dict:
        if self.contract_name not in contracts: return {}
        contract = contracts[self.contract_name]
        all_fields = contract.get_all_fields(contracts)

        props = {}
        required = []
        for name, f_def in all_fields.items():
            props[name] = f_def.gnostic_type.to_json_schema(contracts)
            if f_def.doc: props[name]["description"] = f_def.doc
            if not f_def.is_optional and f_def.default_value is None:
                required.append(name)

        return {"type": "object", "properties": props, "required": required, "title": self.contract_name}


class PrimitiveType(TypeNode):
    """
    =================================================================================
    == THE PRIMITIVE ALCHEMIST: TOTALITY (V-Ω-TOTALITY-VMAX-COERCION-FINALIS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ATOMIC_TRANSFIGURATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_PRIMITIVE_VMAX_TOTALITY_2026_FINALIS

    The supreme authority for the four primordial laws of matter (str, int, float,
    bool). It righteously transfigures substrate noise into logical certainty.
    =================================================================================
    """

    def __init__(self, name: str):
        super().__init__()
        self.name = name.lower()

    def validate(self, value: Any, path: str, contracts: Dict[str, Any]) -> Any:
        """
        =============================================================================
        == THE RITE OF ATOMIC ADJUDICATION (VALIDATE)                              ==
        =============================================================================
        """
        if self.name == 'any':
            return value

        # =========================================================================
        # == STRATUM 1: THE STRING RITE (THE WORD)                               ==
        # =========================================================================
        if self.name == 'str':
            # [ASCENSION 1]: NONETYPE EVAPORATION
            if value is None:
                return ""

            # [ASCENSION 5]: DELEGATION TO THE LEXICAL WARDEN
            # This ensures we benefit from Redaction Amnesty and Unicode Purity.
            return StringType(self.constraints).validate(value, path, contracts)

        # =========================================================================
        # == STRATUM 2: THE INTEGER RITE (THE COUNT)                             ==
        # =========================================================================
        if self.name == 'int':
            # [ASCENSION 1]: VOID EVAPORATION
            if value is None:
                return 0

            # [ASCENSION 2]: APOPHATIC PURITY
            # We strictly forbid booleans from masquerading as integers.
            if isinstance(value, bool):
                raise OntologicalHeresy(path, "Geometric Error: Boolean cannot masquerade as Integer.")

            # [ASCENSION 4]: HYDRAULIC COERCION
            if isinstance(value, str):
                clean_val = value.strip().replace(',', '')
                if clean_val.lstrip('-').isdigit():
                    value = int(clean_val)
                else:
                    # Fallback check for float-strings being willed as ints
                    try:
                        f_val = float(clean_val)
                        if f_val.is_integer():
                            value = int(f_val)
                    except ValueError:
                        pass

            if not isinstance(value, int):
                raise OntologicalHeresy(
                    path=path,
                    message=f"Ontological Error: Expected Integer, perceived {type(value).__name__}."
                )

            # [ASCENSION 6]: BOUNDARY ADJUDICATION
            self._check_numeric_constraints(value, path)
            return value

        # =========================================================================
        # == STRATUM 3: THE FLOAT RITE (THE MEASURE)                             ==
        # =========================================================================
        if self.name == 'float':
            # [ASCENSION 1]: VOID EVAPORATION
            if value is None:
                return 0.0

            # [ASCENSION 2]: APOPHATIC PURITY
            if isinstance(value, bool):
                raise OntologicalHeresy(path, "Geometric Error: Boolean cannot masquerade as Float.")

            try:
                # [ASCENSION 4]: HYDRAULIC COERCION
                # Handles strings, ints, and scientific notation
                clean_val = str(value).strip().replace(',', '')
                final_val = float(clean_val)
            except (ValueError, TypeError):
                raise OntologicalHeresy(
                    path=path,
                    message=f"Ontological Error: Expected Float, perceived {type(value).__name__}."
                )

            # [ASCENSION 6]: BOUNDARY ADJUDICATION
            self._check_numeric_constraints(final_val, path)
            return final_val

        # =========================================================================
        # == STRATUM 4: THE BOOLEAN RITE (THE TRUTH)                             ==
        # =========================================================================
        if self.name == 'bool':
            # [ASCENSION 1]: VOID EVAPORATION
            if value is None:
                return False

            if isinstance(value, bool):
                return value

            # =====================================================================
            # == [ASCENSION 3]: THE ALCHMIST'S THAW (MULTI-DIALECT)               ==
            # =====================================================================
            if isinstance(value, (str, int)):
                v_str = str(value).lower().strip()

                # The Trinity of Resonance (Truthy)
                if v_str in ('true', 'yes', 'on', '1', 'resonant', 'pure', 'manifest'):
                    return True

                # The Trinity of Fracture (Falsy)
                if v_str in ('false', 'no', 'off', '0', 'fractured', 'void', 'none', ''):
                    return False

            raise OntologicalHeresy(
                path=path,
                message=f"Ontological Error: Matter '{value}' cannot be thawed into Boolean Truth."
            )

        raise ValueError(f"Jurisprudence Failure: Unknown primitive law '{self.name}'.")

    def to_json_schema(self, contracts: Dict[str, Any]) -> Dict[str, Any]:
        """[THE REVELATION]: Transmutes the Law into an Ocular JSON Schema."""
        mapping = {
            'str': 'string',
            'int': 'integer',
            'float': 'number',
            'bool': 'boolean',
            'any': {}
        }
        schema = {"type": mapping.get(self.name, "string")}

        # Inscribe constraints if manifest
        if self.name in ('int', 'float'):
            if 'min' in self.constraints: schema["minimum"] = self.constraints['min']
            if 'max' in self.constraints: schema["maximum"] = self.constraints['max']

        return schema

    def __repr__(self) -> str:
        return f"<Ω_PRIMITIVE_TYPE law={self.name} status=RESONANT>"


class PathType(StringType):
    """
    =================================================================================
    == THE GEOMETRIC COMPASS (V-Ω-TOTALITY-V6-SPATIAL-WARD)                        ==
    =================================================================================
    LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SOVEREIGN

    Enforces the Laws of Spacetime on strings. It righteously normalizes
    backslashes into Gnostic forward-slashes and ensures absolute containment
    within the willed reality.
    """

    def validate(self, value: Any, path: str, contracts: Dict) -> str:
        # First, ensure it is a valid string
        val_str = super().validate(value, path, contracts)

        # [ASCENSION 10]: Achronal Normalization
        clean_path = val_str.replace('\\', '/')
        p = Path(clean_path)

        # [ASCENSION 24]: The Absolute Path Ward
        if self.constraints.get('absolute') and not p.is_absolute():
            raise OntologicalHeresy(path, f"Geometric Violation: Path '{val_str}' must be absolute.")

        # [ASCENSION 25]: The Relative Path Ward
        if self.constraints.get('relative') and p.is_absolute():
            raise OntologicalHeresy(path, f"Geometric Violation: Path '{val_str}' must be relative.")

        return clean_path

    def to_json_schema(self, contracts: Dict) -> Dict:
        schema = super().to_json_schema(contracts)
        schema["format"] = "path"
        if self.constraints.get('absolute'): schema["description"] = "Absolute filesystem path"
        return schema



# =========================================================================
# == STRATUM 5: THE RECURSIVE DESCENT PARSER (THE BRAIN)                 ==
# =========================================================================

class GnosticTypeParser:
    """
    =================================================================================
    == THE GNOSTIC TYPE PARSER (V-Ω-TOTALITY-V100000-RECURSIVE-DESCENT)            ==
    =================================================================================
    LIF: ∞ | ROLE: SCHEMA_DECONSTRUCTOR | RANK: OMEGA_SOVEREIGN

    Transmutes string declarations like `Dict[str, List[User]?] | {ip: IPv4}` into
    an immutable tree of `TypeNode` objects. Completely immune to Ouroboros Loops.
    """

    PRIMITIVES = {'str', 'int', 'float', 'bool', 'any'}
    DOMAINS = {
        'email': EmailType, 'uuid': UUIDType, 'path': PathType,
        'bytesize': ByteSizeType, 'semver': SemVerType, 'port': PortType,
        'existingfile': ExistingFileType, 'existingdir': ExistingDirType
    }

    @classmethod
    def parse(cls, type_str: str) -> TypeNode:
        """The Public Gateway to type parsing."""
        if not type_str: return AnyType()

        try:
            # We use ast.parse to leverage Python's flawless tokenizer.
            # [ASCENSION 22]: Handles Dict/Tuple slicing elegantly.
            node = ast.parse(type_str.strip(), mode='eval').body
            return cls._visit(node, depth=0)
        except SyntaxError as e:
            # Fallback for simple space-separated strings or bad syntax
            raise ValueError(f"Lexical Type Fracture: '{type_str}' cannot be perceived as a contract. {e.msg}")

    @classmethod
    def _visit(cls, node: ast.AST, depth: int) -> TypeNode:
        # [ASCENSION 23]: The Ouroboros Depth Guard
        if depth > 50: raise ValueError("Type declaration exceeds maximum recursion depth of 50.")

        # 1. Primitives & Domain Types: "str", "Email"
        if isinstance(node, ast.Name):
            return cls._resolve_name(node.id)

        # 2. Constraints: "int(min=1)"
        if isinstance(node, ast.Call):
            base_type = cls._visit(node.func, depth + 1)
            constraints = {}
            for kw in node.keywords:
                try:
                    constraints[kw.arg] = ast.literal_eval(kw.value)
                except:
                    pass

            # Handle Literal("a", "b")
            if isinstance(base_type, LiteralType):
                opts = []
                for arg in node.args:
                    try:
                        opts.append(ast.literal_eval(arg))
                    except:
                        pass
                return LiteralType(opts)

            # Handle Regex(r"...")
            if isinstance(base_type, RegexType):
                if node.args:
                    try:
                        return RegexType(ast.literal_eval(node.args[0]))
                    except:
                        pass

            base_type.constraints = constraints
            return base_type

        # 3. Generics: "List[str]"
        if isinstance(node, ast.Subscript):
            base_id = node.value.id if isinstance(node.value, ast.Name) else ""
            slice_node = getattr(node.slice, 'value', node.slice)  # Python 3.8/3.9 compat

            if base_id in ('List', 'list', 'Set', 'set'):
                return ListType(cls._visit(slice_node, depth + 1))

            if base_id in ('Dict', 'dict'):
                if isinstance(slice_node, ast.Tuple) and len(slice_node.elts) == 2:
                    return DictType(cls._visit(slice_node.elts[0], depth + 1),
                                    cls._visit(slice_node.elts[1], depth + 1))
                return DictType(StringType(), AnyType())

            if base_id in ('Tuple', 'tuple'):
                if isinstance(slice_node, ast.Tuple):
                    return TupleType([cls._visit(e, depth + 1) for e in slice_node.elts])
                return TupleType([cls._visit(slice_node, depth + 1)])

            if base_id == 'Optional':
                return OptionalType(cls._visit(slice_node, depth + 1))

            if base_id == 'Secret':
                return SecretType(cls._visit(slice_node, depth + 1))

            if base_id == 'Literal':
                if isinstance(slice_node, ast.Tuple):
                    opts = [ast.literal_eval(e) for e in slice_node.elts]
                else:
                    opts = [ast.literal_eval(slice_node)]
                return LiteralType(opts)

        # 4. Unions: "str | int"
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            left = cls._visit(node.left, depth + 1)
            right = cls._visit(node.right, depth + 1)

            # Flatten
            types = []
            if isinstance(left, UnionType):
                types.extend(left.types)
            else:
                types.append(left)
            if isinstance(right, UnionType):
                types.extend(right.types)
            else:
                types.append(right)
            return UnionType(types)

        # 5. Intersections: "A & B"
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitAnd):
            return IntersectionType([cls._visit(node.left, depth + 1), cls._visit(node.right, depth + 1)])

        # 6. Inline Records: {"name": str, "age": int}
        if isinstance(node, ast.Dict):
            fields = {}
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant):
                    fields[k.value] = cls._visit(v, depth + 1)
                elif isinstance(k, ast.Str):  # Python 3.7
                    fields[k.s] = cls._visit(v, depth + 1)
            return InlineRecordType(fields)

        # Fallback for Constants (None)
        if isinstance(node, ast.Constant) and node.value is None:
            return AnyType()

        return AnyType()

    @classmethod
    def _resolve_name(cls, name: str) -> TypeNode:
        """Resolves a raw name string into its Gnostic Entity."""
        n = name.lower()

        # Primitives
        if n in cls.PRIMITIVES: return PrimitiveType(n)
        if n == 'string': return PrimitiveType('str')
        if n == 'integer': return PrimitiveType('int')
        if n == 'number': return PrimitiveType('float')
        if n == 'boolean': return PrimitiveType('bool')

        # Domains
        if n in cls.DOMAINS: return cls.DOMAINS[n]()

        # Keywords acting as Type classes
        if n == 'literal': return LiteralType([])
        if n == 'regex': return RegexType(".*")

        # Custom Contract Reference
        return ContractRefType(name)
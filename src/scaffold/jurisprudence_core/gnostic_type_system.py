# Path: scaffold/jurisprudence_core/gnostic_type_system.py
# --------------------------------------------------------

import ast
import re
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional


def adjudicate_gnostic_purity(value: str, rule_string: str) -> Tuple[bool, Optional[str]]:
    """
    The one true, universal adjudicator. It receives a value and a scripture of laws
    and returns a judgment of its purity.
    """
    if not rule_string:
        return True, None

    # This logic, which was once in jurisprudence.py, now lives here in its rightful home.
    try:
        # We use a simplified context for this validation rite.
        # The 'validate' filter itself is what calls this.
        gnostic_type = GnosticTypeParser.parse(rule_string)
        gnostic_type.validate(value, "value", {})
        return True, None
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"A meta-heresy occurred during adjudication: {e}"


# --- THE BASE CONTRACT ---

class GnosticType(ABC):
    """
    The Abstract Soul of a Type.
    """

    def __init__(self, constraints: Dict[str, Any] = None):
        self.constraints = constraints or {}

    @abstractmethod
    def validate(self, value: Any, context: str, contract_registry: Dict[str, Any]) -> Any:
        """
        Adjudicates the value. Returns the cleaned value or raises ValueError.
        'contract_registry' allows recursive lookup of other Contracts.
        """
        pass

    def _check_constraints(self, value: Any, context: str):
        """Universal constraint logic (min, max)."""
        c = self.constraints
        if 'min' in c:
            if isinstance(value, (int, float)):
                if value < c['min']: raise ValueError(f"{context} is too small (min {c['min']}).")
            elif hasattr(value, '__len__'):
                if len(value) < c['min']: raise ValueError(f"{context} is too short (min len {c['min']}).")

        if 'max' in c:
            if isinstance(value, (int, float)):
                if value > c['max']: raise ValueError(f"{context} is too large (max {c['max']}).")
            elif hasattr(value, '__len__'):
                if len(value) > c['max']: raise ValueError(f"{context} is too long (max len {c['max']}).")


# --- THE PRIMITIVES ---

class AnyType(GnosticType):
    def validate(self, value: Any, context: str, registry: Dict) -> Any:
        return value


class StringType(GnosticType):
    def validate(self, value: Any, context: str, registry: Dict) -> str:
        if not isinstance(value, str): raise ValueError(f"{context} must be a string.")
        self._check_constraints(value, context)
        if 'pattern' in self.constraints:
            if not re.match(self.constraints['pattern'], value):
                raise ValueError(f"{context} does not match pattern '{self.constraints['pattern']}'.")
        return value


class IntegerType(GnosticType):
    def validate(self, value: Any, context: str, registry: Dict) -> int:
        if isinstance(value, bool): raise ValueError(f"{context} must be an integer, not bool.")
        if not isinstance(value, int): raise ValueError(f"{context} must be an integer.")
        self._check_constraints(value, context)
        return value


class FloatType(GnosticType):
    def validate(self, value: Any, context: str, registry: Dict) -> float:
        if isinstance(value, bool): raise ValueError(f"{context} must be a float.")
        if not isinstance(value, (float, int)): raise ValueError(f"{context} must be a number.")
        self._check_constraints(value, context)
        return float(value)


class BoolType(GnosticType):
    def validate(self, value: Any, context: str, registry: Dict) -> bool:
        if not isinstance(value, bool): raise ValueError(f"{context} must be a boolean.")
        return value


# --- THE SEMANTIC TYPES ---

class EmailType(StringType):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    def validate(self, value: Any, context: str, registry: Dict) -> str:
        val = super().validate(value, context, registry)
        if not self.EMAIL_REGEX.match(val): raise ValueError(f"{context} is not a valid email.")
        return val


class UUIDType(StringType):
    def validate(self, value: Any, context: str, registry: Dict) -> str:
        val = super().validate(value, context, registry)
        try:
            uuid.UUID(val)
        except ValueError:
            raise ValueError(f"{context} is not a valid UUID.")
        return val


class PathType(StringType):
    def validate(self, value: Any, context: str, registry: Dict) -> str:
        val = super().validate(value, context, registry)
        p = Path(val)
        if self.constraints.get('absolute') and not p.is_absolute():
            raise ValueError(f"{context} must be an absolute path.")
        return val


class EnumType(GnosticType):
    def validate(self, value: Any, context: str, registry: Dict) -> Any:
        options = self.constraints.get('options', [])
        if value not in options:
            raise ValueError(f"{context} must be one of: {options}")
        return value


# --- THE HIGHER ORDER TYPES (THE SINGULARITY) ---

class ListType(GnosticType):
    def __init__(self, item_type: GnosticType, constraints: Dict = None):
        super().__init__(constraints)
        self.item_type = item_type

    def validate(self, value: Any, context: str, registry: Dict) -> List[Any]:
        if not isinstance(value, list): raise ValueError(f"{context} must be a list.")
        self._check_constraints(value, context)
        return [self.item_type.validate(item, f"{context}[{i}]", registry) for i, item in enumerate(value)]


class DictType(GnosticType):
    def __init__(self, key_type: GnosticType, value_type: GnosticType, constraints: Dict = None):
        super().__init__(constraints)
        self.key_type = key_type
        self.value_type = value_type

    def validate(self, value: Any, context: str, registry: Dict) -> Dict[Any, Any]:
        if not isinstance(value, dict): raise ValueError(f"{context} must be a dict.")
        self._check_constraints(value, context)
        validated = {}
        for k, v in value.items():
            vk = self.key_type.validate(k, f"{context}.key({k})", registry)
            vv = self.value_type.validate(v, f"{context}[{k}]", registry)
            validated[vk] = vv
        return validated


class UnionType(GnosticType):
    def __init__(self, types: List[GnosticType]):
        super().__init__()
        self.types = types

    def validate(self, value: Any, context: str, registry: Dict) -> Any:
        errors = []
        for t in self.types:
            try:
                return t.validate(value, context, registry)
            except ValueError as e:
                errors.append(str(e))

        raise ValueError(f"{context} failed Union check. Mismatches: {'; '.join(errors)}")


class ContractRefType(GnosticType):
    def __init__(self, contract_name: str):
        super().__init__()
        self.contract_name = contract_name

    def validate(self, value: Any, context: str, registry: Dict) -> Any:
        if self.contract_name not in registry:
            raise ValueError(f"Contract '{self.contract_name}' is not defined.")

        # Recursive Call to the Registry
        contract = registry[self.contract_name]
        # We rely on the Contract object's own validate method (defined below or externally)
        # Since GnosticContract is in data_contracts, we do a manual validation here
        # to avoid circular imports, or we move GnosticContract logic here.
        # For purity, we assume value is a dict and validate fields.

        if not isinstance(value, dict):
            raise ValueError(f"{context} must be an object honoring '{self.contract_name}'.")

        # Validate Fields
        for field_name, field_def in contract.fields.items():
            if field_name not in value:
                if field_def.is_optional or field_def.default_value is not None:
                    continue
                raise ValueError(f"Missing required field '{field_name}' in {context} ({self.contract_name}).")

            # The field_def.type_instance is a GnosticType!
            field_def.gnostic_type.validate(value[field_name], f"{context}.{field_name}", registry)

        return value


class OptionalType(GnosticType):
    def __init__(self, inner_type: GnosticType):
        super().__init__()
        self.inner_type = inner_type

    def validate(self, value: Any, context: str, registry: Dict) -> Any:
        if value is None: return None
        return self.inner_type.validate(value, context, registry)


# --- THE AST PARSER (THE BRAIN) ---

class GnosticTypeParser:
    """
    Translates Python type strings ("List[str]", "int(min=1)") into GnosticType objects.
    """

    @classmethod
    def parse(cls, type_str: str) -> GnosticType:
        try:
            # We use ast.parse in 'eval' mode to handle nested structures
            node = ast.parse(type_str, mode='eval').body
            return cls._visit(node)
        except Exception as e:
            # Fallback for simple strings that AST might dislike if they look like keywords?
            # Actually AST handles most things well.
            raise ValueError(f"Invalid type signature '{type_str}': {e}")

    @classmethod
    def _visit(cls, node) -> GnosticType:
        # 1. Basic Types: "str", "int"
        if isinstance(node, ast.Name):
            return cls._resolve_primitive(node.id)

        # 2. Constraints: "int(min=1)"
        if isinstance(node, ast.Call):
            base_type = cls._visit(node.func)
            constraints = {}
            for kw in node.keywords:
                try:
                    constraints[kw.arg] = ast.literal_eval(kw.value)
                except:
                    pass  # Logic for complex constraint values if needed

            # Handle Enum positional args: enum("a", "b")
            if isinstance(base_type, EnumType):
                opts = []
                for arg in node.args:
                    try:
                        opts.append(ast.literal_eval(arg))
                    except:
                        pass
                constraints['options'] = opts

            base_type.constraints = constraints
            return base_type

        # 3. Generics: "List[str]"
        if isinstance(node, ast.Subscript):
            base_id = node.value.id if isinstance(node.value, ast.Name) else ""

            if base_id in ('List', 'list', 'Set', 'set'):
                inner = cls._visit(node.slice)
                return ListType(inner)

            if base_id in ('Dict', 'dict'):
                # Dicts in AST often come as Tuple in slice if multiple args?
                # e.g. Dict[str, int] -> slice is Tuple
                if isinstance(node.slice, ast.Tuple):
                    key_t = cls._visit(node.slice.elts[0])
                    val_t = cls._visit(node.slice.elts[1])
                    return DictType(key_t, val_t)
                else:
                    # Fallback Dict[str, Any]
                    return DictType(StringType(), AnyType())

            if base_id == 'Optional':
                inner = cls._visit(node.slice)
                return OptionalType(inner)

        # 4. Unions: "str | int"
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
            left = cls._visit(node.left)
            right = cls._visit(node.right)
            # Flatten unions if recursive
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

        # Fallback for Constants (None)
        if isinstance(node, ast.Constant) and node.value is None:
            return AnyType()  # NoneType

        return AnyType()

    @staticmethod
    def _resolve_primitive(name: str) -> GnosticType:
        n = name.lower()

        # --- Standard Types ---
        if n in ('str', 'string', 'text'): return StringType()
        if n in ('int', 'integer'): return IntegerType()
        if n in ('float', 'number'): return FloatType()
        if n in ('bool', 'boolean'): return BoolType()
        if n == 'uuid': return UUIDType()
        if n == 'email': return EmailType()
        if n == 'path': return PathType()
        if n == 'enum': return EnumType()
        if n == 'any': return AnyType()

        # --- ★★★ THE LEGACY SHORTHANDS (THE FIX) ★★★ ---
        # We map these legacy validator names to concrete StringTypes with patterns.

        if n == 'var_path_safe':
            # Alphanumeric, underscores, hyphens, dots. No spaces or slashes.
            return StringType(constraints={'pattern': r'^[a-zA-Z0-9_.-]+$'})

        if n == 'slug':
            # Lowercase alphanumeric and hyphens.
            return StringType(constraints={'pattern': r'^[a-z0-9-]+$'})

        if n == 'snake':
            # Lowercase alphanumeric and underscores.
            return StringType(constraints={'pattern': r'^[a-z0-9_]+$'})

        if n == 'pascal':
            # PascalCase
            return StringType(constraints={'pattern': r'^[A-Z][a-zA-Z0-9]*$'})

        # --- Unknown -> Assume Contract Reference ---
        return ContractRefType(name)
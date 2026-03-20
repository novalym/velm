# Path: core/alchemist/elara/resolver/engine/prism.py
# ---------------------------------------------------

import json
from typing import Dict, Any, Final, Optional, Tuple, Set

# --- THE DIVINE UPLINKS ---
from ......jurisprudence_core.gnostic_type_system import (
    TypeNode, PrimitiveType, OptionalType, ListType, DictType, AnyType
)
from ......contracts.data_contracts import GnosticContract
from ......logger import Scribe

Logger = Scribe("PolyglotPrism")


class PolyglotPrism:
    """
    =================================================================================
    == THE POLYGLOT PRISM: OMEGA POINT (V-Ω-TOTALITY-VMAX-ROSETTA-MATRIX)          ==
    =================================================================================
    LIF: 50,000x | ROLE: MULTIVERSAL_TYPE_CASTER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_PRISM_VMAX_ROSETTA_MATRIX_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for cross-dimensional type casting. This
    organ takes a pure `GnosticContract` (Language-Agnostic Schema) and collapses
    its wavefunction into production-grade syntax for Python (Pydantic V2),
    TypeScript (Interfaces), Zod (Validation), and Rust (Structs).

    It is the heart of the Isomorphic Polyglot Matrix, mathematically annihilating
    the "Babel Fracture."
    =================================================================================
    """

    # [ASCENSION 1]: The Type Sieve
    # Maps Gnostic primitives to their substrate-specific incarnations.
    _TYPE_MAP: Final[Dict[str, Dict[str, str]]] = {
        "python": {
            "str": "str", "int": "int", "float": "float", "bool": "bool",
            "UUID": "UUID", "datetime": "datetime", "SecretStr": "SecretStr",
            "EmailStr": "EmailStr", "Any": "Any"
        },
        "typescript": {
            "str": "string", "int": "number", "float": "number", "bool": "boolean",
            "UUID": "string", "datetime": "string", "SecretStr": "string",
            "EmailStr": "string", "Any": "any"
        },
        "zod": {
            "str": "z.string()", "int": "z.number().int()", "float": "z.number()",
            "bool": "z.boolean()", "UUID": "z.string().uuid()", "datetime": "z.coerce.date()",
            "SecretStr": "z.string()", "EmailStr": "z.string().email()", "Any": "z.any()"
        },
        "rust": {
            "str": "String", "int": "i64", "float": "f64", "bool": "bool",
            "UUID": "uuid::Uuid", "datetime": "chrono::DateTime<chrono::Utc>",
            "SecretStr": "secrecy::SecretString", "EmailStr": "String", "Any": "serde_json::Value"
        }
    }

    @classmethod
    def emit_class(cls, contract: GnosticContract, language: str) -> str:
        """
        =========================================================================
        == THE RITE OF THE ROSETTA CAST (EMIT_CLASS)                           ==
        =========================================================================
        Transmutes a GnosticContract into the willed substrate language.
        """
        lang = str(language).lower()

        if lang == "python" or lang == "pydantic":
            return cls._emit_python_pydantic(contract)
        elif lang in ("typescript", "ts"):
            return cls._emit_typescript_interface(contract)
        elif lang == "zod":
            return cls._emit_zod_schema(contract)
        elif lang == "rust":
            return cls._emit_rust_struct(contract)
        elif lang == "go":
            return cls._emit_go_struct(contract)

        return f"/* UNKNOWN_PRISM_TONGUE: {lang} */"

    # =========================================================================
    # == STRATUM I: PYTHON (PYDANTIC V2)                                     ==
    # =========================================================================
    @classmethod
    def _emit_python_pydantic(cls, contract: GnosticContract) -> str:
        lines = []
        imports = {"from pydantic import BaseModel, Field"}

        # Determine Heritage
        base_class = contract.parent if contract.parent else "BaseModel"

        lines.append(f"class {contract.name}({base_class}):")
        if contract.fields:
            if any(f.doc for f in contract.fields.values()):
                lines.append('    """Forged via ELARA Polyglot Prism."""')

            for f_name, field in contract.fields.items():
                py_type, req_imports = cls._resolve_type(field.gnostic_type, "python")
                imports.update(req_imports)

                # Apply Modifiers
                if field.is_optional:
                    py_type = f"Optional[{py_type}]"
                    imports.add("from typing import Optional")

                # Forge Field Definition
                field_args = []
                if field.default_value is not None:
                    # Handle string formatting for defaults
                    if isinstance(field.default_value, str):
                        field_args.append(f'default="{field.default_value}"')
                    else:
                        field_args.append(f'default={field.default_value}')
                elif not field.is_optional:
                    field_args.append("...")  # Ellipsis for required
                else:
                    field_args.append("default=None")

                if field.doc:
                    field_args.append(f'description="{field.doc}"')

                if "secret" in field.gnostic_type.constraints or field.gnostic_type.name == "SecretStr":
                    field_args.append('repr=False')

                field_def = f"Field({', '.join(field_args)})" if field_args else ""
                lines.append(f"    {f_name}: {py_type} = {field_def}")
        else:
            lines.append("    pass")

        # Prepend required imports
        import_block = "\n".join(sorted(list(imports)))
        return f"{import_block}\n\n" + "\n".join(lines)

    # =========================================================================
    # == STRATUM II: TYPESCRIPT & ZOD                                        ==
    # =========================================================================
    @classmethod
    def _emit_typescript_interface(cls, contract: GnosticContract) -> str:
        lines = []

        extends_clause = f" extends {contract.parent}" if contract.parent else ""
        lines.append(f"export interface {contract.name}{extends_clause} {{")

        for f_name, field in contract.fields.items():
            ts_type, _ = cls._resolve_type(field.gnostic_type, "typescript")

            # Optional Marker
            opt_marker = "?" if field.is_optional else ""

            if field.doc:
                lines.append(f"  /** {field.doc} */")

            # Readonly modifier
            prefix = "readonly " if "readonly" in field.gnostic_type.constraints else ""

            lines.append(f"  {prefix}{f_name}{opt_marker}: {ts_type};")

        lines.append("}")
        return "\n".join(lines)

    @classmethod
    def _emit_zod_schema(cls, contract: GnosticContract) -> str:
        lines = []
        lines.append("import { z } from 'zod';\n")

        base_obj = f"z.object({{"
        if contract.parent:
            # If inheriting, we assume the parent schema is imported and we merge
            base_obj = f"{contract.parent}Schema.extend({{"

        lines.append(f"export const {contract.name}Schema = {base_obj}")

        for f_name, field in contract.fields.items():
            zod_chain, _ = cls._resolve_type(field.gnostic_type, "zod")

            if field.doc:
                zod_chain += f'.describe("{field.doc}")'

            if field.is_optional:
                zod_chain += ".optional()"

            if field.default_value is not None:
                if isinstance(field.default_value, str):
                    zod_chain += f'.default("{field.default_value}")'
                else:
                    zod_chain += f'.default({json.dumps(field.default_value)})'

            lines.append(f"  {f_name}: {zod_chain},")

        lines.append("});")
        lines.append(f"\nexport type {contract.name} = z.infer<typeof {contract.name}Schema>;")
        return "\n".join(lines)

    # =========================================================================
    # == STRATUM III: RUST                                                   ==
    # =========================================================================
    @classmethod
    def _emit_rust_struct(cls, contract: GnosticContract) -> str:
        lines = []
        lines.append("#[derive(Serialize, Deserialize, Debug, Clone)]")
        lines.append(f"pub struct {contract.name} {{")

        for f_name, field in contract.fields.items():
            rs_type, _ = cls._resolve_type(field.gnostic_type, "rust")

            if field.is_optional:
                rs_type = f"Option<{rs_type}>"

            if field.doc:
                lines.append(f"    /// {field.doc}")

            # Convert pythonic snake_case to Rust snake_case (usually matches, but safe)
            lines.append(f"    pub {f_name}: {rs_type},")

        lines.append("}")
        return "\n".join(lines)

    # =========================================================================
    # == THE INTERNAL TYPE RESOLVER                                          ==
    # =========================================================================
    @classmethod
    def _resolve_type(cls, g_type: TypeNode, lang: str) -> Tuple[str, Set[str]]:
        """
        Recursively translates a TypeNode into a native string and required imports.
        """
        imports = set()

        # 1. Primitives
        if isinstance(g_type, PrimitiveType):
            mapped = cls._TYPE_MAP[lang].get(g_type.name, cls._TYPE_MAP[lang]["Any"])

            # Substrate Import Suture
            if lang == "python":
                if g_type.name == "UUID": imports.add("from uuid import UUID")
                if g_type.name == "datetime": imports.add("from datetime import datetime")
                if g_type.name == "Any": imports.add("from typing import Any")
                if g_type.name == "SecretStr": imports.add("from pydantic import SecretStr")
                if g_type.name == "EmailStr": imports.add("from pydantic import EmailStr")

            return mapped, imports

        # 2. Collections (Lists)
        elif isinstance(g_type, ListType):
            inner_str, inner_imports = cls._resolve_type(g_type.inner_type, lang)
            imports.update(inner_imports)

            if lang == "python":
                imports.add("from typing import List")
                return f"List[{inner_str}]", imports
            elif lang in ("typescript", "ts"):
                return f"Array<{inner_str}>", imports
            elif lang == "zod":
                return f"z.array({inner_str})", imports
            elif lang == "rust":
                return f"Vec<{inner_str}>", imports

        # 3. Mappings (Dicts)
        elif isinstance(g_type, DictType):
            k_str, k_imp = cls._resolve_type(g_type.key_type, lang)
            v_str, v_imp = cls._resolve_type(g_type.value_type, lang)
            imports.update(k_imp)
            imports.update(v_imp)

            if lang == "python":
                imports.add("from typing import Dict")
                return f"Dict[{k_str}, {v_str}]", imports
            elif lang in ("typescript", "ts"):
                return f"Record<{k_str}, {v_str}>", imports
            elif lang == "zod":
                return f"z.record({k_str}, {v_str})", imports
            elif lang == "rust":
                return f"std::collections::HashMap<{k_str}, {v_str}>", imports

        # 4. Optionals
        elif isinstance(g_type, OptionalType):
            inner_str, inner_imports = cls._resolve_type(g_type.inner_type, lang)
            imports.update(inner_imports)
            # Optionals are usually handled at the field level, but if nested:
            if lang == "python":
                imports.add("from typing import Optional")
                return f"Optional[{inner_str}]", imports
            elif lang in ("typescript", "ts"):
                return f"{inner_str} | null", imports
            elif lang == "zod":
                return f"{inner_str}.nullable()", imports
            elif lang == "rust":
                return f"Option<{inner_str}>", imports

        # Fallback
        return cls._TYPE_MAP[lang]["Any"], imports

    @classmethod
    def _emit_go_struct(cls, contract: GnosticContract) -> str:
        lines = [f"type {contract.name} struct {{"]
        for f_name, field in contract.fields.items():
            go_type = {"UUID": "string", "EmailStr": "string", "str": "string",
                       "int": "int64", "float": "float64", "bool": "bool"}.get(field.gnostic_type.name, "interface{}")

            if field.is_optional: go_type = f"*{go_type}"  # Use pointers for optional fields in Go

            # JSON tags
            tag = f'`json:"{f_name}{",omitempty" if field.is_optional else ""}"`'
            lines.append(f"\t{f_name.capitalize()} {go_type} {tag}")

        lines.append("}")
        return "\n".join(lines)
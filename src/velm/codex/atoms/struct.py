# scaffold/semantic_injection/directives/struct_domain.py

"""
=================================================================================
== THE POLYGLOT MASON (V-Ω-STRUCT-DOMAIN)                                      ==
=================================================================================
LIF: 50,000,000,000

This artisan implements the `@struct` namespace. It accepts a high-level schema
definition and materializes it into language-specific data structures.

Usage:
    models.py :: @struct/pydantic(name="User", fields="id:uuid, name:str, email:email")
    types.ts  :: @struct/typescript(name="User", fields="id:string, active:bool")
    schema.sql:: @struct/sql(name="users", fields="id:pk, name:varchar(255)")
=================================================================================
"""
from typing import Dict, Any, List, Tuple

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("struct")
class StructDomain(BaseDirectiveDomain):
    """
    The Forge of Data Structures.
    """

    @property
    def namespace(self) -> str:
        return "struct"

    def help(self) -> str:
        return "Generates data models (Pydantic, TypeScript, SQL, Go) from a schema string."

    def _parse_fields(self, fields_str: str) -> List[Tuple[str, str]]:
        """
        Parses 'name:type, age:int' into [('name', 'type'), ('age', 'int')]
        """
        fields = []
        for part in fields_str.split(','):
            if ':' in part:
                k, v = part.split(':', 1)
                fields.append((k.strip(), v.strip().lower()))
            else:
                fields.append((part.strip(), 'str'))  # Default type
        return fields

    def _directive_pydantic(self, context: Dict[str, Any], name: str, fields: str, *args, **kwargs) -> str:
        """@struct/pydantic(name="User", fields="...")"""
        parsed = self._parse_fields(fields)

        # Type Mapping
        py_types = {
            'str': 'str', 'string': 'str', 'int': 'int', 'integer': 'int',
            'bool': 'bool', 'boolean': 'bool', 'float': 'float',
            'uuid': 'UUID', 'email': 'EmailStr', 'date': 'datetime'
        }

        imports = ["from pydantic import BaseModel"]
        if any(t[1] == 'uuid' for t in parsed): imports.append("from uuid import UUID")
        if any(t[1] == 'date' for t in parsed): imports.append("from datetime import datetime")
        if any(t[1] == 'email' for t in parsed): imports.append("from pydantic import EmailStr")

        lines = list(set(imports)) + ["", f"class {name}(BaseModel):"]
        for field_name, field_type in parsed:
            py_type = py_types.get(field_type, 'str')
            lines.append(f"    {field_name}: {py_type}")

        return "\n".join(lines)

    def _directive_typescript(self, context: Dict[str, Any], name: str, fields: str, export: bool = True, *args,
                              **kwargs) -> str:
        """@struct/typescript(name="User", fields="...")"""
        parsed = self._parse_fields(fields)

        ts_types = {
            'str': 'string', 'string': 'string', 'uuid': 'string', 'email': 'string',
            'int': 'number', 'float': 'number', 'integer': 'number',
            'bool': 'boolean', 'boolean': 'boolean', 'date': 'Date'
        }

        prefix = "export " if str(export).lower() == 'true' else ""
        lines = [f"{prefix}interface {name} {{"]
        for field_name, field_type in parsed:
            ts_type = ts_types.get(field_type, 'string')
            lines.append(f"  {field_name}: {ts_type};")
        lines.append("}")

        return "\n".join(lines)

    def _directive_go(self, context: Dict[str, Any], name: str, fields: str, *args, **kwargs) -> str:
        """@struct/go(name="User", fields="...")"""
        parsed = self._parse_fields(fields)

        go_types = {
            'str': 'string', 'string': 'string', 'uuid': 'string', 'email': 'string',
            'int': 'int', 'integer': 'int', 'float': 'float64',
            'bool': 'bool', 'boolean': 'bool', 'date': 'time.Time'
        }

        lines = [f"type {name} struct {{"]
        for field_name, field_type in parsed:
            go_type = go_types.get(field_type, 'string')
            # Capitalize field name for export in Go
            go_field = field_name[0].upper() + field_name[1:]
            lines.append(f"    {go_field} {go_type} `json:\"{field_name}\"`")
        lines.append("}")

        return "\n".join(lines)

    def _directive_sql(self, context: Dict[str, Any], name: str, fields: str, db: str = "postgres", *args,
                       **kwargs) -> str:
        """@struct/sql(name="users", fields="...")"""
        parsed = self._parse_fields(fields)

        sql_types = {
            'str': 'VARCHAR(255)', 'string': 'VARCHAR(255)', 'text': 'TEXT',
            'int': 'INTEGER', 'integer': 'INTEGER',
            'bool': 'BOOLEAN', 'boolean': 'BOOLEAN',
            'uuid': 'UUID' if db == 'postgres' else 'CHAR(36)',
            'pk': 'SERIAL PRIMARY KEY' if db == 'postgres' else 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'date': 'TIMESTAMP'
        }

        lines = [f"CREATE TABLE {name} ("]
        defs = []
        for field_name, field_type in parsed:
            sql_type = sql_types.get(field_type, 'VARCHAR(255)')
            defs.append(f"    {field_name} {sql_type}")

        lines.append(",\n".join(defs))
        lines.append(");")

        return "\n".join(lines)
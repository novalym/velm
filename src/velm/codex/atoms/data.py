# Path: src/velm/codex/atoms/data.py
# ----------------------------------

"""
=================================================================================
== THE DATA ARCHITECT (V-Ω-DATA-DOMAIN)                                        ==
=================================================================================
LIF: 100,000,000,000 | ROLE: SCHEMA_MATERIALIZER

This artisan implements the `@data` namespace. It solves the "Schema Void" by
allowing the Architect to define data structures once and project them into
SQL, Pydantic, or TypeScript simultaneously.
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("data")
class DataDomain(BaseDirectiveDomain):
    """The Keeper of Schemas."""

    @property
    def namespace(self) -> str:
        return "data"

    def help(self) -> str:
        return "Generates data models (SQL, Pydantic, Prisma)."

    def _directive_model(self, context: Dict[str, Any], name: str, fields: str, flavor: str = "pydantic") -> str:
        """
        data.model(name="User", fields="id:uuid, name:str", flavor="pydantic")
        """
        # Simple parser: "key:type, key2:type"
        parsed_fields = [f.strip().split(':') for f in fields.split(',')]

        if flavor == "pydantic":
            lines = [f"class {name}(BaseModel):"]
            imports = {"from pydantic import BaseModel"}

            for fname, ftype in parsed_fields:
                py_type = "str"
                if ftype == "uuid":
                    py_type = "UUID"
                    imports.add("from uuid import UUID")
                elif ftype == "int":
                    py_type = "int"
                elif ftype == "bool":
                    py_type = "bool"
                elif ftype == "datetime":
                    py_type = "datetime"
                    imports.add("from datetime import datetime")

                lines.append(f"    {fname}: {py_type}")

            return "\n".join(sorted(list(imports))) + "\n\n" + "\n".join(lines)

        elif flavor == "sql":
            lines = [f"CREATE TABLE {name.lower()}s ("]
            for fname, ftype in parsed_fields:
                sql_type = "VARCHAR(255)"
                if ftype == "uuid":
                    sql_type = "UUID PRIMARY KEY"
                elif ftype == "int":
                    sql_type = "INTEGER"
                elif ftype == "bool":
                    sql_type = "BOOLEAN"
                elif ftype == "datetime":
                    sql_type = "TIMESTAMP"

                lines.append(f"    {fname} {sql_type},")

            # Remove last comma hack
            lines[-1] = lines[-1].rstrip(',')
            lines.append(");")
            return "\n".join(lines)

        return f"# Unknown flavor: {flavor}"

    def _directive_connection(self, context: Dict[str, Any], db: str = "postgres") -> str:
        """data.connection(db="postgres") -> Connection string logic."""
        return dedent(f"""
            import os

            def get_db_url():
                user = os.getenv("DB_USER", "postgres")
                password = os.getenv("DB_PASSWORD", "password")
                host = os.getenv("DB_HOST", "localhost")
                port = os.getenv("DB_PORT", "5432")
                name = os.getenv("DB_NAME", "app_db")
                return f"postgresql://{{user}}:{{password}}@{{host}}:{{port}}/{{name}}"
        """).strip()



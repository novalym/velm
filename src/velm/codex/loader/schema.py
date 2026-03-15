# Path: src/velm/codex/loader/schema.py
# -------------------------------------

import inspect
from typing import Dict, Any


class SchemaGenerator:
    """
    =============================================================================
    == THE JSON SCHEMA TRANSMUTER (V-Ω-REACT-FLOW-BRIDGE)                      ==
    =============================================================================
    Converts Python methods into structured JSON schemas for Visual UI rendering
    and LLM Tool Calling.
    """

    @staticmethod
    def generate() -> Dict[str, Any]:
        from .registry import CodexRegistry
        CodexRegistry.awaken()

        schema = {"type": "object", "properties": {}}

        for d_name, d_handler in CodexRegistry._domains.items():
            domain_schema = {
                "type": "object",
                "description": d_handler.help(),
                "rites": {}
            }

            for rite in [r.replace('_directive_', '') for r in dir(d_handler) if r.startswith('_directive_')]:
                method = getattr(d_handler, f"_directive_{rite}")
                sig = inspect.signature(method)
                doc = inspect.getdoc(method) or ""

                params = {"type": "object", "properties": {}, "required": []}

                for p_name, p_val in sig.parameters.items():
                    if p_name in ('self', 'context', 'args', 'kwargs'):
                        continue

                    # Map Python types to JSON Schema types
                    ptype = "string"
                    if p_val.annotation is int:
                        ptype = "integer"
                    elif p_val.annotation is float:
                        ptype = "number"
                    elif p_val.annotation is bool:
                        ptype = "boolean"

                    prop_data = {"type": ptype}
                    if p_val.default is not inspect.Parameter.empty:
                        prop_data["default"] = p_val.default
                    else:
                        params["required"].append(p_name)

                    params["properties"][p_name] = prop_data

                domain_schema["rites"][rite] = {
                    "description": doc,
                    "parameters": params
                }

            schema["properties"][d_name] = domain_schema

        return schema
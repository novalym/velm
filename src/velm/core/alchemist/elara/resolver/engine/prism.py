# Path: core/alchemist/elara/resolver/engine/prism.py
# ---------------------------------------------------

from typing import Dict


class PolyglotPrism:
    """
    =============================================================================
    == THE POLYGLOT PRISM (V-Ω-TOTALITY)                                       ==
    =============================================================================
    [ASCENSION 147]: Transmutes G-IR internal fields into native code representations
    for Python, TypeScript, Rust, and Go dynamically.
    """

    @classmethod
    def emit_class(cls, class_name: str, g_ir_fields: Dict[str, str], language: str) -> str:
        lang = str(language).lower()
        if lang == "python":
            lines = [f"class {class_name}(BaseModel):", '    """Forged via ELARA Polyglot Prism."""']
            for k, v in g_ir_fields.items():
                py_type = {"uuid": "UUID", "email": "EmailStr", "str": "str", "int": "int", "bool": "bool"}.get(v,
                                                                                                                "Any")
                lines.append(f"    {k}: {py_type}")
            return "\n".join(lines)
        elif lang in ("typescript", "ts"):
            lines = [f"export interface {class_name} {{"]
            for k, v in g_ir_fields.items():
                ts_type = {"uuid": "string", "email": "string", "str": "string", "int": "number",
                           "bool": "boolean"}.get(v, "any")
                lines.append(f"  {k}: {ts_type};")
            lines.append("}")
            return "\n".join(lines)
        elif lang == "rust":
            lines = ["#[derive(Serialize, Deserialize, Debug, Clone)]", f"pub struct {class_name} {{"]
            for k, v in g_ir_fields.items():
                rs_type = {"uuid": "uuid::Uuid", "int": "i64", "str": "String", "bool": "bool"}.get(v, "String")
                lines.append(f"    pub {k}: {rs_type},")
            lines.append("}")
            return "\n".join(lines)
        elif lang == "go":
            lines = [f"type {class_name} struct {{"]
            for k, v in g_ir_fields.items():
                go_type = {"uuid": "string", "int": "int64", "str": "string", "bool": "bool"}.get(v, "interface{}")
                lines.append(f"\t{k.capitalize()} {go_type} `json:\"{k}\"`")
            lines.append("}")
            return "\n".join(lines)
        return f"/* UNKNOWN_PRISM_TONGUE: {lang} */"

    @classmethod
    def parse_gir_content(cls, raw_content: str) -> Dict[str, str]:
        fields = {}
        for line in raw_content.splitlines():
            clean = line.strip()
            if not clean or clean.startswith(('#', '//', '/*')): continue
            if ':' in clean:
                parts = [x.strip() for x in clean.split(':', 1)]
                if len(parts) == 2: fields[parts[0]] = parts[1].lower()
        return fields


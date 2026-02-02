# Path: scaffold/utils/dossier_scribe/constellation/arch_scribe/mermaids.py
# -------------------------------------------------------------------------

from pathlib import Path


class MermaidWeaver:
    """
    =================================================================================
    == THE GRAPH WEAVER (V-Ω-STYLED-TOPOGRAPHY)                                    ==
    =================================================================================
    Forges the Mermaid.js directed graph string.
    """

    @staticmethod
    def weave(root: Path) -> str:
        lines = ["graph TD;", f"    root[{root.name}]"]

        # Styles
        lines.append("    classDef config fill:#f9f,stroke:#333,stroke-width:2px;")
        lines.append("    classDef src fill:#bbf,stroke:#333,stroke-width:2px;")
        lines.append("    classDef infra fill:#bfb,stroke:#333,stroke-width:2px;")

        # We only map the top 2 levels to avoid chaos
        for item in root.iterdir():
            if item.name.startswith('.') or item.name == '__pycache__': continue
            if item.name == "scaffold.lock": continue
            if item.name == "ARCHITECTURE.md": continue  # Don't map self

            clean_name = item.name.replace('.', '_').replace('-', '_')
            node_id = f"root_{clean_name}"

            style_class = ""
            if item.name in ['src', 'app', 'lib']: style_class = ":::src"
            if item.name.endswith(('.toml', '.json', '.yaml')): style_class = ":::config"
            if 'docker' in item.name.lower(): style_class = ":::infra"

            if item.is_dir():
                lines.append(f"    root --> {node_id}[/{item.name}/]{style_class}")

                # Level 2
                count = 0
                for sub in item.iterdir():
                    if sub.name.startswith('.') or sub.name == '__pycache__': continue
                    sub_clean = sub.name.replace('.', '_').replace('-', '_')
                    sub_id = f"{node_id}_{sub_clean}"

                    sub_style = ""
                    if sub.name.endswith(('.py', '.ts', '.rs')): sub_style = ":::src"

                    shape = "[/.../]" if sub.is_dir() else "({...})"
                    lines.append(f"    {node_id} --> {sub_id}{shape}{sub_style}")
                    count += 1
                    if count >= 6:  # Limit children for readability
                        lines.append(f"    {node_id} --> {node_id}_more( ... )")
                        break
            else:
                lines.append(f"    root --> {node_id}({item.name}){style_class}")

        return "\n".join(lines)
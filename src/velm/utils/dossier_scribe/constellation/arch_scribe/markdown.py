# Path: scaffold/utils/dossier_scribe/constellation/arch_scribe/markdown.py
# -------------------------------------------------------------------------

import json
import platform
from datetime import datetime
from typing import List

from .....utils import get_human_readable_size
from .dna import ProjectDNA
from .mermaids import MermaidWeaver


class MarkdownForge:
    """
    =================================================================================
    == THE CODEX WRITER (V-Ω-NARRATIVE-ENGINE-INVISIBLE)                           ==
    =================================================================================
    Assembles the final text.

    [ASCENSION]: The AI Context is now woven into the fabric of the file using
    HTML comments, rendering it invisible to the mortal eye (Preview Mode) but
    luminous to the AI Gaze (Raw Mode).
    """

    @staticmethod
    def forge_document(project_name: str, dna: ProjectDNA, tree_text: str) -> str:

        # [ASCENSION 12] The Luminous Footer (Framework specific actions)
        next_actions = ["- [ ] Explore the codebase"]
        if "Python" in dna.frameworks or "Poetry" in dna.frameworks:
            next_actions.append("- [ ] Run `poetry install`")
        if "Node.js" in dna.frameworks or "React" in dna.frameworks:
            next_actions.append("- [ ] Run `npm install && npm run dev`")
        if "Docker" in dna.frameworks:
            next_actions.append("- [ ] Run `docker-compose up -d`")

        content = [
            f"# 🏛️ Gnostic Architecture: {project_name}",
            f"",
            f"> **Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> **System:** {dna.system_type} | **Tongue:** {dna.primary_language}",
            f"",
            "## 🗺️ Navigation",
            "- [Executive Summary](#-executive-summary)",
            "- [System Topography (Mermaid)](#%EF%B8%8F-system-topography)",
            "- [Directory Manifest](#-directory-manifest)",
            "- [Key Portals](#-key-portals)",
            "- [The Visual Tree](#-the-visual-tree)",
            "- [Gnostic Delta](#-gnostic-delta)",
            "",
            "---",
            "",
            "## 🔭 Executive Summary",
            f"This reality appears to be a **{dna.primary_language}** project.",
            f"It consists of **{dna.file_count}** scriptures and **{dna.dir_count}** sanctums, totaling **{dna.total_size_human}**.",
            "",
            "### 🧬 DNA Analysis",
            "| Attribute | Gnosis |",
            "| :--- | :--- |",
            f"| **Primary Tongue** | {dna.primary_language} {dna.language_emoji} |",
            f"| **Frameworks** | {', '.join(dna.frameworks) or 'None Detected'} |",
            f"| **Technical Debt** | {dna.debt_count} markers (TODO/FIXME) |",
            f"| **Git Branch** | `{dna.git_branch}` |",
            f"| **Git Commit** | `{dna.git_commit}` |",
            f"| **Generator** | Scaffold (Python {platform.python_version()}) |",
            "",
            "### 🕸️ Key Dependencies",
            ", ".join([f"`{d}`" for d in dna.dependencies]) or "None detected in top-level manifests.",
            "",
            "---",
            "",
            "## 🕸️ System Topography",
            "A directed graph of the high-level structural relationships.",
            "",
            "```mermaid",
            MermaidWeaver.weave(dna.root),
            "```",
            "",
            "---",
            "",
            "## 📂 Directory Manifest",
            "The sacred purpose of the top-level sanctums.",
            "",
            "| Sanctum | Deduced Purpose |",
            "| :--- | :--- |",
            *[f"| **`{d}/`** | {dna.divine_directory_purpose(d)} |" for d in dna.top_level_dirs],
            "",
            "---",
            "",
            "## 🔑 Key Portals",
            "Direct access to critical scriptures.",
            "",
            "| Scripture | Type | Link |",
            "| :--- | :--- | :--- |",
            *[f"| `{f}` | {t} | [Open]({p}) |" for f, t, p in dna.key_files],
            "",
            "---",
            "",
            "## 🌳 The Visual Tree",
            "<details>",
            "<summary>Click to expand the full ASCII structure</summary>",
            "",
            "```text",
            tree_text,
            "```",
            "</details>",
            "",
            "### 🔮 Legend of Sigils",
            "| Sigil | Meaning |",
            "| :---: | :--- |",
            "| ✨ | **Created:** A new soul forged from the void. |",
            "| ⚡ | **Transfigured:** An existing soul modified. |",
            "| ➡️ | **Moved:** A soul translocated in space. |",
            "| 🛡️ | **Unchanged:** A soul preserved in stasis. |",
            "| 💀 | **Annihilated:** A soul returned to the void. |",
            "",
            "---",
            "",
            "## 📜 Gnostic Delta",
            "The chronicle of the most recent rite.",
            "",
            "| Scripture | Action | Size |",
            "| :--- | :---: | :---: |",
            *[f"| `{a.path.name}` | {a.action} | {get_human_readable_size(a.size_bytes)} |" for a in dna.artifacts],
            "",
            "---",
            "",
            "## 🚀 Next Steps",
            *[f"{a}" for a in next_actions],
            "",
            "---",
            "> *This document contains hidden JSON DNA for AI analysis.*",
            "",
            "<!-- SCAFFOLD_AI_DNA_START",
            json.dumps(dna.generate_json_map(), indent=2),
            "SCAFFOLD_AI_DNA_END -->"
        ]
        return "\n".join(content)
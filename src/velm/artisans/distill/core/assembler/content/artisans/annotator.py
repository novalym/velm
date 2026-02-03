# Path: scaffold/artisans/distill/core/assembler/content/artisans/annotator.py

import re
import difflib
import subprocess
from pathlib import Path
from typing import Set, Dict, List, Any

from ..contracts import WeavingContext
from .......core.cortex.contracts import FileGnosis


class Annotator:
    """A polyglot scribe that weaves temporal, runtime, and performance Gnosis."""

    COMMENT_SYNTAX: Dict[str, str] = {
        '.py': '#', '.rb': '#', '.sh': '#', '.yaml': '#', '.yml': '#', '.toml': '#', '.dockerfile': '#',
        '.js': '//', '.ts': '//', '.jsx': '//', '.tsx': '//', '.go': '//', '.rs': '//', '.java': '//', '.c': '//',
        '.cpp': '//', '.cs': '//', '.swift': '//', '.kt': '//', '.php': '//', '.dart': '//',
        '.html': '<!--', '.xml': '<!--', '.md': '<!--', '.svg': '<!--',
        '.css': '/*', '.scss': '/*', '.less': '/*',
        '.sql': '--', '.lua': '--', '.hs': '--',
        '.ini': ';', '.conf': '#'
    }

    def inject_all(self, content: str, ctx: WeavingContext) -> str:
        """The Grand Rite of Annotation."""
        annotated = content

        if ctx.diff_context:
            annotated = self._inject_diff_context(annotated, ctx.project_root / ctx.gnosis.path, ctx.project_root)

        if ctx.perf_stats:
            annotated = self._inject_perf_annotations(annotated, ctx.gnosis, ctx.perf_stats)

        path_str = str(ctx.gnosis.path).replace('\\', '/')
        file_heat = ctx.heat_map.get(path_str, set())
        file_runtime = ctx.runtime_values.get(path_str, {})
        if file_heat or file_runtime:
            annotated = self._apply_runtime_annotations(annotated, file_heat, file_runtime,
                                                        ctx.project_root / ctx.gnosis.path)

        return annotated

    def _inject_diff_context(self, content: str, file_path: Path, project_root: Path) -> str:
        """The Ghost of Versions Past."""
        try:
            rel_path = file_path.relative_to(project_root).as_posix()
            old_content = subprocess.check_output(
                ['git', 'show', f'HEAD:{rel_path}'],
                cwd=project_root, stderr=subprocess.DEVNULL, text=True, encoding='utf-8'
            )
            lines, old_lines = content.splitlines(), old_content.splitlines()
            comment_char = self.COMMENT_SYNTAX.get(file_path.suffix.lower(), '#')
            matcher = difflib.SequenceMatcher(None, old_lines, lines)
            output = []
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == 'equal':
                    output.extend(lines[j1:j2])
                elif tag == 'replace':
                    for k in range(i1, i2):
                        if old_lines[k].strip(): output.append(f"    {comment_char} [WAS: {old_lines[k].strip()}]")
                    output.extend(lines[j1:j2])
                elif tag == 'insert':
                    output.extend(lines[j1:j2])
                elif tag == 'delete':
                    for k in range(i1, i2):
                        if old_lines[k].strip(): output.append(f"    {comment_char} [DELETED: {old_lines[k].strip()}]")
            return "\n".join(output)
        except Exception:
            return content

    def _inject_perf_annotations(self, content: str, gnosis: FileGnosis, perf_stats: Dict) -> str:
        """The Wraith of Celerity."""
        path_key = str(gnosis.path).replace('\\', '/')
        file_stats = perf_stats.get(path_key)
        if not file_stats: return content
        lines, functions = content.splitlines(), gnosis.ast_metrics.get("functions", [])
        functions.sort(key=lambda x: x['lineno'], reverse=True)
        for func in functions:
            name, lineno = func['name'], func['lineno'] - 1
            if name in file_stats and 0 <= lineno < len(lines):
                stats = file_stats[name]
                perf_note = f"time={stats['time']:.3f}s | calls={stats['calls']}"
                line = lines[lineno]
                comment_char = self.COMMENT_SYNTAX.get(gnosis.path.suffix.lower(), '#')
                lines[lineno] = f"{line.ljust(80)} {comment_char} [PERF: {perf_note}]"
        return "\n".join(lines)

    def _apply_runtime_annotations(self, content: str, heat: Set, runtime: Dict, path: Path) -> str:
        """The Chronomancer's Needle & Wraith's Ink."""
        lines, annotated = content.splitlines(), []
        comment_char = self.COMMENT_SYNTAX.get(path.suffix.lower(), '#')
        for i, line in enumerate(lines):
            line_num = i + 1
            if line_num in runtime:
                for note in runtime[line_num]: annotated.append(f"    {comment_char} [👻 STATE: {note}]")
            if line_num in heat:
                line = f"{line.ljust(80)} {comment_char} [🔥]" if len(
                    line) < 80 else f"{line}\n    {comment_char} [🔥 CHANGED]"
            annotated.append(line)
        return "\n".join(annotated)
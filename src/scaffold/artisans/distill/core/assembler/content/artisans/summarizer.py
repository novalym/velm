# Path: scaffold/artisans/distill/core/assembler/content/artisans/summarizer.py

import re
import json
from pathlib import Path

class Summarizer:
    """A specialist scribe for condensing massive lockfiles."""

    def summarize_lockfile(self, filename: str, content: str) -> str:
        """The Rite of Lockfile Summarization, now with expanded knowledge."""
        summary = []
        try:
            if 'package-lock.json' in filename:
                data = json.loads(content)
                deps = data.get('packages', {}).get('', {}).get('dependencies', {})
                summary.append(f"// npm dependencies: {', '.join(deps.keys())}")
            elif 'poetry.lock' in filename:
                names = re.findall(r'name = "([\w-]+)"', content)
                unique_names = sorted(list(set(names)))
                summary.append(f"# poetry dependencies: {', '.join(unique_names[:30])}...")
            elif 'go.sum' in filename:
                lines = content.splitlines()
                deps = sorted(list({line.split()[0] for line in lines}))
                summary.append(f"// go dependencies: {', '.join(deps[:30])}...")
            elif 'Cargo.lock' in filename:
                names = re.findall(r'^name = "([\w-]+)"', content, re.MULTILINE)
                unique_names = sorted(list(set(names)))
                summary.append(f"# rust dependencies: {', '.join(unique_names[:30])}...")
            else:
                summary.append(f"# [Summary] {filename}: {len(content)} bytes")
        except Exception:
            summary.append(f"# [Summary] {filename} (Unparseable)")

        return "\n".join(summary)

    def summarize_code(self, path: Path, content: str) -> str:
        """
        [NEW] Summons the 'Fast' AI to distill the file's purpose.
        """
        # 1. Heuristic: Read docstrings first to save tokens
        # (Simple regex for top-level docstring)
        match = re.search(r'^["\']{3}(.*?)["\']{3}', content, re.DOTALL)
        if match:
            doc = match.group(1).strip().split('\n')[0]
            return f"# [Summary: {doc}]"

        # 2. AI Fallback (The Semantic Gaze)
        # Only use if we have a budget/permission? We assume yes for 'distill'.
        # We use a very short prompt to the FAST model.
        try:
            ai = AIEngine.get_instance()
            if not ai.config.enabled:
                return f"# [Summary: {len(content)} chars of logic]"

            prompt = f"Summarize the purpose of this file in 10 words or less. File: {path.name}\n\n{content[:2000]}"
            summary = ai.ignite(prompt, model="fast", max_tokens_override=50).strip()
            return f"# [AI Summary: {summary}]"
        except Exception:
            return f"# [Summary: {len(content)} chars of logic]"
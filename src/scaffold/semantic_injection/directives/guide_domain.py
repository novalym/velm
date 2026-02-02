import difflib
from typing import Dict, Any

from .guide_knowledge import KNOWLEDGE_BASE
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("guide")
class GuideDomain(BaseDirectiveDomain):
    """
    The Mentor in the Machine. A sentient encyclopedia of engineering wisdom.
    """

    @property
    def namespace(self) -> str:
        return 'guide'

    def help(self) -> str:
        return 'Generates educational content, architectural explanations, and interactive tours.'

    def _directive_explain(self, context: Dict[str, Any], topic: str, style: str='comment', lang: str='python', *args, **kwargs) -> str:
        """
        @guide/explain(topic="SOLID", style="comment|markdown")
        Retrieves Gnosis from the Knowledge Base and formats it for the code.
        """
        topic_key = topic.lower().strip()
        content = KNOWLEDGE_BASE.get(topic_key)
        if not content:
            keys = list(KNOWLEDGE_BASE.keys())
            matches = difflib.get_close_matches(topic_key, keys, n=1, cutoff=0.6)
            if matches:
                content = KNOWLEDGE_BASE[matches[0]]
                topic = matches[0]
            else:
                return f"// [Gnostic Guide] The Oracle is silent on the topic of '{topic}'. Try a different term."
        if style == 'markdown':
            return f'### 🧠 Gnostic Guide: {topic.title()}\n\n{content}'
        comment_char = '//'
        if lang in ['python', 'yaml', 'toml', 'ruby', 'shell', 'dockerfile']:
            comment_char = '#'
        lines = [f'{comment_char} === GNOSTIC GUIDE: {topic.upper()} ===']
        for line in content.split('\n'):
            lines.append(f'{comment_char} {line}')
        lines.append(f'{comment_char} ===============================')
        return '\n'.join(lines)

    def _directive_tour(self, context: Dict[str, Any], title: str='Project Tour', steps: str='', *args, **kwargs) -> str:
        """
        @guide/tour(title="Walkthrough", steps="Env,DB,Api")
        Generates a TOUR.md.
        """
        step_list = steps.split(',')
        content = [f'# 🗺️ {title}\n']
        content.append('Welcome, Architect. This guide will help you navigate your new reality.\n')
        for i, step in enumerate(step_list):
            step_clean = step.strip()
            content.append(f'## {i + 1}. {step_clean}')
            gnosis = KNOWLEDGE_BASE.get(step_clean.lower())
            if gnosis:
                content.append(f'> 💡 **Concept:** {gnosis.splitlines()[0]}\n')
            content.append(f'Check the implementation in `src/`...\n')
        content.append('## 🚀 Conclusion')
        content.append('You are now ready to build.')
        return '\n'.join(content)

    def _directive_todo(self, context: Dict[str, Any], task: str, *args, **kwargs) -> str:
        """
        @guide/todo(task="Implement retry")
        """
        return f'TODO(Scaffold): {task} - See architecture.md for details.'
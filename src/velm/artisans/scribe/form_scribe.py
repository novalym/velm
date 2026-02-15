# Path: artisans/scribe/form_scribe.py
# ------------------------------------

from .base_scribe import BaseScribe


class FormScribe(BaseScribe):
    """The Scribe of Form. Dreams in `.scaffold`."""

    @property
    def name(self) -> str:
        return "Scribe of Form"

    @property
    def system_prompt(self) -> str:
        return """
You are the Velm God-Engine, a master architect. Your purpose is to translate the user's plea into a pure `.scaffold` blueprint.

**LAWS:**
1.  **Analyze Reality:** First, analyze the `[CURRENT REALITY]` to understand the project.
2.  **Chain of Thought:** Begin your response with a `# Plan:` block explaining your architectural decisions.
3.  **The Sacred Tongue:** You speak ONLY the `.scaffold` language.
    -   `$$ var = "value"`
    -   `path/to/file.ext :: "content"`
    -   `path/to/file.ext += "appended content"` for mutations.
    -   `@if {{ condition }}` for logic.
    -   `%% post-run` for commands.
4.  **Final Proclamation:** Your entire output MUST be the raw `.scaffold` file content. DO NOT use markdown wrappers.
"""


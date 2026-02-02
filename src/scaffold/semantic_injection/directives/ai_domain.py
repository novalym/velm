# scaffold/semantic_injection/directives/ai_domain.py

"""
=================================================================================
== THE NEURAL FORGE (V-Ω-AI-DOMAIN-ULTIMA)                                     ==
=================================================================================
LIF: 10,000,000,000,000

This artisan implements the `@ai` namespace. It is the high-level interface
between the Architect's blueprint and the `core.ai` engine.

It transforms vague intents into precise, context-aware realities by injecting
Gnostic State into the prompt and selecting the optimal System Persona.

Usage:
    # Generate complex logic with context awareness
    auth.py :: @ai/code(prompt="JWT validation middleware with refresh tokens", lang="python")

    # Generate specific artifacts
    README.md :: @ai/text(prompt="An enthusiastic intro for a crypto trading bot", temp=0.9)

    # Generate tests
    tests/test_auth.py :: @ai/unit_test(target="auth.py logic", framework="pytest")

    # Generate config
    k8s.yaml :: @ai/config(desc="Deployment for a stateless container", format="yaml")
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("NeuralForge")

@domain("ai")
class AiDomain(BaseDirectiveDomain):
    """
    The Bridge to the Latent Space.
    """

    @property
    def namespace(self) -> str:
        return "ai"

    def help(self) -> str:
        return "Generates content using LLMs. Supports: code, text, unit_test, config, explain."

    # =========================================================================
    # == INTERNAL RITES (HELPER ARTISANS)                                    ==
    # =========================================================================

    def _get_engine(self) -> AIEngine:
        """Summons the Singleton Brain."""
        return AIEngine.get_instance()

    def _forge_context_block(self, context: Dict[str, Any]) -> Dict[str, str]:
        """
        [THE CONTEXTUAL INFUSION]
        Extracts relevant Gnosis from the blueprint to ground the AI's hallucination.
        """
        # We select only high-value architectural context to save tokens/noise.
        relevant_keys = [
            "project_name", "project_slug", "stack", "framework",
            "database", "orm", "language", "author", "description"
        ]
        return {k: str(context[k]) for k in relevant_keys if k in context}

    def _forge_placeholder(self, prompt: str, error: str, lang: str = "text") -> str:
        """
        [THE RESILIENCE PROTOCOL]
        Generates a safe, commented-out placeholder if the AI fails or is dormant.
        """
        # 1. Divine the Comment Syntax
        comment_sigil = "#"
        if lang in ["js", "ts", "java", "c", "cpp", "go", "rust", "scala", "kotlin", "swift"]:
            comment_sigil = "//"
        elif lang in ["html", "xml", "svg"]:
            comment_sigil = "<!--"  # Special handling needed for closing, simplified here
        elif lang in ["css", "scss"]:
            comment_sigil = "/*"

            # 2. Forge the Scripture
        header = f"{comment_sigil} [AI GENERATION SKIPPED]"
        reason = f"{comment_sigil} Reason: {error}"
        prompt_line = f"{comment_sigil} Prompt: {prompt}"

        return f"{header}\n{reason}\n{prompt_line}\n{comment_sigil} TODO: Implement manually."

    # =========================================================================
    # == THE RITES OF COGNITION                                              ==
    # =========================================================================

    def _directive_code(self,
                        context: Dict[str, Any],
                        prompt: str = "",
                        lang: str = "python",
                        model: str = "smart",
                        temp: float = 0.2,
                        imports: str = "",
                        *args, **kwargs) -> str:
        """
        @ai/code(prompt="...", lang="python", imports="pandas,numpy")

        The God-Engine of Logic.
        Generates production-grade, idiomatic code with strict architectural alignment.
        """
        if not prompt: return "# Void prompt provided. The Oracle remains silent."

        # --- MOVEMENT I: THE CONTEXTUAL INFUSION ---
        project_ctx = self._forge_context_block(context)
        stack_hint = f"Stack: {project_ctx.get('stack', 'Generic')}"

        # --- MOVEMENT II: THE PERSONA ENGINEERING ---
        # We forge a System Prompt that enforces high standards.
        import_constraint = f"Required Imports: {imports}" if imports else "Use standard library or common ecosystem packages."

        system_instruction = dedent(f"""
            You are a Principal Software Architect and Senior Engineer.

            OBJECTIVE:
            Write idiomatic, production-grade, and secure {lang} code based on the User's Request.

            CONTEXT:
            Project: {project_ctx.get('project_name', 'Unnamed')}
            {stack_hint}
            {import_constraint}

            CONSTRAINTS (ABSOLUTE):
            1. OUTPUT FORMAT: Return ONLY the raw code. Do NOT wrap in markdown code blocks (```). Do NOT include conversational filler ("Here is the code").
            2. QUALITY: Use modern syntax, strict type hinting (if applicable to {lang}), and defensive error handling.
            3. DOCS: Include a concise top-level comment/docstring explaining the logic.
            4. SAFETY: Avoid hardcoded secrets. Use environment variables where appropriate.
        """).strip()

        # --- MOVEMENT III: THE IGNITION ---
        try:
            raw_response = self._get_engine().ignite(
                user_query=prompt,
                system=system_instruction,
                context=project_ctx,
                model=model
            )

            # --- MOVEMENT IV: THE RITE OF UNBOXING (MARKDOWN STRIPPER) ---
            # LLMs often disobey the "no markdown" constraint. We force purity.
            clean_response = raw_response.strip()

            # Strip opening ```lang
            if clean_response.startswith("```"):
                # Find the first newline to skip the language identifier (e.g. ```python)
                newline_idx = clean_response.find("\n")
                if newline_idx != -1:
                    clean_response = clean_response[newline_idx + 1:]
                else:
                    # Fallback if it's just ``` with no newline (rare)
                    clean_response = clean_response.lstrip("`")

            # Strip closing ```
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]

            return clean_response.strip()

        except Exception as e:
            Logger.warn(f"Neural connection severed during code generation: {e}")
            return self._forge_placeholder(prompt, str(e), lang)



    def _directive_text(self,
                        context: Dict[str, Any],
                        prompt: str = "",
                        tone: str = "professional",
                        model: str = "smart",
                        temp: float = 0.7,
                        *args, **kwargs) -> str:
        """
        @ai/text(prompt="...", tone="inspiring")
        Generates prose (documentation, readme content, marketing copy).
        """
        if not prompt: return ""

        project_context = self._forge_context_block(context)

        system_prompt = dedent(f"""
            You are a Technical Writer and Product Owner.
            Task: Generate text content based on the user request.
            Tone: {tone}.
            Constraints:
            - Return ONLY the raw text content. Do not wrap in markdown code blocks.
            - Use Markdown formatting (headers, bold, lists) where appropriate.
        """).strip()

        try:
            return self._get_engine().ignite(
                user_query=prompt,
                system=system_prompt,
                context=project_context,
                model=model
            )
        except Exception as e:
            return f"<!-- AI ERROR: {e} -->\n{prompt}"

    def _directive_unit_test(self,
                             context: Dict[str, Any],
                             target: str = "",
                             framework: str = "pytest",
                             model: str = "smart",
                             *args, **kwargs) -> str:
        """
        @ai/unit_test(target="auth.py login function", framework="jest")
        Generates unit tests for a described feature or file.
        """
        if not target: return "# No test target specified."

        project_context = self._forge_context_block(context)

        system_prompt = dedent(f"""
            You are a QA Automation Architect.
            Task: Write a comprehensive unit test suite using {framework}.
            Target: {target}.
            Constraints:
            - Return ONLY the code. No markdown.
            - Cover happy paths and edge cases.
            - Mock external dependencies where implied.
        """).strip()

        try:
            return self._get_engine().ignite(
                user_query=f"Generate tests for: {target}",
                system=system_prompt,
                context=project_context,
                model=model
            )
        except Exception as e:
            return self._forge_placeholder(f"Tests for {target}", str(e))

    def _directive_config(self,
                          context: Dict[str, Any],
                          desc: str = "",
                          format: str = "yaml",
                          *args, **kwargs) -> str:
        """
        @ai/config(desc="K8s deployment for redis", format="yaml")
        Generates configuration files (YAML, JSON, TOML, INI).
        """
        if not desc: return "# No configuration description."

        system_prompt = dedent(f"""
            You are a DevOps Engineer.
            Task: Generate a configuration file in {format.upper()} format.
            Requirement: {desc}.
            Constraints:
            - Return ONLY the raw {format} content. No markdown blocks.
            - Include comments explaining key settings.
        """).strip()

        try:
            return self._get_engine().ignite(
                user_query=desc,
                system=system_prompt,
                model="smart"  # Always use smart model for config correctness
            )
        except Exception as e:
            return self._forge_placeholder(desc, str(e), "config")

    def _directive_explain(self,
                           context: Dict[str, Any],
                           topic: str = "",
                           audience: str = "developer",
                           *args, **kwargs) -> str:
        """
        @ai/explain(topic="Dependency Injection", audience="junior")
        Generates an educational explanation or docstring.
        """
        system_prompt = dedent(f"""
            You are a Principal Engineer and Mentor.
            Task: Explain the concept '{topic}'.
            Target Audience: {audience}.
            Constraints:
            - Be concise but thorough.
            - Use analogies if helpful.
            - Return plain text/markdown.
        """).strip()

        try:
            return self._get_engine().ignite(
                user_query=f"Explain {topic}",
                system=system_prompt,
                model="smart"
            )
        except Exception as e:
            return f"<!-- AI EXPLANATION FAILED: {e} -->"

    def _directive_regex(self, context: Dict[str, Any], desc: str = "", *args, **kwargs) -> str:
        """
        @ai/regex(desc="Email address validation")
        Generates a regex pattern.
        """
        system_prompt = "You are a Regex Expert. Return ONLY the raw regex pattern for the requested logic. No slashes, no flags, just the pattern."
        try:
            return self._get_engine().ignite(
                user_query=desc,
                system=system_prompt,
                model="fast"  # Regex is usually simple enough for fast models
            )
        except Exception:
            return ".* # AI Regex Failed"
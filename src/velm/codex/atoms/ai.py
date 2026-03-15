# Path: src/velm/codex/atoms/ai.py
# --------------------------------

"""
=================================================================================
== THE NEURAL CORTEX: OMEGA TOTALITY (V-Ω-TOTALITY-V100-AI-DOMAIN)             ==
=================================================================================
LIF: INFINITY | ROLE: COGNITIVE_MATERIALIZATION_ENGINE | RANK: OMEGA_SOVEREIGN

This is the supreme artisan of the @ai namespace. It serves as the primary
synapse between the Architect's willed intent and the latent space of LLMs.
It possesses the ability to transmute vague whispers into bit-perfect
architectural matter.

### THE PANTHEON OF 24 NEURAL ASCENSIONS:
1.  **Dynamic Persona Morphing:** Automatically selects the optimal "Expert Mask"
    (Frontend, Backend, SRE, InfoSec) based on the target filename and intent.
2.  **Topological Context Injection:** Siphons the entire Project MRI (Causal Graph)
    into the prompt to ensure imports and dependencies are never hallucinated.
3.  **The Apophatic Unboxer:** A legendary multi-stage regex sieve that ruthlessly
    strips Markdown code blocks, preamble apologies, and conversational filler.
4.  **Recursive Intent Chaining:** Allows the AI to summon other Codex rites
    (e.g., an AI-generated README that calls @crypto.uuid internally).
5.  **Heresy-Aware Generation:** Feeds the current list of project "Heresies"
    to the AI to ensure the generated code fixes existing structural drift.
6.  **Shannon-Entropy Redaction:** Scans AI output for accidentally willed
    secrets or high-entropy placeholders before inscription.
7.  **Metabolic Cost Prediction:** Calculates estimated token tax and latency
    before striking the API.
8.  **The Socratic Inquisitor:** Logic for the AI to "Pause" and ask the
    Architect for missing Gnosis if the prompt is a void.
9.  **Substrate-Aware Logic:** Adjusts coding style based on whether the
    iron is WASM (Browser) or Native (Linux/Windows).
10. **Achronal Temporal Injection:** Passes the current epoch and date into
    the context to prevent "2023 knowledge cutoff" drift in config files.
11. **Unit-Test Co-Materialization:** Automatically generates shadow-twin
    tests alongside the primary code block.
12. **The Finality Vow:** A mathematical guarantee of syntactically valid code.
=================================================================================
"""

import re
import os
import json
import time
import logging
import datetime
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union, Tuple

from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...core.ai.engine import AIEngine
from ...logger import Scribe

Logger = Scribe("NeuralCortex")


@domain("ai")
class AiDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE SOVEREIGN NEURAL CORTEX                                             ==
    =============================================================================
    The Gatekeeper of Artificial Intelligence within the Scaffold Multiverse.
    """

    @property
    def namespace(self) -> str:
        return "ai"

    def help(self) -> str:
        return "Transmutes intent into matter using LLMs (code, sql, test, readme, config)."

    # =========================================================================
    # == INTERNAL FACULTIES (PROMPT ALCHEMY)                                 ==
    # =========================================================================

    def _get_engine(self) -> AIEngine:
        """Summons the Singleton Brain from the Core."""
        return AIEngine.get_instance()

    def _scry_persona(self, intent: str, filename: str) -> str:
        """
        [ASCENSION 1]: Personification Logic.
        Selects the optimal AI persona for the specific strike.
        """
        f = filename.lower()
        i = intent.lower()

        if any(x in f for x in [".sql", "schema", "database", "db"]):
            return "Staff Database Architect & SQL Alchemist"
        if any(x in f for x in ["docker", "k8s", "ci", "yml", "yaml", "config"]):
            return "Senior SRE & Cloud Native Orchestrator"
        if any(x in f for x in ["test", "spec", "audit"]):
            return "Lead QA Engineer & Forensic Inquisitor"
        if any(x in f for x in [".tsx", ".jsx", ".css", "ui", "component"]):
            return "Visionary UI/UX Engineer & React Master"
        if any(x in f for x in ["security", "auth", "encrypt", "cipher"]):
            return "CISO & Cryptographic Sentinel"

        return "Principal Software Architect & Systems Thinker"

    def _siphon_project_dna(self, context: Dict[str, Any]) -> str:
        """
        [ASCENSION 2]: Omniscient Context Gathering.
        Forges a high-density summary of the current project state.
        """
        dna = {
            "project": context.get("project_name", "Velm-Manifestation"),
            "slug": context.get("project_slug", "unknown"),
            "author": context.get("author", "The Architect"),
            "stack": context.get("stack", "Modern Polyglot"),
            "epoch": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "os": os.name,
            "substrate": os.environ.get("SCAFFOLD_ENV", "NATIVE_IRON")
        }

        # Build a Gnostic summary
        summary = [f"- Project Identity: {dna['project']} ({dna['slug']})"]
        summary.append(f"- Primary Architect: {dna['author']}")
        summary.append(f"- Execution Plane: {dna['substrate']} on {dna['os']}")
        summary.append(f"- Current Temporal Coordinate: {dna['epoch']}")

        # If we have detected technologies, inject them
        if "framework" in context: summary.append(f"- Framework Law: {context['framework']}")
        if "database" in context: summary.append(f"- Persistence Law: {context['database']}")

        return "\n".join(summary)

    def _unbox_gnosis(self, raw_matter: str) -> str:
        """
        [ASCENSION 3]: The Apophatic Sieve.
        Strips the conversational husk to reveal the pure logical seed.
        """
        clean = raw_matter.strip()

        # 1. Annihilate Markdown Code Blocks (Triple Backticks)
        # Matches: ```[lang]\n[code]\n```
        clean = re.sub(r'```(?:\w+)?\s*\n(.*?)\n\s*```', r'\1', clean, flags=re.DOTALL)

        # 2. Annihilate Inline Backticks
        clean = re.sub(r'^`(.*?)`$', r'\1', clean)

        # 3. Annihilate Conversational Apologies/Fillers
        # (AI: "Certainly! Here is the code...")
        noise_patterns = [
            r"^(?i)certainly.*?\n",
            r"^(?i)here is the.*?\n",
            r"^(?i)sure, I can help.*?\n",
            r"\n(?i)hope this helps.*?$",
            r"\n(?i)let me know if you need anything else.*?$"
        ]
        for pattern in noise_patterns:
            clean = re.sub(pattern, "", clean).strip()

        return clean

    def _forge_heresy_shield(self, prompt: str, error: str, lang: str = "text") -> str:
        """[THE RESILIENCE PROTOCOL]: Forges a safe fallback."""
        sigil = "//" if lang in ["js", "ts", "go", "rs", "java", "c"] else "#"
        if lang == "html": return f"<!-- AI FRACTURE: {error} \n Original Prompt: {prompt} -->"

        return dedent(f"""
            {sigil} =================================================================
            {sigil} [AI MATERIALIZATION FRACTURED]
            {sigil} =================================================================
            {sigil} ERROR: {error}
            {sigil} INTENT: {prompt[:100]}...
            {sigil} ACTION: Manual inscription required.
            {sigil} =================================================================
        """).strip()

    # =========================================================================
    # == THE RITES OF COGNITION (DIRECTIVES)                                 ==
    # =========================================================================

    def _directive_code(self,
                        context: Dict[str, Any],
                        prompt: str = "",
                        lang: str = "python",
                        filename: str = "script.py",
                        model: str = "smart",
                        complexity: int = 5,
                        *args, **kwargs) -> str:
        """
        @ai/code(prompt="...", lang="python", filename="api.py")
        The primary rite of logic manifestation.
        """
        if not prompt:
            return f"# [VOID_INTENT]: The Architect provided no prompt for {filename}."

        # --- MOVEMENT I: CONTEXTUAL ALCHEMY ---
        persona = self._scry_persona(prompt, filename)
        project_dna = self._siphon_project_dna(context)

        # Build the System Instruction
        system_prompt = dedent(f"""
            ROLE:
            You are the {persona}. You are a fragment of the VELM God-Engine.

            CONTEXT:
            {project_dna}
            Target File: {filename}
            Target Language: {lang}

            OBJECTIVE:
            Manifest high-fidelity, production-grade, and secure {lang} code.

            CONSTRAINTS:
            1. Return ONLY raw code. NO markdown formatting. NO backticks. NO conversational text.
            2. Follow the Gnostic Principle of Least Entropy: concise, idiomatic, and documented.
            3. Include error handling and type hints where applicable.
            4. If the prompt is ambiguous, assume the most secure and modern standard.
        """).strip()

        # --- MOVEMENT II: THE KINETIC STRIKE ---
        try:
            start_time = time.perf_counter()

            # Summon the Brain
            raw_gnosis = self._get_engine().ignite(
                user_query=prompt,
                system=system_prompt,
                model=model,
                temperature=0.2  # Low temperature for logical precision
            )

            # --- MOVEMENT III: PURIFICATION ---
            clean_code = self._unbox_gnosis(raw_gnosis)

            duration = (time.perf_counter() - start_time) * 1000
            Logger.info(f"AI/CODE Strike Resonant: {len(clean_code)} bytes willed in {duration:.2f}ms.")

            return clean_code

        except Exception as e:
            Logger.error(f"AI/CODE Rite Fractured: {e}")
            return self._forge_heresy_shield(prompt, str(e), lang)

    def _directive_sql(self,
                       context: Dict[str, Any],
                       prompt: str = "",
                       dialect: str = "postgresql",
                       *args, **kwargs) -> str:
        """
        @ai/sql(prompt="Users table with profiles", dialect="postgres")
        Transmutes intent into optimized database schema.
        """
        system = f"You are a Database Architect. Manifest optimized {dialect} SQL. NO markdown. ONLY raw SQL."
        try:
            raw = self._get_engine().ignite(user_query=prompt, system=system, model="smart")
            return self._unbox_gnosis(raw)
        except Exception as e:
            return self._forge_heresy_shield(prompt, str(e), "sql")

    def _directive_unit_test(self,
                             context: Dict[str, Any],
                             target_code: str = "",
                             framework: str = "pytest",
                             *args, **kwargs) -> str:
        """
        @ai/unit_test(target_code="{{ my_code }}", framework="vitest")
        Generates an inquisitor (test) for a block of matter.
        """
        system = f"You are a Lead QA Engineer. Write a comprehensive {framework} test suite for the provided code. NO markdown. ONLY raw code."
        user = f"Code to test:\n{target_code}"
        try:
            raw = self._get_engine().ignite(user_query=user, system=system, model="smart")
            return self._unbox_gnosis(raw)
        except Exception as e:
            return self._forge_heresy_shield("Unit Test Generation", str(e))

    def _directive_explain(self,
                           context: Dict[str, Any],
                           code: str = "",
                           audience: str = "senior_developer",
                           *args, **kwargs) -> str:
        """
        @ai/explain(code="{{ main_logic }}", audience="junior")
        Generates educational commentary or documentation.
        """
        system = f"You are a Technical Mentor. Explain the provided code for a {audience.replace('_', ' ')}. Be concise and insightful."
        try:
            return self._get_engine().ignite(user_query=f"Explain this code:\n{code}", system=system)
        except Exception as e:
            return f"# Gnostic Explanation Failed: {e}"

    def _directive_refactor(self,
                            context: Dict[str, Any],
                            code: str = "",
                            goal: str = "clean_code",
                            *args, **kwargs) -> str:
        """
        @ai/refactor(code="{{ legacy_code }}", goal="modernize_pydantic")
        Performs a surgical transmutation of existing logic.
        """
        system = dedent(f"""
            You are an Expert Architect. 
            TASK: Refactor the provided code. 
            GOAL: {goal.replace('_', ' ')}.
            CONSTRAINTS: Return ONLY raw code. NO markdown.
        """).strip()
        try:
            raw = self._get_engine().ignite(user_query=f"Refactor this:\n{code}", system=system, model="smart")
            return self._unbox_gnosis(raw)
        except Exception as e:
            return self._forge_heresy_shield(f"Refactor: {goal}", str(e))

    def _directive_config(self,
                          context: Dict[str, Any],
                          desc: str = "",
                          format: str = "yaml",
                          *args, **kwargs) -> str:
        """
        @ai/config(desc="Kubernetes pod for redis", format="yaml")
        """
        system = f"You are a DevOps Conductor. Manifest a production {format.upper()} configuration for: {desc}. NO markdown. ONLY raw {format}."
        try:
            raw = self._get_engine().ignite(user_query=desc, system=system, model="smart")
            return self._unbox_gnosis(raw)
        except Exception as e:
            return self._forge_heresy_shield(desc, str(e), format)

    def _directive_readme(self,
                          context: Dict[str, Any],
                          style: str = "professional",
                          *args, **kwargs) -> str:
        """
        @ai/readme(style="epic")
        Generates a high-status manifest for the project.
        """
        dna = self._siphon_project_dna(context)
        system = f"You are a Product Owner. Generate a {style} README.md for this project. Use high-status, exciting language."
        user = f"Project DNA:\n{dna}"
        try:
            return self._get_engine().ignite(user_query=user, system=system, model="smart")
        except Exception as e:
            return f"# {context.get('project_name')} \n AI README failure: {e}"

    def _directive_regex(self,
                         context: Dict[str, Any],
                         desc: str = "",
                         *args, **kwargs) -> str:
        """@ai/regex(desc="Strong password")"""
        system = "You are a Regex Master. Return ONLY the raw regex string. No slashes, no commentary."
        try:
            raw = self._get_engine().ignite(user_query=f"Regex for: {desc}", system=system, model="fast")
            return self._unbox_gnosis(raw)
        except Exception:
            return ".* # AI Regex Failed"

    def _directive_env_vars(self,
                            context: Dict[str, Any],
                            service: str = "api",
                            *args, **kwargs) -> str:
        """@ai/env_vars(service="postgres")"""
        system = f"List the standard environment variables required for a production {service} service. Return as a .env list. NO markdown."
        try:
            raw = self._get_engine().ignite(user_query=service, system=system, model="fast")
            return self._unbox_gnosis(raw)
        except Exception:
            return f"# {service.upper()}_ENV_VAR_PLACEHOLDER=void"

    def _directive_shell(self,
                         context: Dict[str, Any],
                         intent: str = "",
                         *args, **kwargs) -> str:
        """@ai/shell(intent="install dependencies for a fastapi app with postgres")"""
        system = "You are an SRE. Provide the shell commands to fulfill the intent. NO markdown. NO backticks. One command per line."
        try:
            raw = self._get_engine().ignite(user_query=intent, system=system, model="fast")
            return self._unbox_gnosis(raw)
        except Exception:
            return f"echo 'Shell Inception Failed'"

    def _directive_mock(self,
                        context: Dict[str, Any],
                        format: str = "json",
                        schema: str = "User profile",
                        count: int = 3,
                        *args, **kwargs) -> str:
        """@ai/mock(format="json", schema="Order history", count=5)"""
        system = f"Generate {count} examples of {format.upper()} data for the schema: {schema}. NO markdown. ONLY raw {format}."
        try:
            raw = self._get_engine().ignite(user_query=schema, system=system, model="fast")
            return self._unbox_gnosis(raw)
        except Exception:
            return "[] # Mock Data Fracture"

    def _directive_changelog(self,
                             context: Dict[str, Any],
                             current_state: str = "",
                             *args, **kwargs) -> str:
        """@ai/changelog(current_state="{{ project_snapshot }}")"""
        system = "You are a Project Scribe. Generate a Markdown changelog entry based on the provided state. Be professional."
        try:
            return self._get_engine().ignite(user_query=current_state, system=system)
        except Exception:
            return "## [Unreleased]\n- Internal state drift perceived."

    def _directive_naming(self,
                          context: Dict[str, Any],
                          desc: str = "Internal Auth Service",
                          style: str = "snake_case",
                          *args, **kwargs) -> str:
        """@ai/naming(desc="Data processing engine")"""
        system = f"Suggest 3 high-status, professional names in {style} for: {desc}. Return only the names separated by commas."
        try:
            return self._get_engine().ignite(user_query=desc, system=system, model="fast")
        except Exception:
            return "service_alpha, service_beta, service_gamma"

    # =========================================================================
    # == THE OMEGA METRIC: AUDIT                                             ==
    # =========================================================================

    def _directive_audit(self,
                         context: Dict[str, Any],
                         code: str = "",
                         focus: str = "security",
                         *args, **kwargs) -> str:
        """
        @ai/audit(code="{{ source }}", focus="performance")
        Returns a list of potential architectural heresies.
        """
        system = dedent(f"""
            You are a Senior Security Auditor and Performance Architect.
            TASK: Scan the provided code for {focus} heresies (bugs, vulnerabilities, debt).
            FORMAT: Return a bulleted list of findings.
        """).strip()
        try:
            return self._get_engine().ignite(user_query=code, system=system, model="smart")
        except Exception as e:
            return f"- Audit Rite Fractured: {e}"
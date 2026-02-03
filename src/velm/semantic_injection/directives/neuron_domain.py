# scaffold/semantic_injection/directives/neuron_domain.py

"""
=================================================================================
== THE CORTEX BUILDER (V-Ω-NEURON-DOMAIN)                                      ==
=================================================================================
LIF: 10,000,000,000,000

This artisan implements the `@neuron` namespace. It is the High Priest of AI
Engineering. It does not just write code; it builds **Cognitive Architectures**.

It integrates with the `neuron_knowledge` library to generate robust,
best-practice implementations for RAG, Agents, and LLM connectivity.

Usage:
    # 1. Infrastructure
    services/llm.py :: @neuron/client(provider="openai")
    services/local_llm.py :: @neuron/client(provider="ollama", base="http://host.docker.internal:11434")

    # 2. Memory (RAG)
    services/memory.py :: @neuron/rag(db="pgvector")

    # 3. Structured Data
    extractors/user.py :: @neuron/structure(model="User", fields="name:str, bio:str")

    # 4. Tools
    tools/search.py :: @neuron/tool(name="SearchWeb", desc="Searches the internet")

=================================================================================
"""
from typing import Dict, Any

# The Divine Summons of the Knowledge Library
from .neuron_knowledge import providers, memory, agents, orchestration, optimization, edge, evaluation
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("neuron")
class NeuronDomain(BaseDirectiveDomain):
    """
    The Architect of Artificial Minds.
    """

    @property
    def namespace(self) -> str:
        return "neuron"

    def help(self) -> str:
        return "Generates AI infrastructure: RAG pipelines, LLM clients, Agents, and Structured Data."

    # =========================================================================
    # == THE RITE OF CONNECTION                                              ==
    # =========================================================================

    def _directive_client(self, context: Dict[str, Any], provider: str = "openai", base: str = "",
                          async_mode: bool = True, *args, **kwargs) -> str:
        """
        @neuron/client(provider="ollama", base="http://localhost:11434")
        Generates a robust, configured LLM client.
        """
        return providers.forge_client_setup(
            provider=provider,
            async_mode=str(async_mode).lower() == 'true',
            custom_base=base
        )

    # =========================================================================
    # == THE RITE OF MEMORY                                                  ==
    # =========================================================================

    def _directive_rag(self, context: Dict[str, Any], db: str = "chroma", embed: str = "openai", *args,
                       **kwargs) -> str:
        """
        @neuron/rag(db="pgvector")
        Generates a full RAG pipeline class.
        """
        return memory.forge_rag_pipeline(vector_db=db, embedding=embed)

    # =========================================================================
    # == THE RITE OF STRUCTURE                                               ==
    # =========================================================================

    def _directive_structure(self, context: Dict[str, Any], model: str, fields: str, *args, **kwargs) -> str:
        """
        @neuron/structure(model="Invoice", fields="id:str, total:float, items:List[str]")
        Generates a Pydantic model + Instructor wrapper for structured LLM output.
        """
        return agents.forge_structured_extractor(model_name=model, fields=fields)

    # =========================================================================
    # == THE RITE OF AGENCY                                                  ==
    # =========================================================================

    def _directive_tool(self, context: Dict[str, Any], name: str, desc: str, *args, **kwargs) -> str:
        """
        @neuron/tool(name="Calculator", desc="Performs math")
        Generates a LangChain/OpenAI tool definition.
        """
        return agents.forge_tool_definition(tool_name=name, desc=desc)

    def _directive_crew(self, context: Dict[str, Any], agents: str = "Researcher,Writer", hierarchy: str = "sequential",
                        *args, **kwargs) -> str:
        """
        @neuron/crew(agents="Researcher,Writer", hierarchy="sequential")
        Generates a Multi-Agent System using CrewAI.
        """
        return orchestration.forge_crew_structure(
            agents_csv=agents,
            process=hierarchy
        )

    def _directive_dspy(self, context: Dict[str, Any], signature: str, name: str = "Cognitive",
                        strategy: str = "ChainOfThought", *args, **kwargs) -> str:
        """
        @neuron/dspy(signature="context, question -> reasoning, answer")
        Generates a DSPy optimization pipeline.
        """
        return optimization.forge_dspy_module(
            classname=name,
            signature=signature,
            strategy=strategy
        )

    def _directive_service(self, context: Dict[str, Any], model: str = "llama3", runtime: str = "ollama", port: int = 0,
                           gpu: str = "true", *args, **kwargs) -> str:
        """
        @neuron/service(model="mistral", runtime="ollama", gpu="true")
        Generates a Docker Compose service for local LLM inference.
        """
        # Smart Defaults based on Runtime
        final_port = port
        if not final_port:
            if runtime == "ollama":
                final_port = 11434
            elif runtime == "vllm":
                final_port = 8000
            elif runtime == "llamacpp":
                final_port = 8080

        is_gpu = str(gpu).lower() in ('true', '1', 'yes')

        return edge.forge_inference_service(
            runtime=runtime,
            model=model,
            port=final_port,
            gpu=is_gpu
        )

    def _directive_setup_script(self, context: Dict[str, Any], runtime: str = "ollama", model: str = "llama3", *args,
                                **kwargs) -> str:
        """
        @neuron/setup_script(model="llama3")
        Generates a shell script to pull the model into the running service.
        """
        return edge.forge_model_puller(runtime=runtime, model=model)

    def _directive_eval(self, context: Dict[str, Any], framework: str = "deepeval",
                        metrics: str = "hallucination,relevance", target: str = "ai_feature", *args, **kwargs) -> str:
        """
        @neuron/eval(framework="deepeval", metrics="hallucination,toxicity")
        Generates an evaluation test suite for AI outputs.
        """
        return evaluation.forge_eval_suite(
            framework=framework,
            metrics=metrics,
            target=target
        )

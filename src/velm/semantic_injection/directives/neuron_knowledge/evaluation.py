# scaffold/semantic_injection/directives/neuron_knowledge/evaluation.py

"""
=================================================================================
== THE INQUISITOR OF TRUTH (V-Ω-EVAL-BUILDER)                                  ==
=================================================================================
LIF: 10,000,000,000,000,000

This artisan generates rigorous evaluation pipelines for AI systems.
It constructs Unit Tests (DeepEval) or Benchmarks (Ragas) to scientifically
measure Hallucination, Relevance, and Safety.

Usage:
    @neuron/eval(framework="deepeval", metrics="hallucination:0.3, toxicity")
=================================================================================
"""
from contextlib import contextmanager
from typing import List, Dict, Set, Tuple


# =============================================================================
# == THE GNOSTIC CODE BUILDER (STANDARD)                                     ==
# =============================================================================

class GnosticCodeBuilder:
    """
    A stateful engine for constructing indented code without string-mashing.
    """

    def __init__(self, indent_char: str = "    "):
        self.lines: List[str] = []
        self.level: int = 0
        self.indent_char: str = indent_char
        self.imports: Set[str] = set()
        self.from_imports: Dict[str, Set[str]] = {}
        self.metadata: List[str] = []

    def add_import(self, module: str):
        self.imports.add(module)

    def add_from_import(self, module: str, name: str):
        if module not in self.from_imports:
            self.from_imports[module] = set()
        self.from_imports[module].add(name)

    def add_metadata(self, key: str, value: str):
        self.metadata.append(f"# {key}: {value}")

    def add(self, line: str = ""):
        if not line:
            self.lines.append("")
        else:
            self.lines.append((self.indent_char * self.level) + line)

    @contextmanager
    def block(self, header: str):
        self.add(header)
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1
            self.add("")

    def render(self) -> str:
        output = []
        if self.metadata:
            output.extend(self.metadata)
            output.append("")

        if self.imports:
            output.extend([f"import {m}" for m in sorted(self.imports)])
        if self.from_imports:
            for mod in sorted(self.from_imports.keys()):
                names = ", ".join(sorted(self.from_imports[mod]))
                output.append(f"from {mod} import {names}")

        if self.imports or self.from_imports:
            output.append("")
            output.append("")

        output.extend(self.lines)
        return "\n".join(output).strip()


# =============================================================================
# == THE FORGE (GENERATION LOGIC)                                            ==
# =============================================================================

def forge_eval_suite(
        framework: str = "deepeval",
        metrics: str = "hallucination",
        target: str = "rag_pipeline"
) -> str:
    """
    Forges a comprehensive Evaluation Suite.
    """
    cb = GnosticCodeBuilder()

    # Parse Metrics: "hallucination:0.5, toxicity" -> [('hallucination', 0.5), ('toxicity', None)]
    parsed_metrics = []
    for m in metrics.split(','):
        parts = m.strip().split(':')
        name = parts[0].lower()
        thresh = float(parts[1]) if len(parts) > 1 else None
        parsed_metrics.append((name, thresh))

    cb.add_import("os")

    if framework == "deepeval":
        return _forge_deepeval(cb, parsed_metrics, target)
    elif framework == "ragas":
        return _forge_ragas(cb, parsed_metrics, target)
    else:
        return "# Unknown framework. Use 'deepeval' or 'ragas'."


def _forge_deepeval(cb: GnosticCodeBuilder, metrics: List[Tuple[str, float]], target: str) -> str:
    """
    Constructs a Pytest-compatible DeepEval suite.
    """
    cb.add_metadata("requirements", "deepeval, pytest, openai")
    cb.add_metadata("description", "AI Unit Tests using DeepEval")

    cb.add_import("pytest")
    cb.add_from_import("deepeval", "assert_test")
    cb.add_from_import("deepeval.test_case", "LLMTestCase")

    metric_vars = []

    # Metric instantiation logic
    metric_definitions = []

    for name, threshold in metrics:
        # Defaults
        t_val = threshold if threshold is not None else 0.5

        if "hallucination" in name:
            cb.add_from_import("deepeval.metrics", "HallucinationMetric")
            metric_definitions.append(f"hallucination = HallucinationMetric(threshold={t_val})")
            metric_vars.append("hallucination")
        elif "relevan" in name:  # Matches relevance, answer_relevancy
            cb.add_from_import("deepeval.metrics", "AnswerRelevancyMetric")
            metric_definitions.append(f"relevancy = AnswerRelevancyMetric(threshold={t_val})")
            metric_vars.append("relevancy")
        elif "toxic" in name:
            cb.add_from_import("deepeval.metrics", "ToxicityMetric")
            metric_definitions.append(f"toxicity = ToxicityMetric(threshold={t_val})")
            metric_vars.append("toxicity")
        elif "bias" in name:
            cb.add_from_import("deepeval.metrics", "BiasMetric")
            metric_definitions.append(f"bias = BiasMetric(threshold={t_val})")
            metric_vars.append("bias")

    # --- The Test Function ---
    with cb.block(f"def test_{target}_quality():"):
        cb.add(f'"""Adjudicates the quality of the {target}."""')

        # Mock Data
        cb.add("# 1. Define the Gnostic Reality (Mock Data)")
        cb.add('input_query = "What is the primary directive?"')
        cb.add('actual_output = "To facilitate Symbiotic Creation."')
        cb.add('retrieval_context = ["The Scaffold Engine\'s primary directive is Symbiotic Creation."]')

        cb.add("")
        cb.add("# 2. Forge the Test Case")
        with cb.block("test_case = LLMTestCase("):
            cb.add("input=input_query,")
            cb.add("actual_output=actual_output,")
            cb.add("retrieval_context=retrieval_context")
        cb.add(")")

        cb.add("")
        cb.add("# 3. Initialize Inquisitors (Metrics)")
        for definition in metric_definitions:
            cb.add(definition)

        cb.add("")
        cb.add("# 4. The Rite of Judgment")
        cb.add(f"assert_test(test_case, [{', '.join(metric_vars)}])")

    # --- Main Guard ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        cb.add("# [ELEVATION] Environment Sentinel")
        with cb.block("if not os.getenv('OPENAI_API_KEY'):"):
            cb.add("print('[Warning] OPENAI_API_KEY is missing. DeepEval requires an LLM Judge.')")

        cb.add("print('To execute this inquisition, run:')")
        cb.add(f"print('pytest {{__file__}}')")

    return cb.render()


def _forge_ragas(cb: GnosticCodeBuilder, metrics: List[Tuple[str, float]], target: str) -> str:
    """
    Constructs a Ragas benchmark suite.
    """
    cb.add_metadata("requirements", "ragas, datasets, pandas, openai")
    cb.add_metadata("description", "RAG Evaluation Pipeline using Ragas")

    cb.add_from_import("datasets", "Dataset")
    cb.add_from_import("ragas", "evaluate")

    metric_vars = []

    for name, _ in metrics:
        if "faith" in name:
            cb.add_from_import("ragas.metrics", "faithfulness")
            metric_vars.append("faithfulness")
        elif "answer" in name and "relev" in name:
            cb.add_from_import("ragas.metrics", "answer_relevancy")
            metric_vars.append("answer_relevancy")
        elif "context" in name and "prec" in name:
            cb.add_from_import("ragas.metrics", "context_precision")
            metric_vars.append("context_precision")
        elif "context" in name and "rec" in name:
            cb.add_from_import("ragas.metrics", "context_recall")
            metric_vars.append("context_recall")

    # --- The Evaluation Function ---
    with cb.block(f"def evaluate_{target}():"):
        cb.add('"""Conducts a Ragas evaluation on the Gnostic Dataset."""')

        # Mock Data Construction
        cb.add("# 1. Prepare the Gnostic Dataset")
        with cb.block("data_samples = {"):
            cb.add("'question': ['How do I define a directive?', 'What is the Alchemist?'],")
            cb.add("'answer': ['Use the @ symbol followed by the namespace.', 'It handles variable transmutation.'],")
            cb.add(
                "'contexts': [['Directives are defined in neuron_domain.py'], ['The Alchemist resolves Jinja templates.']],")
            cb.add("'ground_truth': ['Use @namespace/directive', 'A component for variable resolution']")
        cb.add("}")

        cb.add("dataset = Dataset.from_dict(data_samples)")

        cb.add("")
        cb.add("# 2. The Rite of Judgment")
        cb.add(f"print(f'Evaluating with metrics: {metric_vars}')")

        with cb.block("score = evaluate("):
            cb.add("dataset,")
            cb.add(f"metrics=[{', '.join(metric_vars)}],")
        cb.add(")")

        cb.add("")
        cb.add("# 3. Proclaim Results")
        cb.add("print(f'Evaluation Scores: {score}')")
        cb.add("df = score.to_pandas()")
        cb.add("df.to_csv('evaluation_report.csv')")
        cb.add("print('Detailed report inscribed to evaluation_report.csv')")

    # --- Main Guard ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        with cb.block("if not os.getenv('OPENAI_API_KEY'):"):
            cb.add("print('[Error] OPENAI_API_KEY required for Ragas evaluation.')")
            cb.add("exit(1)")

        cb.add(f"evaluate_{target}()")

    return cb.render()
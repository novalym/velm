# scaffold/semantic_injection/directives/neuron_knowledge/optimization.py

"""
=================================================================================
== THE COGNITIVE ARCHITECT (V-Ω-DSPY-SYNTHESIZER)                              ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This artisan is a compiler. It translates high-level Gnostic Intent (signatures,
strategies) into a production-grade, self-optimizing Neural Network using DSPy.

It features a 'Quote Guard' to prevent syntax heresies and a 'Context Engine'
to inject dependencies dynamically.
=================================================================================
"""
import re
from contextlib import contextmanager
from typing import List, Dict, Tuple, Set


# =============================================================================
# == THE GNOSTIC CODE SYNTHESIZER                                            ==
# =============================================================================

class GnosticCodeBuilder:
    """
    A stateful compiler that manages indentation, imports, and quote safety.
    """

    def __init__(self):
        self.lines: List[str] = []
        self.level: int = 0
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
        """Adds a line at the current indentation level."""
        if not line:
            self.lines.append("")
        else:
            self.lines.append(("    " * self.level) + line)

    def add_comment(self, text: str):
        self.add(f"# {text}")

    @contextmanager
    def block(self, header: str):
        """Creates an indented block (class, def, if, etc.)."""
        self.add(header)
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1
            self.add("")  # Spacing after blocks

    def render(self) -> str:
        """Compiles the Gnostic State into the final Python scripture."""
        # 1. Metadata Headers
        output = []
        if self.metadata:
            output.extend(self.metadata)
            output.append("")

        # 2. Imports (Sorted & Deduplicated)
        if self.imports:
            output.extend([f"import {m}" for m in sorted(self.imports)])
        if self.from_imports:
            for mod in sorted(self.from_imports.keys()):
                names = ", ".join(sorted(self.from_imports[mod]))
                output.append(f"from {mod} import {names}")

        if self.imports or self.from_imports:
            output.append("")
            output.append("")

        # 3. Code Body
        output.extend(self.lines)

        return "\n".join(output).strip()


# =============================================================================
# == THE PARSING LOGIC                                                       ==
# =============================================================================

def _parse_field(field_str: str) -> Tuple[str, str]:
    """
    Parses 'name "description"' or 'name'.
    Returns (name, description).
    """
    match = re.match(r'^\s*(\w+)(?:\s+["\']([^"\']+)["\'])?', field_str.strip())
    if match:
        name = match.group(1)
        # Fallback description is derived from the name
        desc = match.group(2) or f"The {name.replace('_', ' ')}"
        return name, desc
    return field_str.strip(), f"The {field_str.strip()}"


def _parse_signature(sig_str: str) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
    """Parses the input -> output syntax."""
    if "->" not in sig_str:
        return [("input", "Input data")], [("output", "Model response")]

    inputs_part, outputs_part = sig_str.split("->")
    inputs = [_parse_field(f) for f in inputs_part.split(",") if f.strip()]
    outputs = [_parse_field(f) for f in outputs_part.split(",") if f.strip()]
    return inputs, outputs


# =============================================================================
# == THE FORGE (GENERATION LOGIC)                                            ==
# =============================================================================

def forge_dspy_module(
        classname: str = "Cognitive",
        signature: str = "question -> answer",
        strategy: str = "ChainOfThought",
        optimizer: str = "BootstrapFewShot",
        metric: str = "answer_exact_match"
) -> str:
    """
    The Grand Architect of Neural Modules.
    Constructs a bulletproof, self-contained DSPy script.
    """
    cb = GnosticCodeBuilder()

    # --- 1. Gnostic Configuration ---
    cb.add_metadata("requirements", "dspy-ai, openai")
    cb.add_metadata("description", f"Self-optimizing {classname} agent using {strategy}")

    cb.add_import("os")
    cb.add_import("dspy")

    inputs, outputs = _parse_signature(signature)

    # --- 2. The Signature Class ---
    sig_classname = f"{classname}Signature"
    with cb.block(f"class {sig_classname}(dspy.Signature):"):
        cb.add(f'"""{classname} System Signature: {signature}"""')
        cb.add("")

        for name, desc in inputs:
            cb.add(f"{name} = dspy.InputField(desc=\"{desc}\")")

        for name, desc in outputs:
            cb.add(f"{name} = dspy.OutputField(desc=\"{desc}\")")

    # --- 3. The Module Class ---
    mod_classname = f"{classname}Module"
    with cb.block(f"class {mod_classname}(dspy.Module):"):

        # __init__
        with cb.block("def __init__(self):"):
            cb.add("super().__init__()")

            # [INTELLIGENCE] RAG Auto-Detection
            has_context = any(i[0].lower() == 'context' for i in inputs)
            if has_context:
                cb.add_comment("RAG Detected: Initializing retriever")
                cb.add("self.retrieve = dspy.Retrieve(k=3)")

            # [INTELLIGENCE] Strategy Selection
            cb.add_comment(f"Strategy: {strategy} (Adds reasoning steps)")
            if strategy == "ChainOfThought":
                cb.add(f"self.prog = dspy.ChainOfThought({sig_classname})")
            elif strategy == "ReAct":
                cb.add(f"self.prog = dspy.ReAct({sig_classname})")
            else:
                cb.add(f"self.prog = dspy.Predict({sig_classname})")

        # forward
        input_args = ", ".join([i[0] for i in inputs])
        with cb.block(f"def forward(self, {input_args}):"):
            if has_context:
                cb.add_comment("Auto-Retrieve context if passed as None (Conceptual)")
                # Logic could be added here to use self.retrieve

            call_args = ", ".join([f"{i[0]}={i[0]}" for i in inputs])
            cb.add(f"return self.prog({call_args})")

    # --- 4. The Optimizer Function ---
    cb.add_from_import("dspy.teleprompt", optimizer)

    with cb.block("def optimize_pipeline(trainset, valset=None):"):
        cb.add(f'"""Optimizes the {classname} module using {optimizer}."""')

        # [INTELLIGENCE] Metric Factory
        if metric == "answer_exact_match":
            cb.add("metric = dspy.evaluate.answer_exact_match")
        else:
            # Fallback or custom metric placeholder
            cb.add_comment("Custom metric placeholder")
            with cb.block("def custom_metric(gold, pred, trace=None):"):
                cb.add("return gold.answer.lower() == pred.answer.lower()")
            cb.add("metric = custom_metric")

        # Optimizer Configuration
        opt_params = "metric=metric"
        if optimizer == "BootstrapFewShot":
            opt_params += ", max_bootstrapped_demos=4, max_labeled_demos=4"

        cb.add("")
        cb.add(f"teleprompter = {optimizer}({opt_params})")
        cb.add(f"print(f'[Optimization] Compiling {mod_classname} with {optimizer}...')")

        with cb.block("try:"):
            cb.add(f"compiled_prog = teleprompter.compile({mod_classname}(), trainset=trainset, valset=valset)")
            cb.add("return compiled_prog")
        with cb.block("except Exception as e:"):
            cb.add("print(f'[Warning] Optimization failed: {e}')")
            cb.add(f"return {mod_classname}() # Return unoptimized fallback")

    # --- 5. The Main Execution Guard ---
    with cb.block('if __name__ == "__main__":'):

        # [INTELLIGENCE] Environment Sentinel
        with cb.block("if not os.getenv('OPENAI_API_KEY'):"):
            cb.add("print('[Error] OPENAI_API_KEY not found in environment.')")
            cb.add("print('Please set it via: export OPENAI_API_KEY=sk-...')")
            cb.add("exit(1)")

        cb.add_comment("1. Configuration")
        cb.add("lm = dspy.OpenAI(model='gpt-3.5-turbo')")
        cb.add("dspy.settings.configure(lm=lm)")

        cb.add("")
        cb.add_comment("2. Instantiation")
        cb.add(f"agent = {mod_classname}()")

        cb.add("")
        cb.add_comment("3. Zero-Shot Inference")

        # [INTELLIGENCE] The Quote Guard Fix
        # We construct the print statement carefully to avoid quote collision.
        # We use double quotes for the f-string, and single quotes for the data.

        call_args_list = []
        print_args_list = []

        for i in inputs:
            # Example: question='What is the capital of Mars?'
            val = f"Example {i[0]}"
            call_args_list.append(f"{i[0]}='{val}'")
            print_args_list.append(f"{i[0]}='{val}'")

        call_str = ", ".join(call_args_list)
        print_str = ", ".join(print_args_list)

        # The specific fix: ensure the outer f-string uses double quotes so single quotes inside work
        cb.add(f'print(f"[Run] Predicting: {print_str}...")')

        with cb.block("try:"):
            cb.add(f"pred = agent({call_str})")

            # Output Logging
            first_output_name = outputs[0][0]
            cb.add(f"print(f'[Result] {first_output_name}: {{pred.{first_output_name}}}')")

            if strategy == "ChainOfThought":
                cb.add("if hasattr(pred, 'rationale'):")
                cb.add("    print(f'[Reasoning] {pred.rationale}')")

        with cb.block("except Exception as e:"):
            cb.add("print(f'[Error] Inference failed: {e}')")

        cb.add("")
        cb.add_comment("4. Inspection")
        cb.add("lm.inspect_history(n=1)")

    return cb.render()
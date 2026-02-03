# scaffold/forge/instruction_forger.py

import json
from typing import List, Dict, Any
from pathlib import Path
from ..core.ai.engine import AIEngine
from ..logger import Scribe
from rich.progress import track

Logger = Scribe("InstructionForger")


class InstructionForger:
    """
    =============================================================================
    == THE SCRIBE OF PEDAGOGY (V-Ω-SYNTHETIC-DATA-GEN)                         ==
    =============================================================================
    Uses a Teacher Model (Smart AI) to create training data for the Student Model.
    It looks at code and hallucinates the prompt that *would have* created it.
    """

    SYSTEM_PROMPT = """
    You are an expert developer creating a dataset for instruction tuning an LLM.
    I will provide you with a file's content and its path.
    Your task is to generate a realistic "Instruction" that a user would give to an AI to generate this exact code.

    The Output format must be valid JSON:
    {
        "instruction": "The natural language request",
        "input": "Any necessary context (optional, usually empty for code gen)",
        "output": "The provided code content"
    }

    If the code is a Scaffold blueprint (.scaffold), the instruction should be about "scaffolding" or "generating architecture".
    """

    def __init__(self):
        self.ai = AIEngine.get_instance()

    def forge_dataset(self, raw_corpus: List[Dict[str, str]], output_path: Path, limit: int = None):
        """
        Transmutes raw corpus into a JSONL dataset.
        """
        dataset = []
        candidates = raw_corpus[:limit] if limit else raw_corpus

        Logger.info(f"Forging instructions for {len(candidates)} scriptures. This may take time...")

        with open(output_path, 'w', encoding='utf-8') as f:
            for item in track(candidates, description="Forging Synthetic Wisdom..."):
                try:
                    # Construct the prompt for the Teacher
                    user_query = f"FILE_PATH: {item['path']}\n\nCONTENT:\n```\n{item['content'][:8000]}\n```"  # Truncate to fit context

                    response = self.ai.ignite(
                        user_query=user_query,
                        system=self.SYSTEM_PROMPT,
                        model="smart",  # Use the best model available to teach
                        json_mode=True
                    )

                    data = json.loads(response)

                    # Ensure the output is the actual code, not the AI's summary of it
                    data['output'] = item['content']

                    # Write immediately to stream
                    f.write(json.dumps(data) + "\n")
                    dataset.append(data)

                except Exception as e:
                    Logger.warn(f"Failed to forge instruction for {item['path']}: {e}")

        Logger.success(f"Dataset inscribed at {output_path}. {len(dataset)} training examples forged.")
        return dataset
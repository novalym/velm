# scaffold/forge/adapters/huggingface.py

import sys
import subprocess
from pathlib import Path
from typing import Dict, Any
from .base import TrainingAdapter
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("HuggingFaceAdapter")


class HuggingFaceAdapter(TrainingAdapter):
    """
    =============================================================================
    == THE IRON ALCHEMIST (V-Ω-PEFT-LORA-TRAINER)                              ==
    =============================================================================
    Trains models using the HuggingFace ecosystem (transformers, peft, trl).
    Optimized for QLoRA (4-bit quantization) to run on consumer GPUs.
    """

    TRAINING_SCRIPT = """
import sys
import json
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
import torch

def train(dataset_path, base_model_id, output_dir, epochs, batch_size, lr):
    print(f"Loading base model: {base_model_id}...")

    # Quantization Config (4-bit for efficiency)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
    )

    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        quantization_config=bnb_config,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    dataset = load_dataset('json', data_files=dataset_path, split="train")

    def formatting_prompts_func(example):
        output_texts = []
        for i in range(len(example['instruction'])):
            text = f"### Instruction: {example['instruction'][i]}\\n### Input: {example['input'][i]}\\n### Response: {example['output'][i]}"
            output_texts.append(text)
        return output_texts

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        peft_config=peft_config,
        formatting_func=formatting_prompts_func,
        args=TrainingArguments(
            per_device_train_batch_size=int(batch_size),
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=-1, # use epochs
            num_train_epochs=int(epochs),
            learning_rate=float(lr),
            fp16=True,
            logging_steps=1,
            output_dir=output_dir,
            optim="paged_adamw_8bit"
        ),
    )

    print("Igniting the Neural Forge...")
    trainer.train()
    print("Training complete. Saving adapter...")
    trainer.save_model(output_dir)

if __name__ == "__main__":
    train(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
"""

    def train(self, dataset_path: Path, model_name: str, output_dir: Path, params: Dict[str, Any]):
        # 1. Dependency Check
        self._check_deps()

        # 2. Materialize Training Script
        script_path = self.root / ".scaffold" / "cache" / "train_lora.py"
        script_path.parent.mkdir(parents=True, exist_ok=True)
        script_path.write_text(self.TRAINING_SCRIPT, encoding='utf-8')

        Logger.info(f"Summoning the Iron Alchemist to train '{params.get('base_model')}'...")
        Logger.info("This rite requires a GPU (NVIDIA) and Patience.")

        cmd = [
            sys.executable, str(script_path),
            str(dataset_path),
            params.get("base_model"),
            str(output_dir),
            str(params.get("epochs", 1)),
            str(params.get("batch_size", 2)),
            str(params.get("learning_rate", 2e-4))
        ]

        try:
            # We stream output to show progress bars
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                print(line, end='')

            process.wait()

            if process.returncode == 0:
                Logger.success(f"LoRA Adapter forged at: {output_dir}")
                Logger.info("To use this model, you must load it with the base model using an inference server.")
            else:
                raise ArtisanHeresy("The training process collapsed.", details="Check CUDA/VRAM availability.")

        except KeyboardInterrupt:
            process.kill()
            Logger.warn("Training interrupted by Architect.")

    def _check_deps(self):
        try:
            import torch
            import transformers
            import peft
            import trl
            import bitsandbytes
        except ImportError as e:
            raise ArtisanHeresy(
                "The Iron Alchemist lacks materials.",
                suggestion="pip install torch transformers peft trl bitsandbytes accelerate scipy",
                child_heresy=e
            )
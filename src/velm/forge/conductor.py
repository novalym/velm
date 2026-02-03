# scaffold/forge/conductor.py

from pathlib import Path
from typing import Optional

from .corpus_harvester import CorpusHarvester
from .instruction_forger import InstructionForger
from .adapters.huggingface import HuggingFaceAdapter
from ..logger import Scribe
from ..interfaces.requests import TrainRequest

Logger = Scribe("ForgeConductor")


class ForgeConductor:
    """
    The High Priest of the Gnostic Forge.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.harvester = CorpusHarvester(project_root)
        self.forger = InstructionForger()

        # Future: Factory for adapters
        self.adapter = HuggingFaceAdapter(project_root)

    def conduct_training_rite(self, request: TrainRequest):
        Logger.info(f"Initiating Ouroboros Protocol: Training '{request.output_model_name}'...")

        # 1. Harvest
        Logger.info("Phase I: Harvesting the Corpus...")
        corpus = self.harvester.harvest()

        if not corpus:
            Logger.warn("No Gnosis found. The training cannot proceed on a void.")
            return

        # 2. Forge Dataset
        dataset_path = self.root / ".scaffold" / "datasets" / f"{request.output_model_name}.jsonl"
        dataset_path.parent.mkdir(parents=True, exist_ok=True)

        if request.generate_instructions:
            Logger.info("Phase II: Synthesizing Instructions (Self-Instruct)...")
            self.forger.forge_dataset(corpus, dataset_path, limit=request.limit_samples)
        else:
            # TODO: Handle raw text training or manual datasets
            Logger.warn("Raw pre-training not yet implemented. Use --generate-instructions.")
            return

        # 3. Train
        Logger.info("Phase III: The Alchemical Fire (Training)...")
        output_dir = self.root / ".scaffold" / "models" / request.output_model_name

        self.adapter.train(
            dataset_path=dataset_path,
            model_name=request.output_model_name,
            output_dir=output_dir,
            params=request.model_dump()
        )
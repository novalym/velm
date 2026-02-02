# scaffold/forge/adapters/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any


class TrainingAdapter(ABC):
    """
    The Sacred Contract for AI Training Backends.
    """

    def __init__(self, project_root: Path):
        self.root = project_root

    @abstractmethod
    def train(self, dataset_path: Path, model_name: str, output_dir: Path, params: Dict[str, Any]):
        """
        Conducts the Rite of Training.
        """
        pass


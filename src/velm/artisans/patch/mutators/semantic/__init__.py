
from abc import ABC
from .....logger import Scribe

Logger = Scribe("MutatorBase")

class BaseMutator(ABC):
    """
    The Ancestral Soul of all Mutators.
    Provides shared Gnosis for logging and basic validation.
    """
    pass
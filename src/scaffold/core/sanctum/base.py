# Path: scaffold/core/sanctum/base.py
# -----------------------------------

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class SanctumInterface(ABC):
    """
    =================================================================================
    == THE SACRED CONTRACT OF THE SANCTUM (V-Ω-INTERFACE-ULTIMA)                   ==
    =================================================================================
    LIF: 10,000,000,000

    The Abstract Soul of a Filesystem.
    Defines the Gnostic rites for interacting with any reality (Local, SSH, S3, Memory).
    """

    @property
    @abstractmethod
    def uri(self) -> str:
        """The connection string identifying this sanctum (e.g., ssh://user@host/path)."""
        pass

    @property
    @abstractmethod
    def root(self) -> Union[Path, str]:
        """
        The foundational anchor of this reality.
        - Local: A `pathlib.Path` object.
        - Remote/Cloud: A string representation of the base path/key.
        """
        pass

    @property
    @abstractmethod
    def is_local(self) -> bool:
        """
        Adjudicates if the sanctum exists within the mortal coil (Local Disk).
        True enables optimizations like 'git show' and direct shell execution.
        """
        pass

    @abstractmethod
    def resolve_path(self, path: Union[str, Path]) -> str:
        """Normalizes a relative path to the absolute path in the target reality."""
        pass

    @abstractmethod
    def exists(self, path: Union[str, Path]) -> bool:
        """Gazes into the reality to see if a form exists."""
        pass

    @abstractmethod
    def is_dir(self, path: Union[str, Path]) -> bool:
        """Adjudicates if the form is a container (directory)."""
        pass

    @abstractmethod
    def is_file(self, path: Union[str, Path]) -> bool:
        """Adjudicates if the form is a scripture (file)."""
        pass

    @abstractmethod
    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        """Forges a new container in the reality."""
        pass

    @abstractmethod
    def write_bytes(self, path: Union[str, Path], data: bytes):
        """Inscribes raw entropy into the reality."""
        pass

    @abstractmethod
    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        """Inscribes luminous text into the reality."""
        pass

    @abstractmethod
    def read_bytes(self, path: Union[str, Path]) -> bytes:
        """Perceives raw entropy from the reality."""
        pass

    @abstractmethod
    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Perceives luminous text from the reality."""
        pass

    @abstractmethod
    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        """Transmutes the location of a form (Atomic Move)."""
        pass

    @abstractmethod
    def unlink(self, path: Union[str, Path]):
        """Annihilates a scripture."""
        pass

    @abstractmethod
    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """Annihilates a container."""
        pass

    @abstractmethod
    def chmod(self, path: Union[str, Path], mode: int):
        """Consecrates the permissions of a form."""
        pass

    @abstractmethod
    def close(self):
        """Closes the bridge to the reality."""
        pass
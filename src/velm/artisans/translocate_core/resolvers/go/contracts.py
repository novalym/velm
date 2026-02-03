# // scaffold/artisans/translocate_core/resolvers/go/contracts.py
from dataclasses import dataclass

@dataclass
class GoDetectedImport:
    line_num: int
    import_path: str       # e.g. "github.com/user/project/pkg/utils"
    alias: str | None      # e.g. "u" in `import u "..."`
    start_byte: int
    end_byte: int

@dataclass
class GoHealingEdict:
    line_num: int
    original_path: str
    new_path: str
    start_byte: int
    end_byte: int
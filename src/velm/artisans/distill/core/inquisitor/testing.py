# Path: artisans/distill/core/inquisitor/testing.py
# -------------------------------------------------

from pathlib import Path
from typing import List, Optional, Tuple

from .....inquisitor import get_treesitter_gnosis


class TestInquisitor:
    """
    =================================================================================
    == THE TEST INQUISITOR (THE BOND FORGER'S EYE)                                 ==
    =================================================================================
    This divine artisan possesses a singular, focused Gaze. It looks only upon test
    scriptures. Within their soul, it perceives their import statements to find every
    symbol they summon from the application's core (`src/`, `app/`, etc.).

    For each bond it perceives, it returns a tuple of `(test_file, source_file)`,
    providing the `GraphBuilder` with the Gnosis required to forge the unbreakable,
    bidirectional bond between a test and its source.
    =================================================================================
    """

    def __init__(self, project_root: Path, all_files_set: set[str], symbol_map: dict[str, str]):
        self.root = project_root
        self.all_files = all_files_set
        self.symbol_map = symbol_map

    def find_bonds(self, test_file_path: Path) -> List[Tuple[str, str]]:
        """
        Performs the Gaze upon a single test file and returns all perceived bonds.
        """
        bonds = []
        try:
            content = test_file_path.read_text(encoding='utf-8')
            gnosis = get_treesitter_gnosis(test_file_path, content)

            if "error" in gnosis or "dependencies" not in gnosis:
                return []

            imported_symbols = gnosis["dependencies"].get("imported_symbols", [])
            test_path_str = str(test_file_path.relative_to(self.root)).replace('\\', '/')

            for symbol in imported_symbols:
                # Ask the symbol map where this symbol lives
                source_file_str = self.symbol_map.get(symbol.split('.')[-1]) # Use simple name for lookup

                if source_file_str and source_file_str in self.all_files:
                    # We found a link from a test to a source file.
                    # We must ensure we are not linking to another test file.
                    if 'test' not in source_file_str and 'spec' not in source_file_str:
                        bonds.append((test_path_str, source_file_str))

        except Exception:
            return []

        # Return unique bonds
        return list(set(bonds))
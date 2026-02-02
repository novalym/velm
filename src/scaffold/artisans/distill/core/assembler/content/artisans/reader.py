# Path: scaffold/artisans/distill/core/assembler/content/artisans/reader.py

from pathlib import Path
from typing import Optional


class SoulReader:
    """A sovereign artisan for the pure, resilient reading of a scripture's soul."""

    def read(self, path: Path) -> Optional[str]:
        """
        Performs a multi-stage Gaze to read a file's content, gracefully
        handling binary souls and encoding heresies.
        """
        if not path.exists():
            return None

        try:
            # The Entropy Gaze: We read a small chunk to *prove* it's not binary.
            with open(path, 'rb') as f:
                chunk = f.read(1024)
                if b'\0' in chunk:
                    return None  # Binary soul confirmed.
        except Exception:
            return None  # Unreadable, permission error, etc.

        # The Gaze of Forgiveness (Encoding Fallback)
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return path.read_text(encoding=encoding)
            except (UnicodeDecodeError, Exception):
                continue

        return None  # All attempts failed.


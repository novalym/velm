# Path: artisans/librarian/purifiers/memory.py
# ------------------------------------------
import gc
import sys


class MemoryPurifier:
    """Evaporates in-memory bloat."""

    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger

    def lustrate(self) -> int:
        # 1. Clear Alchemist (Jinja) Cache
        if hasattr(self.engine, 'alchemist'):
            try:
                self.engine.alchemist.env.cache.clear()
            except:
                pass

        # 2. Force Python Lustration
        pre_count = len(gc.get_objects())
        gc.collect()
        post_count = len(gc.get_objects())

        return max(0, pre_count - post_count)
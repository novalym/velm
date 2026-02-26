# Path: artisans/librarian/purifiers/process.py
# -------------------------------------------
import os
import time

try: import psutil
except: psutil = None

class ProcessPurifier:
    """Reaps orphaned child souls."""
    def __init__(self, logger):
        self.logger = logger

    def reap_orphans(self) -> int:
        if not psutil: return 0
        count = 0
        current_proc = psutil.Process()
        for child in current_proc.children(recursive=True):
            try:
                # If child is a zombie or has been running for > 1 hour
                if child.status() == psutil.STATUS_ZOMBIE or (time.time() - child.create_time() > 3600):
                    child.terminate()
                    count += 1
            except: pass
        return count
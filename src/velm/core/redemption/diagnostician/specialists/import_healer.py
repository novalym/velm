# Path: scaffold/core/redemption/diagnostician/specialists/import_healer.py
# -------------------------------------------------------------------------

import sys
import difflib
from typing import Optional
from ..contracts import Diagnosis
from ..grimoire import PACKAGE_MAP


class ImportHealer:
    """The Specialist of Broken Bonds and Missing Souls."""

    @staticmethod
    def heal(exc: BaseException) -> Optional[Diagnosis]:

        # 1. The Gaze of the Missing Library
        if isinstance(exc, ModuleNotFoundError):
            name = exc.name
            if not name: return None

            # Handle submodules 'yaml.scanner' -> 'yaml'
            root_pkg = name.split('.')[0]
            install_name = PACKAGE_MAP.get(root_pkg, root_pkg)

            return Diagnosis(
                heresy_name="MissingAlly",
                cure_command=f"pip install {install_name}",
                advice=f"The soul '{root_pkg}' is missing from the environment.",
                confidence=1.0,
                metadata={"package": install_name}
            )

        # 2. The Gaze of the Typos (AttributeError)
        if isinstance(exc, AttributeError):
            # "module 'scaffold' has no attribute 'runn'"
            msg = str(exc)
            if "has no attribute" in msg:
                import re
                match = re.search(r"'(.*?)' has no attribute '(.*?)'", msg)
                if match:
                    obj_name, bad_attr = match.groups()
                    # If we can get the object, we can scan its dir()
                    # This is hard in post-mortem without the stack frame,
                    # but we can guess common typos.
                    return Diagnosis(
                        heresy_name="FracturedAttribute",
                        cure_command=None,
                        advice=f"Attribute '{bad_attr}' is unknown. Check spelling.",
                        confidence=0.7,
                        metadata={}
                    )

        # 3. The Gaze of the Ouroboros (Circular Import)
        if isinstance(exc, ImportError) and "cannot import name" in str(exc):
            return Diagnosis(
                heresy_name="Ouroboros",
                cure_command=None,
                advice="Circular dependency detected. Refactor imports to avoid cycles.",
                confidence=0.9,
                metadata={}
            )

        return None
# Path: scaffold/setup_entry.py
import os
import sys


# --- CORE RITES ---
# This ensures that win_context_menu is importable after the package is installed.
def run_registry_hook():
    """
    Called by the 'scaffold_reg_hook' entry point to register context menus.
    This is executed on 'pip install -e .'.
    """
    if os.name == 'nt':
        try:
            from .win_context_menu import register_context_menus
            register_context_menus()
        except Exception as e:
            print(f"CRITICAL HOOK FAILURE: Context menu registration failed. Error: {e}", file=sys.stderr)
            print("Please ensure you run 'pip install -e .' with elevated permissions if necessary.", file=sys.stderr)


def run_uninstallation_hook():
    """
    Called by 'scaffold_unreg_hook' before uninstallation.
    """
    if os.name == 'nt':
        try:
            from .win_context_menu import unregister_context_menus
            unregister_context_menus()
        except Exception as e:
            # We don't exit non-zero, as pip uninstall should proceed
            print(f"WARNING: Context menu unregistration failed. Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    # This block allows manual testing: python scaffold/setup_entry.py register
    if len(sys.argv) > 1 and sys.argv[1] == 'register':
        run_registry_hook()
    elif len(sys.argv) > 1 and sys.argv[1] == 'unregister':
        run_uninstallation_hook()
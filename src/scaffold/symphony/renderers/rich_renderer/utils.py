# Path: scaffold/symphony/renderers/rich_renderer/utils.py
# --------------------------------------------------------
from .theme import GnosticTheme


def get_command_icon(command: str) -> str:
    return GnosticTheme.get_icon_and_style(command)[0]


def determine_spinner(command: str) -> str:
    """
    [THE ORACLE OF ANIMATION]
    Divines the appropriate spinner style based on the command intent.
    """
    cmd = command.lower()

    if "install" in cmd or "download" in cmd or "fetch" in cmd:
        return GnosticTheme.SPINNER_INSTALL  # bouncingBar

    if "build" in cmd or "compile" in cmd or "transmute" in cmd:
        return GnosticTheme.SPINNER_BUILD  # star

    if "network" in cmd or "connect" in cmd or "ssh" in cmd:
        return GnosticTheme.SPINNER_NETWORK  # earth

    if "wait" in cmd or "sleep" in cmd:
        return GnosticTheme.SPINNER_WAIT  # clock

    return GnosticTheme.SPINNER_DEFAULT  # dots
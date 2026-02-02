# scaffold/core/runtime/plugin_interface.py

from typing import Type, Any


def register_scaffold_artisan(request_class: Any, command_name: str):
    """
    A sacred decorator to consecrate a third-party Artisan.

    Usage:
        @register_scaffold_artisan(MyRequest, "my-command")
        class MyArtisan(BaseArtisan):
            ...
    """

    def decorator(cls: Type):
        # We inscribe the metadata directly onto the class soul
        setattr(cls, "_scaffold_plugin_info", {
            "request": request_class,
            "command": command_name
        })
        return cls

    return decorator



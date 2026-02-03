# scaffold/semantic_injection/directives/ui_knowledge/python_ui/nicegui_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("nicegui-app")
def forge_nicegui_app(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a modern, reactive web app using NiceGUI.
    """
    return dedent(f"""
        from nicegui import ui

        def {name.lower()}_app():
            with ui.header().classes(replace='row items-center') as header:
                ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
                ui.label('{name}').classes('text-h6')

            with ui.left_drawer().classes('bg-blue-100') as left_drawer:
                ui.label('Navigation')
                ui.link('Home', '#')
                ui.link('Settings', '#')

            with ui.column().classes('w-full items-center'):
                ui.label('Welcome to the Gnostic Web').classes('text-4xl font-bold')

                with ui.card():
                    ui.label('Interactive Elements')
                    ui.switch('Dark Mode', on_change=lambda e: ui.dark_mode(e.value))

                    result = ui.label()
                    ui.button('Click Me', on_click=lambda: result.set_text('Clicked!'))

        {name.lower()}_app()
        ui.run()
    """).strip()
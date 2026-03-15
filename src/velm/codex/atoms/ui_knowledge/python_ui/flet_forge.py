# scaffold/semantic_injection/directives/ui_knowledge/python_ui/flet_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("flet-todo")
def forge_flet_todo(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Flutter-based To-Do app using Flet (Python).
    """
    return dedent(f"""
        import flet as ft

        def main(page: ft.Page):
            page.title = "{name}"
            page.vertical_alignment = ft.MainAxisAlignment.START

            new_task = ft.TextField(hint_text="What needs to be done?", width=300)

            def add_clicked(e):
                if new_task.value:
                    page.add(ft.Checkbox(label=new_task.value))
                    new_task.value = ""
                    new_task.focus()
                    page.update()

            page.add(
                ft.Row([
                    new_task,
                    ft.ElevatedButton("Add", on_click=add_clicked)
                ]),
                ft.Text("Active Tasks:", size=20, weight="bold")
            )

        ft.app(target=main)
    """).strip()
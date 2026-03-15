# scaffold/semantic_injection/directives/ui_knowledge/python_ui/reflex_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("reflex-chat")
def forge_reflex_chat(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a full-stack chat app using Reflex.
    """
    return dedent(f"""
        import reflex as rx

        class State(rx.State):
            question: str = ""
            chat_history: list[tuple[str, str]] = []

            def answer(self):
                # Simulate AI
                answer = "I perceive: " + self.question
                self.chat_history.append((self.question, answer))
                self.question = ""

        def chat() -> rx.Component:
            return rx.box(
                rx.foreach(
                    State.chat_history,
                    lambda messages: rx.vstack(
                        rx.text(messages[0], text_align="right", color="blue"),
                        rx.text(messages[1], text_align="left", color="green"),
                        margin_y="1em",
                    )
                )
            )

        def index() -> rx.Component:
            return rx.container(
                rx.heading("{name}", margin_bottom="1em"),
                chat(),
                rx.hstack(
                    rx.input(placeholder="Ask...", value=State.question, on_change=State.set_question),
                    rx.button("Send", on_click=State.answer)
                )
            )

        app = rx.App()
        app.add_page(index)
    """).strip()
# scaffold/semantic_injection/directives/ui_knowledge/python_ui/gradio_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("gradio-chat")
def forge_gradio_chat(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a modern ChatInterface for LLM interactions.
    Usage: app.py :: @ui/component(name="Bot", props="title:My Bot")
    """
    config = {k: v for k, v in props}
    title = config.get("title", "Gnostic Chat")

    return dedent(f"""
        import gradio as gr
        import time

        def echo_mind(message, history):
            \"\"\"
            Connect this to your @neuron/client.
            \"\"\"
            response = f"I perceive your thought: '{{message}}'"
            for i in range(len(response)):
                time.sleep(0.02)
                yield response[:i+1]

        demo = gr.ChatInterface(
            fn=echo_mind,
            title="{title}",
            description="Interact with the Neural Cortex.",
            theme="soft",
            examples=["What is the meaning of code?", "Generate a Python script."],
            retry_btn="Re-think",
            undo_btn="Undo",
            clear_btn="Tabula Rasa",
        )

        if __name__ == "__main__":
            demo.queue().launch()
    """).strip()


@ComponentRegistry.register("gradio-vision")
def forge_gradio_vision(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Computer Vision workspace.
    """
    return dedent(f"""
        import gradio as gr
        import numpy as np

        def process_vision(input_img, threshold):
            \"\"\"Simulates image processing.\"\"\"
            # Convert to grayscale for demo
            if input_img is None: return None
            return np.dot(input_img[...,:3], [0.2989, 0.5870, 0.1140])

        with gr.Blocks(title="{name}") as demo:
            gr.Markdown("# 👁️ {name} Processing")

            with gr.Row():
                with gr.Column():
                    input_img = gr.Image(label="Input Source")
                    threshold = gr.Slider(0, 100, value=50, label="Sensitivity")
                    btn = gr.Button("Process", variant="primary")

                with gr.Column():
                    output_img = gr.Image(label="Gnostic Output")
                    json_out = gr.JSON(label="Metadata")

            btn.click(fn=process_vision, inputs=[input_img, threshold], outputs=output_img)

        if __name__ == "__main__":
            demo.launch()
    """).strip()
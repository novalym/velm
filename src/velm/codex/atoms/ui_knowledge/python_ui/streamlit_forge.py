# scaffold/semantic_injection/directives/ui_knowledge/python_ui/streamlit_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("streamlit-dashboard")
def forge_streamlit_dashboard(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a data analytics dashboard with key metrics and charts.
    Usage: app.py :: @ui/component(name="Analytics", props="title:Sales Data, sidebar:true")
    """
    config = {k: v for k, v in props}
    title = config.get("title", "Gnostic Dashboard")

    return dedent(f"""
        import streamlit as st
        import pandas as pd
        import numpy as np
        import time

        st.set_page_config(page_title="{title}", layout="wide", page_icon="📊")

        # --- Sidebar Navigation ---
        with st.sidebar:
            st.header("{title}")
            st.markdown("Configure your reality.")
            dates = st.date_input("Date Range", [])
            category = st.multiselect("Categories", ["Tech", "Magic", "Alchemy"], default=["Tech"])
            st.divider()
            st.caption("Forged by Scaffold")

        # --- Main Stage ---
        st.title("🚀 {title}")
        st.markdown("Real-time telemetry from the **Gnostic Core**.")

        # KPI Row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Users", "10,420", "+4%")
        col2.metric("Revenue", "$42,000", "-2%")
        col3.metric("Latency", "45ms", "12ms")
        col4.metric("System Status", "Optimal", delta_color="normal")

        # --- Data Visualization ---
        st.subheader("Temporal Flux")

        # Generate Mock Data
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Alpha', 'Beta', 'Gamma']
        )

        st.line_chart(chart_data)

        # --- Data Table ---
        with st.expander("View Raw Gnosis"):
            st.dataframe(chart_data.style.highlight_max(axis=0))

        if st.button("Refresh Data"):
            with st.spinner("Communing with database..."):
                time.sleep(1)
            st.success("Data refreshed!")
    """).strip()


@ComponentRegistry.register("streamlit-rag")
def forge_streamlit_rag(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a specialized RAG interface for file upload and chat.
    """
    return dedent(f"""
        import streamlit as st

        st.set_page_config(page_title="Neural Memory", layout="wide")
        st.title("🧠 Neural Memory Explorer")

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Ingestion")
            uploaded_file = st.file_uploader("Upload Scripture", type=['txt', 'pdf', 'md'])
            if uploaded_file:
                st.info(f"Ingesting {{uploaded_file.name}}...")
                # Connect @neuron/rag here
                st.success("Knowledge embedded.")

            st.divider()
            st.markdown("**Active Knowledge Base:**")
            st.checkbox("Manual.pdf", value=True)
            st.checkbox("Emails.txt", value=True)

        with col2:
            st.subheader("Interrogation")

            if "messages" not in st.session_state:
                st.session_state.messages = []

            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

            if prompt := st.chat_input("Query the memory..."):
                st.session_state.messages.append({{"role": "user", "content": prompt}})
                with st.chat_message("user"):
                    st.write(prompt)

                # Simulate RAG response
                with st.chat_message("assistant"):
                    st.write("Scanning vector space...")
                    response = f"Based on the scriptures, I believe '{{prompt}}' refers to the Gnostic Protocol."
                    st.write(response)

                st.session_state.messages.append({{"role": "assistant", "content": response}})
    """).strip()
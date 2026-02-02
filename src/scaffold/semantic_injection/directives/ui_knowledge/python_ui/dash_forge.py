# scaffold/semantic_injection/directives/ui_knowledge/python_ui/dash_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("dash-analytics")
def forge_dash_analytics(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges an Enterprise Analytical Dashboard using Plotly Dash.
    """
    return dedent(f"""
        from dash import Dash, html, dcc, callback, Output, Input
        import plotly.express as px
        import pandas as pd

        app = Dash(__name__)

        # Mock Data
        df = pd.DataFrame({{
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        }})

        app.layout = html.Div(children=[
            html.H1(children='{name}'),

            html.Div(children='''
                Gnostic Analytics: Enterprise Data Visualization.
            '''),

            dcc.Dropdown(
                id='city-filter',
                options=df['City'].unique(),
                value='SF'
            ),

            dcc.Graph(id='example-graph')
        ])

        @callback(
            Output('example-graph', 'figure'),
            Input('city-filter', 'value')
        )
        def update_graph(city):
            filtered_df = df[df.City == city]
            fig = px.bar(filtered_df, x="Fruit", y="Amount", color="Fruit", barmode="group")
            return fig

        if __name__ == '__main__':
            app.run(debug=True)
    """).strip()
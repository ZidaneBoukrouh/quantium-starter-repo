from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/processed_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

app = Dash(__name__)
app.title = "Soul Foods Sales Visualiser"

def make_figure(region):
    filtered_df = df.copy()

    if region != "all":
        filtered_df = filtered_df[filtered_df["Region"] == region]

    daily_sales = filtered_df.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Sales Over Time - {region.title()}",
        markers=False
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_white",
        paper_bgcolor="#fffaf5",
        plot_bgcolor="#ffffff",
        font=dict(family="Arial", size=14, color="#2d1f1a"),
        margin=dict(l=40, r=40, t=70, b=40)
    )

    fig.update_traces(line=dict(color="#e75480", width=3))
    return fig

app.layout = html.Div(
    className="app-container",
    children=[
        html.Div(
    className="header-card",
    children=[
        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            className="app-title",
            id="app-header"
        ),
        html.P(
            "Explore Pink Morsel sales over time and compare regional performance before and after the January 15, 2021 price increase.",
            className="app-subtitle"
        ),
    ],
),
        html.Div(
            className="controls-card",
            children=[
                html.Label("Filter by region", className="radio-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    className="radio-group",
                    inputClassName="radio-input",
                    labelClassName="radio-option",
                ),
            ],
        ),
        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(id="sales-chart", figure=make_figure("all"))
            ],
        ),
    ],
)

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    return make_figure(selected_region)

if __name__ == "__main__":
    app.run(debug=True)
from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/processed_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

daily_sales = df.groupby("Date", as_index=False)["Sales"].sum()

fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales",
    template="plotly_white"
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
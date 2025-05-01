import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import os

# Load and prepare data
df = pd.read_csv('formatted_sales.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Region'] = df['Region'].str.lower()
df = df.sort_values('Date')

# Region options
region_options = [
    {'label': 'All', 'value': 'all'},
    {'label': 'North', 'value': 'north'},
    {'label': 'East', 'value': 'east'},
    {'label': 'South', 'value': 'south'},
    {'label': 'West', 'value': 'west'},
]

# Create app and apply external CSS (assets/style.css)
app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"

app.layout = html.Div(
    className="container",
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            id="header",
            className="header"
        ),
        html.Div(
            [
                html.Label("Select Region:", className="radio-label"),
                dcc.RadioItems(
                    id='region_picker',
                    options=region_options,
                    value='all',
                    inline=True,
                    className="radio-group"
                ),
            ],
            className="radio-container"
        ),
        dcc.Graph(id='visualization', className="chart"),
        html.P(
            "Red dashed line marks the price increase on Jan 15, 2021.",
            className="note"
        ),
    ]
)

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_chart(selected_region):
    if selected_region == 'all':
        filtered = df
    else:
        filtered = df[df['Region'] == selected_region]

    # Group by date for total sales per day
    daily_sales = filtered.groupby('Date', as_index=False)['sales'].sum()
    if daily_sales.empty:
        # Return an empty figure with appropriate layout
        return go.Figure(layout={
            "title": "No data available for this region.",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Total Sales ($)"}
        })

    fig = px.line(
        daily_sales,
        x='Date',
        y='sales',
        title="Pink Morsel Sales Over Time",
        labels={'sales': 'Total Sales ($)', 'Date': 'Date'}
    )
    fig.add_vline(
        x=pd.to_datetime('2021-01-15'),
        line_dash="dash",
        line_color="red"
    )
    fig.add_annotation(
        x=pd.to_datetime('2021-01-15'),
        y=max(daily_sales['sales']) if not daily_sales.empty else 0,
        text="Price Increase",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40,
        font=dict(color="red"),
        bgcolor="white"
    )

    fig.update_layout(
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
        font=dict(family="Montserrat, sans-serif", size=14, color="#333"),
        title_font_size=22,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    fig.update_traces(line=dict(width=3))
    return fig

if __name__ == '__main__':
    # Ensure assets directory exists for CSS
    os.makedirs('assets', exist_ok=True)
    # Write a sample CSS file if not present
    css_path = os.path.join('assets', 'style.css')
    app.run(debug=True, use_reloader=False)

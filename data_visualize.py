import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load your formatted data
df = pd.read_csv('formatted_sales.csv')

# Ensure 'Date' is a datetime object and sort
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Group by Date for total sales per day (if not already grouped)
daily_sales = df.groupby('Date', as_index=False)['sales'].sum()

# Create the line chart
fig = px.line(
    daily_sales,
    x='Date',
    y='sales',
    title="Pink Morsel Sales Over Time",
    labels={'sales': 'Total Sales ($)', 'Date': 'Date'}
)

# Add vertical line for price increase date
fig.add_shape(
    type="line",
    x0=pd.to_datetime('2021-01-15'),
    x1=pd.to_datetime('2021-01-15'),
    y0=0,
    y1=daily_sales['sales'].max(),
    line=dict(color="red", dash="dash"),
)

# Add annotation for the vertical line
fig.add_annotation(
    x=pd.to_datetime('2021-01-15'),
    y=daily_sales['sales'].max(),
    text="Price Increase",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40
)

# Build the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig),
    html.P("Red dashed line marks the price increase on Jan 15, 2021.", style={'textAlign': 'center'})
])

if __name__ == '__main__':
    app.run(debug=True)

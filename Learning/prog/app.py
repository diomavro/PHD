from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np

# App initialization
app = Dash(__name__)

# Function to compute normal distribution
def normal_dist(mean, variance):
    x = np.linspace(mean - 3 * np.sqrt(variance), mean + 3 * np.sqrt(variance), 500)
    y = (1 / np.sqrt(2 * np.pi * variance)) * np.exp(-((x - mean) ** 2) / (2 * variance))
    return x, y

# Layout
app.layout = html.Div([
    dcc.Graph(id='normal-plot'),
    html.Label("Mean:"),
    dcc.Slider(id='mean-slider', min=-5, max=5, step=0.1, value=0),
    html.Label("Variance:"),
    dcc.Slider(id='variance-slider', min=0.1, max=5, step=0.1, value=1)
])

# Callback
@app.callback(
    Output('normal-plot', 'figure'),
    [Input('mean-slider', 'value'),
     Input('variance-slider', 'value')]
)
def update_plot(mean, variance):
    x, y = normal_dist(mean, variance)
    figure = go.Figure(data=go.Scatter(x=x, y=y, mode='lines'))
    figure.update_layout(title="Interactive Normal Distribution",
                         xaxis_title="X", yaxis_title="Density")
    return figure

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

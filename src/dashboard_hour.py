import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv(
    'jkt-bdg.csv')

app = dash.Dash()

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='month-slider',
        min=df['month'].min(),
        max=df['month'].max(),
        value=df['month'].min(),
        step=None,
        marks={str(month): str(month) for month in df['month'].unique()}
    )
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('month-slider', 'value')])
def update_figure(selected_month):
    filtered_df = df[df.month == selected_month]
    traces = []
    for i in filtered_df.arrival.unique():
        df_by_arrival = filtered_df[filtered_df['arrival'] == i]
        traces.append(go.Scatter(
            x=df_by_arrival['hour'],
            y=df_by_arrival['adult'],
            text=df_by_arrival['type_train'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 1, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'Hour'},
            yaxis={'title': 'Ticket Price', 'range': [80000, 1200000]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server()

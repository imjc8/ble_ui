# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
app = Dash(__name__)
import plotly.graph_objects as go
from subprocess import run
import json


def count_to_float(count, vref, bits):
    return vref/(2**bits - 1) *count

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

@app.callback(Output('live-update-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    df = pd.read_csv("data.csv")
    dac_count =  df.iloc[:,0].to_numpy()
    adc_count = df.iloc[:,1].to_numpy()
    dac = count_to_float(dac_count,3.3,12)
    adc = count_to_float(adc_count,3.3,11)
    fig = px.scatter(x=dac, y=adc,title="XY plot")
    return fig

@app.callback(Output('td-plot', 'figure'), Input('interval-component2', 'n_intervals'))
def update_graph_live_td(n):
    df = pd.read_csv("data.csv")
    dac_count =  df.iloc[:,0].to_numpy()
    adc_count = df.iloc[:,1].to_numpy()
    dac = count_to_float(dac_count,3.3,12)
    adc = count_to_float(adc_count,3.3,11)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(0,len(dac)),y=dac,
                        mode='lines',
                        name='dac'))
    fig.add_trace(go.Scatter(x=np.arange(0,len(adc)),y=adc,
                        mode='lines+markers',
                        name='adc'))

    return fig

@app.callback(Output('xaxis-column','options'),Input('submit-button-state','n_clicks'))
def scan_ble(n):
    out = run(["python3","scanner.py"],capture_output=True)
    print(out.stdout)
    print(json.loads(out.stdout))
    return json.loads(out.stdout)
    pass

@app.callback(Output("dummy1", "children"),Input('start_exp','n_clicks'))
def scan_ble(n):
    if n:
        print('start')
        out = run(["python3","write_ble.py","0","0","0","0","0"],check=True,capture_output=True)
        return None
    pass


app.layout = html.Div(children=[
    html.Div([
            html.H3("BLE devices"),
            dcc.Dropdown(
                options=['test','asdf'],
                id='xaxis-column'
            ),
            html.Button(id='submit-button-state', n_clicks=0, children='Scan for BLE devices')
    ]),
    html.Div([
        dcc.Input(id='min_volt', type='number', min=2, max=10),
        dcc.Input(id='max_volt', type='number', min=2, max=10),
        dcc.Input(id='start_volt',type='number',min=2,max=10),
        dcc.Input(id='scanrate',type='number',min=0,max=2),
        dcc.Dropdown(id='scan_dir',options=["Up","Down"],value="Up"),
        dcc.Input(id='cyc',type='number',min=0,max=10),
        html.Button(id='start_exp',children='Start experiment')
    ]),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Interval(
            id='interval-component',
            interval=1*500, # in milliseconds
            n_intervals=0
    ),
    dcc.Interval(
        id='interval-component2',
        interval=1*500, # in milliseconds
        n_intervals=0
    ),
    dcc.Graph(
        id='live-update-graph',
        figure=px.scatter(x=[0,0],y=[0,0])
    ),
    dcc.Graph(
        id='td-plot'
    ),
    html.Div(id='dummy1'),
])

if __name__ == '__main__':

    app.run_server(debug=True)
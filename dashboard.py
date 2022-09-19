# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
app = Dash(__name__)
import plotly.graph_objects as go
from subprocess import run
import json
import psutil

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def count_to_float(count, vref, bits):
    return vref/(2**bits - 1) *count

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

@app.callback(Output('indicator', 'children'), Input('interval-component3', 'n_intervals'))
def check_if_running(n):
    proc_iter = psutil.process_iter(attrs=["pid", "name", "cmdline"])
    process = any("write_ble.py" in p.info["cmdline"] for p in proc_iter)
    #print(process)
    if process:
        return "Experiment is running"
    else:
        return "Experiment is not running"


@app.callback(Output('live-update-graph', 'figure'), Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    #df = pd.read_csv("data.csv")
    df = pd.read_csv("-0.6 to 0.8.csv",skiprows=1)
    dac =  df.iloc[:,0].to_numpy()[:-9]
    #adc =  moving_average(df.iloc[:,1].to_numpy(), n=10)
    adc = df.iloc[:,1].to_numpy()[:-9]
    #dac = count_to_float(dac_count,3.3,12)
    #adc = count_to_float(adc_count,3.3,11)
    fig = px.scatter(x=dac, y=adc,title="XY plot", labels={"x":"Stimulation voltage (V)","y":"Measure current (A)"})
    return fig

@app.callback(Output('td-plot', 'figure'), Input('interval-component2', 'n_intervals'))
def update_graph_live_td(n):
    df = pd.read_csv("data.csv")
    dac =  df.iloc[:,0].to_numpy()
    adc = df.iloc[:,1].to_numpy()
    #dac = count_to_float(dac_count,3.3,12)
    #adc = count_to_float(adc_count,3.3,11)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.arange(0,len(dac)),y=dac,
                        mode='lines',
                        name='dac'))
    fig.add_trace(go.Scatter(x=np.arange(0,len(adc)),y=adc,
                        mode='lines+markers',
                        name='adc'))

    return fig

def scan_ble(n):
    out = run(["python3","scanner.py"],capture_output=True)
    print(out.stdout)
    print(json.loads(out.stdout))
    return json.loads(out.stdout)
    pass

@app.callback(Output("dummy1", "children"),Input('start_exp','n_clicks'), 
              State('min_volt','value'),
              State('max_volt','value'),
              State('start_volt','value'),
              State('scanrate','value'),
              State('scan_dir','value'),
              State('cyc','value')
)
def scan_ble(n, min_volt, max_volt, start_volt, scanrate, scan_dir, n_cycles):
    if n:
        print('start')
        if scan_dir == "Down":
            args1234 = ["python3","write_ble.py","-d",str(min_volt),str(max_volt),str(start_volt),str(scanrate),str(n_cycles)]
        else:
            args1234 = ["python3","write_ble.py",str(min_volt),str(max_volt),str(start_volt),str(scanrate),str(n_cycles)]
        print(args1234)
        out = run(args1234,check=True,capture_output=True)
        #print(out)
        return None
    pass


app.layout = html.Div(children=[
    # html.Div([
    #         html.H3("BLE devices"),
    #         dcc.Dropdown(
    #             options=['test','asdf'],
    #             id='xaxis-column'
    #         ),
    #         html.Button(id='submit-button-state', n_clicks=0, children='Scan for BLE devices')
    # ]),
    html.Div([
        html.H1("Potentiostat Control"),
        html.H2("Minimum potential"),
        dcc.Input(id='min_volt', type='number', min=-1.65, max=1.65, value=-0.8),
        html.H2("Maximum potential"),
        dcc.Input(id='max_volt', type='number', min=-1.65, max=1.65, value=0.6),
        html.H2("Starting potential"),
        dcc.Input(id='start_volt',type='number',min=-1.65,max=1.65, value=0),
        html.H2("Scan rate"),
        dcc.Input(id='scanrate',type='number',min=0,max=2, value=1),
        html.H2("Scan direction"),
        dcc.Dropdown(id='scan_dir',options=["Up","Down"],value="Up"),
        html.H2("Number of cycles"),
        dcc.Input(id='cyc',type='number',min=1,max=10, value=2),
        html.Button(id='start_exp',children='Start experiment')
    ]),
    html.Div(id='indicator',children='''
       Experiment not running.
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
    dcc.Interval(
        id='interval-component3',
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
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

#--------Load CSV file---------
df = pd.read_csv("sensor_data.csv")


#--------- LAYOUT OF THE DASHBOARD
app.layout = html.Div(children=[
    html.H1(children="DIME LAB"),
    html.H2(children="VF-2_1 Vibration"),

    dcc.Dropdown(id="select_yr",
                options = [
                    {"label":"2021", "value":2021},
                    {"label":"2020", "value":2020},
                    {"label":"2019", "value":2019}
                ],
                multi=False,
                value=2021,
                style = {'width': "50%"}
    ),
    html.Div(id='output_msg', children=[]),
    html.Br(),
    html.Div(id='output_time', children=[]),
    html.Br(),

    dcc.Graph(
        id='my_sensor_plot',
        figure=dict(),
    ),
    html.Br()
])
#
@app.callback(
    [Output(component_id='output_msg', component_property='children'),
    Output(component_id='output_time', component_property='children'),
    Output(component_id='my_sensor_plot', component_property='figure')],
    [
        Input(component_id='select_yr', component_property='value')
    ]
)
def update_graph(year):

    container = "The year chosen by the user is:{}".format(year)
    time = "The time now is:{}".format(dt.datetime.now())

    df_Yr = df[df['Year']==year]

    trace = dict(
        type = "scatter",
        y = df_Yr["Temperature"],
        line = {"color":"#42C4F7"},
        mode="lines",
    )

    return container, time, dict(data=[trace])


if __name__ == '__main__':
    app.run_server(debug=True)
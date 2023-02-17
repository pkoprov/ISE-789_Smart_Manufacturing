import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
import os
import requests

from dash.dependencies import Input, Output

from api import sensorData, getsensorData200

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device_width, initial-scale=1"}]
)

server = app.server

app_color = {"graph_bg": "#71e1e2", "graph_line": "#009BEF"}

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 1000)

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("REAL TIME MONITORING OF BINIL'S RASPI SIMULATOR", className="app__header__title"),
                        html.P(
                            "This app continually queries my PostGres DB and displays live charts of RASPI's sensors",
                            className="app__header__title--grey"
                        ),
                        html.Div(
                            [
                                html.Button('Submit', id='submit-val', n_clicks=0),
                                html.Div(id='container-button-basic', children='Enter a value and press submit')
                            ]

                        ),
                        html.Div(
                            [
                                html.Button('Last 200', id='retrieve-200', n_clicks=0),
                                html.Div(id='container-button-200', children='')

                            ]
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dimelab.png"),
                            className="app__menu__img",
                        )
                    ],
                    className="app__header__logo",
                )
            ],
            className="app__header",
        ),

        # Our Sensor Data Graphs
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H6("TEMPERATURE DATA", className="graph__title")
                            ]
                        ),
                        dcc.Graph(
                            id="sensor-temperature",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            )
                        ),
                        dcc.Interval(
                            id="sensor-temperature-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        )
                    ],
                    className="half column sensor__temperature__container"
                ),
                html.Div(
                    [

                        html.Div(
                            [
                                html.H6("SENSOR DATA", className="graph__title")
                            ]
                        ),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Temperature Reading(C)",
                                    "value": "temperature",
                                },
                                {
                                    "label": "Pressure Reading(C)",
                                    "value": "pressure",
                                },
                                {
                                    "label": "Humidity Reading(C)",
                                    "value": "humidity",
                                }
                            ],
                            value='temperature',
                            id="chart-dropdown",
                            className="dropdown"
                        ),
                        dcc.Graph(
                            id="sensor-data",
                            figure=dict(
                                layout=dict(
                                    plot_bgcolor=app_color["graph_bg"],
                                    paper_bgcolor=app_color["graph_bg"],
                                )
                            ),
                        ),
                        dcc.Interval(
                            id="sensor-data-update",
                            interval=int(GRAPH_INTERVAL),
                            n_intervals=0,
                        ),
                    ],
                    className="half column sensor__temperature__container_2"
                ),
            ],
            className="app__content",
        )
    ],
    className="app__container",
)


# ---Helper function
def get_current_time():
    now = dt.datetime.now()
    total_time = (now.hour * 3600) + (now.minute * 60) + now.second
    return total_time


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks >= 1:
        resp = requests.get("https://pasha-rest-server.herokuapp.com/startmqtt")

    return 'The button has been clicked {} times'.format(n_clicks)


@app.callback(
    Output("sensor-temperature", "figure"),
    [
        Input("sensor-temperature-update", "n_intervals"),
        Input("retrieve-200", 'n_clicks')
    ]
)
def get_sensor_temperature(interval, n_clicks):
    total_time = get_current_time()

    if n_clicks % 2 == 0:
        df = sensorData(total_time - 200, total_time)
    else:
        df = getsensorData200()

    trace = dict(
        type="scatter",
        y=df["temperature"],
        line={"color": app_color["graph_line"]},
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={'color': "#fff"},
        height=700,
        xaxis={
            "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            "range": [
                min(37, min(df["temperature"])),
                max(42, max(df["temperature"]))
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(df["temperature"].iloc[-1] / 10)),

        }
    )
    return dict(data=[trace], layout=layout)


@app.callback(
    Output("sensor-data", "figure"),
    [
        Input("sensor-data-update", "n_intervals"),
        Input("chart-dropdown", "value"),
    ]
)
def sensor__temperature__container_2(interval, chart_dropdown):
    total_time = get_current_time()
    df = sensorData(total_time - 200, total_time)

    trace = dict(
        type="scatter",
        y=df[chart_dropdown],
        line={"color": app_color["graph_line"]},
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=app_color["graph_bg"],
        paper_bgcolor=app_color["graph_bg"],
        font={'color': "#fff"},
        height=700,
        xaxis={
            "range": [0, 200],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": ["200", "150", "100", "50", "0"],
            "title": "Time Elapsed (sec)",
            # "autorange":"reversed"
        },
        yaxis={
            "range": [
                min(0, min(df[chart_dropdown])),
                max(45, max(df[chart_dropdown]))
            ],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": app_color["graph_line"],
            "nticks": max(6, round(df[chart_dropdown].iloc[-1] / 10)),
        }
    )

    return dict(data=[trace], layout=layout)


if __name__ == "__main__":
    app.run_server(debug=False)

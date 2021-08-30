"""
Creates the dash application.
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

import numpy as np
import pandas as pd
import plotly.express as px

import time

# external stylesheets
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?family=Lato&family=Titillium+Web&display=swap",
        "rel": "stylesheet",

    },
]

# preprocess data for dashboard use
dataset = pd.read_csv("ancira_dataset/ancira_car_listing.csv")
dataset = dataset[dataset.price != "-1"]
dataset["make"].str.lower()

# dataset.query("transmission == 'manual' and dealership == 'Ancira Nissan'")
dataset.sort_values("alert_dt", inplace=True)

# create dash class instance
app = dash.Dash(__name__,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    external_stylesheets
                ])

# figures
# Price to Miles
mil_to_price_fig = px.scatter(dataset,
                              x=dataset["mileage"],
                              y=dataset["price"],
                              color="year",
                              title="Price of Used Cars"
                              )

mil_to_price_fig.update_layout(
    title_x=0.5,
    font_color="#f72585",
    width=750
)

mil_to_price_fig.update_xaxes(title="total mileage (in miles)", showline=True, linewidth=2, linecolor='black')
mil_to_price_fig.update_yaxes(title="price ($)", tickprefix="$", showline=True, linewidth=2, linecolor='black')

# make to volume graph
vol_to_make_fig = px.bar(dataset["make"].value_counts(), title="Volume by Make", orientation='h')
vol_to_make_fig.update_layout(
    title_x=0.5,
    font_color="#f72585",
    showlegend=False
)
vol_to_make_fig.update_traces(marker_color='#6930c3')
vol_to_make_fig.update_xaxes(title="volume", showline=True, linewidth=2, linecolor='black')
vol_to_make_fig.update_yaxes(title="make", showline=True, linewidth=2, linecolor='black')

# UI

app.layout = dbc.Container(
    fluid=True,
    className="card background-color",
    children=[

        # header
        html.Div(
            className="background-color",
            children=[
                html.Img(src="/assets/sport-car.png", className="header-emoji", width=80),
                html.H1(
                    children="Used Car Analytics",
                    className="header-title",
                ),
                html.P(
                    children="Analyzing the behavior of used cars from a local dealership.",
                    className="header-description"
                ),

                html.Div(
                    children=[
                        dcc.Graph(figure=mil_to_price_fig, id="price-mile-chart"),

                    ], className="card card-container"
                ),
            ], style={'textAlign': 'center'}
        ),  # end of header section

        # filter
        html.Div(
            children=[
                # drop down menu option 1
                html.Div(
                    children=[
                        html.Div(children="Make", className="menu-title"),
                        dcc.Dropdown(
                            id="make-filter",
                            options=[
                                {"label": make, "value": make}
                                for make in np.sort(dataset.make.unique())
                            ],
                            value="Ford",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),

                # drop down
                html.Div(
                    children=[
                        html.Div(children="Transmission", className="menu-title"),
                        dcc.Dropdown(
                            id="trans-filter",
                            options=[
                                {"label": transmission, "value": transmission}
                                for transmission in np.sort(dataset.transmission.unique())
                            ],
                            value="manual",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),

                # range slider menu
                html.Div(
                    children=[
                        html.Div(children="Year", className="menu-title"),
                        dcc.RangeSlider(
                            id="year-filter",
                            min=dataset["year"].min(),
                            max=dataset["year"].max(),
                            step=1,
                            allowCross=False
                        ),
                    ]
                ),

            ]
        ),

        # Graphs
        html.Div(
            children=[
                # dcc.Input(id="loading-input-1", value=''),
                #     dcc.Loading(
                #         id="loading-1",
                #         type="default",
                #         children=html.Div(id="loading-output-1")
                #     ),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(
                                    dcc.Graph(
                                        id="price-mpg-chart",
                                        className="card card-container",
                                        config={"displayModeBar": False},
                                        figure={
                                            "data": [
                                                {"x": dataset["hwy_mpg"], "y": dataset["price"], "type": "bar",
                                                 "name": "hwy", 'marker': {"color": "#6930c3"}
                                                 },
                                                {"x": dataset["city_mpg"], "y": dataset["price"], "type": "bar",
                                                 "name": "city", 'marker': {"color": "#fb8b24"},
                                                 }
                                            ],

                                            "layout": {
                                                "title": {
                                                    "text": "Price by MPG Type",
                                                    "x": 0.4,
                                                    "xanchor": "left"
                                                },

                                                "font": {
                                                    "color": "#f72585"
                                                },

                                                "xaxis": {
                                                    "title": "mileage (miles)",
                                                    "fixedrange": True
                                                },

                                                "yaxis": {
                                                    "title": "price ($)",
                                                    "tickprefix": "$",
                                                    "fixedrange": True
                                                },
                                            },
                                        },
                                    ),
                                ),),

                                dbc.Col(
                                    html.Div(
                                        dcc.Graph(figure=vol_to_make_fig, id="make-vol-chart"),
                                        className="card card-container"
                                ),)  # end of Div and Col

                            ]
                        ),
                    ]  # end of row div

                )  # end of div
            ]
        ),  # end graphs section
    ],
)  # end of container


# callbacks
# @app.callback(Output("loading-output-1", "children"), Input("loading-input-1"))
# def input_triggers_spinner(value):
#     time.sleep(1)
#     return value


if __name__ == "__main__":
    app.run_server(debug=True)

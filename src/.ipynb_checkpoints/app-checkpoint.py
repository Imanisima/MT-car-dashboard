"""
Creates the dash application.
"""

from modules.backend.process.scraper_proc import web_scraping_proc
from modules.frontend.dashboard_figures import *

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

import time

import numpy as np
import pandas as pd


external_stylesheets = [
        {
            "href": "https://fonts.googleapis.com/css2?family=Lato&family=Titillium+Web&display=swap",
            "rel": "stylesheet",

        },
]

# create dash class instance
app = dash.Dash(__name__,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    external_stylesheets
                    ]
                )



def data_preprocess(data_file="modules/frontend/ancira_car_listing.csv"):
    """
    Preprocesses data in preparation for dashboard
    PARAMETERS
        data_file : str
            path to store csv file

    RETURNS
        df : dataframe
    """

    df = pd.read_csv(data_file)
    df = df[df.price != "-1"]
    df["make"].str.lower()
    df["transmission"].str.lower()
    df.sort_values("alert_dt", inplace=True)

    return df


# UI
def dash_app_layout(app, dataset):
    """
    Responsible for the dashboard layout.
    PARAMETERS
        app : dash object
        dataset : dataframe

    RETURNS
        Nothing
    """
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
                className="card",
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
                                # value="Select one",
                                clearable=False,
                                className="dropdown",
                            ),
                        ]
                    ),

                    # drop down
                    html.Div(
                        children=[
                            html.Div(children="Transmission Type", className="menu-title"),
                            dcc.Dropdown(
                                id="trans-filter",
                                options=[
                                    {"label": transmission, "value": transmission}
                                    for transmission in np.sort(dataset.transmission.unique())
                                ],
                                # value="manual",
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
                                                        "color": "#b5179e"
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
    # while True:
    #     web_scraping_proc()
    car_data = data_preprocess()
    dash_app_layout(app, car_data)

    app.run_server(debug=True)
        # time.sleep(300)

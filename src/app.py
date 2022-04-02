"""
Creates the dash application.

Features to add:
* add link to car listing
"""

from modules.backend.process.scraper_proc import web_scraping_proc
from modules.frontend.dashboard_figures import *

import dash, dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

import time

import numpy as np
import pandas as pd

import plotly.express as px

import webbrowser

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

PAGE_SIZE = 10


def data_preprocess(car_csv="modules/frontend/ancira_car_listing.csv"):
    """
    Preprocesses data in preparation for dashboard
    PARAMETERS
        data_file : str
            path to store csv file

    RETURNS
        df : dataframe
    """

    df = pd.read_csv(car_csv)

    df = df[df.price != "-1"]
    df["make"].str.lower()
    # df["transmission"].str.lower()
    df.sort_values("alert_dt", inplace=True)

    return df


# UI
def dash_app_layout(app, dataset, mdataset):
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
                        children="A search for manual transmission cars",
                        className="header-description"
                    ),

                    html.Div(
                        children=[
                            dcc.Graph(figure=mil_to_price_fig, id="price-mile-chart"),

                        ], className="card card-container"
                    ),
                ], style={'textAlign': 'center'}
            ),  # end of header section

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

                    ),  # end of div - first 3 charts

                ]
            ),  # end graphs section

            html.Br(),
            html.Br(),

            # DataTable
            html.Div(
                children=[
                    dbc.Label('Manual Transmission Cars'),
                    dash_table.DataTable(

                        # pagination
                        id='datatable-paging-page-count',
                        columns=[
                            {"name": i, "id": i} for i in sorted(mdataset.columns)
                        ],
                        page_current=0,
                        page_size=PAGE_SIZE,
                        page_action='custom',

                        # styling
                        # - default styling
                        style_data={
                            'color': 'black',
                            'backgroundColor': 'white'
                        },

                        style_table={'overflowX': 'auto'},

                        # - alternating rows
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#E7C8DD',
                            }
                        ],

                        # - header
                        style_header={
                            'backgroundColor': '#E7C8DD',
                            'color': 'black',
                            'fontWeight': 'bold'
                        },

                        # - cells
                        style_cell={'textAlign': 'left', 'padding': '5px'},
                        style_as_list_view=True,

                    ),

                    html.Br(),
                    html.Br(),
                    html.Br()
                ]
            ) # end of dataTable container

        ],
    )  # end of container


    # callbacks
    # @app.callback(Output("loading-output-1", "children"), Input("loading-input-1"))
    # def input_triggers_spinner(value):
    #     time.sleep(1)
    #     return value

    # DATATABLE CALLBACKS
    @app.callback(
        Output('datatable-paging-page-count', 'data'),
        Input('datatable-paging-page-count', "page_current"),
        Input('datatable-paging-page-count', "page_size")
    )

    def update_table(page_current,page_size):
        return mdataset.iloc[
            page_current*page_size:(page_current+ 1)*page_size
        ].to_dict('records')


if __name__ == "__main__":
    # while True:
    web_scraping_proc()

    car_data = data_preprocess()
    mcar_data = data_preprocess(car_csv="modules/frontend/ancira_mcar_listing.csv")

    dash_app_layout(app, car_data, mcar_data)

    url = "http://127.0.0.1:8050"
    webbrowser.open(url, new = 0, autoraise=True)

    app.run_server(debug=False)
        # time.sleep(300)

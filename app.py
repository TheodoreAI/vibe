# The outline for this code is from: https://realpython.com/python-dash/

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
from sentiment import *
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

# Getting the style.css for formatting the html elements from the assets directory:
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
# Get the data from the new csv files after the analysis
data = pd.read_csv("movie_data.csv")
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # creating a dash object

app.title = "Virtual Interface Bank of Emotions"  # the title of the application

# The allowed input tupes are set by this tupple
ALLOWED_TYPES = (
    "text",
)

app.layout = html.Div(

    children=[

        html.Div([

            html.H1(children="Vibe"),
            html.P(
                children="The application where the atmosphere of a movie as communicated to and felt by others can be measured. ",
            ),

        ], className="header-title"),

        # The following code for the text input for the search query came from Dash source docs: https://dash.plotly.com/dash-core-components/input
        # This is going to need a callback function to make the new pie charts from Wikipedia text
        html.Div(
            children=[
                html.H2(
                    children="Enter a movie title:"
                ),
                dcc.Input(
                    id="my-input-movie",
                    type="text",
                    placeholder="Enter Movie",
                    className="first-input",
                    required=True
                ),
                html.Button('Submit', id="submit_movie_name", n_clicks=0, className="button-input"),
                html.Div(id="my-output-movie")
            ],

            className="Input-header-div"),

        html.Div([
            dcc.Graph(
                id="the_graph"
            )
        ]),

        html.Div(
            children=[
                dcc.Dropdown(
                    id='my_dropdown',
                    options=[
                        {'value': sent, 'label': sent} for sent in
                        ["Terminator 2: Judgement Day", "Iron Man", "Up", "Interstellar", "Por mis pistolas",
                         "Saw"]],
                    value="Terminator 2: Judgement Day",
                    multi=False,
                    clearable=False,
                    style={"width": "50%"},
                    className="dropdown-menu"
                ),

            ], className="dropdown-menu"),

    ])


@app.callback(
    Output('the_graph', 'figure'),
    [Input('my_dropdown', 'value')]
)
# input into the function and output is the return
def update_graph(values):
    dff = data
    neg = data.to_dict()['neg'].values()
    pos = data.to_dict()['pos'].values()
    neu = data.to_dict()['neu'].values()
    title = data.to_dict()['title'].values()

    df = data.loc[data['title'] == values]
    # If its the right movie selected in the drop down, then get the data for that specific movie
    values_from_movie = []
    if list(df.to_dict()['title'].values())[0] == values:
        labels = ['neg', 'neu', 'pos']
        single_movie_neg = list(df.to_dict()['neg'].values())
        single_movie_neu = list(df.to_dict()['neu'].values())
        single_movie_pos = list(df.to_dict()['pos'].values())
        values_from_movie.append(single_movie_neg[0])
        values_from_movie.append(single_movie_neu[0])
        values_from_movie.append(single_movie_pos[0])

        print(values_from_movie)

    # Use `hole` to create a donut-like pie chart and giving them the right values based on the movie
    fig = go.Figure(data=[go.Pie(labels=labels, values=values_from_movie, hole=.3)])
    return fig


# Making a callback to get the input from the Input field



@app.callback(
    [Output('my-output-movie', "children")],
    [Input('submit_movie_name', 'n_clicks')],
    [State('my-input-movie', 'value')]
)
def make_movie_request(n_clicks, movie_name):
    list_movie = []
    if movie_name is None:
        print("It's empty")
        raise PreventUpdate

    print(movie_name, n_clicks)
    list_movie.append(movie_name.lower())
    return list_movie


if __name__ == '__main__':
    app.run_server(debug=True)

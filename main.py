# The outline for this code is from: https://realpython.com/python-dash/
# try to use this: https://en.wikipedia.org/w/api.php?format=xml&action=query&list=embeddedin&%22%20+%20%20%20%20%20%20%20%20%20%22einamespace=0&eilimit=500&eititle=Template:Infobox%20film
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import os
# from flask_restful import Resource, Api
from imdb import IMDb
import wikipedia

from collections import defaultdict
from csv import writer
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Getting the style.css for formatting the html elements from the assets directory:
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
# Get the data from the new csv files after the analysis
movie_data = os.path.join('movie_data.csv')
data = pd.read_csv(movie_data)
# df = data.loc[data['title']]
# print(df.to_dict()['title'].values())


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)  # creating a dash object
server = app.server
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
                         "Saw", "The Dark Knight Rises"]

                    ],
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
    # print(df.to_dict()['title'].values())
    # If its the right movie selected in the drop down, then get the data for that specific movie
    values_from_movie = []
    labels = ['neg', 'neu', 'pos']

    if list(df.to_dict()['title'].values())[0] == values:
        single_movie_neg = list(df.to_dict()['neg'].values())
        single_movie_neu = list(df.to_dict()['neu'].values())
        single_movie_pos = list(df.to_dict()['pos'].values())
        values_from_movie.append(single_movie_neg[0])
        values_from_movie.append(single_movie_neu[0])
        values_from_movie.append(single_movie_pos[0])

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
        raise PreventUpdate

    list_movie.append(movie_name.lower())

    # passing the movie query to the get_movies() function
    get_movies(list_movie)


    # this
    return list_movie


# @app.callback(
#     [Output('user_dropdown', "children")],
#     [Input('submit_movie_name', 'n_clicks')],
#     [State('my-input-movie', 'value')]
# )
# def dropdown_options(n_clicks, movie_name):
#     print(movie_name)
#     return movie_name
#

def get_movies(movie_list):
    """This function gets the movie plot and passes plot and title on a list."""
    # making the imdb class to make the movie queries:
    # formatting the title
    imdb = IMDb()
    title = imdb.search_movie(movie_list[0])[0].data['title']

    # passing the title to the wikipedia module (this is where the API from RISA will get inserted the text to make the POST request
    wiki_page = wikipedia.WikipediaPage(title)

    plot = wiki_page.section("Plot")

    # passing the plot and the title of the movie to the sentiment analysis function:
    pass_title_plot_sentiment([plot, movie_list[0]])


def pass_title_plot_sentiment(plot_title_arr):
    """This function passes the plot and movie title to the sentiment.py
    file code to output the data analysis."""

    #     doing a rudimentary analysis
    sia = SentimentIntensityAnalyzer()
    dict_output = sia.polarity_scores(plot_title_arr[0])
    # open the movie_data.csv and put the new row
    with open(movie_data, 'a') as movie_data_csv:
        dict_output['title'] = plot_title_arr[1]
        values_list = [vals for vals in dict_output.values()]
        csv_writer = writer(movie_data_csv)
        csv_writer.writerow(values_list)




if __name__ == '__main__':
    app.run_server(debug=True)

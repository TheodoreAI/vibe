# The outline for this code is from: https://realpython.com/python-dash/
# I'm using a wikipedia module content scrapper to seach movies using titles: https://en.wikipedia.org/w/api.php?format=xml&action=query&list=embeddedin&%22%20+%20%20%20%20%20%20%20%20%20%22einamespace=0&eilimit=500&eititle=Template:Infobox%20film
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
import os
# from flask_restful import Resource, Api
from imdb import IMDb
import wikipedia
from flask import jsonify
from collections import defaultdict
from csv import writer
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from flask import abort
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
import pickle as pickle

nltk.download('vader_lexicon')

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

server = flask.Flask(__name__, template_folder='templates')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=server)  # creating a dash object
app.title = "Virtual Interface Bank of Emotions"  # the title of the application

# The allowed input tuples are set by this tuple

ALLOWED_TYPES = (
    "text",
)

tabs_styles = {
    'height': '44px',
    'align-items': 'center'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-weight': 'bold',
    'border-radius': '15px',
    'background-color': '#F2F2F2',
    'box-shadow': '4px 4px 4px 4px lightgrey',
    'height': '40px',
    'font-size': 'large'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-radius': '15px',
    'height': '40px',
    'font-weight': 'bold',
    'font-size': 'large'
}

app.layout = html.Div(

    children=[

        html.Div([

            html.H1(children="Vibe"),
            html.H4(
                children="The application where the atmosphere of a movie as communicated to and felt by others can be measured. ",
                id="description-text"
            ),

        ], className="header-title"),
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
                ),

                html.Button('Submit', id="submit_movie_name", n_clicks=0, className="button-input"),

                html.Div(id="my-output-movie")

            ],

            className="Input-header-div"),
        html.Br(),
        html.Div([
            html.Div(children=[
                dcc.Tabs(id='tabs-example', value='Tab-1', children=[
                    dcc.Tab(label="Film title tab:", value='tab-1', style=tab_style, selected_style=tab_selected_style),
                    dcc.Tab(label='Film plot tab:', value='tab-2', style=tab_style, selected_style=tab_selected_style)
                ], style=tabs_styles),
                html.Div(id='tabs-example-content', children=html.Div([
                    html.H3('Tab-content 2')
                ]))
            ]),
            html.Br(),
            dcc.Graph(
                id="user-graph"
            ),

            html.Label([
                "Movies you choose: ",
                dcc.Dropdown(
                    id='user-dropdown',
                    multi=False,
                    options=[],
                    value="",
                    style={"width": "50%"},
                )], className="dropdown-menu"),

            dcc.Graph(
                id="the_graph"
            ),
            html.Label([
                "Example Movies Analyzed:",
                dcc.Dropdown(
                    id='my_dropdown',
                    options=[

                        {'value': sent, 'label': sent} for sent in
                        ["Terminator 2: Judgement Day", "Iron Man",
                         "Up", "Interstellar", "Por mis pistolas",
                         "Saw", "The Dark Knight Rises"]

                    ],
                    value="Terminator 2: Judgement Day",
                    multi=False,
                    clearable=False,
                    style={"width": "50%"},
                )], className="dropdown-menu"),
        ]),
    ])


class Movie:
    """This class is used to save movie info to use it."""

    def __init__(self, movie_title, movie_plot):
        self.movie_title = movie_title
        self.movie_plot = movie_plot


def save_pickle(title, plot):
    """Saves movie data in pickle form."""
    with open('Movie_data.pkl', 'wb') as output:
        movie_1 = Movie(title, plot)
        pickle.dump(movie_1, output, pickle.HIGHEST_PROTOCOL)

    del movie_1


@app.callback([
    Output('my-output-movie', 'children')],
    [Input('submit_movie_name', 'n_clicks')],
    [State('my-input-movie', 'value')]
)
def update_output_movie_query(submit_n_clicks, movie_name):
    """Displays a success message below input. Need to fix the failure message."""
    if movie_name is None:
        raise PreventUpdate

    else:
        # https://stackoverflow.com/questions/56196916/get-movies-section-from-wikipedia-one-by-one excellent resource
        imdb = IMDb()
        title = imdb.search_movie(movie_name)[0].data['title']
        film_format = "{} (film)".format(movie_name)
        wiki_page = wikipedia.WikipediaPage(film_format)
        print(wikipedia.WikipediaPage(film_format) == True)
        try:
            wikipedia.WikipediaPage(film_format)
            plot = wiki_page.section("Plot")
            if plot is None:
                return ["Try with another movie, or check spelling of: {}".format(movie_name)]

            else:
                # "Submitted {} successfully".format(movie_name)
                save_pickle(movie_name, plot)
                return ["You have successfully chosen {}!:".format(movie_name)]
        except wikipedia.exceptions.PageError:
            return ["Try with another movie, or check spelling of: {}".format(movie_name)]


@app.callback(
    Output('the_graph', 'figure'),
    [Input('my_dropdown', 'value')]
)
# input into the function and output is the return
def update_graph(my_dropdown_values):
    df = data.loc[data['title'] == my_dropdown_values]
    # print(df.to_dict()['title'].values())
    # If its the right movie selected in the drop down, then get the data for that specific movie
    values_from_movie = []
    labels = ['neg', 'neu', 'pos']

    if list(df.to_dict()['title'].values())[0] == my_dropdown_values:
        single_movie_neg = list(df.to_dict()['neg'].values())
        single_movie_neu = list(df.to_dict()['neu'].values())
        single_movie_pos = list(df.to_dict()['pos'].values())
        values_from_movie.append(single_movie_neg[0])
        values_from_movie.append(single_movie_neu[0])
        values_from_movie.append(single_movie_pos[0])

    # Use `hole` to create a donut-like pie chart and giving them the right values based on the movie
    fig = go.Figure(data=[go.Pie(labels=labels, values=values_from_movie, hole=.3)])
    return fig


@app.callback(
    Output('user-graph', 'figure'),
    [Input('user-dropdown', 'value')]
)
def update_user_graph(user_dropdown_values):
    """ If its the right movie selected in the drop down, then get the data for that specific movie"""
    movie_data_user = os.path.join('movie_data_user.csv')
    data_user = pd.read_csv(movie_data_user)
    dff = data_user
    if user_dropdown_values == '':
        raise PreventUpdate
    else:
        df = dff.loc[dff['title'] == user_dropdown_values]
        values_from_movie = []
        labels = ['neg', 'neu', 'pos']
        if list(df.to_dict()['title'].values())[0] == user_dropdown_values:
            single_movie_neg = list(df.to_dict()['neg'].values())
            single_movie_neu = list(df.to_dict()['neu'].values())
            single_movie_pos = list(df.to_dict()['pos'].values())
            values_from_movie.append(single_movie_neg[0])
            values_from_movie.append(single_movie_neu[0])
            values_from_movie.append(single_movie_pos[0])
        # Use `hole` to create a donut-like pie chart and giving them the right values based on the movie
        fig = go.Figure(data=[go.Pie(labels=labels, values=values_from_movie, hole=.3)])
        return fig


@app.callback(
    [Output(component_id='user-dropdown', component_property="options"),
     Output(component_id='user-dropdown', component_property='value')],
    [Input(component_id='submit_movie_name', component_property='n_clicks')],
    [State('my-input-movie', 'value'), State('user-dropdown', 'options'), State('user-dropdown', 'value')]

)
def dropdown_options(n_clicks, movie_name, current_options, device_str):
    """Update the dropdown options for the movies."""
    if not movie_name:
        return current_options, device_str
    else:
        if get_movies(movie_name):

            if device_str:

                if movie_name != device_str:
                    device_str = movie_name
                    current_options.append({'label': movie_name, 'value': movie_name})
            else:
                device_str = movie_name
                current_options.append({'label': movie_name, 'value': movie_name})
            return current_options, device_str
        else:

            return current_options, device_str


@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    """To save data with pickle I used: https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence/4529901"""
    with open('Movie_data.pkl', 'rb') as inpt:
        movie_1 = pickle.load(inpt)

        if tab == 'tab-1':
            return html.Div([
                html.H3(movie_1.movie_title)
            ])
        elif tab == 'tab-2':
            return html.Div([
                html.P(movie_1.movie_plot)
            ])


def get_request_api_microservice(title, plot):
    """Call API to make the flashcards:"""
    url_api = 'http://flashcard-service.herokuapp.com/{}/{}'.format(title, plot)
    res = requests.get(url=url_api)
    return res.content


def get_movies(movie_str):
    """This function gets the movie plot and passes plot and title on a list."""
    film_format = "{} (film)".format(movie_str)
    wiki_page = wikipedia.WikipediaPage(film_format)
    plot = wiki_page.section("Plot")
    if plot is not None:

        # pass the plot and title of the movie in an array to the analysis fn
        pass_title_plot_sentiment([plot, movie_str])
        return True

    else:
        error = wikipedia.PageError
        print(error)
        print(error.args)
        raise PreventUpdate


def remove_punctuation(plot):
    """Removes the punctuation from string.
    Source: https://www.programiz.com/python-programming/examples/remove-punctuation"""
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    no_punc = ""
    for char in plot:
        if char not in punc:
            no_punc = no_punc + char

    return no_punc


def remove_stopwords(plot_title):
    """Removes the stopwords from my string."""

    plot_without_punc = remove_punctuation(plot_title)

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(plot_without_punc)
    filtered_plot = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_plot = []

    # remove stop words
    for w in word_tokens:
        if w not in stop_words:
            filtered_plot.append(w)
    string_plot = ' '.join(filtered_plot)
    return string_plot


def pass_title_plot_sentiment(plot_title_arr):
    """This function passes the plot and movie title to the sentiment.py
    file code to output the data analysis."""

    #     doing a rudimentary analysis
    filtered_plot = remove_stopwords(plot_title_arr[0])
    print(filtered_plot)
    sia = SentimentIntensityAnalyzer()
    dict_output = sia.polarity_scores(filtered_plot)

    # open the movie_data.csv and put the new row
    with open(os.path.join('movie_data_user.csv'), 'a') as md_user_csv:
        dict_output['title'] = plot_title_arr[1]
        values_list = [vals for vals in dict_output.values()]
        csv_writer = writer(md_user_csv)
        csv_writer.writerow(values_list)

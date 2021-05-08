# The outline for this code is from: https://realpython.com/python-dash/

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from sentiment import *
import plotly.express as px
import plotly.graph_objects as go

# Get the data from the new csv files after the analysis
data = pd.read_csv("movie_data.csv")
app = dash.Dash(__name__)

app.title = "Virtual Interface Bank of Emotions"

app.layout = html.Div([
    html.Div([
        html.H1(children="Vibe",),
        html.P(
            children="The application where the atmosphere of a movie as communicated to and felt by others can be measured. ",
        ),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                {'value': sent, 'label': sent} for sent in ["Terminator 2: Judgement Day", "Iron Man", "Up"]],
            value="Terminator 2: Judgement Day",
            multi=False,
            clearable=False,
            style={"width": "50%"},
        ),
    ]),

    html.Div([
        dcc.Graph(
            id="the_graph"
        )
    ]),
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
        labels = ['neg', 'pos', 'neu']
        single_movie_neg = list(df.to_dict()['neg'].values())
        single_movie_pos = list(df.to_dict()['pos'].values())
        single_movie_neu = list(df.to_dict()['neu'].values())
        values_from_movie.append(single_movie_pos[0])
        values_from_movie.append(single_movie_neu[0])
        values_from_movie.append(single_movie_neg[0])
        print(values_from_movie)

    # labels = ['', 'Hydrogen', 'Carbon_Dioxide', 'Nitrogen']
    # values = [4500, 2500, 1053, 500]

    # print(type(list(neg)), type(title), type(labels))

    # Use `hole` to create a donut-like pie chart and giving them the right values based on the movie
    fig = go.Figure(data=[go.Pie(labels=labels, values=values_from_movie, hole=.3)])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

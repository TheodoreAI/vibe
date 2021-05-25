from dashboard import app, server
from flask import render_template

import requests


url_get = 'http://flashcard-service.herokuapp.com/front/back'



@server.route('/sentiment-cards', methods=['GET'])
def post_request_flashcard_api():
    """This function will be used to request the API data for Rhonda's microservice.
    """
    return render_template('home.html')



if __name__ == '__main__':
    app.run_server(debug=True)

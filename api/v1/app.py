#!/usr/bin/python3
""" Flask app"""

from models import storage
from api.v1.views import app_views
from flask import Flask
import os
from flask import jsonify
import requests


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.errorhandler(404)
def not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


class Handler:
    def not_found(error):
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        return response


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)

#!/usr/bin/python3
"""_summary_"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    '''
    close query after each session
    '''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''
    return JSON formatted 404 status code response
    '''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)

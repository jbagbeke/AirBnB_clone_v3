#!/usr/bin/python3
"""
    Starts a FLASK WEB APP
                            """
from models import storage
from flask import Flask, jsonify, render_template
from flask import make_response
from api.v1.views import app_views
from flask_cors import CORS
import os

# Creating the Flask instance
app = Flask(__name__)

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def hbnb_teardown(self):
    """
        Closes current db session
                                """
    storage.close()


@app.errorhandler(404)
def hbnb_not_found(error):
    not_found = {'error': 'Not found'}
    return make_response(jsonify(not_found), 404)


if __name__ == '__main__':
    host_var = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port_var = os.getenv('HBNB_API_PORT', 5000)

    app.run(host=host_var, port=port_var, threaded=True)

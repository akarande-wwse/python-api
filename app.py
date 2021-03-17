from flask import Flask, send_from_directory
from ariadne import graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from src.graphql import schema
from src.database import Session

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    context = {"referer": request.referrer, "session": Session()}

    success, result = graphql_sync(
        schema,
        data,
        context_value=context,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path) 

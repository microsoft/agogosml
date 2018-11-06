import os

from flask import Flask, request

from streaming_client.listener_client import ListenerClient


class FlaskHttpListenerClient(ListenerClient):

    def __init__(self):
        pass

    def start(self, port, on_message_received):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():

            msg = request.get_json(force=True)
            on_message_received(msg)

        app.run(debug=True, port=port)
        pass

    def stop(self):
        self.shutdown_server()
        pass

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

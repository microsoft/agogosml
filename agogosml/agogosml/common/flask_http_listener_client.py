""" Flask client to receive messages from customer app"""
from flask import Flask, request
from .listener_client import ListenerClient


class FlaskHttpListenerClient(ListenerClient):
    def __init__(self, port):
        self.port = port
        pass

    def start(self, on_message_received):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():

            msg = request.data
            on_message_received(msg)

        app.run(port=self.port)
        pass

    def stop(self):
        self.shutdown_server()
        pass

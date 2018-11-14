""" Flask client to receive messages from customer app"""
from flask import Flask, request
from .listener_client import ListenerClient


class FlaskHttpListenerClient(ListenerClient):
    def __init__(self, port):
        self.port = port

    def start(self, on_message_received):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():
            msg = str(request.data, 'utf-8', 'ignore')
            on_message_received(self, msg)

        app.run(port=self.port)

    def stop(self):
        raise NotImplementedError()

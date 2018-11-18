""" Flask client to receive messages from customer app"""
from flask import Flask, request
from .listener_client import ListenerClient


class FlaskHttpListenerClient(ListenerClient):
    def __init__(self, port, host='127.0.0.1'):
        self.port = port
        self.host = host

    def start(self, on_message_received):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():
            msg = str(request.data, 'utf-8', 'ignore')
            on_message_received(self, msg)
            return ""

        app.run(host=self.host, port=self.port)

    def stop(self):
        raise NotImplementedError()

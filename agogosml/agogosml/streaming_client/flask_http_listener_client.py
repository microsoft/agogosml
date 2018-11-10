""" Flask client to receive messages from customer app"""
import os
import threading

from flask import Flask, request

from agogosml.streaming_client.listener_client import ListenerClient


class FlaskHttpListenerClient(ListenerClient):

    def __init__(self, port):
        self.port = port
        pass

    def start(self, on_message_received):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():

            msg = request.get_json()
            on_message_received(msg)

        app.run(port=self.port)
        pass

    def stop(self):
        self.shutdown_server()
        pass

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

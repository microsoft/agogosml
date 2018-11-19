""" Flask client to receive messages from customer app"""
import threading
import time
from flask import Flask, request
from .listener_client import ListenerClient

DEFAULT_HOST = '127.0.0.1'


class FlaskHttpListenerClient(ListenerClient):
    def __init__(self, port, host=DEFAULT_HOST):
        self.port = port
        self.host = host

    def thread_flask(self):

        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():
            msg = str(request.data, 'utf-8', 'ignore')
            self.on_message_received(msg)
            return ""

        app.run(
            host=self.host, port=self.port, debug=False, use_reloader=False)

    def start(self, on_message_received):

        self.on_message_received = on_message_received
        t_flask = threading.Thread(name='agogosml', target=self.thread_flask)
        t_flask.setDaemon(True)
        t_flask.start()

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            exit(1)

    def stop(self):
        raise KeyboardInterrupt

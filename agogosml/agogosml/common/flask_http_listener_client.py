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
            if self.on_message_received(msg):
                return 'msg:' + msg
            else:
                print('Error: The callback failed to process the message, returning 500')
                return 'Error: The callback failed to process the message', 500

        app.run(
            host=self.host, port=self.port, debug=False, use_reloader=False, threaded=True)

    def start(self, on_message_received):
        self.on_message_received = on_message_received
        self.t_flask = threading.Thread(name='agogosml', target=self.thread_flask)
        self.t_flask.setDaemon(True)
        self.t_flask.start()

    def stop(self):
        self.shutdown_server()
        # self.t_flask.join()

    def shutdown_server(self):
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
        except:
            print('error while shutting down flask server')

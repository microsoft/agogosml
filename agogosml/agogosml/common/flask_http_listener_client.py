""" Flask client to receive messages from customer app"""
import threading
import time
from flask import Flask, request
from .listener_client import ListenerClient
from multiprocessing import Process

DEFAULT_HOST = '127.0.0.1'

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with Werkzeug Server')
    func()

    
class FlaskHttpListenerClient(ListenerClient):
    def __init__(self, port, host=DEFAULT_HOST):
        self.port = port
        self.host = host
        self.app = Flask(__name__)
        self.add_routes()
        
    def add_routes(self):
        @self.app.route("/", methods=["POST"])
        def on_input():
            msg = str(request.data, 'utf-8', 'ignore')
            self.on_message_received(msg)
            return ""

    def start(self, on_message_received):

        self.on_message_received = on_message_received
        self.server = Process(target=self.app.run, kwargs={"port": self.port, "host":self.host})
        self.server.start()


    def stop(self):
        self.server.terminate()
        self.server.join()

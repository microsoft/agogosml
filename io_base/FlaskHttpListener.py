import os

from flask import Flask, request

from io_base.abstract_listener import AbstractListener


class FlaskHttpListener(AbstractListener):

    def __init__(self):
        pass

    def start(self, port, message_broker):
        app = Flask(__name__)

        @app.route("/input", methods=["POST"])
        def server_input():

            msg = request.get_json(force=True)
            message_broker.send(msg)

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

""" Flask client to receive messages from customer app"""
import threading

from flask import Flask
from flask import request

from .listener_client import ListenerClient

DEFAULT_HOST = '127.0.0.1'


class FlaskHttpListenerClient(ListenerClient):
    """ Flask client to receive messages from customer app"""

    def __init__(self, config: dict):
        """
        Listener implementation that uses a flask server.

        Configuration keys:

            PORT
            HOST
        """
        self.port = int(config['PORT']) if 'PORT' in config else None
        self.host = config.get('HOST', DEFAULT_HOST)
        self.on_message_received = None
        self.t_flask = None

    def run_flask_server(self):
        """Run the flask server"""
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def on_input():  # pylint: disable=unused-variable
            msg = str(request.data, 'utf-8', 'ignore')
            if self.on_message_received(msg):
                return 'msg: %s' % msg

            print('Error: The callback failed to process the message, returning 500')
            return 'Error: The callback failed to process the message', 500

        app.run(
            host=self.host, port=self.port, debug=False, use_reloader=False, threaded=True)

    def start(self, on_message_received):
        self.on_message_received = on_message_received
        self.t_flask = threading.Thread(name='agogosml', target=self.run_flask_server)
        self.t_flask.setDaemon(True)
        self.t_flask.start()

    def stop(self):
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
        except Exception as ex:
            print('error while shutting down flask server: %s' % ex)

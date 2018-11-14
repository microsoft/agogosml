"""HTTP client to receive messages from customer app"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from .listener_client import ListenerClient
import urllib.request
import urllib.parse
import os
import logging
from dotenv import load_dotenv
from functools import partial

load_dotenv()


class HttpListener(BaseHTTPRequestHandler, ListenerClient):
    """Handles HTTP requests that come to the server."""
    def __init__(self, host, port, on_message_received=None):
        self.host = host
        self.port = int(port)
        self.server_class = HTTPServer
        self.on_message_received = on_message_received

    def _set_headers(self):
        """Sets common headers when returning an OK HTTPStatus. """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')  # TODO: figure out if this is json or text
        self.end_headers()

    def do_POST(self):  # pylint: disable=C0103
        """Handles a POST request to the server.
        Sends 400 error if there is an issue, otherwise sends a success message. """
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode("utf-8")
        print("THIS IS WHAT DATA LOOKS LIKE: ", data, type(data))
        self.on_message_received(data)

    def run(self, on_message_received, server_class=HTTPServer):
        """Run the server on specified host and port, using our
        custom Socket class to receive and process requests.
        """
        handler_class = self
        address = (self.host, self.port)
        httpd = self.server_class(address, on_message_received, handler_class)
        logging.info('Running server on host ${HOST} and port ${PORT}')
        httpd.serve_forever()

    def stop(self):
        pass

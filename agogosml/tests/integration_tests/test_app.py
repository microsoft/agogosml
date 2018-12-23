import os

from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.http_message_sender import HttpMessageSender


class TestApp:

    def __init__(self, app_port, app_host, output_port, output_host):
        self.listener = FlaskHttpListenerClient(app_port, app_host)
        self.sender = HttpMessageSender(output_host, output_port)

    def start(self):
        self.listener.start(self.on_message_received)

    def on_message_received(self, message):
        print('Test App message received: ' + message)
        self.sender.send(message)

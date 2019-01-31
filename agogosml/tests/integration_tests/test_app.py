from agogosml.common.flask_http_listener_client import FlaskHttpListenerClient
from agogosml.common.http_message_sender import HttpMessageSender
from agogosml.utils.logger import Logger

logger = Logger()


class TestApp:

    def __init__(self, app_port, app_host, output_port, output_host):
        self.listener = FlaskHttpListenerClient({'PORT': app_port, 'HOST': app_host})
        self.sender = HttpMessageSender({'HOST': output_host, 'PORT': output_port})

    def start(self):
        self.listener.start(self.on_message_received)

    def on_message_received(self, message):
        logger.info('Test App message received: ' + message)
        sender_result = self.sender.send(message)
        logger.info('Sender result: ' + str(sender_result))
        return sender_result

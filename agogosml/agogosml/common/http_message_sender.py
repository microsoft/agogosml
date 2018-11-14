"""
HttpMessageSender
"""
import logging
import json
import requests
from .message_sender import MessageSender

LOGGER = logging.getLogger("STREAM")
LOGGER.setLevel(logging.INFO)


class HttpMessageSender(MessageSender):  # pylint: disable=too-few-public-methods
    """
    HttpMessageSender
    """
    def __init__(self, host_endpoint, port_endpoint):
        LOGGER.info("host_endpoint: {}".format(host_endpoint))
        LOGGER.info("port_endpoint: {}".format(port_endpoint))

        if host_endpoint is None:
            raise ValueError('Host endpoint cannot be None.')

        if host_endpoint == "":
            raise ValueError('Host endpoint cannot be empty.')

        if int(port_endpoint) <= 0:
            raise ValueError('Port cannot be 0 or less.')

        self.host_endpoint = host_endpoint
        self.port_endpoint = port_endpoint
        pass

    def send(self, message):
        """
        Sends messages to specified address via HTTP

        :param message:  json formatted message
        """
        try:
            server_address = "http://" + self.host_endpoint + ":" + self.port_endpoint
            # TODO: Add retries as some of the messages are failing to send
            request = requests.post(server_address, data=json.dumps(message))
            if request.status_code != 200:
                LOGGER.error(
                    "Error with a request {} and message not sent was {}"
                    .format(request.status_code, message))
                print("Error with a request {} and message not sent was {}".
                      format(request.status_code, message))
                return False
            return True

        except Exception as e_e:
            LOGGER.error('Failed to send request: ' + str(e_e))

        finally:
            return False

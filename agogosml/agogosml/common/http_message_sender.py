"""HttpMessageSender."""

import requests

from ..utils.logger import Logger
from .message_sender import MessageSender

logger = Logger()


class HttpMessageSender(MessageSender):
    """HttpMessageSender."""

    def __init__(self, config: dict):
        """
        Configuration keys:

            HOST
            PORT
        """
        host_endpoint = config.get('HOST')
        port_endpoint = config.get('PORT')

        logger.info("host_endpoint: %s", host_endpoint)
        logger.info("port_endpoint: %s", port_endpoint)

        if host_endpoint is None:
            raise ValueError('Host endpoint cannot be None.')

        if host_endpoint == "":
            raise ValueError('Host endpoint cannot be empty.')

        if int(port_endpoint) <= 0:
            raise ValueError('Port cannot be 0 or less.')

        self.host_endpoint = host_endpoint
        self.port_endpoint = port_endpoint

    def send(self, message):
        """
        Sends messages to specified address via HTTP.

        :param message: JSON formatted message.
        """
        return_value = False
        try:
            server_address = "http://" + self.host_endpoint + ":" + self.port_endpoint
            # TODO: Add retries as some of the messages are failing to send
            request = requests.post(server_address, data=message)
            if request.status_code != 200:
                logger.error("Error with a request %s and message not sent was %s",
                             request.status_code, message)
                print("Error with a request %s and message not sent was %s",
                      request.status_code, message)
            else:
                return_value = True

        except Exception as e_e:
            logger.error('Failed to send request: %s', e_e)

        return return_value

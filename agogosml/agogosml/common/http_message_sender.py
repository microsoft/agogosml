"""
HttpMessageSender
"""
import logging
import requests
from .message_sender import MessageSender

logger = logging.getLogger(__name__)


class HttpMessageSender(MessageSender):  # pylint: disable=too-few-public-methods
    """
    HttpMessageSender
    """

    def __init__(self, host_endpoint, port_endpoint):
        logger.info("host_endpoint: {}".format(host_endpoint))
        logger.info("port_endpoint: {}".format(port_endpoint))

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
            request = requests.post(server_address, data=message)
            if request.status_code != 200:
                logger.error(
                    "Error with a request {} and message not sent was {}".
                    format(request.status_code, message))
                print("Error with a request {} and message not sent was {}".
                      format(request.status_code, message))
                return False
            return True

        except Exception as e_e:
            logger.error('Failed to send request: ' + str(e_e))

        finally:
            return False

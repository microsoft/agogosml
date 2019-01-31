"""HttpMessageSender."""

from agogosml.utils.http_request import post_with_retries
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
            SCHEME
        """
        host_endpoint = config.get('HOST')
        port_endpoint = config.get('PORT')
        scheme_endpoint = config.get('SCHEME', 'http')

        logger.info("host_endpoint: %s", host_endpoint)
        logger.info("port_endpoint: %s", port_endpoint)
        logger.info("scheme_endpoint: %s", scheme_endpoint)

        if host_endpoint is None:
            raise ValueError('Host endpoint cannot be None.')

        if host_endpoint == "":
            raise ValueError('Host endpoint cannot be empty.')

        if int(port_endpoint) <= 0:
            raise ValueError('Port cannot be 0 or less.')

        if scheme_endpoint not in ('http', 'https'):
            raise ValueError('Scheme must be http or https')

        self.host_endpoint = host_endpoint
        self.port_endpoint = port_endpoint
        self.scheme_endpoint = scheme_endpoint

    def send(self, message):
        """
        Sends messages to specified address via HTTP.

        :param message: JSON formatted message.
        """
        return_value = False
        try:
            server_address = "%s://%s:%s" % (self.scheme_endpoint, self.host_endpoint, self.port_endpoint)
            status_code = post_with_retries(server_address, message)
            if status_code != 200:
                logger.error("Error with a request %s and message not sent was %s",
                             status_code, message)
                print("Error with a request %s and message not sent was %s" %
                      (status_code, message))
            else:
                return_value = True

        except Exception as e_e:
            logger.error('Failed to send request: %s', e_e)

        return return_value

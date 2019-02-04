"""HttpMessageSender."""

from agogosml.common.message_sender import MessageSender
from agogosml.utils.http_request import post_with_retries
from agogosml.utils.logger import Logger


class HttpMessageSender(MessageSender):
    """HttpMessageSender."""

    def __init__(self, config: dict):
        """
        Message sender implementation that uses HTTP(S) to send messages.

        Configuration keys:

            HOST
            PORT
            SCHEME
            RETRIES
            BACKOFF
        """
        host = config.get('HOST')
        port = config.get('PORT')
        scheme = config.get('SCHEME', 'http')
        retries = config.get('RETRIES', 3)
        backoff = config.get('BACKOFF', 1)

        if not host:
            raise ValueError('Host endpoint must be provided.')

        if not port or int(port) <= 0:
            raise ValueError('Port cannot be 0 or less.')

        if scheme not in ('http', 'https'):
            raise ValueError('Scheme must be http or https')

        self.server_address = "%s://%s:%s" % (scheme, host, port)
        self.retries = retries
        self.backoff = backoff

        self.logger = Logger()

        self.logger.info("server_address: %s", self.server_address)

    def send(self, message):
        return_value = False
        try:
            status_code = post_with_retries(
                self.server_address, message,
                retries=self.retries,
                backoff=self.backoff)

            if status_code != 200:
                self.logger.error("Error with a request %s and message not sent was %s",
                                  status_code, message)
                print("Error with a request %s and message not sent was %s" %
                      (status_code, message))
            else:
                return_value = True

        except Exception as ex:
            self.logger.error('Failed to send request: %s', ex)

        return return_value

"""HttpMessageSender."""

from agogosml.common.message_sender import MessageSender
from agogosml.utils.http_request import post_with_retries
from agogosml.utils.logger import Logger


class HttpMessageSender(MessageSender):
    """HttpMessageSender."""

    def __init__(self, config: dict):  # pragma: no cover
        """
        Message sender implementation that uses HTTP(S) to send messages.

        Configuration keys:

            HOST
            PORT
            SCHEME
            RETRIES
            BACKOFF
            EXTRA_URLS
        """
        host = config.get('HOST')
        port = config.get('PORT')
        scheme = config.get('SCHEME', 'http')
        retries = config.get('RETRIES', 3)
        backoff = config.get('BACKOFF', 1)
        extra_urls = config.get('EXTRA_URLS') or []

        if not host:
            raise ValueError('Host endpoint must be provided.')

        if not port or int(port) <= 0:
            raise ValueError('Port cannot be 0 or less.')

        if scheme not in ('http', 'https'):
            raise ValueError('Scheme must be http or https')

        self.server_address = "%s://%s:%s" % (scheme, host, port)
        self.retries = retries
        self.backoff = backoff
        self.extra_urls = extra_urls

        self.logger = Logger()

        self.logger.info("server_address: %s", self.server_address)

    def send(self, message):  # pragma: no cover
        return_value = self._send(message, self.server_address)

        for extra_url in self.extra_urls:
            self._send(message, extra_url)

        return return_value

    def _send(self, message, url):
        return_value = False
        try:
            status_code = post_with_retries(
                url, message,
                retries=self.retries,
                backoff=self.backoff)

            if status_code != 200:
                self.logger.error("[Server %s] Error with a request %s and message not sent was %s",
                                  url, status_code, message)
                print("[Server %s] Error with a request %s and message not sent was %s" %
                      (url, status_code, message))
            else:
                return_value = True

        except Exception as ex:
            self.logger.error('[Server %s] Failed to send request: %s', url, ex)

        return return_value

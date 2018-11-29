""" Entrypoint for customer application. Listens for HTTP requests from
the input reader, and sends the transformed message to the output writer. """
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.parse
import os
import logging
from dotenv import load_dotenv
import datahelper

load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
OUTPUT_URL = os.getenv("OUTPUT_URL")
SCHEMA_FILEPATH = os.getenv("SCHEMA_FILEPATH")


class Socket(BaseHTTPRequestHandler):
    """Handles HTTP requests that come to the server."""

    def _set_headers(self):
        """Sets common headers when returning an OK HTTPStatus. """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):  # pylint: disable=C0103
        """Handles a POST request to the server.
        Sends 400 error if there is an issue, otherwise sends a success message.

        Raises:
          ValidationError: Returns when data given is not valid against schema
          HTTPError: Returns when there is an error sending message to output url

        """
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        data = data.decode("utf-8")

        try:
            datahelper.validate_schema(data, SCHEMA_FILEPATH)
        except BaseException:
            self.send_error(
                400, 'Incorrect data format. Please check JSON schema.')
            logging.error('Incorrect data format. Please check JSON schema.')
            raise

        try:
            transformed_data = datahelper.transform(data)
            output_message(transformed_data)
            self._set_headers()
            self.wfile.write(bytes("Data successfully consumed", 'utf8'))
        except BaseException:
            self.send_error(400, 'Error when sending output message')
            logging.error('Error when sending output message')
            raise


def output_message(data: object):
    """Outputs the transformed payload to the specified HTTP endpoint

    Args:
      data: transformed json object to send to output writer
    """

    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(OUTPUT_URL, encoded_data)
    response = urllib.request.urlopen(req)
    logging.info('Response received from output writer')
    # TO DO: Design retry policy based on BL. For now, print result
    print(response.read().decode('utf-8'))


def run(server_class=HTTPServer, handler_class=Socket):
    """Run the server on specified host and port, using our
    custom Socket class to receive and process requests.
    """

    server_address = (HOST, int(PORT))
    httpd = server_class(server_address, handler_class)
    logging.info('Running server on host ${HOST} and port ${PORT}')
    httpd.serve_forever()


if __name__ == "__main__":
    run()

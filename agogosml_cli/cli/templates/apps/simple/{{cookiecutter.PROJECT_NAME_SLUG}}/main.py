""" Entrypoint for customer application. Listens for HTTP requests from
the input reader, and sends the transformed message to the output writer. """
import json
import logging
import os
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

import requests

import datahelper


class Socket(BaseHTTPRequestHandler):
    """Handles HTTP requests that come to the server."""

    schema_filepath = ''
    output_url = ''

    def _set_headers(self):
        """Sets common headers when returning an OK HTTPStatus. """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
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
            datahelper.validate_schema(data, self.schema_filepath)
        except BaseException:
            self.send_error(
                400, 'Incorrect data format. Please check JSON schema.')
            logging.error('Incorrect data format. Please check JSON schema.')
            raise

        try:
            transformed_data = datahelper.transform(data)
            self.__output_message(transformed_data)
            self._set_headers()
            self.wfile.write(bytes("Data successfully consumed", 'utf8'))
        except BaseException:
            self.send_error(400, 'Error when sending output message')
            logging.error('Error when sending output message')
            raise

    def __output_message(self, data: object):
        """Outputs the transformed payload to the specified HTTP endpoint

        Args:
          data: transformed json object to send to output writer
        """
        request = requests.post(self.output_url, data=json.dumps(data))
        if request.status_code != 200:

            logging.error("Error with a request %s and message not sent was %s",
                          request.status_code, data)
        else:
            logging.info("%s Response received from output writer",
                         request.status_code)


def run(args, server_class=HTTPServer, handler_class=Socket):
    """Run the server on specified host and port, using our
    custom Socket class to receive and process requests.
    """
    server_address = (args.host, int(args.port))
    handler_class.output_url = args.output_url
    handler_class.schema_filepath = args.schema_filepath
    httpd = server_class(server_address, handler_class)
    logging.info('Running server on host ${HOST} and port ${PORT}')
    httpd.serve_forever()


def cli():
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)

    # HOST & PORT are the values used to run the current application
    parser.add_argument('--host', default=os.getenv('HOST'))
    parser.add_argument('--port', default=os.getenv('PORT'))

    # OUTPUT_URL is the url which receives all the output messages after they are processed by the app
    parser.add_argument('--output_url', default=os.getenv('OUTPUT_URL'))

    # Filepath for the JSON schema which represents
    # the schema for the expected input messages to the app
    parser.add_argument('--schema_filepath', default=os.getenv('SCHEMA_FILEPATH'))

    args = parser.parse_args()

    run(args)


if __name__ == "__main__":
    cli()

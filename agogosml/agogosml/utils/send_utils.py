import requests
import logging
import json

logger = logging.getLogger("STREAM")
logger.setLevel(logging.INFO)


def send_message(message, app_host, app_port):
    """
    Sends messages to specified address via HTTP

    :param message:  json formatted message
    :param app_host: host of address
    :param app_port: port of address 
    """
    try:
        server_address = "http://" + app_host + ":" + app_port
        # TODO: Add retries as some of the messages are failing to send
        request = requests.post(server_address, data=json.dumps(message))
        if request.status_code != 200:
            logger.error(
                "Error with a request {} and message not sent was {}".
                format(request.status_code, message))
            print("Error with a request {} and message not sent was {}".
                  format(request.status_code, message))
            return False
        return True

    except Exception as e:
        logger.error('Failed to send request: ' + str(e))

    finally:
        return False

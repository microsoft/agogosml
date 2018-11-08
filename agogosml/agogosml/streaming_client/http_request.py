import requests
import logging

logger = logging.getLogger("STREAM")
logger.setLevel(logging.INFO)


def send_message(message, app_host, app_port):

    try:
        server_address = "http://" + app_host + ":" + app_port
        request = requests.post(server_address, data=message)
        if request.status_code != 200:
            logger.error(
              "Error with a request {} and message not sent was {}".
              format(request.status_code, message))
            return False
        return True

    except Exception as e:
        logger.error('Failed to send request: ' + str(e))

    finally:
        return False

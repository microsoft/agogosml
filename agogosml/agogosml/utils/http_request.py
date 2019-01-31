from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from urllib3 import Retry


def post_with_retries(url: str, data: dict, retries: int = 5, backoff: float = 1) -> int:
    """
    >>> post_with_retries('http://httpstat.us/503', {}, retries=1, backoff=0)
    500
    >>> post_with_retries('https://httpstat.us/200', {}, retries=1, backoff=0)
    200
    """
    retry_adapter = HTTPAdapter(max_retries=Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=frozenset(['POST'])
    ))

    with Session() as session:
        session.mount('http://', retry_adapter)
        session.mount('https://', retry_adapter)

        try:
            response = session.post(url, data=data)
        except RetryError:
            return 500

        return response.status_code

"""Storage streaming client"""
from datetime import datetime
from io import BytesIO
from uuid import uuid4

from libcloud.storage.base import Container
from libcloud.storage.providers import get_driver
from libcloud.storage.types import ContainerAlreadyExistsError
from libcloud.storage.types import Provider

from agogosml.common.abstract_streaming_client import AbstractStreamingClient
from agogosml.utils.logger import Logger


class StorageStreamingClient(AbstractStreamingClient):
    """Storage streaming client"""

    def __init__(self, config: dict):
        """
        Streaming client implementation that stores the events in a storage.

        Configuration keys:
          STORAGE_PROVIDER -- e.g. AZURE_BLOBS
          STORAGE_KEY -- the blob storage account name
          STORAGE_SECRET -- the blob storage access key
          STORAGE_CONTAINER
          TIMESLICE_FORMAT

        >>> import os
        >>> import shutil
        >>> import tempfile
        >>> storage_folder = tempfile.mkdtemp()
        >>> storage_container = 'some-container'
        >>> client = StorageStreamingClient({ \
            'STORAGE_PROVIDER': 'LOCAL', \
            'STORAGE_KEY': storage_folder, \
            'STORAGE_SECRET': '', \
            'STORAGE_CONTAINER': storage_container, \
        })
        >>> client.send('some-message')
        >>> len(os.listdir(os.path.join(storage_folder, storage_container)))
        1
        >>> shutil.rmtree(storage_folder)
        """

        provider = getattr(Provider, config.get('STORAGE_PROVIDER', 'AZURE_BLOBS'))
        driver_class = get_driver(provider)
        driver = driver_class(config['STORAGE_KEY'], config['STORAGE_SECRET'])

        self.logger = Logger()

        try:
            self.container: Container = driver.create_container(config['STORAGE_CONTAINER'])
            self.logger.info('Created container %s', config['STORAGE_CONTAINER'])
        except ContainerAlreadyExistsError:
            self.container: Container = driver.get_container(config['STORAGE_CONTAINER'])
            self.logger.debug('Using existing container %s', config['STORAGE_CONTAINER'])

        self.timeslice_format = config.get('TIMESLICE_FORMAT', '%Y/%m/%d/%H/%M/%S')

    def start_receiving(self, on_message_received_callback):
        self.logger.error('Unexpectedly called %s on %s',
                          self.start_receiving.__name__, self.__class__.__name__)

    def send(self, message):
        message_payload = BytesIO(message.encode('utf-8'))
        message_uid = str(uuid4())
        message_time = datetime.utcnow()
        message_folder = message_time.strftime(self.timeslice_format)
        message_path = '{}/{}'.format(message_folder, message_uid)
        self.container.upload_object_via_stream(message_payload, message_path)

    def stop(self):
        self.logger.error('Unexpectedly called %s on %s',
                          self.stop.__name__, self.__class__.__name__)

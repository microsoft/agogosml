""" Logger """
import os
import logging
import logging.config
from pathlib import Path

import yaml
from typing import Union
from applicationinsights import TelemetryClient
from applicationinsights.channel import AsynchronousQueue
from applicationinsights.channel import AsynchronousSender
from applicationinsights.channel import TelemetryChannel
from applicationinsights.channel import TelemetryContext
from cached_property import cached_property
from singleton_decorator import singleton


class NullTelemetryClient:
    def track_trace(self, name, properties=None, severity=None):
        pass


@singleton
class Logger(object):
    """A logger implementation."""

    def __init__(self,
                 name: str = __name__,
                 path: str = 'logging.yaml',
                 env_key: str = 'LOG_CFG',
                 level: int = logging.INFO):

        self.level = level
        self.name = name
        self.path = path
        self.env_key = env_key

    @cached_property
    def logger(self) -> logging.Logger:
        value = os.getenv(self.env_key)
        path = Path(value or self.path)

        if path.is_file():
            with path.open('rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=self.level)

        return logging.getLogger(self.name)

    @cached_property
    def telemetry_client(self) -> Union[TelemetryClient, NullTelemetryClient]:
        ikey = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')
        if not ikey:
            return NullTelemetryClient()

        sender = AsynchronousSender()
        queue = AsynchronousQueue(sender)
        context = TelemetryContext()
        context.instrumentation_key = ikey
        channel = TelemetryChannel(context, queue)
        return TelemetryClient(ikey, telemetry_channel=channel)

    def debug(self, message: str):
        """
        Log debug message.

        :param message: Debug message string.
        """
        self._log(logging.DEBUG, message)

    def info(self, message: str):
        """
        Log info message

        :param message: Info message string.
        """
        self._log(logging.INFO, message)

    def error(self, message: str):
        """
        Log error message

        :param message: Error message string.
        """
        self._log(logging.ERROR, message)

    def _log(self, level: int, message: str):
        if not self.logger.isEnabledFor(level):
            return

        self.logger.log(level, message)
        self.telemetry_client.track_trace(
            message, severity=logging.getLevelName(level))

import logging
import logging.config
import os
from pathlib import Path
from typing import Dict
from typing import Optional
from typing import Union

import yaml
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

    def track_event(self, name, properties=None, measurements=None):
        pass


@singleton
class Logger(object):
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
    def _logger(self) -> logging.Logger:
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
    def _telemetry(self) -> Union[TelemetryClient, NullTelemetryClient]:
        ikey = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')
        if not ikey:
            return NullTelemetryClient()

        sender = AsynchronousSender()
        queue = AsynchronousQueue(sender)
        context = TelemetryContext()
        context.instrumentation_key = ikey
        channel = TelemetryChannel(context, queue)
        return TelemetryClient(ikey, telemetry_channel=channel)

    def debug(self, message: str, *args):
        self._log(logging.DEBUG, message, *args)

    def info(self, message: str, *args):
        self._log(logging.INFO, message, *args)

    def error(self, message: str, *args):
        self._log(logging.ERROR, message, *args)

    def event(self, name: str, props: Optional[Dict[str, str]] = None):
        props = props or {}
        self._logger.info('Event %s: %r', name, props)
        self._telemetry.track_event(name, props)

    def _log(self, level: int, message: str, *args):
        if not self._logger.isEnabledFor(level):
            return

        self._logger.log(level, message, *args)
        self._telemetry.track_trace(
            message, severity=logging.getLevelName(level))

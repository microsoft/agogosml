""" Logger """
import logging.config
import os
from pathlib import Path

import yaml


class Logger(object):
    """A logger implementation."""

    __instance = None
    logger = None

    @staticmethod
    def setup_logging(log_path='logging.yaml',
                      level=logging.INFO,
                      env_key='LOG_CFG'):
        """Setup logging configuration."""

        value = os.getenv(env_key, None)
        if value:
            path = Path(value)
        else:
            path = Path(log_path)

        if path.is_file():
            with path.open('rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=level)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self,
                 name=__name__,
                 path='logging.yaml',
                 env_key='LOG_CFG',
                 level=logging.INFO):

        self.level = level
        self.name = name
        self.path = path
        self.env_key = env_key
        self.logger = None

        Logger.setup_logging(
            log_path=self.path, level=self.level, env_key=self.env_key)

        self.logger = logging.getLogger(self.name)

    def debug(self, message):
        """
        Log debug message.

        :param message: Debug message string.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Log info message

        :param message: Info message string.
        """
        self.logger.info(message)

    def error(self, message):
        """
        Log error message

        :param message: Error message string.
        """
        self.logger.error(message)

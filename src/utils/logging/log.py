import os
import logging.config
import yaml


def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class Logger(object):

    __instance = None

    def __new__(cls, name=__name__, level=logging.INFO):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
        Logger.__instance.level = level
        Logger.__instance.name = name
        return Logger.__instance

    def __init__(self):
        setup_logging(default_level=self.level or logging.INFO)
        self.logger = logging.getLogger(self.name)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

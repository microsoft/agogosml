import os
import logging.config
import yaml


def setup_logging(
    log_path='logging.yaml',
    level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = log_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level)


class Logger(object):

    __instance = None

    def __new__(cls, name=__name__, path='logging.yaml', env_key='LOG_CFG', level=logging.INFO):
        if Logger.__instance is None:
            Logger.__instance = object.__new__(cls)
        Logger.__instance.level = level
        Logger.__instance.name = name
        Logger.__instance.path = path
        Logger.__instance.env_key = env_key
        return Logger.__instance

    def __init__(self):
        setup_logging(
          log_path=self.path,
          level=self.level,
          env_key=self.env_key)
        self.logger = logging.getLogger(self.name)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
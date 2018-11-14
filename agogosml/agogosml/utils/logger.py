import os
import logging.config
import yaml

class Logger(object):

    __instance = None

    @staticmethod
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
            logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level)

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self, name=__name__, path='logging.yaml', env_key='LOG_CFG', level=logging.INFO):

        self.level = level
        self.name = name
        self.path = path
        self.env_key = env_key
        self.logger = None

        Logger.setup_logging(log_path=self.path, level=self.level, env_key=self.env_key)

        self.logger = logging.getLogger(self.name)

    @classmethod
    def info(self, message):
        self.logger.info(message)

    @classmethod
    def error(self, message):
        self.logger.error(message)
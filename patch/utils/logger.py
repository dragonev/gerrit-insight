import sys
import logging
from patch.utils.singleton import Singleton


class Logger(object):

    __metaclass__ = Singleton

    def __init__(self):
        pass

    def config_logger(self, log_name, log_path, log_level=logging.INFO):
        """
        log_name : Return a logger with the specified name.
        log_path : the place where log outputs.
        """
        self.log_name = log_name
        self.log_path = log_path
        self.log_level = log_level

        formatter = logging.Formatter(
            # fmt='%(asctime)s %(filename)s line:%(lineno)d %(levelname)s %(message)s',
            fmt='%(asctime)s %(levelname)s %(message)s',
            datefmt='%G-%m-%d %H:%M:%S')

        file_handler = logging.FileHandler(self.log_path)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger = logging.getLogger(self.log_name)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(self.log_level)

    def manage_logger(self):
        """
        Here we can manage the logs that server prints.
        """
        pass

    def get_logger(self):
        """
        Get a logger with the specified name.
        """
        return self.logger

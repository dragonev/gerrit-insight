import os
import time
from django.conf import settings
import patch.utils.logger as logger


class Logger(object):

    @staticmethod
    def init_logger(log_dir, log_name):
        """
        Configurate log parameters for current server.
        """
        log_path = os.path.join(log_dir, log_name)
        logger.Logger().config_logger(log_name, log_path)

    @staticmethod
    def d(msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        logger.Logger().get_logger().debug(msg, *args, **kwargs)

    @staticmethod
    def i(msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        logger.Logger().get_logger().info(msg, *args, **kwargs)

    @staticmethod
    def w(msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        logger.Logger().get_logger().warning(msg, *args, **kwargs)

    @staticmethod
    def e(msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        logger.Logger().get_logger().error(msg, *args, **kwargs)

    @staticmethod
    def c(msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        logger.Logger().get_logger().error(msg, *args, **kwargs)


class DateSet(object):

    @staticmethod
    def convert_second_to_date(second):
        """
        return date_format: "2016-05-05 20:28:54"
        """
        time_array = time.localtime(second)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

    @staticmethod
    def convert_date_to_second(date):
        """
        data format: "2016-05-05 20:28:54"
        """
        time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
        return time.mktime(time_array)

    @staticmethod
    def get_local_date():
        """
        get local date, format: "2016-05-05 20:28:54"
        """
        return convert_second_to_date(time.time())

    @staticmethod
    def get_local_second():
        """
        Return the current time in seconds since the Epoch.
        """
        return time.time()

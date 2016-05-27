u"""로거 객체 입니다."""
# -*- coding: utf-8 -*-
import logging
from logging import getLogger, handlers, Formatter


class Log:
    """docstring for."""

    __log_level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    __my_logger = None

    @staticmethod
    def init(logger_name='photolog',
             log_level='debug',
             log_filepath='photolog/resource/log/photolog.log'):
        """init."""
        Log.__my_logger = getLogger(logger_name)
        Log.__my_logger.setLevel(Log.__log_level_map.get(log_level, 'warn'))
        formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        Log.__my_logger.addHandler(console_handler)

        file_handler = handlers.TimeRotatingFileHandler(log_filepath,
                                                        when="D",
                                                        interval=1)
        file_handler.setFormatter(formatter)
        Log.__my_logger.addHandler(file_handler)

    @staticmethod
    def debug(msg):
        """hi."""
        Log.__my_logger.debug(msg)

    @staticmethod
    def info(msg):
        """hi."""
        Log.__my_logger.info(msg)

    @staticmethod
    def warn(msg):
        """hi."""
        Log.__my_logger.warn(msg)

    @staticmethod
    def error(msg):
        """hi."""
        Log.__my_logger.error(msg)

    @staticmethod
    def critical(msg):
        """hi."""
        Log.__my_logger.critical(msg)

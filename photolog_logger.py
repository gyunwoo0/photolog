u"""로거 객체 입니다."""
# -*- coding: utf-8 -*-
import logging
from logging import getLogger, handlers, Formatter


class Log:
    """docstring for """
    __log_level_map = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    __my_logger = None

    @staticmethod
    def __init__(logger_name='photolog',
                 log_level='debug',
                 log_filepath='photolog/resource/log/photolog.log'):
        Log.__my_logger = getLogger(logger_name)
        Log.__my_logger.setLevel(Log.__log_level_map.get(log_level, warn))
        formatter = Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        Log.__my_logger.addHandler(console_handler)

        file_handler = handlers.TimeRotatingFileHandler(log_filepath,
                                                        when="D",
                                                        interval=1)
        file_handler.setFormatter(formatter)
        Log.__my_logger.addHandler(file_handler)

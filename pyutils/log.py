import logging
import sys
from logging import handlers


class Logger(object):

    def __init__(
            self, file_name='log.log',
            # file_size 单位: MB
            file_size=50,
            file_count=5,
            time_fmt='%Y-%m-%d %H:%M:%S',
            log_fmt='%(asctime)s [%(filename)s %(lineno)d] %(levelname)s %(message)s',
            log_level=logging.INFO,
            # output_type[0]: 输出到文件, output_type[1]: 输出到控制台
            output_type=(True, True)):
        self._logger = logging.getLogger()
        if output_type[0] or output_type[1]:
            self.formatter = logging.Formatter(log_fmt, time_fmt)
        if output_type[0]:
            file_size = file_size * 1024 * 1024
            file_header = self._get_file_handler(
                file_name, file_size, file_count)
            self._logger.addHandler(file_header)
        if output_type[1]:
            console_handler = self._get_console_handler()
            self._logger.addHandler(console_handler)
        self._logger.setLevel(log_level)

    def _get_file_handler(self, file_name, file_size, file_count):
        fh = handlers.RotatingFileHandler(
            filename=file_name,
            maxBytes=file_size,
            backupCount=file_count,
            encoding='utf-8')
        fh.setFormatter(self.formatter)
        return fh

    def _get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    @property
    def logger(self):
        return self._logger

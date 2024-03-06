'''
    Logging utilities
'''
import os
import logging

from utils.consts import DFT_LOGGER


class LogMixin(object):
    '''
        Mixin to embed logging logic into class.
        Can log into root logger or have its own logger with dedicated file handler.
    '''
    def __init__(self, logger_name: str = DFT_LOGGER, **kwargs):
        super().__init__()
        self.log = self.create_logger(logger_name)

    def create_logger(self, name: str):
        '''
            Create dedicated class logger or use the root logger
        '''
        from bootstrap import Container

        log = logging.getLogger()
        if name == DFT_LOGGER:
            return log

        filepath = os.path.dirname(Container.config.logging.filename())
        filename = os.path.join(filepath, f'{name}.log')
        handler = logging.FileHandler(filename, mode=Container.config.logging.filemode)
        formatter = logging.Formatter(Container.config.logging.format, datefmt=Container.config.logging.datefmt)
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        log = logging.Logger(name)
        log.setLevel(logging.INFO)
        log.addHandler(handler)

        return log

    @property
    def log_filename(self):
        file_handlers = list(filter(lambda h: isinstance(h, logging.FileHandler), self.log.handlers))
        if len(file_handlers) > 0:
            file_handler: logging.FileHandler = file_handlers[0]
            return file_handler.baseFilename

        return None

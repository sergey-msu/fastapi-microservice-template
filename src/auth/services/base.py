'''
    Base service class
'''
from utils.logging import LogMixin


class ServiceBase(LogMixin):
    '''
        Base service class
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

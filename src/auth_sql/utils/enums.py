'''
    Custom enums
'''
import enum


class AuthTokenLocation(enum.Enum):
    COOKIES = 'cookies'
    HEADER = 'header'

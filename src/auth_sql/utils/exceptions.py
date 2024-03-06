'''
    App-wide exceptions
'''
from starlette.exceptions import HTTPException
from fastapi import status


class AppException(HTTPException):
    status_code = 500
    detail = 'Critical server error'

    def __init__(self, msg=None):
        super().__init__(status_code=self.status_code, detail=msg or self.detail)


class InvalidCredentialsError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Could not validate credentials'
    headers = {'WWW-Authenticate': 'Bearer'}


class CredentialsNotFoundError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'No auth token found'
    headers = {'WWW-Authenticate': 'Bearer'}


class InvalidPayloadError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Invalid payload'


class WrongRefreshTokenError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Refresh token wrong or not found'


class InvalidRefreshTokenIdError(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid refresh token'

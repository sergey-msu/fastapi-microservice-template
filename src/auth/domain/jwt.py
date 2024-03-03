'''
    JWT core functions
'''
from datetime import datetime as dt
from datetime import timedelta

from jose import JWTError
from jose import jwt

from utils.exceptions import InvalidCredentialsError


class JWT:
    '''
        JWT core functions
    '''
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key: str = secret_key
        self.algorithm: str = algorithm

    def create_token(self, payload: str, expire_min: int) -> str:
        '''
            Create JWT token
        '''
        now = dt.utcnow()
        body = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(minutes=expire_min),
            'sub': payload,
        }
        token = jwt.encode(body, self.secret_key, algorithm=self.algorithm)

        return token

    def validate_token(self, token: str) -> str:
        '''
            Validate access token, returns payload if valid
        '''
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload.get('sub')
        except JWTError as err:
            raise InvalidCredentialsError(msg=str(err))

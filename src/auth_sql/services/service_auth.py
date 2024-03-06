'''
    Authentication service
'''
from fastapi import Request
from fastapi import Response

from utils.enums import AuthTokenLocation
from utils.exceptions import InvalidPayloadError
from utils.exceptions import WrongRefreshTokenError
from utils.exceptions import CredentialsNotFoundError
from services.base import ServiceBase
from domain.jwt import JWT
from data.repositories import Repository
import models


class AuthService(ServiceBase):
    '''
        Authentication service
    '''
    def __init__(
        self,
        jwt: JWT,
        repository: Repository,
        expire_min: int,
        refresh_min: int,
        token_name: str,
        token_location: str,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.jwt = jwt
        self.repository = repository
        self.expire_min = expire_min
        self.refresh_min = refresh_min
        self.token_name = token_name
        self.token_location = AuthTokenLocation(token_location)

    async def create_token(self, user_id: str) -> models.TokenCreated:
        '''
            Create access and refresh tokens
        '''
        access_token = self.jwt.create_token(payload=user_id, expire_min=self.expire_min)
        refresh_token = self.jwt.create_token(payload=user_id, expire_min=self.refresh_min)

        token_model = models.TokenCreating(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        result = await self.repository.tokens.add_one(token_model)

        token_id = result['id']
        self.log.info(f'new token {token_id} created for user_id={user_id}')

        return models.TokenCreated(
            id=token_id,
            **token_model.model_dump()
        )

    async def validate_token(self, token: str) -> str:
        '''
            Validate JWT token, returns payload if valid
        '''
        return self.jwt.validate_token(token)

    async def invalidate_token(self, user_id: str):
        '''
            Invalidate refresh token
        '''
        await self.repository.tokens.remove_refresh_token(user_id=user_id)

    async def refresh_access_token(self, refresh_token: str) -> models.TokenCreated:
        '''
            Refresh access token via refresh token
        '''
        user_id = self.jwt.validate_token(refresh_token)
        if user_id is None:
            raise InvalidPayloadError

        old_refresh_token = await self.repository.tokens.get_refresh_token(user_id=user_id)
        if refresh_token != old_refresh_token:
            raise WrongRefreshTokenError

        return await self.create_token(user_id)

    async def get_access_token(self, request: Request) -> str:
        '''
            Extract access token from cookies/headers/etc.
        '''
        token = None

        match self.token_location:
            case AuthTokenLocation.COOKIES:
                token = request.cookies.get(self.token_name)
            case AuthTokenLocation.HEADER:
                auth_header = request.headers.get('Authorization')
                if auth_header:
                    token = auth_header.split(' ')[1]

        if not token:
            raise CredentialsNotFoundError

        return token

    async def set_access_token(self, access_token: str, response: Response):
        '''
            Set access token to cookies/headers/etc.
        '''
        match self.token_location:
            case AuthTokenLocation.COOKIES:
                response.set_cookie(self.token_name, access_token, httponly=True)
            case AuthTokenLocation.HEADER:
                response.headers['Authorization'] = f'Bearer {access_token}'

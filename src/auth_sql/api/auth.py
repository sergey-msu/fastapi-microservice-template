'''
    User API endpoints
'''
from fastapi import APIRouter
from fastapi import Request
from fastapi import Response
from fastapi_versioning import version
from dependency_injector.wiring import inject

from services import AuthService
from bootstrap import Container
from bootstrap import resolve
import models


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@version(1)
@router.post('/token', response_model=models.TokenCreated)
@inject
async def token(
    user_id: str,
    response: Response,
    service_auth: AuthService = resolve(Container.service_auth)
):
    ''' Issue new auth tokens '''
    token = await service_auth.create_token(user_id)
    await service_auth.set_access_token(token.access_token, response)
    return token


@version(1)
@router.post('/validate', response_model=models.Result)
@inject
async def validate(
    request: Request,
    service_auth: AuthService = resolve(Container.service_auth)
):
    ''' Validate access token '''
    token = await service_auth.get_access_token(request)
    result = await service_auth.validate_token(token)
    return models.Result(value=result)


@version(1)
@router.post('/refresh', response_model=models.TokenCreated)
@inject
async def refresh(
    refresh_token: str,
    response: Response,
    service_auth: AuthService = resolve(Container.service_auth)
):
    ''' Refresh access token '''
    token = await service_auth.refresh_access_token(refresh_token)
    await service_auth.set_access_token(token.access_token, response)
    return token


@version(1)
@router.post('/invalidate', response_model=models.Result)
@inject
async def invalidate(
    user_id: str,
    service_auth: AuthService = resolve(Container.service_auth)
):
    ''' Invalidate access and refresh token '''
    await service_auth.invalidate_token(user_id)
    return models.OK

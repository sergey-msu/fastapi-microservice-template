'''
    User API endpoints
'''
from fastapi import APIRouter
from fastapi import Request
from fastapi import Response
from fastapi_versioning import version
from dependency_injector.wiring import inject

from utils.decorators import auth
from bootstrap import Container
from bootstrap import resolve
from services import UsersService
import models


router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@version(1)
@router.post('/login', response_model=models.UserLogged)
@inject
async def login(
    response: Response,
    user_data: models.UserAuth,
    service_users: UsersService = resolve(Container.service_users),
):
    ''' Sign in into app '''
    return await service_users.login(user_data, response)


@version(1)
@router.post('/register', response_model=models.UserCreated)
@inject
async def register(
    user_data: models.UserAuth,
    service_users: UsersService = resolve(Container.service_users),
):
    ''' Sign in into app '''
    return await service_users.register(user_data)


@version(1)
@router.post('/logout', response_model=models.Result)
@auth()
@inject
async def sign_out(
    request: Request,
    response: Response,
    service_users: UsersService = resolve(Container.service_users),
):
    ''' Sign out from the app. Auth needed. '''
    user_id = await service_users.get_current_userid(request)
    await service_users.logout(user_id, response)

    return models.OK


@version(1)
@router.post('/personal', response_model=models.Result)
@auth()
@inject
async def sign_out(
    request: Request,
    response: Response,
    service_users: UsersService = resolve(Container.service_users),
):
    ''' Returns some personal users info. Auth needed. '''

    return models.OK

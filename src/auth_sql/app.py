'''
    FastAPI app entry point
'''
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from dotenv import load_dotenv

# load env vars from .env file
load_dotenv()

from utils.middlewares import app_exception_handler # noqa E402
from api import auth # noqa E402
from bootstrap import Container # noqa E402


def create_app() -> FastAPI:
    # create app DI container
    container = Container.instance()

    # setup 3-rd parties logging
    for name in logging.Logger.manager.loggerDict.keys():
        if name not in ['fastapi', 'uvicorn.error']:
            logging.getLogger(name).setLevel(logging.WARNING)

    # create API app
    app = FastAPI(**container.config.app())

    # routers
    app.include_router(auth.router)

    # versioning
    app = VersionedFastAPI(
        app,
        version_format='{major}',
        prefix_format='/api/v{major}',
    )

    # errors handling
    app.add_exception_handler(Exception, app_exception_handler)

    # middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=container.config.server.cors(),
        allow_credentials=True,
        allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
        allow_headers=[
            'Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
            'Access-Control-Allow-Origin', 'Authorization'],
    )

    app.container = container

    return app


app = create_app()


@app.on_event('startup')
async def before_startup():
    ''' App startup callback '''
    logging.getLogger().info('application started')


@app.on_event('shutdown')
async def after_shutdown():
    ''' App shutdown callback '''
    logging.getLogger().info('application finished')

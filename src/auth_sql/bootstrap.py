'''
    Application DI container
'''
import os
import threading
from typing_extensions import Self
from logging import basicConfig

from dependency_injector import containers
from dependency_injector import providers
from dependency_injector.wiring import Provide
from fastapi import Depends

from utils.consts import MODE_ENV_VAR
from data import repositories
from domain.jwt import JWT
import services


class Container(containers.DeclarativeContainer):
    '''
        Application DI container
    '''

    # Configuration

    app_mode = os.environ[MODE_ENV_VAR].lower()
    config = providers.Configuration(yaml_files=['./config.yaml', f'./config.{app_mode}.yaml'], strict=True)

    # Logging

    logging = providers.Resource(
        basicConfig,
        filename=config.logging.filename,
        filemode=config.logging.filemode,
        format=config.logging.format,
        datefmt=config.logging.datefmt,
        level=config.logging.level,
    )

    # Data

    repository_tokens = providers.Factory(
        repositories.TokensRepository,
        url=config.data.db.url,
        echo=config.data.db.echo,
    )

    # other repos ...

    repository = providers.Factory(
        repositories.Repository,
        tokens=repository_tokens,
        # other repos ...
    )

    # Domain

    jwt = providers.Singleton(
        JWT,
        secret_key=config.services.auth.secret_key,
        algorithm=config.services.auth.algorithm,
    )

    # Services

    service_auth = providers.Factory(
        services.AuthService,
        jwt=jwt,
        repository=repository,
        expire_min=config.services.auth.expire_min,
        refresh_min=config.services.auth.refresh_min,
        algorithm=config.services.auth.algorithm,
        token_name=config.services.auth.token_name,
        token_location=config.services.auth.token_location,
    )

    # .init

    __lock = threading.Lock()
    __instance: Self = None

    @classmethod
    def instance(cls):
        with cls.__lock:
            if cls.__instance is None:
                container = Container()
                container.init_resources()
                container.wire(
                    modules=[__name__],
                    packages=['api']
                )

                cls.__instance = container
        return cls.__instance


def resolve(instance):
    return Depends(Provide[instance])

from typing import List

import aiohttp

from application.dependencies.interface import AsyncInitialization, RPCMethod
from application.dependencies.utils import session_maker
from application.repositories.jwt_auth.dependencies import DependenciesGetUserId
from application.repositories.jwt_auth.tokenaizer import TokenizerRepository
from application.repositories.vk_client.models import ApiVkConfig
from application.repositories.vk_client.repository import VkClientApi
from application.usecases.check_token_backend import BackendValidatorTokenUseCase
from application.usecases.generate_token_backend import BackendGeneratorTokenUseCase
from application.usecases.profile_logics import BackendProfileViewUseCase
from application.usecases.refresh_token_backend import BackendRefreshTokenUseCase
from runner.configs import config
from runner.routes.service import ServiceEntrypoint


class ApplicationDependenciesContainer(AsyncInitialization, RPCMethod, object):
    def __init__(self):
        self.__rpc_methods: List[RPCMethod] = []

    def add_route(self, route: RPCMethod):
        self.__rpc_methods.append(route)

    @property
    def methods(self) -> list:
        all_methods = []
        for route in self.__rpc_methods:
            all_methods += route.methods
        return all_methods

    @classmethod
    async def create(cls):
        self = ApplicationDependenciesContainer()
        aio = await session_maker()
        transport = aiohttp.ClientSession(connector=aio, headers={"Content-Type": "application/json"})
        jwt_repository = TokenizerRepository(
            secret_key_access=config.access_secret, secret_key_refresh=config.refresh_secret
        )
        vk_client_config = ApiVkConfig(client_id=config.vk_client_id, client_secret=config.vk_client_secret)
        vk_client = VkClientApi(transport=transport, config=vk_client_config)
        uc_generator_token_backend = BackendGeneratorTokenUseCase(
            jwt_repo=jwt_repository,
            vk_client=vk_client,
        )
        uc_refresh_token_backend = BackendRefreshTokenUseCase(
            jwt_repo=jwt_repository,
        )
        dp_validate_token_backend = DependenciesGetUserId(
            uc=BackendValidatorTokenUseCase(
                jwt_repo=jwt_repository,
            )
        )
        uc_profile_view_sync = BackendProfileViewUseCase(
            jwt_repo=jwt_repository,
            vk_client=vk_client,
        )
        service_entrypoint = ServiceEntrypoint(
            uc_generate=uc_generator_token_backend,
            uc_refresh=uc_refresh_token_backend,
            uc_view_profile=uc_profile_view_sync,
            dp=dp_validate_token_backend,
        )
        self.add_route(route=service_entrypoint)
        return self
